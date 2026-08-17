"""Persistencia en SQLite: deduplicación de eventos, hilos y cola de borradores.

SQLite y no Postgres a propósito: esto corre en un contenedor chico y el volumen
son decenas de mensajes al día, no miles por segundo.
"""
import time
from pathlib import Path
from typing import Any

import aiosqlite

ESQUEMA = """
CREATE TABLE IF NOT EXISTS eventos_vistos (
    evento_id TEXT PRIMARY KEY,
    visto_en  INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS turnos (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    autor_id       TEXT NOT NULL,
    rol            TEXT NOT NULL,          -- 'contacto' | 'yo'
    texto          TEXT NOT NULL,
    automatico     INTEGER NOT NULL DEFAULT 0,
    creado_en      INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_turnos_autor ON turnos (autor_id, creado_en);

CREATE TABLE IF NOT EXISTS borradores (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    evento_id       TEXT NOT NULL UNIQUE,
    autor_id        TEXT NOT NULL,
    autor_usuario   TEXT,
    tipo            TEXT NOT NULL,
    texto_entrante  TEXT NOT NULL,
    respuesta       TEXT NOT NULL,
    categoria       TEXT NOT NULL,
    confianza       REAL NOT NULL,
    razon           TEXT NOT NULL,
    prioridad       TEXT NOT NULL DEFAULT 'normal',
    estado          TEXT NOT NULL DEFAULT 'pendiente',
    comentario_id   TEXT,
    creado_en       TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_borradores_estado ON borradores (estado, id);
"""

_UN_DIA_MS = 24 * 60 * 60 * 1000


class Almacen:
    def __init__(self, ruta: str):
        self.ruta = ruta
        Path(ruta).parent.mkdir(parents=True, exist_ok=True)

    async def iniciar(self) -> None:
        async with aiosqlite.connect(self.ruta) as db:
            await db.executescript(ESQUEMA)
            await db.commit()

    # --- Deduplicación ---------------------------------------------------

    async def evento_nuevo(self, evento_id: str) -> bool:
        """True si es la primera vez que vemos este evento.

        Meta reintenta los webhooks que no responden 200 rápido, así que el
        mismo mensaje llega varias veces. Sin esto, respondes tres veces.
        """
        async with aiosqlite.connect(self.ruta) as db:
            try:
                await db.execute("INSERT INTO eventos_vistos (evento_id, visto_en) VALUES (?, ?)",
                                 (evento_id, int(time.time() * 1000)))
                await db.commit()
                return True
            except aiosqlite.IntegrityError:
                return False

    # --- Hilos -----------------------------------------------------------

    async def registrar_turno(self, autor_id: str, rol: str, texto: str,
                              automatico: bool = False) -> None:
        async with aiosqlite.connect(self.ruta) as db:
            await db.execute(
                "INSERT INTO turnos (autor_id, rol, texto, automatico, creado_en) "
                "VALUES (?, ?, ?, ?, ?)",
                (autor_id, rol, texto, int(automatico), int(time.time() * 1000)))
            await db.commit()

    async def historial(self, autor_id: str, limite: int = 10) -> list[dict[str, Any]]:
        async with aiosqlite.connect(self.ruta) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute(
                "SELECT rol, texto, creado_en FROM turnos WHERE autor_id = ? "
                "ORDER BY creado_en DESC LIMIT ?", (autor_id, limite))
            filas = await cur.fetchall()
        return [dict(f) for f in reversed(filas)]

    async def estado_contacto(self, autor_id: str, ventana_horas: int) -> dict[str, Any]:
        """Datos que necesita `politica.Contexto` para decidir."""
        ahora = int(time.time() * 1000)
        async with aiosqlite.connect(self.ruta) as db:
            db.row_factory = aiosqlite.Row

            cur = await db.execute(
                "SELECT COUNT(*) AS n FROM turnos "
                "WHERE autor_id = ? AND rol = 'yo' AND automatico = 1 AND creado_en >= ?",
                (autor_id, ahora - _UN_DIA_MS))
            autorespuestas_hoy = (await cur.fetchone())["n"]

            cur = await db.execute(
                "SELECT rol FROM turnos WHERE autor_id = ? ORDER BY creado_en DESC LIMIT 1",
                (autor_id,))
            fila = await cur.fetchone()
            ultimo_rol = fila["rol"] if fila else None

            cur = await db.execute(
                "SELECT MAX(creado_en) AS t FROM turnos WHERE autor_id = ? AND rol = 'contacto'",
                (autor_id,))
            ultimo_del_contacto = (await cur.fetchone())["t"]

            cur = await db.execute("SELECT COUNT(*) AS n FROM turnos WHERE autor_id = ?",
                                   (autor_id,))
            total_turnos = (await cur.fetchone())["n"]

        dentro = (ultimo_del_contacto is not None
                  and ahora - ultimo_del_contacto <= ventana_horas * 60 * 60 * 1000)

        return {
            "autorespuestas_hoy": autorespuestas_hoy,
            "ultimo_turno_fue_mio": ultimo_rol == "yo",
            "dentro_de_ventana": dentro,
            "es_primer_contacto": total_turnos <= 1,
        }

    # --- Borradores ------------------------------------------------------

    async def guardar_borrador(self, **campos: Any) -> int:
        columnas = ", ".join(campos)
        marcas = ", ".join("?" for _ in campos)
        async with aiosqlite.connect(self.ruta) as db:
            cur = await db.execute(
                f"INSERT OR REPLACE INTO borradores ({columnas}) VALUES ({marcas})",
                tuple(campos.values()))
            await db.commit()
            return cur.lastrowid or 0

    async def pendientes(self, limite: int = 50) -> list[dict[str, Any]]:
        async with aiosqlite.connect(self.ruta) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute(
                "SELECT * FROM borradores WHERE estado = 'pendiente' "
                "ORDER BY CASE prioridad WHEN 'alta' THEN 0 ELSE 1 END, id DESC LIMIT ?",
                (limite,))
            return [dict(f) for f in await cur.fetchall()]

    async def borrador(self, borrador_id: int) -> dict[str, Any] | None:
        async with aiosqlite.connect(self.ruta) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM borradores WHERE id = ?", (borrador_id,))
            fila = await cur.fetchone()
        return dict(fila) if fila else None

    async def marcar_borrador(self, borrador_id: int, estado: str,
                              respuesta: str | None = None) -> None:
        async with aiosqlite.connect(self.ruta) as db:
            if respuesta is None:
                await db.execute("UPDATE borradores SET estado = ? WHERE id = ?",
                                 (estado, borrador_id))
            else:
                await db.execute("UPDATE borradores SET estado = ?, respuesta = ? WHERE id = ?",
                                 (estado, respuesta, borrador_id))
            await db.commit()
