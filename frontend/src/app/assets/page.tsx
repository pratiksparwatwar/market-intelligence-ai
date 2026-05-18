"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchAssets, AssetSummary } from "@/lib/api";
import SentimentBadge from "@/components/SentimentBadge";
import { BarChart2 } from "lucide-react";

const ASSET_ICONS: Record<string, string> = {
  "Indian equity market": "📈",
  "Gold": "🥇",
  "Real estate": "🏠",
  "Crude oil": "🛢️",
  "USD/INR": "💱",
  "Bitcoin": "₿",
  "Global markets": "🌐",
};

export default function AssetsPage() {
  const [assets, setAssets] = useState<AssetSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAssets().then((d) => { setAssets(d); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return (
    <div className="flex justify-center py-16">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400" />
    </div>
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Asset Watch</h1>
        <p className="text-gray-400 text-sm mt-1">Market intelligence grouped by asset category</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {assets.map((a) => (
          <Link key={a.asset} href={`/assets/${encodeURIComponent(a.asset)}`}>
            <div className="bg-gray-800 border border-gray-700 rounded-xl p-5 hover:border-blue-500/50 transition-all cursor-pointer h-full">
              <div className="flex items-center gap-3 mb-3">
                <span className="text-2xl">{ASSET_ICONS[a.asset] ?? "📊"}</span>
                <h3 className="text-white font-semibold text-sm leading-tight">{a.asset}</h3>
              </div>

              {a.latest_sentiment ? (
                <SentimentBadge sentiment={a.latest_sentiment} />
              ) : (
                <span className="text-xs text-gray-500">No intelligence yet</span>
              )}

              <div className="mt-3 flex gap-4 text-xs text-gray-400">
                <span><strong className="text-gray-200">{a.theme_count}</strong> themes</span>
                <span><strong className="text-gray-200">{a.article_count}</strong> articles</span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
