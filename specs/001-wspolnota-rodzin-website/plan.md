# Implementation Plan: Wspólnota Rodzin Mobile Website

**Branch**: `001-wspolnota-rodzin-website` | **Date**: 2026-09-19 | **Spec**: [specs/001-wspolnota-rodzin-website/spec.md](spec.md)

**Input**: Feature specification from `specs/001-wspolnota-rodzin-website/spec.md`

## Summary

Build a fast, elegant, client-side static mobile website for "Wspólnota Rodzin" (Parafia św. Jadwigi Śląskiej, Wrocław-Kozanów) ready for instant deployment on OVH shared web hosting. In strict accordance with Constitution Principle I, **Stitch MCP** will be used as the authoritative tool for frontend design system definition, screen generation, and component creation. The visual design synthesizes the disciplined card borders, hairline lines, and centered 600px container of `website_reference` with the warm community branding and 4 pillars from `headline_reference.png`. All 10 parish news entries from `news_reference` are stored in an AI-agent-editable JSON data file with localized photos and downloadable PDFs, delivering an app-like mobile reading experience with zero backend dependencies.

## Technical Context

**Design & Creation Tooling**: **Stitch MCP** (`create_project`, `create_design_system`, `generate_screen_from_text`, `get_screen`, `generate_variants`). Used to generate the mobile layout, design tokens, cards, and modal reader.

**Language/Version**: Semantic HTML5, Vanilla CSS3, Client JavaScript (ES2022+), zero compilation toolchains.

**Primary Dependencies**: None (strictly zero third-party npm runtime dependencies; fully self-contained).

**Storage**: Plain static JSON files (`data/content.json`) with hydration fallback (`js/content-data.js`) for seamless offline `file://` and `http://` viewing.

**Testing**: Automated static file linting, JSON schema validation against `contracts/content-schema.json`, and headless browser rendering verification.

**Target Platform**: OVH Web Hosting (`www/` or `public_html/` static directory), mobile browsers (iOS Safari, Android Chrome, mobile Firefox).

**Project Type**: Static Web Application (Jamstack / Mobile-first).

**Performance Goals**: First Contentful Paint < 1.0s, total page weight < 2.5MB (including high-resolution local images), zero Cumulative Layout Shift (CLS).

**Constraints**: Mobile-first layout (constrained to 600px max-width centered canvas), zero backend runtimes (no Node.js/PHP/Python server), zero external CDN/font tracking requirements.

**Scale/Scope**: Single-page mobile view with header hero, 4 interactive community pillars, 10 news articles, in-page accessible article reader modal, and 2 PDF document downloads.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (Stitch MCP for Frontend Design & Creation)**: **PASS**. Stitch MCP is formally designated as the design and screen generation authority for all UI components, tokens, and screen variants.
- **Principle II (Pure Static Frontend Architecture)**: **PASS**. Zero server-side runtimes or databases; pure HTML/CSS/JS ready for OVH.
- **Principle III (AI-Agent Content Maintainability)**: **PASS**. Content completely decoupled into `data/content.json` matching `contracts/content-schema.json`.
- **Principle IV (Mobile-First & Aesthetic Fidelity)**: **PASS**. Centered 600px viewport combining `website_reference` lines with `headline_reference.png` branding.
- **Principle V (Autonomous Self-Containment)**: **PASS**. All media, icons, and PDF documents localized with relative paths.

## Implementation Workflow (Stitch MCP Integration)

### Stage 1: Design Generation via Stitch MCP
1. Initialize a dedicated project in Stitch MCP (`wspolnota-rodzin-kozanow`).
2. Establish the design system and color palette (warm terracotta `#b85d38`, cream/sand `#fcf9f5`, gold `#d49a3d`, deep charcoal `#262626`, and crisp border rules `#e5e0d8`).
3. Generate the primary mobile home screen via Stitch MCP with:
   - "Wspólnota Rodzin" header hero, church/heart insignia, and subtitle.
   - 4 community pillars grid ("Wspólne Spotkania", "Rodzinna Modlitwa", "Przyjaźnie i Relacje", "Następne Spotkanie").
   - Segmented news feed tiles matching `website_reference` lines and card borders.
4. Generate the mobile article reader modal screen via Stitch MCP.
5. Export clean HTML/CSS components and tokens into `css/style.css` and `css/components.css`.

### Stage 2: Static Data & Hydration Layer
1. Populate `data/content.json` with the full community metadata and all 10 articles from `news_reference` (including local image references and PDF attachments).
2. Generate `js/content-data.js` as an offline DOM fallback for local `file://` execution.
3. Wire `js/app.js` to render the dynamic feed, manage modal open/close transitions, and handle URL hash navigation (`#artykul-ID`).

### Stage 3: Asset Packaging & Local Verification
1. Copy all images and PDFs into `assets/images/` and `assets/docs/`.
2. Verify responsive layout across mobile viewports (320px, 375px, 414px) and centered desktop preview (600px).
3. Validate against `contracts/content-schema.json` and ensure 100% relative link resolution.

## Project Structure

### Documentation (this feature)

```text
specs/001-wspolnota-rodzin-website/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Phase 0 architectural & styling decisions
├── data-model.md        # Phase 1 entity definitions and ERD
├── quickstart.md        # Phase 1 setup and verification guide
├── contracts/           # Phase 1 contract specifications
│   ├── content-schema.json
│   └── ui-interface.md
└── checklists/
    └── requirements.md  # Quality validation checklist
```

### Source Code (repository root)

```text
./
├── index.html                  # Main mobile website entrypoint (Stitch MCP layout)
├── css/
│   ├── style.css               # Design system tokens, typography, container layout
│   └── components.css          # Header hero, pillar tiles, news cards, modal reader
├── js/
│   ├── app.js                  # Data hydration, rendering engine, modal controller
│   └── content-data.js         # Embedded JSON data fallback for offline file:// protocol
├── data/
│   └── content.json            # Master content data file (editable by AI agents)
└── assets/
    ├── images/
    │   ├── header/             # Headline banner graphic, church emblem, texture
    │   └── icons/              # SVG icons for pillars (users, heart, church, calendar)
    ├── news/
    │   ├── 01/ ... 10/         # Localized image files for each of the 10 articles
    └── docs/
        ├── Oswidczenie-KEP.pdf # Downloadable attachment from Post 3
        └── Apel-Rady.pdf       # Downloadable attachment from Post 3
```

## Complexity Tracking

*No constitutional violations. Zero unnecessary architectural abstractions.*
