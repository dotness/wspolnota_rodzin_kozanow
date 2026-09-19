# Tasks: Wspólnota Rodzin Mobile Website

**Branch**: `001-wspolnota-rodzin-website` | **Date**: 2026-09-19 | **Spec**: [specs/001-wspolnota-rodzin-website/spec.md](spec.md) | **Plan**: [specs/001-wspolnota-rodzin-website/plan.md](plan.md)

## Phase 1: Setup (Shared Infrastructure & Stitch MCP Project)

**Purpose**: Project directory scaffolding, schema validation setup, and Stitch MCP initialization

- [X] T001 Create project directory structure (`css/`, `js/`, `data/`, `assets/images/`, `assets/news/`, `assets/docs/`, `scripts/`) in repository root
- [X] T002 Initialize Stitch MCP project `wspolnota-rodzin-kozanow` using `create_project`
- [X] T003 [P] Set up JSON schema validation script in `scripts/validate_content.py` to validate against `specs/001-wspolnota-rodzin-website/contracts/content-schema.json`

---

## Phase 2: Foundational (Blocking Prerequisites & Design System)

**Purpose**: Core design tokens, asset localization, and decoupled content store that MUST be complete before user stories can be assembled

**⚠️ CRITICAL**: Blocking prerequisites for all user story components

- [X] T004 Define and register the mobile design system in Stitch MCP (`create_design_system`) with warm Kozanów tokens (terracotta `#b85d38`, sand `#fcf9f5`, gold `#d49a3d`, charcoal `#262626`, and `website_reference` divider border `#e5e0d8`)
- [X] T005 [P] Copy and organize local image assets and documents from `headline_reference.png` and `news_reference` into `assets/images/` and `assets/docs/`
- [X] T006 [P] Create master content data store in `data/content.json` populated with community profile, 4 pillars, and 10 news entries adhering to `contracts/content-schema.json`
- [X] T007 Create embedded fallback script `js/content-data.js` to enable offline `file://` execution without CORS blocks
- [X] T008 Implement client data loader and hydration module in `js/app.js` with dual-mode hydration (`fetch` with fallback to `window.COMMUNITY_DATA`)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - View Community Branding & Pillars (Priority: P1) 🎯 MVP

**Goal**: Display the "Wspólnota Rodzin" header, church emblem, subtitle, parish location, 4 core pillar cards, and banner motto in a centered 600px mobile view.

**Independent Test**: Open the page on a mobile viewport (<= 600px width); verify header identity, 4 pillar cards ("Wspólne Spotkania", "Rodzinna Modlitwa", "Przyjaźnie i Relacje", "Następne Spotkanie"), and motto render with warm visual styling.

- [X] T009 [US1] Generate mobile header and pillars screen components in Stitch MCP using `generate_screen_from_text`
- [X] T010 [P] [US1] Create core layout, typography, and container styles in `css/style.css` (centered 600px mobile container, light neutral canvas)
- [X] T011 [P] [US1] Implement header hero and pillars styling in `css/components.css` (church emblem, typography, 2x2 card grid, and banner quote)
- [X] T012 [US1] Build header and pillar semantic markup in `index.html` with data bindings to `SiteConfig` and `CommunityPillar`
- [X] T013 [US1] Add interactive pillar detail drawer / expandable card behavior in `js/app.js`

**Checkpoint**: At this point, User Story 1 (MVP) is fully functional and testable independently.

---

## Phase 4: User Story 2 - Browse and Read 10 Parish News Entries (Priority: P1)

**Goal**: Present the 10 parish news items in clean tile cards mirroring `website_reference` with an accessible in-page article reader modal and local document attachments.

**Independent Test**: Scroll down to the news feed; verify 10 chronological tiles with photos, titles, and dates. Click "Czytaj całość" to open the article modal reader and verify full text and PDF downloads.

- [X] T014 [US2] Generate news card list and article reader modal components in Stitch MCP using `generate_screen_from_text`
- [X] T015 [P] [US2] Implement news card tile styling in `css/components.css` (hairline divider rules, card borders, badge dates, responsive images)
- [X] T016 [P] [US2] Implement accessible article modal reader styling in `css/components.css` (sticky top bar, typography, attachment callouts)
- [X] T017 [US2] Implement dynamic news card rendering in `js/app.js` iterating through all 10 articles from `data/content.json`
- [X] T018 [US2] Implement modal reader open/close behavior and URL hash navigation (`#artykul-ID`) in `js/app.js`
- [X] T019 [US2] Integrate downloadable PDF attachment actions in `js/app.js` linking to `assets/docs/Oswidczenie-KEP.pdf` and `assets/docs/Apel-Rady.pdf`

**Checkpoint**: At this point, User Stories 1 AND 2 both work independently and form a complete mobile experience.

---

## Phase 5: User Story 3 - AI-Agent Content Updatability & Maintenance (Priority: P2)

**Goal**: Enable AI agents to update, add, or prune news items and community banners solely by modifying `data/content.json` without modifying presentation HTML/CSS.

**Independent Test**: Modify `data/content.json` (e.g. update meeting date or add an article); reload page; confirm changes render immediately without code modification.

- [X] T020 [P] [US3] Create `data/README.md` documenting schema rules, field descriptions, and step-by-step instructions for AI agents updating content
- [X] T021 [US3] Integrate validation command in `scripts/validate_content.py` to test `data/content.json` against `specs/001-wspolnota-rodzin-website/contracts/content-schema.json`
- [X] T022 [US3] Test agent update workflow by executing automated content update simulation per `quickstart.md` Scenario 3

**Checkpoint**: Content management is proven to be completely decoupled and agent-maintainable.

---

## Phase 6: User Story 4 - Seamless Static Hosting Deployment (Priority: P2)

**Goal**: Guarantee zero backend runtime dependencies, 100% relative local asset paths, and zero-configuration compatibility with OVH web hosting (`www/`).

**Independent Test**: Run a local zero-config web server (`python3 -m http.server`); crawl all links and assets to ensure 0 broken links and 100% HTTP 200 responses.

- [X] T023 [P] [US4] Configure meta tags, open graph, favicon, and mobile viewport settings in `index.html`
- [X] T024 [US4] Create automated asset verification script in `scripts/verify_assets.py` to confirm all referenced images, PDFs, and scripts exist locally
- [X] T025 [US4] Execute end-to-end static file crawl test in `scripts/verify_assets.py` proving zero external network requests and 100% HTTP 200 status

**Checkpoint**: Website is 100% deploy-ready for OVH web hosting.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Performance optimization, accessibility, and final end-to-end validation

- [X] T026 [P] Polish mobile tap targets, focus rings, and contrast compliance according to WCAG AA in `css/style.css`
- [X] T027 [P] Optimize and compress image assets in `assets/` for rapid 4G mobile loading
- [X] T028 Run complete verification suite matching `specs/001-wspolnota-rodzin-website/quickstart.md` and document results

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Story 1 (Phase 3 - MVP)**: Depends on Foundational completion.
- **User Story 2 (Phase 4)**: Depends on Foundational completion (integrates alongside US1 in `index.html`).
- **User Story 3 (Phase 5)**: Depends on US1 and US2 data integration.
- **User Story 4 (Phase 6)**: Depends on US1, US2, and US3.
- **Polish (Phase 7)**: Depends on all user story implementations being complete.

### Parallel Opportunities

- **Phase 1**: `T002` (Stitch project) and `T003` (Schema script) can run in parallel.
- **Phase 2**: `T005` (Copy assets) and `T006` (Populate content.json) can run in parallel.
- **Phase 3**: `T010` (Layout styles) and `T011` (Hero styles) can run in parallel.
- **Phase 4**: `T015` (News card styles) and `T016` (Modal reader styles) can run in parallel.
- **Phase 5 & 6**: `T020` (Agent README) and `T023` (Meta tags) can run in parallel.
- **Phase 7**: `T026` (Accessibility polish) and `T027` (Image compression) can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1: Setup (`T001` - `T003`).
2. Complete Phase 2: Foundational (`T004` - `T008`).
3. Complete Phase 3: User Story 1 (`T009` - `T013`).
4. **STOP and VALIDATE**: Verify community branding and 4 pillars on mobile viewport.

### Incremental Delivery
1. Add User Story 2 (`T014` - `T019`): 10 news cards + modal reader with PDF attachments.
2. Add User Story 3 (`T020` - `T022`): AI-agent update validation and documentation.
3. Add User Story 4 (`T023` - `T025`): OVH static hosting verification.
4. Final Polish (`T026` - `T028`): Accessibility, asset compression, quickstart run.

---

## Phase 8: Convergence

**Purpose**: Close the implementation gap between specification, plan, constitution, and the codebase

- [X] T029 Execute Stitch MCP screen generation for mobile layout per Constitution I (missing)
- [X] T030 Build pure client-side static frontend architecture per Constitution II (missing)
- [X] T031 Implement AI-agent maintainable decoupled content store in `data/content.json` per Constitution III (missing)
- [X] T032 Implement mobile-first presentation with centered 600px container and hairline divider lines per Constitution IV (missing)
- [X] T033 Localize all images, icons, and PDF document attachments under `assets/` per Constitution V (missing)
- [X] T034 Create `index.html` main mobile entrypoint with semantic layout and Polish meta tags per FR-001, FR-012 (missing)
- [X] T035 Implement design tokens, responsive typography, and card borders in `css/style.css` and `css/components.css` per FR-002, FR-010 (missing)
- [X] T036 Render top header "Wspólnota Rodzin", emblem, slogan, and 4 pillar tiles per FR-003, US1 (missing)
- [X] T037 Render reverse-chronological feed of 10 parish news entries with photos and metadata per FR-004, FR-005, US2 (missing)
- [X] T038 Implement in-page accessible article reader modal with URL hash routing per FR-008, US2 (missing)
- [X] T039 Wire local PDF attachment download links for Post 3 documents per FR-005, US2 (missing)
- [X] T040 Implement dual-mode client hydration with `js/content-data.js` fallback for offline `file://` execution per FR-007, US3 (missing)
- [X] T041 Create documentation for AI agents updating content in `data/README.md` per FR-007, US3 (missing)
- [X] T042 Implement content schema validation script `scripts/validate_content.py` per SC-004, US3 (missing)
- [X] T043 Implement automated asset and link verification crawler in `scripts/verify_assets.py` per SC-005, US4 (missing)
