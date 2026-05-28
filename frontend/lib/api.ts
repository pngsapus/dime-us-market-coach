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
        message: "ไม่สามารถเชื่อมต่อข้อมูลจำลองจาก backend ได้",
        retryPath: path,
      };
    }
    return { ok: true, data: (await response.json()) as T };
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
  return getJson<DiscoveryRun>("/discovery/latest");
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
