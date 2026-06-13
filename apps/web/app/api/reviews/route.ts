import { NextRequest, NextResponse } from "next/server";

const AGENT_URL = process.env.AGENT_URL ?? "http://localhost:8000";

// Proxy the browser's review analysis request to the Python agent.
export async function POST(req: NextRequest) {
  let body: Record<string, unknown> = {};
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ detail: "invalid JSON body" }, { status: 400 });
  }

  const competitor = typeof body.competitor === "string" ? body.competitor : "";
  const businessType = typeof body.businessType === "string" ? body.businessType : "";
  const area = typeof body.area === "string" ? body.area : "";

  if (!competitor.trim() || !businessType.trim() || !area.trim()) {
    return NextResponse.json(
      { detail: "competitor, businessType, and area are required" },
      { status: 400 }
    );
  }

  try {
    const res = await fetch(`${AGENT_URL}/reviews`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ competitor, business_type: businessType, area }),
      cache: "no-store",
      signal: AbortSignal.timeout(55_000),
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    const timedOut = err instanceof Error && err.name === "TimeoutError";
    return NextResponse.json(
      {
        detail: timedOut
          ? "The review analysis took too long. Please try again."
          : `agent unreachable at ${AGENT_URL}: ${String(err)}`,
      },
      { status: timedOut ? 504 : 502 }
    );
  }
}
