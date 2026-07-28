# DNS de `compai.cl` en Cloudflare

La zona vive en Cloudflare (plan Free) y el dominio se inscribe en **NIC Chile**
(Cloudflare Registrar no vende `.cl`, así que el registro y la zona quedan en
sitios distintos: NIC Chile es el registrador, Cloudflare solo el DNS).

> **Atajo (Windows)**: [`scripts/configure-cloudflare.ps1`](../scripts/configure-cloudflare.ps1)
> hace los pasos 2 y 4 de abajo. Es idempotente: re-ejecutarlo no duplica nada
> y sirve tanto para crear la zona como para apuntar los registros A después.
> `-Dominio compay.cl` lo reutiliza para el dominio de redirección.

## Orden correcto (el dominio aún no está inscrito)

Es tentador inscribir primero y configurar el DNS después, pero **NIC Chile
pide los nameservers durante la inscripción**. Creando la zona antes, el
dominio queda delegado correctamente desde el minuto cero y se evita un
segundo trámite:

1. **Token de Cloudflare** — *dashboard → My Profile → API Tokens → Create
   Token → Custom token*:
   - Permisos: **Zone → Zone → Edit** (crear la zona) y **Zone → DNS → Edit**
     (los registros A).
   - Zone Resources: *Include → All zones from an account → (tu cuenta)*.
   - El secreto **se muestra una sola vez**.
2. **Crear la zona** — correr el script **sin IP** (ENTER en la pregunta de la
   IP). Devuelve los dos nameservers asignados, del tipo `xxx.ns.cloudflare.com`.
3. **Inscribir en NIC Chile** — https://www.nic.cl, declarando esos dos
   nameservers. La zona pasa sola de `pending` a `active` cuando NIC Chile
   publica la delegación. Verificar con:

   ```
   nslookup -type=NS compai.cl
   ```

4. **Registros A** — solo cuando el VPS exista: re-ejecutar el script e
   ingresar su IP pública. Crea `tienda`, `panel` y `api` (los tres subdominios
   del [`Caddyfile`](../infra/Caddyfile)).

## Por qué DNS-only (nube gris) y no proxy naranja

Los registros A se crean con `proxied: false` **a propósito**. Caddy emite y
renueva los certificados por ACME contra Let's Encrypt; con el proxy naranja
activo Cloudflare termina el TLS por su cuenta e interfiere con el desafío
HTTP-01, dejando a Caddy sin poder emitir.

Pasar a proxy naranja más adelante es posible —y aporta caché y mitigación de
DoS— pero exige cambiar antes la estrategia de TLS (modo *Full (strict)* con
certificado de origen de Cloudflare, o el desafío DNS-01 en Caddy). No es un
interruptor que se pueda dar vuelta sin tocar la configuración.

## Estado

| Elemento | Estado |
|---|---|
| `compai.cl` en NIC Chile | **No inscrito** (verificado 2026-07-28: WHOIS responde "Nombre de dominio no existe") |
| `compay.cl` en NIC Chile | No inscrito |
| Zona en Cloudflare | Pendiente de crear |
| Registros A | Pendientes — requieren la IP del VPS |
