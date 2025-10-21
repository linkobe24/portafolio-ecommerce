import Link from "next/link";
import { Github, Twitter, Linkedin, LucideIcon } from "lucide-react";

interface SocialLink {
  href: string;
  icon: LucideIcon;
  label: string;
}

const SOCIAL_LINKS: SocialLink[] = [
  { href: "https://github.com", icon: Github, label: "GitHub" },
  { href: "https://twitter.com", icon: Twitter, label: "Twitter" },
  { href: "https://linkedin.com", icon: Linkedin, label: "LinkedIn" },
];

export function SocialLinks() {
  return (
    <div className="flex gap-4">
      {SOCIAL_LINKS.map((social) => {
        const Icon = social.icon;
        return (
          <Link
            key={social.label}
            href={social.href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-muted-foreground hover:text-foreground"
          >
            <Icon className="h-5 w-5" />
            <span className="sr-only">{social.label}</span>
          </Link>
        );
      })}
    </div>
  );
}
