const riskConfig = {
  low: { label: "Low Risk", className: "bg-green-500/20 text-green-400 border border-green-500/30" },
  medium: { label: "Medium Risk", className: "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30" },
  high: { label: "High Risk", className: "bg-red-500/20 text-red-400 border border-red-500/30" },
};

export default function RiskBadge({ risk }: { risk: string }) {
  const config = riskConfig[risk as keyof typeof riskConfig] ?? riskConfig.medium;
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${config.className}`}>
      {config.label}
    </span>
  );
}
