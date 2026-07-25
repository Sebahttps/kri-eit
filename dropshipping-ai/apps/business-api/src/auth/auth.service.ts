import { Inject, Injectable, UnauthorizedException } from "@nestjs/common";
import { JwtService } from "@nestjs/jwt";
import { compare } from "bcryptjs";
import { Pool } from "pg";
import { DB } from "../db/db.module";

@Injectable()
export class AuthService {
  constructor(
    @Inject(DB) private readonly db: Pool,
    private readonly jwt: JwtService,
  ) {}

  async login(email: string, password: string) {
    const { rows } = await this.db.query(
      "SELECT id, email, nombre, password_hash FROM supervisors WHERE email = $1 AND activo",
      [email],
    );
    const supervisor = rows[0];
    if (!supervisor || !(await compare(password, supervisor.password_hash))) {
      throw new UnauthorizedException("Credenciales inválidas");
    }
    const token = await this.jwt.signAsync({
      sub: supervisor.id,
      email: supervisor.email,
      nombre: supervisor.nombre,
    });
    return {
      access_token: token,
      supervisor: { id: supervisor.id, email: supervisor.email, nombre: supervisor.nombre },
    };
  }
}
