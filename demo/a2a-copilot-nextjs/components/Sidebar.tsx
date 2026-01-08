'use client';

import Link from 'next/link';
import { Sparkles, MessageCircle, Users, Settings, PanelLeft, PanelLeftClose, Search, Bot } from 'lucide-react';
import { useAppStore } from '@/utils/store';
import styles from './Sidebar.module.css';

export default function Sidebar() {
    const {
        sidebarCollapsed,
        toggleSidebar,
        activeNav,
        setActiveNav,
        agents
    } = useAppStore();

    const navItems = [
        { key: 'chat', label: 'Chat', icon: MessageCircle, href: '/chat' },
        { key: 'agents', label: 'Agents', icon: Users, href: '/agents' },
        { key: 'settings', label: 'Settings', icon: Settings, href: '/settings' },
    ];

    return (
        <aside className={`${styles.sidebar} ${sidebarCollapsed ? styles.collapsed : ''}`}>
            <div className={styles.content}>
                {/* Header */}
                <div className={styles.header}>
                    <Link href="/" className={styles.logo} onClick={() => setActiveNav('chat')}>
                        <div className={styles.logoIcon}>
                            <Sparkles size={24} color="white" />
                        </div>
                        {!sidebarCollapsed && <span className={styles.logoText}>A2A Copilot</span>}
                    </Link>
                    {!sidebarCollapsed && <div className={styles.spacer} />}
                    <button className={styles.toggleBtn} onClick={toggleSidebar}>
                        {sidebarCollapsed ? <PanelLeft size={18} /> : <PanelLeftClose size={18} />}
                    </button>
                </div>

                {/* Search */}
                {!sidebarCollapsed && (
                    <div className={styles.searchWrapper}>
                        <div className={styles.searchInput}>
                            <Search size={16} className={styles.searchIcon} />
                            <input type="text" placeholder="Search..." />
                        </div>
                    </div>
                )}

                {/* Navigation */}
                <nav className={styles.nav}>
                    {navItems.map((item) => (
                        <Link
                            key={item.key}
                            href={item.href}
                            className={`${styles.navItem} ${activeNav === item.key ? styles.active : ''}`}
                            onClick={() => setActiveNav(item.key as 'chat' | 'agents' | 'settings')}
                        >
                            <item.icon size={20} />
                            {!sidebarCollapsed && <span>{item.label}</span>}
                        </Link>
                    ))}
                </nav>

                {/* Agents Section */}
                {!sidebarCollapsed && (
                    <div className={styles.agentsSection}>
                        <div className={styles.agentsSectionHeader}>
                            <span className={styles.agentsSectionTitle}>AGENTS</span>
                            <span className={styles.agentsCount}>{agents.length}</span>
                        </div>
                        {agents.length > 0 ? (
                            <div className={styles.agentsList}>
                                {agents.map((agent, index) => (
                                    <div key={index} className={styles.agentMiniCard}>
                                        <div className={styles.agentMiniIcon}>
                                            <Bot size={16} color="white" />
                                        </div>
                                        <div className={styles.agentMiniInfo}>
                                            <span className={styles.agentMiniName}>{agent.name}</span>
                                            <div className={styles.agentMiniStatus}>
                                                <span className={styles.statusDot} />
                                                <span>Connected</span>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className={styles.noAgents}>No agents connected</div>
                        )}
                    </div>
                )}

                <div className={styles.spacer} />

                {/* User Profile */}
                <div className={styles.userProfile}>
                    <div className={styles.avatar}>U</div>
                    {!sidebarCollapsed && (
                        <div className={styles.userInfo}>
                            <span className={styles.userName}>Guest User</span>
                            <span className={styles.userEmail}>Not signed in</span>
                        </div>
                    )}
                </div>
            </div>
        </aside>
    );
}
