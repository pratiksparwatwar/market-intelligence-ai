import { Article } from "@/lib/api";
import { ExternalLink } from "lucide-react";
import { formatDistanceToNow } from "date-fns";

export default function ArticleCard({ article }: { article: Article }) {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-4 flex flex-col gap-2">
      <div className="flex items-start justify-between gap-2">
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-white text-sm font-medium hover:text-blue-400 transition-colors leading-snug flex-1"
        >
          {article.title}
        </a>
        <a href={article.url} target="_blank" rel="noopener noreferrer" className="shrink-0 text-gray-500 hover:text-blue-400">
          <ExternalLink className="h-4 w-4" />
        </a>
      </div>

      {article.summary && (
        <p className="text-gray-400 text-xs leading-relaxed line-clamp-2">{article.summary}</p>
      )}

      <div className="flex flex-wrap items-center gap-2 mt-1">
        <span className="text-xs bg-gray-700 text-gray-300 px-2 py-0.5 rounded font-medium">
          {article.source}
        </span>
        {article.asset_tags.map((t) => (
          <span key={t} className="text-xs bg-blue-900/30 text-blue-400 px-1.5 py-0.5 rounded">
            {t}
          </span>
        ))}
        {article.sector_tags.map((t) => (
          <span key={t} className="text-xs bg-purple-900/30 text-purple-400 px-1.5 py-0.5 rounded">
            {t}
          </span>
        ))}
        <span className="text-xs text-gray-500 ml-auto">
          {article.published_at
            ? formatDistanceToNow(new Date(article.published_at), { addSuffix: true })
            : ""}
        </span>
      </div>
    </div>
  );
}
