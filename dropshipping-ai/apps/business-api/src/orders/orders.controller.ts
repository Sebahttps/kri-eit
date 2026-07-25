import {
  Body,
  Controller,
  Get,
  Param,
  ParseUUIDPipe,
  Post,
  Query,
  UseGuards,
} from "@nestjs/common";
import { Type } from "class-transformer";
import {
  ArrayMinSize,
  IsArray,
  IsEmail,
  IsIn,
  IsInt,
  IsOptional,
  IsString,
  IsUUID,
  Min,
  MinLength,
  ValidateNested,
} from "class-validator";
import { JwtAuthGuard } from "../auth/jwt.guard";
import { OrdersService } from "./orders.service";

class ItemDto {
  @IsUUID()
  product_id: string;

  @IsInt()
  @Min(1)
  cantidad: number;
}

class ClienteDto {
  @IsString()
  @MinLength(2)
  nombre: string;

  @IsOptional()
  @IsEmail()
  email?: string;

  @IsOptional()
  @IsString()
  telefono?: string;

  @IsOptional()
  @IsString()
  direccion?: string;
}

class CrearPedidoDto {
  @ValidateNested()
  @Type(() => ClienteDto)
  cliente: ClienteDto;

  @IsArray()
  @ArrayMinSize(1)
  @ValidateNested({ each: true })
  @Type(() => ItemDto)
  items: ItemDto[];
}

class CheckoutDto {
  @IsIn(["online", "contra_entrega"])
  payment_method: "online" | "contra_entrega";
}

@Controller("orders")
export class OrdersController {
  constructor(private readonly orders: OrdersService) {}

  // --- Tienda (público) ---

  @Post()
  crear(@Body() dto: CrearPedidoDto) {
    return this.orders.crear(dto.cliente, dto.items);
  }

  @Post(":id/checkout")
  checkout(@Param("id", ParseUUIDPipe) id: string, @Body() dto: CheckoutDto) {
    return this.orders.checkout(id, dto.payment_method);
  }

  @Post(":id/pay")
  pagar(@Param("id", ParseUUIDPipe) id: string) {
    return this.orders.pagar(id);
  }

  @Get(":id")
  detalle(@Param("id", ParseUUIDPipe) id: string) {
    return this.orders.detalle(id);
  }

  // --- Supervisor (requiere JWT) ---

  @Get()
  @UseGuards(JwtAuthGuard)
  listar(@Query("limite") limite?: string) {
    return this.orders.listar(limite ? Number(limite) : undefined);
  }
}
