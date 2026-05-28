import Link from "next/link";

export function PageActions({ actions }: { actions: Array<{ href: string; label: string; primary?: boolean }> }) {
  return (
    <div className="flex flex-wrap gap-2">
      {actions.map((action) => (
        <Link
          key={action.href}
          href={action.href}
          className={action.primary ? "rounded-md bg-accent px-3 py-2 text-sm font-medium text-white" : "rounded-md border border-line bg-white px-3 py-2 text-sm font-medium hover:bg-panel"}
        >
          {action.label}
        </Link>
      ))}
    </div>
  );
}
