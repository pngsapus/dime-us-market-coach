import { ApiErrorState } from "@/components/ApiErrorState";
import { Freshness } from "@/components/Freshness";
import { MetricCard } from "@/components/MetricCard";
import { PageActions } from "@/components/PageActions";
import { StatusBadge } from "@/components/StatusBadge";
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
        <header>
          <h1 className="text-2xl font-semibold">{symbol.toUpperCase()} แผนวิเคราะห์จำลอง</h1>
          <p className="mt-1 text-sm text-muted">ไม่สามารถโหลดแผนจาก backend mock API ได้</p>
        </header>
        <ApiErrorState retryHref={`/stocks/${symbol}/practice-plan`} />
        <PageActions actions={[{ href: `/stocks/${symbol}/explain`, label: "กลับไป Stock Explain" }]} />
      </div>
    );
  }

  const plan = result.data;

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">{plan.symbol} แผนวิเคราะห์จำลอง</h1>
        <p className="mt-1 text-sm text-muted">{plan.disclaimer}</p>
        <p className="mt-1 text-sm text-muted">ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง</p>
      </header>

      <PageActions
        actions={[
          { href: `/stocks/${plan.symbol}/explain`, label: "กลับไป Stock Explain" },
          { href: "/dime-check", label: "ตรวจสอบราคาจริงใน Dime", primary: true },
        ]}
      />

      <section className="rounded-md border border-line bg-white p-6 shadow-sm">
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
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        <div className="rounded-md border border-line bg-white p-6 shadow-sm">
          <h2 className="text-base font-semibold">เหตุผลของแผน</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-6 text-muted">
            {plan.reasons.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
        <div className="rounded-md border border-line bg-white p-6 shadow-sm">
          <h2 className="text-base font-semibold">ข้อควรระวัง</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-6 text-muted">
            {plan.cautions.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
      </section>

      <section className="rounded-md border border-line bg-white p-6 shadow-sm">
        <h2 className="text-base font-semibold">Explanation trace</h2>
        <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm leading-6 text-muted">
          {plan.explanation_trace.map((item) => <li key={item}>{item}</li>)}
        </ol>
      </section>

      <Freshness freshness={plan.data_freshness} />
    </div>
  );
}
