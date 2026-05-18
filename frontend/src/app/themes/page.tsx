"use client";
import { useEffect, useState } from "react";
import { fetchThemes, MarketTheme } from "@/lib/api";
import ThemeCard from "@/components/ThemeCard";
import Disclaimer from "@/components/Disclaimer";

const SENTIMENTS = ["", "bullish", "bearish", "neutral", "mixed"];
const RISKS = ["", "low", "medium", "high"];

export default function ThemesPage() {
  const [themes, setThemes] = useState<MarketTheme[]>([]);
  const [loading, setLoading] = useState(true);
  const [sentiment, setSentiment] = useState("");
  const [risk, setRisk] = useState("");

  useEffect(() => {
    setLoading(true);
    const params: Record<string, string> = {};
    if (sentiment) params.sentiment = sentiment;
    if (risk) params.risk_level = risk;
    fetchThemes(params).then((d) => { setThemes(d); setLoading(false); }).catch(() => setLoading(false));
  }, [sentiment, risk]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Market Themes</h1>
        <p className="text-gray-400 text-sm mt-1">AI-identified themes from latest market news</p>
      </div>

      <Disclaimer />

      <div className="flex flex-wrap gap-3">
        <div>
          <label className="text-xs text-gray-400 block mb-1">Sentiment</label>
          <select
            value={sentiment}
            onChange={(e) => setSentiment(e.target.value)}
            className="bg-gray-800 border border-gray-700 text-gray-200 text-sm rounded px-3 py-1.5"
          >
            {SENTIMENTS.map((s) => <option key={s} value={s}>{s || "All"}</option>)}
          </select>
        </div>
        <div>
          <label className="text-xs text-gray-400 block mb-1">Risk Level</label>
          <select
            value={risk}
            onChange={(e) => setRisk(e.target.value)}
            className="bg-gray-800 border border-gray-700 text-gray-200 text-sm rounded px-3 py-1.5"
          >
            {RISKS.map((r) => <option key={r} value={r}>{r || "All"}</option>)}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-16">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400" />
        </div>
      ) : themes.length === 0 ? (
        <div className="bg-gray-800/50 border border-dashed border-gray-700 rounded-lg p-12 text-center">
          <p className="text-gray-500">No themes found. Try adjusting filters or generate themes from the Admin panel.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {themes.map((t) => <ThemeCard key={t.id} theme={t} />)}
        </div>
      )}
    </div>
  );
}
