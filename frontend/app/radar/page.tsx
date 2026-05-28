import Link from "next/link";
import { StatusBadge } from "@/components/StatusBadge";
import { getDiscoveryLatest, getRadar } from "@/lib/api";
import { ApiErrorState } from "@/components/ApiErrorState";
import { Card } from "@/components/Card";
import { DataFreshnessCard } from "@/components/DataFreshnessCard";
import { EmptyState } from "@/components/EmptyState";
import { PageActions } from "@/components/PageActions";
import { PageHeader } from "@/components/PageHeader";
import { WarningBox } from "@/components/WarningBox";
import type { DiscoveryResult, DiscoveryRun, StockSnapshot } from "@/lib/types";

export default async function RadarPage() {
  const result = await getRadarDiscovery();
  if (!result.ok) {
    return (
      <ApiErrorState
        title="ไม่สามารถโหลดข้อมูล Radar Discovery ได้"
        detail={result.message}
        retryHref="/radar"
      />
    );
  }
  const discovery = result.data;
  const stocks = discovery.results;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Radar หุ้นที่ควรติดตาม"
        description="ระบบจำลองนี้ช่วยจัดอันดับหุ้นจากข้อมูลตัวอย่าง เพื่อให้คุณเลือกตัวที่อยากศึกษาต่อ ไม่ใช่คำแนะนำให้ซื้อขาย"
      />
      <p className="max-w-3xl text-sm leading-6 text-muted">
        เลือกหุ้นที่อยากศึกษาต่อจาก Radar หรือใช้เมนูด้านซ้ายเพื่อข้ามไปยังหน้าที่ต้องการได้ตลอด ปุ่มในหน้านี้เป็นขั้นตอนแนะนำสำหรับไปวิเคราะห์ต่อเท่านั้น
      </p>
      <PageActions actions={[{ href: "/dashboard", label: "กลับไป Dashboard" }]} />
      <WarningBox title="ข้อมูลจำลองในเครื่อง">
        {discovery.disclaimer} ใช้เพื่อประกอบการพิจารณาเท่านั้น ไม่ใช่คำสั่งซื้อ
      </WarningBox>
      <Card>
        <h2 className="text-base font-semibold">วิธีใช้หน้านี้</h2>
        <ol className="mt-3 grid gap-2 text-sm leading-6 text-muted sm:grid-cols-2 lg:grid-cols-4">
          <li>1. ดูสถานะและคะแนนภาพรวม</li>
          <li>2. อ่านเหตุผลและข้อควรระวัง</li>
          <li>3. เลือกหุ้นที่อยากศึกษาต่อ</li>
          <li>4. ไปหน้าอธิบายหุ้นหรือแผนวิเคราะห์จำลอง</li>
        </ol>
      </Card>
      <div className="grid gap-4">
        {stocks.map((stock) => (
          <Card key={stock.symbol}>
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="max-w-3xl">
                <div className="text-xs font-semibold text-muted">อันดับ {stock.rank} · {stock.sector_theme}</div>
                <h2 className="mt-1 text-lg font-semibold">{stock.symbol} · {stock.name}</h2>
                <div className="mt-1 text-sm text-muted">
                  ราคาจำลอง {stock.mock_price} · เปลี่ยนแปลงจำลอง {stock.mock_daily_change_pct}% · ความสด {stock.data_freshness.age_minutes} นาที
                </div>
                <p className="mt-3 text-sm leading-6 text-muted">{stock.beginner_summary}</p>
              </div>
              <div className="flex shrink-0 items-center gap-3">
                <div className="text-sm font-semibold">Score {stock.final_score}</div>
                <StatusBadge status={stock.category} />
              </div>
            </div>
            <div className="mt-4 grid gap-4 md:grid-cols-2">
              <div>
                <div className="text-sm font-medium">เหตุผลหลัก</div>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted">{stock.key_reasons.slice(0, 3).map((item) => <li key={item}>{item}</li>)}</ul>
              </div>
              <div>
                <div className="text-sm font-medium">ข้อควรระวัง</div>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted">{stock.caution_points.slice(0, 3).map((item) => <li key={item}>{item}</li>)}</ul>
              </div>
            </div>
            <details className="mt-4 rounded-md border border-line bg-panel px-3 py-2 text-sm text-muted">
              <summary className="cursor-pointer font-medium text-ink">ดูรายละเอียดคะแนนและร่องรอยการจัดอันดับ</summary>
              <div className="mt-3 grid gap-2 sm:grid-cols-3 lg:grid-cols-6">
                <Score label="แนวโน้ม" value={stock.trend_score} />
                <Score label="โมเมนตัม" value={stock.momentum_score} />
                <Score label="คุณภาพ" value={stock.quality_score} />
                <Score label="สภาพคล่อง" value={stock.liquidity_score} />
                <Score label="ความเสี่ยงมูลค่า" value={stock.valuation_risk_score} />
                <Score label="ความผันผวน" value={stock.volatility_risk_score} />
              </div>
              <ol className="mt-3 list-decimal space-y-1 pl-5">
                {stock.explanation_trace.map((item) => <li key={item}>{item}</li>)}
              </ol>
            </details>
            <div className="mt-4 flex flex-wrap gap-2">
              <Link href={`/stocks/${stock.symbol}/explain`} className="rounded-md border border-line px-3 py-2 text-sm font-medium hover:bg-panel">อ่านคำอธิบาย</Link>
              <Link href={`/stocks/${stock.symbol}/practice-plan`} className="rounded-md border border-line px-3 py-2 text-sm font-medium hover:bg-panel">ดูแผนวิเคราะห์จำลอง</Link>
            </div>
          </Card>
        ))}
      </div>
      {stocks.length > 0 ? <DataFreshnessCard freshness={discovery.data_freshness} /> : <EmptyState title="ยังไม่มีหุ้นใน Radar" detail="ถ้า backend พร้อมใช้งานแล้ว ให้ลองโหลดหน้าใหม่อีกครั้ง" />}
    </div>
  );
}

async function getRadarDiscovery(): Promise<{ ok: true; data: DiscoveryRun } | { ok: false; message: string }> {
  const discoveryResult = await getDiscoveryLatest();
  if (discoveryResult.ok) return discoveryResult;

  const radarResult = await getRadar();
  if (!radarResult.ok) {
    return {
      ok: false,
      message: `${discoveryResult.message}; fallback /api/radar ก็โหลดไม่สำเร็จ: ${radarResult.message}`,
    };
  }

  if (!Array.isArray(radarResult.data) || radarResult.data.length === 0) {
    return {
      ok: false,
      message: `${discoveryResult.message}; fallback /api/radar ไม่มีรายการให้แสดง`,
    };
  }

  return {
    ok: true,
    data: adaptRadarSnapshots(radarResult.data, discoveryResult.message),
  };
}

function adaptRadarSnapshots(stocks: StockSnapshot[], sourceMessage: string): DiscoveryRun {
  const firstFreshness = stocks[0].data_freshness;
  return {
    generated_at: firstFreshness.as_of,
    universe_count: stocks.length,
    data_freshness: firstFreshness,
    disclaimer: `ใช้ข้อมูล /api/radar compatibility เพราะ ${sourceMessage} ข้อมูลนี้เป็นข้อมูลจำลองในเครื่อง ไม่ใช่ราคาจาก Dime โดยตรง`,
    results: stocks.map((stock, index) => adaptStockSnapshot(stock, index + 1)),
  };
}

function adaptStockSnapshot(stock: StockSnapshot, rank: number): DiscoveryResult {
  return {
    symbol: stock.symbol,
    name: stock.company_name,
    sector_theme: stock.market_context,
    beginner_summary: stock.market_context,
    rank,
    final_score: stock.score,
    category: stock.status,
    key_reasons: stock.reasons,
    caution_points: stock.cautions,
    explanation_trace: stock.explanation_trace,
    data_freshness: stock.data_freshness,
    disclaimer: "ข้อมูลนี้เป็นข้อมูลจำลอง ไม่ใช่ราคาจาก Dime โดยตรง",
    mock_price: stock.price,
    mock_daily_change_pct: 0,
    trend_score: stock.score,
    momentum_score: stock.score,
    quality_score: stock.score,
    valuation_risk_score: 0,
    volatility_risk_score: 0,
    liquidity_score: stock.score,
    beginner_fit_score: stock.score,
  };
}

function Score({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-md border border-line bg-panel px-3 py-2">
      <div className="text-[11px] font-medium text-muted">{label}</div>
      <div className="mt-1 text-sm font-semibold">{value}/100</div>
    </div>
  );
}
