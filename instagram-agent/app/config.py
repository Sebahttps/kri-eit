"""Configuración del agente de Instagram. Todo viene de variables de entorno."""
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    # --- Credenciales de Meta ---
    app_secret: str = ""               # App Secret de la app de Meta (firma los webhooks)
    verify_token: str = ""             # token que tú inventas y repites en el panel de Meta
    access_token: str = ""             # token de larga duración de la cuenta profesional
    ig_user_id: str = ""               # IGSID de tu propia cuenta (para ignorar tus ecos)

    # --- Graph API ---
    graph_base: str = "https://graph.instagram.com"   # Instagram Login
    graph_version: str = "v23.0"

    # --- Modelo ---
    anthropic_api_key: str = ""
    model: str = "claude-opus-5"
    effort: str = "low"                # respuestas de DM: prioridad latencia

    # --- Política de autonomía ---
    # Categorías que el agente puede responder solo. El resto queda en borrador.
    auto_categorias: str = "reaccion_trivial,cumplido,saludo_conocido"
    auto_confianza_minima: float = 0.80   # bajo esto, siempre borrador
    auto_max_por_contacto_dia: int = 3    # tope de respuestas automáticas por persona/día
    auto_max_caracteres: int = 140        # si el borrador sale largo, no es trivial → revisar
    modo_solo_borradores: bool = False    # interruptor de pánico: apaga todo el envío automático

    # --- Infra ---
    db_path: str = str(BASE_DIR.parent / "datos" / "instagram.db")
    persona_path: str = str(BASE_DIR / "persona.md")
    panel_token: str = ""              # protege /panel y /borradores
    ventana_respuesta_horas: int = 24  # ventana de mensajería estándar de Meta

    class Config:
        env_prefix = "IG_"
        env_file = ".env"

    @property
    def graph_url(self) -> str:
        return f"{self.graph_base}/{self.graph_version}"

    @property
    def auto_categorias_set(self) -> set[str]:
        return {c.strip() for c in self.auto_categorias.split(",") if c.strip()}


settings = Settings()
