# `src/app/` — Next.js 16 App Router

This is the web app. Next.js 16 + React 19 + Tailwind 4, mounted at `/`.

## What lives here

| File / dir | Purpose |
|---|---|
| `layout.tsx` | Root layout. Wires up `<CopilotKit>` + `<ThemeProvider>` + A2UI catalog. |
| `page.tsx` | Home page. Mounts `<ExampleLayout>` + `<CopilotChat>` + `<ExampleCanvas>`. |
| `globals.css` | Tailwind 4 directives + global CSS. |
| `api/copilotkit/` | The CopilotKit runtime route (touched by Workstream B). |
| `declarative-generative-ui/` | A2UI catalog: definitions + renderers for the demo. |

## What you probably want to edit

- **Theme tokens** → `src/lib/a2ui-theme.css` (Seam #1)
- **Header / branding** → `src/components/BrandFrame.tsx` (Seam #2)
- **What the chat looks like** → `page.tsx` (the `<CopilotChat>` block)

## What you probably should NOT edit

- `layout.tsx`'s `<CopilotKit>` config — versions are pinned for a reason.
- `api/copilotkit/route.ts` — owned by the A2A/runtime workstream.

See `AGENTS.md` and `HACKATHON.md` for the full customization recipes.
