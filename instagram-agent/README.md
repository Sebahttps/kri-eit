# 📸 Agente de Instagram

Responde solo lo trivial —reacciones a historias, "🔥", elogios cortos— y te deja
todo lo demás como borrador listo para aprobar de un toque. Pensado para una
cuenta personal donde del otro lado hay conocidos, no clientes.

---

## ⚠️ Lo que hay que saber antes de empezar

| | |
|---|---|
| **Requisito sin vuelta** | La API de mensajes de Meta **no funciona en cuentas personales**. Hay que pasar la cuenta a **Profesional → Creador**. Es gratis, reversible, no cambia tu @, ni tus seguidores, ni el aspecto del perfil. |
| **Ventana de 24 h** | Meta solo deja responder un DM dentro de las 24 h siguientes al último mensaje de la persona. Pasado eso, el agente arma el borrador pero no lo envía. |
| **Revisión de Meta** | Para usarlo solo con tu cuenta basta el modo desarrollo. Si algún día lo usa otra persona, Meta exige App Review. |
| **El riesgo real** | Que un conocido te pille respondiendo con bot queda peor que responder tarde. Por eso el reparto por defecto es conservador. Súbelo solo cuando lleves un par de semanas leyendo lo que redacta. |

---

## Qué responde solo y qué no

| Categoría | Ejemplo | Por defecto |
|---|---|---|
| `reaccion_trivial` | "🔥", "jajaja", reacción a historia | 🤖 automático |
| `cumplido` | "quedó increíble la foto" | 🤖 automático |
| `saludo_conocido` | "tanto tiempo, cómo estái?" | 🤖 automático |
| `pregunta_personal` | "vai el sábado?" | ✋ borrador |
| `peticion_favor` | "me pasas el contacto?" | ✋ borrador |
| `comercial` | propuestas de marcas | ✋ borrador (bloqueado) |
| `sensible` | conflicto, coqueteo, mala noticia | ✋ borrador, prioridad alta (bloqueado) |
| `spam` | bots y estafas | 🚫 se descarta |

Además, **nunca** se envía solo si: **nunca le has contestado a esa persona**,
hace falta información que solo tú tienes, la confianza es baja, ya van 3
respuestas automáticas con ese contacto en el día, la respuesta salió de más de
140 caracteres, o el mensaje llegó fuera de la ventana de 24 h de Meta.

La primera barrera es la que más manda y no se mide en mensajes sino en
respuestas tuyas: alguien que te escribe cuatro veces seguidas sigue siendo un
desconocido. Lo que abre la puerta a que el agente conteste solo es que **tú
hayas respondido antes desde el panel**.

*Bloqueado* significa que ni agregándolo a `IG_AUTO_CATEGORIAS` sale solo: son
las categorías donde un bot hace daño de verdad.

---

## Puesta en marcha

### 1. Pasar la cuenta a Creador

Instagram → Configuración → **Tipo de cuenta y herramientas** → Cambiar a cuenta
profesional → **Creador**. Elige una categoría cualquiera; se puede ocultar del
perfil en el mismo menú.

### 2. Crear la app en Meta

En [developers.facebook.com](https://developers.facebook.com/apps) → Crear app →
tipo **Otro** → **Empresa**. Dentro de la app, agrega el producto
**Instagram → Configuración de la API con inicio de sesión de Instagram**.

Permisos que necesitas:

- `instagram_business_basic`
- `instagram_business_manage_messages`
- `instagram_business_manage_comments`

Anota de ahí: **App Secret** (Configuración → Básica), el **token de acceso** de
la cuenta y tu **IGSID** (el id numérico de tu cuenta profesional).

### 3. Levantar el servicio

```bash
cd instagram-agent
cp .env.example .env          # y rellena las credenciales
pip install -r requirements.txt
uvicorn app.main:app --port 8000
```

Meta exige **HTTPS con certificado válido** para el webhook. En desarrollo:

```bash
ngrok http 8000               # te da https://algo.ngrok.app
```

Para producción sirve cualquier VPS con dominio, o el `Dockerfile` incluido
(monta un volumen en `/srv/datos` o pierdes historial y borradores en cada
despliegue).

### 4. Conectar el webhook

En la app de Meta → Instagram → Webhooks:

- **URL de devolución de llamada**: `https://tu-dominio/webhook`
- **Token de verificación**: el mismo valor que pusiste en `IG_VERIFY_TOKEN`
- **Campos suscritos**: `messages`, `messaging_reactions`, `comments`

Meta llama al `GET /webhook` en ese momento; si el token calza, queda verificado.

### 5. Probar sin miedo

Arranca con el freno puesto:

```bash
IG_MODO_SOLO_BORRADORES=true uvicorn app.main:app --port 8000
```

Así **no envía nada**: todo cae en el panel. Mándate mensajes desde otra cuenta,
abre `https://tu-dominio/panel?token=TU_PANEL_TOKEN` y lee lo que redactó. Cuando
lo que ves te suene a ti, apaga el freno.

---

## El panel

`GET /panel?token=…` — la bandeja de pendientes. Cada borrador muestra el mensaje
que llegó, la categoría, la confianza, el motivo por el que no salió solo, y un
cuadro editable. Botón *Enviar* (con tus ediciones) o *Descartar*.

> El panel muestra tus DMs. `IG_PANEL_TOKEN` tiene que ser largo y aleatorio:
> `openssl rand -hex 32`.

| Endpoint | Para qué |
|---|---|
| `GET /health` | Estado y modo actual |
| `GET /borradores` | Pendientes en JSON |
| `POST /borradores/{id}/enviar` | Enviar (`{"texto": "..."}` para editar) |
| `POST /borradores/{id}/descartar` | Descartar |

El `?token=…` va **solo la primera vez**, al abrir `/panel`. De ahí queda en una
cookie `HttpOnly` y no vuelve a aparecer en ninguna URL: una credencial en el
query string se escribe en el log de accesos de Caddy y en el historial del
navegador, y esta abre tus mensajes privados.

---

## Ajustar el tono

`app/persona.md` es el tono del agente en lenguaje natural: cómo escribes, qué
nunca dices, ejemplos de respuestas correctas. **Es lo primero que hay que tocar
cuando algo no suena a ti** — no hace falta cambiar código, y el servicio lo
relee al reiniciar.

Para ajustar cuánto se automatiza, `.env`:

| Variable | Efecto |
|---|---|
| `IG_MODO_SOLO_BORRADORES` | `true` apaga todo envío automático |
| `IG_AUTO_CATEGORIAS` | Qué categorías salen solas |
| `IG_AUTO_CONFIANZA_MINIMA` | Súbela si ves respuestas que no habrías mandado |
| `IG_AUTO_MAX_POR_CONTACTO_DIA` | Tope de respuestas automáticas por persona |
| `IG_AUTO_MAX_CARACTERES` | Sobre esto, va a revisión aunque sea trivial |

---

## Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

`test_seguridad.py` y `test_politica.py` corren sin instalar nada (solo stdlib).
`test_esquemas.py` y `test_flujo.py` necesitan las dependencias; el flujo completo
se prueba con dobles, así que **ningún test toca la red ni tu cuenta**.

---

## Cómo está armado

```
webhook firmado → normalizar → deduplicar → clasificar+redactar → decidir
                                                                    ├── enviar
                                                                    └── borrador → panel
```

| Archivo | Responsabilidad |
|---|---|
| `app/seguridad.py` | Firma HMAC de Meta y handshake del webhook |
| `app/esquemas.py` | Aplana los 4 formatos de evento de Meta a uno solo |
| `app/politica.py` | **Qué sale solo y qué no.** Sin red ni BD: es donde se decide |
| `app/redactor.py` | Claude: clasifica y redacta en una sola llamada |
| `app/procesador.py` | Encadena el recorrido completo de un evento |
| `app/almacen.py` | SQLite: deduplicación, historial, cola de borradores |
| `app/instagram.py` | Cliente de la Graph API |
| `app/panel.py` | HTML de la bandeja de revisión |
| `app/persona.md` | **El tono.** Editable sin tocar código |
