const sentimentConfig = {
  bullish: { label: "Bullish", className: "bg-green-500/20 text-green-400 border border-green-500/30" },
  bearish: { label: "Bearish", className: "bg-red-500/20 text-red-400 border border-red-500/30" },
  neutral: { label: "Neutral", className: "bg-gray-500/20 text-gray-400 border border-gray-500/30" },
  mixed: { label: "Mixed", className: "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30" },
};

export default function SentimentBadge({ sentiment }: { sentiment: string }) {
  const config = sentimentConfig[sentiment as keyof typeof sentimentConfig] ?? sentimentConfig.neutral;
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${config.className}`}>
      {config.label}
    </span>
  );
}
