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
  const providerLabel = status.provider === "mock_provider" ? "ผู้ให้ข้อมูลจำลอง" : status.provider;
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
        <ul className="mt-4 list-disc space-y-2 pl-5 text-sm text-muted">{status.limitations.map((item) => <li key={item}>{item}</li>)}</ul>
      </Card>
      <DataFreshnessCard freshness={status.freshness} />
    </div>
  );
}
