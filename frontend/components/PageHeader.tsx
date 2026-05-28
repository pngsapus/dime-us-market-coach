import { StatusBadge } from "./StatusBadge";

export function PageHeader({
  title,
  description,
  eyebrow,
  status,
}: {
  title: string;
  description?: string;
  eyebrow?: string;
  status?: string;
}) {
  return (
    <header className="flex flex-wrap items-start justify-between gap-3">
      <div>
        {eyebrow && <div className="mb-1 text-xs font-medium uppercase tracking-wide text-muted">{eyebrow}</div>}
        <h1 className="text-2xl font-semibold">{title}</h1>
        {description && <p className="mt-1 max-w-3xl text-sm leading-6 text-muted">{description}</p>}
      </div>
      {status && <StatusBadge status={status} />}
    </header>
  );
}
