import Link from "next/link";
import { SiteNav, PageHeader } from "@/components/pdf-analyst/Brand";

export default function Home() {
  return (
    <>
      <SiteNav active="home" />
      <PageHeader
        eyebrow="Vantage AI × A2UI v0.9"
        meta={
          <span className="pill">
            <span className="dot" /> live competitive intel
          </span>
        }
        title={
          <>
            Know the local landscape before you{" "}
            <br className="hidden md:inline" />
            <span
              className="bg-clip-text text-transparent"
              style={{ backgroundImage: "var(--brand-gradient)" }}
            >
              sign the lease.
            </span>
          </>
        }
        subtitle="Name an area and a business — “a Pilates studio in Shoreditch” — and Vantage AI searches the live web, then paints a competitive-landscape dashboard: who's already there, how they're doing, and whether there's room for you."
      />

      <main className="flex-1 max-w-[1320px] mx-auto px-6 py-12 w-full">
        <div className="grid md:grid-cols-2 gap-5">
          <ModeCard
            href="/fixed"
            badge="01 · MARKET SCAN"
            title="The landscape at a glance"
            blurb="Name an area and business. Vantage AI searches the live web and paints a fixed competitive-intelligence dashboard."
            bullets={[
              "Live competitor data via Linkup web search",
              "KPIs, demand curve, service mix, competitor table",
              "Click a chip to re-scope to a neighbouring area",
            ]}
            cta="Run a market scan"
          />
          <ModeCard
            href="/dynamic"
            badge="02 · DEEP DIVE"
            title="Ask anything, get the right shape"
            blurb="Follow up on the landscape. The agent answers your question, then a second LLM pass invents the UI from the catalog."
            bullets={[
              "Pick any of the 21 catalog components, in any combination",
              "Stat for single numbers · LineChart for trends · DataTable for lists",
              "Same brand tokens. The agent never sees CSS",
            ]}
            cta="Open the deep dive"
          />
        </div>

        <section className="mt-14">
          <div className="flex items-end justify-between mb-4">
            <div>
              <span className="mono text-[11px] uppercase tracking-[0.14em] text-[var(--muted-2)]">
                The design system
              </span>
              <h2 className="text-[22px] font-semibold tracking-tight mt-1">
                21 components, one catalog
              </h2>
            </div>
            <Link
              href="/catalog"
              className="mono text-[12px] text-[var(--ink)] hover:text-[var(--lilac)] transition"
            >
              See them all →
            </Link>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
            {CATALOG_GROUPS.flatMap((g) =>
              g.items.map((name) => (
                <div
                  key={name}
                  className="surface px-3 py-3 text-[13px] flex items-center justify-between"
                >
                  <span className="mono uppercase tracking-wider text-[11px] text-[var(--muted-2)]">
                    {g.short}
                  </span>
                  <span className="font-medium text-[var(--ink)]">{name}</span>
                </div>
              )),
            )}
          </div>
        </section>

      </main>

      <footer className="border-t border-[var(--line)] py-6 mt-10">
        <div className="max-w-[1320px] mx-auto px-6 text-xs text-[var(--muted)] flex items-center justify-between">
          <span>Vantage AI · live competitive intelligence</span>
          <span className="mono">v0.2</span>
        </div>
      </footer>
    </>
  );
}

const CATALOG_GROUPS = [
  {
    short: "LAY",
    items: ["Stack", "Row", "Grid", "Card", "Section", "Divider"],
  },
  {
    short: "TXT",
    items: ["Heading", "Text", "Overline", "Badge", "Callout", "BulletList"],
  },
  {
    short: "DATA",
    items: [
      "StatCard",
      "BarChart",
      "HorizontalBarChart",
      "LineChart",
      "DonutChart",
      "ScatterChart",
      "DataTable",
    ],
  },
  { short: "ACT", items: ["Button", "ChoiceChips"] },
];

function ModeCard({
  href,
  badge,
  title,
  blurb,
  bullets,
  cta,
}: {
  href: string;
  badge: string;
  title: string;
  blurb: string;
  bullets: string[];
  cta: string;
}) {
  return (
    <Link
      href={href}
      className="group surface p-7 hover:border-[var(--lilac)] transition relative overflow-hidden"
    >
      <div className="absolute -top-20 -right-20 w-[260px] h-[260px] rounded-full brand-gradient-soft opacity-0 group-hover:opacity-100 transition-opacity" />
      <div className="relative">
        <span className="mono text-[11px] uppercase tracking-[0.14em] text-[var(--muted-2)]">
          {badge}
        </span>
        <h3 className="text-[24px] font-semibold tracking-tight mt-2">
          {title}
        </h3>
        <p className="mt-3 text-[var(--muted)] leading-relaxed text-[15px]">
          {blurb}
        </p>
        <ul className="mt-5 space-y-2">
          {bullets.map((b) => (
            <li
              key={b}
              className="flex items-start gap-2.5 text-[13.5px] text-[var(--ink-2)]"
            >
              <span className="mt-2 w-1.5 h-1.5 rounded-full bg-[var(--lilac)] flex-none" />
              <span>{b}</span>
            </li>
          ))}
        </ul>
        <span className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-[var(--ink)] group-hover:text-[var(--ink)] transition mono">
          {cta} <span aria-hidden>→</span>
        </span>
      </div>
    </Link>
  );
}
