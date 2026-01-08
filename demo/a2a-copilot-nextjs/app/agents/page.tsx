'use client';

import { useEffect } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { Bot, Plus, RefreshCw, Trash2, MessageCircle, Link as LinkIcon, Users, X, Check } from 'lucide-react';
import Sidebar from '@/components/Sidebar';
import { useAppStore } from '@/utils/store';
import styles from './page.module.css';

function AgentTile({ name, description, url }: { name: string; description: string; url: string }) {
    const { removeAgent } = useAppStore();

    return (
        <div className={styles.tile}>
            <div className={styles.tileHeader}>
                <div className={styles.tileIcon}>
                    <Bot size={20} color="white" />
                </div>
                <div className={styles.tileActions}>
                    <button className={styles.actionBtn}>
                        <MessageCircle size={14} />
                    </button>
                    <button className={styles.actionBtn} onClick={() => removeAgent(url)}>
                        <Trash2 size={14} />
                    </button>
                </div>
            </div>
            <h3 className={styles.tileName}>{name}</h3>
            <div className={styles.tileStatus}>
                <span className={styles.statusDot} />
                <span>Connected</span>
            </div>
            <p className={styles.tileDescription}>{description || 'No description'}</p>
            <div className={styles.tileUrl}>
                <LinkIcon size={12} />
            </div>
        </div>
    );
}

function AddAgentDialog() {
    const { showAgentDialog, toggleAgentDialog, newAgentUrl, setNewAgentUrl, registerAgent } = useAppStore();

    return (
        <Dialog.Root open={showAgentDialog} onOpenChange={toggleAgentDialog}>
            <Dialog.Trigger asChild>
                <button className={styles.addBtn}>
                    <Plus size={16} />
                    Add Agent
                </button>
            </Dialog.Trigger>
            <Dialog.Portal>
                <Dialog.Overlay className={styles.overlay} />
                <Dialog.Content className={styles.dialogContent}>
                    <div className={styles.dialogHeader}>
                        <div className={styles.dialogIcon}>
                            <Plus size={20} color="white" />
                        </div>
                        <Dialog.Title className={styles.dialogTitle}>Register Remote Agent</Dialog.Title>
                    </div>
                    <Dialog.Description className={styles.dialogDescription}>
                        Configure the agent connection settings for production use.
                    </Dialog.Description>

                    <div className={styles.formGroup}>
                        <label>Agent URL</label>
                        <input
                            type="text"
                            placeholder="https://api.example.com or http://localhost:9999"
                            value={newAgentUrl}
                            onChange={(e) => setNewAgentUrl(e.target.value)}
                            className={styles.input}
                        />
                        <span className={styles.hint}>The agent&apos;s base URL. Must expose /.well-known/agent.json</span>
                    </div>

                    <div className={styles.dialogActions}>
                        <Dialog.Close asChild>
                            <button className={styles.cancelBtn}>Cancel</button>
                        </Dialog.Close>
                        <Dialog.Close asChild>
                            <button className={styles.submitBtn} onClick={registerAgent}>
                                <Check size={16} />
                                Register Agent
                            </button>
                        </Dialog.Close>
                    </div>

                    <Dialog.Close asChild>
                        <button className={styles.closeBtn}>
                            <X size={16} />
                        </button>
                    </Dialog.Close>
                </Dialog.Content>
            </Dialog.Portal>
        </Dialog.Root>
    );
}

function AgentsHeader() {
    const { refreshAgents } = useAppStore();

    return (
        <div className={styles.header}>
            <div className={styles.headerInfo}>
                <h1>Remote Agents</h1>
                <p>Manage your connected A2A agents</p>
            </div>
            <div className={styles.headerActions}>
                <button className={styles.refreshBtn} onClick={refreshAgents}>
                    <RefreshCw size={16} />
                    Refresh
                </button>
                <AddAgentDialog />
            </div>
        </div>
    );
}

function EmptyAgentsState() {
    return (
        <div className={styles.emptyState}>
            <div className={styles.emptyIcon}>
                <Users size={40} color="white" />
            </div>
            <h2>No agents connected</h2>
            <p>Add your first remote agent to get started.</p>
            <AddAgentDialog />
        </div>
    );
}

function AgentGrid() {
    const { agents } = useAppStore();

    if (agents.length === 0) {
        return <EmptyAgentsState />;
    }

    return (
        <div className={styles.gridContainer}>
            <div className={styles.grid}>
                {agents.map((agent, index) => (
                    <AgentTile key={index} {...agent} />
                ))}
            </div>
        </div>
    );
}

export default function AgentsPage() {
    const { setActiveNav, refreshAgents } = useAppStore();

    useEffect(() => {
        setActiveNav('agents');
        refreshAgents();
    }, [setActiveNav, refreshAgents]);

    return (
        <div className={styles.layout}>
            <Sidebar />
            <main className={styles.main}>
                <AgentsHeader />
                <AgentGrid />
            </main>
        </div>
    );
}
