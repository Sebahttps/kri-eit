import {
  Controller,
  Get,
  Inject,
  ServiceUnavailableException,
} from "@nestjs/common";
import { Pool } from "pg";
import { DB } from "../db/db.module";

/**
 * Sonda para monitores externos.
 *
 * Responde 200 solo si el proceso vive **y** la base contesta. Un health que
 * se limita a confirmar que el proceso existe no distingue el caso que más
 * importa: el gateway arrancó, acepta conexiones y devuelve errores en cada
 * petición porque perdió Postgres. Desde fuera eso se ve igual que estar sano.
 *
 * No expone versiones, nombres de host ni detalles del error: es público y sin
 * autenticar, y esos datos solo le sirven a quien busca por dónde entrar.
 */
@Controller("health")
export class HealthController {
  constructor(@Inject(DB) private readonly db: Pool) {}

  @Get()
  async estado() {
    try {
      await this.db.query("SELECT 1");
    } catch {
      // 503 y no 500: le dice al monitor "no disponible ahora", que es una
      // condición reintentable y transitoria, en vez de "error del servidor".
      throw new ServiceUnavailableException({ estado: "degradado", db: false });
    }
    return { estado: "ok", db: true };
  }
}
