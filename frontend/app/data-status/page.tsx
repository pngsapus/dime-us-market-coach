import { Card } from "@/components/Card";
import { DataFreshnessCard } from "@/components/DataFreshnessCard";
import { StatusBadge } from "@/components/StatusBadge";
import { getDataStatus } from "@/lib/api";
import { ApiErrorState } from "@/components/ApiErrorState";
import { PageActions } from "@/components/PageActions";
import { PageHeader } from "@/components/PageHeader";

export default async function DataStatusPage() {
  const result = await getDataStatus();
  if (!result.ok) {
    return <ApiErrorState retryHref="/data-status" />;
  }
  const status = result.data;
  const providerLabel = status.provider === "mock_provider" || status.provider === "mock" ? "ผู้ให้ข้อมูลจำลอง" : status.provider;
  const healthLabel = status.health === "healthy" ? "พร้อมใช้งาน" : status.health === "degraded" ? "ข้อมูลล่าช้า" : "ไม่พร้อมใช้งาน";
  return (
    <div className="space-y-6">
      <PageHeader
        title="สถานะข้อมูล"
        description="ตรวจสอบความพร้อมของผู้ให้ข้อมูลจำลองและข้อจำกัดก่อนใช้แผนวิเคราะห์"
        status={healthLabel}
      />
      <PageActions actions={[{ href: "/dashboard", label: "กลับ Dashboard" }, { href: "/settings", label: "ตั้งค่า Risk Profile" }]} />
      <Card>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <div className="text-lg font-semibold">{providerLabel}</div>
            <p className="mt-1 text-sm text-muted">{status.message}</p>
          </div>
          <StatusBadge status={healthLabel} />
        </div>
        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <StatusMetric label="ประเภท provider" value={status.provider_type} />
          <StatusMetric label="Mock fallback" value={status.provider_status.fallback_used ? "กำลังใช้ mock/local fallback" : "ไม่ได้ใช้ fallback"} />
          <StatusMetric label="ข้อมูลตลาดจริง" value={status.is_live_market_data_connected ? "เชื่อมต่อแล้ว" : "ยังไม่เชื่อมต่อ"} />
          <StatusMetric label="ราคาจาก Dime" value={status.is_dime_price_source_connected ? "เชื่อมต่อแล้ว" : "manual input เท่านั้น"} />
          <StatusMetric label="Trading integration" value={status.has_trading_integration ? "เชื่อมต่อแล้ว" : "ไม่มีการเชื่อมต่อ"} />
          <StatusMetric label="Discovery engine" value={status.is_discovery_local_rule_based ? "local rule-based mock data" : "ไม่พร้อมใช้งาน"} />
          <StatusMetric label="ความพร้อม provider" value={status.provider_status.freshness_label} />
        </div>
        {status.provider_status.fallback_reason && (
          <div className="mt-4 rounded-md border border-amber-100 bg-amber-50 p-3 text-sm leading-6 text-warn">
            {status.provider_status.fallback_reason}
          </div>
        )}
        <p className="mt-4 text-sm leading-6 text-muted">
          ความพร้อมสำหรับอนาคต: โครงสร้าง provider พร้อมรองรับการเพิ่มผู้ให้บริการข้อมูลจริงในภายหลัง แต่ตอนนี้ยังไม่มี live market data, Dime API, หรือ trading integration
        </p>
        <ul className="mt-4 list-disc space-y-2 pl-5 text-sm text-muted">{status.limitations.map((item) => <li key={item}>{item}</li>)}</ul>
      </Card>
      <DataFreshnessCard freshness={status.freshness} />
    </div>
  );
}

function StatusMetric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-line bg-panel p-3">
      <div className="text-xs font-medium text-muted">{label}</div>
      <div className="mt-1 text-sm font-semibold">{value}</div>
    </div>
  );
}
