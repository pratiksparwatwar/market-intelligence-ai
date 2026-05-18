"use client";
import { useEffect, useState } from "react";
import { fetchArticles, Article } from "@/lib/api";
import ArticleCard from "@/components/ArticleCard";

const SOURCES = ["", "Moneycontrol", "Economic Times Markets", "Livemint Markets", "Yahoo Finance", "Investing.com", "RBI"];

export default function SourcesPage() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [source, setSource] = useState("");

  useEffect(() => {
    setLoading(true);
    const params: Record<string, string> = { limit: "100" };
    if (source) params.source = source;
    fetchArticles(params).then((d) => { setArticles(d); setLoading(false); }).catch(() => setLoading(false));
  }, [source]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Source Articles</h1>
        <p className="text-gray-400 text-sm mt-1">Latest ingested articles from all configured sources</p>
      </div>

      <div className="flex items-center gap-3">
        <label className="text-sm text-gray-400">Filter by source:</label>
        <select
          value={source}
          onChange={(e) => setSource(e.target.value)}
          className="bg-gray-800 border border-gray-700 text-gray-200 text-sm rounded px-3 py-1.5"
        >
          {SOURCES.map((s) => <option key={s} value={s}>{s || "All sources"}</option>)}
        </select>
        <span className="text-xs text-gray-500 ml-auto">{articles.length} articles</span>
      </div>

      {loading ? (
        <div className="flex justify-center py-16">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400" />
        </div>
      ) : articles.length === 0 ? (
        <div className="bg-gray-800/50 border border-dashed border-gray-700 rounded-lg p-12 text-center">
          <p className="text-gray-500">No articles yet. Use the Admin panel to fetch news.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {articles.map((a) => <ArticleCard key={a.id} article={a} />)}
        </div>
      )}
    </div>
  );
}
