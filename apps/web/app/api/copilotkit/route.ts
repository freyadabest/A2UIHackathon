import {
  CopilotRuntime,
  copilotRuntimeNextJSAppRouterEndpoint,
  ExperimentalEmptyAdapter,
} from "@copilotkit/runtime";
import { HttpAgent } from "@copilotkit/runtime";
import { NextRequest } from "next/server";

const AGENT_URL = process.env.AGENT_URL ?? "http://localhost:8000";

// Connect the CopilotKit runtime to the Python AG-UI agent.
const runtime = new CopilotRuntime({
  agents: {
    vantageai: new HttpAgent({ url: `${AGENT_URL}/` }),
  },
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter: new ExperimentalEmptyAdapter(),
    endpoint: "/api/copilotkit",
  });
  return handleRequest(req);
};
