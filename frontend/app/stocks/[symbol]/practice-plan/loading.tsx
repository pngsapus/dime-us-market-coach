export default function Loading() {
  return (
    <div className="space-y-4">
      <div className="h-8 w-72 animate-pulse rounded bg-line" />
      <div className="rounded-md border border-line bg-white p-6 shadow-sm">
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
          {Array.from({ length: 5 }).map((_, index) => (
            <div key={index} className="h-20 animate-pulse rounded bg-panel" />
          ))}
        </div>
      </div>
    </div>
  );
}
