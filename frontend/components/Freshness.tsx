import type { DataFreshness } from "@/lib/types";
import { DataFreshnessCard } from "./DataFreshnessCard";

export function Freshness({ freshness }: { freshness: DataFreshness }) {
  return <DataFreshnessCard freshness={freshness} />;
}
