import {
  Controller,
  Get,
  Inject,
  NotFoundException,
  Param,
  ParseUUIDPipe,
  Query,
} from "@nestjs/common";
import { Pool } from "pg";
import { DB } from "../db/db.module";

/** Catálogo público de la tienda B2C. Solo productos activos; nunca expone el costo. */
@Controller("products")
export class CatalogController {
  constructor(@Inject(DB) private readonly db: Pool) {}

  @Get()
  async listar(@Query("categoria") categoria?: string, @Query("q") q?: string) {
    const { rows } = await this.db.query(
      `SELECT id, nombre, descripcion, categoria, precio_venta, trending_score
       FROM products
       WHERE activo
         AND ($1::text IS NULL OR categoria = $1)
         AND ($2::text IS NULL OR nombre ILIKE '%' || $2 || '%')
       ORDER BY trending_score DESC, nombre`,
      [categoria ?? null, q ?? null],
    );
    return rows;
  }

  @Get("categorias")
  async categorias() {
    const { rows } = await this.db.query(
      "SELECT DISTINCT categoria FROM products WHERE activo ORDER BY categoria",
    );
    return rows.map((r) => r.categoria);
  }

  @Get(":id")
  async detalle(@Param("id", ParseUUIDPipe) id: string) {
    const { rows } = await this.db.query(
      `SELECT id, nombre, descripcion, categoria, precio_venta, trending_score
       FROM products WHERE id = $1 AND activo`,
      [id],
    );
    if (!rows[0]) throw new NotFoundException("Producto no encontrado");
    return rows[0];
  }
}
