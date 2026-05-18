import { AlertTriangle } from "lucide-react";

export default function Disclaimer() {
  return (
    <div className="bg-amber-900/30 border border-amber-700/50 rounded-lg px-4 py-3 flex items-start gap-3 text-sm text-amber-200">
      <AlertTriangle className="h-4 w-4 mt-0.5 shrink-0 text-amber-400" />
      <p>
        <strong className="text-amber-300">Disclaimer:</strong> This platform provides market
        intelligence and educational insights only. It does not provide investment advice,
        buy/sell recommendations, or guaranteed predictions.
      </p>
    </div>
  );
}
