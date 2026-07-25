import { ValidationPipe } from "@nestjs/common";
import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  const origins = (process.env.BUSINESS_CORS_ORIGIN ?? "http://localhost:3000,http://localhost:3001")
    .split(",")
    .map((o) => o.trim());
  app.enableCors({ origin: origins });
  await app.listen(Number(process.env.PORT ?? 4000));
}
bootstrap();
