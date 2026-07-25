import { Global, Module, OnApplicationShutdown } from "@nestjs/common";
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
      useFactory: () => new Pool({ connectionString: databaseUrl(), max: 10 }),
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
