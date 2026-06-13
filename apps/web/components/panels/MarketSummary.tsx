"use client";

export type MarketSummaryProps = {
  businessType: string;
  area: string;
  competitorCount: number;
  avgRating?: number | null;
  totalReviews?: number;
  topPlayer?: string | null;
  saturation: string;
};

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="stat">
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
}

export function MarketSummary(props: MarketSummaryProps) {
  const {
    businessType,
    area,
    competitorCount,
    avgRating,
    totalReviews,
    topPlayer,
    saturation,
  } = props;

  return (
    <div className="panel panel-summary">
      <div className="panel-head">
        <h2>
          {businessType} · {area}
        </h2>
        <span className={`badge badge-${saturation.split(" ")[0].toLowerCase()}`}>
          {saturation}
        </span>
      </div>
      <div className="stat-grid">
        <Stat label="Competitors found" value={String(competitorCount)} />
        <Stat label="Avg rating" value={avgRating != null ? `${avgRating}★` : "—"} />
        <Stat
          label="Total reviews"
          value={totalReviews ? totalReviews.toLocaleString() : "—"}
        />
        <Stat label="Top player" value={topPlayer ?? "—"} />
      </div>
    </div>
  );
}
