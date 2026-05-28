export function EmptyState({ title, detail }: { title: string; detail?: string }) {
  return (
    <div className="rounded-md border border-line bg-panel p-5 text-sm">
      <div className="font-medium">{title}</div>
      {detail && <div className="mt-1 leading-6 text-muted">{detail}</div>}
    </div>
  );
}
