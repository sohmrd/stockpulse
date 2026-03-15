import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Sign In",
  description: "Sign in to your StockPulse account to track your portfolio and get AI insights.",
};

/**
 * Login page — stub.
 * Full implementation (React Hook Form + Zod validation + API call) ships in Sprint 1.
 */
export default function LoginPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4">
      <div className="w-full max-w-sm space-y-6">
        <div className="space-y-2 text-center">
          <h1 className="text-3xl font-bold tracking-tight">Sign in</h1>
          <p className="text-sm text-muted-foreground">
            Enter your email and password to access your account.
          </p>
        </div>

        {/* Form placeholder — replaced by react-hook-form implementation in Sprint 1 */}
        <div
          className="rounded-lg border border-border bg-card p-6 shadow-sm space-y-4"
          aria-label="Sign in form"
        >
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
              aria-describedby="email-hint"
            />
            <p id="email-hint" className="sr-only">
              Enter the email address associated with your StockPulse account.
            </p>
          </div>

          <div className="space-y-2">
            <label htmlFor="password" className="text-sm font-medium leading-none">
              Password
            </label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
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
            Sign in
          </button>

          <p className="text-center text-xs text-muted-foreground">
            Coming soon — full auth form implementation.
          </p>
        </div>

        <p className="text-center text-sm text-muted-foreground">
          Don&apos;t have an account?{" "}
          <Link
            href="/register"
            className="font-medium text-primary underline-offset-4 hover:underline focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring rounded-sm"
          >
            Create one
          </Link>
        </p>
      </div>
    </main>
  );
}
