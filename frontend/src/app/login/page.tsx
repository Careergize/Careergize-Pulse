"use client";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api-client";
import type { CurrentUser } from "@/types/api";

export default function LoginPage() {
  const router = useRouter();
  const [error, setError] = useState(""); const [loading, setLoading] = useState(false);
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(""); setLoading(true);
    const data = new FormData(event.currentTarget);
    try { await apiFetch<CurrentUser>("/api/v1/auth/login/", { method: "POST", body: JSON.stringify({ email: data.get("email"), password: data.get("password") }) }); router.replace(new URLSearchParams(window.location.search).get("next") || "/dashboard"); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Unable to sign in"); setLoading(false); }
  }
  return <main className="grid min-h-screen bg-slate-950 lg:grid-cols-2">
    <section className="hidden flex-col justify-between p-12 text-white lg:flex"><div className="text-xl font-semibold">Careergize Pulse</div><div><p className="mb-3 text-sm font-semibold uppercase tracking-[.24em] text-blue-300">Call intelligence</p><h1 className="max-w-lg text-5xl font-semibold leading-tight">Turn every conversation into the next best action.</h1></div><p className="text-sm text-slate-400">Secure workspace access</p></section>
    <section className="grid place-items-center rounded-l-[2rem] bg-background px-6"><form onSubmit={submit} className="w-full max-w-sm space-y-6"><div><h2 className="text-3xl font-semibold">Welcome back</h2><p className="mt-2 text-muted-foreground">Sign in with your company email.</p></div>{error && <div role="alert" className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}<label className="block text-sm font-medium">Email<input name="email" type="email" required autoComplete="email" className="mt-2 w-full rounded-lg border bg-white px-3 py-2.5 outline-none focus:ring-2 focus:ring-primary" /></label><label className="block text-sm font-medium">Password<input name="password" type="password" required autoComplete="current-password" className="mt-2 w-full rounded-lg border bg-white px-3 py-2.5 outline-none focus:ring-2 focus:ring-primary" /></label><button disabled={loading} className="w-full rounded-lg bg-primary px-4 py-2.5 font-medium text-white disabled:opacity-60">{loading ? "Signing in…" : "Sign in"}</button></form></section>
  </main>;
}
