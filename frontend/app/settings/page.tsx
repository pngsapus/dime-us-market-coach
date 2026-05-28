import { Card } from "@/components/Card";
import { FormBanner } from "@/components/FormBanner";
import { PageActions } from "@/components/PageActions";
import { PageHeader } from "@/components/PageHeader";
import { SubmitButton } from "@/components/SubmitButton";
import { backendFetch } from "@/lib/serverApi";
import type { RiskProfile } from "@/lib/types";

const defaultProfile: RiskProfile = {
  beginner_level: "new",
  max_loss_per_trade_thb: 1000,
  max_trades_per_day: 2,
  minimum_risk_reward: 1.5,
  preferred_setup_type: "pullback",
};

type PageProps = {
  searchParams: Promise<{ saved?: string; error?: string }>;
};

async function getRiskProfile(): Promise<{ ok: true; data: RiskProfile } | { ok: false }> {
  try {
    const response = await backendFetch("/settings/risk-profile", { cache: "no-store" });
    if (!response.ok) return { ok: false };
    return { ok: true, data: await response.json() };
  } catch {
    return { ok: false };
  }
}

export default async function SettingsPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const result = await getRiskProfile();
  const profile = result.ok ? result.data : defaultProfile;

  return (
    <div className="space-y-6">
      <PageHeader
        title="ตั้งค่า Risk Profile"
        description="กำหนดเพดานความเสี่ยงที่ใช้คำนวณแผนวิเคราะห์จำลอง"
      />
      <PageActions actions={[{ href: "/journal", label: "ไปที่บันทึกการฝึกวิเคราะห์" }, { href: "/data-status", label: "ดูสถานะข้อมูล" }]} />

      {params.saved === "1" && <FormBanner type="success">บันทึก Risk Profile เรียบร้อย</FormBanner>}
      {params.error && <FormBanner type="error">{params.error}</FormBanner>}
      {!result.ok && <FormBanner type="error">ไม่สามารถโหลด Risk Profile จาก backend ได้ กำลังแสดงค่าเริ่มต้นชั่วคราว</FormBanner>}

      <Card>
        <form action="/settings/save" method="post" className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="text-sm">
              <span className="font-medium">ระดับผู้ใช้</span>
              <select name="beginner_level" defaultValue={profile.beginner_level} className="mt-2 w-full rounded-md border border-line px-3 py-2">
                <option value="new">เริ่มต้น</option>
                <option value="learning">กำลังเรียนรู้</option>
                <option value="confident">มีประสบการณ์</option>
              </select>
            </label>
            <NumberInput name="max_loss_per_trade_thb" label="ขาดทุนสูงสุดต่อไม้ (บาท)" defaultValue={profile.max_loss_per_trade_thb} step="0.01" />
            <NumberInput name="max_trades_per_day" label="จำนวนไม้สูงสุดต่อวัน" defaultValue={profile.max_trades_per_day} step="1" />
            <NumberInput name="minimum_risk_reward" label="Risk:Reward ขั้นต่ำ" defaultValue={profile.minimum_risk_reward} step="0.01" />
            <label className="text-sm">
              <span className="font-medium">รูปแบบแผนที่ต้องการ</span>
              <input name="preferred_setup_type" defaultValue={profile.preferred_setup_type} className="mt-2 w-full rounded-md border border-line px-3 py-2" />
            </label>
          </div>
          <SubmitButton idleLabel="บันทึก Risk Profile" loadingLabel="กำลังบันทึก..." />
        </form>
      </Card>
    </div>
  );
}

function NumberInput({ name, label, defaultValue, step }: { name: string; label: string; defaultValue: number; step: string }) {
  return (
    <label className="text-sm">
      <span className="font-medium">{label}</span>
      <input name={name} defaultValue={defaultValue} type="number" min="0" step={step} className="mt-2 w-full rounded-md border border-line px-3 py-2" />
    </label>
  );
}
