"use client";

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// LEGACY shell header (PortKit-era) — NOT Seam #2, and not mounted by
// any live route. The pdf-analyst default demo's chrome (the live Seam
// #2) is src/components/pdf-analyst/Brand.tsx — see HACKATHON.md §2.
// This wrapper is kept for the archived PortKit example; don't wire it
// into the pdf-analyst pages unless you mean to.
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import type { ReactNode } from "react";
import { BackgroundBlurCircles } from "./BackgroundBlurCircles";
import { ModeToggle } from "./ModeToggle";

export interface BrandFrameProps {
  /** Product name shown in the header. Default: "CopilotKit". */
  productName?: string;
  /** Path (in /public) or absolute URL of the logo mark. */
  logoSrc?: string;
  /** Optional accent color (CSS color). Falls back to var(--border-default). */
  accentColor?: string;
  /** The app content beneath the header. */
  children?: ReactNode;
}

/**
 * BrandFrame — minimal header wrapper for the hackathon shell.
 *
 * Wraps the app in the signature CopilotKit frosted-glass backdrop
 * (BackgroundBlurCircles) and renders a lightweight header with the
 * product name, logo, and a ModeToggle in the trailing slot.
 *
 * Real hackathon teams can replace the contents while keeping the
 * shape — swap the logo, product name, or accent color via props.
 * Keep it shallow: the page layout (src/components/example-layout)
 * handles the chat / app split below this header.
 */
export function BrandFrame({
  productName = "CopilotKit",
  logoSrc = "/copilotkit-logo-mark.svg",
  accentColor,
  children,
}: BrandFrameProps) {
  return (
    <div className="relative flex flex-col h-full">
      <BackgroundBlurCircles />
      <header
        className="relative z-10 flex items-center gap-2 px-6 py-4 border-b"
        style={{
          borderColor:
            accentColor ?? "var(--border-default, var(--border, #dbdbe5))",
        }}
      >
        {logoSrc ? (
          <img src={logoSrc} alt={productName} className="h-7" />
        ) : null}
        <span className="font-light text-lg">{productName}</span>
        <div className="ml-auto">
          <ModeToggle />
        </div>
      </header>
      <div className="relative z-10 flex-1 min-h-0">{children}</div>
    </div>
  );
}
