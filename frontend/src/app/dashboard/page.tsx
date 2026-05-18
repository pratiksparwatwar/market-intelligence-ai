"use client";
import { useEffect, useState } from "react";
import { fetchThemes, fetchArticles, fetchAssets, MarketTheme, Article, AssetSummary } from "@/lib/api";
import ThemeCard from "@/components/ThemeCard";
import ArticleCard from "@/components/ArticleCard";
import Disclaimer from "@/components/Disclaimer";
import SentimentBadge from "@/components/SentimentBadge";
import RiskBadge from "@/components/RiskBadge";
import { TrendingUp, AlertTriangle, BarChart2, Newspaper } from "lucide-react";

export default function Dashboard() {
  const [themes, setThemes] = useState<MarketTheme[]>([]);
  const [articles, setArticles] = useState<Article[]>([]);
  const [assets, setAssets] = useState<AssetSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetchThemes({ limit: "6" }),
      fetchArticles({ limit: "8" }),
      fetchAssets(),
    ]).then(([t, a, as]) => {
      setThemes(t);
      setArticles(a);
      setAssets(as);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const riskThemes = themes.filter((t) => t.risk_level === "high");
  const sectorMap: Record<string, MarketTheme[]> = {};
  themes.forEach((t) => {
    t.affected_sectors.forEach((s) => {
      if (!sectorMap[s]) sectorMap[s] = [];
      sectorMap[s].push(t);
    });
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-white">Market Intelligence Dashboard</h1>
        <p className="text-gray-400 text-sm mt-1">AI-generated market themes, risk signals, and sector narratives</p>
      </div>

      <Disclaimer />

      {/* Today's Market Themes */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="h-5 w-5 text-blue-400" />
          <h2 className="text-lg font-semibold text-white">Today&apos;s Market Themes</h2>
          <span className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded">{themes.length}</span>
        </div>
        {themes.length === 0 ? (
          <EmptyState message="No themes generated yet. Use the Admin panel to generate themes." />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {themes.map((t) => <ThemeCard key={t.id} theme={t} />)}
          </div>
        )}
      </section>

      {/* Top Risk Signals */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <AlertTriangle className="h-5 w-5 text-red-400" />
          <h2 className="text-lg font-semibold text-white">Top Risk Signals</h2>
        </div>
        {riskThemes.length === 0 ? (
          <EmptyState message="No high-risk themes detected currently." />
        ) : (
          <div className="space-y-3">
            {riskThemes.map((t) => (
              <div key={t.id} className="bg-red-900/20 border border-red-800/40 rounded-lg p-4 flex items-start justify-between gap-4">
                <div>
                  <p className="text-white font-medium text-sm">{t.theme_title}</p>
                  <p className="text-gray-400 text-xs mt-1 line-clamp-2">{t.short_summary}</p>
                </div>
                <div className="flex flex-col gap-1 items-end shrink-0">
                  <SentimentBadge sentiment={t.sentiment} />
                  <RiskBadge risk={t.risk_level} />
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Asset Watch */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <BarChart2 className="h-5 w-5 text-purple-400" />
          <h2 className="text-lg font-semibold text-white">Asset Watch</h2>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-7 gap-3">
          {assets.map((a) => (
            <div key={a.asset} className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-center">
              <p className="text-white text-xs font-medium leading-tight">{a.asset}</p>
              {a.latest_sentiment ? (
                <div className="mt-2 flex justify-center">
                  <SentimentBadge sentiment={a.latest_sentiment} />
                </div>
              ) : (
                <p className="text-gray-500 text-xs mt-2">No data</p>
              )}
              <p className="text-gray-500 text-xs mt-1">{a.theme_count} themes</p>
            </div>
          ))}
        </div>
      </section>

      {/* Sector Narratives */}
      {Object.keys(sectorMap).length > 0 && (
        <section>
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="h-5 w-5 text-green-400" />
            <h2 className="text-lg font-semibold text-white">Sector Narratives</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {Object.entries(sectorMap).slice(0, 6).map(([sector, sThemes]) => (
              <div key={sector} className="bg-gray-800 border border-gray-700 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-purple-300 font-medium text-sm">{sector}</span>
                  <span className="text-xs text-gray-500">{sThemes.length} theme{sThemes.length !== 1 ? "s" : ""}</span>
                </div>
                {sThemes.slice(0, 2).map((t) => (
                  <div key={t.id} className="flex items-start gap-2 mt-1">
                    <SentimentBadge sentiment={t.sentiment} />
                    <p className="text-gray-400 text-xs line-clamp-1">{t.theme_title}</p>
                  </div>
                ))}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Latest Source Articles */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <Newspaper className="h-5 w-5 text-yellow-400" />
          <h2 className="text-lg font-semibold text-white">Latest Source Articles</h2>
        </div>
        {articles.length === 0 ? (
          <EmptyState message="No articles fetched yet. Use the Admin panel to fetch news." />
        ) : (
          <div className="space-y-3">
            {articles.map((a) => <ArticleCard key={a.id} article={a} />)}
          </div>
        )}
      </section>
    </div>
  );
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="bg-gray-800/50 border border-dashed border-gray-700 rounded-lg p-8 text-center">
      <p className="text-gray-500 text-sm">{message}</p>
    </div>
  );
}
