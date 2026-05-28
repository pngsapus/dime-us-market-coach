import Link from "next/link";
import { Freshness } from "@/components/Freshness";
import { StatusBadge } from "@/components/StatusBadge";
import { getRadar } from "@/lib/api";
import { ApiErrorState } from "@/components/ApiErrorState";

export default async function RadarPage() {
  const result = await getRadar();
  if (!result.ok) {
    return <ApiErrorState retryHref="/radar" />;
  }
  const stocks = result.data;

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">Radar</h1>
        <p className="mt-1 text-sm text-muted">แสดงหุ้นที่น่าติดตามจากเงื่อนไขจำลอง พร้อมเหตุผลและข้อควรระวัง</p>
      </header>
      <div className="grid gap-4">
        {stocks.map((stock) => (
          <article key={stock.symbol} className="rounded-md border border-line bg-white p-6 shadow-sm">
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
          </article>
        ))}
      </div>
      {stocks.length > 0 ? <Freshness freshness={stocks[0].data_freshness} /> : <ApiErrorState detail="Radar ยังไม่มีข้อมูลจาก backend" retryHref="/radar" />}
    </div>
  );
}
