"use client";

export default function Error({ reset }: { error: Error; reset: () => void }) {
  return (
    <section className="rounded-md border border-red-100 bg-red-50 p-5 text-sm">
      <h1 className="text-base font-semibold text-danger">ไม่สามารถแสดงหน้าอธิบายหุ้นได้</h1>
      <p className="mt-2 text-red-900">กรุณาตรวจสอบว่า backend mock API ทำงานอยู่ แล้วลองใหม่อีกครั้ง</p>
      <button onClick={reset} className="mt-4 rounded-md bg-white px-3 py-2 text-sm font-medium text-danger shadow-sm">
        Retry
      </button>
    </section>
  );
}
