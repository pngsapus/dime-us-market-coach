import Link from "next/link";
import { StatusBadge } from "@/components/StatusBadge";
import { getDiscoveryLatest } from "@/lib/api";
import { ApiErrorState } from "@/components/ApiErrorState";
import { Card } from "@/components/Card";
import { DataFreshnessCard } from "@/components/DataFreshnessCard";
import { EmptyState } from "@/components/EmptyState";
import { PageActions } from "@/components/PageActions";
import { PageHeader } from "@/components/PageHeader";
import { WarningBox } from "@/components/WarningBox";

export default async function RadarPage() {
  const result = await getDiscoveryLatest();
  if (!result.ok) {
    return <ApiErrorState retryHref="/radar" />;
  }
  const discovery = result.data;
  const stocks = discovery.results;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Radar Discovery"
        description="จัดอันดับหุ้นและ ETF จาก rule-based local mock data เพื่อช่วยเลือกสิ่งที่ควรศึกษาเพิ่มเติม"
      />
      <PageActions actions={[{ href: "/dashboard", label: "กลับ Dashboard" }]} />
      <WarningBox title="ขอบเขตข้อมูล Discovery">
        {discovery.disclaimer} ใช้เพื่อประกอบการพิจารณาเท่านั้น ไม่ใช่คำสั่งซื้อ
      </WarningBox>
      <div className="grid gap-4">
        {stocks.map((stock) => (
          <Card key={stock.symbol}>
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <div className="text-xs font-semibold uppercase text-muted">อันดับ {stock.rank} · {stock.sector_theme}</div>
                <h2 className="mt-1 text-lg font-semibold">{stock.symbol} · {stock.name}</h2>
                <div className="mt-1 text-sm text-muted">
                  ราคาจำลอง {stock.mock_price} · เปลี่ยนแปลงจำลอง {stock.mock_daily_change_pct}% · ไม่ใช่ราคาจาก Dime โดยตรง
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-sm font-semibold">Score {stock.final_score}</div>
                <StatusBadge status={stock.category} />
              </div>
            </div>
            <div className="mt-4 grid gap-3 sm:grid-cols-3 lg:grid-cols-6">
              <Score label="Trend" value={stock.trend_score} />
              <Score label="Momentum" value={stock.momentum_score} />
              <Score label="Quality" value={stock.quality_score} />
              <Score label="Liquidity" value={stock.liquidity_score} />
              <Score label="Valuation Risk" value={stock.valuation_risk_score} />
              <Score label="Volatility Risk" value={stock.volatility_risk_score} />
            </div>
            <div className="mt-4 grid gap-4 md:grid-cols-2">
              <div>
                <div className="text-sm font-medium">เหตุผลหลัก</div>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted">{stock.key_reasons.map((item) => <li key={item}>{item}</li>)}</ul>
              </div>
              <div>
                <div className="text-sm font-medium">ข้อควรระวัง</div>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted">{stock.caution_points.map((item) => <li key={item}>{item}</li>)}</ul>
              </div>
            </div>
            <div className="mt-4">
              <div className="text-sm font-medium">ร่องรอยการจัดอันดับ</div>
              <ol className="mt-2 list-decimal space-y-1 pl-5 text-sm text-muted">
                {stock.explanation_trace.slice(0, 4).map((item) => <li key={item}>{item}</li>)}
              </ol>
            </div>
            <div className="mt-4 flex gap-2">
              <Link href={`/stocks/${stock.symbol}/explain`} className="rounded-md border border-line px-3 py-2 text-sm font-medium hover:bg-panel">ดูคำอธิบาย</Link>
              <Link href={`/stocks/${stock.symbol}/practice-plan`} className="rounded-md border border-line px-3 py-2 text-sm font-medium hover:bg-panel">ดูแผนวิเคราะห์จำลอง</Link>
            </div>
          </Card>
        ))}
      </div>
      {stocks.length > 0 ? <DataFreshnessCard freshness={discovery.data_freshness} /> : <EmptyState title="ยังไม่มีหุ้นใน Radar" detail="ถ้า backend พร้อมใช้งานแล้ว ให้ลองโหลดหน้าใหม่อีกครั้ง" />}
    </div>
  );
}

function Score({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-md border border-line bg-panel px-3 py-2">
      <div className="text-[11px] font-medium text-muted">{label}</div>
      <div className="mt-1 text-sm font-semibold">{value}/100</div>
    </div>
  );
}
