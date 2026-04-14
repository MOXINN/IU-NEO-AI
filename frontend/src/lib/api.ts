import { fetchEventSource } from "@microsoft/fetch-event-source";
import { useChatStore } from "@/store/chatStore";
import { API_CHAT_STREAM } from "./constants";

class RetryableError extends Error {}
class FatalError extends Error {}

export async function streamChat(message: string, thread_id: string, ctrl: AbortController) {
  const store = useChatStore.getState();
  
  console.log("Starting stream to:", API_CHAT_STREAM);
  
  // Add placeholder response from Assistant first before starting real stream
  store.addMessage({
    id: Math.random().toString(36).substring(7),
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
        if (response.ok && response.headers.get("content-type")?.includes("text/event-stream")) {
          return; // everything's good
        } else if (response.status >= 400 && response.status < 500 && response.status !== 429) {
          // client-side errors are usually non-retriable
          throw new FatalError();
        } else {
          throw new RetryableError();
        }
      },
      onmessage(msg) {
        // Events are sent by our Python backend (`yield { "event": ..., "data": ... }`)
        if (msg.event === "message") {
          store.updateLastMessage(msg.data);
          store.setStatusMessage(null); // Once content arrives, clear status
        } else if (msg.event === "status") {
          store.setStatusMessage(msg.data);
        } else if (msg.event === "done") {
          store.setStreaming(false);
          store.setStatusMessage(null);
        } else if (msg.event === "error") {
          console.error("Server stream error:", msg.data);
          store.setStatusMessage(`Error: ${msg.data}`);
          store.setStreaming(false);
        }
      },
      onclose() {
        console.log("Connection closed by server.");
        store.setStreaming(false);
        store.setStatusMessage(null);
      },
      onerror(err) {
        if (err instanceof FatalError) {
          throw err; // rethrow to stop the operation
        } else {
          console.error("Streaming error caught:", err);
          store.setStatusMessage("Connection lost. Trying again...");
        }
      }
    });
  } catch (err) {
    if (err instanceof Error && err.name === "AbortError") {
      console.log("Stream aborted by user");
    } else {
      console.error("Stream completely failed:", err);
      store.setStatusMessage("Failed to receive response.");
    }
    store.setStreaming(false);
  }
}
