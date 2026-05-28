import { ApiErrorState } from "@/components/ApiErrorState";
import { Card } from "@/components/Card";
import { ExplanationTrace } from "@/components/ExplanationTrace";
import { MetricCard } from "@/components/MetricCard";
import { PageActions } from "@/components/PageActions";
import { PageHeader } from "@/components/PageHeader";
import { StatusBadge } from "@/components/StatusBadge";
import { WarningBox } from "@/components/WarningBox";
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
      <PageHeader
        title="ตรวจสอบราคาจริงใน Dime"
        description="กรอกราคาที่เห็นใน Dime ด้วยตนเอง เพื่อเช็กว่าแผนวิเคราะห์จำลองยังอยู่ในเกณฑ์หรือไม่"
      />

      <PageActions actions={[{ href: `/stocks/${symbol}/practice-plan`, label: "กลับไปแผนวิเคราะห์จำลอง" }, { href: "/journal", label: "ไปที่บันทึกการฝึกวิเคราะห์" }]} />

      <WarningBox title="จุดตรวจสอบสำคัญ">
        ระบบไม่ดึงราคาจาก Dime โดยตรง ผู้ใช้ต้องกรอกราคาที่เห็นใน Dime เองก่อนประเมินแผน
      </WarningBox>

      <Card>
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
      </Card>

      {result && !result.ok && <ApiErrorState retryHref={`/dime-check?symbol=${symbol}&price=${price}`} />}

      {result?.ok && (
        <Card>
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

          <div className="mt-5">
            <PageActions actions={[{ href: "/journal", label: "บันทึกบทเรียนใน Journal", primary: true }]} />
          </div>
        </Card>
      )}
      {result?.ok && <ExplanationTrace items={result.data.explanation_trace} />}
    </div>
  );
}
