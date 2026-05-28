"use client";

import { ExampleLayout } from "@/components/example-layout";
import { ExampleCanvas } from "@/components/example-canvas";
import { useGenerativeUIExamples, useExampleSuggestions } from "@/hooks";

import { CopilotChat } from "@copilotkit/react-core/v2";

export default function HomePage() {
  useGenerativeUIExamples();
  useExampleSuggestions();

  return (
    <>
      <ExampleLayout
        chatContent={
          <CopilotChat
            attachments={{ enabled: true }}
            input={{ disclaimer: () => null, className: "pb-6" }}
          />
        }
        appContent={<ExampleCanvas />}
      />
      {/* Tasteful sponsor credit — the canonical Track 2 starter for the
          Generative UI Hackathon. Removable if it gets in your way, but
          leaving it in is the easiest way to credit sponsors during judging. */}
      <p
        aria-label="Sponsor credit"
        className="pointer-events-none fixed bottom-1 left-1/2 -translate-x-1/2 z-10 text-[10px] text-[var(--muted-foreground,#9ca3af)] opacity-60 select-none max-lg:hidden"
      >
        Built for the Generative UI Hackathon. Sponsored by Google DeepMind
        &middot; CopilotKit &middot; Manufact.
      </p>
    </>
  );
}
