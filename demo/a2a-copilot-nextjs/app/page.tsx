'use client';

import Link from 'next/link';
import { Sparkles, ChevronDown, MessageCircle, Users, Network, Zap, Lightbulb, Globe, CheckCircle, PlusCircle, ArrowRight, BookOpen, MessageSquarePlus } from 'lucide-react';
import styles from './page.module.css';

function NavLink({ text, href }: { text: string; href: string }) {
  return (
    <Link href={href} className={styles.navLink}>
      {text}
    </Link>
  );
}

function DropdownNav({ text }: { text: string }) {
  return (
    <div className={styles.dropdownNav}>
      <span>{text}</span>
      <ChevronDown size={14} />
    </div>
  );
}

function HeaderNavigation() {
  return (
    <header className={styles.header}>
      <div className={styles.headerContent}>
        {/* Logo */}
        <div className={styles.logoSection}>
          <div className={styles.logoIcon}>
            <Sparkles size={20} color="white" />
          </div>
          <div className={styles.divider} />
          <h1 className={styles.logoText}>A2A Copilot</h1>
        </div>

        {/* Navigation */}
        <nav className={styles.nav}>
          <DropdownNav text="How it works" />
          <NavLink text="Features" href="#features" />
          <DropdownNav text="Learn how to use it" />
          <NavLink text="Documentation" href="https://a2a-protocol.org/latest/" />
          <DropdownNav text="More" />
        </nav>

        <div className={styles.spacer} />

        {/* CTA Buttons */}
        <div className={styles.ctaSection}>
          <Link href="/chat">
            <button className={styles.btnPrimary}>Open Copilot Chat</button>
          </Link>
          <Link href="/agents">
            <button className={styles.btnOutline}>View Agents</button>
          </Link>
        </div>
      </div>
    </header>
  );
}

function HeroSection() {
  return (
    <section className={styles.hero}>
      <div className={styles.heroContent}>
        {/* Badge */}
        <div className={styles.badge}>
          <Sparkles size={14} />
          <span>Powered by A2A Protocol</span>
        </div>

        {/* Heading */}
        <h1 className={styles.heroTitle}>
          Welcome to <span className={styles.gradientText}>A2A Copilot</span>
        </h1>

        {/* Subtitle */}
        <p className={styles.heroSubtitle}>
          Your AI-powered assistant for orchestrating multiple agents. Chat naturally and let the host agent route your requests to specialized agents.
        </p>

        {/* CTA Buttons */}
        <div className={styles.heroCta}>
          <Link href="/chat">
            <button className={styles.btnPrimaryLarge}>
              <MessageCircle size={20} />
              Start Chatting
            </button>
          </Link>
          <Link href="/agents">
            <button className={styles.btnSecondaryLarge}>
              <Users size={20} />
              Manage Agents
            </button>
          </Link>
        </div>
      </div>
    </section>
  );
}

function FeatureCard({ icon: Icon, title, description, gradient }: {
  icon: React.ElementType;
  title: string;
  description: string;
  gradient: string;
}) {
  return (
    <div className={styles.featureCard}>
      <div className={styles.featureIcon} style={{ background: gradient }}>
        <Icon size={32} color="white" />
      </div>
      <h3 className={styles.featureTitle}>{title}</h3>
      <p className={styles.featureDescription}>{description}</p>
    </div>
  );
}

function FeaturesSection() {
  return (
    <section className={styles.features} id="features">
      <h2 className={styles.sectionTitle}>How It Works</h2>
      <p className={styles.sectionSubtitle}>A2A enables seamless AI agent collaboration</p>
      <div className={styles.featureGrid}>
        <FeatureCard
          icon={Network}
          title="Orchestrate Agents"
          description="From quick tasks to complex workflows—your host agent intelligently routes requests to the right specialized agents."
          gradient="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        />
        <FeatureCard
          icon={Zap}
          title="Skip the Busywork"
          description="Agents can summarize, analyze, and automate, so you can focus on what matters most."
          gradient="linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
        />
        <FeatureCard
          icon={Lightbulb}
          title="Smart Suggestions"
          description="Not sure what to ask? The system offers helpful prompts to guide your next move and spark ideas."
          gradient="linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
        />
      </div>
    </section>
  );
}

function LanguageBadge({ lang, color }: { lang: string; color: string }) {
  return (
    <span className={styles.languageBadge} style={{ background: color }}>
      {lang}
    </span>
  );
}

function MultiLanguageSection() {
  return (
    <section className={styles.multiLanguage}>
      <div className={styles.multiLanguageContent}>
        <div className={styles.multiLanguageHeader}>
          <Globe size={32} className={styles.globeIcon} />
          <h2 className={styles.sectionTitle}>Multi-Language Agent Support</h2>
        </div>
        <p className={styles.sectionSubtitle}>
          The A2A protocol is language-agnostic. Connect agents written in any programming language!
        </p>
        <div className={styles.languageBadges}>
          <LanguageBadge lang="Python" color="#3776ab" />
          <LanguageBadge lang="JavaScript" color="#f7df1e" />
          <LanguageBadge lang=".NET" color="#512bd4" />
        </div>
        <div className={styles.checkList}>
          <div className={styles.checkItem}>
            <CheckCircle size={20} className={styles.checkIcon} />
            <span>Any agent implementing A2A can connect</span>
          </div>
          <div className={styles.checkItem}>
            <CheckCircle size={20} className={styles.checkIcon} />
            <span>Mix Python, JavaScript, Go agents in one system</span>
          </div>
          <div className={styles.checkItem}>
            <CheckCircle size={20} className={styles.checkIcon} />
            <span>Protocol-based communication over HTTP</span>
          </div>
          <div className={styles.checkItem}>
            <CheckCircle size={20} className={styles.checkIcon} />
            <span>Register remote agents by URL</span>
          </div>
        </div>
        <Link href="/agents" className={styles.registerLink}>
          <PlusCircle size={20} />
          <span>Register your remote agent and start testing with the host agent</span>
          <ArrowRight size={16} />
        </Link>
      </div>
    </section>
  );
}

function QuickActions() {
  return (
    <section className={styles.quickActions}>
      <h2 className={styles.sectionTitle}>Quick Actions</h2>
      <div className={styles.actionGrid}>
        <Link href="/chat" className={styles.actionCard}>
          <MessageSquarePlus size={24} className={styles.actionIconPrimary} />
          <div className={styles.actionText}>
            <strong>New Conversation</strong>
            <span>Start chatting with your agents</span>
          </div>
        </Link>
        <Link href="/agents" className={styles.actionCard}>
          <PlusCircle size={24} className={styles.actionIconSuccess} />
          <div className={styles.actionText}>
            <strong>Add Agent</strong>
            <span>Register a new remote agent</span>
          </div>
        </Link>
        <a href="https://a2a-protocol.org/latest/" target="_blank" rel="noopener noreferrer" className={styles.actionCard}>
          <BookOpen size={24} className={styles.actionIconWarning} />
          <div className={styles.actionText}>
            <strong>Documentation</strong>
            <span>Learn about A2A protocol</span>
          </div>
        </a>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.footerContent}>
        <div className={styles.footerLogo}>
          <Sparkles size={20} color="white" />
          <span>A2A Copilot</span>
        </div>
        <div className={styles.footerLinks}>
          <a href="https://github.com/google-a2a/a2a-samples" target="_blank" rel="noopener noreferrer">
            GitHub
          </a>
          <a href="https://a2a-protocol.org/latest/" target="_blank" rel="noopener noreferrer">
            Documentation
          </a>
        </div>
      </div>
    </footer>
  );
}

export default function Home() {
  return (
    <main className={styles.main}>
      <HeaderNavigation />
      <HeroSection />
      <FeaturesSection />
      <MultiLanguageSection />
      <QuickActions />
      <Footer />
    </main>
  );
}
