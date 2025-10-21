import Link from "next/link";
import { Separator } from "@/components/ui/separator";
import { FooterSection } from "./footer-section";
import { FooterLink } from "./footer-links";
import { SocialLinks } from "./social-links";

const SHOP_LINKS = [
  { href: "/games", label: "Catálogo" },
  { href: "/games?genre=action", label: "Acción" },
  { href: "/games?genre=rpg", label: "RPG" },
  { href: "/games?genre=adventure", label: "Aventura" },
];

const SUPPORT_LINKS = [
  { href: "/help", label: "Centro de ayuda" },
  { href: "/terms", label: "Términos y condiciones" },
  { href: "/privacy", label: "Política de privacidad" },
];

export function Footer() {
  return (
    <footer className="border-t bg-muted/50">
      <div className="container py-12 md:py-16">
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
          {/* Brand */}
          <div className="flex flex-col gap-4">
            <h3 className="text-lg font-bold">MemoryCard</h3>
            <p className="text-sm text-muted-foreground">
              Tu tienda de videojuegos favorita. Encuentra los mejores títulos
              al mejor precio.
            </p>
          </div>

          {/* Shop Links */}
          <FooterSection title="Tienda">
            {SHOP_LINKS.map((link) => (
              <FooterLink key={link.href} href={link.href}>
                {link.label}
              </FooterLink>
            ))}
          </FooterSection>

          {/* Support Links */}
          <FooterSection title="Soporte">
            {SUPPORT_LINKS.map((link) => (
              <FooterLink key={link.href} href={link.href}>
                {link.label}
              </FooterLink>
            ))}
          </FooterSection>

          {/* Social */}
          <div className="flex flex-col gap-4">
            <h4 className="text-sm font-semibold">Síguenos</h4>
            <SocialLinks />
          </div>
        </div>

        <Separator className="my-8" />

        <div className="flex flex-col items-center justify-between gap-4 text-sm text-muted-foreground md:flex-row">
          <p>© 2025 MemoryCard. Todos los derechos reservados.</p>
          <p>
            Construido con{" "}
            <Link
              href="https://nextjs.org"
              target="_blank"
              rel="noopener noreferrer"
              className="font-medium hover:text-foreground"
            >
              Next.js
            </Link>{" "}
            y{" "}
            <Link
              href="https://ui.shadcn.com"
              target="_blank"
              rel="noopener noreferrer"
              className="font-medium hover:text-foreground"
            >
              Shadcn/ui
            </Link>
          </p>
        </div>
      </div>
    </footer>
  );
}
