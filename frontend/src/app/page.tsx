"use client";

import { ChatContainer } from "@/components/chat/ChatContainer";
import { ChatInput } from "@/components/chat/ChatInput";

export default function Home() {
  return (
    <div className="flex flex-col h-full w-full max-w-[100vw] overflow-hidden">
      {/* Top Header */}
      <header className="h-16 flex items-center justify-between px-6 border-b border-white/5 bg-slate-900/40 backdrop-blur-md z-10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <span className="font-bold text-white text-sm tracking-tighter">IU</span>
          </div>
          <h1 className="font-medium text-slate-200 tracking-wide text-sm hidden sm:block">
            Agentic Core
          </h1>
        </div>
        <div className="flex items-center gap-4 text-xs font-semibold uppercase tracking-wider text-slate-400">
          <div className="flex items-center gap-1.5">
            <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]"></div>
            System Online
          </div>
        </div>
      </header>

      {/* Main Chat Area */}
      <ChatContainer />
      
      {/* Input Area */}
      <div className="pb-2 pt-1 bg-gradient-to-t from-slate-900 via-slate-900/80 to-transparent">
        <ChatInput />
      </div>
    </div>
  );
}
