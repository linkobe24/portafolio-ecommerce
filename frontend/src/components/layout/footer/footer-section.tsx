type FooterSectionProps = {
  title: string;
  children: React.ReactNode;
};

export function FooterSection({ title, children }: FooterSectionProps) {
  return (
    <div className="flex flex-col gap-4">
      <h4 className="text-sm font-semibold">{title}</h4>
      <nav className="flex flex-col gap-2">{children}</nav>
    </div>
  );
}
