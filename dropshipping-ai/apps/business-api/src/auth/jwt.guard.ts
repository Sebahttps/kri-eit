import {
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
} from "@nestjs/common";
import { JwtService } from "@nestjs/jwt";

@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(private readonly jwt: JwtService) {}

  async canActivate(ctx: ExecutionContext): Promise<boolean> {
    const req = ctx.switchToHttp().getRequest();
    const [scheme, token] = String(req.headers.authorization ?? "").split(" ");
    if (scheme !== "Bearer" || !token) {
      throw new UnauthorizedException("Falta el token Bearer");
    }
    try {
      req.supervisor = await this.jwt.verifyAsync(token);
      return true;
    } catch {
      throw new UnauthorizedException("Token inválido o expirado");
    }
  }
}
