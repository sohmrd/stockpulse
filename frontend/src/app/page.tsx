import { redirect } from "next/navigation";

/**
 * Root route — redirects authenticated users to the dashboard,
 * unauthenticated users to the login page.
 *
 * Auth state is checked client-side via the auth provider;
 * this server component provides an immediate redirect for
 * the most common case (logged-in returning user going to "/").
 */
export default function RootPage() {
  // The middleware (to be added in Sprint 2) will handle the redirect
  // based on session state. For now we redirect to login as the default.
  redirect("/login");
}
