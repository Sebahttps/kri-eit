import { Module } from "@nestjs/common";
import { OrdersModule } from "../orders/orders.module";
import { ShopifyController } from "./shopify.controller";
import { ShopifyService } from "./shopify.service";

@Module({
  imports: [OrdersModule],
  controllers: [ShopifyController],
  providers: [ShopifyService],
  exports: [ShopifyService],
})
export class ShopifyModule {}
