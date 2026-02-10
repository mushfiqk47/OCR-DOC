"use client";

import { Check, ChevronsUpDown, Search, X } from "lucide-react";
import clsx from "clsx";
import { useState, useMemo, useRef, useEffect } from "react";
import { LANGUAGES } from "@/constants/languages";

interface LanguageSelectorProps {
    value: string;
    onChange: (value: string) => void;
}

export default function LanguageSelector({ value, onChange }: LanguageSelectorProps) {
    const [open, setOpen] = useState(false);
    const [searchQuery, setSearchQuery] = useState("");
    const dropdownRef = useRef<HTMLDivElement>(null);

    const filteredLanguages = useMemo(() => {
        if (!searchQuery) return LANGUAGES;
        const query = searchQuery.toLowerCase();
        return LANGUAGES.filter(
            (lang) =>
                lang.name.toLowerCase().includes(query) ||
                lang.code.toLowerCase().includes(query)
        );
    }, [searchQuery]);

    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    // Reset search when opening/closing
    useEffect(() => {
        if (!open) {
            setSearchQuery("");
        }
    }, [open]);

    return (
        <div className="relative" ref={dropdownRef}>
            <button
                type="button"
                onClick={() => setOpen(!open)}
                className="w-full flex items-center justify-between rounded-xl border border-slate-700 bg-slate-950/50 px-4 py-3 text-slate-200 shadow-sm hover:bg-slate-900 transition-all focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
                <span className="truncate">{value || "Select language..."}</span>
                <ChevronsUpDown className="ml-2 h-4 w-4 opacity-50 shrink-0" />
            </button>

            {open && (
                <div className="absolute z-[60] mt-2 max-h-80 w-full flex flex-col overflow-hidden rounded-xl border border-slate-700 bg-slate-900/95 backdrop-blur-xl shadow-2xl animate-in fade-in zoom-in duration-200">
                    <div className="p-2 border-b border-slate-800 sticky top-0 bg-slate-900/50 z-10">
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
                            <input
                                autoFocus
                                type="text"
                                placeholder="Search languages..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full bg-slate-950 border border-slate-700 rounded-lg py-2 pl-9 pr-8 text-sm text-slate-200 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                            />
                            {searchQuery && (
                                <button
                                    onClick={() => setSearchQuery("")}
                                    className="absolute right-2 top-1/2 -translate-y-1/2 p-1 hover:bg-slate-800 rounded-full"
                                >
                                    <X className="h-3 w-3 text-slate-500" />
                                </button>
                            )}
                        </div>
                    </div>

                    <div className="overflow-y-auto flex-1 custom-scrollbar">
                        {filteredLanguages.length > 0 ? (
                            filteredLanguages.map((language) => (
                                <div
                                    key={`${language.code}-${language.name}`}
                                    className={clsx(
                                        "flex items-center justify-between px-4 py-2.5 cursor-pointer hover:bg-slate-800 transition-colors text-sm",
                                        value === language.name ? "text-indigo-400 bg-indigo-500/10" : "text-slate-300"
                                    )}
                                    onClick={() => {
                                        onChange(language.name);
                                        setOpen(false);
                                    }}
                                >
                                    <div className="flex flex-col">
                                        <span>{language.name}</span>
                                        <span className="text-[10px] opacity-40 uppercase tracking-tighter">{language.code}</span>
                                    </div>
                                    {value === language.name && <Check className="h-4 w-4" />}
                                </div>
                            ))
                        ) : (
                            <div className="px-4 py-8 text-center text-slate-500 text-sm">
                                No languages found
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
