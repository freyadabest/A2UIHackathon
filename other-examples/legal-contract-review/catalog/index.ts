/**
 * Legal Paper Catalog — public entry point.
 *
 * Wires the catalog definitions (schemas) to their React renderers via
 * `createCatalog`. Consumers import `legalPaperCatalog` and pass it to the
 * A2UI renderer's catalog prop. The string id (`copilotkit://legal-paper-catalog`)
 * is what the agent references when it emits an envelope that should be
 * rendered against this catalog instead of the default dashboard catalog.
 *
 * Pattern mirrors `src/app/declarative-generative-ui/index.ts` (canonical
 * dashboard catalog), with the catalog id swapped for the legal surface.
 */

import { createCatalog } from "@copilotkit/a2ui-renderer";
import { legalPaperCatalogDefinitions } from "./definitions";
import { legalPaperCatalogRenderers } from "./renderers";

export const legalPaperCatalog = createCatalog(
  legalPaperCatalogDefinitions,
  legalPaperCatalogRenderers,
  { catalogId: "copilotkit://legal-paper-catalog" },
);

export { legalPaperCatalogDefinitions } from "./definitions";
export type { LegalPaperCatalogDefinitions } from "./definitions";
