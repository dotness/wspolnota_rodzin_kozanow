# Instrukcja Aktualizacji Treści dla Agentów AI (data/content.json)

Ten dokument zawiera zasady i instrukcje dla agentów AI oraz administratorów aktualizujących zawartość strony **Wspólnoty Rodzin** (Wrocław-Kozanów).

---

## 1. Architektura Danych

Cała zawartość dynamiczna strony (dane wspólnoty, filary, terminy spotkań, aktualności i artykuły) znajduje się w pliku:
`data/content.json`

Struktura pliku jest zdefiniowana w kontrakcie JSON Schema:
`specs/001-wspolnota-rodzin-website/contracts/content-schema.json`

Po każdej modyfikacji `data/content.json` należy zaktualizować również plik awaryjny (fallback offline):
`js/content-data.js`
oraz uruchomić walidator:
`python3 scripts/validate_content.py`

---

## 2. Główne Sekcje `data/content.json`

### A. `siteConfig` (Konfiguracja i Nagłówek)
- `siteTitle` (string): Nazwa wspólnoty, np. `"Wspólnota Rodzin"`.
- `slogan` (string): Hasło nagłówkowe, np. `"Razem w wierze, w miłości, na co dzień"`.
- `location` (string): Miejscowość/osiedle, np. `"Wrocław-Kozanów"`.
- `parishName` (string): Parafia, np. `"Parafia św. Jadwigi Śląskiej"`.
- `motto` (string): Motto na wstędze, np. `"Bo rodzina to wielki dar"`.
- `nextMeeting` (object): Informacja o najbliższym spotkaniu:
  - `dateText`: np. `"Niedziela, 15 października 2026, godz. 16:00"`.
  - `locationText`: np. `"Dom Parafialny (sala kominkowa), Kozanów"`.
  - `description`: Krótki opis programu spotkania.

### B. `pillars` (4 Filary Wspólnoty)
Tablica dokładnie 4 obiektów:
- `id`: `"spotkania"`, `"modlitwa"`, `"relacje"`, `"termin"`.
- `title`: Tytuł kafelka (np. `"Wspólne Spotkania"`).
- `subtitle`: Podtytuł (np. `"Formacja i Rozmowy"`).
- `description`: Rozwinięty opis wyświetlany po tapnięciu w kafelek.
- `icon`: Identyfikator ikony (`users`, `heart`, `people`, `calendar`).

### C. `news` (Aktualności / Wpisy Parafialne)
Tablica wpisów w kolejności odwrotnie chronologicznej (najnowsze na początku):
- `id` (string): Unikalny identyfikator, np. `"2026-09-18-intencje"`.
- `title` (string): Pełny tytuł artykułu.
- `date` (string, format `YYYY-MM-DD`): Data publikacji.
- `author` (string, opcjonalnie): Autor wpisu lub źródło (np. `"Parafia Kozanów"`).
- `featuredImage` (string, opcjonalnie): Względna ścieżka do miniatury wpisu w `assets/news/...`.
- `excerpt` (string): Krótkie podsumowanie (1-3 zdania) wyświetlane na kafelku.
- `contentHtml` (string): Pełna treść artykułu w formacie HTML (`<p>`, `<ul>`, `<blockquote>`, `<img>`, `<a>`). **Tylko bezpieczne znaczniki HTML bez skryptów inline.**
- `attachments` (array, opcjonalnie): Lista załączników do pobrania:
  - `name`: Tytuł pliku (np. `"Oświadczenie KEP"`).
  - `path`: Względna ścieżka lokalna (np. `"assets/docs/Oswidczenie-KEP.pdf"`).
  - `sizeText`: Czytelny rozmiar (np. `"249 KB"`).
- `sourceUrl` (string, opcjonalnie): Link do oryginalnego wpisu w serwisie parafialnym.

---

## 3. Procedura Dodawania Nowego Artykułu

1. **Pobierz i zapisz zdjęcia/załączniki lokalnie**:
   - Zdjęcia umieść w katalogu `assets/news/{kolejny_numer_lub_slug}/`.
   - Dokumenty PDF umieść w katalogu `assets/docs/`.
   - *Ważne*: Nie używaj zewnętrznych linków URL do obrazów i załączników – wszystkie zasoby muszą być lokalne.

2. **Edytuj `data/content.json`**:
   - Wstaw nowy obiekt artykułu na **początek** tablicy `news`.
   - Upewnij się, że wszystkie ścieżki względne są poprawne.

3. **Zsynchronizuj `js/content-data.js`**:
   - Wygeneruj zaktualizowany plik JS przy użyciu skryptu:
     ```bash
     python3 scripts/export_js_data.py
     ```
   - Skrypt ten przepisuje `data/content.json` do `window.COMMUNITY_DATA = ...;` zapewniając działanie offline (`file://`).

4. **Zweryfikuj poprawność**:
   - Uruchom walidator schematu:
     ```bash
     python3 scripts/validate_content.py
     ```
   - Uruchom weryfikator zasobów:
     ```bash
     python3 scripts/verify_assets.py
     ```

---

## 4. Zasady Bezpieczeństwa dla Agentów AI

- Nigdy nie wstawiaj zewnętrznych skryptów (`<script>`), atrybutów `onclick` ani stylów CSS w `contentHtml`.
- Dozwolone znaczniki HTML w `contentHtml`: `<p>`, `<br>`, `<strong>`, `<em>`, `<ul>`, `<ol>`, `<li>`, `<a>`, `<blockquote>`, `<h3>`, `<h4>`, `<img>`.
- Ścieżki do plików zawsze muszą być względne bez wiodącego ukośnika (np. `assets/news/...`, nie `/assets/news/...`).
