# Quickstart & Verification Guide: Wspólnota Rodzin Mobile Website

**Feature**: `001-wspolnota-rodzin-website`  
**Date**: 2026-09-19  

## Prerequisites

- Any modern web browser (Google Chrome, Firefox, Safari, Edge).
- Python 3 (standard on Linux/macOS) or any static file server for local HTTP preview.

---

## Local Development & Preview

### 1. Start Local Static Server
From the workspace root directory:

```bash
# Launch a lightweight zero-dependency local HTTP server
python3 -m http.server 8000
```

### 2. View in Browser
Open `http://localhost:8000` in your web browser.
- Open Developer Tools (`F12` or `Ctrl+Shift+I`).
- Switch to Device Emulation mode (`Ctrl+Shift+M`) and select a mobile device preset (e.g. *iPhone 14*, *Pixel 7*, or *375x667*).

---

## Validation Scenarios

### Scenario 1: Branding & Header Verification
1. Load `http://localhost:8000/`.
2. Verify that the top header showcases:
   - "Wspólnota Rodzin" title and church-heart emblem.
   - Subtitle "Razem w wierze, w miłości, na co dzień".
   - 4 pillar tiles: "Wspólne Spotkania", "Rodzinna Modlitwa", "Przyjaźnie i Relacje", and "Następne Spotkanie".
   - Banner motto "Bo rodzina to wielki dar".

### Scenario 2: News Feed & Media Loading
1. Scroll down to the "Aktualności i Ogłoszenia" section.
2. Confirm exactly 10 cards are rendered in reverse chronological order.
3. Check that images load with HTTP 200 from local `assets/` relative paths.
4. Click "Czytaj całość" on an article (e.g., Post 3: "Oświadczenie KEP i Apel Rady Biskupów").
5. Verify the modal opens smoothly and the PDF attachment links ("Oświadczenie KEP", "Apel Rady") are clickable and download the local PDFs.

### Scenario 3: AI-Agent Content Update Simulation
1. Edit `data/content.json`.
2. Change the `nextMeeting.dateText` value to `"Niedziela, 27 września, godz. 17:00"`.
3. Refresh the browser at `http://localhost:8000`.
4. Verify the updated meeting date immediately reflects in the header tile without requiring any build script.

---

## Deployment to OVH Shared Web Hosting

1. Connect to your OVH Web Hosting via SFTP/FTP (FileZilla or OVH WebFTP).
2. Navigate to the root web folder (usually `www/` or `public_html/`).
3. Upload all files and folders:
   - `index.html`
   - `css/`
   - `js/`
   - `data/`
   - `assets/`
4. Access your domain (e.g., `https://twojadomena.pl/`) to verify live functionality.
