export default function ConfidenceBadge({ score }: { score: number }) {
  const pct = Math.round(score);
  const color = pct >= 75 ? "bg-blue-500" : pct >= 50 ? "bg-yellow-500" : "bg-gray-500";

  return (
    <div className="flex items-center gap-2">
      <div className="w-24 bg-gray-700 rounded-full h-1.5">
        <div className={`${color} h-1.5 rounded-full`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs text-gray-400">{pct}% confidence</span>
    </div>
  );
}
