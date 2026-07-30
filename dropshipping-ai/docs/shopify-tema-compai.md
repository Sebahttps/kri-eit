# Identidad CompAI en el tema de Shopify

La tienda corre **Horizon 4.1.3** (`theme_store_id` 2481), el tema por defecto
actual de Shopify — no Dawn. Detectado el 2026-07-30 leyendo
`Shopify.theme` en el HTML de la tienda.

> **Esto requiere acceso al admin.** Los pasos 1 a 3 los hace el usuario en el
> editor de temas. Con la app del Dev Dashboard creada y el scope
> `write_themes`, se pueden automatizar por API.

## Por qué los colores van en el editor y no en CSS propia

Horizon aplica los colores mediante **clases de esquema por sección**
(`.color-custom-<id>`), no solo en `:root`. Cada sección elige su esquema desde
el editor. Sobreescribirlos desde CSS propia obligaría a selectores tan amplios
(`[class*="color-"]`) que además de los esquemas de contenido alcanzarían los de
las insignias de **oferta** y **agotado**, dejándolas ilegibles.

Los colores se definen donde el tema los espera. La CSS propia queda para lo que
el editor no alcanza.

## 1. Colores

*Tienda online → Temas → Personalizar → Ajustes del tema → Colores*

En el esquema principal:

| Ajuste | Valor |
|---|---|
| Fondo | `#f7f2e6` |
| Texto | `#1c1917` |
| Fondo de botón sólido | `#a2551f` |
| Texto de botón sólido | `#ffffff` |
| Botón de contorno | `#a2551f` |
| Bordes | `#e5dcc8` |

Si hay un segundo esquema para tarjetas o secciones alternas, usar `#fdfbf4`
como fondo y el mismo texto.

**El verde `#15734a` no se pone aquí.** Está reservado al doble check; usarlo
como color de sección le quitaría el significado. Lo aplica la CSS propia.

Contrastes verificados: texto sobre fondo 15,65:1; cobre sobre fondo 4,88:1;
blanco sobre cobre 5,45:1 — todos sobre el mínimo AA.

## 2. Logotipo

*Ajustes del tema → Logotipo*

- **Encabezado**: `brand/logo-compai.svg` — ancho recomendado 160 px.
- **Favicon**: `brand/favicon.svg`.

⚠️ Antes de subir el logotipo, **convertirlo a curvas** (Figma o Inkscape:
*Texto → Contornear*). Usa texto en vivo y sin ese paso se dibuja con la fuente
de cada dispositivo. El favicon es geometría pura y se sube tal cual.

## 3. CSS propia

*Ajustes del tema → CSS propia* → pegar
[`brand/shopify-custom.css`](../brand/shopify-custom.css) completo.

Cubre foco visible en cobre, selección de texto, ancho mínimo del logotipo,
números tabulares en los precios, `prefers-reduced-motion`, y el bloque de las
cinco promesas con doble check.

## 4. Las cinco promesas

Agregar una sección de **texto enriquecido** con una lista de viñetas, una
promesa por viñeta, con los mismos textos que la tienda propia:

- Stock confirmado con el proveedor antes de cobrarte
- Paga al recibir si prefieres
- Seguimiento en tiempo real de tu despacho
- Garantía legal de 6 meses, gestión inmediata
- 10 días para retractarte, sin preguntas

La CSS las convierte en burbujas de chat con doble check verde cuando la sección
lleva la clase `.compai-promesas`. Si la sección no permite añadir la clase, usar
la **CSS propia de la sección** (seleccionarla en el editor → *CSS propia*) y
pegar ahí el bloque `.compai-promesas li`, que Shopify antepone al selector de
esa sección automáticamente.

El doble check va como imagen de fondo en un data URI, no como carácter: así no
depende de que la fuente del visitante tenga el glifo y conserva el trazo exacto
del logotipo.

## Tipografía: una divergencia consciente

Horizon usa **Inter**; la tienda propia y el panel usan la pila del sistema
(`system-ui`). No se unifica, por dos razones: Shopify solo ofrece las familias
de su propia biblioteca, e Inter es una elección correcta para una tienda.

El cliente ve una sola de las dos, así que la divergencia no es visible para
nadie. Si más adelante se quiere unificar, lo barato es mover las apps Next.js a
Inter, no al revés.
