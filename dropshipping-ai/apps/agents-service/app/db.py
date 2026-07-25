"""Pool de conexiones Postgres y helpers de auditoría."""
import json
from typing import Any

import asyncpg

from .config import settings

_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(settings.database_url, min_size=2, max_size=10)
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


async def audit(agente: str, accion: str, entidad: str | None = None,
                entidad_id: str | None = None, detalle: dict[str, Any] | None = None) -> None:
    """Toda acción de agente queda en agent_actions — base de las garantías legales."""
    pool = await get_pool()
    await pool.execute(
        """INSERT INTO agent_actions (agente, accion, entidad, entidad_id, detalle)
           VALUES ($1, $2, $3, $4, $5::jsonb)""",
        agente, accion, entidad, entidad_id, json.dumps(detalle or {}),
    )
