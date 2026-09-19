# Technical Research: Wspólnota Rodzin Mobile Website

**Feature**: `001-wspolnota-rodzin-website`  
**Date**: 2026-09-19  

## Research Objectives

Evaluate the optimal architectural, stylistic, and data management choices for a mobile-first, static website representing "Wspólnota Rodzin" (Parafia św. Jadwigi, Wrocław-Kozanów), hosted on OVH shared web hosting and easily maintainable by AI agents.

---

## Decision 1: Architecture & Technology Stack

### Decision
Use **Pure HTML5, Vanilla CSS3, and Modular Client-Side JavaScript (ES2022+)** with no server runtime and no build toolchain required.

### Rationale
1. **OVH Web Hosting Compatibility**: OVH shared web hosting natively serves static files from `www/` or `public_html/` with zero configuration, maximum uptime, and instant TTFB (Time to First Byte).
2. **AI Agent Friendliness**: AI agents can inspect, understand, edit, and validate plain HTML, CSS, and JSON files without running compilation steps (`npm run build`), troubleshooting bundler errors, or handling lockfile drift.
3. **Performance & Lightweight Footprint**: Completely removes the multi-megabyte bundle overhead of frontend frameworks, delivering sub-second page loads on 3G/4G mobile devices.
4. **Offline & Longevity**: Static files have zero runtime vulnerabilities and continue working indefinitely without node runtime updates or security patches.

### Alternatives Considered
- **Next.js / Astro Static Export (`SSG`)**: Provides components and templating, but requires a Node.js build pipeline (`npm install`, `build`), adding friction for lightweight AI agent updates and potential CI/CD breakages.
- **Single Page App (React / Vue / Svelte via Vite)**: Unnecessary complexity for a mobile news and community presentation site; adds client-side hydration lag.
- **WordPress / PHP CMS**: Explicitly rejected by requirements ("i dont want any backend, just frontend").

---

## Decision 2: Content Management & AI Agent Update Pattern

### Decision
Store all dynamic content (community header details, pillars, next meeting date, and all 10 news entries) in a structured JSON file at `data/content.json`, with a lightweight fallback data script (`js/content-data.js`) embedded into the DOM.

### Rationale
1. **Single Source of Truth**: When an AI agent is instructed to "add a news post" or "change next meeting time", it only needs to touch `data/content.json` (or `js/content-data.js`).
2. **Dual-Environment Resilience**: 
   - When hosted on OVH over HTTP/HTTPS, client JavaScript uses standard `fetch('data/content.json')`.
   - When opened locally via `file://` (where browser CORS restrictions might block `fetch`), the site gracefully falls back to `window.COMMUNITY_DATA` defined in `js/content-data.js` or pre-rendered static HTML elements, ensuring seamless local offline preview.
3. **Structured Schema**: Validated against `contracts/content-schema.json`, providing deterministic constraints for AI agent prompting.

### Alternatives Considered
- **Hardcoding content directly in `index.html`**: Requires AI agents to parse and modify deep HTML markup trees, increasing risk of tag mismatches, styling breakage, or accidental deletions.
- **Markdown files for each article**: Excellent for long blogs, but requires either a client-side markdown parser (like marked.js) or a static site generator. Embedding clean HTML/Markdown-ready strings in JSON gives the best balance of simplicity and structure.

---

## Decision 3: Visual Design & Styling System

### Decision
Combine the **visual structure of `website_reference`** (centered 600px mobile canvas, crisp tile boundaries, subtle hairline divider lines, generous vertical rhythm) with the **warm, welcoming community identity of `headline_reference.png`** (warm terracotta/brick accent `#b85d38`, sand/cream tones `#fcf9f5`, gold/amber accents, and soft charcoal `#262626` for readable text).

### Rationale
1. **User Requirement Compliance**: Matches the user's explicit preference: *"look like website_reference, but the top header is to be about polish Wspolnota Rodzin from headline_reference.png ... keep the style as website_reference, i like the tiles lines and overall feeling - it will be only mobile for now."*
2. **Header Composition**:
   - Top insignia: Church roof silhouette with central heart and cross (from the reference poster).
   - Main title: "Wspólnota Rodzin" in elegant, warm typography.
   - Slogan: *"Razem w wierze, w miłości, na co dzień"*.
   - Location banner: *"Wrocław Kozanów • Parafia św. Jadwigi Śląskiej"*.
   - Community Pillar Grid: 4 interactive cards ("Wspólne Spotkania", "Rodzinna Modlitwa", "Przyjaźnie i Relacje", "Następne Spotkanie").
   - Sub-motto: *"Bo rodzina to wielki dar"*.
3. **News Tile Rhythm**:
   - Each news entry sits in a framed card with a subtle border (`1px solid #e5e0d8`), top metadata line, proportional photo display, clear title, concise excerpt, and an action button to read the full article.

### Alternatives Considered
- **Full-width fluid responsive design**: User explicitly requested: *"it will be only mobile for now"*. Centering the mobile layout on wider screens (like a newsletter viewer or mobile web app wrapper) preserves the intended visual proportions on all screens.

---

## Decision 4: Article Reading Experience on Mobile

### Decision
Implement an **accessible, lightweight in-page Modal / Drawer Reader** for full articles, alongside downloadable asset links for PDFs.

### Rationale
1. Keeps the user in a smooth, continuous mobile single-page flow without jarring page reloads.
2. Supports deep linking (`#news-1`, `#news-2`) via `window.location.hash` so users and parish newsletters can link directly to specific announcements.
3. Automatically formats embedded photos, paragraphs, and downloadable PDF attachment buttons (e.g. for the KEP and Bishops' council declarations).

### Alternatives Considered
- **Navigating to separate HTML files (`post.html`)**: While functional, it breaks mobile momentum and requires browser back navigation. In-page modal reading with browser history support (`history.pushState`) provides a native app-like mobile experience.

---

## Decision 5: Media and Asset Organization

### Decision
Localize and optimize all assets into a dedicated `assets/` structure:
- `assets/images/header/`: Header illustration, logo, background texture.
- `assets/images/news/`: Photos for all 10 articles (scaled and compressed for fast mobile loading).
- `assets/docs/`: PDF attachments (such as `Oswidczenie-KEP.pdf` and `Apel-Rady.pdf`).

### Rationale
Guarantees 100% self-containment, eliminates broken external links, and prevents CORS or hotlinking issues on OVH hosting.

---

## Decision 6: Frontend Design & Screen Generation Tooling (Stitch MCP)

### Decision
Utilize **Stitch MCP** as the primary design system and screen generation tool to design, explore variants, and generate the mobile screens and component markup.

### Rationale
1. **Constitutional Compliance**: Aligns directly with Constitution Principle I (*Stitch MCP for Frontend Design & Creation*).
2. **Design Fidelity**: Stitch MCP specializes in generating refined UI screens and design tokens matching visual references.
3. **Structured Workflow**:
   - `create_project` to initialize `wspolnota-rodzin-kozanow` in Stitch.
   - `create_design_system` to establish the warm Kozanów palette and `website_reference` tile rules.
   - `generate_screen_from_text` to create the mobile home screen and article reader modal.
   - `get_screen` to export clean HTML/CSS components for final assembly.
