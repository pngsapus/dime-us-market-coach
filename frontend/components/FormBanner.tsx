export function FormBanner({ type, children }: { type: "success" | "error"; children: React.ReactNode }) {
  const classes = type === "success"
    ? "border-emerald-100 bg-emerald-50 text-accent"
    : "border-red-100 bg-red-50 text-danger";

  return (
    <div className={`rounded-md border p-3 text-sm ${classes}`}>
      {children}
    </div>
  );
}
