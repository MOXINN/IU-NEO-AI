import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ToastProvider } from "@/components/providers/ToastProvider";
import { ErrorBoundary } from "@/components/ui/ErrorBoundary";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "IU NWEO | Enterprise AI",
  description: "Next-gen university companion for Integral University",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased text-iu-text-main`}
      >
        <div className="relative min-h-screen overflow-hidden">
          {/* Subtle animated background elements */}
          <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-indigo-900/20 via-transparent to-transparent opacity-60"></div>

          <main className="relative z-0 h-screen flex flex-col">
            <ErrorBoundary>
              {children}
            </ErrorBoundary>
          </main>
        </div>
        <ToastProvider />
      </body>
    </html>
  );
}
