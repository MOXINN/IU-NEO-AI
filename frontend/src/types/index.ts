/**
 * IU NWEO AI — Shared TypeScript Types
 *
 * Central type definitions used across components, store, and API layer.
 */

export type Role = "user" | "assistant";

export interface Message {
  id: string;
  role: Role;
  content: string;
  timestamp: number;
}

export type SSEEventType = "status" | "message" | "done" | "error";

export interface APIErrorResponse {
  error: boolean;
  error_code: string;
  detail: string;
}
