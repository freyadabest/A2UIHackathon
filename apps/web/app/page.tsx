"use client";

import { useState } from "react";
import { PanelRenderer, PanelSpec } from "@/components/PanelRenderer";

type DashboardResponse = {
  idea: string;
  businessType: string;
  area: string;
  usingSampleData: boolean;
  panels: PanelSpec[];
};

type ReviewPanel = {
  type: "panel";
  name: "ReviewThemes";
  props: Record<string, unknown>;
};

const EXAMPLES = [
  "I want to open a Pilates studio in Shoreditch",
  "A specialty coffee shop in Williamsburg, Brooklyn",
  "Launch a vegan bakery in Lisbon",
];

export default function Page() {
  const [idea, setIdea] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [reviewPanels, setReviewPanels] = useState<ReviewPanel[]>([]);
  const [reviewLoading, setReviewLoading] = useState<string | null>(null);
  const [reviewError, setReviewError] = useState<string | null>(null);

  async function build(input: string) {
    const trimmed = input.trim();
    if (!trimmed || loading) return;
    setLoading(true);
    setError(null);
    setReviewPanels([]);
    setReviewError(null);
    try {
      const res = await fetch("/api/dashboard", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idea: trimmed }),
        signal: AbortSignal.timeout(60_000),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json?.detail ?? "request failed");
      setData(json as DashboardResponse);
    } catch (e) {
      const msg =
        e instanceof Error && e.name === "TimeoutError"
          ? "The search took too long. Please try again."
          : e instanceof Error
            ? e.message
            : "Something went wrong";
      setError(msg);
      setData(null);
    } finally {
      setLoading(false);
    }
  }

  async function analyzeReviews(competitor: string) {
    if (!data || reviewLoading) return;
    setReviewLoading(competitor);
    setReviewError(null);
    try {
      const res = await fetch("/api/reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          competitor,
          businessType: data.businessType,
          area: data.area,
        }),
        signal: AbortSignal.timeout(55_000),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json?.detail ?? "request failed");
      setReviewPanels((prev) => [...prev, json as ReviewPanel]);
    } catch (e) {
      const msg =
        e instanceof Error && e.name === "TimeoutError"
          ? "The review analysis took too long. Please try again."
          : e instanceof Error
            ? e.message
            : "Something went wrong";
      setReviewError(msg);
    } finally {
      setReviewLoading(null);
    }
  }

  const competitors =
    data?.panels
      .find((p) => p.name === "CompetitorTable")
      ?.props?.competitors as Array<{ name: string }> | undefined;

  return (
    <main className="shell">
      <header className="hero">
        <div className="logo">VantageAI</div>
        <h1>Describe a business idea. Get a live competitor dashboard.</h1>
        <p className="tagline">
          One sentence in — the agent searches the real web with Linkup and
          generatively renders your market intelligence.
        </p>

        <form
          className="prompt"
          onSubmit={(e) => {
            e.preventDefault();
            build(idea);
          }}
        >
          <input
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            placeholder='e.g. "I want to open a Pilates studio in Shoreditch"'
            aria-label="Business idea"
          />
          <button type="submit" disabled={loading || !idea.trim()}>
            {loading ? "Building…" : "Build dashboard"}
          </button>
        </form>

        <div className="chips">
          {EXAMPLES.map((ex) => (
            <button
              key={ex}
              className="chip"
              onClick={() => {
                setIdea(ex);
                build(ex);
              }}
              disabled={loading}
            >
              {ex}
            </button>
          ))}
        </div>
      </header>

      <section className="canvas">
        {loading && (
          <div className="loading">
            <div className="spinner" />
            <span>Searching the web and assembling your dashboard…</span>
          </div>
        )}

        {error && !loading && (
          <div className="panel error">
            <strong>Couldn&apos;t build the dashboard.</strong>
            <p>{error}</p>
          </div>
        )}

        {data && !loading && (
          <>
            {data.usingSampleData && (
              <div className="notice">
                Showing sample data — set <code>LINKUP_API_KEY</code> for live
                web results.
              </div>
            )}
            <PanelRenderer panels={data.panels} />

            {competitors && competitors.length > 0 && (
              <div className="panel follow-ups">
                <div className="panel-head">
                  <h2>Deep Dive</h2>
                  <span className="panel-sub">
                    Pick a competitor to analyze their reviews
                  </span>
                </div>
                <div className="follow-up-grid">
                  {competitors.map((c, i) => (
                    <button
                      key={`${c.name}-${i}`}
                      className="follow-up-btn"
                      onClick={() => analyzeReviews(c.name)}
                      disabled={reviewLoading === c.name}
                    >
                      {reviewLoading === c.name
                        ? `Analyzing ${c.name}…`
                        : `What are ${c.name}&rsquo;s strengths & weaknesses?`}
                    </button>
                  ))}
                </div>
                {reviewError && (
                  <p className="empty" style={{ marginTop: 12 }}>
                    {reviewError}
                  </p>
                )}
              </div>
            )}

            {reviewPanels.length > 0 && (
              <PanelRenderer panels={reviewPanels} />
            )}
          </>
        )}

        {!data && !loading && !error && (
          <div className="placeholder">
            Your generated dashboard will appear here.
          </div>
        )}
      </section>
    </main>
  );
}
