export function MetricCard({ label, value, tone = "default" }: { label: string; value: string | number; tone?: "default" | "warning" }) {
  const toneClass = tone === "warning" ? "border-amber-100 bg-amber-50" : "border-line bg-panel";
  return (
    <div className={`rounded-md border p-4 ${toneClass}`}>
      <div className="text-xs font-medium text-muted">{label}</div>
      <div className="mt-1 text-lg font-semibold text-ink">{value}</div>
    </div>
  );
}
