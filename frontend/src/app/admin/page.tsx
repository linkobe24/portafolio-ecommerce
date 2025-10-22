import { AuthGuard } from "@/components/providers/auth-guard";

export default function AdminPage() {
  return (
    <AuthGuard requireAdmin>
      <div className="container py-12">
        <h1 className="text-3xl font-bold">Panel Admin</h1>
        {/* Contenido admin */}
      </div>
    </AuthGuard>
  );
}
