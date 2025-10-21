import Link from "next/link";
import { NavActions } from "./nav-actions";
import { MobileMenu } from "./mobile-menu";
import { NavLink } from "./nav-link";

const NAV_LINKS = [
  { href: "/games", label: "Catálogo" },
  { href: "/games?genre=action", label: "Acción" },
  { href: "/games?genre=rpg", label: "RPG" },
  { href: "/games?genre=adventure", label: "Aventura" },
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-backdrop-filter:bg-background/60">
      <div className="container flex h-16 items-center">
        {/* Logo */}
        <Link href="/" className="mr-6 flex items-center space-x-2">
          <span className="text-xl font-bold">MemoryCard</span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex md:flex-1 md:items-center md:gap-6">
          {NAV_LINKS.map((link) => (
            <NavLink key={link.href} href={link.href}>
              {link.label}
            </NavLink>
          ))}
        </nav>

        {/* Actions */}
        <div className="flex flex-1 items-center justify-end gap-2">
          <NavActions />
          <MobileMenu links={NAV_LINKS} />
        </div>
      </div>
    </header>
  );
}
