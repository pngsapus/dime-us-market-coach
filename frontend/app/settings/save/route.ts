import { NextRequest, NextResponse } from "next/server";
import { backendFetch, redirectWithMessage } from "@/lib/serverApi";

export async function POST(request: NextRequest) {
  const form = await request.formData();
  const payload = {
    beginner_level: String(form.get("beginner_level") ?? "new"),
    max_loss_per_trade_thb: Number(form.get("max_loss_per_trade_thb")),
    max_trades_per_day: Number(form.get("max_trades_per_day")),
    minimum_risk_reward: Number(form.get("minimum_risk_reward")),
    preferred_setup_type: String(form.get("preferred_setup_type") ?? "pullback").trim() || "pullback",
  };

  if (!Number.isFinite(payload.max_loss_per_trade_thb) || payload.max_loss_per_trade_thb <= 0) {
    return NextResponse.redirect(redirectWithMessage(request.url, "/settings", { error: "กรุณาระบุขาดทุนสูงสุดต่อไม้ให้ถูกต้อง" }), 303);
  }
  if (!Number.isInteger(payload.max_trades_per_day) || payload.max_trades_per_day < 1) {
    return NextResponse.redirect(redirectWithMessage(request.url, "/settings", { error: "กรุณาระบุจำนวนไม้สูงสุดต่อวันให้ถูกต้อง" }), 303);
  }
  if (!Number.isFinite(payload.minimum_risk_reward) || payload.minimum_risk_reward <= 0) {
    return NextResponse.redirect(redirectWithMessage(request.url, "/settings", { error: "กรุณาระบุ Risk:Reward ขั้นต่ำให้ถูกต้อง" }), 303);
  }

  try {
    const response = await backendFetch("/settings/risk-profile", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      cache: "no-store",
    });
    if (!response.ok) {
      return NextResponse.redirect(redirectWithMessage(request.url, "/settings", { error: "บันทึก Risk Profile ไม่สำเร็จ" }), 303);
    }
    return NextResponse.redirect(redirectWithMessage(request.url, "/settings", { saved: "1" }), 303);
  } catch {
    return NextResponse.redirect(redirectWithMessage(request.url, "/settings", { error: "ไม่สามารถเชื่อมต่อ backend เพื่อบันทึก Risk Profile ได้" }), 303);
  }
}
