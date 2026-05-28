import { getDiscoveryLatest, getMarketSummary } from "@/lib/api";
import { StatusBadge } from "@/components/StatusBadge";
import { ApiErrorState } from "@/components/ApiErrorState";
import { Card } from "@/components/Card";
import { DataFreshnessCard } from "@/components/DataFreshnessCard";
import { EmptyState } from "@/components/EmptyState";
import { MetricCard } from "@/components/MetricCard";
import { PageActions } from "@/components/PageActions";
import { PageHeader } from "@/components/PageHeader";
import { WarningBox } from "@/components/WarningBox";

export default async function DashboardPage() {
  const [summaryResult, discoveryResult] = await Promise.all([getMarketSummary(), getDiscoveryLatest()]);
  if (!summaryResult.ok) {
    return <ApiErrorState retryHref="/dashboard" />;
  }
  const summary = summaryResult.data;
  const discovery = discoveryResult.ok ? discoveryResult.data : null;
  const radar = discovery?.results.slice(0, 3) ?? [];

  return (
    <div className="space-y-6">
      <PageHeader
        title="ภาพรวมตลาดวันนี้"
        description="ดูภาพรวมตลาดก่อน แล้วเลือกได้ว่าจะไป Radar หรือใช้เมนูด้านซ้ายเพื่อข้ามไปหน้าที่ต้องการ"
        status={summary.status}
      />
      <WarningBox title="ขอบเขตข้อมูล">
        ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง และใช้เพื่อวิเคราะห์/วางแผนเท่านั้น
      </WarningBox>
      <Card>
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <div className="text-xl font-semibold">{summary.headline}</div>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-muted">{summary.summary_th}</p>
          </div>
          <StatusBadge status={summary.status} />
        </div>
        <div className="mt-5 grid gap-3 sm:grid-cols-3">
          {Object.entries(summary.indices).map(([name, value]) => (
            <MetricCard key={name} label={name} value={value.toLocaleString()} />
          ))}
        </div>
      </Card>
      <div className="grid gap-4 lg:grid-cols-[1fr_320px]">
        <Card>
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h2 className="text-base font-semibold">ขั้นตอนแนะนำ: เลือกหุ้นจาก Radar</h2>
            <PageActions actions={[{ href: "/radar", label: "ไปที่ Radar", primary: true }]} />
          </div>
          {discovery && (
            <div className="mt-2 text-xs text-muted">
              Radar ล่าสุด {new Date(discovery.generated_at).toLocaleString("th-TH")} · ข้อมูลจำลองในเครื่อง ไม่ใช่ราคาจาก Dime โดยตรง
            </div>
          )}
          <div className="mt-4 divide-y divide-line">
            {radar.map((stock) => (
              <div key={stock.symbol} className="flex items-center justify-between gap-4 py-3">
                <div>
                  <div className="font-medium">#{stock.rank} {stock.symbol} · {stock.name}</div>
                  <div className="text-sm text-muted">Score {stock.final_score} · {stock.sector_theme}</div>
                </div>
                <StatusBadge status={stock.category} />
              </div>
            ))}
            {radar.length === 0 && <EmptyState title="ยังไม่มีข้อมูล Radar" detail="กรุณาตรวจสอบสถานะ backend หรือโหลดหน้าใหม่อีกครั้ง" />}
          </div>
        </Card>
        <DataFreshnessCard freshness={discovery?.data_freshness ?? summary.data_freshness} />
      </div>
    </div>
  );
}
