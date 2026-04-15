# IU NWEO AI — Frontend

> Next.js 16 + React 19 chat interface for the Integral University AI Assistant.

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 16.2.3 | React framework (App Router) |
| React | 19.2.4 | UI library |
| Tailwind CSS | v4 | Utility-first styling |
| Zustand | 5.x | State management |
| react-hot-toast | latest | Toast notifications |
| react-markdown | latest | Markdown rendering for AI responses |
| Framer Motion | 12.x | Animations |
| Lucide React | latest | Icon system |
| @microsoft/fetch-event-source | 2.x | SSE streaming client |

## Architecture

```
frontend/
├── src/
│   ├── app/                         # Next.js App Router
│   │   ├── layout.tsx               # Root layout (fonts, providers)
│   │   ├── page.tsx                 # Home page (chat UI)
│   │   └── globals.css              # Design system tokens + utilities
│   ├── components/
│   │   ├── chat/                    # Chat-specific components
│   │   │   ├── ChatContainer.tsx    # Message list + auto-scroll
│   │   │   ├── ChatInput.tsx        # Input area with send/stop/clear
│   │   │   └── MessageBubble.tsx    # Message bubble with markdown rendering
│   │   ├── ui/                      # Shared UI primitives
│   │   │   └── ErrorBoundary.tsx    # React error boundary
│   │   └── providers/
│   │       └── ToastProvider.tsx    # Toast notification provider
│   ├── lib/
│   │   ├── api.ts                   # SSE client (fetchEventSource)
│   │   ├── constants.ts             # API URLs
│   │   └── utils.ts                 # cn(), generateId(), formatTimestamp()
│   ├── store/
│   │   └── chatStore.ts             # Zustand store (messages, streaming, thread)
│   └── types/
│       └── index.ts                 # Shared TypeScript interfaces
```

## Prerequisites

- **Node.js** 20+
- **npm** 10+

## Installation

```bash
npm install
```

## Environment Variables

Create a `.env.local` file (optional — defaults to `localhost:8080`):

```env
NEXT_PUBLIC_API_URL=http://localhost:8080
```

## Running

```bash
# Development (with hot-reload)
npm run dev

# Production build
npm run build
npm start
```

The dev server runs at **http://localhost:3000**.

## Design System

### Color Tokens (defined in `globals.css`)

| Token | Value | Usage |
|-------|-------|-------|
| `--color-iu-bg-base` | `#0f172a` | Page background |
| `--color-iu-bg-glass` | `rgba(30,41,59,0.7)` | Glass panel background |
| `--color-iu-accent` | `#6366f1` | Primary accent (indigo) |
| `--color-iu-accent-glow` | `rgba(99,102,241,0.5)` | Glow effects |
| `--color-iu-text-main` | `#f8fafc` | Primary text |
| `--color-iu-text-muted` | `#94a3b8` | Secondary text |
| `--color-iu-border` | `rgba(255,255,255,0.08)` | Subtle borders |

### Custom Utilities

| Class | Effect |
|-------|--------|
| `.glass-panel` | Glassmorphism panel (blur + border + semi-transparent bg) |

### Fonts

- **Geist Sans** — UI text
- **Geist Mono** — Code blocks

## Component Reference

### `<ChatContainer />`
Renders the message list with auto-scroll. Shows an empty state with branding when no messages exist. Displays a status pill (animated pulse) during LangGraph node transitions.

### `<ChatInput />`
Textarea with three action buttons:
- **Clear** (Trash icon) — Resets conversation and generates a new thread ID
- **Send** (Arrow icon) — Sends message and initiates SSE stream
- **Stop** (Square icon) — Aborts the current stream (visible during streaming)

### `<MessageBubble />`
Renders individual messages. User messages appear right-aligned with indigo background. Assistant messages appear left-aligned with glass-panel styling and full markdown rendering (tables, code blocks, bold, links, etc.).

### `<ErrorBoundary />`
React class component wrapping the app. Catches render crashes and shows a styled recovery UI with a "Try Again" button.

### `<ToastProvider />`
Configures react-hot-toast with dark glassmorphism styling. Positioned top-right. Error toasts last 5s, standard toasts 4s.

## Error Handling

| Scenario | User Feedback |
|----------|---------------|
| Server returns 4xx | Toast error with status code |
| Server returns 5xx | Toast "Server error. Retrying..." |
| SSE stream error event | Toast with error message from backend |
| Connection lost | Toast "Connection lost. Trying to reconnect..." |
| User aborts stream | Toast "Stream stopped." |
| Fatal stream failure | Toast "Failed to get a response. Please try again." |
| React render crash | Error boundary with "Try Again" button |
