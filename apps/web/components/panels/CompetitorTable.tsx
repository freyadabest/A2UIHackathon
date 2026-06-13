"use client";

export type Competitor = {
  name: string;
  rating?: number | null;
  reviews?: number | null;
  url?: string;
  location?: string;
};

export function CompetitorTable({ competitors }: { competitors: Competitor[] }) {
  return (
    <div className="panel">
      <div className="panel-head">
        <h2>Competitors</h2>
        <span className="panel-sub">{competitors.length} found</span>
      </div>
      {competitors.length === 0 ? (
        <p className="empty">No competitors found — try a different area.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th className="num">Rating</th>
              <th className="num">Reviews</th>
              <th>Location</th>
            </tr>
          </thead>
          <tbody>
            {competitors.map((c, i) => (
              <tr key={`${c.name}-${i}`}>
                <td>
                  {c.url ? (
                    <a href={c.url} target="_blank" rel="noreferrer">
                      {c.name}
                    </a>
                  ) : (
                    c.name
                  )}
                </td>
                <td className="num">{c.rating != null ? `${c.rating}★` : "—"}</td>
                <td className="num">
                  {c.reviews != null ? c.reviews.toLocaleString() : "—"}
                </td>
                <td>{c.location ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
