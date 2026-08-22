# CompAI Global Solutions SpA — identidad tributaria y societaria

**Actualizado:** 2026-08-19 · Fuente: certificados originales en
`C:\Users\sebas\compai_workspace\` (**fuera del repo**, ver abajo).

> **Este archivo se versiona en un repo público.** Solo lleva datos de la
> persona jurídica, que van impresos en cada factura que emita la empresa y
> constan en certificados de valor probatorio público. **No lleva** RUT
> personal, domicilio particular, teléfono ni correo — eso vive solo en local.

## Lo esencial

| | |
|---|---|
| **Razón social** | COMPAI GLOBAL SOLUTIONS SpA |
| **Nombre de fantasía** | CompAI SpA — autorizado por estatuto para operar incluso ante bancos |
| **RUT** | **78.491.451-8** |
| **Tipo** | Sociedad por Acciones, accionista único, **sin directorio** |
| **Constitución** | 15-ago-2026, Registro de Empresas y Sociedades (Ley 20.659) |
| **Domicilio social** | Comuna de Santiago (el domicilio **tributario** es otro, ver nota) |
| **Duración** | Indefinida |
| **Capital** | $4.000.000 · 4.000 acciones nominativas, serie única, sin valor nominal |
| **Administración** | Gerente General, con las facultades de un factor de comercio |
| **Inicio de actividades** | **16-ago-2026** · folio 16884724 · certificado el 17-ago |
| **Clasificación SII** | **Primera categoría · afecto a IVA · segmento MICRO EMPRESA** |
| **Registro de Proveedores** | Inscrita y **hábil**, acreditada **hasta el 19-08-2027** (verificado el 22-ago-2026 en la ficha pública). Había opción de 6 y 12 meses; se pagó la anual |
| **Domicilio tributario** | Comuna de **Independencia** (actualizado en el RES en ago-2026; el estatuto original decía comuna de Santiago). Inmueble propio del titular |
| **Declaración de beneficiarios finales** | N° 948459, firmada 19-ago-2026 |

**Por qué importa el segmento MICRO EMPRESA:** Mercado Público registra como
EMT a las personas jurídicas y a las naturales de primera categoría. Ser EMT es
lo que da acceso a la **primera convocatoria de Compra Ágil** — el único canal
donde un proveedor sin historial compite de igual a igual, porque se evalúa
precio y plazo, no currículum. Esa condición ya está cumplida.

## Giros ante el SII

Los siete códigos declarados. **Lo que se puede facturar sale de acá, no del
estatuto** — el objeto social es más amplio que los giros.

> **Corregido el 22-ago-2026: son SIETE, no cinco.** Esta tabla listaba solo
> las cinco primeras y con las glosas parafraseadas. Faltaban 711002 y 829900,
> y de acá salió la lista incompleta que se publicó en compai.cl. Las glosas de
> abajo son ahora las que emite el SII, textuales.

Las siete son **primera categoría, afectas a IVA, con fecha 16-08-2026**.

| Código | Actividad (glosa del SII) |
|---|---|
| 465100 | VENTA AL POR MAYOR DE COMPUTADORES, EQUIPO PERIFERICO Y PROGRAMAS INFORMATICOS |
| 469000 | VENTA AL POR MAYOR NO ESPECIALIZADA |
| 620200 | ACTIVIDADES DE CONSULTORIA DE INFORMATICA Y DE GESTION DE INSTALACIONES INFORMATICAS |
| 620900 | OTRAS ACTIVIDADES DE TECNOLOGIA DE LA INFORMACION Y DE SERVICIOS INFORMATICOS |
| 631100 | PROCESAMIENTO DE DATOS, HOSPEDAJE Y ACTIVIDADES CONEXAS |
| 711002 | EMPRESAS DE SERVICIOS DE INGENIERIA Y ACTIVIDADES CONEXAS DE CONSULTORIA TECNICA |
| 829900 | OTRAS ACTIVIDADES DE SERVICIOS DE APOYO A LAS EMPRESAS N.C.P. |

> **Estado ante el SII al 22-ago-2026:** la solicitud de **emisión de facturas**
> está observada. El Servicio pidió acreditar **todas** las actividades y una
> descripción del negocio. Ver `sii-descripcion-del-negocio.md` en esta misma
> carpeta.

## El estatuto está redactado para vender al Estado

No es un estatuto genérico, y conviene saber lo que ya cubre para no volver a
preguntarlo:

- **Objeto, letra e):** participación en *"licitaciones públicas y privadas,
  cotizaciones, convenios marco, **compras ágiles**, tratos directos y toda
  forma de contratación"*. El giro no deja fuera ninguna modalidad.
- **Objeto, letra b):** compra y venta al por mayor y menor, importación,
  distribución, representación e intermediación de bienes muebles, y **en
  especial** equipos e insumos médicos, dentales, de laboratorio y
  hospitalarios; equipos computacionales, tecnológicos, eléctricos y
  electrónicos; mobiliario, oficina, ferretería, material didáctico y escolar.
- **Facultades del Gerente General:** representar a la sociedad ante la
  **Dirección de Compras y Contratación Pública**, SII, Tesorería, Aduanas,
  ISP, SEREMI de Salud, **CENABAST**, Contraloría, **Tribunal de Contratación
  Pública** e INAPI.
- **Letra f):** ceder, endosar, descontar y **factorizar facturas**, y celebrar
  contratos de factoring y confirming. Esto no es decorativo: es la salida
  práctica a la mora del comprador público, porque los fondos municipales son
  inembargables (art. 32 Ley 18.695) y un título ejecutivo contra un municipio
  puede no tener sobre qué trabar embargo.
- **Letra k):** contratar boletas bancarias de garantía, pólizas y
  **certificados de fianza**. Cubierto para cuando aparezca una licitación que
  las exija.

**Lo que el estatuto permite pero la ley regula aparte:** los dispositivos
médicos tienen exigencias de registro ante el ISP. Que esté en el objeto social
no significa que se pueda vender sin ese trámite.

## Dónde están los originales

`C:\Users\sebas\compai_workspace\` — **fuera del repo, y así se queda.**
`.gitignore` bloquea `compai_workspace/`, `*.pfx`, `*.p12`, `*.pem` y `*.key`.

| Carpeta | Qué hay |
|---|---|
| `Constitución de Sociedad Por Acciones/` | Estatuto actualizado y constitución (CVE verificable 15 días) |
| `Certificado de Vigencia/` | Vigencia al 19-08-2026 |
| `SII/` | Declaración jurada de inicio de actividades, beneficiarios finales, autorización de uso del inmueble |
| `Certificado Tributario Digital/` | **`.pfx` — llave privada.** Es la firma de la empresa ante el SII |
| `Kit de Marca CompAI/`, `Logos y Timbres/` | Identidad, timbres, SVG y PNG |
| `NIC/` | Titularidad de `compai.cl` |

**El `.pfx` es la pieza más delicada de todo el conjunto.** No es un
certificado público: contiene la llave privada con la que se firma en nombre de
la empresa. No se sube a ningún repositorio, no se manda por chat y no se copia
a un servidor.

## Pendientes que este documento no resuelve

1. **Patente municipal.** El domicilio tributario es un departamento en
   **Independencia**, en calidad de *cedido*, con Sebastián como propietario. Ser
   propietario evita la autorización notarial del arrendador, pero **un
   departamento es copropiedad**: la patente comercial pide autorización del
   comité de administración. Y una **SpA no califica para Microempresa
   Familiar** — esa vía es solo para persona natural y EIRL. No bloquea vender.
2. **La pregunta de las empresas relacionadas.** La declaración jurada de
   beneficiarios finales incluye si la empresa tiene vínculos de actuación
   económica con otras. Hay una constructora familiar en el cuadro. Ver
   `riesgo-empresas-relacionadas.md`.
3. **Marca INAPI.** La solicitud de clase 35 sigue sin presentarse. El titular
   previsto era persona natural; ahora que la SpA existe, hay que decidir si se
   presenta directamente a nombre de la sociedad y ahorrarse la cesión.
