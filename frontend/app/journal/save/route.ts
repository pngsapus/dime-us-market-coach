import { NextRequest, NextResponse } from "next/server";
import { API_BASE, redirectWithMessage } from "@/lib/serverApi";

export async function POST(request: NextRequest) {
  const form = await request.formData();
  const payload = {
    symbol: String(form.get("symbol") ?? "").trim().toUpperCase(),
    decision: String(form.get("decision") ?? "").trim(),
    reason: String(form.get("reason") ?? "").trim(),
    result: String(form.get("result") ?? "").trim(),
    lesson_learned: String(form.get("lesson_learned") ?? "").trim(),
  };

  if (!payload.symbol) {
    return NextResponse.redirect(redirectWithMessage(request.url, "/journal", { error: "กรุณาระบุ Symbol" }), 303);
  }
  if (!payload.decision) {
    return NextResponse.redirect(redirectWithMessage(request.url, "/journal", { error: "กรุณาระบุการตัดสินใจหรือสถานะ" }), 303);
  }
  if (!payload.reason && !payload.lesson_learned) {
    return NextResponse.redirect(redirectWithMessage(request.url, "/journal", { error: "กรุณาระบุเหตุผลหรือบทเรียนที่ได้อย่างน้อยหนึ่งรายการ" }), 303);
  }

  try {
    const response = await fetch(`${API_BASE}/journal`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      cache: "no-store",
    });
    if (!response.ok) {
      return NextResponse.redirect(redirectWithMessage(request.url, "/journal", { error: "บันทึกไม่สำเร็จ" }), 303);
    }
    return NextResponse.redirect(redirectWithMessage(request.url, "/journal", { saved: "1" }), 303);
  } catch {
    return NextResponse.redirect(redirectWithMessage(request.url, "/journal", { error: "ไม่สามารถเชื่อมต่อ backend เพื่อบันทึก Journal ได้" }), 303);
  }
}
