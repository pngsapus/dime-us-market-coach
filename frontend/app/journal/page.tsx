import { FormBanner } from "@/components/FormBanner";
import { SubmitButton } from "@/components/SubmitButton";
import { API_BASE } from "@/lib/serverApi";

type JournalEntry = {
  id: number;
  symbol: string;
  decision: string;
  reason: string;
  result: string;
  lesson_learned: string;
  created_at: string;
};

type PageProps = {
  searchParams: Promise<{ saved?: string; error?: string }>;
};

async function getJournal(): Promise<{ ok: true; data: JournalEntry[] } | { ok: false }> {
  try {
    const response = await fetch(`${API_BASE}/journal`, { cache: "no-store" });
    if (!response.ok) return { ok: false };
    return { ok: true, data: await response.json() };
  } catch {
    return { ok: false };
  }
}

export default async function JournalPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const result = await getJournal();
  const entries = result.ok ? result.data : [];

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">บันทึกการฝึกวิเคราะห์</h1>
        <p className="mt-1 text-sm text-muted">บันทึกเหตุผล ผลลัพธ์ และบทเรียนจากการฝึกวิเคราะห์</p>
      </header>

      {params.saved === "1" && <FormBanner type="success">บันทึกเรียบร้อย</FormBanner>}
      {params.error && <FormBanner type="error">{params.error}</FormBanner>}
      {!result.ok && <FormBanner type="error">ไม่สามารถโหลดรายการบันทึกจาก backend ได้</FormBanner>}

      <section className="rounded-md border border-line bg-white p-6 shadow-sm">
        <form action="/journal/save" method="post" className="space-y-4">
          <div className="grid gap-3 sm:grid-cols-2">
            <input name="symbol" defaultValue="NVDA" className="rounded-md border border-line px-3 py-2 text-sm" placeholder="Symbol" />
            <input name="decision" defaultValue="รอจังหวะ" className="rounded-md border border-line px-3 py-2 text-sm" placeholder="การตัดสินใจ" />
            <textarea name="reason" className="min-h-24 rounded-md border border-line px-3 py-2 text-sm" placeholder="เหตุผล" />
            <textarea name="lesson_learned" className="min-h-24 rounded-md border border-line px-3 py-2 text-sm" placeholder="บทเรียนที่ได้" />
            <textarea name="result" className="min-h-20 rounded-md border border-line px-3 py-2 text-sm sm:col-span-2" placeholder="ผลลัพธ์หรือสิ่งที่สังเกตได้ (ถ้ามี)" />
          </div>
          <SubmitButton idleLabel="บันทึก" loadingLabel="กำลังบันทึก..." />
        </form>
      </section>

      <section className="rounded-md border border-line bg-white p-6 shadow-sm">
        <h2 className="text-base font-semibold">รายการล่าสุด</h2>
        <div className="mt-3 divide-y divide-line">
          {entries.map((entry) => (
            <div key={entry.id} className="py-3 text-sm">
              <div className="font-medium">{entry.symbol} · {entry.decision}</div>
              {entry.reason && <div className="mt-1 text-muted">เหตุผล: {entry.reason}</div>}
              {entry.result && <div className="mt-1 text-muted">ผลลัพธ์: {entry.result}</div>}
              {entry.lesson_learned && <div className="mt-1 text-muted">บทเรียนที่ได้: {entry.lesson_learned}</div>}
            </div>
          ))}
          {entries.length === 0 && <div className="py-3 text-sm text-muted">ยังไม่มีบันทึก</div>}
        </div>
      </section>
    </div>
  );
}
