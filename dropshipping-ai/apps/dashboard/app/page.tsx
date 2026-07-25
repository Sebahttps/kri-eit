import KpiCards from "@/components/kpi-cards";
import SalesCharts from "@/components/sales-charts";
import Suggestions from "@/components/suggestions";
import Tickets from "@/components/tickets";
import Trending from "@/components/trending";

export default function Home() {
  return (
    <main className="mx-auto max-w-6xl space-y-4 p-4 lg:p-8">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">Panel del Supervisor</h1>
          <p className="text-sm text-ink-2">
            Dropshipping autónomo · Agentes IA operando, tú decides lo crítico
          </p>
        </div>
        <span className="flex items-center gap-2 text-xs text-ink-2">
          <span
            className="inline-block h-2 w-2 animate-pulse rounded-full"
            style={{ backgroundColor: "var(--status-good)" }}
            aria-hidden
          />
          datos en vivo
        </span>
      </header>

      <KpiCards />
      <SalesCharts />

      <div className="grid gap-4 lg:grid-cols-2">
        <Suggestions />
        <div className="space-y-4">
          <Trending />
          <Tickets />
        </div>
      </div>
    </main>
  );
}
