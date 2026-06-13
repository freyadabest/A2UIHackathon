// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// CUSTOMIZATION SEAM #2 — Re-brand the shell
// See HACKATHON.md §2 for the full recipe.
//
// The pdf-analyst chrome: Logo, SiteNav (top nav), PageHeader (landing
// hero), WorkspaceHeader (the /fixed and /dynamic workspace bar). Swap the
// logo asset in public/brand/, rename the product, rewrite the hero copy.
// Brand tints come from src/app/(pdf)/pdf-analyst.css (Seam #1).
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import Link from "next/link";

/** Vantage AI wordmark — an ascending "vantage peak" mark + the one-word
 *  "VantageAI" logotype set in the display font (Sora). `size` is the cap
 *  height in px; the mark and type scale from it. */
export function Logo({ size = 28 }: { size?: number }) {
  const mark = Math.round(size * 1.18);
  return (
    <span
      className="inline-flex items-center gap-2.5 select-none"
      aria-label="VantageAI"
    >
      <svg
        width={mark}
        height={mark}
        viewBox="0 0 120 120"
        fill="none"
        aria-hidden
      >
        <defs>
          <linearGradient
            id="vantageMark"
            x1="10"
            y1="110"
            x2="110"
            y2="14"
            gradientUnits="userSpaceOnUse"
          >
            <stop stopColor="#f3b8cd" />
            <stop offset="0.5" stopColor="#f1cdb0" />
            <stop offset="1" stopColor="#e6a6c2" />
          </linearGradient>
        </defs>
        <path
          d="M14 98 L46 30 L66 64 L84 38 L106 70"
          stroke="url(#vantageMark)"
          strokeWidth="13"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <circle cx="106" cy="70" r="9.5" fill="url(#vantageMark)" />
      </svg>
      <span
        className="font-bold tracking-[-0.02em] leading-none"
        style={{
          fontFamily: "var(--font-display), var(--font-body)",
          fontSize: size,
        }}
      >
        <span style={{ color: "var(--ink)" }}>Vantage</span>
        <span
          className="bg-clip-text text-transparent"
          style={{ backgroundImage: "var(--brand-gradient)" }}
        >
          AI
        </span>
      </span>
    </span>
  );
}

export function SiteNav({
  active,
}: {
  active?: "home" | "fixed" | "dynamic" | "catalog";
}) {
  const links: Array<{ href: string; label: string; key: typeof active }> = [
    { href: "/", label: "Overview", key: "home" },
    { href: "/fixed", label: "Market scan", key: "fixed" },
    { href: "/catalog", label: "Catalog", key: "catalog" },
  ];
  return (
    <header className="shrink-0 border-b border-[var(--line)] bg-[var(--surface)]">
      <div className="max-w-[1480px] mx-auto px-5 h-14 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3">
          <Logo size={28} />
          <span className="hidden sm:inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full border border-[var(--line)] bg-[var(--surface-soft)] text-[10.5px] uppercase tracking-[0.12em] mono text-[var(--muted)]">
            <span className="w-1.5 h-1.5 rounded-full bg-[var(--lilac)]" />
            A2UI
          </span>
        </Link>
        <nav className="flex flex-1 items-center gap-2 ml-8">
          {links.map((l) => (
            <Link
              key={l.key}
              href={l.href}
              className={`flex-1 text-center px-3 py-1.5 rounded-lg text-[13.5px] transition ${
                active === l.key
                  ? "bg-[var(--surface-soft)] text-[var(--ink)] border border-[var(--line)]"
                  : "text-[var(--muted)] hover:text-[var(--ink)]"
              }`}
            >
              {l.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}

/** Used only on overview & catalog pages. never on demo pages where the
 *  whole viewport is workspace. Compact, no atmosphere, no gradient. */
export function PageHeader({
  eyebrow,
  title,
  subtitle,
  meta,
}: {
  eyebrow: string;
  title: React.ReactNode;
  subtitle: React.ReactNode;
  meta?: React.ReactNode;
}) {
  return (
    <section className="border-b border-[var(--line)] bg-[var(--bg)]">
      <div className="max-w-[1480px] mx-auto px-5 py-8">
        <div className="flex items-center gap-3 mb-3">
          <span className="mono text-[11px] uppercase tracking-[0.14em] text-[var(--muted-2)]">
            {eyebrow}
          </span>
          {meta}
        </div>
        <h1
          className="text-[34px] md:text-[48px] font-bold tracking-[-0.02em] leading-[1.05] text-[var(--ink)]"
          style={{ fontFamily: "var(--font-display), var(--font-body)" }}
        >
          {title}
        </h1>
        <p className="mt-4 text-[var(--muted)] max-w-3xl text-[17px] md:text-[18px] leading-relaxed">
          {subtitle}
        </p>
      </div>
    </section>
  );
}

/** Used by the demo pages. A thin one-row title strip. no hero, no gradient,
 *  no overflow. Sits between the nav and the workspace split. */
export function WorkspaceHeader({
  eyebrow,
  title,
  agentId,
  status,
}: {
  eyebrow: string;
  title: string;
  agentId: string;
  status?: React.ReactNode;
}) {
  return (
    <div className="shrink-0 border-b border-[var(--line)] bg-[var(--bg)]">
      <div className="max-w-[1480px] mx-auto px-5 py-3 flex items-center gap-4">
        <span className="mono text-[10.5px] uppercase tracking-[0.14em] text-[var(--muted-2)]">
          {eyebrow}
        </span>
        <span className="text-[14px] font-semibold tracking-tight text-[var(--ink)]">
          {title}
        </span>
        <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full border border-[var(--line)] bg-[var(--surface)] text-[10.5px] uppercase tracking-[0.12em] mono text-[var(--muted)]">
          <span className="w-1.5 h-1.5 rounded-full bg-[var(--lilac)]" />
          agent: {agentId}
        </span>
        <div className="ml-auto flex items-center gap-3">{status}</div>
      </div>
    </div>
  );
}
