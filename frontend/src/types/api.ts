export type Role = "super_admin" | "company_admin" | "manager" | "agent" | "analyst";
export interface CurrentUser { id: string; name: string; email: string; role: Role; organization_detail: { id: string; name: string; timezone: string } | null; }
export interface Paginated<T> { count: number; next: string | null; previous: string | null; results: T[]; }
export interface User { id: string; name: string; email: string; phone: string; role: Role; status: string; }
export interface Team { id: string; name: string; manager: string | null; manager_name: string | null; }
export interface CallEvent { id: string; event_type: string; timestamp: string; payload: Record<string, unknown>; }
export interface CallNote { id: string; author_name: string; text: string; created_at: string; }
export interface Call { id: string; direction: "inbound" | "outbound"; caller_number: string; receiver_number: string; contact_name: string | null; agent_name: string | null; team_name: string | null; tracked_number_value: string | null; status: string; started_at: string; answered_at: string | null; ended_at: string | null; ring_duration: number; talk_duration: number; total_duration: number; recording_url: string; source: string; outcome_name: string | null; follow_up_required: boolean; events: CallEvent[]; notes: CallNote[]; }
