"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { StockSearch } from "@/components/search";

export default function NavBar() {
  const router = useRouter();

  return (
    <header className="sticky top-0 z-40 w-full border-b border-border bg-background/95 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-7xl items-center gap-4 px-4">
        {/* Brand */}
        <Link href="/dashboard" className="shrink-0 font-bold text-lg tracking-tight">
          StockPulse
        </Link>

        {/* Search — center */}
        <div className="flex-1 max-w-md mx-auto">
          <StockSearch
            onSelect={(ticker) => router.push(`/stock/${ticker}`)}
            placeholder="Search stocks…"
          />
        </div>

        {/* Nav links */}
        <nav className="flex shrink-0 items-center gap-4 text-sm font-medium text-muted-foreground">
          <Link href="/dashboard" className="hover:text-foreground transition-colors">
            Dashboard
          </Link>
          <Link href="/portfolio" className="hover:text-foreground transition-colors">
            Portfolio
          </Link>
        </nav>
      </div>
    </header>
  );
}
