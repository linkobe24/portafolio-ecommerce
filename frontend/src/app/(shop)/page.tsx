import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function HomePage() {
  return (
    <div className="container py-12">
      {/* Hero Section */}
      <section className="flex flex-col items-center gap-4 text-center">
        <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
          Bienvenido a MemoryCard
        </h1>
        <p className="max-w-2xl text-lg text-muted-foreground">
          Tu tienda de videojuegos favorita. Encuentra los mejores títulos para
          PC, PlayStation, Xbox y Nintendo Switch.
        </p>
        <div className="flex gap-4">
          <Button size="lg" asChild>
            <Link href="/games">Ver Catálogo</Link>
          </Button>
          <Button size="lg" variant="outline" asChild>
            <Link href="/about">Sobre Nosotros</Link>
          </Button>
        </div>
      </section>

      {/* Features */}
      <section className="mt-24 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>🎮 Amplio Catálogo</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Miles de videojuegos para todas las plataformas
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>💳 Pago Seguro</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Transacciones 100% seguras y encriptadas
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>🚚 Entrega Digital</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Recibe tus juegos al instante por correo
            </p>
          </CardContent>
        </Card>
      </section>

      {/* Tech Stack Info */}
      <section className="mt-24">
        <Card>
          <CardHeader>
            <CardTitle>Stack Tecnológico</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <h4 className="mb-2 font-semibold">Frontend</h4>
                <ul className="list-inside list-disc text-sm text-muted-foreground">
                  <li>Next.js 15 (App Router)</li>
                  <li>TypeScript</li>
                  <li>Tailwind CSS 4</li>
                  <li>Shadcn/ui</li>
                  <li>TanStack Query v5</li>
                </ul>
              </div>
              <div>
                <h4 className="mb-2 font-semibold">Backend</h4>
                <ul className="list-inside list-disc text-sm text-muted-foreground">
                  <li>FastAPI (Python)</li>
                  <li>PostgreSQL</li>
                  <li>SQLAlchemy 2.0</li>
                  <li>JWT Authentication</li>
                  <li>RAWG API Integration</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
