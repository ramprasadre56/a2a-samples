// Types for the A2A Copilot application

export interface Message {
  id: string;
  role: 'user' | 'agent';
  content: string;
  contextId?: string;
}

export interface Agent {
  name: string;
  description: string;
  url: string;
}

export interface User {
  name: string;
  email: string;
  image?: string;
}
