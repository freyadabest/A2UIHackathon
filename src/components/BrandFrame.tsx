"use client";

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// CUSTOMIZATION SEAM #2 — Re-brand the shell
// See HACKATHON.md §2 for the full recipe.
// Pattern to copy: this file — swap the logo, product name, and
// accent colors. Use it as a thin header wrapper around the app
// shell. The default props mirror the inherited demo so you can
// drop it in without breaking anything.
//
// Don't touch:
//   - src/components/EnvelopeInspector.tsx (judging chrome)
//   - chat affordances in src/app/page.tsx
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import type { ReactNode } from "react";

export interface BrandFrameProps {
  /** Product name shown in the header. Default: "CopilotKit". */
  productName?: string;
  /** Path (in /public) or absolute URL of the logo mark. */
  logoSrc?: string;
  /** Optional accent color (CSS color). Falls back to var(--primary). */
  accentColor?: string;
  /** The app content beneath the header. */
  children?: ReactNode;
}

/**
 * BrandFrame — minimal header wrapper for the hackathon shell.
 *
 * This is a stub. Real hackathon teams will replace the contents with
 * their own brand chrome (product name, logo, tagline, accent bar).
 * Keep it shallow — the page layout (src/components/example-layout)
 * handles the chat/app split below this header.
 */
export function BrandFrame({
  productName = "CopilotKit",
  logoSrc = "/copilotkit-logo-mark.svg",
  accentColor,
  children,
}: BrandFrameProps) {
  const accentStyle = accentColor
    ? { borderColor: accentColor }
    : { borderColor: "var(--primary, #137fec)" };

  return (
    <div className="flex flex-col h-full">
      <header
        className="flex items-center gap-2 px-6 py-4 border-b-2"
        style={accentStyle}
      >
        {logoSrc ? (
          <img src={logoSrc} alt={productName} className="h-7" />
        ) : null}
        <span className="font-extrabold text-2xl">{productName}</span>
      </header>
      <div className="flex-1 min-h-0">{children}</div>
    </div>
  );
}
