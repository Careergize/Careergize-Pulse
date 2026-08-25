"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Search } from "lucide-react";

import { PageHeader } from "@/components/page-state";
import { apiFetch } from "@/lib/api-client";
import type { Call, Paginated } from "@/types/api";

const seconds = (value: number) => `${Math.floor(value / 60)}:${String(value % 60).padStart(2, "0")}`;

export default function CallsPage() {
  const [data, setData] = useState<Paginated<Call> | null>(null);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  useEffect(() => {
    const params = new URLSearchParams();
    if (query) params.set("search", query);
    if (status) params.set("status", status);
    const timer = setTimeout(() => apiFetch<Paginated<Call>>(`/api/v1/calls/?${params}`).then(setData).catch((e: Error) => setError(e.message)), 200);
    return () => clearTimeout(timer);
  }, [query, status]);
  return <>
    <PageHeader title="Calls" description="Monitor every inbound and outbound conversation." />
    <div className="mb-4 flex flex-wrap gap-3 rounded-xl border bg-white p-4">
      <label className="relative min-w-64 flex-1"><Search className="absolute left-3 top-2.5 text-slate-400" size={18}/><input aria-label="Search calls" value={query} onChange={e => setQuery(e.target.value)} placeholder="Phone number or contact" className="w-full rounded-lg border py-2 pl-10 pr-3 text-sm"/></label>
      <select aria-label="Status" value={status} onChange={e => setStatus(e.target.value)} className="rounded-lg border px-3 text-sm"><option value="">All statuses</option>{["ringing","answered","missed","busy","failed","completed"].map(x => <option key={x}>{x}</option>)}</select>
    </div>
    {error ? <p className="text-red-600">{error}</p> : <div className="overflow-x-auto rounded-xl border bg-white"><table className="w-full text-left text-sm"><thead className="border-b bg-slate-50 text-xs uppercase text-slate-500"><tr>{["Date/Time","Caller","Contact","Direction","Agent","Source","Duration","Status","Outcome","Follow-up"].map(x => <th key={x} className="px-4 py-3 font-medium">{x}</th>)}</tr></thead><tbody>{data?.results.map(call => <tr key={call.id} className="border-b last:border-0 hover:bg-slate-50"><td className="whitespace-nowrap px-4 py-3"><Link className="font-medium text-blue-700" href={`/calls/${call.id}`}>{new Date(call.started_at).toLocaleString()}</Link></td><td className="px-4 py-3">{call.caller_number}</td><td className="px-4 py-3">{call.contact_name ?? "—"}</td><td className="px-4 py-3 capitalize">{call.direction}</td><td className="px-4 py-3">{call.agent_name ?? "—"}</td><td className="px-4 py-3">{call.source || "—"}</td><td className="px-4 py-3 tabular-nums">{seconds(call.total_duration)}</td><td className="px-4 py-3 capitalize">{call.status}</td><td className="px-4 py-3">{call.outcome_name ?? "—"}</td><td className="px-4 py-3">{call.follow_up_required ? "Yes" : "No"}</td></tr>)}</tbody></table>{!data && <p className="p-8 text-center text-slate-500">Loading calls…</p>}{data?.results.length === 0 && <p className="p-8 text-center text-slate-500">No matching calls.</p>}<div className="border-t px-4 py-3 text-sm text-slate-500">{data?.count ?? 0} calls</div></div>}
  </>;
}
