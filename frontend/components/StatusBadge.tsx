export function StatusBadge({ status }: { status: string }) {
  const tone = status.includes("ไม่") || status.includes("ยกเลิก") || status.includes("ล่าช้า") || status.includes("ไม่เพียงพอ")
    ? "border-red-100 bg-red-50 text-danger"
    : status.includes("รอ") || status.includes("ยังไม่เข้าโซน")
      ? "border-amber-100 bg-amber-50 text-warn"
      : "border-emerald-100 bg-emerald-50 text-accent";
  return <span className={`inline-flex rounded-full border px-3 py-1 text-xs font-medium ${tone}`}>{status}</span>;
}
