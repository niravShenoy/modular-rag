// ui/src/components/Providers.tsx   ← New file
"use client";

import { HeroUIProvider } from "@heroui/react";
import { ReactNode } from "react";

export default function Providers({ children }: { children: ReactNode }) {
  return <HeroUIProvider>{children}</HeroUIProvider>;
}