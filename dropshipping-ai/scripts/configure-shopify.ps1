# Configura la tienda Shopify para el modo hibrido, desde tu PC (Windows).
# No requiere instalar nada: usa Windows PowerShell 5.1 (incluido en Windows).
#
# Que hace:
#   1. Valida el token contra la tienda.
#   2. Crea los 4 productos del catalogo con los SKUs EXACTOS de la base
#      interna (ME-001, ME-002, IS-101, IS-205), sin seguimiento de
#      inventario en Shopify (el stock real lo verifica el Agente B2B).
#   3. (Opcional) Crea el webhook orders/create hacia el gateway. Hazlo solo
#      cuando el VPS ya este desplegado; si no, dejalo en blanco y re-ejecuta
#      este script mas tarde (es idempotente: no duplica nada).
#
# Uso:  clic derecho > "Ejecutar con PowerShell", o en una consola:
#       powershell -ExecutionPolicy Bypass -File .\configure-shopify.ps1
#
# Mensajes sin tildes a proposito: PowerShell 5.1 lee mal el UTF-8 sin BOM.

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$ApiVersion = "2024-01"

Write-Host "== Configuracion de Shopify para el modo hibrido ==" -ForegroundColor Cyan

# --- Credenciales (no salen de esta maquina) ---
$Domain = Read-Host "Dominio myshopify de la tienda (ej. mitienda-1234.myshopify.com)"
$Domain = $Domain.Trim().ToLower() -replace "^https?://", "" -replace "/.*$", ""
if ($Domain -notlike "*.myshopify.com") {
    throw "El dominio debe terminar en .myshopify.com (recibido: $Domain)"
}

$TokenSecure = Read-Host "Admin API access token (shpat_...)" -AsSecureString
$Token = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($TokenSecure))
if ($Token -notlike "shpat_*") {
    Write-Host "AVISO: el token no empieza con shpat_ ; continuo igual..." -ForegroundColor Yellow
}

$Base = "https://$Domain/admin/api/$ApiVersion"
$Headers = @{ "X-Shopify-Access-Token" = $Token; "Content-Type" = "application/json" }

# --- 1. Validar acceso ---
$Shop = (Invoke-RestMethod -Uri "$Base/shop.json" -Headers $Headers -Method Get).shop
Write-Host ("OK: conectado a '" + $Shop.name + "' (" + $Shop.myshopify_domain + ", moneda " + $Shop.currency + ")") -ForegroundColor Green

# --- 2. Productos con los SKUs de la base interna ---
# Mismos SKUs y precios que db/seed.sql: la condicion para que el conector
# mapee los pedidos es que el SKU de la variante coincida con products.sku.
$Catalogo = @(
    @{ sku = "ME-001"; titulo = "Freidora de aire 5L";        tipo = "hogar";       precio = "42000" },
    @{ sku = "ME-002"; titulo = "Aspiradora robot compacta";  tipo = "hogar";       precio = "79900" },
    @{ sku = "IS-101"; titulo = "Audifonos inalambricos Pro"; tipo = "tecnologia";  precio = "21990" },
    @{ sku = "IS-205"; titulo = "Lampara de escritorio LED";  tipo = "iluminacion"; precio = "12990" }
)

$Existentes = (Invoke-RestMethod -Uri "$Base/products.json?limit=250&fields=id,title,variants" -Headers $Headers -Method Get).products
$SkusExistentes = @()
foreach ($p in $Existentes) { foreach ($v in $p.variants) { if ($v.sku) { $SkusExistentes += $v.sku } } }

foreach ($item in $Catalogo) {
    if ($SkusExistentes -contains $item.sku) {
        Write-Host ("Ya existe  " + $item.sku + "  (" + $item.titulo + ") - se omite")
        continue
    }
    $Body = @{
        product = @{
            title        = $item.titulo
            product_type = $item.tipo
            status       = "active"
            variants     = @(@{
                sku                = $item.sku
                price              = $item.precio
                requires_shipping  = $true
                # sin inventory_management: Shopify no controla stock;
                # el stock real lo confirma el Agente B2B con el proveedor
            })
        }
    } | ConvertTo-Json -Depth 5
    $Nuevo = Invoke-RestMethod -Uri "$Base/products.json" -Headers $Headers -Method Post -Body $Body
    Write-Host ("Creado     " + $item.sku + "  (" + $item.titulo + ", id " + $Nuevo.product.id + ")") -ForegroundColor Green
}

# --- 3. Webhook orders/create (solo con el gateway ya desplegado) ---
$GatewayUrl = Read-Host "URL del gateway para el webhook (ej. https://api.tudominio.cl) o ENTER para omitir"
if ($GatewayUrl.Trim()) {
    $Address = $GatewayUrl.Trim().TrimEnd("/") + "/webhooks/shopify"
    if ($Address -notlike "https://*") { throw "La URL del webhook debe ser https://" }
    $Webhooks = (Invoke-RestMethod -Uri "$Base/webhooks.json?limit=250" -Headers $Headers -Method Get).webhooks
    $YaExiste = $Webhooks | Where-Object { $_.topic -eq "orders/create" -and $_.address -eq $Address }
    if ($YaExiste) {
        Write-Host "Ya existe el webhook orders/create hacia $Address - se omite"
    } else {
        $Body = @{ webhook = @{ topic = "orders/create"; address = $Address; format = "json" } } | ConvertTo-Json -Depth 4
        $Wh = Invoke-RestMethod -Uri "$Base/webhooks.json" -Headers $Headers -Method Post -Body $Body
        Write-Host ("Creado webhook orders/create -> " + $Address + " (id " + $Wh.webhook.id + ")") -ForegroundColor Green
    }
    Write-Host ""
    Write-Host "IMPORTANTE (firma del webhook): los webhooks creados por API se" -ForegroundColor Yellow
    Write-Host "firman con el CLIENT SECRET de tu app del Dev Dashboard (no con el" -ForegroundColor Yellow
    Write-Host "secreto que muestra la pantalla de webhooks del admin). En el" -ForegroundColor Yellow
    Write-Host ".env.prod usa:  SHOPIFY_WEBHOOK_SECRET = Client Secret de la app" -ForegroundColor Yellow
} else {
    Write-Host "Webhook omitido. Re-ejecuta este script cuando el VPS este desplegado."
}

# --- Resumen ---
Write-Host ""
Write-Host "== Listo. Valores para infra/.env.prod del VPS ==" -ForegroundColor Cyan
Write-Host ("SHOPIFY_STORE_DOMAIN=" + $Domain)
Write-Host "SHOPIFY_ADMIN_TOKEN=(el shpat_ que ingresaste)"
Write-Host "SHOPIFY_WEBHOOK_SECRET=(Client Secret de la app en el Dev Dashboard)"
Write-Host ""
Write-Host "Pendientes manuales en el admin de Shopify:"
Write-Host " - Contra entrega: Configuracion > Pagos > Metodos de pago manuales > Cash on Delivery"
Write-Host " - Fotos y descripciones de los 4 productos; tema visual de la tienda"
Write-Host " - Corregir tildes en los titulos si quieres (ej. Audifonos -> con tilde);"
Write-Host "   el mapeo de pedidos usa el SKU, asi que el titulo puede editarse libremente"
