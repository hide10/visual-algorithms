# AGENTS.md

## Project intent
- This project is a static educational site for visualizing core programming algorithms.
- Primary domain target: `algorithm.hide10.com`
- Secondary distribution target: GitHub Pages
- Content policy:
  - Keep pages usable as plain static files.
  - Prefer one algorithm per directory with its own `index.html`.
  - Teach with motion first, notation second.

## Product rules
- Each algorithm page should include:
  - Short concept explanation
  - Interactive visualization
  - Pseudocode or step mapping
  - Complexity summary
  - A short explanation of why that complexity occurs
- Concept pages are allowed for cross-cutting topics such as:
  - complexity
  - recursion
  - stable sort
  - graph representation
- Japanese is the primary language for now.

## Current structure
- `/index.html`
  - top page and series entry point
- `/scripts/generate_site.py`
  - source of truth for generated content pages
- `/app.js`
  - shared playback runtime for the generated visualizer pages
- `/styles.css`
  - shared site styles

## Visual/content direction
- Avoid generic documentation aesthetics.
- Use a strong but readable visual identity.
- Optimize for beginners:
  - start from intuition and concrete examples
  - delay formal notation until the reader has context
  - surface common misunderstandings explicitly
- Favor compact explanations over textbook-style density.

## Deployment strategy
- Both GitHub Pages and `algorithm.hide10.com` should be served from the same static source where possible.
- Keep links relative so the site works in either environment.
- If environment-specific behavior is needed later, isolate it behind small config files or build-time replacement only.
- Planned monetization policy:
  - `algorithm.hide10.com`: clean educational experience, no ads by default
  - `hide10.com` mirrored/embedded version: ads allowed in layout wrappers outside the core teaching content

## Editing guidance
- Prefer editing shared styles only when a change benefits multiple pages.
- Reuse the established page pattern before inventing new page structures.
- When adding a new algorithm:
  - create `/<algorithm-name>/index.html`
  - link it from `/index.html`
  - keep controls and stats understandable without prior explanation
- Do not introduce framework dependencies unless static HTML becomes a clear blocker.

## Near-term roadmap
- Review generated pages one by one and tighten explanations
- Prepare a minimal publish note for GitHub Pages and custom domain hosting
- Keep content additions centralized in `/scripts/generate_site.py`
