"use client";

import {
    useReactTable,
    getCoreRowModel,
    getFilteredRowModel,
    flexRender,
    createColumnHelper,
} from "@tanstack/react-table";
import { useMemo, useState } from "react";
import { Download, Search } from "lucide-react";

interface DataGridProps {
    data: any[];
    downloadUrl?: string;
}

export default function DataGrid({ data, downloadUrl }: DataGridProps) {
    const columnHelper = createColumnHelper<any>();
    const [globalFilter, setGlobalFilter] = useState("");

    const columns = useMemo(() => {
        if (!data || data.length === 0) return [];
        // Auto-generate columns based on first row keys
        return Object.keys(data[0]).map((key) =>
            columnHelper.accessor(key, {
                header: () => <span className="font-semibold text-slate-300">{key}</span>,
                cell: (info) => info.getValue(),
            })
        );
    }, [data, columnHelper]);

    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
        getFilteredRowModel: getFilteredRowModel(),
        state: {
            globalFilter,
        },
        onGlobalFilterChange: setGlobalFilter,
    });

    if (!data || data.length === 0) {
        return (
            <div className="text-center p-8 text-slate-500 bg-slate-900/50 rounded-xl border border-dashed border-slate-800">
                No data to display.
            </div>
        );
    }

    return (
        <div className="space-y-4">
            <div className="flex flex-col sm:flex-row justify-between gap-4">
                {/* Search Bar */}
                <div className="relative w-full max-w-sm">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Search className="h-4 w-4 text-slate-500" />
                    </div>
                    <input
                        type="text"
                        value={globalFilter ?? ""}
                        onChange={(e) => setGlobalFilter(e.target.value)}
                        placeholder="Search data..."
                        className="w-full pl-10 pr-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors"
                    />
                </div>

                {downloadUrl && (
                    <a
                        href={`http://localhost:8000${downloadUrl}`}
                        download
                        className="flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-emerald-600 text-white font-medium hover:bg-emerald-700 transition-colors shadow-lg shadow-emerald-500/20 whitespace-nowrap"
                    >
                        <Download className="h-4 w-4" />
                        Download Excel
                    </a>
                )}
            </div>

            <div className="rounded-xl border border-slate-700 overflow-hidden bg-slate-900 shadow-xl">
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm text-slate-300">
                        <thead className="bg-slate-800 text-slate-200 uppercase text-xs">
                            {table.getHeaderGroups().map((headerGroup) => (
                                <tr key={headerGroup.id}>
                                    {headerGroup.headers.map((header) => (
                                        <th key={header.id} className="px-6 py-4 font-bold tracking-wider">
                                            {header.isPlaceholder
                                                ? null
                                                : flexRender(
                                                    header.column.columnDef.header,
                                                    header.getContext()
                                                )}
                                        </th>
                                    ))}
                                </tr>
                            ))}
                        </thead>
                        <tbody className="divide-y divide-slate-800">
                            {table.getRowModel().rows.map((row) => (
                                <tr key={row.id} className="hover:bg-slate-800/50 transition-colors">
                                    {row.getVisibleCells().map((cell) => (
                                        <td key={cell.id} className="px-6 py-4 whitespace-nowrap">
                                            {flexRender(cell.column.columnDef.cell, cell.getContext())}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <div className="bg-slate-800/50 px-6 py-3 border-t border-slate-800 text-xs text-slate-500">
                    Showing preview of first 5 rows
                </div>
            </div>
        </div>
    );
}
