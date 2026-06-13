/**
 * A2UI v0.9 envelope types — single import point.
 *
 * Envelopes are emitted by the agent (via `copilotkit.a2ui` Python helpers)
 * and flow over AG-UI as ActivityMessages with activityType = "a2ui-surface".
 * The actual payload lives under `content[A2UI_OPERATIONS_KEY]`.
 *
 * Each operation has the shape:
 *   { version: "v0.9", <envelopeKey>: { surfaceId, ... } }
 *
 * Where <envelopeKey> is one of:
 *   createSurface | updateComponents | updateDataModel | deleteSurface | ...
 */
export const A2UI_OPERATIONS_KEY = "a2ui_operations" as const;
export const A2UI_ACTIVITY_TYPE = "a2ui-surface" as const;

/** All envelope keys we surface in the inspector. */
export type A2UIEnvelopeKey =
  | "createSurface"
  | "updateComponents"
  | "updateDataModel"
  | "deleteSurface"
  | "appendComponents"
  | "appendDataModel";

/** Raw envelope as emitted by the agent. */
export interface A2UIEnvelope {
  version: string;
  [envelopeKey: string]: unknown;
}

/**
 * A captured envelope — what the inspector renders.
 * `body` is the raw envelope; `kind` is the inferred envelope key.
 */
export interface CapturedEnvelope {
  /** Stable id for keying/diffing. */
  id: string;
  /** Inferred envelope key (createSurface, updateComponents, etc.). */
  kind: A2UIEnvelopeKey | "unknown";
  /** Surface id, if extractable from the envelope payload. */
  surfaceId: string | null;
  /** ISO timestamp when the envelope was captured client-side. */
  capturedAt: string;
  /** Source agent id, if known. */
  agentId?: string;
  /** Raw envelope payload. */
  body: A2UIEnvelope;
}

/**
 * The recognized envelope keys in priority order.
 * If multiple are present on one envelope (shouldn't happen but defensive),
 * the first match wins.
 */
export const KNOWN_ENVELOPE_KEYS: A2UIEnvelopeKey[] = [
  "createSurface",
  "updateComponents",
  "updateDataModel",
  "deleteSurface",
  "appendComponents",
  "appendDataModel",
];

/** Extract the envelope kind from a raw envelope payload. */
export function inferEnvelopeKind(env: A2UIEnvelope): A2UIEnvelopeKey | "unknown" {
  for (const key of KNOWN_ENVELOPE_KEYS) {
    if (key in env) return key;
  }
  return "unknown";
}

/** Try to pull a surfaceId out of any common envelope shape. */
export function extractSurfaceId(env: A2UIEnvelope): string | null {
  for (const key of KNOWN_ENVELOPE_KEYS) {
    const payload = env[key];
    if (payload && typeof payload === "object" && "surfaceId" in payload) {
      const sid = (payload as Record<string, unknown>).surfaceId;
      if (typeof sid === "string") return sid;
    }
  }
  return null;
}
