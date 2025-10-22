import { AuthGuard } from "@/components/providers/auth-guard";

export default function ProfilePage() {
  return (
    <AuthGuard>
      <div className="container py-12">
        <h1 className="text-3xl font-bold">Mi Perfil</h1>
        {/* Contenido de perfil */}
      </div>
    </AuthGuard>
  );
}
