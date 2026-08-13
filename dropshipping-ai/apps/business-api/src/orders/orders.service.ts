import {
  BadRequestException,
  Inject,
  Injectable,
  Logger,
  NotFoundException,
  ServiceUnavailableException,
  UnprocessableEntityException,
} from "@nestjs/common";
import { Pool } from "pg";
import { DB } from "../db/db.module";

const AGENTS_API = () => process.env.AGENTS_API_URL ?? "http://localhost:8000";

type ItemDto = { product_id: string; cantidad: number };

@Injectable()
export class OrdersService {
  private readonly log = new Logger(OrdersService.name);

  constructor(@Inject(DB) private readonly db: Pool) {}

  /**
   * Única puerta hacia el agents-service. Existe para que sus dos fallos, que
   * no son lo mismo, tampoco se reporten igual:
   *  - contesta con error  -> 422, lo decide quien llama según el caso
   *  - no contesta         -> 503, condición transitoria y reintentable
   *
   * Antes el segundo caso ni siquiera llegaba a decidirse: el fetch lanzaba y
   * salía un 500 "Internal server error" que no distingue "el otro servicio
   * está caído" de "este servicio tiene un bug".
   */
  private async llamarAgentes(ruta: string, init?: Parameters<typeof fetch>[1]) {
    try {
      return await fetch(`${AGENTS_API()}${ruta}`, init);
    } catch (e) {
      // El detalle queda en el log; hacia fuera no se publica la URL interna.
      this.log.error(`agents-service inalcanzable en ${AGENTS_API()}${ruta}: ${(e as Error).message}`);
      throw new ServiceUnavailableException(
        "El Agente B2B no está disponible; el pedido queda como está. Reintenta en unos minutos.",
      );
    }
  }

  /** Crea el pedido en estado 'carrito' con sus ítems y total calculado. */
  async crear(cliente: { nombre: string; email?: string; telefono?: string; direccion?: string },
              items: ItemDto[]) {
    const conn = await this.db.connect();
    try {
      await conn.query("BEGIN");

      let customerId: string;
      if (cliente.email) {
        const existente = await conn.query(
          "SELECT id FROM customers WHERE email = $1", [cliente.email]);
        customerId = existente.rows[0]?.id;
      }
      customerId ??= (
        await conn.query(
          `INSERT INTO customers (nombre, email, telefono, direccion)
           VALUES ($1, $2, $3, $4) RETURNING id`,
          [cliente.nombre, cliente.email ?? null, cliente.telefono ?? null, cliente.direccion ?? null],
        )
      ).rows[0].id;

      const order = (
        await conn.query(
          "INSERT INTO orders (customer_id) VALUES ($1) RETURNING id, numero",
          [customerId],
        )
      ).rows[0];

      let total = 0;
      for (const item of items) {
        const producto = (
          await conn.query(
            "SELECT precio_venta, costo FROM products WHERE id = $1 AND activo",
            [item.product_id],
          )
        ).rows[0];
        if (!producto) {
          throw new BadRequestException(`Producto ${item.product_id} no existe o está inactivo`);
        }
        total += Number(producto.precio_venta) * item.cantidad;
        await conn.query(
          `INSERT INTO order_items (order_id, product_id, cantidad, precio_unitario, costo_unitario)
           VALUES ($1, $2, $3, $4, $5)`,
          [order.id, item.product_id, item.cantidad, producto.precio_venta, producto.costo],
        );
      }
      await conn.query("UPDATE orders SET total = $2 WHERE id = $1", [order.id, total]);

      await conn.query("COMMIT");
      return { order_id: order.id, numero: order.numero, total, status: "carrito" };
    } catch (e) {
      await conn.query("ROLLBACK");
      throw e;
    } finally {
      conn.release();
    }
  }

  /**
   * Checkout: el Agente B2B confirma stock con el proveedor (promesa a) y
   * según el medio de pago el pedido queda listo para pagar o confirmado
   * contra entrega (promesa b). Contra entrega emite la OC de inmediato.
   */
  async checkout(orderId: string, paymentMethod: "online" | "contra_entrega") {
    const resp = await this.llamarAgentes(
      `/back-office/pedidos/${orderId}/confirmar-stock`,
      { method: "POST" },
    );
    if (!resp.ok) {
      throw new UnprocessableEntityException(
        `El Agente B2B no pudo verificar stock (HTTP ${resp.status})`,
      );
    }
    const stock = await resp.json();
    if (!stock.stock_confirmado) {
      return {
        status: "sin_stock",
        productos_sin_stock: stock.productos_sin_stock,
        mensaje: "Sin stock confirmado con el proveedor: el pago NO se habilita (promesa a).",
      };
    }

    await this.db.query("UPDATE orders SET payment_method = $2 WHERE id = $1", [
      orderId,
      paymentMethod,
    ]);

    if (paymentMethod === "contra_entrega") {
      // el trigger de la base vuelve a validar que el stock esté confirmado
      await this.db.query(
        `UPDATE orders SET status = 'contra_entrega_confirmado', payment_status = 'no_aplica'
         WHERE id = $1`,
        [orderId],
      );
      const oc = await this.emitirOrdenCompra(orderId);
      return { status: "contra_entrega_confirmado", orden_compra: oc };
    }

    await this.db.query("UPDATE orders SET status = 'pago_pendiente' WHERE id = $1", [orderId]);
    return { status: "pago_pendiente", mensaje: "Stock confirmado: pago habilitado." };
  }

  /**
   * Pago online. Punto de integración del PSP real (Webpay/MercadoPago):
   * aquí se confirmaría la transacción antes de marcar 'pagado'.
   * El trigger trg_pago_requiere_stock es la última línea de defensa.
   */
  async pagar(orderId: string) {
    const { rows } = await this.db.query(
      "SELECT status FROM orders WHERE id = $1", [orderId]);
    if (!rows[0]) throw new NotFoundException("Pedido no encontrado");
    if (rows[0].status !== "pago_pendiente") {
      throw new UnprocessableEntityException(
        `El pedido está en '${rows[0].status}'; el pago requiere checkout con stock confirmado`,
      );
    }
    await this.db.query(
      `UPDATE orders SET payment_status = 'pagado', status = 'pagado', pagado_at = now()
       WHERE id = $1`,
      [orderId],
    );
    const oc = await this.emitirOrdenCompra(orderId);
    return { status: "pagado", orden_compra: oc };
  }

  /**
   * El Agente B2B emite la OC (o escala al Supervisor si supera su umbral).
   *
   * No lanza: se llama después de que el pago quedó registrado, así que un
   * agents-service caído no puede convertirse en un error de la petición. Eso
   * le diría al cliente que su pago falló cuando sí se cobró. La OC queda
   * pendiente y se reporta en la respuesta.
   */
  private async emitirOrdenCompra(orderId: string) {
    const resp = await this.llamarAgentes("/back-office/ordenes-compra", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ order_id: orderId }),
    }).catch(() => null);
    if (!resp) {
      return { status: "error", detalle: "Agente B2B no disponible: la OC queda pendiente" };
    }
    if (!resp.ok) {
      return { status: "error", detalle: `Agente B2B respondió HTTP ${resp.status}` };
    }
    return resp.json();
  }

  async detalle(orderId: string) {
    const { rows } = await this.db.query(
      `SELECT o.id, o.numero, o.status, o.payment_method, o.payment_status, o.total,
              o.stock_confirmado_at, o.entregado_at, o.limite_retracto_at, o.created_at,
              c.nombre AS cliente,
              s.carrier, s.tracking_number, s.tracking_url, s.status AS envio_status
       FROM orders o
       JOIN customers c ON c.id = o.customer_id
       LEFT JOIN shipments s ON s.order_id = o.id
       WHERE o.id = $1`,
      [orderId],
    );
    if (!rows[0]) throw new NotFoundException("Pedido no encontrado");
    const items = await this.db.query(
      `SELECT oi.cantidad, oi.precio_unitario, p.nombre
       FROM order_items oi JOIN products p ON p.id = oi.product_id
       WHERE oi.order_id = $1`,
      [orderId],
    );
    return { ...rows[0], items: items.rows };
  }

  async listar(limite = 50) {
    const { rows } = await this.db.query(
      `SELECT o.id, o.numero, o.status, o.payment_method, o.total, o.created_at,
              c.nombre AS cliente
       FROM orders o JOIN customers c ON c.id = o.customer_id
       ORDER BY o.created_at DESC LIMIT $1`,
      [Math.min(limite, 200)],
    );
    return rows;
  }
}
