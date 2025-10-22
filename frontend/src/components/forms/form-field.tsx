"use client";

import { Label } from "../ui/label";
import { Input } from "../ui/input";
import { FormMessage } from "./form-message";
import type { InputHTMLAttributes } from "react";
import type { FieldError } from "react-hook-form";

interface FormFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: FieldError;
  required?: boolean;
}

export function FormField({
  label,
  error,
  required,
  id,
  ...inputProps
}: FormFieldProps) {
  const fieldId = id || inputProps.name;

  return (
    <div className="space-y-2">
      <Label htmlFor={fieldId}>
        {label}
        {required && <span className="text-destructive ml-1">*</span>}
      </Label>
      <Input
        id={fieldId}
        aria-invalid={error ? "true" : "false"}
        aria-describedby={error ? `${fieldId}-error` : undefined}
        className={error ? "border-destructive" : ""}
        {...inputProps}
      />
      {error && (
        <FormMessage id={`${fieldId}-error`}>{error.message}</FormMessage>
      )}
    </div>
  );
}
