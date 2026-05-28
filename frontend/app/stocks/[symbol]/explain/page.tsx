import { ApiErrorState } from "@/components/ApiErrorState";
import { Freshness } from "@/components/Freshness";
import { MetricCard } from "@/components/MetricCard";
import { PageActions } from "@/components/PageActions";
import { StatusBadge } from "@/components/StatusBadge";
import { getStockExplain } from "@/lib/api";

type PageProps = {
  params: Promise<{ symbol: string }>;
};

export default async function StockExplainPage({ params }: PageProps) {
  const { symbol } = await params;
  const result = await getStockExplain(symbol);

  if (!result.ok) {
    return (
      <div className="space-y-5">
        <header>
          <h1 className="text-2xl font-semibold">{symbol.toUpperCase()} Stock Explain</h1>
          <p className="mt-1 text-sm text-muted">ไม่สามารถโหลดคำอธิบายจาก backend mock API ได้</p>
        </header>
        <ApiErrorState retryHref={`/stocks/${symbol}/explain`} />
        <PageActions actions={[{ href: "/radar", label: "กลับไป Radar" }]} />
      </div>
    );
  }

  const data = result.data;

  return (
    <div className="space-y-6">
      <header className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold">{data.symbol} Stock Explain</h1>
          <p className="mt-1 text-sm text-muted">{data.company_name}</p>
          <p className="mt-2 text-sm text-muted">ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง</p>
        </div>
        <StatusBadge status={data.status} />
      </header>

      <PageActions
        actions={[
          { href: "/radar", label: "กลับไป Radar" },
          { href: `/stocks/${data.symbol}/practice-plan`, label: "ไปที่แผนวิเคราะห์จำลอง", primary: true },
        ]}
      />

      <section className="rounded-md border border-line bg-white p-6 shadow-sm">
        <h2 className="text-base font-semibold">ภาพรวมสำหรับผู้เริ่มต้น</h2>
        <p className="mt-3 text-sm leading-6 text-muted">{data.summary_th}</p>
        <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <MetricCard label="ราคาจำลอง" value={data.price} />
          <MetricCard label="VWAP" value={data.vwap} />
          <MetricCard label="แนวรับ" value={data.support} />
          <MetricCard label="แนวต้าน" value={data.resistance} />
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        <div className="rounded-md border border-line bg-white p-6 shadow-sm">
          <h2 className="text-base font-semibold">เหตุผลที่ควรติดตาม</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-6 text-muted">
            {data.reasons.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
        <div className="rounded-md border border-line bg-white p-6 shadow-sm">
          <h2 className="text-base font-semibold">ข้อควรระวัง</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-6 text-muted">
            {data.cautions.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
      </section>

      <section className="rounded-md border border-line bg-white p-6 shadow-sm">
        <h2 className="text-base font-semibold">ทำไมระบบจึงสรุปแบบนี้</h2>
        <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm leading-6 text-muted">
          {data.explanation_trace.map((item) => <li key={item}>{item}</li>)}
        </ol>
      </section>

      <Freshness freshness={data.data_freshness} />
    </div>
  );
}
