import { ApiErrorState } from "@/components/ApiErrorState";
import { Card } from "@/components/Card";
import { DataFreshnessCard } from "@/components/DataFreshnessCard";
import { ExplanationTrace } from "@/components/ExplanationTrace";
import { MetricCard } from "@/components/MetricCard";
import { PageActions } from "@/components/PageActions";
import { PageHeader } from "@/components/PageHeader";
import { WarningBox } from "@/components/WarningBox";
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
        <PageHeader title={`${symbol.toUpperCase()} อธิบายหุ้น`} description="ไม่สามารถโหลดคำอธิบายจาก backend mock API ได้" />
        <ApiErrorState retryHref={`/stocks/${symbol}/explain`} />
        <PageActions actions={[{ href: "/radar", label: "กลับไป Radar" }]} />
      </div>
    );
  }

  const data = result.data;

  return (
    <div className="space-y-6">
      <PageHeader
        title={`${data.symbol} อธิบายหุ้น`}
        description={`${data.company_name} · ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง`}
        status={data.status}
      />

      <PageActions
        actions={[
          { href: "/radar", label: "กลับไป Radar" },
          { href: `/stocks/${data.symbol}/practice-plan`, label: "ไปที่แผนวิเคราะห์จำลอง", primary: true },
        ]}
      />

      <WarningBox>
        คำอธิบายนี้เป็นการช่วยอ่านข้อมูลจำลอง ไม่ใช่คำแนะนำให้ทำรายการซื้อขาย
      </WarningBox>

      <Card>
        <h2 className="text-base font-semibold">ภาพรวมสำหรับผู้เริ่มต้น</h2>
        <p className="mt-3 text-sm leading-6 text-muted">{data.summary_th}</p>
        <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <MetricCard label="ราคาจำลอง" value={data.price} />
          <MetricCard label="VWAP" value={data.vwap} />
          <MetricCard label="แนวรับ" value={data.support} />
          <MetricCard label="แนวต้าน" value={data.resistance} />
        </div>
      </Card>

      <section className="grid gap-4 md:grid-cols-2">
        <Card>
          <h2 className="text-base font-semibold">เหตุผลที่ควรติดตาม</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-6 text-muted">
            {data.reasons.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </Card>
        <Card>
          <h2 className="text-base font-semibold">ข้อควรระวัง</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-6 text-muted">
            {data.cautions.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </Card>
      </section>

      <ExplanationTrace items={data.explanation_trace} title="ทำไมระบบจึงสรุปแบบนี้" />

      <DataFreshnessCard freshness={data.data_freshness} />
    </div>
  );
}
