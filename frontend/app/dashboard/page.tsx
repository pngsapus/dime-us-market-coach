import { getMarketSummary, getRadar } from "@/lib/api";
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
  const [summaryResult, radarResult] = await Promise.all([getMarketSummary(), getRadar()]);
  if (!summaryResult.ok) {
    return <ApiErrorState retryHref="/dashboard" />;
  }
  const summary = summaryResult.data;
  const radar = radarResult.ok ? radarResult.data : [];

  return (
    <div className="space-y-6">
      <PageHeader
        title="ภาพรวมตลาดวันนี้"
        description="เริ่มจากภาพรวมตลาด แล้วค่อยไปดู Radar หุ้นที่ควรติดตามจากข้อมูลจำลอง"
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
            <h2 className="text-base font-semibold">ขั้นถัดไป: เลือกหุ้นจาก Radar</h2>
            <PageActions actions={[{ href: "/radar", label: "ไปที่ Radar", primary: true }]} />
          </div>
          <div className="mt-4 divide-y divide-line">
            {radar.map((stock) => (
              <div key={stock.symbol} className="flex items-center justify-between gap-4 py-3">
                <div>
                  <div className="font-medium">{stock.symbol} · {stock.company_name}</div>
                  <div className="text-sm text-muted">Score {stock.score} · VWAP {stock.vwap}</div>
                </div>
                <StatusBadge status={stock.status} />
              </div>
            ))}
            {radar.length === 0 && <EmptyState title="ยังไม่มีข้อมูล Radar" detail="กรุณาตรวจสอบสถานะ backend หรือโหลดหน้าใหม่อีกครั้ง" />}
          </div>
        </Card>
        <DataFreshnessCard freshness={summary.data_freshness} />
      </div>
    </div>
  );
}
