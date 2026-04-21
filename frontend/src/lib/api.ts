import { fetchEventSource } from "@microsoft/fetch-event-source";
import { useChatStore } from "@/store/chatStore";
import { API_CHAT_STREAM } from "./constants";
import { generateId } from "./utils";
import toast from "react-hot-toast";

class RetryableError extends Error {}
class FatalError extends Error {}

export async function streamChat(
  message: string,
  thread_id: string,
  ctrl: AbortController
) {
  const store = useChatStore.getState();

  // Add placeholder response from Assistant before starting the stream
  store.addMessage({
    id: generateId(),
    role: "assistant",
    content: "",
    timestamp: Date.now(),
  });

  store.setStreaming(true);
  store.setStatusMessage("Thinking...");

  try {
    await fetchEventSource(API_CHAT_STREAM, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message, thread_id }),
      signal: ctrl.signal,

      async onopen(response) {
        if (
          response.ok &&
          response.headers.get("content-type")?.includes("text/event-stream")
        ) {
          return; // everything's good
        } else if (
          response.status >= 400 &&
          response.status < 500 &&
          response.status !== 429
        ) {
          toast.error(`Request failed (${response.status}). Please try again.`);
          throw new FatalError();
        } else {
          toast.error("Server error. Retrying...");
          throw new RetryableError();
        }
      },

      onmessage(msg) {
        console.debug(`SSE Event: ${msg.event}`, msg.data);
        if (msg.event === "message") {
          if (msg.data) {
            store.updateLastMessage(msg.data);
            store.setStatusMessage(null);
          }
        } else if (msg.event === "status") {
          store.setStatusMessage(msg.data);
        } else if (msg.event === "done") {
          console.log("Stream finished normally.");
          store.setStreaming(false);
          store.setStatusMessage(null);
        } else if (msg.event === "error") {
          console.error("Server-side stream error:", msg.data);
          toast.error(`AI Error: ${msg.data}`);
          store.setStatusMessage(null);
          store.setStreaming(false);
        }
      },

      onclose() {
        store.setStreaming(false);
        store.setStatusMessage(null);
      },

      onerror(err) {
        if (err instanceof FatalError) {
          throw err; // rethrow to stop the operation
        } else {
          console.error("Streaming error caught:", err);
          toast.error("Connection lost. Trying to reconnect...");
          store.setStatusMessage("Reconnecting...");
        }
      },
    });
  } catch (err) {
    if (err instanceof Error && err.name === "AbortError") {
      toast("Stream stopped.", { icon: "⏹️" });
    } else if (!(err instanceof FatalError)) {
      console.error("Stream completely failed:", err);
      toast.error("Failed to get a response. Please try again.");
    }
    store.setStreaming(false);
    store.setStatusMessage(null);
  }
}
