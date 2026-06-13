import { CompetitorTable } from "@/components/panels/CompetitorTable";
import { MarketSummary } from "@/components/panels/MarketSummary";
import { RatingsChart } from "@/components/panels/RatingsChart";

// Maps an A2UI panel name (emitted by the agent) to a React component.
// Extend this as new panels are added (SentimentBoard, OpportunityVerdict, ...).
export const PANEL_REGISTRY = {
  MarketSummary,
  RatingsChart,
  CompetitorTable,
} as const;

export type PanelName = keyof typeof PANEL_REGISTRY;
