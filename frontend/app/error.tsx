"use client";

import { ErrorState } from "@/components/ErrorState";

export default function Error({ reset }: { error: Error; reset: () => void }) {
  return (
    <div className="space-y-4">
      <ErrorState
        title="ไม่สามารถแสดงหน้านี้ได้"
        detail="ระบบพบข้อผิดพลาดระหว่างโหลดหน้า กรุณาลองใหม่อีกครั้ง"
        retryHref="."
      />
      <button onClick={reset} className="rounded-md bg-accent px-3 py-2 text-sm font-medium text-white">
        โหลดหน้าใหม่
      </button>
    </div>
  );
}
