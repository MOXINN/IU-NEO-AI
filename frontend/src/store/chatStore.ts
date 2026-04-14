import { create } from "zustand";

export type Role = "user" | "assistant";

export interface Message {
  id: string;
  role: Role;
  content: string;
  timestamp: number;
}

interface ChatState {
  messages: Message[];
  isStreaming: boolean;
  statusMessage: string | null;
  activeThreadId: string;
  addMessage: (message: Message) => void;
  updateLastMessage: (contentDelta: string) => void;
  setStreaming: (isStreaming: boolean) => void;
  setStatusMessage: (msg: string | null) => void;
  clearChat: () => void;
}

const generateId = () => Math.random().toString(36).substring(2, 9);

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isStreaming: false,
  statusMessage: null,
  activeThreadId: `thread_${generateId()}`,

  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),

  updateLastMessage: (contentDelta) =>
    set((state) => {
      if (state.messages.length === 0) return state;
      const newMessages = [...state.messages];
      const last = newMessages[newMessages.length - 1];
      if (last.role === "assistant") {
        newMessages[newMessages.length - 1] = {
          ...last,
          content: last.content + contentDelta,
        };
      }
      return { messages: newMessages };
    }),

  setStreaming: (isStreaming) => set({ isStreaming }),
  
  setStatusMessage: (statusMessage) => set({ statusMessage }),

  clearChat: () =>
    set({
      messages: [],
      activeThreadId: `thread_${generateId()}`,
      statusMessage: null,
    }),
}));
