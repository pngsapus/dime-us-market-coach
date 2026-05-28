"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3, BookOpen, ClipboardCheck, Gauge, LineChart, Radar, Settings, ShieldAlert } from "lucide-react";

const nav = [
  { href: "/dashboard", label: "ภาพรวมตลาด", icon: Gauge, match: (path: string) => path === "/dashboard" },
  { href: "/radar", label: "Radar", icon: Radar, match: (path: string) => path === "/radar" },
  { href: "/stocks/NVDA/explain", label: "อธิบายหุ้น", icon: BookOpen, match: (path: string) => path.includes("/explain") },
  { href: "/stocks/NVDA/practice-plan", label: "แผนวิเคราะห์จำลอง", icon: ClipboardCheck, match: (path: string) => path.includes("/practice-plan") },
  { href: "/dime-check", label: "ตรวจราคา Dime", icon: ShieldAlert, match: (path: string) => path === "/dime-check" },
  { href: "/journal", label: "บันทึกการฝึกวิเคราะห์", icon: BarChart3, match: (path: string) => path === "/journal" },
  { href: "/settings", label: "ตั้งค่า Risk Profile", icon: Settings, match: (path: string) => path === "/settings" },
  { href: "/data-status", label: "สถานะข้อมูล", icon: LineChart, match: (path: string) => path === "/data-status" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="min-h-screen">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-line bg-white px-4 py-5 lg:block">
        <div className="mb-6">
          <div className="text-lg font-semibold">Dime US Market Coach</div>
          <div className="mt-1 text-xs text-muted">ใช้เพื่อการวิเคราะห์เท่านั้น · ข้อมูลจำลอง</div>
        </div>
        <nav className="space-y-1">
          {nav.map((item) => {
            const Icon = item.icon;
            const active = item.match(pathname);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 rounded-md px-3 py-2 text-sm transition ${active ? "bg-panel font-medium text-accent" : "text-ink hover:bg-panel"}`}
              >
                <Icon size={17} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
        <div className="mt-6 rounded-md border border-amber-100 bg-amber-50 p-3 text-xs leading-5 text-warn">
          ข้อมูลนี้ไม่ใช่ราคาจาก Dime โดยตรง และระบบไม่ส่งคำสั่งซื้อขาย
        </div>
      </aside>
      <main className="lg:pl-64">
        <div className="mx-auto max-w-6xl px-4 py-6 sm:px-6 lg:px-8">{children}</div>
      </main>
    </div>
  );
}
