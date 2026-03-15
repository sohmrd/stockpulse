import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Settings",
  description: "Manage your StockPulse account settings, preferences, and notifications.",
};

/**
 * Settings page — stub.
 *
 * Sprint 5 deliverables:
 * - Profile settings (display name, email)
 * - Notification preferences
 * - Connected accounts (OAuth)
 * - Danger zone (delete account)
 */
export default function SettingsPage() {
  return (
    <main className="flex flex-1 flex-col gap-6 p-4 md:p-6 lg:p-8">
      <div className="space-y-1">
        <h1 className="text-2xl font-bold tracking-tight">Settings</h1>
        <p className="text-sm text-muted-foreground">
          Manage your account preferences.
        </p>
      </div>

      <div className="space-y-4">
        {/* Profile section placeholder */}
        <section
          aria-labelledby="profile-heading"
          className="rounded-lg border border-border bg-card p-4 shadow-sm"
        >
          <h2 id="profile-heading" className="text-base font-semibold mb-4">
            Profile
          </h2>
          <div className="space-y-3">
            <div className="space-y-1">
              <p className="text-sm font-medium text-muted-foreground">Display name</p>
              <div className="h-5 w-32 rounded bg-muted animate-pulse" aria-hidden="true" />
            </div>
            <div className="space-y-1">
              <p className="text-sm font-medium text-muted-foreground">Email</p>
              <div className="h-5 w-48 rounded bg-muted animate-pulse" aria-hidden="true" />
            </div>
          </div>
        </section>

        {/* Notifications section placeholder */}
        <section
          aria-labelledby="notifications-heading"
          className="rounded-lg border border-border bg-card p-4 shadow-sm"
        >
          <h2 id="notifications-heading" className="text-base font-semibold mb-2">
            Notifications
          </h2>
          <p className="text-sm text-muted-foreground">
            Notification preferences coming in Sprint 5.
          </p>
        </section>
      </div>
    </main>
  );
}
