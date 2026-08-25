"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { apiFetch } from "@/lib/api-client";
import type { Call } from "@/types/api";

const duration = (n: number) => `${Math.floor(n / 60)}m ${n % 60}s`;

export default function CallDetailPage() {
  const { id } = useParams<{id: string}>();
  const [call, setCall] = useState<Call | null>(null);
  const [note, setNote] = useState("");
  const [error, setError] = useState("");
  const load = () => apiFetch<Call>(`/api/v1/calls/${id}/`).then(setCall).catch((e: Error) => setError(e.message));
  useEffect(() => {
    void apiFetch<Call>(`/api/v1/calls/${id}/`).then(setCall).catch((e: Error) => setError(e.message));
  }, [id]);
  const addNote = async () => { if (!note.trim()) return; await apiFetch("/api/v1/call-notes/", {method: "POST", body: JSON.stringify({call: id, text: note})}); setNote(""); load(); };
  if (error) return <p className="text-red-600">{error}</p>;
  if (!call) return <p className="text-slate-500">Loading call…</p>;
  const rows = [["Caller", call.caller_number], ["Contact", call.contact_name], ["Direction", call.direction], ["Agent", call.agent_name], ["Team", call.team_name], ["Started", new Date(call.started_at).toLocaleString()], ["Answered", call.answered_at && new Date(call.answered_at).toLocaleString()], ["Ended", call.ended_at && new Date(call.ended_at).toLocaleString()], ["Ring duration", duration(call.ring_duration)], ["Talk duration", duration(call.talk_duration)], ["Source", call.source], ["Status", call.status], ["Outcome", call.outcome_name]];
  return <><Link href="/calls" className="mb-4 inline-block text-sm text-blue-700">← Back to calls</Link><h1 className="text-2xl font-semibold">Call from {call.caller_number}</h1><p className="mb-6 mt-1 text-slate-500">{new Date(call.started_at).toLocaleString()}</p><div className="grid gap-6 xl:grid-cols-3"><section className="rounded-xl border bg-white p-5 xl:col-span-2"><h2 className="mb-4 font-semibold">Call details</h2><dl className="grid gap-x-8 gap-y-4 sm:grid-cols-2">{rows.map(([label,value]) => <div key={label}><dt className="text-xs uppercase text-slate-500">{label}</dt><dd className="mt-1 capitalize">{value || "—"}</dd></div>)}</dl>{call.recording_url && <div className="mt-6 border-t pt-5"><h3 className="mb-3 font-medium">Recording</h3><audio controls className="w-full" src={call.recording_url}>Call recording</audio></div>}</section><aside className="space-y-6"><section className="rounded-xl border bg-white p-5"><h2 className="mb-4 font-semibold">Notes</h2><textarea value={note} onChange={e => setNote(e.target.value)} placeholder="Add a call note" className="min-h-24 w-full rounded-lg border p-3 text-sm"/><button onClick={addNote} className="mt-2 rounded-lg bg-blue-700 px-4 py-2 text-sm font-medium text-white">Add note</button><div className="mt-4 space-y-3">{call.notes.map(x => <article key={x.id} className="rounded-lg bg-slate-50 p-3 text-sm"><p>{x.text}</p><p className="mt-2 text-xs text-slate-500">{x.author_name} · {new Date(x.created_at).toLocaleString()}</p></article>)}</div></section><section className="rounded-xl border bg-white p-5"><h2 className="mb-4 font-semibold">Related events</h2><ol className="space-y-3">{call.events.map(x => <li key={x.id} className="border-l-2 border-blue-200 pl-3"><p className="text-sm font-medium capitalize">{x.event_type.replaceAll("_", " ")}</p><time className="text-xs text-slate-500">{new Date(x.timestamp).toLocaleString()}</time></li>)}</ol></section></aside></div></>;
}
