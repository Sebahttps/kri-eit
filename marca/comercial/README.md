# Documentos comerciales

Plantillas para Google Sheets, con las fórmulas escritas. **Archivo → Importar
→ Subir**, elegir el CSV. El logo se pone después con *Insertar → Imagen →
Imagen sobre las celdas*, usando `marca/png/compai-logotipo-dia.png` — la
versión diurna, porque estos documentos se imprimen en blanco.

| Archivo | Para qué |
|---|---|
| `cotizacion.csv` | **El que se usa para Compra Ágil.** Validez 15 días |
| `orden-de-pedido.csv` | Requiere firma y timbre de Gerencia General |
| `factura.csv` | Solo la cara visual, para copias y control interno |

**La factura con validez tributaria se emite siempre desde el facturador
electrónico del SII.** Este diseño no reemplaza ese documento y no sirve para
declarar: es la versión presentable de algo que ya existe en el sistema.

## Los cuatro campos que deciden una Compra Ágil

La cotización trae **validez de la oferta, plazo de entrega, garantía y forma de
pago**. Los cuatro juntos, y no es adorno: son lo que el comprador público
necesita para evaluar, y lo que casi ninguna cotización de la competencia trae.
Una oferta que obliga a preguntar por el plazo de entrega, en un proceso que
cierra en 24 o 48 horas hábiles, es una oferta que se descarta.

Trae además el campo **ID adquisición**, que le permite al comprador amarrar la
cotización a su proceso sin escribir un correo.

Y el pie dice explícitamente que **el neto no incluye IVA**. El organismo
compara totales; una ambigüedad ahí cuesta la adjudicación, no una aclaración.

## Lo que no está acá

La firma de correo, la papelería y las tarjetas viven en
`compai_workspace/Kit de Marca CompAI/soportes/` y **no se versionan**: llevan
el teléfono personal, y este repo es público.
