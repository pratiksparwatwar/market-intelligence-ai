"use client";
import { useState } from "react";
import { adminFetchNews, adminGenerateThemes, adminClearData } from "@/lib/api";
import { RefreshCw, Cpu, Trash2, CheckCircle, XCircle } from "lucide-react";

interface ActionLog {
  type: "success" | "error";
  message: string;
  count?: number;
  time: string;
}

export default function AdminPage() {
  const [logs, setLogs] = useState<ActionLog[]>([]);
  const [loading, setLoading] = useState<string | null>(null);

  const run = async (action: string, fn: () => Promise<{ status: string; message: string; count?: number }>) => {
    setLoading(action);
    try {
      const result = await fn();
      setLogs((prev) => [{
        type: result.status === "success" ? "success" : "error",
        message: result.message,
        count: result.count,
        time: new Date().toLocaleTimeString(),
      }, ...prev]);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Request failed";
      setLogs((prev) => [{ type: "error", message: msg, time: new Date().toLocaleTimeString() }, ...prev]);
    } finally {
      setLoading(null);
    }
  };

  const actions = [
    {
      key: "fetch",
      label: "Fetch News",
      description: "Fetch latest articles from all configured RSS sources and store them in the database.",
      icon: RefreshCw,
      color: "blue",
      fn: adminFetchNews,
    },
    {
      key: "generate",
      label: "Generate Themes",
      description: "Run the AI pipeline on the latest 50 articles to identify and generate market themes.",
      icon: Cpu,
      color: "green",
      fn: adminGenerateThemes,
    },
    {
      key: "clear",
      label: "Clear All Data",
      description: "Delete all articles and themes from the database. Use to reset test data.",
      icon: Trash2,
      color: "red",
      fn: adminClearData,
      confirm: true,
    },
  ];

  const colorMap: Record<string, string> = {
    blue: "bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800",
    green: "bg-green-600 hover:bg-green-700 disabled:bg-green-800",
    red: "bg-red-600 hover:bg-red-700 disabled:bg-red-800",
  };

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold text-white">Admin Panel</h1>
        <p className="text-gray-400 text-sm mt-1">Manually trigger pipeline steps</p>
      </div>

      <div className="bg-amber-900/20 border border-amber-700/40 rounded-lg p-4 text-sm text-amber-300">
        This admin panel is for development and manual testing. In production, trigger pipelines via scheduled jobs or secure endpoints.
      </div>

      <div className="space-y-4">
        {actions.map(({ key, label, description, icon: Icon, color, fn, confirm }) => (
          <div key={key} className="bg-gray-800 border border-gray-700 rounded-xl p-5 flex items-center justify-between gap-4">
            <div className="flex items-start gap-4">
              <div className={`p-2 rounded-lg bg-gray-700`}>
                <Icon className="h-5 w-5 text-gray-300" />
              </div>
              <div>
                <h3 className="text-white font-semibold text-sm">{label}</h3>
                <p className="text-gray-400 text-xs mt-0.5 max-w-md">{description}</p>
              </div>
            </div>
            <button
              disabled={!!loading}
              onClick={() => {
                if (confirm && !window.confirm(`Are you sure you want to ${label.toLowerCase()}?`)) return;
                run(key, fn);
              }}
              className={`shrink-0 px-4 py-2 rounded-lg text-white text-sm font-medium transition-colors ${colorMap[color]} flex items-center gap-2`}
            >
              {loading === key && <span className="animate-spin rounded-full h-3 w-3 border-b border-white" />}
              {label}
            </button>
          </div>
        ))}
      </div>

      {logs.length > 0 && (
        <div>
          <h2 className="text-white font-semibold mb-3">Activity Log</h2>
          <div className="space-y-2">
            {logs.map((log, i) => (
              <div
                key={i}
                className={`flex items-start gap-3 p-3 rounded-lg text-sm ${
                  log.type === "success" ? "bg-green-900/20 border border-green-800/40" : "bg-red-900/20 border border-red-800/40"
                }`}
              >
                {log.type === "success" ? (
                  <CheckCircle className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />
                ) : (
                  <XCircle className="h-4 w-4 text-red-400 mt-0.5 shrink-0" />
                )}
                <div className="flex-1">
                  <span className={log.type === "success" ? "text-green-300" : "text-red-300"}>
                    {log.message}
                  </span>
                  {log.count !== undefined && (
                    <span className="text-gray-400 ml-2">({log.count} items)</span>
                  )}
                </div>
                <span className="text-gray-500 text-xs shrink-0">{log.time}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
