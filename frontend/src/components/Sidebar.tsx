"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Home, FileText, Table, Image as ImageIcon, ScanBarcode,
  ChevronDown, ChevronRight, Settings, FileType, FileStack,
  PanelLeftClose, PanelLeft
} from "lucide-react";
import clsx from "clsx";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

type NavGroup = {
  title: string;
  icon: React.ElementType;
  color: string;
  items: { name: string; href: string }[];
};

const navGroups: NavGroup[] = [
  {
    title: "Conversion",
    icon: FileType,
    color: "text-blue-400",
    items: [
      { name: "JPG to Word", href: "/jpg-to-word" },
      { name: "PDF Translator", href: "/pdf-translator" },
      { name: "PDF to Text", href: "/pdf-to-text" },
      { name: "PDF to Word", href: "/pdf-to-word" },
      { name: "Text to PDF", href: "/text-to-pdf" },
      { name: "Text to Word", href: "/text-to-word" },
      { name: "Word to PDF", href: "/word-to-pdf" },
      { name: "HTML to PDF", href: "/html-to-pdf" },
      { name: "PDF to HTML", href: "/pdf-to-html" },
    ]
  },
  {
    title: "Spreadsheet",
    icon: Table,
    color: "text-emerald-400",
    items: [
      { name: "JPG to Excel", href: "/jpg-to-excel" },
      { name: "PDF to Excel", href: "/pdf-to-excel" },
      { name: "PDF to CSV", href: "/pdf-to-csv" },
      { name: "Excel to JPG", href: "/excel-to-jpg" },
    ]
  },
  {
    title: "Image Tools",
    icon: ImageIcon,
    color: "text-purple-400",
    items: [
      { name: "Invert Image", href: "/invert-image" },
      { name: "Text to Image", href: "/text-to-image" },
      { name: "Image Translator", href: "/image-translator" },
      { name: "Image to PDF", href: "/image-to-pdf" },
      { name: "PDF to JPG", href: "/pdf-to-jpg" },
      { name: "Word to JPG", href: "/word-to-jpg" },
      { name: "Merge PDF", href: "/merge-pdf" },
    ]
  },
  {
    title: "Scan & Code",
    icon: ScanBarcode,
    color: "text-amber-400",
    items: [
      { name: "QR Scanner", href: "/qr-scanner" },
      { name: "QR Generator", href: "/qr-generator" },
      { name: "Barcode Scanner", href: "/barcode-scanner" },
    ]
  },
];

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

export default function Sidebar({ isOpen, onToggle }: SidebarProps) {
  const pathname = usePathname();
  // Default open all or specific? Let's keep them open by default for visibility
  const [openGroups, setOpenGroups] = useState<Record<string, boolean>>({
    "Conversion": true,
    "Spreadsheet": true,
    "Image Tools": true,
    "Scan & Code": true,
  });

  const toggleGroup = (title: string) => {
    setOpenGroups(prev => ({ ...prev, [title]: !prev[title] }));
  };

  return (
    <aside className={clsx(
      "fixed left-0 top-0 z-40 h-screen w-64 glass-panel flex flex-col transition-transform duration-300 ease-in-out",
      !isOpen && "-translate-x-full"
    )}>
      <div className="flex items-center justify-between px-6 py-6 border-b border-slate-800/60">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-indigo-500 to-blue-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <span className="font-bold text-white text-lg">DI</span>
          </div>
          <span className="text-lg font-bold text-slate-100 tracking-tight">DocIntel</span>
        </div>
        <button 
          onClick={onToggle}
          className="p-1.5 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-slate-100 transition-colors"
          title="Close Sidebar"
        >
          <PanelLeftClose className="h-5 w-5" />
        </button>
      </div>

      <nav className="flex-1 overflow-y-auto py-6 px-3 space-y-1 custom-scrollbar">
        <Link
          href="/"
          className={clsx(
            "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-200 mb-6",
            pathname === "/"
              ? "bg-slate-800 text-white shadow-md shadow-slate-900/20"
              : "text-slate-400 hover:bg-slate-800/50 hover:text-slate-200"
          )}
        >
          <Home className="h-5 w-5" />
          Dashboard
        </Link>

        {navGroups.map((group) => (
          <div key={group.title} className="mb-2">
            <button
              onClick={() => toggleGroup(group.title)}
              className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-xs font-semibold uppercase tracking-wider text-slate-500 hover:text-slate-300 transition-colors"
            >
              <div className="flex items-center gap-2">
                <group.icon className={clsx("h-4 w-4", group.color)} />
                {group.title}
              </div>
              {openGroups[group.title] ?
                <ChevronDown className="h-3 w-3" /> :
                <ChevronRight className="h-3 w-3" />
              }
            </button>

            <AnimatePresence initial={false}>
              {openGroups[group.title] && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                  className="overflow-hidden"
                >
                  <div className="mt-1 space-y-0.5 pl-2 relative">
                    {/* Guide line */}
                    <div className="absolute left-4 top-0 bottom-0 w-px bg-slate-800/60" />

                    {group.items.map((item) => {
                      const isActive = pathname === item.href;
                      return (
                        <Link
                          key={item.href}
                          href={item.href}
                          className={clsx(
                            "flex items-center gap-2 rounded-lg py-2 pl-6 pr-3 text-sm font-medium transition-all duration-200 relative",
                            isActive
                              ? "text-blue-400 bg-blue-500/5"
                              : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/30"
                          )}
                        >
                          {isActive && (
                            <motion.div
                              layoutId="sidebar-active"
                              className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-blue-500 rounded-r-full"
                            />
                          )}
                          {item.name}
                        </Link>
                      );
                    })}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </nav>

      <div className="border-t border-slate-800/60 p-4">
        <button className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium text-slate-400 transition-all hover:bg-slate-800/50 hover:text-slate-200">
          <Settings className="h-5 w-5" />
          Settings
        </button>
      </div>
    </aside>
  );
}
