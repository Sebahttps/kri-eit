/** @type {import('next').NextConfig} */
const nextConfig = {
  // Proxy hacia el gateway y el agente B2C: sin CORS y con URLs internas ocultas
  async rewrites() {
    const gw = process.env.BUSINESS_API_URL || "http://localhost:4000";
    const agents = process.env.AGENTS_API_URL || "http://localhost:8000";
    return [
      { source: "/api/gw/:path*", destination: `${gw}/:path*` },
      { source: "/api/agents/:path*", destination: `${agents}/:path*` },
    ];
  },
};

export default nextConfig;
