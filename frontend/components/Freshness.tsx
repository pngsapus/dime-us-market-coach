import type { DataFreshness } from "@/lib/types";

export function Freshness({ freshness }: { freshness: DataFreshness }) {
  const providerLabel = freshness.provider === "mock_provider" ? "ผู้ให้ข้อมูลจำลอง" : freshness.provider;
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm shadow-sm">
      <div className="font-medium">ความสดของข้อมูล</div>
      <div className="mt-1 text-muted">
        {providerLabel} · {freshness.age_minutes} นาที · {freshness.is_stale ? "ข้อมูลล่าช้า" : "พร้อมใช้"}
      </div>
      <div className="mt-1 text-xs text-muted">{freshness.note}</div>
    </div>
  );
}
