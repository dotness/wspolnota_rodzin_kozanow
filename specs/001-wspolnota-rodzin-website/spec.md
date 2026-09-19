# Feature Specification: Wspólnota Rodzin Mobile Website

**Feature Branch**: `001-wspolnota-rodzin-website`

**Created**: 2026-09-19

**Status**: Draft

**Input**: User description: "I want you to create a new website, that i can host in OVH web hosting service , i dont want any backend, just frontend. I will update the content with AI Agents. I want the website to look like website_reference, but the top header is to be about polish Wspolnota Rodzin from headline_reference.png. I want you to add 10 news from news_reference to this new website. Keep the style as website_reference, i like the tiles lines and overall feeling - it will be only mobile for now."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Community Branding and Pillars (Priority: P1)

As a parishioner or visiting family on a mobile device, I want to immediately see the "Wspólnota Rodzin" header, community motto, and core pillars so that I understand who the community is, what values they represent, and when the next gathering takes place.

**Why this priority**: The header sets the identity and purpose of the website. It welcomes families and establishes the Kozanów community presence inspired by the official parish community materials.

**Independent Test**: Can be validated by opening the page on any mobile screen (or viewport <= 600px); delivers immediate recognition of "Wspólnota Rodzin", the Kozanów parish affiliation, the four core community pillars, and next meeting information.

**Acceptance Scenarios**:

1. **Given** a user opens the website on a mobile device, **When** the page loads, **Then** the header displays the community title "Wspólnota Rodzin", the subtitle "Razem w wierze, w miłości, na co dzień", the parish attribution ("Parafia św. Jadwigi Śląskiej – Wrocław Kozanów"), and the visual imagery inspired by the parish reference.
2. **Given** the user views the header, **When** scrolling through the top section, **Then** four clearly demarcated tiles/pillars are presented: "Wspólne Spotkania", "Rodzinna Modlitwa", "Przyjaźnie i Relacje", and "Następne Spotkanie", along with the closing quote "Bo rodzina to wielki dar".

---

### User Story 2 - Browse and Read 10 Parish News Entries (Priority: P1)

As a community member, I want to read the 10 latest news articles and parish announcements presented in clean, segmented tiles similar to the reference design, so that I can stay up to date with parish life.

**Why this priority**: News and announcements are the primary dynamic content that families visit the website to check regularly.

**Independent Test**: Can be verified by browsing the chronological feed of 10 articles; each article provides its title, publication date, featured image, excerpt, and full readable content with local media assets.

**Acceptance Scenarios**:

1. **Given** the user scrolls past the header, **When** reviewing the news feed, **Then** exactly 10 latest news entries from the Kozanów parish archive are displayed in descending chronological order.
2. **Given** a news entry tile with an image, **When** viewed on mobile, **Then** the image scales proportionally within the tile boundary with clean borders and dividers matching the reference visual style.
3. **Given** an entry containing documents or external references (such as episcopal statements or prayer vigils), **When** clicked, **Then** the user can read the full text and access associated attachments directly.

---

### User Story 3 - AI-Agent Content Updatability and Maintenance (Priority: P2)

As a website maintainer using AI agents, I want the website's content and structure to be completely decoupled from complex build tools or proprietary CMS databases, so that an AI agent can reliably read, append, update, or prune news items and community announcements using plain structured files.

**Why this priority**: Ensures long-term sustainability without requiring full-stack developer intervention or complex backend infrastructure.

**Independent Test**: Can be validated by modifying a structured content file (e.g., adding an 11th article or editing the "Następne Spotkanie" date) and confirming that the site updates automatically without build failures or broken markup.

**Acceptance Scenarios**:

1. **Given** an AI agent tasked with updating the news feed, **When** inspecting the repository, **Then** it finds a clean, well-documented static data structure containing all news items and header configurations.
2. **Given** an update made to a news item or community banner, **When** the files are saved, **Then** the updated content renders cleanly without requiring server restarts or backend compilation.

---

### User Story 4 - Seamless Static Hosting Deployment (Priority: P2)

As a site administrator, I want the website to consist entirely of static frontend assets (HTML, CSS, JavaScript, media) capable of running on standard OVH web hosting, so that deployment requires nothing more than copying files to the public hosting directory (`public_html` / `www`).

**Why this priority**: Eliminates server-side runtime vulnerabilities, database connection overhead, maintenance downtime, and hosting cost spikes.

**Independent Test**: Can be verified by serving the distribution directory via any zero-configuration static file server or standard HTTP file hosting; all internal links, images, and fonts load with HTTP 200 without backend dependencies.

**Acceptance Scenarios**:

1. **Given** the site files uploaded to an OVH shared hosting directory, **When** requested by a web browser over HTTPS, **Then** all assets, styles, and images load successfully without 404 errors or reliance on PHP/Node/database backends.

---

### Edge Cases

- **Slow mobile network connectivity**: Images and assets must be sized appropriately to ensure fast initial render even on 3G/4G connections.
- **Missing or optional article images**: Articles without a featured image must maintain consistent card spacing, typographic balance, and visual appeal without broken image icons.
- **Very long article text**: Long titles or multi-paragraph statements must wrap properly and remain legible without breaking container borders or horizontal overflow on narrow screens (320px–420px).
- **Offline or restrictive browser viewing**: All media and fonts must be locally bundled or resilient so that no third-party tracker or blocked CDN breaks the page presentation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The website MUST be implemented strictly as a client-side static frontend (HTML, CSS, client JavaScript) requiring no backend language runtimes (PHP, Node.js, Python) or database engines (MySQL, PostgreSQL).
- **FR-002**: The website MUST be optimized for mobile devices, constrained to a centered mobile canvas (maximum 600px width) mirroring the layout, tile borders, horizontal dividers, and visual rhythm of `website_reference`.
- **FR-003**: The top header MUST feature the Polish "Wspólnota Rodzin" identity derived from `headline_reference.png`, including:
  - Community name: "Wspólnota Rodzin"
  - Slogan: "Razem w wierze, w miłości, na co dzień"
  - Parish attribution: "Parafia św. Jadwigi Śląskiej – Wrocław Kozanów"
  - Core community pillars: "Wspólne Spotkania", "Rodzinna Modlitwa", "Przyjaźnie i Relacje", and "Następne Spotkanie"
  - Community motto: "Bo rodzina to wielki dar"
- **FR-004**: The website MUST include the 10 latest news entries extracted from `news_reference`, ordered from newest to oldest.
- **FR-005**: Each news entry MUST display its publication date, title, featured imagery (when available), text content or excerpt, and any relevant links or document attachments.
- **FR-006**: All media assets (photos, icons, logos, attachments) MUST be stored locally within the website repository and referenced via relative paths.
- **FR-007**: The news content and header configuration MUST be stored in a clean, human- and agent-readable data structure (such as structured JSON or Markdown) to enable seamless updates by AI agents.
- **FR-008**: The site MUST support full text viewing for each article without breaking the mobile reading flow (either through clean in-page expandable tiles, accessible modal dialogs, or dedicated lightweight mobile article views).
- **FR-009**: The layout MUST prevent any horizontal scrolling on mobile viewports ranging from 320px up to full tablet/desktop dimensions.
- **FR-010**: The visual design MUST preserve the clean white/light neutral background, crisp divider lines, balanced padding, and card outlines established in `website_reference`.
- **FR-011**: The website MUST be ready for direct deployment to OVH shared web hosting by placing files directly into the web root directory.
- **FR-012**: The site MUST include appropriate Polish language meta tags (`lang="pl"`), responsive viewport configuration, title, and descriptive metadata for search engines and social sharing.

### Key Entities

- **CommunityProfile**: Represents the header metadata and identity (community name, parish name, motto, theme imagery, and status of upcoming meetings).
- **CommunityPillar**: Represents a core activity or value of the family community (title, subtitle/tags, icon representation).
- **NewsItem**: Represents a parish news entry (unique identifier, publication date, title, slug, featured image relative path, summary/excerpt, full body content, external references, and file attachments).
- **Attachment**: Represents downloadable files associated with an announcement (filename, relative file path, document type, file size).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the 10 reference news articles and associated images/attachments are visible and accessible directly on the website.
- **SC-002**: First contentful paint and complete page load occurs in under 1.5 seconds on standard 4G mobile network conditions.
- **SC-003**: Zero layout shifts or horizontal scrollbars occur across mobile viewports from 320px to 480px width.
- **SC-004**: An AI agent can add a new article or update an existing announcement by editing a single designated content file in under 30 seconds without modifying core layout templates.
- **SC-005**: 100% of internal links, images, and downloadable assets resolve with HTTP 200 status when served from a standard static web server.
- **SC-006**: The website passes standard web accessibility and mobile usability audits without contrast or tap-target violations.

## Assumptions

- **Target Audience**: Families and parishioners of Parafia św. Jadwigi on Kozanów accessing the site primarily on smartphones.
- **Mobile-First Scope**: The initial release focuses on mobile viewport presentation (up to 600px width, centered on larger screens like newsletter previews). A multi-column desktop layout is explicitly out of scope for this version.
- **Hosting Environment**: Standard OVH web hosting with static file delivery (Apache/Nginx serving static HTML/CSS/JS/images).
- **Content Updates**: Content is authored and updated statically by maintainers or AI agents by committing changes to the project files, which are then uploaded to OVH via FTP or automated CI/CD deployment.
- **Offline & Self-Contained**: External API dependencies (like a live WordPress query or third-party tracking scripts) are avoided to ensure the site remains fast, resilient, and fully functional indefinitely.
