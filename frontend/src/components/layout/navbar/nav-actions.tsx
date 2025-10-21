"use client";

import Link from "next/link";
import { ShoppingCart, User } from "lucide-react";
import { Button } from "../../ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@radix-ui/react-dropdown-menu";
import { ThemeToggle } from "./theme-toggle";

export function NavActions() {
  return (
    <div className="flex items-center gap-2">
      <ThemeToggle />

      <Button variant="ghost" size="icon" asChild>
        <Link href="/cart">
          <span className="contents">
            <ShoppingCart className="h-5 w-5" />
            <span className="sr-only">Carrito</span>
          </span>
        </Link>
      </Button>

      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" size="icon">
            <span className="contents">
              <User className="h-5 w-5" />
              <span className="sr-only">Menú de usuario</span>
            </span>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuItem asChild>
            <Link href="/profile">Mi Perfil</Link>
          </DropdownMenuItem>
          <DropdownMenuItem asChild>
            <Link href="/orders">Mis Órdenes</Link>
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem asChild>
            <Link href="/login">Iniciar Sesión</Link>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}
