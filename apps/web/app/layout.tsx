import type { ReactNode } from "react";

export const metadata = {
  title: "VantageAI",
  description: "Describe a business idea, watch an agent build a live market-intelligence dashboard.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
