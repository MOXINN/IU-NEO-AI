import clsx from "clsx";
import { Message } from "@/store/chatStore";

export function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";

  return (
    <div
      className={clsx(
        "flex w-full mb-6",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={clsx(
          "max-w-[85%] sm:max-w-[75%] rounded-2xl px-5 py-3.5 shadow-sm text-[15px] leading-relaxed relative",
          "transition-all duration-300 ease-out animate-in fade-in slide-in-from-bottom-2",
          isUser
            ? "bg-indigo-600 text-white rounded-br-none"
            : "glass-panel text-slate-100 rounded-bl-none prose prose-invert prose-p:my-1 prose-pre:bg-slate-800/80 prose-pre:border prose-pre:border-slate-700"
        )}
      >
        {/* Simple markdown bold/code parser since we didn't install react-markdown yet for speed */}
        {message.content.split("\n").map((line, i) => (
          <p key={i} className="my-1">
            {line}
          </p>
        ))}
        {!isUser && message.content === "" && (
          <div className="flex space-x-1 items-center h-4">
            <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
            <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
            <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"></span>
          </div>
        )}
      </div>
    </div>
  );
}
