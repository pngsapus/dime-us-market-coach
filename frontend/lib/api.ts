import type { DataStatus, DiscoveryRun, MarketSummary, PracticePlan, RiskProfile, StockExplain, StockSnapshot } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api";

export type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; message: string; retryPath: string };

async function getJson<T>(path: string): Promise<ApiResult<T>> {
  try {
    const response = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
    if (!response.ok) {
      return {
        ok: false,
        message: `backend ตอบกลับ HTTP ${response.status} สำหรับ ${path}`,
        retryPath: path,
      };
    }
    try {
      return { ok: true, data: (await response.json()) as T };
    } catch {
      return {
        ok: false,
        message: `อ่านข้อมูล JSON จาก backend ไม่สำเร็จสำหรับ ${path}`,
        retryPath: path,
      };
    }
  } catch {
    return {
      ok: false,
      message: "ไม่สามารถเชื่อมต่อข้อมูลจำลองจาก backend ได้",
      retryPath: path,
    };
  }
}

export function getMarketSummary() {
  return getJson<MarketSummary>("/market/summary");
}

export function getRadar() {
  return getJson<StockSnapshot[]>("/radar");
}

export function getDiscoveryLatest() {
  return getJson<unknown>("/discovery/latest").then((result): ApiResult<DiscoveryRun> => {
    if (!result.ok) return result;
    if (!isDiscoveryRun(result.data)) {
      return {
        ok: false,
        message: "รูปแบบข้อมูล Discovery จาก backend ไม่ตรงกับที่ Radar ต้องใช้",
        retryPath: "/discovery/latest",
      };
    }
    return { ok: true, data: result.data };
  });
}

export function getStockExplain(symbol: string) {
  return getJson<StockExplain>(`/stocks/${symbol}/explain`);
}

export function getPracticePlan(symbol: string) {
  return getJson<PracticePlan>(`/stocks/${symbol}/practice-plan`);
}

export function getRiskProfile() {
  return getJson<RiskProfile>("/settings/risk-profile");
}

export function getDataStatus() {
  return getJson<DataStatus>("/data-status");
}

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function isDiscoveryRun(value: unknown): value is DiscoveryRun {
  if (!isObject(value) || !Array.isArray(value.results)) return false;
  return value.results.every((item) => (
    isObject(item) &&
    typeof item.symbol === "string" &&
    typeof item.name === "string" &&
    typeof item.beginner_summary === "string" &&
    typeof item.rank === "number" &&
    typeof item.final_score === "number" &&
    typeof item.category === "string" &&
    Array.isArray(item.key_reasons) &&
    Array.isArray(item.caution_points) &&
    Array.isArray(item.explanation_trace) &&
    isObject(item.data_freshness)
  ));
}
