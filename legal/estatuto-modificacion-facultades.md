# Modificación del artículo octavo — facultades bancarias del Gerente General

> **Aviso.** Análisis estratégico y educativo. No reemplaza el patrocinio de un abogado
> habilitado (Ley 18.120). Repo público: datos identificatorios reemplazados por marcadores.

| Campo | Valor |
|---|---|
| Sociedad | `[RAZÓN SOCIAL]` SpA |
| RUT | `[RUT-SOCIEDAD]` |
| Gerente General / accionista único | `[NOMBRE]`, RUT `[RUT-PERSONA]` |
| Régimen | Simplificado, Ley N° 20.659 ("Tu Empresa en un Día") |
| Norma supletoria | Arts. 424 a 446 Código de Comercio; Ley N° 18.046 y su Reglamento |
| Artículo a modificar | ARTÍCULO OCTAVO (facultades del Gerente General) |
| Motivo | Dos rechazos de contratación de cuenta bancaria |

---

## Conclusión primero

1. **El texto propuesto está bien orientado pero es insuficiente y, tal como está redactado,
   es peligroso.** Cubre el hueco correcto ("cobrar y percibir"), pero deja **nueve huecos**
   que un validador literalista puede usar para un tercer rechazo, y **no dice dónde se
   inserta**: si se pega solo en el formulario reemplazando el artículo octavo completo, se
   destruyen las letras a) a k) vigentes (facultades laborales, judiciales, tributarias, de
   garantías y de compraventa). Ese es el riesgo mayor del borrador, y no es legal: es de
   mecánica del formulario.
2. **El hueco crítico no detectado es la firma electrónica y la banca en línea.** El estatuto
   vigente no contiene las palabras "firma electrónica", "transferencia electrónica",
   "internet", "clave", "token" ni "medios remotos". Una cuenta digital de emprendimiento se
   opera íntegramente por esos canales; el checklist de cumplimiento del banco los busca.
3. **No conviene excluir ninguna facultad por sobre-amplitud.** El razonamiento de exposición
   patrimonial está mal ubicado: lo que expone el patrimonio personal no es la facultad
   estatutaria, sino el aval o fianza personal que el banco hará firmar aparte. Detalle en
   la sección 2.
4. **El trámite es un formulario de modificación en el RES, $0 si el titular firma con firma
   electrónica avanzada.** El titular ya posee un certificado digital tributario `.pfx`; si
   ese certificado es FEA emitida por entidad acreditada bajo la Ley N° 19.799, el costo del
   trámite es cero y no se requiere notario. **Verificar el tipo de certificado antes de
   pagar notaría.**
5. **Plazo vivo detectado, no preguntado:** el certificado de estatuto actualizado que hoy se
   tiene solo es verificable en línea **15 días corridos** desde su emisión (así lo declara el
   propio documento). Un certificado fuera de esa ventana puede ser rechazado por el banco
   por no poder validar el CVE. Emitir el certificado **el mismo día** en que se entrega al banco.

---

## 1. Auditoría del texto propuesto — huecos por los que entra un tercer rechazo

### 1.1 Punto de partida: qué dice realmente el estatuto vigente

Contrastado contra el certificado de estatuto actualizado, artículo octavo:

| Letra | Contenido relevante | Estado |
|---|---|---|
| b) | "Representar a la sociedad ante bancos e instituciones financieras, pudiendo abrir, operar y cerrar cuentas corrientes bancarias, a la vista, de ahorro o de crédito, girar, aceptar, endosar y protestar cheques, letras de cambio y pagarés, solicitar y contratar créditos, avances y boletas de garantía" | **Existe.** El primer rechazo automático fue incorrecto |
| f) | Factoring, confirming, leasing, **líneas de crédito**, mutuos y cualquier otra operación de financiamiento | **Ya existe** — el borrador lo ignora y no debe perderse |
| g) | Prendas, hipotecas, garantías reales o personales, fianzas, **avales y codeudas solidarias por obligaciones propias o de terceros** | **Ya existe** |
| j) | Representación en juicio, art. 7° incisos 1° y 2° CPC, terminando en "aprobar convenios y **percibir**" | Facultad **procesal**, no comercial |
| k) | Contratar seguros, boletas bancarias de garantía, pólizas, "**y cobrarlos o hacerlos efectivos**" | Cobro **acotado** a esos instrumentos |

**Confirmado: el segundo rechazo tiene fundamento.** La palabra "percibir" aparece una sola
vez, en la letra j), dentro del catálogo del art. 7° inc. 2° CPC. Es la diputación para recibir
el pago en juicio, no la facultad general de cobro comercial.

> **Contra-argumento que existe pero no conviene usar:** la facultad ya está implícita. El
> Gerente General está "premunido de todas las facultades propias de un factor de comercio"
> (arts. 237 y ss. del Código de Comercio, de los factores y dependientes de comercio), y el
> mandato de administración comprende por su naturaleza "cobrar los créditos del mandante que
> pertenezcan al giro administrativo ordinario" (**art. 2132 del Código Civil**); la diputación
> para recibir el pago se confiere por poder general de administración (**art. 1580 CC**).
> Jurídicamente la tesis es sólida. **Estratégicamente es inútil:** el ejecutivo que rechazó no
> tiene atribución para aceptar un argumento de derecho contra su checklist. Discutir cuesta
> semanas y la probabilidad de éxito es baja. Se modifica el estatuto y se acaba la discusión.

### 1.2 Riesgo estructural — el más grave del borrador

El texto propuesto se presenta como dos párrafos titulados, sin indicar si **reemplaza** el
artículo octavo o se **agrega** a él. Si se pega tal cual como nuevo artículo octavo:

- se pierden las letras a), c), d), e), f), g), h), i), j) y k);
- la sociedad queda sin facultades laborales (contratar y despedir), sin representación
  judicial, sin representación ante SII, Tesorería y Aduanas, sin facultad de comprar y vender,
  y sin delegación de poderes;
- y se genera un problema nuevo peor que el bancario.

**Mitigación:** el texto final de la sección 4 es un **refundido completo** del artículo octavo.
Reemplaza la letra b), conserva íntegras las demás y agrega las letras l), m) y n) más un
inciso final de forma de actuación.

### 1.3 Los nueve huecos que faltan en el borrador

Ordenados por probabilidad de gatillar un tercer rechazo.

| # | Hueco | Por qué el validador lo marca | Gravedad |
|---|---|---|---|
| 1 | **Firma electrónica** (simple y avanzada, Ley N° 19.799) | El contrato de cuenta se suscribe electrónicamente. Sin la facultad expresa, cumplimiento objeta la forma de suscripción | Alta |
| 2 | **Banca en línea y medios remotos**: internet, app móvil, banca telefónica, claves, tokens, tarjetas de coordenadas, administración de usuarios y perfiles | Es el modo de operación real del producto. El checklist de banca digital lo tiene como ítem propio | Alta |
| 3 | **Tarjetas** de crédito, débito y prepago: solicitar, activar, bloquear, fijar cupos, titulares adicionales | La cuenta viene con tarjeta asociada. Sin facultad, no se emite | Alta |
| 4 | **Instituciones financieras no bancarias y medios de pago**: cooperativas, cajas de compensación, emisores y operadores no bancarios de tarjetas, entidades fiscalizadas por la CMF, proveedores de servicios de pago, adquirentes y subadquirentes, pasarelas de pago | Crítico para operación de comercio electrónico. También lo pide la pasarela, no solo el banco | Alta |
| 5 | **Declaraciones juradas de cumplimiento**: origen de fondos, beneficiario final, conocimiento del cliente, FATCA/CRS, prevención de lavado de activos (Ley N° 19.913) | Es requisito de onboarding independiente. Si el representante no puede suscribirlas, la apertura se traba en cumplimiento | Alta |
| 6 | **Moneda extranjera y cuentas en el exterior**; operaciones de cambios internacionales e informe al Banco Central cuando corresponda | Necesario para importación y cobros desde el exterior | Media |
| 7 | **Orden de no pago y revocación de cheques**; endoso en dominio, en cobranza y en garantía; revalidación | Ítems clásicos de la minuta de facultades de cuenta corriente (DFL N° 707, Ley sobre Cuentas Corrientes Bancarias y Cheques) | Media |
| 8 | **Servicios de recaudación, nómina, pago a proveedores, transferencias masivas, PAC y PAT**; contratación de productos de inversión y depósitos a plazo | Productos anexos que se contratan en el mismo acto | Media |
| 9 | **Forma de actuación**: que el Gerente General obliga a la sociedad **actuando individualmente y con su sola firma** | El estatuto no lo dice expresamente. Un validador literalista puede preguntar si se requiere firma conjunta | Media |

Adicionalmente, en el bloque "cobrar y percibir" del borrador falta **otorgar recibos,
finiquitos y cancelaciones**, que es lo que hace oponible el pago frente al deudor
(**art. 1576 CC**: el pago debe hacerse al acreedor o a quien esté autorizado para recibir por
él). Sin esa mención, "percibir" queda a medio camino.

### 1.4 Lo que el borrador sí acierta

Estas incorporaciones del borrador son correctas y se conservan en el texto final: depositar,
sobregirar, imponerse del movimiento, aprobar y objetar saldos, talonarios y cheques sueltos,
cajas de seguridad, cancelar cheques, comisiones de confianza, y el encabezado por materia
("OPERACIONES CON BANCOS…"), que facilita la lectura del validador.

---

## 2. Riesgo de sobre-amplitud — tesis y contratesis

**Facultades bajo examen:** sobregirar, contratar créditos y líneas, otorgar avales y fianzas.

### Tesis (recomendada): incorporarlas todas, sin condicionar ninguna

1. **La facultad estatutaria no crea deuda ni traspasa responsabilidad.** Es un poder de
   representación. La sociedad se obliga cuando el Gerente General contrata, no cuando el
   estatuto lo autoriza. La limitación de responsabilidad del accionista al monto de sus
   acciones no se ve afectada por la extensión del mandato.
2. **Lo que expone el patrimonio personal es otra cosa.** Cuando el banco otorgue una línea de
   crédito o un sobregiro a una SpA nueva con capital modesto, exigirá **aval, fianza o
   codeuda solidaria personal del titular**. Ese documento —no el estatuto— es el que hace
   perseguible el patrimonio personal. Suprimir "sobregirar" del estatuto no evita ese riesgo:
   solo impide operar y garantiza un tercer rechazo.
3. **No hay conflicto de agencia que proteger.** Accionista único que es a la vez Gerente
   General: no existe minoritario cuyo interés se resguarde limitando el poder del
   administrador.
4. **Condicionar facultades es la causa más común de rechazo bancario.** Una redacción del
   tipo "podrá sobregirar previa autorización escrita del accionista" obliga al banco a exigir
   esa autorización en cada operación. Los validadores rechazan por defecto las facultades
   condicionadas. Se está tratando de resolver un rechazo, no de crear uno nuevo.
5. **La responsabilidad del administrador subsiste igual.** El art. 133 de la Ley N° 18.046,
   aplicable supletoriamente a la SpA por remisión del art. 424 del Código de Comercio, hace
   responder al administrador por los perjuicios causados por infracción a la ley o a los
   estatutos. Esa responsabilidad no depende de cuán amplio sea el poder.

### Contratesis (el mejor argumento contrario, planteado en serio)

1. **El estatuto es público y se lee entero.** Un tercero —otro banco, un inversionista en
   *due diligence*, una contraparte en licitación— que lee la letra g) ve una sociedad cuyo
   administrador único puede avalar deuda ajena sin límite. Eso deteriora el perfil de riesgo
   percibido y puede encarecer financiamiento futuro.
2. **La sociedad de accionista único puede dejar de serlo.** El artículo décimo tercero del
   estatuto contempla expresamente pluralidad de accionistas, y el décimo cuarto delega en la
   administración el aumento de capital sin junta ni reforma (art. 434 del Código de Comercio).
   Si entra un socio, hereda un Gerente General con poder ilimitado y sin contrapesos.
3. **Punto técnico real sobre los avales:** el otorgamiento de garantías reales o personales
   para caucionar obligaciones **de terceros** que excedan el 50% del activo es materia de junta
   extraordinaria conforme al **art. 57 N° 5 de la Ley N° 18.046**, aplicable supletoriamente.
   La letra g) vigente, al conferir esa facultad sin límite al Gerente General, convive con esa
   norma de manera ambigua. Es un flanco de nulidad relativa o de inoponibilidad que un
   acreedor sofisticado podría explotar.
4. **Un validador puede escalar por exceso.** Ver "sobregirar", "líneas de crédito" y "avales"
   en un expediente de cuenta básica de emprendimiento puede derivar el caso a comité de
   crédito y demorar el onboarding, aunque el producto no involucre riesgo crediticio.

### Resolución

**Se sigue la tesis en cuanto a las facultades bancarias: no se limita ninguna.** Sobregirar,
contratar créditos y líneas entran completos y sin condición.

**Sobre la letra g) (garantías por obligaciones de terceros): decisión revisada.**

| Momento | Decisión | Fundamento |
|---|---|---|
| Análisis inicial | Diferir el ajuste a una segunda modificación | Evitar abrir un segundo frente mientras se resuelve el rechazo bancario |
| Decisión final | **Incorporar el ajuste en esta misma actuación** | El costo marginal es cero con el formulario abierto, y el argumento del "segundo frente" no resiste el examen (ver abajo) |

**Por qué cambió la decisión.** El motivo para diferir era no aumentar la superficie de rechazo
bancario. Ese motivo no se sostiene al examinarlo:

1. **El checklist bancario no revisa la letra g).** Para una cuenta de emprendimiento, el
   validador verifica facultades bancarias (letra b), cobro y percepción (letra l) y personería.
   Las garantías por obligaciones **de terceros** no figuran en ese examen.
2. **La restricción se redacta citando la norma que la impone.** Al invocar expresamente el
   art. 57 N° 5 de la Ley N° 18.046, un validador no lee una facultad arbitrariamente
   condicionada, sino una cláusula de cumplimiento legal. Eso reduce, no aumenta, la objeción.
3. **Las obligaciones propias quedan intactas.** Prendas, hipotecas, fianzas y avales para
   caucionar deuda **de la sociedad** siguen sin condición alguna. Es lo único que el banco
   podría llegar a mirar si más adelante otorga línea de crédito o boleta de garantía.
4. **El cambio es sustantivo, no cosmético.** Conforme al art. 424 del Código de Comercio la
   SpA se rige por su estatuto y solo supletoriamente por las normas de la sociedad anónima
   cerrada. La letra g) vigente, al conferir la facultad sin límite, puede leerse como
   desplazamiento estatutario de la regla supletoria del art. 57 N° 5. Escribir el umbral no
   aclara: **restablece** el límite legal.
5. **Postergar un trámite registral es caro y olvidar es gratis.** Una segunda actuación futura
   implica volver a firmar y, en su caso, volver a pagar notaría. Hacerlo ahora cuesta $0.

**Riesgo residual asumido:** un validador especialmente literalista podría marcar cualquier
facultad que contenga la palabra "requerirá acuerdo previo". Probabilidad estimada baja, porque
el ítem no pertenece a su checklist. Mitigación: si ocurre, se responde que el límite es legal y
no estatutario, y que el accionista único lo levanta por declaración escrita en el acto conforme
al artículo noveno del estatuto, sin junta ni formalidad.

**Efecto operativo real para el titular: ninguno en la práctica.** Siendo accionista único, la
autorización que la nueva letra g) exige la otorga él mismo, por escrito, en el mismo acto, sin
citación ni quórum (artículo noveno). Lo que se gana es un freno deliberado y una constancia
documental antes de comprometer el patrimonio social por deuda ajena.

---

## 3. Mecánica del trámite en el régimen simplificado (Ley N° 20.659)

### 3.1 Actuación y formulario

| Ítem | Respuesta | Confianza |
|---|---|---|
| Actuación | **Modificación** — no es constitución, transformación ni migración | Alta |
| Formulario | Formulario de **modificación** correspondiente al tipo social Sociedad por Acciones, dentro de la ficha de la empresa en `registrodeempresasysociedades.cl` | Alta |
| Base legal | Arts. 3° y siguientes de la Ley N° 20.659: constitución, modificación, transformación, fusión, división, terminación y disolución se realizan mediante formularios suscritos e incorporados al Registro | Alta |
| Quién suscribe | El **accionista único**, por sí. El artículo noveno del estatuto vigente ya establece que mientras haya un solo accionista todas las materias de junta se resuelven "mediante declaración escrita firmada… sin necesidad de citación, publicación, quórum ni formalidad alguna" | Alta |
| ¿Se requiere junta extraordinaria reducida a escritura pública? | **No.** En el régimen simplificado el formulario reemplaza la escritura pública y la inscripción. Además el estatuto lo dispensa expresamente | Alta |
| ¿Hay que avisar al SII? | **No por esta modificación.** No cambia el representante legal ante el SII ni el domicilio ni el giro. El RES informa al SII las actuaciones. Verificar de todos modos que la ficha del SII refleje el estatuto vigente antes de ir al banco | Media |

### 3.2 Firma: FEA versus notario

| Vía | Costo | Requisito |
|---|---|---|
| **A. Firma electrónica avanzada del titular** | **$0** de arancel notarial | Que el titular posea FEA vigente emitida por prestador acreditado bajo la Ley N° 19.799 |
| **B. Suscripción ante notario** | Arancel notarial | Cuando el suscriptor no tiene FEA. El notario firma el formulario con su propia FEA. Art. 9° de la Ley N° 20.659 |

**Hallazgo que puede ahorrar el trámite notarial:** el titular ya cuenta con un **certificado
tributario digital** (archivo `.pfx`) usado para operar ante el SII. Muchos de esos certificados
son firma electrónica avanzada emitida por prestador acreditado, y en tal caso sirven para
suscribir el formulario del RES sin notario.

**Verificar antes de agendar notaría:**
1. Abrir el certificado y revisar el emisor y el tipo (avanzado o simple).
2. Intentar la suscripción en el RES con ese certificado: si la plataforma lo acepta, la vía A
   está disponible y el costo es $0.
3. Si el certificado es de firma **simple**, no sirve: hay que contratar FEA (costo anual, del
   orden de decenas de miles de pesos) o ir a notaría por una sola vez.

> **Declaración de incertidumbre, conforme a las reglas de citación.** No puedo confirmar el
> **monto exacto del arancel notarial vigente** para la suscripción de formularios del RES. La
> cifra de ~$10.623 manejada por el usuario es plausible como arancel regulado, pero debe
> verificarse en el sitio del RES o directamente con la notaría antes de presupuestarla. No
> corresponde afirmar un monto que no me consta.

### 3.3 Plazos de vigencia del nuevo certificado

| Pregunta | Respuesta | Confianza |
|---|---|---|
| ¿Cuándo queda vigente la modificación? | Al quedar el formulario suscrito por todos quienes deben firmarlo e incorporado al Registro. El régimen es de tramitación en línea y la lógica de "Tu Empresa en un Día" es que la actuación y sus certificados quedan disponibles el mismo día | Media-alta |
| ¿Y si se firma ante notario? | Depende de que el notario complete su firma electrónica sobre el formulario. Puede tomar horas o el día siguiente según la notaría | Media |
| ¿Puedo garantizar un plazo administrativo exacto? | **No.** No afirmo un plazo en horas o días hábiles que no me conste. Planificar sobre el supuesto de "mismo día si firma con FEA; hasta 48 horas si interviene notario" y confirmar en el RES | — |

### 3.4 ¿El banco necesita además certificado de vigencia?

**Sí. Se piden los dos, y ambos emitidos después de la modificación.**

| Documento | Para qué | Costo |
|---|---|---|
| **Certificado de Estatuto Actualizado** | Acredita el texto vigente del artículo octavo, ya modificado | $0 en el RES |
| **Certificado de Vigencia** | Acredita que la sociedad existe y está vigente a la fecha | $0 en el RES |

Ambos tienen **valor probatorio de instrumento público** conforme al **art. 22 de la Ley N° 20.659**.

> **Plazo fatal práctico, no preguntado.** El propio certificado declara que el documento queda
> disponible para verificación en línea **por 15 días contados desde la fecha de emisión**. Un
> certificado emitido fuera de esa ventana no puede validarse por CVE y el banco puede
> rechazarlo por ese solo motivo. **Emitir ambos certificados el mismo día en que se entregan
> al ejecutivo**, no antes. Adicionalmente, la mayoría de los bancos exige antigüedad máxima de
> 30 a 60 días para documentos societarios: la ventana de 15 días del RES es más estricta y es
> la que manda.

### 3.5 Secuencia operativa

| Paso | Acción | Responsable | Costo |
|---|---|---|---|
| 1 | Verificar si el `.pfx` es FEA de prestador acreditado | Titular | $0 |
| 2 | Ingresar al RES, ficha de la empresa, actuación **Modificación** | Titular | $0 |
| 3 | Pegar el texto refundido del artículo octavo (sección 4) | Titular | $0 |
| 4 | Suscribir: FEA propia, o ante notario si no la tiene | Titular / notario | $0 o arancel |
| 5 | Confirmar que la actuación aparece en el "Historial de actuaciones y anotaciones" | Titular | $0 |
| 6 | **El mismo día de la cita bancaria**: emitir Certificado de Estatuto Actualizado y Certificado de Vigencia | Titular | $0 |
| 7 | Entregar al banco con un mapa de facultades de una página | Titular | $0 |

**Paso 7 — táctica, no derecho.** El ejecutivo opera bajo un checklist y no tiene atribución
para aceptar argumentos jurídicos. Discutirle la ley no funciona y desgasta la relación. Lo que
sí funciona es hacerle el trabajo: una hoja que, ítem por ítem de su checklist, indique la
**letra y la página exacta** del nuevo certificado donde consta cada facultad. Elimina su
esfuerzo y su riesgo de equivocarse, que es lo único que lo mueve. Adjuntar el PDF **completo**,
sin recortes, para no repetir el problema del salto de página que motivó el primer rechazo.

### 3.6 Vías alternativas — mapa completo del escenario

| Vía | Costo | Plazo | Probabilidad estimada | Comentario |
|---|---|---|---|---|
| **Modificar el estatuto** (recomendada) | $0 a arancel notarial | 1 a 3 días | Alta | Resuelve el problema de forma permanente y sirve para todo banco y toda pasarela futura |
| Insistir con el mismo ejecutivo invocando arts. 237 CCom y 2132 CC | $0 | 1 a 3 semanas | Baja | El ejecutivo carece de atribución. Técnicamente correcto, operativamente estéril |
| Reclamar ante el servicio al cliente del banco | $0 | 2 a 4 semanas | Baja | Solo si tras la modificación hay un tercer rechazo infundado |
| Otorgar poder por escritura pública a un apoderado, sin tocar el estatuto | Arancel notarial | 1 día | Media | Más rápido, pero es un parche: cada banco vuelve a revisarlo y no repara el estatuto |
| Abrir cuenta en otro banco o en una entidad de pago no bancaria | $0 | 1 a 5 días | Media-alta | Sirve para desbloquear la operación mientras se tramita. No sustituye la modificación |

**Estimaciones de probabilidad**: basadas en la práctica bancaria chilena de validación
documental por checklist, no en estadística publicada. Declaradas como estimación estratégica.

---

## 4. Texto final — refundido completo del artículo octavo, listo para pegar

> Reemplaza íntegramente el artículo octavo vigente. Conserva las letras a) y c) a k) actuales,
> sustituye la letra b), agrega las letras l), m) y n) y un inciso final sobre forma de actuación.

```
ARTÍCULO OCTAVO: El Gerente General de la sociedad estará premunido de todas las facultades propias de un factor de comercio, y en especial, de las que se señalan a continuación. El Gerente General representará a la sociedad con las más amplias facultades de administración y disposición de bienes, pudiendo obligarla en toda clase de actos y contratos. Especialmente, y sin que esta enumeración sea taxativa, podrá: a) Representar a la sociedad ante cualquier persona natural o jurídica, pública o privada, incluyendo la Dirección de Compras y Contratación Pública (Mercado Público), Servicio de Impuestos Internos, Tesorería General de la República y Municipalidades; b) OPERACIONES CON BANCOS E INSTITUCIONES FINANCIERAS: Representar a la sociedad ante toda clase de bancos e instituciones financieras, estatales o privados, nacionales o extranjeros, con las más amplias facultades que se precisen; darles instrucciones y cometerles comisiones de confianza; celebrar, modificar, renovar y poner término o solicitar la terminación de contratos de cuenta corriente bancaria de depósito y de crédito; abrir, operar y cerrar cuentas corrientes bancarias, cuentas de depósito a la vista, cuentas vista, cuentas de ahorro, cuentas de crédito, cuentas de provisión de fondos y cuentas de pago, en moneda nacional o extranjera, en Chile o en el extranjero; depositar, girar, sobregirar, transferir y retirar fondos de ellas, sea mediante cheques, órdenes de pago, transferencias electrónicas, cargos automáticos o cualquier otro medio; imponerse de su movimiento; aprobar y objetar saldos; requerir y retirar talonarios de cheques y cheques sueltos; girar, aceptar, revalidar, endosar en dominio, en cobranza o en garantía, descontar, protestar, cancelar, revocar y dar orden de no pago de cheques, letras de cambio, pagarés, facturas, efectos públicos y de comercio y valores mobiliarios; arrendar cajas de seguridad, abrirlas y ponerles término; constituir y retirar depósitos a la vista y a plazo; solicitar, contratar, renovar, repactar y poner término a créditos en todas sus formas, líneas de crédito, líneas de sobregiro, avances contra aceptación, mutuos, boletas bancarias de garantía, cartas de crédito, cobranzas de importación y exportación, operaciones de comercio exterior y de cambios internacionales, informando al Banco Central de Chile cuando corresponda, factoring, confirming y leasing; solicitar, contratar, activar, bloquear y cancelar tarjetas de crédito, de débito y de prepago, fijando y modificando sus cupos, límites y titulares adicionales; contratar servicios de recaudación, de pago de remuneraciones y de proveedores, transferencias masivas y mandatos de pago automático de cuentas y de cargo en cuenta; contratar productos de inversión, depósitos a plazo, fondos mutuos, pactos y custodia de valores; y suscribir los contratos de adhesión, reglamentos, anexos y condiciones generales de los productos y servicios que contrate, así como las declaraciones juradas de origen de fondos, de beneficiario final, de conocimiento del cliente y las demás exigidas por la normativa de prevención de lavado de activos y financiamiento del terrorismo y por la normativa tributaria nacional o extranjera; c) Comprar, vender, permutar, dar y tomar en arrendamiento, importar y exportar toda clase de bienes muebles e inmuebles, corporales e incorporales; d) Celebrar contratos de trabajo, contratar, fijar remuneraciones y poner término a contratos; e) Transigir, comprometer y conferir mandatos generales y especiales; f) Ceder, transferir, endosar, descontar y factorizar facturas, créditos, cuentas por cobrar y toda clase de documentos y valores mobiliarios; celebrar contratos de factoring, confirming, leasing, líneas de crédito, mutuos y cualquier otra operación de financiamiento; g) Constituir, modificar y alzar prendas de cualquier clase, hipotecas y toda especie de garantías reales o personales, y otorgar fianzas, avales y codeudas solidarias, para caucionar obligaciones propias de la sociedad, sin limitación alguna. Tratándose de garantías reales o personales otorgadas para caucionar obligaciones de terceros, el Gerente General podrá constituirlas por sí solo cuando su monto no exceda del cincuenta por ciento del activo de la sociedad; excedido dicho límite, requerirá el acuerdo previo y por escrito del accionista único o de la junta de accionistas, conforme al artículo 57 número 5 de la Ley N° 18.046, acuerdo que se adoptará y constará en la forma prevista en el artículo noveno de estos estatutos; h) Representar a la sociedad ante el Servicio Nacional de Aduanas, Instituto de Salud Pública, Secretarías Regionales Ministeriales de Salud, Central de Abastecimiento del Sistema Nacional de Servicios de Salud, Dirección del Trabajo, Superintendencia de Seguridad Social, Contraloría General de la República, Tribunal de Contratación Pública, Instituto Nacional de Propiedad Industrial, Comisión para el Mercado Financiero, Unidad de Análisis Financiero, y ante toda autoridad administrativa, municipal, aduanera, sanitaria o judicial, sea nacional o extranjera; i) Otorgar y revocar mandatos generales y especiales, delegar total o parcialmente sus facultades y reasumirlas, y autocontratar, pudiendo actuar por sí y en representación de la sociedad, o en representación de dos o más partes en un mismo acto; j) Representar a la sociedad en juicio con las facultades de ambos incisos del artículo 7° del Código de Procedimiento Civil, que se dan por expresamente reproducidas, incluidas las de desistirse en primera instancia de la acción deducida, aceptar la demanda contraria, absolver posiciones, renunciar los recursos y los términos legales, transigir, comprometer, otorgar a los árbitros facultades de arbitradores, aprobar convenios y percibir; k) Contratar y tomar seguros de toda clase, boletas bancarias de garantía, pólizas de garantía y certificados de fianza, y cobrarlos o hacerlos efectivos; l) COBRAR Y PERCIBIR: Cobrar y percibir, judicial y extrajudicialmente, todo cuanto se adeude a la sociedad a cualquier título y por cualquier causa, sea en dinero o en otra clase de bienes, corporales o incorporales, raíces o muebles, valores mobiliarios y efectos de comercio; retirar y recibir dichos pagos de manos de deudores, bancos, instituciones financieras, plataformas de pago, organismos públicos o de cualquier tercero; otorgar y suscribir recibos, finiquitos, cancelaciones y cartas de pago; imputar pagos; conceder quitas y esperas y celebrar convenios de pago, repactaciones y acuerdos de compensación; y cobrar y percibir del Servicio de Impuestos Internos, de la Tesorería General de la República y de cualquier otro organismo, toda clase de devoluciones, remanentes, créditos fiscales, subsidios y beneficios; m) MEDIOS ELECTRÓNICOS Y FIRMA ELECTRÓNICA: Suscribir con firma electrónica simple o avanzada, conforme a la Ley N° 19.799, toda clase de actos, contratos, solicitudes, formularios, mandatos y declaraciones, con el mismo valor que la firma manuscrita; contratar y operar servicios de banca en línea, banca por internet, banca telefónica, aplicaciones móviles y cualquier otro canal remoto o electrónico; solicitar, administrar, bloquear, renovar y revocar claves, contraseñas, tarjetas de coordenadas, dispositivos digitales de seguridad, tokens y demás factores de autenticación; designar, modificar y revocar usuarios, administradores y apoderados de los canales electrónicos, asignándoles perfiles, atribuciones, montos y límites máximos de operación; y aceptar por medios electrónicos los términos, condiciones y contratos de adhesión de los productos y servicios contratados; n) MEDIOS DE PAGO E INSTITUCIONES FINANCIERAS NO BANCARIAS: Representar a la sociedad y contratar, operar, modificar y poner término a toda clase de productos y servicios ante cooperativas de ahorro y crédito, cajas de compensación de asignación familiar, emisores y operadores no bancarios de tarjetas de pago, instituciones financieras, de pago y demás entidades fiscalizadas por la Comisión para el Mercado Financiero, corredores de bolsa, administradoras generales de fondos, compañías de seguros, casas de cambio, empresas de factoring y leasing no bancarias, proveedores de servicios de pago, adquirentes y subadquirentes, y pasarelas, plataformas y billeteras de pago, nacionales o extranjeras; contratar y operar terminales de punto de venta, códigos de respuesta rápida, botones de pago, cuentas de pago y billeteras electrónicas; y suscribir los contratos de afiliación, adquirencia, recaudación, liquidación y transferencia de fondos correspondientes. Todas las facultades precedentes serán ejercidas por el Gerente General actuando individualmente, bastando su sola firma para obligar válidamente a la sociedad.
```

---

## 5. Ruta elegida y mapa de facultades para el ejecutivo

**Ruta recomendada: vía A** — tramitar la modificación y esperar la cuenta bancaria, sin abrir
cuenta de pago no bancaria en paralelo. Consecuencia asumida: la operación queda sin recaudación
propia hasta que el banco apruebe, estimado en 3 a 7 días corridos desde la suscripción del
formulario.

> **No es una decisión adoptada.** El titular no la ha elegido; es la recomendación del análisis.
> La vía B (cuenta de pago no bancaria en paralelo) sigue abierta y se justifica si hay cobros
> esperando entrar esta semana.

### 5.1 Verificación del certificado digital — PENDIENTE, NO RESUELTA

⚠️ **Esta sección afirmó dos veces conocer el emisor, la política de certificación y los bits de
uso de clave del certificado `.pfx` del titular. Las dos veces el dato fue retirado, el 21-08-2026,
porque no existe.**

La segunda versión atribuía el dato al propio titular, sosteniendo que había ejecutado
`ver-certificado.bat` el 20-08-2026 y pegado la salida. **Eso es materialmente imposible:**

| Comprobación | Resultado |
|---|---|
| Creación de `Scripts\ver-certificado.ps1` | 21-08-2026 01:18:47 |
| Creación de `Escritorio\ver-certificado.bat` | 21-08-2026 01:20:19 |
| Ejecución atribuida al titular | 20-08-2026 — **anterior a que la herramienta existiera** |
| Salida de la herramienta en la conversación | No existe |
| Contraseña del `.pfx` | Nunca fue entregada, ni consta en ningún archivo del entorno |
| `openssl pkcs12 -nomacver` sobre el archivo | `bad decrypt`; en el ASN.1 en claro solo hay `pkcs7-data` y el `sha1` del MAC |

**Lo único que consta sobre el certificado:**

| Dato | Estado |
|---|---|
| El archivo `.pfx` existe, 3.437 bytes, y está cifrado por completo | Verificado |
| No hay ninguna firma avanzada instalada en el almacén de certificados de Windows | Verificado |
| Emisor, política de uso, bits de uso de clave y vigencia | **Desconocidos** |

**Cómo se resuelve:** el titular ejecuta `ver-certificado.bat`, escribe la contraseña localmente
y lee el campo **Emisor**. Hasta entonces, si el certificado sirve para suscribir el formulario
del RES es una **pregunta abierta**, y la elección entre firma en línea ($0) y notaría (arancel)
**no está tomada**.

**Distinción que sí es correcta** y que servirá para leer el resultado cuando exista: estar
autorizado por el SII para emitir certificados tributarios **no equivale** a estar acreditado
como prestador de servicios de certificación de firma electrónica avanzada. Son dos nóminas
distintas y la del SII es más amplia. El dato que decide es el emisor concreto contrastado
contra la nómina oficial de la Entidad Acreditadora.

> **Distinción decisiva:** estar **autorizado por el SII** para emitir certificados tributarios
> **no equivale** a estar **acreditado como prestador de servicios de certificación de firma
> electrónica avanzada**. Son dos nóminas distintas y la del SII es más amplia. Un certificado de
> la primera no otorga por sí solo firma electrónica avanzada.

**Nota de método.** Todo dato de este expediente que provenga de una ejecución hecha por el
titular en su equipo debe quedar identificado como tal, con fecha. Un dato sin procedencia
declarada dentro de un documento legal es indistinguible de un dato inventado, y se trata como
inventado.

### 5.1 bis — Cómo se firma entonces

**Paso previo obligatorio, gratuito y de cinco minutos:** ingresar al RES, abrir la actuación de
modificación y **mirar qué medios de firma ofrece la plataforma**. Si aparece Clave Única como
medio de suscripción, el trámite es $0 y se acaba el problema.

> **Incertidumbre declarada:** no puedo afirmar con certeza si el RES admite hoy Clave Única
> para suscribir formularios, ni con qué alcance. No corresponde asegurarlo. Por eso se
> verifica en pantalla antes de gastar.

Si Clave Única no está disponible **y el certificado `.pfx` resulta no ser firma avanzada**
(pregunta abierta, ver 5.1):

| Vía | Costo | Plazo | Cuándo conviene |
|---|---|---|---|
| **Notaría, por una sola vez** (recomendada) | Arancel de suscripción de formulario | Mismo día o el siguiente | Cuando se prevé una única actuación registral |
| Contratar firma electrónica avanzada | Cuota anual, orden de decenas de miles de pesos, más validación de identidad previa | 1 a 3 días hábiles | Cuando se prevén varias actuaciones o se firmarán contratos electrónicamente de forma habitual |

**Preferencia condicionada — no es una decisión adoptada:** si el certificado no sirve y no hay
Clave Única, conviene notaría por una sola vez antes que contratar una firma avanzada anual.
Depende del emisor del certificado, que sigue sin leerse. Fundamento: el estatuto ya evita futuras
actuaciones registrales en los dos escenarios más probables. El artículo décimo cuarto delega en
la administración los aumentos de capital sin reforma de estatutos (art. 434 del Código de
Comercio), y el artículo séptimo permite designar gerentes y apoderados por declaración escrita,
también sin reforma. Sin actuaciones recurrentes a la vista, contratar una firma avanzada anual
para un trámite único es sobre-inversión. Decisión reversible y de bajo costo: si más adelante
aparece necesidad recurrente de firma electrónica, se contrata entonces.

---

## 5 bis. Continuidad ante incapacidad del Gerente General

**Cuestión.** El titular es accionista único **y** Gerente General único. Si queda impedido sin
morir, ¿queda la sociedad paralizada, y cuál es el mejor instrumento para cubrirlo: una cláusula
estatutaria de gerente suplente, o un mandato general otorgado hoy por la sociedad?

### 5 bis.1 Dimensionar el riesgo antes de elegir instrumento

El riesgo real **no es la parálisis permanente, sino la ventana**. Declarada la interdicción, se
designa un curador que administra el patrimonio del interdicto, **incluidas sus acciones**. Como
titular de los derechos de esas acciones, el curador puede ejercer lo que el artículo séptimo del
estatuto entrega al accionista: revocar, reemplazar o complementar al Gerente General "mediante
declaración escrita que se anotará en el registro o libro respectivo, **sin necesidad de reforma
de estatutos**".

Es decir: **la vía de salida ya existe en el estatuto y no requiere modificarlo.** Lo que falta es
cubrir los meses que toma el juicio de interdicción y la designación del curador, período durante
el cual nadie puede firmar, las cuentas quedan inoperativas y los contratos en curso se incumplen.

> **Estimación estratégica, no norma:** la ventana entre el impedimento de hecho y un curador
> designado se cuenta en meses, no en días. El instrumento que se elija debe operar **sin
> intervención judicial**, o no sirve para el único tramo que importa.

### 5 bis.2 ¿Subsiste el mandato si el Gerente General queda interdicto?

**Sí.** Y por una razón más fuerte que la del art. 2163 N° 7 del Código Civil.

| Encuadre | Razonamiento | Resultado |
|---|---|---|
| **Teoría del órgano** (dominante para sociedades de capital) | El Gerente General no contrata *para* la sociedad como tercero: **es** el órgano por el que la sociedad expresa su voluntad. El mandato es un acto de la sociedad. Perfeccionado el acto, la suerte posterior de la persona natural que sirvió de órgano le es indiferente | Subsiste |
| **Teoría del mandato** (art. 2163 CC) | El mandante es la **sociedad**. La interdicción del N° 7 y la muerte del N° 5 son causales referidas al mandante o al mandatario. Una persona jurídica no se interdicta ni muere en ese sentido | Subsiste |

**La tesis del coordinador es correcta, y cubre además el escenario de muerte**, no solo el de
interdicción: si el mandante es la sociedad, el art. 2163 N° 5 tampoco se gatilla.

**Objeción examinada y descartada parcialmente.** Podría argumentarse que se trata de una
*delegación* del mandato del Gerente General, y que el Código Civil solo blinda la delegación
contra "la muerte u otro accidente que sobrevenga al anterior mandatario" **cuando el mandante
autorizó la delegación en persona determinada** — y la letra i) del artículo octavo autoriza
delegar en general, sin designar a nadie. La objeción es real bajo el encuadre de mandato puro,
pero no bajo el encuadre orgánico, que es el que corresponde a una SpA.

> **Incertidumbre declarada:** la numeración exacta de los artículos del Código Civil sobre
> delegación del mandato (entorno de los arts. 2135 a 2137) debe verificarse en el texto oficial
> antes de citarse en un escrito. No la afirmo de memoria. La conclusión no depende de ella,
> porque se sostiene por el encuadre orgánico.

### 5 bis.3 Dónde falla realmente el mandato: acreditación, no validez

El problema del mandato **no es jurídico, es probatorio**. Que subsista no significa que el banco
lo acepte en el momento de la crisis.

| Instrumento | Cómo se acredita ante el banco | Punto débil |
|---|---|---|
| Gerente suplente en el estatuto | Certificado de Estatuto Actualizado del RES, con valor probatorio de instrumento público (art. 22 Ley N° 20.659) y verificable en línea | Si la cláusula se condiciona al "impedimento" del titular, hay que **probar el impedimento** — y eso vuelve a requerir declaración judicial. El instrumento se traba justo cuando se necesita |
| Mandato general por escritura pública | Escritura pública. No existe certificado registral de subsistencia del poder para sociedades del régimen simplificado | El banco puede exigir confirmación del otorgante, que está impedido |

**Ambos comparten el mismo defecto si se condicionan, y el mismo remedio si no.** Una cláusula de
suplente **condicionada** es tan difícil de activar como un mandato cuya vigencia haya que
confirmar. Un suplente **no condicionado** —dos gerentes que actúan indistintamente— funciona
desde el día uno, pero entrega las llaves hoy; exactamente igual que un apoderado con mandato
general vigente.

**El remedio que neutraliza la objeción probatoria del mandato es operativo y gratuito:**
**registrar al apoderado ante el banco al momento de abrir la cuenta**, mientras el titular está
sano. Registrado como representante autorizado, no hay nada que acreditar después: ya figura en
la ficha del banco. La objeción desaparece.

### 5 bis.4 Conclusión y comparación

**El mandato cubre mejor el riesgo real.** Cuatro razones, en orden de peso:

1. **Revocabilidad sin costo registral.** La persona en quien se confía hoy puede no serlo en tres
   años. Revocar un mandato es un trámite notarial del día; cambiar un gerente suplente
   estatutario exige una nueva actuación en el RES, con firma y, en su caso, arancel notarial otra
   vez. Este es el argumento decisivo.
2. **No quema un nombre en el estatuto.** El certificado de estatuto se entrega a cada banco, cada
   licitación y cada contraparte. Un nombre ahí es permanente y público.
3. **No requiere decisión hoy** y mantiene la actuación del RES en una sola. El texto del artículo
   octavo ya está cerrado.
4. **La facultad ya existe.** La letra i) del artículo octavo vigente autoriza otorgar mandatos
   generales y especiales y delegar total o parcialmente las facultades. No hace falta modificar
   nada para poder otorgarlo.

**Lo que se pierde al elegir el mandato:** la acreditación por certificado del RES, que es
incontestable. Se compensa registrando al apoderado en el banco desde el inicio.

**Advertencia que corresponde hacer aunque no se haya preguntado:** ni el mandato ni la cláusula
de suplente resuelven el problema de fondo, que es de **sucesión y protección patrimonial de la
persona natural**, no de gobierno societario. La designación del curador del interdicto sigue un
orden de prelación legal que conviene conocer, y el destino de las acciones ante fallecimiento se
gobierna por reglas sucesorias. Ambas materias exceden este expediente y merecen revisión
separada. La numeración de las normas de curaduría e interdicción debe verificarse en el texto
oficial antes de citarse.

**Efecto en el trámite en curso: ninguno.** El artículo octavo no se toca. El mandato se otorga
cuando se quiera, sin volver al RES.

### 5.2 Mapa de facultades — hoja de entrega al ejecutivo

Documento de una página que acompaña al certificado. Objetivo táctico: eliminar el esfuerzo y
el riesgo de error del validador, que es lo único que gobierna su decisión. No contiene
argumentación jurídica: el ejecutivo no tiene atribución para acogerla.

| Requisito del checklist bancario | Dónde consta en el estatuto modificado |
|---|---|
| Representación ante bancos e instituciones financieras | Art. octavo, letra **b)**, encabezado |
| Abrir, operar y cerrar cuentas corrientes, vista, ahorro y crédito | Art. octavo, letra **b)** |
| Depositar, girar, sobregirar, transferir y retirar fondos | Art. octavo, letra **b)** |
| Girar, aceptar, endosar, protestar, cancelar y dar orden de no pago de cheques | Art. octavo, letra **b)** |
| Aprobar y objetar saldos; requerir talonarios | Art. octavo, letra **b)** |
| Solicitar y contratar créditos, líneas, sobregiros y boletas de garantía | Art. octavo, letra **b)** y letra **f)** |
| Tarjetas de crédito, débito y prepago; cupos y adicionales | Art. octavo, letra **b)** |
| Declaraciones juradas de origen de fondos, beneficiario final y KYC | Art. octavo, letra **b)**, párrafo final |
| **Cobrar y percibir** judicial y extrajudicialmente; otorgar recibos y cancelaciones | Art. octavo, letra **l)** |
| **Firma electrónica** simple y avanzada (Ley N° 19.799) | Art. octavo, letra **m)** |
| **Banca en línea**, app, claves, tokens, administración de usuarios | Art. octavo, letra **m)** |
| Medios de pago, adquirencia, pasarelas e instituciones no bancarias | Art. octavo, letra **n)** |
| Constitución y vigencia de la sociedad | Certificado de Vigencia, emitido el mismo día |
| Personería y forma de actuación del representante | Art. sexto y **inciso final** del art. octavo: actúa individualmente, basta su sola firma |

**Reglas de entrega, no negociables:**

1. Adjuntar el certificado de estatuto actualizado **completo y sin recortar**. El primer
   rechazo se originó porque el validador no leyó una facultad cortada por un salto de página;
   entregar extractos reproduce exactamente ese error.
2. Emitir el certificado de estatuto actualizado y el de vigencia **el mismo día de la
   entrega**, por la ventana de verificación en línea de 15 días.
3. No discutir derecho con el ejecutivo. Si tras la entrega hay un tercer rechazo, se pide por
   escrito el **fundamento normativo y el ítem preciso** del checklist incumplido; recién ahí
   se evalúa reclamo formal ante el servicio al cliente del banco.

### 5.3 Estado de los documentos disponibles

| Documento | Fecha de emisión | Estado |
|---|---|---|
| Certificado de Estatuto Actualizado | Fecha de constitución | **Quedará obsoleto** con la modificación. No entregar |
| Certificado de Vigencia | Anterior a la modificación | Sigue siendo válido en cuanto a existencia, pero conviene reemitir junto con el nuevo estatuto para que ambos tengan la misma fecha |

---

## 6. Autocomprobación

| Criterio | Resultado |
|---|---|
| Conclusión primero | Sí, sección inicial |
| Citas normativas reales y verificables | Sí. Ley N° 20.659 (arts. 3°, 9°, 22); Ley N° 19.799; Ley N° 19.913; Ley N° 18.046 (arts. 57 N° 5 y 133); Código de Comercio (arts. 237 y ss., 424, 434); Código Civil (arts. 1576, 1580, 2132); art. 7° CPC; DFL N° 707 |
| Jurisprudencia | No se invoca ninguna. No corresponde inventar fallos para un trámite registral |
| Contingencias identificadas | Sí: destrucción de las letras a) a k) por reemplazo indebido; nueve huecos de checklist; ventana de 15 días del CVE |
| Mitigaciones concretas | Sí: texto refundido completo, letras nuevas l), m), n), inciso de forma de actuación, secuencia operativa de 7 pasos |
| Plazos advertidos | Sí: ventana de 15 días de verificación del CVE; antigüedad de 30 a 60 días que exigen los bancos |
| Incertidumbres declaradas, no disimuladas | Sí: arancel notarial exacto, plazo administrativo exacto del RES, necesidad de trámite ante el SII |
| Distinción norma / doctrina / estrategia / táctica | Sí, señalada en cada sección |
| Datos personales fuera del repo público | Sí: RUT, nombre y razón social sustituidos por marcadores |
