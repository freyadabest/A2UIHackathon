import { NextRequest, NextResponse } from "next/server";

const AGENT_URL = process.env.AGENT_URL ?? "http://localhost:8000";

// Proxy the browser's idea -> the Python agent's generative dashboard.
export async function POST(req: NextRequest) {
  let idea = "";
  try {
    const body = await req.json();
    idea = typeof body?.idea === "string" ? body.idea : "";
  } catch {
    return NextResponse.json({ detail: "invalid JSON body" }, { status: 400 });
  }

  if (!idea.trim()) {
    return NextResponse.json({ detail: "idea must not be empty" }, { status: 400 });
  }

  try {
    const res = await fetch(`${AGENT_URL}/dashboard`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idea }),
      cache: "no-store",
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    return NextResponse.json(
      { detail: `agent unreachable at ${AGENT_URL}: ${String(err)}` },
      { status: 502 },
    );
  }
}
