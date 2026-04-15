"use client";

import { Toaster } from "react-hot-toast";

/**
 * Global toast notification provider.
 * Wrapped into the root layout for app-wide error/success toasts.
 */
export function ToastProvider() {
  return (
    <Toaster
      position="top-right"
      toastOptions={{
        duration: 4000,
        style: {
          background: "rgba(30, 41, 59, 0.95)",
          color: "#f8fafc",
          border: "1px solid rgba(255, 255, 255, 0.08)",
          backdropFilter: "blur(12px)",
          fontSize: "14px",
          borderRadius: "12px",
          padding: "12px 16px",
        },
        success: {
          iconTheme: {
            primary: "#10b981",
            secondary: "#f8fafc",
          },
        },
        error: {
          iconTheme: {
            primary: "#ef4444",
            secondary: "#f8fafc",
          },
          duration: 5000,
        },
      }}
    />
  );
}
