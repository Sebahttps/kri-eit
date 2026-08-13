import { Logger, ValidationPipe } from "@nestjs/common";
import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";

async function bootstrap() {
  // rawBody: necesario para verificar la firma HMAC de los webhooks de Shopify
  const app = await NestFactory.create(AppModule, { rawBody: true });
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  const origins = (process.env.BUSINESS_CORS_ORIGIN ?? "http://localhost:3000,http://localhost:3001")
    .split(",")
    .map((o) => o.trim());
  app.enableCors({ origin: origins });
  await app.listen(Number(process.env.PORT ?? 4000));
}
bootstrap().catch((e) => {
  // Sin este catch, cualquier fallo de arranque salía como
  // UnhandledPromiseRejection: un volcado de pila que no dice qué faltaba.
  Logger.error(`No se pudo arrancar: ${(e as Error).message}`, "Bootstrap");
  process.exit(1);
});
