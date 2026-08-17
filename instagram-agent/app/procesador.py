"""El recorrido completo de un evento: deduplicar → clasificar → decidir → actuar."""
import logging
from datetime import datetime, timezone

from . import politica
from .almacen import Almacen
from .config import settings
from .esquemas import EventoEntrante
from .instagram import ClienteInstagram, ErrorInstagram
from .redactor import clasificar_y_redactar

log = logging.getLogger(__name__)


class Procesador:
    def __init__(self, almacen: Almacen, cliente: ClienteInstagram | None = None):
        self.almacen = almacen
        self.instagram = cliente or ClienteInstagram()

    async def procesar(self, evento: EventoEntrante) -> politica.Decision:
        if not await self.almacen.evento_nuevo(evento.id):
            return politica.Decision("ignorar", "evento duplicado (reintento de Meta)")

        await self.almacen.registrar_turno(
            evento.autor_id, "contacto", evento.texto or f"({evento.contexto})")

        historial = await self.almacen.historial(evento.autor_id, limite=10)
        clas = await clasificar_y_redactar(evento, historial[:-1])

        estado = await self.almacen.estado_contacto(
            evento.autor_id, settings.ventana_respuesta_horas)
        # La ventana de 24 h aplica a DMs. Un comentario público se puede
        # responder cuando sea.
        if evento.tipo == "comentario":
            estado["dentro_de_ventana"] = True
            estado["es_primer_contacto"] = False

        decision = politica.decidir(
            clas, politica.Contexto(**estado),
            auto_categorias=settings.auto_categorias_set,
            confianza_minima=settings.auto_confianza_minima,
            max_por_contacto_dia=settings.auto_max_por_contacto_dia,
            max_caracteres=settings.auto_max_caracteres,
            solo_borradores=settings.modo_solo_borradores,
        )

        if decision.envia:
            try:
                await self._enviar(evento, decision.respuesta)
                await self.almacen.registrar_turno(
                    evento.autor_id, "yo", decision.respuesta, automatico=True)
                log.info("Respondido automáticamente a %s (%s)",
                         evento.autor_id, clas.categoria)
                return decision
            except ErrorInstagram as exc:
                log.warning("Envío falló, pasa a borrador: %s", exc)
                decision = politica.Decision(
                    "borrador", f"el envío falló: {exc}", decision.respuesta,
                    prioridad="alta")

        if decision.accion == "borrador":
            await self._guardar_borrador(evento, clas, decision)

        return decision

    async def _enviar(self, evento: EventoEntrante, texto: str) -> None:
        if evento.tipo == "comentario" and evento.comentario_id:
            await self.instagram.responder_comentario(evento.comentario_id, texto)
        else:
            await self.instagram.enviar_dm(evento.autor_id, texto)

    async def _guardar_borrador(self, evento: EventoEntrante,
                                clas: politica.Clasificacion,
                                decision: politica.Decision) -> int:
        return await self.almacen.guardar_borrador(
            evento_id=evento.id,
            autor_id=evento.autor_id,
            autor_usuario=evento.autor_usuario,
            tipo=evento.tipo,
            texto_entrante=evento.texto or f"({evento.contexto})",
            respuesta=decision.respuesta,
            categoria=clas.categoria,
            confianza=clas.confianza,
            razon=decision.razon,
            prioridad=decision.prioridad,
            estado="pendiente",
            comentario_id=evento.comentario_id,
            creado_en=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )

    async def enviar_borrador(self, borrador_id: int, texto: str | None = None) -> dict:
        """Envía un borrador aprobado desde el panel (con o sin ediciones tuyas)."""
        borrador = await self.almacen.borrador(borrador_id)
        if not borrador:
            raise ValueError(f"borrador {borrador_id} no existe")
        if borrador["estado"] != "pendiente":
            raise ValueError(f"borrador {borrador_id} ya está '{borrador['estado']}'")

        final = (texto or borrador["respuesta"]).strip()
        if not final:
            raise ValueError("no se puede enviar una respuesta vacía")

        if borrador["tipo"] == "comentario" and borrador["comentario_id"]:
            await self.instagram.responder_comentario(borrador["comentario_id"], final)
        else:
            await self.instagram.enviar_dm(borrador["autor_id"], final)

        await self.almacen.registrar_turno(borrador["autor_id"], "yo", final,
                                           automatico=False)
        await self.almacen.marcar_borrador(borrador_id, "enviado", final)
        return {"id": borrador_id, "estado": "enviado", "respuesta": final}
