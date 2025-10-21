import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./global.css";
import { ThemeProvider } from "@/components/providers/theme-provider";
import { QueryProvider } from "@/components/providers/query-providers";
import { ReactNode } from "react";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "MemoryCard - La tienda de videojuegos",
    template: "%s | MemoryCard",
  },
  description: "Encuentra los mejores videjuegos al mejor precio",
  keywords: [
    "videojuegos",
    "gaming",
    "e-commerce",
    "playstation",
    "xbox",
    "pc",
  ],
  authors: [{ name: "Manuel Beltran" }],
  creator: "Manuel Beltran",
  openGraph: {
    type: "website",
    locale: "es_ES",
    url: process.env.NEXT_PUBLIC_APP_URL,
    title: "MemoryCard - La tienda de videojuegos",
    description: "Encuentra los mejores videojuegos al mejor precio",
    siteName: "MemoryCard",
  },
  twitter: {
    card: "summary_large_image",
    title: "MemoryCard - La tienda de videojuegos",
    description: "Encuentra los mejores videojuegos al mejor precio",
  },
};

type RootLayoutProps = {
  children: ReactNode;
};

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          <QueryProvider>{children}</QueryProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
