# Configura la zona DNS del dominio en Cloudflare, desde tu PC (Windows).
# No requiere instalar nada: usa Windows PowerShell 5.1 (incluido en Windows).
#
# Que hace:
#   1. Verifica el API token y detecta el Account ID.
#   2. Crea la zona si no existe (plan Free) y muestra los NAMESERVERS que
#      hay que declarar en NIC Chile.
#   3. (Opcional) Apunta la raiz y www a Shopify, que es la vitrina publica
#      del modo hibrido. Esto NO depende del VPS: se puede hacer de inmediato.
#   4. (Opcional) Crea/actualiza los registros A de hola, panel y api
#      apuntando a la IP del VPS. Hazlo solo cuando el VPS ya exista; si no,
#      deja la IP en blanco y re-ejecuta este script mas tarde.
#
# Reparto del dominio en modo hibrido:
#   raiz y www  -> Shopify (vitrina y checkout), TLS emitido por Shopify
#   hola        -> VPS, tienda propia (canal secundario), TLS por Caddy
#   panel       -> VPS, dashboard del Supervisor
#   api         -> VPS, gateway y webhook orders/create
#
# TODOS los registros se crean en DNS-only (nube gris) A PROPOSITO, por dos
# motivos independientes que apuntan a lo mismo: Caddy necesita el desafio
# HTTP-01 de ACME para los subdominios, y Shopify NO soporta el proxy de
# Cloudflare en la raiz (deja el certificado colgado en "pending").
#
# ORDEN CORRECTO para un dominio .cl que AUN NO esta inscrito:
#   a) correr este script sin IP  -> obtienes los nameservers
#   b) inscribir el dominio en NIC Chile declarando esos nameservers
#   c) cuando exista el VPS, re-ejecutar este script con la IP
#
# Uso:  powershell -ExecutionPolicy Bypass -File .\configure-cloudflare.ps1
#       powershell -ExecutionPolicy Bypass -File .\configure-cloudflare.ps1 -Dominio compay.cl
#
# Mensajes sin tildes a proposito: PowerShell 5.1 lee mal el UTF-8 sin BOM.

param(
    [string]$Dominio = "compai.cl",
    # Agrega el AAAA de Shopify en la raiz. Opcional: Shopify lo documenta,
    # pero un AAAA equivocado rompe solo a los usuarios con IPv6 mientras el
    # resto navega bien, que es una falla dificil de notar. Por eso no va por
    # defecto: activalo si el panel de Shopify te lo pide explicitamente.
    [switch]$ConIPv6
)

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$Api = "https://api.cloudflare.com/client/v4"

Write-Host "== Configuracion de la zona $Dominio en Cloudflare ==" -ForegroundColor Cyan

# --- Credenciales (no salen de esta maquina) ---
$TokenSecure = Read-Host "API token de Cloudflare" -AsSecureString
$Token = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($TokenSecure))
if (-not $Token) { throw "El API token es obligatorio" }

$Headers = @{ "Authorization" = "Bearer $Token"; "Content-Type" = "application/json" }

# Llama a la API y desenvuelve el sobre {success, errors, result} de Cloudflare.
# En PS 5.1 un 4xx lanza excepcion, asi que hay que leer el cuerpo a mano para
# mostrar el mensaje real en vez de un "400 Bad Request" pelado.
function Invoke-CF([string]$Ruta, [string]$Metodo = "GET", $Cuerpo = $null) {
    $params = @{ Uri = "$Api$Ruta"; Headers = $Headers; Method = $Metodo }
    if ($Cuerpo -ne $null) { $params.Body = ($Cuerpo | ConvertTo-Json -Depth 8 -Compress) }
    try {
        $r = Invoke-RestMethod @params
    } catch {
        $detalle = ""
        if ($_.Exception.Response) {
            $sr = New-Object IO.StreamReader($_.Exception.Response.GetResponseStream())
            $texto = $sr.ReadToEnd(); $sr.Close()
            try {
                $j = $texto | ConvertFrom-Json
                $detalle = ($j.errors | ForEach-Object { "[$($_.code)] $($_.message)" }) -join " | "
            } catch { $detalle = $texto }
        }
        throw ("Cloudflare $Metodo $Ruta -> " + $_.Exception.Message + " :: " + $detalle)
    }
    if (-not $r.success) {
        throw ("Cloudflare: " + (($r.errors | ForEach-Object { "[$($_.code)] $($_.message)" }) -join " | "))
    }
    return $r.result
}

# --- 1. Verificar token ---
$verif = Invoke-CF "/user/tokens/verify"
Write-Host ("OK: token valido (estado: " + $verif.status + ")") -ForegroundColor Green

# --- 2. Account ID ---
try {
    $cuentas = @(Invoke-CF "/accounts")
} catch {
    Write-Host "AVISO: el token no puede listar cuentas; pide el Account ID a mano." -ForegroundColor Yellow
    $cuentas = @()
}
if ($cuentas.Count -eq 1) {
    $AccountId = $cuentas[0].id
    Write-Host ("Cuenta: " + $cuentas[0].name + " (" + $AccountId + ")")
} elseif ($cuentas.Count -gt 1) {
    Write-Host "Hay varias cuentas:"
    for ($i = 0; $i -lt $cuentas.Count; $i++) { Write-Host ("  [$i] " + $cuentas[$i].name + "  " + $cuentas[$i].id) }
    $sel = Read-Host "Indice de la cuenta a usar"
    $AccountId = $cuentas[[int]$sel].id
} else {
    # Un token con permisos solo de zona no puede listar cuentas (/accounts
    # devuelve vacio y /memberships da 10000). No es un problema: si se omite
    # el campo account, Cloudflare lo infiere para usuarios de una sola cuenta.
    Write-Host "El token no puede listar cuentas (normal si solo tiene permisos de zona)." -ForegroundColor Yellow
    $AccountId = (Read-Host "Account ID, o ENTER para que Cloudflare lo infiera").Trim()
}

# --- 3. Zona: crear si no existe (idempotente) ---
$zonas = @(Invoke-CF "/zones?name=$Dominio")
if ($zonas.Count -gt 0) {
    $Zona = $zonas[0]
    Write-Host ("Ya existe la zona " + $Dominio + " (id " + $Zona.id + ", estado " + $Zona.status + ") - se reutiliza")
} else {
    $nueva = @{ name = $Dominio; type = "full" }
    if ($AccountId) { $nueva.account = @{ id = $AccountId } }
    $Zona = Invoke-CF "/zones" "POST" $nueva
    Write-Host ("Creada la zona " + $Dominio + " (id " + $Zona.id + ", estado " + $Zona.status + ")") -ForegroundColor Green
}

Write-Host ""
Write-Host "== NAMESERVERS para declarar en NIC Chile ==" -ForegroundColor Cyan
foreach ($ns in $Zona.name_servers) { Write-Host ("   " + $ns) -ForegroundColor Green }
Write-Host ""
if ($Zona.status -ne "active") {
    Write-Host "La zona esta en estado '$($Zona.status)': Cloudflare aun no ve la delegacion." -ForegroundColor Yellow
    Write-Host "Se activara sola cuando NIC Chile publique esos nameservers." -ForegroundColor Yellow
    Write-Host ""
}

# Crea o corrige un registro, comparando contra los ya existentes. Todos van
# en DNS-only: el proxy naranja rompe el ACME de Caddy en los subdominios y la
# validacion de Shopify en la raiz. "@" significa la raiz del dominio.
function Set-Registro($Zona, $Existentes, [string]$Tipo, [string]$Nombre, [string]$Contenido) {
    $fqdn = if ($Nombre -eq "@") { $Dominio } else { "$Nombre.$Dominio" }
    $cuerpo = @{ type = $Tipo; name = $Nombre; content = $Contenido; ttl = 300; proxied = $false }
    $actual = $Existentes | Where-Object { $_.type -eq $Tipo -and $_.name -eq $fqdn }

    if ($actual) {
        if ($actual.content -eq $Contenido -and -not $actual.proxied) {
            Write-Host ("Ya correcto  " + $fqdn.PadRight(28) + $Tipo.PadRight(6) + $Contenido)
            return
        }
        [void](Invoke-CF ("/zones/" + $Zona.id + "/dns_records/" + $actual.id) "PUT" $cuerpo)
        Write-Host ("Actualizado  " + $fqdn.PadRight(28) + $Tipo.PadRight(6) + $Contenido) -ForegroundColor Green
    } else {
        [void](Invoke-CF ("/zones/" + $Zona.id + "/dns_records") "POST" $cuerpo)
        Write-Host ("Creado       " + $fqdn.PadRight(28) + $Tipo.PadRight(6) + $Contenido) -ForegroundColor Green
    }
}

$existentes = @(Invoke-CF ("/zones/" + $Zona.id + "/dns_records?per_page=100"))

# --- 4. Shopify en la raiz (no depende del VPS: se puede hacer ya) ---
# En modo hibrido la vitrina publica es Shopify, que se queda con la raiz y
# con www. Valores de la guia oficial de Shopify para dominios de terceros.
$ShopifyIp = "23.227.38.65"
$ShopifyCname = "shops.myshopify.com"

$resp = Read-Host "Apuntar la raiz y www a Shopify (vitrina publica)? [s/N]"
if ($resp -match '^[sSyY]') {
    Set-Registro $Zona $existentes "A"     "@"   $ShopifyIp
    Set-Registro $Zona $existentes "CNAME" "www" $ShopifyCname
    if ($ConIPv6) {
        Set-Registro $Zona $existentes "AAAA" "@" "2620:0127:f00f:5::"
    } else {
        Write-Host "AAAA (IPv6) omitido. Shopify lo documenta como opcional; si su panel" -ForegroundColor Yellow
        Write-Host "te lo pide, re-ejecuta con -ConIPv6." -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "En Shopify: Configuracion > Dominios > $Dominio > cambiar tipo a" -ForegroundColor Yellow
    Write-Host "DOMINIO PRINCIPAL (no 'redireccion', que dejaria el .myshopify.com a la" -ForegroundColor Yellow
    Write-Host "vista, ni 'alias', que duplica contenido y perjudica el SEO)." -ForegroundColor Yellow
    Write-Host ""
    $existentes = @(Invoke-CF ("/zones/" + $Zona.id + "/dns_records?per_page=100"))
} else {
    Write-Host "Registros de Shopify omitidos."
}

# --- 5. Subdominios del VPS (solo con el VPS ya creado) ---
$Ip = Read-Host "IP publica del VPS para los registros A, o ENTER para omitir"
if ($Ip.Trim()) {
    $Ip = $Ip.Trim()
    if ($Ip -notmatch '^\d{1,3}(\.\d{1,3}){3}$') { throw "IPv4 invalida: $Ip" }
    foreach ($octeto in $Ip.Split(".")) {
        if ([int]$octeto -gt 255) { throw "IPv4 invalida (octeto > 255): $Ip" }
    }

    # Subdominios del Caddyfile: STORE_DOMAIN, DASHBOARD_DOMAIN, API_DOMAIN.
    # "hola" y no "tienda": la vitrina publica vive en la raiz del dominio
    # (Shopify), y llamar "tienda" al canal secundario invita a confusion.
    foreach ($s in @("hola", "panel", "api")) {
        Set-Registro $Zona $existentes "A" $s $Ip
    }

    Write-Host ""
    Write-Host "== Valores para infra/.env.prod del VPS ==" -ForegroundColor Cyan
    Write-Host ("STORE_DOMAIN=hola." + $Dominio)
    Write-Host ("DASHBOARD_DOMAIN=panel." + $Dominio)
    Write-Host ("API_DOMAIN=api." + $Dominio)
} else {
    Write-Host "Registros del VPS omitidos. Re-ejecuta este script cuando exista."
}

Write-Host ""
Write-Host "Siguientes pasos:"
if ($Zona.status -ne "active") {
    Write-Host " 1. Inscribir $Dominio en NIC Chile (https://www.nic.cl) declarando los"
    Write-Host "    nameservers de arriba. Asi la zona queda delegada desde el minuto cero."
    Write-Host " 2. Esperar la propagacion y verificar:  nslookup -type=NS $Dominio"
    Write-Host " 3. Con el VPS creado, re-ejecutar este script con la IP."
} else {
    Write-Host " - Zona activa. Con el VPS creado, re-ejecutar este script con la IP."
}
Write-Host ""
Write-Host "TODOS los registros quedan en DNS-only (nube gris) a proposito: Caddy" -ForegroundColor Yellow
Write-Host "emite el TLS por ACME en los subdominios, y Shopify no soporta el proxy" -ForegroundColor Yellow
Write-Host "de Cloudflare en la raiz. No actives el naranjo en esta zona." -ForegroundColor Yellow
