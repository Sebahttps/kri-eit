/** @type {import('next').NextConfig} */
const nextConfig = {
  // Proxy hacia el servicio de agentes: evita CORS y esconde la URL interna
  async rewrites() {
    const agents = process.env.AGENTS_API_URL || "http://localhost:8000";
    return [{ source: "/api/agents/:path*", destination: `${agents}/:path*` }];
  },
};

export default nextConfig;
