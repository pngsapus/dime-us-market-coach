import { ApiErrorState } from "@/components/ApiErrorState";
import { Card } from "@/components/Card";
import { DataFreshnessCard } from "@/components/DataFreshnessCard";
import { ExplanationTrace } from "@/components/ExplanationTrace";
import { MetricCard } from "@/components/MetricCard";
import { PageActions } from "@/components/PageActions";
import { PageHeader } from "@/components/PageHeader";
import { StatusBadge } from "@/components/StatusBadge";
import { WarningBox } from "@/components/WarningBox";
import { getPracticePlan } from "@/lib/api";

type PageProps = {
  params: Promise<{ symbol: string }>;
};

export default async function PracticePlanPage({ params }: PageProps) {
  const { symbol } = await params;
  const result = await getPracticePlan(symbol);

  if (!result.ok) {
    return (
      <div className="space-y-5">
        <PageHeader title={`${symbol.toUpperCase()} แผนวิเคราะห์จำลอง`} description="ไม่สามารถโหลดแผนจาก backend mock API ได้" />
        <ApiErrorState retryHref={`/stocks/${symbol}/practice-plan`} />
        <PageActions actions={[{ href: `/stocks/${symbol}/explain`, label: "กลับไป Stock Explain" }]} />
      </div>
    );
  }

  const plan = result.data;

  return (
    <div className="space-y-6">
      <PageHeader
        title={`${plan.symbol} แผนวิเคราะห์จำลอง`}
        description={`${plan.disclaimer} · ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง`}
        status={plan.status}
      />

      <PageActions
        actions={[
          { href: `/stocks/${plan.symbol}/explain`, label: "กลับไปหน้าอธิบายหุ้น" },
          { href: `/dime-check?symbol=${plan.symbol}`, label: "ตรวจสอบราคาจริงใน Dime", primary: true },
        ]}
      />

      <WarningBox>
        แผนนี้เป็นแบบจำลองเพื่อฝึกประเมินความเสี่ยง ผู้ใช้ต้องตรวจสอบราคาจริงใน Dime ด้วยตนเอง
      </WarningBox>

      <Card>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 className="text-base font-semibold">{plan.plan_type}</h2>
          <StatusBadge status={plan.status} />
        </div>
        <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
          <MetricCard label="Entry Zone" value={`${plan.entry_zone.low} - ${plan.entry_zone.high}`} />
          <MetricCard label="Stop Loss" value={plan.stop_loss} />
          <MetricCard label="Take Profit" value={plan.take_profit} />
          <MetricCard label="Risk:Reward" value={plan.risk_reward} />
          <MetricCard label="จำนวนหุ้นสูงสุด" value={plan.max_position_size_shares} />
        </div>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <MetricCard label="ความเสี่ยงจำลอง" value={`${plan.expected_loss_thb.toLocaleString()} บาท`} tone="warning" />
          <MetricCard label="ผลตอบแทนจำลองตามแผน" value={`${plan.expected_profit_thb.toLocaleString()} บาท`} />
        </div>
      </Card>

      <section className="grid gap-4 md:grid-cols-2">
        <Card>
          <h2 className="text-base font-semibold">เหตุผลของแผน</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-6 text-muted">
            {plan.reasons.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </Card>
        <Card>
          <h2 className="text-base font-semibold">ข้อควรระวัง</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-6 text-muted">
            {plan.cautions.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </Card>
      </section>

      <ExplanationTrace items={plan.explanation_trace} />

      <DataFreshnessCard freshness={plan.data_freshness} />
    </div>
  );
}
