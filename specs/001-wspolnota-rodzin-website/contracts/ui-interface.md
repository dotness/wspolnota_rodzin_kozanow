# UI Interface & Interaction Contracts

**Feature**: `001-wspolnota-rodzin-website`  
**Date**: 2026-09-19  

## Layout & Viewport Specifications

- **Target Device Profile**: Mobile viewport (360px – 430px wide, 375px baseline for iPhone SE / Android).
- **Desktop/Tablet Presentation**: Centered mobile canvas constrained to `max-width: 600px` on light neutral backdrop (`#f4f1ea`), reproducing the clean layout of `website_reference`.
- **Horizontal Overflow**: `overflow-x: hidden` strictly enforced; all components use `box-sizing: border-box`.
- **Design Authority**: All screen mockups, component variants, and design tokens are authored and generated using **Stitch MCP** in accordance with Constitution Principle I.

---

## Component Contracts

### 1. Header Hero (`<header class="community-header">`)
- **Logo / Crest**: Church roof contour with central heart and cross icon.
- **Main Heading**: "Wspólnota Rodzin" styled with warm, welcoming typography.
- **Subtitle**: *"Razem w wierze, w miłości, na co dzień"* followed by delicate heart glyph.
- **Parish Location**: *"Wrocław Kozanów • Parafia św. Jadwigi Śląskiej"*.
- **Background**: Warm brick / sunlight gradient overlay inspired by `headline_reference.png`.

### 2. Pillars Grid (`<section class="pillars-grid">`)
- **Grid Layout**: 2x2 grid on screens >= 360px, collapsing cleanly to 1 column on ultra-compact devices.
- **Pillar Card**:
  - Border: `1px solid rgba(0,0,0,0.08)`, rounded corners (`8px`).
  - Content: Pillar icon, uppercase bold title, sub-label (e.g. `modlitwa • rozmowa • wsparcie`).
  - Interactive Action: Tap opens brief expandable info card explaining the pillar or next meeting details.
- **Banner Banner Quote**: Centered text block: *"Bo rodzina to wielki dar ♡"*.

### 3. News Feed Container (`<main class="news-feed">`)
- **Section Heading**: "Aktualności i Ogłoszenia" with fine horizontal rule divider matching `website_reference`.
- **News Item Card (`<article class="news-card">`)**:
  - **Date Badge**: Clean uppercase date tag (e.g. `14 WRZEŚNIA 2026`).
  - **Title**: Semantically tagged `<h3>`, strong font contrast, line-height 1.35.
  - **Media Preview**: 16:9 or native aspect ratio image with rounded top corners, `object-fit: cover`.
  - **Excerpt**: 2-3 lines of summary text with trailing ellipsis.
  - **Action Link**: "Czytaj całość →" button opening the full reader.

### 4. Article Modal Reader (`<dialog id="article-reader">` or custom overlay)
- **Header**: Sticky/fixed bar with "← Wróć do aktualności" button and close icon.
- **Body**: Complete publication date, author, full HTML body, embedded images with captions.
- **Attachments Box**: Highlighted callout section for PDF attachments (with file icon, document name, and direct download link).
- **History Integration**: Updates URL hash (e.g. `#artykul-19372`) allowing standard browser "Back" gesture to close the modal.

### 5. Community Footer (`<footer class="site-footer">`)
- **Address**: "Parafia św. Jadwigi Śląskiej, ul. Pilczycka 139, 54-144 Wrocław".
- **Contact & Community Info**: Meeting times, link to main parish website.
- **Copyright & Note**: "Wspólnota Rodzin • Wrocław-Kozanów".
