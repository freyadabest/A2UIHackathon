import { CompetitorTable } from "@/components/panels/CompetitorTable";

// Maps an A2UI panel name (emitted by the agent) to a React component.
// Extend this as new panels are added (SentimentBoard, OpportunityVerdict, ...).
export const PANEL_REGISTRY = {
  CompetitorTable,
} as const;

export type PanelName = keyof typeof PANEL_REGISTRY;
