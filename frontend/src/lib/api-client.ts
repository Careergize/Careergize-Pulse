import { publicEnv } from "@/lib/env";

export class ApiError extends Error {
  constructor(public status: number, message: string) { super(message); }
}

function cookie(name: string) {
  if (typeof document === "undefined") return undefined;
  return document.cookie.split("; ").find((item) => item.startsWith(`${name}=`))?.split("=")[1];
}

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const method = init?.method?.toUpperCase() ?? "GET";
  if (!["GET", "HEAD", "OPTIONS"].includes(method) && !cookie("csrftoken")) {
    await fetch(`${publicEnv.NEXT_PUBLIC_API_URL}/api/v1/auth/csrf/`, { credentials: "include" });
  }
  const response = await fetch(`${publicEnv.NEXT_PUBLIC_API_URL}${path}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json", ...(cookie("csrftoken") ? { "X-CSRFToken": decodeURIComponent(cookie("csrftoken")!) } : {}), ...init?.headers },
    ...init,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null) as { error?: { message?: string } } | null;
    throw new ApiError(response.status, body?.error?.message ?? `Request failed (${response.status})`);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}
