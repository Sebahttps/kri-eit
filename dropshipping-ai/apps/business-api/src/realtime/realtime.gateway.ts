import { OnModuleDestroy, OnModuleInit } from "@nestjs/common";
import { WebSocketGateway, WebSocketServer } from "@nestjs/websockets";
import { Client } from "pg";
import { Server } from "socket.io";
import { databaseUrl } from "../db/db.module";

const AGENTS_API = () => process.env.AGENTS_API_URL ?? "http://localhost:8000";

/**
 * Tiempo real del dashboard sin polling en el navegador:
 *  - Postgres NOTIFY 'eventos' (migración 001) -> evento 'evento' por WebSocket
 *    (sugerencias nuevas, cambios de pedido, seguimiento, tickets)
 *  - snapshot de KPIs cada 10 s -> evento 'kpis'
 */
@WebSocketGateway({ namespace: "/eventos", cors: { origin: "*" } })
export class RealtimeGateway implements OnModuleInit, OnModuleDestroy {
  @WebSocketServer() server: Server;

  private listener: Client;
  private kpiTimer: NodeJS.Timeout;

  async onModuleInit() {
    this.listener = new Client({ connectionString: databaseUrl() });
    await this.listener.connect();
    await this.listener.query("LISTEN eventos");
    this.listener.on("notification", (msg) => {
      if (!msg.payload) return;
      try {
        this.server.emit("evento", JSON.parse(msg.payload));
      } catch {
        // payload no-JSON: se ignora
      }
    });

    this.kpiTimer = setInterval(async () => {
      try {
        const resp = await fetch(`${AGENTS_API()}/kpis/resumen`);
        if (resp.ok) this.server.emit("kpis", await resp.json());
      } catch {
        // agentes caídos: el próximo tick reintenta
      }
    }, 10_000);
  }

  async onModuleDestroy() {
    clearInterval(this.kpiTimer);
    await this.listener?.end();
  }
}
