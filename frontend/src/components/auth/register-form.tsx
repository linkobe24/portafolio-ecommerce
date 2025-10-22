"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  registerSchema,
  type RegisterFormData,
} from "@/lib/validations/auth.schemas";
import { FormField } from "@/components/forms/form-field";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/use-auth";
import { useState } from "react";
import { AlertCircle, Loader2 } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";

type RegisterFormProps = {
  onSuccess?: () => void;
};

export function RegisterForm({ onSuccess }: RegisterFormProps) {
  const { register: registerUser, error, clearError } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    setIsSubmitting(true);
    clearError();

    try {
      // extraer confirmPassword antes de enviar al backend
      const { confirmPassword, ...registerData } = data;
      await registerUser(registerData);
      onSuccess?.();
    } catch (err) {
    } finally {
      setIsSubmitting(false);
    }
  };
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <FormField
        label="Nombre completo"
        type="text"
        placeholder="Juan Pérez"
        error={errors.full_name}
        required
        {...register("full_name")}
      />

      <FormField
        label="Email"
        type="email"
        placeholder="tu@email.com"
        error={errors.email}
        required
        {...register("email")}
      />

      <FormField
        label="Contraseña"
        type="password"
        placeholder="••••••••"
        error={errors.password}
        required
        {...register("password")}
      />

      <FormField
        label="Confirmar contraseña"
        type="password"
        placeholder="••••••••"
        error={errors.confirmPassword}
        required
        {...register("confirmPassword")}
      />

      <Button type="submit" className="w-full" disabled={isSubmitting}>
        {isSubmitting ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Creando cuenta...
          </>
        ) : (
          "Crear Cuenta"
        )}
      </Button>
    </form>
  );
}
