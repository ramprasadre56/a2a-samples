'use client';

import { useEffect } from 'react';
import { Settings } from 'lucide-react';
import Sidebar from '@/components/Sidebar';
import { useAppStore } from '@/utils/store';
import styles from './page.module.css';

export default function SettingsPage() {
    const { setActiveNav } = useAppStore();

    useEffect(() => {
        setActiveNav('settings');
    }, [setActiveNav]);

    return (
        <div className={styles.layout}>
            <Sidebar />
            <main className={styles.main}>
                <div className={styles.content}>
                    <div className={styles.icon}>
                        <Settings size={48} color="white" />
                    </div>
                    <h1>Settings</h1>
                    <p>Settings page coming soon...</p>
                </div>
            </main>
        </div>
    );
}
