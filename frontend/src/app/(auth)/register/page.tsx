import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Create Account",
  description: "Create a free StockPulse account to start tracking your portfolio.",
};

/**
 * Register page — stub.
 * Full implementation (React Hook Form + Zod validation + API call) ships in Sprint 1.
 */
export default function RegisterPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4">
      <div className="w-full max-w-sm space-y-6">
        <div className="space-y-2 text-center">
          <h1 className="text-3xl font-bold tracking-tight">Create account</h1>
          <p className="text-sm text-muted-foreground">
            Get started with StockPulse — free forever.
          </p>
        </div>

        {/* Form placeholder — replaced by react-hook-form implementation in Sprint 1 */}
        <div
          className="rounded-lg border border-border bg-card p-6 shadow-sm space-y-4"
          aria-label="Create account form"
        >
          <div className="space-y-2">
            <label htmlFor="display_name" className="text-sm font-medium leading-none">
              Display name
            </label>
            <input
              id="display_name"
              type="text"
              autoComplete="name"
              placeholder="Jane Smith"
              className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
              disabled
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="email" className="text-sm font-medium leading-none">
              Email
            </label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              placeholder="you@example.com"
              className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
              disabled
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="password" className="text-sm font-medium leading-none">
              Password
            </label>
            <input
              id="password"
              type="password"
              autoComplete="new-password"
              placeholder="••••••••"
              className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
              disabled
            />
          </div>

          <button
            type="submit"
            disabled
            className="inline-flex h-9 w-full items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors disabled:pointer-events-none disabled:opacity-50"
          >
            Create account
          </button>

          <p className="text-center text-xs text-muted-foreground">
            Coming soon — full auth form implementation.
          </p>
        </div>

        <p className="text-center text-sm text-muted-foreground">
          Already have an account?{" "}
          <Link
            href="/login"
            className="font-medium text-primary underline-offset-4 hover:underline focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring rounded-sm"
          >
            Sign in
          </Link>
        </p>
      </div>
    </main>
  );
}
