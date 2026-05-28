export function WarningBox({ title = "ข้อควรระวัง", children }: { title?: string; children: React.ReactNode }) {
  return (
    <div className="rounded-md border border-amber-100 bg-amber-50 p-4 text-sm">
      <div className="font-medium text-warn">{title}</div>
      <div className="mt-1 leading-6 text-amber-900">{children}</div>
    </div>
  );
}
