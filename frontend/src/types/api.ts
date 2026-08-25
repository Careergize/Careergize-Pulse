export type Role = "super_admin" | "company_admin" | "manager" | "agent" | "analyst";
export interface CurrentUser { id: string; name: string; email: string; role: Role; organization_detail: { id: string; name: string; timezone: string } | null; }
export interface Paginated<T> { count: number; next: string | null; previous: string | null; results: T[]; }
export interface User { id: string; name: string; email: string; phone: string; role: Role; status: string; }
export interface Team { id: string; name: string; manager: string | null; manager_name: string | null; }
