import { ApiErrorState } from "@/components/ApiErrorState";
import { MetricCard } from "@/components/MetricCard";
import { PageActions } from "@/components/PageActions";
import { StatusBadge } from "@/components/StatusBadge";
import type { DimeCheckResponse } from "@/lib/types";

type PageProps = {
  searchParams: Promise<{ symbol?: string; price?: string }>;
};

async function checkPrice(symbol: string, price: number): Promise<{ ok: true; data: DimeCheckResponse } | { ok: false }> {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api"}/dime/check-price`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symbol, dime_price: price }),
      cache: "no-store",
    });
    if (!response.ok) return { ok: false };
    return { ok: true, data: await response.json() };
  } catch {
    return { ok: false };
  }
}

export default async function DimeCheckPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const symbol = (params.symbol ?? "NVDA").toUpperCase();
  const price = Number(params.price ?? "131");
  const shouldCheck = Boolean(params.price) && Number.isFinite(price) && price > 0;
  const result = shouldCheck ? await checkPrice(symbol, price) : null;

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">ตรวจสอบราคาจริงใน Dime</h1>
        <p className="mt-1 text-sm text-muted">กรอกราคาที่เห็นใน Dime เอง เพื่อเช็กว่าแผนวิเคราะห์จำลองยังอยู่ในเกณฑ์หรือไม่</p>
        <p className="mt-1 text-sm text-muted">ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง และระบบไม่ส่งคำสั่งซื้อขาย</p>
      </header>

      <PageActions actions={[{ href: "/stocks/NVDA/practice-plan", label: "กลับไปแผนวิเคราะห์จำลอง" }, { href: "/journal", label: "ไปที่บันทึกการฝึกวิเคราะห์" }]} />

      <section className="rounded-md border border-line bg-white p-6 shadow-sm">
        <form className="grid gap-4 sm:grid-cols-3" action="/dime-check">
          <label className="text-sm">
            <span className="font-medium">Symbol</span>
            <select name="symbol" defaultValue={symbol} className="mt-2 w-full rounded-md border border-line px-3 py-2">
              <option>NVDA</option>
              <option>AMD</option>
              <option>TSLA</option>
            </select>
          </label>
          <label className="text-sm">
            <span className="font-medium">ราคาที่เห็นใน Dime</span>
            <input name="price" defaultValue={price} type="number" step="0.01" min="0.01" className="mt-2 w-full rounded-md border border-line px-3 py-2" />
          </label>
          <button type="submit" className="self-end rounded-md bg-accent px-4 py-2 text-sm font-medium text-white">
            ตรวจสอบแผน
          </button>
        </form>
      </section>

      {result && !result.ok && <ApiErrorState retryHref={`/dime-check?symbol=${symbol}&price=${price}`} />}

      {result?.ok && (
        <section className="rounded-md border border-line bg-white p-6 shadow-sm">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h2 className="text-lg font-semibold">ผลตรวจสอบแผน</h2>
              <p className="mt-1 text-sm text-muted">ใช้เพื่อประกอบการพิจารณาเท่านั้น ไม่ใช่คำสั่งซื้อ</p>
            </div>
            <StatusBadge status={result.data.status} />
          </div>

          <p className="mt-4 rounded-md bg-panel p-4 text-sm leading-6 text-muted">{result.data.reason}</p>

          <div className="mt-4 grid gap-3 sm:grid-cols-3">
            <MetricCard label="ราคาที่กรอก" value={result.data.dime_price} />
            <MetricCard label="Risk:Reward ใหม่" value={result.data.risk_reward} />
            <MetricCard label="สถานะความเสี่ยง" value={result.data.passes_risk_profile ? "ผ่านเกณฑ์" : "ไม่ผ่านเกณฑ์"} tone={result.data.passes_risk_profile ? "default" : "warning"} />
          </div>

          <div className="mt-4 rounded-md border border-line bg-white p-4">
            <div className="text-sm font-medium">แนวทางถัดไป</div>
            <div className="mt-1 text-sm text-muted">{result.data.action}</div>
          </div>

          {result.data.explanation_trace.length > 0 && (
            <div className="mt-5">
              <h3 className="text-sm font-semibold">Explanation trace</h3>
              <ol className="mt-2 list-decimal space-y-2 pl-5 text-sm leading-6 text-muted">
                {result.data.explanation_trace.map((item) => <li key={item}>{item}</li>)}
              </ol>
            </div>
          )}
        </section>
      )}
    </div>
  );
}
