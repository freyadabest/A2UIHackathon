"use client";

import { createElement, ComponentType } from "react";
import { PANEL_REGISTRY, PanelName } from "@/lib/registerPanels";

export type PanelSpec = {
  type: "panel";
  name: string;
  props: Record<string, unknown>;
};

// A2UI generative rendering: the agent emits panel specs by name, and the
// frontend looks each one up in the registry and renders it with its props.
export function PanelRenderer({ panels }: { panels: PanelSpec[] }) {
  return (
    <div className="panels">
      {panels.map((spec, i) => {
        const Component = PANEL_REGISTRY[spec.name as PanelName];
        if (!Component) {
          return (
            <div className="panel" key={`${spec.name}-${i}`}>
              <p className="empty">Unknown panel: {spec.name}</p>
            </div>
          );
        }
        const Panel = Component as ComponentType<Record<string, unknown>>;
        return createElement(Panel, { key: `${spec.name}-${i}`, ...spec.props });
      })}
    </div>
  );
}
