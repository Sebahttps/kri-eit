import { Logger, OnModuleDestroy, OnModuleInit } from "@nestjs/common";
import { WebSocketGateway, WebSocketServer } from "@nestjs/websockets";
import { Client } from "pg";
import { Server } from "socket.io";
import { databaseUrl } from "../db/db.module";

const AGENTS_API = () => process.env.AGENTS_API_URL ?? "http://localhost:8000";
const REINTENTO_MS = 5_000;

/**
 * Tiempo real del dashboard sin polling en el navegador:
 *  - Postgres NOTIFY 'eventos' (migración 001) -> evento 'evento' por WebSocket
 *    (sugerencias nuevas, cambios de pedido, seguimiento, tickets)
 *  - snapshot de KPIs cada 10 s -> evento 'kpis'
 *
 * Ambas fuentes son accesorias: si no están, el dashboard pierde la
 * actualización en vivo pero el API sigue atendiendo. Por eso nada de lo que
 * pasa aquí puede tumbar el arranque ni el proceso.
 */
@WebSocketGateway({ namespace: "/eventos", cors: { origin: "*" } })
export class RealtimeGateway implements OnModuleInit, OnModuleDestroy {
  @WebSocketServer() server: Server;

  private readonly log = new Logger(RealtimeGateway.name);
  private listener: Client | null = null;
  private kpiTimer: NodeJS.Timeout;
  private reintentoTimer: NodeJS.Timeout | null = null;
  private cerrado = false;

  async onModuleInit() {
    // Deliberadamente sin await: si Postgres no contesta, el API arranca igual
    // y el LISTEN se reintenta solo. Esperar aquí hacía que el rechazo saliera
    // por bootstrap() y matara el proceso antes de abrir el puerto — con lo que
    // el /health, que existe justamente para reportar "base caída", nunca
    // alcanzaba a contestarlo.
    void this.conectarListener();

    this.kpiTimer = setInterval(async () => {
      try {
        const resp = await fetch(`${AGENTS_API()}/kpis/resumen`);
        if (resp.ok) this.server.emit("kpis", await resp.json());
      } catch {
        // agentes caídos: el próximo tick reintenta
      }
    }, 10_000);
  }

  private async conectarListener() {
    if (this.cerrado) return;

    const cliente = new Client({ connectionString: databaseUrl() });

    // pg emite 'error' cuando una conexión ya establecida se cae (Postgres se
    // reinició, la red se cortó). Un Client sin este manejador convierte ese
    // evento en excepción no capturada, que en Node mata el proceso: el API
    // entero se caía porque se reinició la base.
    cliente.on("error", (e) => {
      this.log.warn(`conexión de eventos perdida: ${e.message}`);
      this.descartar(cliente);
    });

    try {
      await cliente.connect();
      await cliente.query("LISTEN eventos");
    } catch (e) {
      this.log.warn(
        `sin eventos en vivo (${(e as Error).message}); reintento en ${REINTENTO_MS / 1000} s`,
      );
      this.descartar(cliente);
      return;
    }

    cliente.on("notification", (msg) => {
      if (!msg.payload) return;
      try {
        this.server.emit("evento", JSON.parse(msg.payload));
      } catch {
        // payload no-JSON: se ignora
      }
    });

    this.listener = cliente;
    this.log.log("escuchando eventos de Postgres");
  }

  /** Cierra el cliente inservible y programa un reintento, sin duplicarlos. */
  private descartar(cliente: Client) {
    void cliente.end().catch(() => {});
    if (this.listener === cliente) this.listener = null;
    if (this.cerrado || this.reintentoTimer) return;
    this.reintentoTimer = setTimeout(() => {
      this.reintentoTimer = null;
      void this.conectarListener();
    }, REINTENTO_MS);
    // que un reintento pendiente no impida cerrar el proceso
    this.reintentoTimer.unref?.();
  }

  async onModuleDestroy() {
    this.cerrado = true;
    clearInterval(this.kpiTimer);
    if (this.reintentoTimer) clearTimeout(this.reintentoTimer);
    await this.listener?.end().catch(() => {});
  }
}
