import { Global, Logger, Module, OnApplicationShutdown } from "@nestjs/common";
import { Pool } from "pg";

export const DB = "DB_POOL";

export function databaseUrl(): string {
  return (
    process.env.BUSINESS_DATABASE_URL ??
    "postgresql://dropship:dropship@localhost:5432/dropship"
  );
}

@Global()
@Module({
  providers: [
    {
      provide: DB,
      useFactory: () => {
        const pool = new Pool({ connectionString: databaseUrl(), max: 10 });
        // Un cliente ocioso del pool que se cae emite 'error'. Sin manejador,
        // Node lo trata como excepción no capturada y mata el proceso: perder
        // Postgres un instante tumbaba el API en vez de degradarlo, y el
        // /health nunca llegaba a reportar el 503 que tiene previsto.
        pool.on("error", (e) =>
          new Logger("DbModule").warn(`conexión ociosa caída: ${e.message}`),
        );
        return pool;
      },
    },
  ],
  exports: [DB],
})
export class DbModule implements OnApplicationShutdown {
  constructor() {}
  async onApplicationShutdown() {
    // el pool se cierra con el proceso; Nest gestiona el ciclo de vida
  }
}
