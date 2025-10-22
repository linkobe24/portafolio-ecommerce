"use client";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { LoginForm } from "../login-form";
import { RegisterForm } from "../register-form";
import { ReactNode, useState } from "react";

interface AuthDialogProps {
  children: ReactNode;
  defaultTab?: "login" | "register";
}

// AuthDialog - Modal de autenticación con tabs Login/Register

export function AuthDialog({
  children,
  defaultTab = "login",
}: AuthDialogProps) {
  const [open, setOpen] = useState(false);
  const [activeTab, setActiveTab] = useState(defaultTab);

  const handleSuccess = () => {
    setOpen(false);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="sm:mx-w-[425px]">
        <DialogHeader>
          <DialogTitle>
            {activeTab === "login" ? "Iniciar Sesión" : "Crear Cuenta"}
          </DialogTitle>
          <DialogDescription>
            {activeTab === "login"
              ? "Ingresa tus credenciales para continuar"
              : "Completa el formulario para crear tu cuenta"}
          </DialogDescription>
        </DialogHeader>

        <Tabs
          value={activeTab}
          onValueChange={(v) => setActiveTab(v as "login" | "register")}
        >
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="login">Login</TabsTrigger>
            <TabsTrigger value="register">Registro</TabsTrigger>
          </TabsList>

          <TabsContent value="login">
            <LoginForm onSuccess={handleSuccess} />
          </TabsContent>

          <TabsContent value="register">
            <RegisterForm onSuccess={handleSuccess} />
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
