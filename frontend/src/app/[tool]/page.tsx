
"use client";

import { use, useState } from "react";
import FileUploader from "@/components/FileUploader";
import LanguageSelector from "@/components/LanguageSelector";
import { Loader2, Download, AlertCircle, CheckCircle, ArrowLeft, Copy, FileText, RotateCcw } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import clsx from "clsx";

// --- Tool Configuration ---

type ToolConfig = {
    id: string;
    title: string;
    description: string;
    endpoint: string;
    accept?: Record<string, string[]>; // Optional for text input tools
    resultType: "file" | "text" | "image";
    outputExtension?: string;
    multiple?: boolean;
    inputMode: "file" | "text"; // New field to distinguish input type
    placeholder?: string; // For text input
    needsTargetLanguage?: boolean;
};

const TOOLS: Record<string, ToolConfig> = {
    // --- Group 1: Document Conversion ---
    "jpg-to-word": {
        id: "jpg-to-word",
        title: "JPG to Word",
        description: "Convert your images into editable Word documents.",
        endpoint: "/api/convert/jpg-to-word",
        accept: { "image/*": [".jpg", ".jpeg", ".png"] },
        resultType: "file",
        outputExtension: "docx",
        inputMode: "file"
    },
    "pdf-to-text": {
        id: "pdf-to-text",
        title: "PDF to Text",
        description: "Extract plain text from your PDF documents.",
        endpoint: "/api/convert/pdf-to-text",
        accept: { "application/pdf": [".pdf"] },
        resultType: "text",
        inputMode: "file"
    },
    "pdf-to-word": {
        id: "pdf-to-word",
        title: "PDF to Word",
        description: "Convert PDF documents to editable Word files.",
        endpoint: "/api/convert/pdf-to-word",
        accept: { "application/pdf": [".pdf"] },
        resultType: "file",
        outputExtension: "docx",
        inputMode: "file"
    },
    "text-to-pdf": {
        id: "text-to-pdf",
        title: "Text to PDF",
        description: "Create secure PDF documents from plain text.",
        endpoint: "/api/convert/text-to-pdf",
        resultType: "file",
        outputExtension: "pdf",
        inputMode: "text",
        placeholder: "Enter the text you want to convert to PDF..."
    },
    "text-to-word": {
        id: "text-to-word",
        title: "Text to Word",
        description: "Convert plain text content into Word documents.",
        endpoint: "/api/convert/text-to-word",
        resultType: "file",
        outputExtension: "docx",
        inputMode: "text",
        placeholder: "Type your text here to convert to Word..."
    },
    "word-to-pdf": {
        id: "word-to-pdf",
        title: "Word to PDF",
        description: "Convert Word documents to PDF format.",
        endpoint: "/api/convert/word-to-pdf",
        accept: { "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"] },
        resultType: "file",
        outputExtension: "pdf",
        inputMode: "file"
    },
    "html-to-pdf": {
        id: "html-to-pdf",
        title: "HTML to PDF",
        description: "Convert HTML files to PDF.",
        endpoint: "/api/convert/html-to-pdf",
        accept: { "text/html": [".html", ".htm"] },
        resultType: "file",
        outputExtension: "pdf",
        inputMode: "file"
    },
    "pdf-to-html": {
        id: "pdf-to-html",
        title: "PDF to HTML",
        description: "Convert PDF documents into HTML web pages.",
        endpoint: "/api/convert/pdf-to-html",
        accept: { "application/pdf": [".pdf"] },
        resultType: "file",
        outputExtension: "html",
        inputMode: "file"
    },
    "pdf-translator": {
        id: "pdf-translator",
        title: "PDF Translator",
        description: "Translate PDF documents to another language while preserving the original layout.",
        endpoint: "/api/convert/pdf-translator",
        accept: { "application/pdf": [".pdf"] },
        resultType: "file",
        outputExtension: "pdf",
        inputMode: "file",
        needsTargetLanguage: true
    },

    // --- Group 2: Spreadsheet Tools ---
    "jpg-to-excel": {
        id: "jpg-to-excel",
        title: "JPG to Excel",
        description: "Extract tabular data from JPG images to Excel.",
        endpoint: "/api/convert/jpg-to-excel",
        accept: { "image/*": [".jpg", ".jpeg", ".png"] },
        resultType: "file",
        outputExtension: "xlsx",
        inputMode: "file"
    },
    "pdf-to-excel": {
        id: "pdf-to-excel",
        title: "PDF to Excel",
        description: "Convert PDF tables into Excel spreadsheets.",
        endpoint: "/api/convert/pdf-to-excel",
        accept: { "application/pdf": [".pdf"] },
        resultType: "file",
        outputExtension: "xlsx",
        inputMode: "file"
    },
    "pdf-to-csv": {
        id: "pdf-to-csv",
        title: "PDF to CSV",
        description: "Extract PDF data into comma-separated values.",
        endpoint: "/api/convert/pdf-to-csv",
        accept: { "application/pdf": [".pdf"] },
        resultType: "file",
        outputExtension: "csv",
        inputMode: "file"
    },
    "excel-to-jpg": {
        id: "excel-to-jpg",
        title: "Excel to JPG",
        description: "Convert Excel spreadsheets to image format.",
        endpoint: "/api/convert/excel-to-jpg",
        accept: { "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"] },
        resultType: "image",
        outputExtension: "jpg",
        inputMode: "file"
    },

    // --- Group 3: Image Tools ---
    "invert-image": {
        id: "invert-image",
        title: "Invert Image",
        description: "Invert the colors of your image.",
        endpoint: "/api/convert/invert-image",
        accept: { "image/*": [".jpg", ".jpeg", ".png"] },
        resultType: "image",
        inputMode: "file"
    },
    "text-to-image": {
        id: "text-to-image",
        title: "Text to Image",
        description: "Generate images from text descriptions.",
        endpoint: "/api/convert/text-to-image",
        resultType: "image",
        outputExtension: "png",
        inputMode: "text",
        placeholder: "Describe the image you want to generate..."
    },
    "image-translator": {
        id: "image-translator",
        title: "Image Translator",
        description: "Translate text within images instantly.",
        endpoint: "/api/convert/image-translator",
        accept: { "image/*": [".jpg", ".jpeg", ".png"] },
        resultType: "text", // Returns JSON {original, translated}
        inputMode: "file",
        needsTargetLanguage: true
    },
    "image-to-pdf": {
        id: "image-to-pdf",
        title: "Image to PDF",
        description: "Combine images into a single PDF.",
        endpoint: "/api/convert/images-to-pdf",
        accept: { "image/*": [".jpg", ".jpeg", ".png"] },
        resultType: "file",
        outputExtension: "pdf",
        multiple: true,
        inputMode: "file"
    },
    "pdf-to-jpg": {
        id: "pdf-to-jpg",
        title: "PDF to JPG",
        description: "Convert PDF pages into high-quality JPG images.",
        endpoint: "/api/convert/pdf-to-jpg",
        accept: { "application/pdf": [".pdf"] },
        resultType: "image",
        outputExtension: "jpg",
        inputMode: "file"
    },
    "word-to-jpg": {
        id: "word-to-jpg",
        title: "Word to JPG",
        description: "Convert Word document pages to JPG images.",
        endpoint: "/api/convert/word-to-jpg",
        accept: { "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"] },
        resultType: "image",
        outputExtension: "jpg",
        inputMode: "file"
    },
    "merge-pdf": {
        id: "merge-pdf",
        title: "Merge PDF",
        description: "Combine multiple PDF files into one document.",
        endpoint: "/api/convert/merge-pdf",
        accept: { "application/pdf": [".pdf"] },
        resultType: "file",
        outputExtension: "pdf",
        multiple: true,
        inputMode: "file"
    },

    // --- Group 4: Scan & Code ---
    "qr-scanner": {
        id: "qr-scanner",
        title: "QR Code Scanner",
        description: "Scan and decode QR codes instantly.",
        endpoint: "/api/convert/qr-scanner",
        accept: { "image/*": [".jpg", ".jpeg", ".png"] },
        resultType: "text",
        inputMode: "file"
    },
    "qr-generator": {
        id: "qr-generator",
        title: "QR Code Generator",
        description: "Create custom QR codes for URLs and text.",
        endpoint: "/api/convert/qr-generator",
        resultType: "image",
        outputExtension: "png",
        inputMode: "text",
        placeholder: "Enter URL or text to generate QR code..."
    },
    "barcode-scanner": {
        id: "barcode-scanner",
        title: "Barcode Scanner",
        description: "Scan standard barcodes from images.",
        endpoint: "/api/convert/barcode-scanner",
        accept: { "image/*": [".jpg", ".jpeg", ".png"] },
        resultType: "text",
        inputMode: "file"
    },
};


export default function ToolPage({ params }: { params: Promise<{ tool: string }> }) {
    const { tool } = use(params);
    const router = useRouter();

    const [status, setStatus] = useState<"idle" | "uploading" | "processing" | "success" | "error">("idle");
    const [resultUrl, setResultUrl] = useState<string | null>(null);
    const [resultText, setResultText] = useState<string | null>(null);
    const [translationResult, setTranslationResult] = useState<{ original: string, translated: string } | null>(null);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);
    const [textInput, setTextInput] = useState("");
    const [targetLanguage, setTargetLanguage] = useState("Spanish");

    const config = TOOLS[tool];

    const handleReset = () => {
        setStatus("idle");
        setResultUrl(null);
        setResultText(null);
        setTranslationResult(null);
        setErrorMsg(null);
        setTextInput("");
    };

    if (!config) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
                <AlertCircle className="h-16 w-16 text-slate-600" />
                <h1 className="text-2xl font-bold">Tool Not Found</h1>
                <p className="text-slate-400">The tool you requested ({tool}) is not available yet.</p>
                <Link href="/" className="text-blue-400 hover:underline flex items-center gap-2">
                    <ArrowLeft className="h-4 w-4" /> Back to Dashboard
                </Link>
            </div>
        );
    }

    const [copied, setCopied] = useState(false);

    const handleCopy = async (text: string) => {
        try {
            if (navigator.clipboard && window.isSecureContext) {
                await navigator.clipboard.writeText(text);
            } else {
                // Fallback for non-secure contexts or older browsers
                const textArea = document.createElement("textarea");
                textArea.value = text;
                textArea.style.position = "fixed";
                textArea.style.left = "-999999px";
                textArea.style.top = "-999999px";
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                document.execCommand('copy');
                textArea.remove();
            }
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    };

    const handleProcess = async (payload: File | File[] | string) => {
        setStatus("processing");
        setErrorMsg(null);
        setResultUrl(null);
        setResultText(null);
        setTranslationResult(null);

        const formData = new FormData();

        if (typeof payload === "string") {
            formData.append("text", payload);
        } else {
            const fileList = Array.isArray(payload) ? payload : [payload];
            fileList.forEach(f => {
                if (config.multiple) {
                    formData.append("files", f);
                } else {
                    formData.append("file", f);
                }
            });
        }

        if (config.needsTargetLanguage) {
            formData.append("target_language", targetLanguage);
        }

        try {
            const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
            const res = await fetch(`${API_BASE_URL}${config.endpoint}`, {
                method: "POST",
                body: formData,
            });

            if (!res.ok) {
                const errorData = await res.json().catch(() => ({ detail: "Unknown Error" }));
                throw new Error(errorData.detail || "Processing failed");
            }

            // Handle different result types
            if (config.id === "image-translator") {
                const data = await res.json();
                setTranslationResult({
                    original: data.original_text,
                    translated: data.translated_text
                });
                // Also set text for generic display if needed
                setResultText(data.translated_text);
            } else if (config.resultType === "text") {
                const data = await res.json();
                setResultText(data.text);
            } else {
                // Blob for file/image
                const blob = await res.blob();
                const url = URL.createObjectURL(blob);
                setResultUrl(url);
            }
            setStatus("success");

        } catch (e: any) {
            console.error(e);
            setErrorMsg(e.message);
            setStatus("error");
        }
    };

    return (
        <div className="space-y-8 max-w-5xl mx-auto">
            <div className="flex items-center gap-4 mb-8">
                <Link href="/" className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors">
                    <ArrowLeft className="h-5 w-5 text-slate-300" />
                </Link>
                <div>
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent capitalize">
                        {config.title}
                    </h1>
                    <p className="text-slate-400 mt-1">{config.description}</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Input Section */}
                <div className="glass-card p-8 rounded-2xl border border-white/5 space-y-6 h-fit">
                    <h2 className="text-xl font-semibold text-slate-200">Input</h2>

                    {config.needsTargetLanguage && (
                        <div className="mb-6">
                            <label className="block text-sm font-medium text-slate-400 mb-2">Target Language</label>
                            <LanguageSelector
                                value={targetLanguage}
                                onChange={(val) => setTargetLanguage(val)}
                            />
                        </div>
                    )}

                    {config.inputMode === "text" ? (
                        <div className="space-y-4">
                            <textarea
                                value={textInput}
                                onChange={(e) => setTextInput(e.target.value)}
                                placeholder={config.placeholder}
                                className="w-full h-48 bg-slate-950/50 border border-slate-700 rounded-xl p-4 text-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none resize-none placeholder:text-slate-600"
                            />
                            <button
                                onClick={() => handleProcess(textInput)}
                                disabled={!textInput.trim() || status === "processing"}
                                className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                            >
                                {status === "processing" ? <Loader2 className="animate-spin h-5 w-5" /> : <CheckCircle className="h-5 w-5" />}
                                {status === "processing" ? "Processing..." : "Convert Now"}
                            </button>
                        </div>
                    ) : (
                        <FileUploader
                            onFileSelect={(f) => handleProcess(f)}
                            accept={config.accept}
                            multiple={config.multiple}
                        />
                    )}

                    {status === "processing" && config.inputMode === "file" && (
                        <div className="flex flex-col items-center justify-center p-8 bg-slate-900/50 rounded-xl border border-slate-800 animate-pulse">
                            <Loader2 className="h-8 w-8 text-indigo-500 animate-spin mb-3" />
                            <p className="text-indigo-400 font-medium">Processing your files...</p>
                        </div>
                    )}

                    {status === "error" && (
                        <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl flex items-start gap-3">
                            <AlertCircle className="h-5 w-5 text-red-500 shrink-0 mt-0.5" />
                            <p className="text-red-400 text-sm">{errorMsg}</p>
                        </div>
                    )}
                </div>

                {/* Result Section */}
                <div className="glass-card p-8 rounded-2xl border border-white/5 flex flex-col items-center justify-center min-h-[400px] relative overflow-hidden">
                    {/* Background decorations */}
                    <div className="absolute top-0 right-0 p-32 bg-indigo-500/5 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none" />
                    <div className="absolute bottom-0 left-0 p-32 bg-cyan-500/5 rounded-full blur-3xl -ml-16 -mb-16 pointer-events-none" />

                    {status !== "idle" && (
                        <button
                            onClick={handleReset}
                            className="absolute top-6 right-6 p-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-white transition-all z-30 group backdrop-blur-md border border-white/10 shadow-lg"
                            title="Start Over"
                        >
                            <RotateCcw className="h-5 w-5 group-hover:rotate-[-45deg] transition-transform duration-300" />
                        </button>
                    )}

                    {status === "idle" || status === "processing" || status === "uploading" ? (
                        <div className="text-center text-slate-500 relative z-10">
                            <div className="w-20 h-20 rounded-full bg-slate-800/50 flex items-center justify-center mx-auto mb-6 border border-slate-700/50">
                                <Download className="h-10 w-10 opacity-40" />
                            </div>
                            <p className="text-lg font-medium text-slate-400">Result will appear here</p>
                            <p className="text-sm opacity-60 mt-1">Ready to process your request</p>
                        </div>
                    ) : (
                        <div className="w-full space-y-6 text-center animate-in fade-in zoom-in duration-300 relative z-10">

                            {/* Special Translation Result View */}
                            {translationResult && (
                                <div className="grid grid-cols-1 gap-4 text-left">
                                    <div className="space-y-2">
                                        <label className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Original</label>
                                        <div className="p-4 bg-slate-950/50 rounded-xl border border-slate-800 text-sm text-slate-300 max-h-40 overflow-y-auto">
                                            {translationResult.original}
                                        </div>
                                    </div>
                                    <div className="flex justify-center">
                                        <ArrowLeft className="rotate-[-90deg] text-slate-600" />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs uppercase tracking-wider text-emerald-500 font-semibold">Translated</label>
                                        <div className="p-4 bg-emerald-950/10 rounded-xl border border-emerald-500/20 text-sm text-emerald-300 max-h-60 overflow-y-auto">
                                            {translationResult.translated}
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Standard Text Result */}
                            {config.resultType === "text" && !translationResult && (
                                <div className="space-y-3 w-full">
                                    <div className="flex items-center justify-between">
                                        <h3 className="text-sm font-medium text-slate-400">Result Output</h3>
                                        <button
                                            onClick={() => handleCopy(resultText || "")}
                                            className={clsx(
                                                "text-xs flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all",
                                                copied ? "text-emerald-400 bg-emerald-500/10" : "text-indigo-400 hover:text-indigo-300 bg-indigo-500/5 hover:bg-indigo-500/10"
                                            )}
                                        >
                                            {copied ? <CheckCircle className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
                                            {copied ? "Copied!" : "Copy Text"}
                                        </button>
                                    </div>
                                    <div className="bg-slate-950 p-6 rounded-xl text-left font-mono text-sm text-slate-300 overflow-auto max-h-[500px] w-full border border-slate-800 shadow-inner group relative">
                                        <pre className="whitespace-pre-wrap leading-relaxed">{resultText}</pre>
                                    </div>
                                </div>
                            )}

                            {/* Image Result */}
                            {config.resultType === "image" && resultUrl && (
                                <div className="space-y-4">
                                    <div className="rounded-xl overflow-hidden border border-slate-700 shadow-2xl bg-slate-950">
                                        <img src={resultUrl} alt="Result" className="max-h-[300px] w-auto mx-auto object-contain" />
                                    </div>
                                </div>
                            )}

                            {/* Download Button */}
                            {(config.resultType === "file" || config.resultType === "image") && resultUrl && (
                                <div className="pt-4">
                                    <a
                                        href={resultUrl}
                                        download={`converted.${config.outputExtension || 'file'}`}
                                        className="inline-flex items-center gap-2 px-8 py-4 rounded-full bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white font-semibold transition-all shadow-lg shadow-indigo-500/25 transform hover:-translate-y-1"
                                    >
                                        <Download className="h-5 w-5" />
                                        Download {config.outputExtension?.toUpperCase()}
                                    </a>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

