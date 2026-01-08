'use client';

import { useEffect } from 'react';
import { Sparkles, Send, AlertCircle, X, Key, Check } from 'lucide-react';
import Sidebar from '@/components/Sidebar';
import { useAppStore } from '@/utils/store';
import styles from './page.module.css';

function MessageBubble({ role, content }: { role: 'user' | 'agent'; content: string }) {
    const isUser = role === 'user';

    return (
        <div className={`${styles.messageRow} ${isUser ? styles.userRow : ''}`}>
            {!isUser && (
                <div className={styles.agentAvatar}>
                    <Sparkles size={16} color="white" />
                </div>
            )}
            <div className={`${styles.messageBubble} ${isUser ? styles.userBubble : styles.agentBubble}`}>
                <p>{content}</p>
            </div>
            {isUser && (
                <div className={styles.userAvatar}>U</div>
            )}
        </div>
    );
}

function TypingIndicator() {
    const { isProcessing } = useAppStore();

    if (!isProcessing) return null;

    return (
        <div className={styles.messageRow}>
            <div className={styles.agentAvatar}>
                <Sparkles size={16} color="white" />
            </div>
            <div className={styles.typingBubble}>
                <span className={styles.dot} style={{ animationDelay: '0s' }} />
                <span className={styles.dot} style={{ animationDelay: '0.2s' }} />
                <span className={styles.dot} style={{ animationDelay: '0.4s' }} />
            </div>
        </div>
    );
}

function SuggestionChip({ text, prompt }: { text: string; prompt: string }) {
    const { setCurrentInput } = useAppStore();

    return (
        <button className={styles.suggestionChip} onClick={() => setCurrentInput(prompt)}>
            <Sparkles size={14} />
            <span>{text}</span>
        </button>
    );
}

function EmptyState() {
    const { apiKey, setApiKey } = useAppStore();
    const hasApiKey = apiKey.length > 10;

    if (!hasApiKey) {
        return (
            <div className={styles.emptyState}>
                <div className={styles.emptyCard}>
                    <div className={styles.emptyIcon}>
                        <Key size={32} color="white" />
                    </div>
                    <h2>Configure API Key</h2>
                    <p>Enter your Google Gemini API key to start chatting with AI agents.</p>
                    <input
                        type="password"
                        placeholder="Enter your Gemini API key..."
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                        className={styles.apiKeyInput}
                    />
                    <button className={styles.saveKeyBtn}>
                        <Check size={18} />
                        Save API Key
                    </button>
                    <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className={styles.getKeyLink}>
                        Get a free API key from Google AI Studio →
                    </a>
                </div>
            </div>
        );
    }

    return (
        <div className={styles.emptyState}>
            <div className={styles.emptyIcon}>
                <Sparkles size={48} color="white" />
            </div>
            <h2>How can I help you today?</h2>
            <p>I can route your requests to specialized agents. Try asking me something!</p>
            <span className={styles.suggestionLabel}>Try these suggestions:</span>
            <div className={styles.suggestions}>
                <SuggestionChip text="Convert currency" prompt="Convert 100 USD to EUR" />
                <SuggestionChip text="Say hello" prompt="Hello, how are you?" />
                <SuggestionChip text="List agents" prompt="What agents are available?" />
            </div>
        </div>
    );
}

function ChatMessages() {
    const { messages } = useAppStore();

    if (messages.length === 0) {
        return <EmptyState />;
    }

    return (
        <div className={styles.messagesContainer}>
            <div className={styles.messages}>
                {messages.map((msg) => (
                    <MessageBubble key={msg.id} role={msg.role} content={msg.content} />
                ))}
                <TypingIndicator />
            </div>
        </div>
    );
}

function ChatInput() {
    const { currentInput, setCurrentInput, isProcessing, sendMessage } = useAppStore();

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        sendMessage();
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className={styles.inputContainer}>
            <form className={styles.inputForm} onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Ask me anything..."
                    value={currentInput}
                    onChange={(e) => setCurrentInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={isProcessing}
                    className={styles.input}
                />
                <button type="submit" disabled={isProcessing} className={styles.sendBtn}>
                    {isProcessing ? (
                        <span className={styles.spinner} />
                    ) : (
                        <Send size={20} />
                    )}
                </button>
            </form>
        </div>
    );
}

function ErrorBanner() {
    const { errorMessage, clearError } = useAppStore();

    if (!errorMessage) return null;

    return (
        <div className={styles.errorBanner}>
            <AlertCircle size={18} />
            <span>{errorMessage}</span>
            <button onClick={clearError} className={styles.closeError}>
                <X size={14} />
            </button>
        </div>
    );
}

export default function ChatPage() {
    const { setActiveNav } = useAppStore();

    useEffect(() => {
        setActiveNav('chat');
    }, [setActiveNav]);

    return (
        <div className={styles.layout}>
            <Sidebar />
            <main className={styles.main}>
                <ErrorBanner />
                <ChatMessages />
                <ChatInput />
            </main>
        </div>
    );
}
