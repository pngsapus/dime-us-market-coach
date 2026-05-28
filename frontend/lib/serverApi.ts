export const API_BASE = process.env.BACKEND_API_BASE_URL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api";
const DEFAULT_TIMEOUT_MS = 5000;

export async function backendFetch(path: string, init: RequestInit = {}, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await fetch(`${API_BASE}${path}`, {
      ...init,
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timeout);
  }
}

export function redirectWithMessage(baseUrl: string, path: string, params: Record<string, string>) {
  const url = new URL(path, baseUrl);
  Object.entries(params).forEach(([key, value]) => url.searchParams.set(key, value));
  return url;
}
