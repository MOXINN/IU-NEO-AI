import React, { useRef, useEffect } from "react";
import { useChatStore } from "@/store/chatStore";
import { MessageBubble } from "./MessageBubble";
import { Bot } from "lucide-react";

export function ChatContainer() {
  const messages = useChatStore((state) => state.messages);
  const statusMessage = useChatStore((state) => state.statusMessage);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll on new message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, statusMessage]);

  return (
    <div className="flex-1 overflow-y-auto px-4 md:px-10 py-6 scroll-smooth scrollbar-thin scrollbar-thumb-slate-700/50 scrollbar-track-transparent">
      {messages.length === 0 ? (
        <div className="h-full flex flex-col items-center justify-center opacity-80 animate-in fade-in duration-1000">
          <div className="w-20 h-20 bg-indigo-500/10 rounded-full flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(99,102,241,0.2)]">
            <Bot size={36} className="text-indigo-400" />
          </div>
          <h2 className="text-2xl font-light text-slate-200 mb-2">Integral University AI</h2>
          <p className="text-slate-400 text-sm max-w-md text-center">
            Your enterprise agentic assistant. Ask me about courses, prerequisites, or campus facilities.
          </p>
        </div>
      ) : (
        <div className="max-w-4xl mx-auto w-full">
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
          
          {statusMessage && (
            <div className="flex justify-start mb-6">
              <div className="text-xs text-indigo-400 font-mono tracking-wide flex items-center bg-indigo-900/20 px-3 py-1.5 rounded-full border border-indigo-500/20">
                <span className="inline-block w-2 h-2 rounded-full bg-indigo-500 animate-pulse mr-2"></span>
                {statusMessage}
              </div>
            </div>
          )}
          
          <div ref={bottomRef} className="h-4" />
        </div>
      )}
    </div>
  );
}
