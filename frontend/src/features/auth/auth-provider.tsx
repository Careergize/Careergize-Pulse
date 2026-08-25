"use client";
import { createContext, useContext, useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api-client";
import type { CurrentUser } from "@/types/api";

const AuthContext = createContext<{ user: CurrentUser | null; loading: boolean; signOut: () => Promise<void> }>({ user: null, loading: true, signOut: async () => {} });
export function useAuth() { return useContext(AuthContext); }

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter(); const pathname = usePathname();
  useEffect(() => { apiFetch<CurrentUser>("/api/v1/auth/me/").then(setUser).catch(() => router.replace(`/login?next=${encodeURIComponent(pathname)}`)).finally(() => setLoading(false)); }, [pathname, router]);
  async function signOut() { await apiFetch("/api/v1/auth/logout/", { method: "POST" }); setUser(null); router.replace("/login"); }
  if (loading) return <div className="grid min-h-screen place-items-center"><div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" aria-label="Loading" /></div>;
  if (!user) return null;
  return <AuthContext.Provider value={{ user, loading, signOut }}>{children}</AuthContext.Provider>;
}
