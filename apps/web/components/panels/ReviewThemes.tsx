"use client";

export type Theme = {
  theme: string;
  mentions: number;
  sentiment: "positive" | "negative";
  examples: string[];
};

export type ReviewThemesProps = {
  competitor: string;
  strengths: Theme[];
  weaknesses: Theme[];
  usingSampleData?: boolean;
};

function ThemeCard({ theme, variant }: { theme: Theme; variant: "strength" | "weakness" }) {
  const isStrength = variant === "strength";
  return (
    <div className={`theme-card theme-${variant}`}>
      <div className="theme-header">
        <span className="theme-title">{theme.theme}</span>
        <span className="theme-mentions">{theme.mentions}x</span>
      </div>
      <div className="theme-examples">
        {theme.examples.slice(0, 2).map((ex, i) => (
          <blockquote key={i} className="theme-quote">
            &ldquo;{ex}&rdquo;
          </blockquote>
        ))}
      </div>
    </div>
  );
}

export function ReviewThemes({
  competitor,
  strengths,
  weaknesses,
  usingSampleData,
}: ReviewThemesProps) {
  return (
    <div className="panel">
      <div className="panel-head">
        <h2>Review Themes — {competitor}</h2>
        {usingSampleData && <span className="panel-sub">sample data</span>}
      </div>

      <div className="themes-section">
        <h3 className="themes-heading themes-heading-strength">
          Strengths
        </h3>
        {strengths.length === 0 ? (
          <p className="empty">No clear strengths mentioned in reviews.</p>
        ) : (
          <div className="themes-grid">
            {strengths.map((t, i) => (
              <ThemeCard key={`strength-${i}`} theme={t} variant="strength" />
            ))}
          </div>
        )}
      </div>

      <div className="themes-section">
        <h3 className="themes-heading themes-heading-weakness">
          Weaknesses
        </h3>
        {weaknesses.length === 0 ? (
          <p className="empty">No clear weaknesses mentioned in reviews.</p>
        ) : (
          <div className="themes-grid">
            {weaknesses.map((t, i) => (
              <ThemeCard key={`weakness-${i}`} theme={t} variant="weakness" />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
