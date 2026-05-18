import Link from "next/link";
import { formatDistanceToNow } from "date-fns";
import { MarketTheme } from "@/lib/api";
import SentimentBadge from "./SentimentBadge";
import RiskBadge from "./RiskBadge";
import ConfidenceBadge from "./ConfidenceBadge";

export default function ThemeCard({ theme }: { theme: MarketTheme }) {
  return (
    <Link href={`/themes/${theme.id}`}>
      <div className="bg-gray-800 border border-gray-700 rounded-xl p-5 hover:border-blue-500/50 hover:bg-gray-800/80 transition-all cursor-pointer h-full flex flex-col gap-3">
        <div className="flex items-start justify-between gap-2">
          <h3 className="text-white font-semibold text-base leading-tight">{theme.theme_title}</h3>
        </div>

        <div className="flex flex-wrap gap-1.5">
          <SentimentBadge sentiment={theme.sentiment} />
          <RiskBadge risk={theme.risk_level} />
        </div>

        <p className="text-gray-400 text-sm leading-relaxed line-clamp-3">{theme.short_summary}</p>

        <ConfidenceBadge score={theme.confidence_score} />

        {theme.affected_assets.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {theme.affected_assets.map((a) => (
              <span key={a} className="text-xs bg-blue-900/40 text-blue-300 border border-blue-800/40 px-2 py-0.5 rounded">
                {a}
              </span>
            ))}
          </div>
        )}

        {theme.affected_sectors.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {theme.affected_sectors.map((s) => (
              <span key={s} className="text-xs bg-purple-900/40 text-purple-300 border border-purple-800/40 px-2 py-0.5 rounded">
                {s}
              </span>
            ))}
          </div>
        )}

        <div className="text-xs text-gray-500 mt-auto">
          {formatDistanceToNow(new Date(theme.generated_at), { addSuffix: true })}
          {" · "}{theme.supporting_article_ids.length} source{theme.supporting_article_ids.length !== 1 ? "s" : ""}
        </div>
      </div>
    </Link>
  );
}
