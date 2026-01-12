import { create } from 'zustand';
import { Message, Agent } from '@/types';

interface AppState {
    // Chat state
    messages: Message[];
    currentInput: string;
    isProcessing: boolean;
    contextId: string | null;

    // Agent state
    agents: Agent[];
    newAgentUrl: string;
    showAgentDialog: boolean;

    // UI state
    sidebarCollapsed: boolean;
    activeNav: 'chat' | 'agents' | 'settings';

    // API key
    apiKey: string;

    // Error
    errorMessage: string;

    // Actions
    setCurrentInput: (input: string) => void;
    setApiKey: (key: string) => void;
    setNewAgentUrl: (url: string) => void;
    toggleSidebar: () => void;
    setActiveNav: (nav: 'chat' | 'agents' | 'settings') => void;
    toggleAgentDialog: () => void;
    clearError: () => void;
    newConversation: () => void;

    // Async actions
    sendMessage: () => Promise<void>;
    refreshAgents: () => Promise<void>;
    registerAgent: () => Promise<void>;
    removeAgent: (url: string) => void;
}

export const useAppStore = create<AppState>((set, get) => ({
    // Initial state
    messages: [],
    currentInput: '',
    isProcessing: false,
    contextId: null,
    agents: [],
    newAgentUrl: '',
    showAgentDialog: false,
    sidebarCollapsed: false,
    activeNav: 'chat',
    apiKey: typeof window !== 'undefined' ? localStorage.getItem('gemini_api_key') || '' : '',
    errorMessage: '',

    // Setters
    setCurrentInput: (input) => set({ currentInput: input }),
    setApiKey: (key) => {
        if (typeof window !== 'undefined') {
            localStorage.setItem('gemini_api_key', key);
        }
        set({ apiKey: key });
    },
    setNewAgentUrl: (url) => set({ newAgentUrl: url }),
    toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
    setActiveNav: (nav) => set({ activeNav: nav }),
    toggleAgentDialog: () => set((state) => ({
        showAgentDialog: !state.showAgentDialog,
        newAgentUrl: state.showAgentDialog ? '' : state.newAgentUrl
    })),
    clearError: () => set({ errorMessage: '' }),
    newConversation: () => set({ messages: [], contextId: null, errorMessage: '' }),

    // Send message to host agent
    sendMessage: async () => {
        const { currentInput, contextId, apiKey } = get();
        if (!currentInput.trim()) return;

        set({ isProcessing: true, errorMessage: '' });
        const userMessage = currentInput;
        set({ currentInput: '' });

        // Add user message immediately
        const userMsg: Message = {
            id: crypto.randomUUID(),
            role: 'user',
            content: userMessage,
            contextId: contextId || undefined,
        };
        set((state) => ({ messages: [...state.messages, userMsg] }));

        try {
            const response = await fetch('/api/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...(apiKey ? { 'X-API-Key': apiKey } : {})
                },
                body: JSON.stringify({
                    message: userMessage,
                    contextId
                }),
            });

            if (!response.ok) throw new Error('Failed to send message');

            const data = await response.json();

            if (data.contextId) {
                set({ contextId: data.contextId });
            }

            if (data.response) {
                const agentMsg: Message = {
                    id: crypto.randomUUID(),
                    role: 'agent',
                    content: data.response,
                    contextId: data.contextId,
                };
                set((state) => ({ messages: [...state.messages, agentMsg] }));
            }
        } catch (error) {
            const err = error as Error;
            set({ errorMessage: `Error: ${err.message}` });
            const errorMsg: Message = {
                id: crypto.randomUUID(),
                role: 'agent',
                content: `Sorry, an error occurred: ${err.message}`,
                contextId: contextId || undefined,
            };
            set((state) => ({ messages: [...state.messages, errorMsg] }));
        } finally {
            set({ isProcessing: false });
        }
    },

    // Refresh agents list
    refreshAgents: async () => {
        try {
            const response = await fetch('/api/agents');
            if (!response.ok) throw new Error('Failed to fetch agents');

            const data = await response.json();
            const agents: Agent[] = (data.result || []).map((a: { name: string; description?: string; url?: string }) => ({
                name: a.name,
                description: a.description || '',
                url: a.url || '',
            }));
            set({ agents });
        } catch (error) {
            const err = error as Error;
            set({ errorMessage: `Failed to refresh agents: ${err.message}` });
        }
    },

    // Register new agent
    registerAgent: async () => {
        const { newAgentUrl } = get();
        if (!newAgentUrl.trim()) return;

        try {
            const response = await fetch('/api/agents', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: newAgentUrl }),
            });

            if (!response.ok) throw new Error('Failed to register agent');

            const data = await response.json();
            if (data.success) {
                set({ newAgentUrl: '', showAgentDialog: false });
                get().refreshAgents();
            } else {
                set({ errorMessage: `Failed to register: ${data.error || 'Unknown error'}` });
            }
        } catch (error) {
            const err = error as Error;
            set({ errorMessage: `Failed to register agent: ${err.message}` });
        }
    },

    // Remove agent
    removeAgent: (url) => {
        set((state) => ({
            agents: state.agents.filter((a) => a.url !== url)
        }));
    },
}));
