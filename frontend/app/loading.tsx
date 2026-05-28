export default function Loading() {
  return (
    <div className="space-y-4">
      <div className="h-8 w-64 animate-pulse rounded bg-line" />
      <div className="rounded-md border border-line bg-white p-6 shadow-sm">
        <div className="h-5 w-48 animate-pulse rounded bg-line" />
        <div className="mt-4 h-24 animate-pulse rounded bg-panel" />
      </div>
    </div>
  );
}
