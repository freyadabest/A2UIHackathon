"use client";

export type RatingsBar = { name: string; rating: number };

export function RatingsChart({
  bars,
  max = 5,
}: {
  bars: RatingsBar[];
  max?: number;
}) {
  return (
    <div className="panel">
      <div className="panel-head">
        <h2>Competitor ratings</h2>
        <span className="panel-sub">out of {max}★</span>
      </div>
      {bars.length === 0 ? (
        <p className="empty">No ratings available for these competitors yet.</p>
      ) : (
        <div className="chart">
          {bars.map((b) => (
            <div className="chart-row" key={b.name}>
              <div className="chart-label" title={b.name}>
                {b.name}
              </div>
              <div className="chart-track">
                <div
                  className="chart-fill"
                  style={{ width: `${(b.rating / max) * 100}%` }}
                />
              </div>
              <div className="chart-value">{b.rating.toFixed(1)}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
