import { ArgumentsHost, Catch, Logger, ServiceUnavailableException } from "@nestjs/common";
import { BaseExceptionFilter } from "@nestjs/core";

/**
 * Códigos con los que Postgres o el socket avisan que **no se pudo hablar con
 * la base**, no que la consulta estuviera mal. Un error de SQL (42601, 23505…)
 * no está aquí a propósito: ese sí es culpa de quien pregunta o de un bug, y
 * debe seguir saliendo como 500 o como el error que corresponda.
 */
const CODIGOS_SIN_CONEXION = new Set([
  "ECONNREFUSED", // no hay nadie escuchando
  "ENOTFOUND", // el host no resuelve
  "EHOSTUNREACH",
  "ENETUNREACH",
  "ECONNRESET",
  "EPIPE",
  "ETIMEDOUT",
  "57P01", // admin_shutdown: la base se detuvo
  "57P02", // crash_shutdown
  "57P03", // cannot_connect_now: arrancando todavía
  "08000", // connection_exception
  "08001",
  "08003",
  "08004",
  "08006", // connection_failure
]);

/** Fallos del pool que llegan sin código, solo con mensaje. */
const MENSAJES_SIN_CONEXION = [
  "connection terminated",
  "timeout exceeded when trying to connect",
  "is not queryable",
  "connection ended unexpectedly",
];

export function esBaseInalcanzable(e: unknown): boolean {
  if (!e || typeof e !== "object") return false;
  const codigo = (e as { code?: unknown }).code;
  if (typeof codigo === "string" && CODIGOS_SIN_CONEXION.has(codigo)) return true;
  const mensaje = String((e as { message?: unknown }).message ?? "").toLowerCase();
  return MENSAJES_SIN_CONEXION.some((m) => mensaje.includes(m));
}

/**
 * Traduce "no se pudo hablar con Postgres" a 503 en cualquier ruta.
 *
 * Sin esto, perder la base convertía cada petición en un 500 "Internal server
 * error": el mismo código con el que se reporta un bug del API. Desde fuera —un
 * monitor, la tienda, el dashboard— no había forma de distinguir "este servicio
 * está roto" de "su base no está, vuelve a intentar". Solo /health lo
 * distinguía, y solo para sí mismo.
 *
 * 503 dice lo correcto: transitorio y reintentable. Es el mismo criterio que ya
 * aplicaba HealthController y, desde el arreglo del agents-service, el checkout.
 */
@Catch()
export class DbUnavailableFilter extends BaseExceptionFilter {
  private readonly log = new Logger(DbUnavailableFilter.name);

  catch(exception: unknown, host: ArgumentsHost) {
    if (esBaseInalcanzable(exception)) {
      // El detalle al log; hacia fuera nada sobre el host ni el motor.
      this.log.error(`base inalcanzable: ${(exception as Error).message}`);
      super.catch(
        new ServiceUnavailableException({
          estado: "degradado",
          db: false,
          mensaje: "La base de datos no está disponible; reintenta en unos momentos.",
        }),
        host,
      );
      return;
    }
    super.catch(exception, host);
  }
}
