import Link from "next/link";

type FooterLinkProps = {
  href: string;
  children: React.ReactNode;
  external?: boolean;
};

export function FooterLink({
  href,
  children,
  external = false,
}: FooterLinkProps) {
  const externalProps = external
    ? { target: "_blank", rel: "noopener noreferrer" }
    : {};

  return (
    <Link
      href={href}
      className="text-sm text-muted-foreground hover:text-foreground"
      {...externalProps}
    >
      {children}
    </Link>
  );
}
