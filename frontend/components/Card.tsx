export function Card({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <section className={`rounded-md border border-line bg-white p-6 shadow-sm ${className}`}>
      {children}
    </section>
  );
}
