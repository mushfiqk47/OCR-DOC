"use client";

import { useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import { PanelLeft } from "lucide-react";
import clsx from "clsx";

export default function Shell({ children }: { children: React.ReactNode }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  // You might want to persist this in localStorage or handle mobile responsiveness
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 1024) {
        setIsSidebarOpen(false);
      } else {
        setIsSidebarOpen(true);
      }
    };

    handleResize(); // Set initial state
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="flex min-h-screen">
      <Sidebar isOpen={isSidebarOpen} onToggle={() => setIsSidebarOpen(false)} />
      
      {!isSidebarOpen && (
        <button
          onClick={() => setIsSidebarOpen(true)}
          className="fixed top-6 left-6 z-50 p-2 glass-card rounded-xl text-slate-400 hover:text-white transition-all duration-300 hover:scale-105"
          title="Open Sidebar"
        >
          <PanelLeft className="h-6 w-6" />
        </button>
      )}

      <main className={clsx(
        "flex-1 p-8 transition-all duration-300 ease-in-out overflow-y-auto h-screen",
        isSidebarOpen ? "ml-64" : "ml-0"
      )}>
        <div className="mx-auto max-w-6xl animate-in fade-in slide-in-from-bottom-4 duration-500">
          {children}
        </div>
      </main>
    </div>
  );
}
