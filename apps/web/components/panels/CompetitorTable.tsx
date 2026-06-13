"use client";

export type Competitor = {
  name: string;
  rating?: number;
  reviews?: number;
  url?: string;
  location?: string;
};

export function CompetitorTable({ competitors }: { competitors: Competitor[] }) {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th style={{ textAlign: "left" }}>Name</th>
          <th>Rating</th>
          <th>Reviews</th>
          <th style={{ textAlign: "left" }}>Location</th>
        </tr>
      </thead>
      <tbody>
        {competitors.map((c) => (
          <tr key={c.name}>
            <td>{c.url ? <a href={c.url}>{c.name}</a> : c.name}</td>
            <td style={{ textAlign: "center" }}>{c.rating ?? "—"}</td>
            <td style={{ textAlign: "center" }}>{c.reviews ?? "—"}</td>
            <td>{c.location ?? "—"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
