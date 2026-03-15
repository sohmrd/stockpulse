import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Strict mode helps catch potential issues early
  reactStrictMode: true,

  // Image domains for next/image (expand as needed)
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**.amazonaws.com",
      },
    ],
  },

  // Expose only NEXT_PUBLIC_ vars to the browser — secrets stay server-side
  env: {
    NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000",
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
  },
};

export default nextConfig;
