# A2A Copilot - Next.js Frontend

A modern Next.js frontend for the A2A (Agent-to-Agent) protocol demo, migrated from the original Reflex Python application.

## Features

- 🤖 **Agent Orchestration**: Chat with a host agent that routes requests to specialized remote agents
- 🌐 **Multi-Language Support**: Connect agents written in Python, JavaScript, .NET, and more
- 💬 **Modern Chat UI**: Copilot-style chat interface with typing indicators and suggestions
- 📋 **Agent Management**: Register, view, and manage remote A2A agents
- 🎨 **Beautiful Design**: Premium, responsive UI with animations and gradients

## Getting Started

### Prerequisites

1. **Python Backend**: The Next.js app proxies API calls to the Python host agent. You need to run the original Reflex backend:

```bash
cd ../reflex_ui
pip install -e .
reflex run
```

This starts the backend at `http://localhost:12002`.

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Edit .env.local with your configuration
# - BACKEND_URL should point to your Python backend
# - Add Google OAuth credentials if using authentication

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Deployment to Vercel

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Configure environment variables in Vercel dashboard:
   - `BACKEND_URL`: URL of your deployed Python backend
   - `NEXTAUTH_SECRET`: Random secret string for session encryption
   - `GOOGLE_CLIENT_ID` & `GOOGLE_CLIENT_SECRET`: OAuth credentials

> **Note**: The Python host agent backend must be deployed separately (e.g., Google Cloud Run, Railway, or similar) for full production functionality.

## Project Structure

```
app/
├── page.tsx          # Landing page
├── chat/page.tsx     # Chat interface
├── agents/page.tsx   # Agent management
├── settings/page.tsx # Settings (placeholder)
├── api/
│   ├── message/      # Chat message proxy
│   └── agents/       # Agent list/register proxy
components/
├── Sidebar.tsx       # Navigation sidebar
utils/
├── store.ts          # Zustand state management
types/
├── index.ts          # TypeScript types
```

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **State Management**: Zustand
- **UI Components**: Radix UI Primitives
- **Icons**: Lucide React
- **Styling**: CSS Modules

## License

Apache 2.0 - See the main repository for details.
