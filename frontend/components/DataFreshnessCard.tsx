import type { DataFreshness } from "@/lib/types";

export function DataFreshnessCard({ freshness }: { freshness: DataFreshness }) {
  const providerLabel = freshness.provider === "mock_provider" ? "ผู้ให้ข้อมูลจำลอง" : freshness.provider;
  const stateLabel = freshness.is_stale ? "ข้อมูลล่าช้า / degraded" : "ข้อมูลจำลองพร้อมใช้";
  const toneClass = freshness.is_stale ? "border-amber-100 bg-amber-50" : "border-line bg-white";

  return (
    <section className={`rounded-md border p-4 text-sm shadow-sm ${toneClass}`}>
      <div className="font-medium">ความสดของข้อมูล</div>
      <div className="mt-1 text-muted">
        {providerLabel} · {freshness.age_minutes} นาที · {stateLabel}
      </div>
      <div className="mt-2 rounded-md bg-white/70 p-2 text-xs leading-5 text-muted">
        {freshness.note || "ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง"}
      </div>
    </section>
  );
}
