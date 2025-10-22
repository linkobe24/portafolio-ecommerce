import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "react";

type FormMessageProps = HTMLAttributes<HTMLParagraphElement>;

export function FormMessage({
  className,
  children,
  ...props
}: FormMessageProps) {
  return (
    <p
      className={cn("text-sm font-medium text-destructive", className)}
      role="alert"
      {...props}
    >
      {children}
    </p>
  );
}
