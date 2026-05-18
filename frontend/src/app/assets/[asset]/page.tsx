"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { fetchAssetThemes, fetchAssetArticles, MarketTheme, Article } from "@/lib/api";
import ThemeCard from "@/components/ThemeCard";
import ArticleCard from "@/components/ArticleCard";
import Disclaimer from "@/components/Disclaimer";
import { ArrowLeft } from "lucide-react";

export default function AssetDetailPage() {
  const params = useParams();
  const asset = decodeURIComponent(params.asset as string);
  const [themes, setThemes] = useState<MarketTheme[]>([]);
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<"themes" | "articles">("themes");

  useEffect(() => {
    Promise.all([fetchAssetThemes(asset), fetchAssetArticles(asset)])
      .then(([t, a]) => { setThemes(t); setArticles(a); setLoading(false); })
      .catch(() => setLoading(false));
  }, [asset]);

  if (loading) return (
    <div className="flex justify-center py-16">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400" />
    </div>
  );

  return (
    <div className="space-y-6">
      <Link href="/assets" className="inline-flex items-center gap-2 text-gray-400 hover:text-white text-sm">
        <ArrowLeft className="h-4 w-4" /> Back to Assets
      </Link>

      <div>
        <h1 className="text-2xl font-bold text-white">{asset}</h1>
        <p className="text-gray-400 text-sm mt-1">
          {themes.length} themes · {articles.length} articles
        </p>
      </div>

      <Disclaimer />

      <div className="flex gap-2 border-b border-gray-800 pb-0">
        {(["themes", "articles"] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-medium capitalize border-b-2 transition-colors ${
              tab === t ? "border-blue-500 text-blue-400" : "border-transparent text-gray-400 hover:text-white"
            }`}
          >
            {t} ({t === "themes" ? themes.length : articles.length})
          </button>
        ))}
      </div>

      {tab === "themes" ? (
        themes.length === 0 ? (
          <Empty />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {themes.map((t) => <ThemeCard key={t.id} theme={t} />)}
          </div>
        )
      ) : (
        articles.length === 0 ? <Empty /> : (
          <div className="space-y-3">
            {articles.map((a) => <ArticleCard key={a.id} article={a} />)}
          </div>
        )
      )}
    </div>
  );
}

function Empty() {
  return (
    <div className="bg-gray-800/50 border border-dashed border-gray-700 rounded-lg p-12 text-center">
      <p className="text-gray-500">No data available for this asset yet.</p>
    </div>
  );
}
