import { AppShell } from "@/components/app-shell"; import { AuthProvider } from "@/features/auth/auth-provider";
export default function ProtectedLayout({children}:{children:React.ReactNode}) { return <AuthProvider><AppShell>{children}</AppShell></AuthProvider>; }
