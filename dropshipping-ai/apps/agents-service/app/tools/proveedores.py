"""Conector a proveedores: verificación de stock en milisegundos (promesa a).

Dos modos según el proveedor:
  - api:      GET al endpoint del proveedor (httpx, timeout agresivo)
  - scraping: descarga la página del producto y extrae el stock con un selector CSS

Capa de caché Redis (TTL corto) para responder en <5 ms cuando el mismo
producto se consulta repetidamente durante un pico de ventas.
"""
import json
import time
from dataclasses import dataclass
from uuid import UUID

import httpx
import redis.asyncio as aioredis
from bs4 import BeautifulSoup

from ..config import settings
from ..db import audit, get_pool

_redis: aioredis.Redis | None = None


def get_redis() -> aioredis.Redis:
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    return _redis


@dataclass
class ResultadoStock:
    en_stock: bool
    cantidad: int | None
    latencia_ms: int
    fuente: str                 # 'api' | 'scraping' | 'cache'
    stock_check_id: int | None


async def _consultar_api(base_url: str, sku: str, api_key_ref: str | None) -> tuple[bool, int | None]:
    headers = {"Authorization": f"Bearer {api_key_ref}"} if api_key_ref else {}
    async with httpx.AsyncClient(timeout=3.0) as client:
        resp = await client.get(f"{base_url}/stock/{sku}", headers=headers)
        resp.raise_for_status()
        data = resp.json()
    return bool(data.get("in_stock")), data.get("quantity")


async def _consultar_scraping(url_producto: str, selector: str | None) -> tuple[bool, int | None]:
    async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
        resp = await client.get(url_producto)
        resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    nodo = soup.select_one(selector) if selector else None
    if nodo is None:
        # heurística de respaldo: buscar señales típicas de agotado
        texto = soup.get_text(" ", strip=True).lower()
        agotado = any(s in texto for s in ("agotado", "sin stock", "out of stock", "no disponible"))
        return (not agotado), None
    texto = nodo.get_text(strip=True).lower()
    digitos = "".join(c for c in texto if c.isdigit())
    cantidad = int(digitos) if digitos else None
    en_stock = (cantidad or 0) > 0 or "disponible" in texto or "in stock" in texto
    return en_stock, cantidad


async def verificar_stock(product_id: UUID, cantidad_pedida: int = 1) -> ResultadoStock:
    """Verifica stock contra el proveedor, registra el check y devuelve el resultado."""
    cache_key = f"stock:{product_id}"
    r = get_redis()

    t0 = time.perf_counter()
    cached = await r.get(cache_key)
    if cached:
        data = json.loads(cached)
        return ResultadoStock(
            en_stock=data["en_stock"] and (data["cantidad"] is None or data["cantidad"] >= cantidad_pedida),
            cantidad=data["cantidad"],
            latencia_ms=int((time.perf_counter() - t0) * 1000),
            fuente="cache",
            stock_check_id=None,
        )

    pool = await get_pool()
    row = await pool.fetchrow(
        """SELECT p.sku, p.url_proveedor, s.id AS supplier_id, s.modo, s.base_url,
                  s.api_key_ref, s.selector_stock
           FROM products p JOIN suppliers s ON s.id = p.supplier_id
           WHERE p.id = $1 AND p.activo AND s.activo""",
        product_id,
    )
    if row is None:
        raise ValueError(f"Producto {product_id} no existe o está inactivo")

    if row["modo"] == "api":
        en_stock, cantidad = await _consultar_api(row["base_url"], row["sku"], row["api_key_ref"])
    else:
        en_stock, cantidad = await _consultar_scraping(row["url_proveedor"], row["selector_stock"])

    latencia_ms = int((time.perf_counter() - t0) * 1000)

    check_id = await pool.fetchval(
        """INSERT INTO stock_checks (product_id, supplier_id, en_stock, cantidad, latencia_ms, fuente)
           VALUES ($1, $2, $3, $4, $5, $6) RETURNING id""",
        product_id, row["supplier_id"], en_stock, cantidad, latencia_ms, row["modo"],
    )
    await r.set(cache_key, json.dumps({"en_stock": en_stock, "cantidad": cantidad}),
                ex=settings.stock_cache_ttl_seg)
    await audit("back_office", "stock_verificado", "products", str(product_id),
                {"en_stock": en_stock, "cantidad": cantidad, "latencia_ms": latencia_ms})

    disponible = en_stock and (cantidad is None or cantidad >= cantidad_pedida)
    return ResultadoStock(disponible, cantidad, latencia_ms, row["modo"], check_id)
