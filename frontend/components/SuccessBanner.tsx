export function SuccessBanner({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded-md border border-emerald-100 bg-emerald-50 p-3 text-sm text-accent">
      {children}
    </div>
  );
}
