"use client";
import { useEffect } from "react";import { useRouter } from "next/navigation";import { apiFetch } from "@/lib/api-client";
export default function Logout(){const router=useRouter();useEffect(()=>{apiFetch("/api/v1/auth/logout/",{method:"POST"}).finally(()=>router.replace("/login"))},[router]);return <div className="grid min-h-screen place-items-center text-sm text-muted-foreground">Signing out…</div>}
