from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración del servicio de agentes. Todo viene de variables de entorno."""

    database_url: str = "postgresql://dropship:dropship@localhost:5432/dropship"
    redis_url: str = "redis://localhost:6379/0"
    anthropic_api_key: str = ""
    model: str = "claude-sonnet-5"

    # Umbrales de autonomía: bajo estos valores el Agente B2B decide solo;
    # sobre ellos, genera una Sugerencia y espera al Supervisor.
    umbral_margen_pct: float = 35.0        # cambios de margen sobre esto requieren aprobación
    umbral_costo_oc: float = 200_000.0     # OC sobre este monto (CLP) requieren aprobación
    stock_cache_ttl_seg: int = 30          # caché Redis de verificaciones de stock

    class Config:
        env_prefix = "AGENTS_"


settings = Settings()
