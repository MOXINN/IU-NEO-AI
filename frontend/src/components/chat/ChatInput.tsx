"use client";

import React, { useState, useRef, KeyboardEvent } from "react";
import { Send, Settings, Square, Trash2 } from "lucide-react";
import { useChatStore } from "@/store/chatStore";
import { streamChat } from "@/lib/api";
import { generateId } from "@/lib/utils";

export function ChatInput() {
  const [input, setInput] = useState("");
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const { addMessage, isStreaming, activeThreadId, setStreaming, clearChat, messages } =
    useChatStore();

  const handleSend = async () => {
    if (!input.trim() || isStreaming) return;

    const userMessage = input.trim();
    setInput("");

    // Push local message immediately
    addMessage({
      id: generateId(),
      role: "user",
      content: userMessage,
      timestamp: Date.now(),
    });

    abortControllerRef.current = new AbortController();
    await streamChat(userMessage, activeThreadId, abortControllerRef.current);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setStreaming(false);
    }
  };

  return (
    <div className="p-4 mx-auto max-w-4xl w-full">
      <div className="glass-panel relative flex items-end p-2 sm:p-3 rounded-3xl group transition-all duration-300 focus-within:ring-2 focus-within:ring-indigo-500/50">
        {/* Clear Chat Button */}
        <button
          onClick={clearChat}
          disabled={messages.length === 0 || isStreaming}
          className="p-2 sm:p-3 text-slate-400 hover:text-rose-400 transition-colors disabled:opacity-30 disabled:hover:text-slate-400"
          title="Clear chat"
        >
          <Trash2 size={18} />
        </button>

        <textarea
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything..."
          className="flex-1 max-h-[200px] min-h-[44px] sm:min-h-[52px] bg-transparent text-slate-100 placeholder-slate-500 border-0 focus:ring-0 resize-none px-2 sm:px-4 py-3 sm:py-3.5 outline-none text-[15px]"
          rows={1}
        />

        {isStreaming ? (
          <button
            onClick={handleStop}
            className="p-3 sm:p-3.5 mr-1 bg-rose-500/20 text-rose-400 hover:bg-rose-500/40 rounded-2xl transition-colors"
          >
            <Square size={18} fill="currentColor" />
          </button>
        ) : (
          <button
            onClick={handleSend}
            disabled={!input.trim()}
            className="p-3 sm:p-3.5 mr-1 bg-indigo-600 text-white rounded-2xl hover:bg-indigo-500 disabled:opacity-50 disabled:hover:bg-indigo-600 transition-all active:scale-95 disabled:active:scale-100"
          >
            <Send size={18} className="translate-x-[1px] translate-y-[1px]" />
          </button>
        )}
      </div>
      <div className="text-center mt-3 text-[11px] text-slate-500">
        AI responses may not be fully accurate. Please verify administrative
        details.
      </div>
    </div>
  );
}
