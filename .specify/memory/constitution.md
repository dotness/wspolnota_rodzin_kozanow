<!--
Sync Impact Report
- Version change: Uninitialized Template → 1.0.0
- Added principles:
  - I. Stitch MCP for Frontend Design & Creation
  - II. Pure Static Frontend Architecture (Zero-Backend)
  - III. AI-Agent Content Maintainability & Decoupled Data
  - IV. Mobile-First Presentation & Aesthetic Fidelity
  - V. Autonomous Self-Containment & Local Asset Integrity
- Added sections:
  - Technical & Tooling Constraints
  - Development Workflow & Quality Gates
  - Governance
- Deferred items: None
-->

# Wspólnota Rodzin Kozanów Constitution

## Core Principles

### I. Stitch MCP for Frontend Design & Creation
Stitch MCP MUST be used as the primary design system and screen generation tool for frontend design, UI variant exploration, and component screen creation. All major visual layouts, theme tokens, and component structures must be conceived, generated, or styled leveraging Stitch MCP capabilities before or during code implementation. Manual CSS/HTML iterations must adhere strictly to the design system established through Stitch MCP.

### II. Pure Static Frontend Architecture (Zero-Backend)
The website MUST be delivered purely as client-side static web artifacts (HTML5, Vanilla CSS3, modern modular JavaScript). No server-side language runtimes (PHP, Node.js, Python) or database engines (MySQL, PostgreSQL) may be introduced or required. The output MUST be directly deployable to standard static web hosting providers (such as OVH shared hosting `www/` or `public_html/`) simply by copying static files.

### III. AI-Agent Content Maintainability & Decoupled Data
Content MUST remain strictly decoupled from presentation markup. Dynamic parish announcements, upcoming meeting information, core pillars, and news entries MUST be maintained in human- and agent-readable structured static files (e.g., `data/content.json`). AI agents MUST be capable of adding, editing, or archiving announcements reliably without parsing or altering complex layout code.

### IV. Mobile-First Presentation & Aesthetic Fidelity
The user experience MUST prioritize mobile devices, adhering to a centered mobile canvas with a maximum width of 600px. Visual styling MUST preserve the crisp tile boundaries, hairline divider lines, and disciplined spacing demonstrated in `website_reference`, combined with the warm community branding, typography, and core pillars derived from `headline_reference.png`.

### V. Autonomous Self-Containment & Local Asset Integrity
All media, logos, photographs, font dependencies, and document attachments (e.g., PDFs) MUST be hosted locally within the repository using relative paths. The website MUST NOT depend on external third-party CDNs, tracking scripts, or remote endpoints that could fail, track users, or compromise long-term offline usability.

## Technical & Tooling Constraints

- **Design Tooling**: Stitch MCP is the mandatory authority for screen generation, layout variants, and design system definition.
- **Frontend Core**: Semantic HTML5, Vanilla CSS3, and standard ECMAScript. Heavy frontend frameworks (React, Vue, Angular) and compilation toolchains are prohibited unless explicitly ratified.
- **Data Format**: Standard UTF-8 encoded JSON schema-compliant content structures.
- **Hosting Target**: OVH Web Hosting standard static directory structure (`www/`).

## Development Workflow & Quality Gates

- **Design Gate**: UI changes and screen structures must be verified against Stitch MCP designs and reference assets (`website_reference` layout rules and `headline_reference.png` branding).
- **Agent Verification Gate**: Any content schema adjustment must be validated against `contracts/content-schema.json` to ensure AI agents can continue reading and updating content without syntax errors.
- **Deployment Gate**: The build directory must be verified using zero-dependency local static servers (e.g., `python3 -m http.server`) with 100% relative links and HTTP 200 responses.

## Governance

This Constitution represents the supreme design and engineering policy for the Wspólnota Rodzin Kozanów project. All specifications, implementation plans, tasks, and code contributions must comply with the principles outlined above. Any amendment to these principles requires an explicit documentation update, semantic version bump, and recorded justification.

- **MAJOR bump**: Removal or fundamental redefinition of core architecture principles (e.g., adding a dynamic backend).
- **MINOR bump**: Adding a new principle or significantly expanding guidance (e.g., formalizing a new design tool or workflow).
- **PATCH bump**: Clarifications, non-semantic wording improvements, or typo corrections.

**Version**: 1.0.0 | **Ratified**: 2026-09-19 | **Last Amended**: 2026-09-19
