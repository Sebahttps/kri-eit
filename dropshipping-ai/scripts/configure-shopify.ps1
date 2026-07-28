# Configura la tienda Shopify para el modo hibrido, desde tu PC (Windows).
# No requiere instalar nada: usa Windows PowerShell 5.1 (incluido en Windows).
#
# CREDENCIALES (cambio de enero 2026): las apps personalizadas ya no se crean
# en el admin y las del Dev Dashboard NO muestran un token shpat_ permanente.
# Este script pide Client ID + Client Secret y acuna el token el mismo, via
# client credentials grant (dura 24 h). Requisito: la app y la tienda deben
# estar en la MISMA organizacion de Shopify.
#
# Que hace:
#   1. Intercambia las credenciales por un token y valida el acceso.
#   2. Crea los 4 productos del catalogo con los SKUs EXACTOS de la base
#      interna (ME-001, ME-002, IS-101, IS-205), sin seguimiento de
#      inventario en Shopify (el stock real lo verifica el Agente B2B).
#   3. (Opcional) Crea el webhook orders/create hacia el gateway. Hazlo solo
#      cuando el VPS ya este desplegado; si no, dejalo en blanco y re-ejecuta
#      este script mas tarde (es idempotente: no duplica nada).
#
# Usa la Admin API GraphQL: las APIs REST de productos estan deprecadas y en
# modo mantenimiento desde 2025.
#
# Uso:  clic derecho > "Ejecutar con PowerShell", o en una consola:
#       powershell -ExecutionPolicy Bypass -File .\configure-shopify.ps1
#
# Mensajes sin tildes a proposito: PowerShell 5.1 lee mal el UTF-8 sin BOM.

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$ApiVersion = "2026-04"

Write-Host "== Configuracion de Shopify para el modo hibrido ==" -ForegroundColor Cyan

# --- Credenciales (no salen de esta maquina) ---
$Domain = Read-Host "Dominio myshopify de la tienda (ej. mitienda-1234.myshopify.com)"
$Domain = $Domain.Trim().ToLower() -replace "^https?://", "" -replace "/.*$", ""
if ($Domain -notlike "*.myshopify.com") {
    throw "El dominio debe terminar en .myshopify.com (recibido: $Domain)"
}

$ClientId = (Read-Host "Client ID de la app (Dev Dashboard > tu app > Settings)").Trim()
$SecretSecure = Read-Host "Client Secret de la app" -AsSecureString
$ClientSecret = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecretSecure))
if (-not $ClientId -or -not $ClientSecret) { throw "Client ID y Client Secret son obligatorios" }

# --- 1. Acunar el token y validar acceso ---
Write-Host "Intercambiando credenciales por un token de 24 h..."
try {
    $Auth = Invoke-RestMethod -Method Post -Uri "https://$Domain/admin/oauth/access_token" `
        -ContentType "application/x-www-form-urlencoded" `
        -Body @{ grant_type = "client_credentials"; client_id = $ClientId; client_secret = $ClientSecret }
} catch {
    Write-Host "FALLO el intercambio de credenciales." -ForegroundColor Red
    Write-Host "Causas tipicas:" -ForegroundColor Yellow
    Write-Host " - La app y la tienda estan en organizaciones distintas (client credentials" -ForegroundColor Yellow
    Write-Host "   exige la misma organizacion). Recrea la app desde la org duena de la tienda." -ForegroundColor Yellow
    Write-Host " - La app no esta instalada en la tienda (Dev Dashboard > app > Home > Install app)." -ForegroundColor Yellow
    Write-Host " - Client ID o Client Secret mal copiados." -ForegroundColor Yellow
    throw
}
$Token = $Auth.access_token
Write-Host ("OK: token obtenido (expira en " + $Auth.expires_in + "s). Scopes: " + $Auth.scope) -ForegroundColor Green

$GraphUrl = "https://$Domain/admin/api/$ApiVersion/graphql.json"
$Headers = @{ "X-Shopify-Access-Token" = $Token; "Content-Type" = "application/json" }

# Ejecuta una operacion GraphQL y aborta si hay errores de nivel superior.
function Invoke-Shopify([string]$Query, $Variables) {
    $Body = @{ query = $Query; variables = $Variables } | ConvertTo-Json -Depth 12 -Compress
    $Resp = Invoke-RestMethod -Uri $GraphUrl -Headers $Headers -Method Post -Body $Body
    if ($Resp.errors) {
        throw ("GraphQL: " + (($Resp.errors | ForEach-Object { $_.message }) -join " | "))
    }
    return $Resp.data
}

$Shop = (Invoke-Shopify 'query { shop { name myshopifyDomain currencyCode } }' @{}).shop
Write-Host ("OK: conectado a '" + $Shop.name + "' (" + $Shop.myshopifyDomain + ", moneda " + $Shop.currencyCode + ")") -ForegroundColor Green

# --- 2. Productos con los SKUs de la base interna ---
# Mismos SKUs y precios que db/seed.sql: la condicion para que el conector
# mapee los pedidos es que el SKU de la variante coincida con products.sku.
$Catalogo = @(
    @{ sku = "ME-001"; titulo = "Freidora de aire 5L";        tipo = "hogar";       precio = "42000" },
    @{ sku = "ME-002"; titulo = "Aspiradora robot compacta";  tipo = "hogar";       precio = "79900" },
    @{ sku = "IS-101"; titulo = "Audifonos inalambricos Pro"; tipo = "tecnologia";  precio = "21990" },
    @{ sku = "IS-205"; titulo = "Lampara de escritorio LED";  tipo = "iluminacion"; precio = "12990" }
)

$QueryVariante = @'
query($filtro: String!) {
  productVariants(first: 1, query: $filtro) { nodes { id sku } }
}
'@

$MutacionProducto = @'
mutation($input: ProductSetInput!) {
  productSet(synchronous: true, input: $input) {
    product { id title variants(first: 1) { nodes { sku price } } }
    userErrors { field message }
  }
}
'@

foreach ($item in $Catalogo) {
    $Existe = (Invoke-Shopify $QueryVariante @{ filtro = ("sku:" + $item.sku) }).productVariants.nodes
    if ($Existe -and @($Existe).Count -gt 0) {
        Write-Host ("Ya existe  " + $item.sku + "  (" + $item.titulo + ") - se omite")
        continue
    }

    # Producto de variante unica: el modelo nuevo exige igual una opcion.
    # tracked=false -> Shopify no controla stock; lo confirma el Agente B2B.
    $Input = @{
        title       = $item.titulo
        productType = $item.tipo
        status      = "ACTIVE"
        productOptions = @(
            @{ name = "Title"; values = @(@{ name = "Default Title" }) }
        )
        variants = @(
            @{
                sku           = $item.sku
                price         = $item.precio
                optionValues  = @(@{ optionName = "Title"; name = "Default Title" })
                inventoryItem = @{ tracked = $false; requiresShipping = $true }
            }
        )
    }

    $Res = (Invoke-Shopify $MutacionProducto @{ input = $Input }).productSet
    if ($Res.userErrors -and @($Res.userErrors).Count -gt 0) {
        throw ("No se pudo crear " + $item.sku + ": " +
               (($Res.userErrors | ForEach-Object { ($_.field -join ".") + " " + $_.message }) -join " | "))
    }
    Write-Host ("Creado     " + $item.sku + "  (" + $item.titulo + ", " + $Res.product.id + ")") -ForegroundColor Green
}

# --- 3. Webhook orders/create (solo con el gateway ya desplegado) ---
$GatewayUrl = Read-Host "URL del gateway para el webhook (ej. https://api.compai.cl) o ENTER para omitir"
if ($GatewayUrl.Trim()) {
    $Address = $GatewayUrl.Trim().TrimEnd("/") + "/webhooks/shopify"
    if ($Address -notlike "https://*") { throw "La URL del webhook debe ser https://" }

    $QuerySubs = @'
query {
  webhookSubscriptions(first: 250) {
    nodes {
      id
      topic
      endpoint { ... on WebhookHttpEndpoint { callbackUrl } }
    }
  }
}
'@
    $Suscripciones = (Invoke-Shopify $QuerySubs @{}).webhookSubscriptions.nodes
    $YaExiste = $Suscripciones | Where-Object {
        $_.topic -eq "ORDERS_CREATE" -and $_.endpoint.callbackUrl -eq $Address
    }
    if ($YaExiste) {
        Write-Host "Ya existe el webhook orders/create hacia $Address - se omite"
    } else {
        $MutacionWebhook = @'
mutation($topic: WebhookSubscriptionTopic!, $sub: WebhookSubscriptionInput!) {
  webhookSubscriptionCreate(topic: $topic, webhookSubscription: $sub) {
    webhookSubscription { id }
    userErrors { field message }
  }
}
'@
        $Res = (Invoke-Shopify $MutacionWebhook @{
            topic = "ORDERS_CREATE"
            sub   = @{ uri = $Address; format = "JSON" }
        }).webhookSubscriptionCreate
        if ($Res.userErrors -and @($Res.userErrors).Count -gt 0) {
            throw ("No se pudo crear el webhook: " +
                   (($Res.userErrors | ForEach-Object { ($_.field -join ".") + " " + $_.message }) -join " | "))
        }
        Write-Host ("Creado webhook orders/create -> " + $Address + " (" + $Res.webhookSubscription.id + ")") -ForegroundColor Green
    }
    Write-Host ""
    Write-Host "IMPORTANTE (firma del webhook): los webhooks creados por API se" -ForegroundColor Yellow
    Write-Host "firman con el CLIENT SECRET de tu app del Dev Dashboard. En el" -ForegroundColor Yellow
    Write-Host ".env.prod usa:  SHOPIFY_WEBHOOK_SECRET = Client Secret de la app" -ForegroundColor Yellow
} else {
    Write-Host "Webhook omitido. Re-ejecuta este script cuando el VPS este desplegado."
}

# --- Resumen ---
Write-Host ""
Write-Host "== Listo. Valores para infra/.env.prod del VPS ==" -ForegroundColor Cyan
Write-Host ("SHOPIFY_STORE_DOMAIN=" + $Domain)
Write-Host ("SHOPIFY_CLIENT_ID=" + $ClientId)
Write-Host "SHOPIFY_CLIENT_SECRET=(el Client Secret que ingresaste)"
Write-Host "SHOPIFY_WEBHOOK_SECRET=(el MISMO Client Secret)"
Write-Host ("SHOPIFY_API_VERSION=" + $ApiVersion)
Write-Host ""
Write-Host "NO uses SHOPIFY_ADMIN_TOKEN: el gateway acuna su propio token de 24 h" -ForegroundColor Yellow
Write-Host "con el Client ID/Secret y lo renueva solo." -ForegroundColor Yellow
Write-Host ""
Write-Host "Pendientes manuales en el admin de Shopify:"
Write-Host " - Contra entrega: Configuracion > Pagos > Metodos de pago manuales > Cash on Delivery"
Write-Host " - Fotos y descripciones de los 4 productos; tema visual de la tienda"
Write-Host " - Corregir tildes en los titulos si quieres (ej. Audifonos -> con tilde);"
Write-Host "   el mapeo de pedidos usa el SKU, asi que el titulo puede editarse libremente"
