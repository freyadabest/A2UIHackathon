"use client";

import { useState } from "react";
import {
  CopilotChat,
  useAgent,
  useConfigureSuggestions,
} from "@copilotkit/react-core/v2";
import { SiteNav } from "@/components/pdf-analyst/Brand";
import { SurfaceCanvas, CanvasEmptyState } from "@/components/pdf-analyst/SurfaceCanvas";
import { FilteredUserMessage } from "@/components/pdf-analyst/FilteredUserMessage";
import { FilteredAssistantMessage } from "@/components/pdf-analyst/FilteredAssistantMessage";
import { Split } from "@/components/pdf-analyst/Split";
import { extractPdfText } from "@/lib/pdf";

const AGENT_ID = "fixed_agent";

export default function FixedPage() {
  const { agent: _agent } = useAgent({ agentId: AGENT_ID });

  // Pre-canned example questions shown as clickable pills before the first
  // message. `title` is the pill label; `message` is what gets sent on click.
  useConfigureSuggestions({
    available: "before-first-message",
    consumerAgentId: AGENT_ID,
    suggestions: [
      {
        title: "Pilates studio in Shoreditch",
        message: "I want to open a Pilates studio in Shoreditch.",
      },
      {
        title: "Specialty coffee shop in Hackney",
        message: "I'm scoping a specialty coffee shop in Hackney.",
      },
      {
        title: "Boutique gym in Islington",
        message: "Map the competition for a boutique gym in Islington.",
      },
      {
        title: "Independent bookshop in Brighton",
        message: "I want to open an independent bookshop in Brighton.",
      },
    ],
  });

  const [loaded, setLoaded] = useState<{
    filename: string;
    pages: number;
    chars: number;
  } | null>(null);

  return (
    <div className="h-screen flex flex-col bg-[var(--bg)]">
      <SiteNav active="fixed" />

      <div className="flex-1 min-h-0 flex">
      <Split
        persistKey="fixed.split"
        initialLeftFraction={0.32}
        left={
          <div className="h-full flex flex-col copilot-chat-wrapper">
            {loaded && (
              <div className="shrink-0 px-4 py-2 border-b border-[var(--line)] flex items-center gap-2 bg-[color-mix(in_oklab,var(--mint)_8%,var(--surface))]">
                <span className="w-1.5 h-1.5 rounded-full bg-[#0d6b4f]" />
                <span className="mono text-[10.5px] uppercase tracking-[0.12em] text-[var(--ink)]">
                  loaded
                </span>
                <span className="text-[12.5px] font-medium text-[var(--ink)] truncate">
                  {loaded.filename}
                </span>
                <span className="text-[11px] text-[var(--ink)] ml-auto">
                  {loaded.pages} pg · {Math.round(loaded.chars / 1000)}k chars
                </span>
              </div>
            )}
            <div className="flex-1 min-h-0">
              <CopilotChat
                agentId={AGENT_ID}
                chatView={{
                  messageView: {
                    userMessage: FilteredUserMessage,
                    assistantMessage: FilteredAssistantMessage,
                  },
                }}
                attachments={{
                  enabled: true,
                  accept: "application/pdf",
                  maxSize: 20 * 1024 * 1024,
                  onUpload: async (file) => {
                    const { text, pages } = await extractPdfText(file);
                    setLoaded({
                      filename: file.name,
                      pages,
                      chars: text.length,
                    });
                    return {
                      type: "data",
                      value: text.slice(0, 60_000),
                      mimeType: "text/plain",
                      metadata: {
                        filename: file.name,
                        pages,
                        originalMime: "application/pdf",
                      },
                    };
                  },
                  onUploadFailed: (err) =>
                    console.warn("[pdf upload failed]", err),
                }}
                labels={{
                  chatInputPlaceholder:
                    "Describe an area + business, e.g. “Pilates studio in Shoreditch”…",
                  welcomeMessageText: "Who's already on your turf? Let's find out.",
                }}
              />
            </div>
          </div>
        }
        right={
          <SurfaceCanvas
            channel={AGENT_ID}
            emptyState={
              <CanvasEmptyState
                title="Canvas is empty"
                subtitle="Describe an area and the business you're scoping in the chat. Vantage AI searches the live web for competitors and paints a competitive-landscape dashboard into this canvas."
                hint={
                  <span className="mono text-[11px] uppercase tracking-[0.14em] text-[var(--ink)]">
                    try: “Pilates studio in Shoreditch”
                  </span>
                }
              />
            }
          />
        }
      />
      </div>
    </div>
  );
}
