import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: {
    default: "StockPulse — AI-Powered Stock Tracking",
    template: "%s | StockPulse",
  },
  description:
    "Track your stock portfolio, monitor real-time market data, and receive AI-powered trend analysis and investment insights.",
  keywords: ["stocks", "portfolio tracker", "market data", "AI insights", "investment"],
  authors: [{ name: "StockPulse" }],
  openGraph: {
    type: "website",
    locale: "en_US",
    title: "StockPulse — AI-Powered Stock Tracking",
    description:
      "Track your stock portfolio, monitor real-time market data, and receive AI-powered insights.",
    siteName: "StockPulse",
  },
};

interface RootLayoutProps {
  children: React.ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en" className={inter.variable} suppressHydrationWarning>
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
