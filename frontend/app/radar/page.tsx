import Link from "next/link";
import { StatusBadge } from "@/components/StatusBadge";
import { getRadar } from "@/lib/api";
import { ApiErrorState } from "@/components/ApiErrorState";
import { Card } from "@/components/Card";
import { DataFreshnessCard } from "@/components/DataFreshnessCard";
import { EmptyState } from "@/components/EmptyState";
import { PageActions } from "@/components/PageActions";
import { PageHeader } from "@/components/PageHeader";

export default async function RadarPage() {
  const result = await getRadar();
  if (!result.ok) {
    return <ApiErrorState retryHref="/radar" />;
  }
  const stocks = result.data;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Radar"
        description="เลือกหุ้นที่ควรติดตามจากเงื่อนไขจำลอง แล้วอ่านเหตุผลก่อนดูแผนวิเคราะห์"
      />
      <PageActions actions={[{ href: "/dashboard", label: "กลับ Dashboard" }]} />
      <div className="grid gap-4">
        {stocks.map((stock) => (
          <Card key={stock.symbol}>
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h2 className="text-lg font-semibold">{stock.symbol} · {stock.company_name}</h2>
                <div className="mt-1 text-sm text-muted">ราคาจำลอง {stock.price} · VWAP {stock.vwap} · RVOL {stock.relative_volume}</div>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-sm font-semibold">Score {stock.score}</div>
                <StatusBadge status={stock.status} />
              </div>
            </div>
            <div className="mt-4 grid gap-4 md:grid-cols-2">
              <div>
                <div className="text-sm font-medium">เหตุผล</div>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted">{stock.reasons.map((item) => <li key={item}>{item}</li>)}</ul>
              </div>
              <div>
                <div className="text-sm font-medium">ข้อควรระวัง</div>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted">{stock.cautions.map((item) => <li key={item}>{item}</li>)}</ul>
              </div>
            </div>
            <div className="mt-4 flex gap-2">
              <Link href={`/stocks/${stock.symbol}/explain`} className="rounded-md border border-line px-3 py-2 text-sm font-medium hover:bg-panel">ดูคำอธิบาย</Link>
              <Link href={`/stocks/${stock.symbol}/practice-plan`} className="rounded-md border border-line px-3 py-2 text-sm font-medium hover:bg-panel">ดูแผนวิเคราะห์จำลอง</Link>
            </div>
          </Card>
        ))}
      </div>
      {stocks.length > 0 ? <DataFreshnessCard freshness={stocks[0].data_freshness} /> : <EmptyState title="ยังไม่มีหุ้นใน Radar" detail="ถ้า backend พร้อมใช้งานแล้ว ให้ลองโหลดหน้าใหม่อีกครั้ง" />}
    </div>
  );
}
