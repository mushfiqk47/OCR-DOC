"use client";

import { useCallback, useState } from "react";
import { useDropzone, FileRejection } from "react-dropzone";
import { UploadCloud, File, X, AlertCircle, Files } from "lucide-react";
import clsx from "clsx";
import { motion, AnimatePresence } from "framer-motion";

interface FileUploaderProps {
    onFileSelect: (file: File | File[]) => void;
    accept?: Record<string, string[]>;
    multiple?: boolean;
    maxSize?: number; // in bytes
}

export default function FileUploader({
    onFileSelect,
    accept = {
        "image/*": [".jpeg", ".jpg", ".png"],
        "application/pdf": [".pdf"],
    },
    multiple = false,
    maxSize = 50 * 1024 * 1024, // 50MB
}: FileUploaderProps) {
    // We'll store an array of files even if single mode, for simpler rendering logic
    const [files, setFiles] = useState<File[]>([]);
    const [error, setError] = useState<string | null>(null);

    const onDrop = useCallback(
        (acceptedFiles: File[], fileRejections: FileRejection[]) => {
            if (fileRejections.length > 0) {
                const rejection = fileRejections[0];
                if (rejection.errors[0].code === "file-too-large") {
                    setError("File is too large. Max size is 50MB.");
                } else {
                    setError(rejection.errors[0].message);
                }
                return;
            }

            if (acceptedFiles.length > 0) {
                setError(null);

                if (multiple) {
                    const newFiles = [...files, ...acceptedFiles];
                    setFiles(newFiles);
                    onFileSelect(newFiles);
                } else {
                    // Single mode: replace existing
                    const selectedFile = acceptedFiles[0];
                    setFiles([selectedFile]);
                    onFileSelect(selectedFile);
                }
            }
        },
        [onFileSelect, multiple, files]
    );

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept,
        maxSize,
        multiple,
    });

    const removeFile = (e: React.MouseEvent, index: number) => {
        e.stopPropagation();
        const newFiles = files.filter((_, i) => i !== index);
        setFiles(newFiles);
        onFileSelect(multiple ? newFiles : newFiles[0] || []); // Pass empty or undefined if cleared
    };

    return (
        <div className="w-full space-y-4">
            <div
                {...getRootProps()}
                className={clsx(
                    "relative flex flex-col items-center justify-center rounded-2xl border-2 border-dashed transition-all duration-300 cursor-pointer min-h-[240px] overflow-hidden group",
                    isDragActive
                        ? "border-indigo-500 bg-indigo-500/10"
                        : "border-slate-700 bg-slate-900/30 hover:border-indigo-400 hover:bg-slate-800/50",
                    error ? "border-red-500/50 bg-red-500/5" : ""
                )}
            >
                <input {...getInputProps()} />

                {/* Background Gradient Animation */}
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 via-transparent to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />

                <div className="flex flex-col items-center justify-center gap-4 text-center z-10 p-8">
                    <div className={clsx(
                        "p-4 rounded-full transition-all duration-300 shadow-xl",
                        isDragActive ? "bg-indigo-500 text-white scale-110" : "bg-slate-800 text-indigo-400 group-hover:bg-indigo-500 group-hover:text-white"
                    )}>
                        {multiple ? <Files className="h-8 w-8" /> : <UploadCloud className="h-8 w-8" />}
                    </div>
                    <div>
                        <p className="text-lg font-semibold text-slate-200">
                            {isDragActive ? "Drop files here" : (multiple ? "Drag & drop files here" : "Drag & drop a file here")}
                        </p>
                        <p className="text-sm text-slate-400 mt-1">
                            or click to select {multiple ? "files" : "a file"}
                        </p>
                    </div>
                </div>
            </div>

            {/* Error Message */}
            <AnimatePresence>
                {error && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        exit={{ opacity: 0, height: 0 }}
                        className="flex items-center gap-2 text-sm text-red-400 bg-red-500/10 border border-red-500/20 p-3 rounded-lg"
                    >
                        <AlertCircle className="h-4 w-4 shrink-0" />
                        <span>{error}</span>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* File List */}
            <AnimatePresence>
                {files.length > 0 && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-2"
                    >
                        {files.map((file, index) => (
                            <motion.div
                                key={`${file.name}-${index}`}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                                className="flex items-center gap-4 p-3 rounded-xl bg-slate-800/50 border border-slate-700/50 hover:bg-slate-800 transition-colors group/item"
                            >
                                <div className="h-10 w-10 rounded-lg bg-indigo-500/20 flex items-center justify-center shrink-0">
                                    <File className="h-5 w-5 text-indigo-400" />
                                </div>
                                <div className="flex flex-col flex-1 min-w-0">
                                    <span className="text-sm font-medium text-slate-200 truncate">
                                        {file.name}
                                    </span>
                                    <span className="text-xs text-slate-400">
                                        {(file.size / 1024 / 1024).toFixed(2)} MB
                                    </span>
                                </div>
                                <button
                                    onClick={(e) => removeFile(e, index)}
                                    className="p-2 rounded-full hover:bg-slate-700 transition-colors"
                                >
                                    <X className="h-4 w-4 text-slate-400 hover:text-red-400" />
                                </button>
                            </motion.div>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
