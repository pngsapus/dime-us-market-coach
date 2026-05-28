import { Card } from "./Card";

export function ExplanationTrace({ items, title = "เหตุผลเชิงระบบ" }: { items: string[]; title?: string }) {
  if (items.length === 0) {
    return null;
  }

  return (
    <Card>
      <h2 className="text-base font-semibold">{title}</h2>
      <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm leading-6 text-muted">
        {items.map((item) => <li key={item}>{item}</li>)}
      </ol>
    </Card>
  );
}
