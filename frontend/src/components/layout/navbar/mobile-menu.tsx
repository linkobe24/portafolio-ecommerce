"use client";

import Link from "next/link";
import { Menu } from "lucide-react";
import { Button } from "../../ui/button";
import { Sheet, SheetContent, SheetTrigger } from "../../ui/sheet";

type MobileMenuProps = {
  links: Array<{ href: string; label: string }>;
};

export function MobileMenu({ links }: MobileMenuProps) {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden">
          <span className="contents">
            <Menu className="h-5 w-5" />
            <span className="sr-only">Menu</span>
          </span>
        </Button>
      </SheetTrigger>
      <SheetContent>
        <nav className="flex flex-col gap-4">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-lg font-medium"
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </SheetContent>
    </Sheet>
  );
}
