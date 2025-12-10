import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Anti-Gravity",
  description: "Autonomous Agent Orchestrator",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased h-screen w-screen bg-[#050505] text-white selection:bg-purple-500/30">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-20 pointer-events-none" />
        <main className="h-full w-full flex flex-col">
          {children}
        </main>
      </body>
    </html>
  );
}
