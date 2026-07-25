import {
  Body,
  Controller,
  Inject,
  NotFoundException,
  Post,
} from "@nestjs/common";
import { IsIn, IsOptional, IsString, MinLength } from "class-validator";
import { Pool } from "pg";
import { DB } from "../db/db.module";

// Estados que reporta el carrier -> estados internos del envío/pedido.
// 'entregado' dispara en la base la garantía de 6 meses y la ventana de
// retracto de 10 días (promesas d y e), sin código adicional aquí.
const ESTADO_PEDIDO: Record<string, string | null> = {
  despachado: "despachado",
  en_transito: "en_transito",
  en_reparto: "en_transito",
  entregado: "entregado",
  devuelto: null,
  extraviado: null,
};

class CarrierEventDto {
  @IsString()
  carrier: string;

  @IsString()
  @MinLength(4)
  tracking_number: string;

  @IsIn(["despachado", "en_transito", "en_reparto", "entregado", "devuelto", "extraviado"])
  status: string;

  @IsString()
  descripcion: string;

  @IsOptional()
  @IsString()
  ubicacion?: string;
}

@Controller("webhooks")
export class WebhooksController {
  constructor(@Inject(DB) private readonly db: Pool) {}

  /** Punto de entrada de los carriers: alimenta el seguimiento en tiempo real (promesa c). */
  @Post("carrier")
  async carrier(@Body() evento: CarrierEventDto) {
    const { rows } = await this.db.query(
      "SELECT id, order_id FROM shipments WHERE carrier = $1 AND tracking_number = $2",
      [evento.carrier, evento.tracking_number],
    );
    const shipment = rows[0];
    if (!shipment) {
      throw new NotFoundException(
        `Envío ${evento.carrier}/${evento.tracking_number} no registrado`,
      );
    }

    await this.db.query(
      `INSERT INTO shipment_events (shipment_id, status, descripcion, ubicacion)
       VALUES ($1, $2::shipment_status, $3, $4)`,
      [shipment.id, evento.status, evento.descripcion, evento.ubicacion ?? null],
    );
    await this.db.query(
      "UPDATE shipments SET status = $2::shipment_status WHERE id = $1",
      [shipment.id, evento.status],
    );

    const estadoPedido = ESTADO_PEDIDO[evento.status];
    if (estadoPedido) {
      await this.db.query(
        "UPDATE orders SET status = $2::order_status WHERE id = $1 AND status <> $2::order_status",
        [shipment.order_id, estadoPedido],
      );
    }
    return { ok: true, shipment_id: shipment.id, order_id: shipment.order_id };
  }
}
