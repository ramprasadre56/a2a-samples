import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "A2A Copilot - AI Agent Communication",
  description: "Your AI-powered assistant for orchestrating multiple agents using the A2A Protocol",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
