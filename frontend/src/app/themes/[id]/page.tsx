"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { fetchTheme, MarketThemeDetail } from "@/lib/api";
import SentimentBadge from "@/components/SentimentBadge";
import RiskBadge from "@/components/RiskBadge";
import ConfidenceBadge from "@/components/ConfidenceBadge";
import ArticleCard from "@/components/ArticleCard";
import Disclaimer from "@/components/Disclaimer";
import { ArrowLeft, ExternalLink } from "lucide-react";
import { format } from "date-fns";

export default function ThemeDetailPage() {
  const params = useParams();
  const [theme, setTheme] = useState<MarketThemeDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTheme(Number(params.id)).then((d) => { setTheme(d); setLoading(false); }).catch(() => setLoading(false));
  }, [params.id]);

  if (loading) return (
    <div className="flex justify-center py-16">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400" />
    </div>
  );

  if (!theme) return <div className="text-center text-gray-400 py-16">Theme not found.</div>;

  return (
    <div className="space-y-6 max-w-4xl">
      <Link href="/themes" className="inline-flex items-center gap-2 text-gray-400 hover:text-white text-sm">
        <ArrowLeft className="h-4 w-4" /> Back to Themes
      </Link>

      <div className="bg-gray-800 border border-gray-700 rounded-xl p-6 space-y-4">
        <div className="flex flex-wrap items-center gap-2">
          <SentimentBadge sentiment={theme.sentiment} />
          <RiskBadge risk={theme.risk_level} />
          <span className="text-xs text-gray-500 ml-auto">
            Generated {format(new Date(theme.generated_at), "MMM d, yyyy HH:mm")}
          </span>
        </div>

        <h1 className="text-2xl font-bold text-white">{theme.theme_title}</h1>

        <ConfidenceBadge score={theme.confidence_score} />

        <div className="space-y-4 pt-2">
          <div>
            <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Summary</h3>
            <p className="text-gray-200 text-sm leading-relaxed">{theme.short_summary}</p>
          </div>
          <div>
            <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Why It Matters</h3>
            <p className="text-gray-200 text-sm leading-relaxed">{theme.why_it_matters}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          {theme.affected_assets.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Affected Assets</h3>
              <div className="flex flex-wrap gap-1">
                {theme.affected_assets.map((a) => (
                  <span key={a} className="text-xs bg-blue-900/40 text-blue-300 border border-blue-800/40 px-2 py-0.5 rounded">{a}</span>
                ))}
              </div>
            </div>
          )}
          {theme.affected_sectors.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Affected Sectors</h3>
              <div className="flex flex-wrap gap-1">
                {theme.affected_sectors.map((s) => (
                  <span key={s} className="text-xs bg-purple-900/40 text-purple-300 border border-purple-800/40 px-2 py-0.5 rounded">{s}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      <Disclaimer />

      {theme.supporting_articles.length > 0 && (
        <section>
          <h2 className="text-lg font-semibold text-white mb-4">
            Supporting Sources ({theme.supporting_articles.length})
          </h2>
          <div className="space-y-3">
            {theme.supporting_articles.map((a) => <ArticleCard key={a.id} article={a} />)}
          </div>
        </section>
      )}
    </div>
  );
}
