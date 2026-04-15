import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { cn } from "@/lib/utils";
import type { Message } from "@/types";

export function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";

  return (
    <div
      className={cn(
        "flex w-full mb-6",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={cn(
          "max-w-[85%] sm:max-w-[75%] rounded-2xl px-5 py-3.5 shadow-sm text-[15px] leading-relaxed relative",
          "transition-all duration-300 ease-out animate-in fade-in slide-in-from-bottom-2",
          isUser
            ? "bg-indigo-600 text-white rounded-br-none"
            : "glass-panel text-slate-100 rounded-bl-none"
        )}
      >
        {/* Typing indicator when assistant content is empty (streaming placeholder) */}
        {!isUser && message.content === "" ? (
          <div className="flex space-x-1 items-center h-4">
            <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
            <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
            <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"></span>
          </div>
        ) : isUser ? (
          /* User messages: plain text (no markdown needed) */
          message.content.split("\n").map((line, i) => (
            <p key={i} className="my-0.5">
              {line}
            </p>
          ))
        ) : (
          /* Assistant messages: full markdown rendering */
          <div className="prose prose-invert prose-sm max-w-none prose-p:my-1 prose-headings:my-2 prose-pre:bg-slate-800/80 prose-pre:border prose-pre:border-slate-700 prose-code:text-indigo-300 prose-a:text-indigo-400 prose-strong:text-white">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}
