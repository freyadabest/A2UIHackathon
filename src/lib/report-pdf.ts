/* Download the rendered market-scan surface as a PDF.
 *
 * We deliberately avoid html2canvas/jsPDF here: the dashboard theme leans on
 * modern CSS (`color-mix(in oklab ...)`, gradients) and Recharts SVG, which
 * the rasterizing libs handle poorly. Instead we clone the rendered surface
 * into an off-screen iframe that reuses the document's own stylesheets, then
 * call the browser's native print — which renders all modern CSS correctly and
 * lets the user "Save as PDF". No new dependencies. */

function escapeHtml(s: string): string {
  return s.replace(
    /[&<>"]/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c] as string,
  );
}

export function printElementToPdf(
  el: HTMLElement | null,
  opts: { subtitle?: string } = {},
): void {
  if (!el) return;

  const headHtml = document.head.innerHTML;
  const htmlClass = document.documentElement.className;
  const bodyClass = document.body.className;
  const stamp = new Date().toLocaleString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  const iframe = document.createElement("iframe");
  iframe.setAttribute("aria-hidden", "true");
  iframe.style.cssText =
    "position:fixed;right:0;bottom:0;width:0;height:0;border:0;visibility:hidden;";
  document.body.appendChild(iframe);

  const win = iframe.contentWindow;
  const doc = win?.document;
  if (!win || !doc) {
    iframe.remove();
    return;
  }

  doc.open();
  doc.write(`<!doctype html>
<html class="${htmlClass}">
<head>
<base href="${location.origin}/">
${headHtml}
<style>
  @page { size: A4 landscape; margin: 12mm; background:#fdf8f3; }
  html, body { background:#fdf8f3 !important; height:auto !important; overflow:visible !important; }
  body { margin:0; padding:0; color:#4a3a38; }
  .report-head {
    display:flex; align-items:baseline; justify-content:space-between; gap:16px;
    padding:0 0 14px; margin:0 0 18px; border-bottom:1px solid #ecd9c9;
    font-family: var(--font-display, system-ui), system-ui, sans-serif;
  }
  .report-head .brand { font-size:24px; font-weight:800; letter-spacing:-0.02em; color:#cc7a99; }
  .report-head .meta { font-size:11px; text-transform:uppercase; letter-spacing:0.12em; color:#8c726c; }
  .report-sub { font-size:13px; color:#8c726c; margin:-8px 0 20px; }
  .a2ui-surface { padding:0 !important; background:transparent !important; }
  .a2ui-surface svg { max-width:100%; height:auto; }
  /* Keep diagrams, cards and chart blocks whole across page breaks. */
  .recharts-wrapper,
  .recharts-responsive-container,
  .a2ui-surface svg,
  .a2ui-surface img,
  .a2ui-surface div[class*="rounded-"] {
    break-inside: avoid;
    page-break-inside: avoid;
  }
  .a2ui-surface table { break-inside: auto; }
  .a2ui-surface tr, .a2ui-surface thead { break-inside: avoid; page-break-inside: avoid; }
  /* Keep a section's title on the same page as its chart/content. */
  .a2ui-surface section { break-inside: avoid; page-break-inside: avoid; }
  .a2ui-surface h1, .a2ui-surface h2, .a2ui-surface h3 { break-after: avoid; page-break-after: avoid; }
  * { -webkit-print-color-adjust:exact !important; print-color-adjust:exact !important; }
</style>
</head>
<body class="${bodyClass}">
  <div class="report-head">
    <span class="brand">VantageAI</span>
    <span class="meta">Market scan · ${escapeHtml(stamp)}</span>
  </div>
  ${opts.subtitle ? `<div class="report-sub">${escapeHtml(opts.subtitle)}</div>` : ""}
  <div class="a2ui-surface">${el.innerHTML}</div>
</body>
</html>`);
  doc.close();

  const cleanup = () => setTimeout(() => iframe.remove(), 500);
  const doPrint = () => {
    try {
      win.focus();
      win.print();
    } finally {
      cleanup();
    }
  };

  win.onafterprint = cleanup;
  // Give cloned stylesheets + webfonts a beat to apply before printing.
  if (doc.fonts?.ready) {
    doc.fonts.ready
      .then(() => setTimeout(doPrint, 200))
      .catch(() => setTimeout(doPrint, 400));
  } else {
    setTimeout(doPrint, 500);
  }
}
