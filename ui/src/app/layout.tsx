// ui/src/app/layout.tsx   ← Now a pure Server Component
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Providers from "@/components/Providers";   // ← Client wrapper

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Agentic RAG",
  description: "UI for your RAG project",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}