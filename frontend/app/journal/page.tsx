import { Card } from "@/components/Card";
import { EmptyState } from "@/components/EmptyState";
import { FormBanner } from "@/components/FormBanner";
import { PageActions } from "@/components/PageActions";
import { PageHeader } from "@/components/PageHeader";
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
      <PageHeader
        title="บันทึกการฝึกวิเคราะห์"
        description="จบ workflow ด้วยการบันทึกเหตุผล ผลลัพธ์ และบทเรียนที่ได้จากแผนจำลอง"
      />
      <PageActions actions={[{ href: "/dime-check", label: "กลับไป Dime Check" }, { href: "/dashboard", label: "เริ่มดูภาพรวมใหม่" }]} />

      {params.saved === "1" && <FormBanner type="success">บันทึกเรียบร้อย</FormBanner>}
      {params.error && <FormBanner type="error">{params.error}</FormBanner>}
      {!result.ok && <FormBanner type="error">ไม่สามารถโหลดรายการบันทึกจาก backend ได้</FormBanner>}

      <Card>
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
      </Card>

      <Card>
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
          {entries.length === 0 && <EmptyState title="ยังไม่มีบันทึก" detail="เมื่อบันทึกแผนหรือบทเรียน รายการจะแสดงตรงนี้และเก็บใน SQLite" />}
        </div>
      </Card>
    </div>
  );
}
