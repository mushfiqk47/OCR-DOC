"use client";

import Link from "next/link";
import {
    FileText,
    Table,
    Image as ImageIcon,
    ScanBarcode,
    ArrowRight,
    FileType,
    FileStack,
    Zap,
    Sparkles,
    Search
} from "lucide-react";
import clsx from "clsx";
import { motion } from "framer-motion";
import { useState } from "react";

const categories = [
    {
        title: "Document Conversion",
        icon: FileType,
        description: "Transform documents between formats with high fidelity.",
        color: "from-blue-500 to-indigo-600",
        tools: [
            { name: "JPG to Word", href: "/jpg-to-word", icon: FileText },
            { name: "PDF to Text", href: "/pdf-to-text", icon: FileText },
            { name: "PDF to Word", href: "/pdf-to-word", icon: FileText },
            { name: "Text to PDF", href: "/text-to-pdf", icon: FileText },
            { name: "Text to Word", href: "/text-to-word", icon: FileText },
            { name: "Word to PDF", href: "/word-to-pdf", icon: FileText },
            { name: "HTML to PDF", href: "/html-to-pdf", icon: FileText },
            { name: "PDF to HTML", href: "/pdf-to-html", icon: FileText },
        ]
    },
    {
        title: "Spreadsheet Tools",
        icon: Table,
        description: "Extract data from tables and convert spreadsheet formats.",
        color: "from-emerald-500 to-teal-600",
        tools: [
            { name: "JPG to Excel", href: "/jpg-to-excel", icon: Table },
            { name: "PDF to Excel", href: "/pdf-to-excel", icon: Table },
            { name: "PDF to CSV", href: "/pdf-to-csv", icon: Table },
            { name: "Excel to JPG", href: "/excel-to-jpg", icon: Table },
        ]
    },
    {
        title: "Image Tools",
        icon: ImageIcon,
        description: "Enhance, translate, and manipulate images and PDFs.",
        color: "from-purple-500 to-fuchsia-600",
        tools: [
            { name: "Invert Image", href: "/invert-image", icon: ImageIcon },
            { name: "Text to Image", href: "/text-to-image", icon: ImageIcon },
            { name: "Image Translator", href: "/image-translator", icon: ImageIcon },
            { name: "Image to PDF", href: "/image-to-pdf", icon: ImageIcon },
            { name: "PDF to JPG", href: "/pdf-to-jpg", icon: ImageIcon },
            { name: "Word to JPG", href: "/word-to-jpg", icon: ImageIcon },
            { name: "Merge PDF", href: "/merge-pdf", icon: FileStack },
        ]
    },
    {
        title: "Scan & Code",
        icon: ScanBarcode,
        description: "Generate and scan QR codes and barcodes instantly.",
        color: "from-amber-500 to-orange-600",
        tools: [
            { name: "QR Scanner", href: "/qr-scanner", icon: ScanBarcode },
            { name: "QR Generator", href: "/qr-generator", icon: ScanBarcode },
            { name: "Barcode Scanner", href: "/barcode-scanner", icon: ScanBarcode },
        ]
    },
];

export default function Home() {
    const [searchQuery, setSearchQuery] = useState("");

    const filteredCategories = categories.map(category => ({
        ...category,
        tools: category.tools.filter(tool =>
            tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            category.title.toLowerCase().includes(searchQuery.toLowerCase())
        )
    })).filter(category => category.tools.length > 0);

    return (
        <div className="min-h-screen pb-20">
            {/* Hero Section */}
            <section className="relative overflow-hidden pt-12 pb-20 px-6 text-center">
                {/* Background Decor */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-blue-600/10 blur-[120px] rounded-full -z-10 pointer-events-none" />
                <div className="absolute top-0 left-1/4 w-[400px] h-[400px] bg-indigo-600/10 blur-[100px] rounded-full -z-10 pointer-events-none" />
                <div className="absolute inset-0 bg-gradient-to-b from-slate-950/0 via-slate-950/20 to-slate-950 pointer-events-none" />

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="relative z-10 max-w-4xl mx-auto space-y-6"
                >
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium">
                        <Sparkles className="h-4 w-4" />
                        <span>AI-Powered Document Intelligence</span>
                    </div>

                    <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white">
                        Master Your <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-400 to-cyan-400 animate-gradient">
                            Documents & Data
                        </span>
                    </h1>

                    <p className="text-lg text-slate-400 max-w-2xl mx-auto">
                        A complete suite of 20+ tools to convert, extract, and manipulate documents, images, and spreadsheets with ease.
                    </p>

                    {/* Search Bar */}
                    <div className="max-w-md mx-auto mt-8 relative">
                        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                            <Search className="h-5 w-5 text-slate-500" />
                        </div>
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            placeholder="Find a tool (e.g., 'PDF to Excel', 'QR Code')..."
                            className="w-full pl-11 pr-4 py-4 bg-slate-900/50 border border-slate-700 rounded-2xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all shadow-xl backdrop-blur-sm"
                        />
                    </div>
                </motion.div>
            </section>

            {/* Categories Grid */}
            <div className="max-w-7xl mx-auto px-6 space-y-16">
                {filteredCategories.length > 0 ? (
                    filteredCategories.map((category, idx) => (
                        <motion.div
                            key={category.title}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: idx * 0.1 }}
                            className="space-y-8"
                        >
                            <div className="flex items-center gap-4">
                                <div className={clsx("p-3 rounded-xl bg-gradient-to-br shadow-lg text-white", category.color)}>
                                    <category.icon className="h-6 w-6" />
                                </div>
                                <div>
                                    <h2 className="text-2xl font-bold text-slate-200">{category.title}</h2>
                                    <p className="text-slate-400">{category.description}</p>
                                </div>
                                <div className="ml-auto px-3 py-1 rounded-full bg-slate-800/50 border border-slate-700 text-xs text-slate-400 font-mono">
                                    {category.tools.length} TOOLS
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                                {category.tools.map((tool) => (
                                    <Link key={tool.href} href={tool.href} className="group">
                                        <div className="h-full p-5 glass-card rounded-xl border border-slate-800/50 hover:border-blue-500/30 transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/10 hover:-translate-y-1 flex flex-col relative overflow-hidden">

                                            <div className="flex items-center justify-between mb-4">
                                                <div className="p-2 rounded-lg bg-slate-800/50 text-slate-300 group-hover:bg-blue-500/20 group-hover:text-blue-400 transition-colors">
                                                    <tool.icon className="h-5 w-5" />
                                                </div>
                                                <ArrowRight className="h-4 w-4 text-slate-600 group-hover:text-blue-400 -translate-x-2 opacity-0 group-hover:translate-x-0 group-hover:opacity-100 transition-all duration-300" />
                                            </div>

                                            <h3 className="font-semibold text-slate-200 group-hover:text-blue-300 transition-colors mb-1">
                                                {tool.name}
                                            </h3>

                                            {/* Background gradient effect on hover */}
                                            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
                                        </div>
                                    </Link>
                                ))}
                            </div>
                        </motion.div>
                    ))
                ) : (
                    <div className="text-center py-20">
                        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-800/50 mb-6">
                            <Search className="h-8 w-8 text-slate-500" />
                        </div>
                        <h3 className="text-xl font-semibold text-slate-200">No tools found</h3>
                        <p className="text-slate-400 mt-2">Try searching for something else, like "PDF" or "Excel".</p>
                    </div>
                )}
            </div>
        </div>
    );
}
