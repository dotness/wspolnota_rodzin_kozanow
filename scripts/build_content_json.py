import json
import re
import html
from pathlib import Path

base = Path(__file__).resolve().parent.parent
news_ref_json = base / 'news_reference' / 'all_posts.json'
output_json = base / 'data' / 'content.json'

with open(news_ref_json, 'r', encoding='utf-8') as f:
    posts = json.load(f)

news_items = []

for idx, p in enumerate(posts, 1):
    p_id = p.get('id')
    p_date = p.get('date', '')[:10]
    p_title = html.unescape(p.get('title', {}).get('rendered', '')).strip()
    p_slug = p.get('slug', f'post-{p_id}')
    p_link = p.get('link', '')
    raw_content = p.get('content', {}).get('rendered', '')
    
    # Excerpt
    raw_excerpt = html.unescape(re.sub(r'<[^>]+>', '', p.get('excerpt', {}).get('rendered', '')).strip())
    raw_excerpt = re.sub(r'\s+', ' ', raw_excerpt)
    if not raw_excerpt:
        raw_excerpt = html.unescape(re.sub(r'<[^>]+>', '', raw_content).strip())
        raw_excerpt = raw_excerpt[:160] + "..." if len(raw_excerpt) > 160 else raw_excerpt

    # Author
    author_info = p.get('_embedded', {}).get('author', [])
    author_name = author_info[0].get('name', 'Redakcja') if author_info else 'Redakcja'

    # Featured image
    feat_media = p.get('_embedded', {}).get('wp:featuredmedia', [])
    feat_src = feat_media[0].get('source_url', '') if feat_media else ''
    
    # Find local image
    news_dir = base / 'assets' / 'news' / f'{idx:02d}'
    local_images = list(news_dir.glob('*.jpg')) + list(news_dir.glob('*.png'))
    
    featured_img_path = None
    if local_images:
        # Prefer image with same name or first available
        if feat_src:
            feat_name = Path(feat_src.split('?')[0]).name
            for img in local_images:
                if img.name == feat_name:
                    featured_img_path = f"assets/news/{idx:02d}/{img.name}"
                    break
        if not featured_img_path:
            featured_img_path = f"assets/news/{idx:02d}/{local_images[0].name}"

    # Localize contentHtml
    content_html = raw_content
    if featured_img_path:
        # Replace original urls with relative path
        for img in local_images:
            content_html = re.sub(
                rf'https?://[^"\']*/{re.escape(img.name)}',
                f'assets/news/{idx:02d}/{img.name}',
                content_html
            )
    
    # Attachments (specifically for post 3)
    attachments = []
    if idx == 3:
        attachments = [
            {
                "name": "Oświadczenie KEP – Młody człowiek zasługuje na więcej",
                "path": "assets/docs/Oswidczenie-KEP.pdf",
                "type": "pdf",
                "sizeText": "249 KB"
            },
            {
                "name": "Apel Rady Stałej Biskupów w sprawie pojednania",
                "path": "assets/docs/Apel-Rady.pdf",
                "type": "pdf",
                "sizeText": "144 KB"
            }
        ]
        # Localize PDF links in content
        content_html = content_html.replace(
            "https://www.jadwigakozanow.pl/wp-content/uploads/2026/09/Oswidczenie-KEP.pdf",
            "assets/docs/Oswidczenie-KEP.pdf"
        ).replace(
            "https://www.jadwigakozanow.pl/wp-content/uploads/2026/09/Apel-Rady.pdf",
            "assets/docs/Apel-Rady.pdf"
        )

    news_items.append({
        "id": p_id,
        "title": p_title,
        "date": p_date,
        "author": author_name,
        "slug": p_slug,
        "featuredImage": featured_img_path,
        "excerpt": raw_excerpt,
        "contentHtml": content_html,
        "sourceUrl": p_link,
        "attachments": attachments
    })

data = {
    "siteConfig": {
        "siteTitle": "Wspólnota Rodzin – Kozanów",
        "parishName": "Parafia pw. św. Jadwigi Śląskiej",
        "location": "Wrocław – Kozanów",
        "slogan": "Razem w wierze, w miłości, na co dzień",
        "motto": "Bo rodzina to wielki dar",
        "headerImage": "assets/images/header/wspolnota_rodzin_header.png",
        "nextMeeting": {
            "title": "Najbliższe spotkanie Wspólnoty Rodzin",
            "dateText": "Niedziela, 20 września 2026 r., godz. 16:00",
            "locationText": "Salka parafialna pod kościołem św. Jadwigi",
            "description": "Serdecznie zapraszamy wszystkie rodziny, małżeństwa i dzieci na modlitwę, rozmowę, wsparcie i wspólny poczęstunek."
        }
    },
    "pillars": [
        {
            "id": "spotkania",
            "title": "WSPÓLNE SPOTKANIA",
            "subtitle": "modlitwa • rozmowa • wsparcie",
            "description": "Budujemy wspólnotę opartą na zaufaniu i chrześcijańskich wartościach. Razem modlimy się, rozmawiamy o wyzwaniach codzienności i wzajemnie wspieramy.",
            "icon": "users"
        },
        {
            "id": "modlitwa",
            "title": "RODZINNA MODLITWA",
            "subtitle": "w parafii i w domach",
            "description": "Odkrywamy głębię modlitwy we wspólnocie małżeńskiej i rodzinnej. Uczymy się czerpać siłę z Eucharystii i Słowa Bożego na każdy dzień.",
            "icon": "heart"
        },
        {
            "id": "relacje",
            "title": "PRZYJAŹNIE I RELACJE",
            "subtitle": "z innymi rodzinami",
            "description": "Dajemy dzieciom bezpieczne środowisko rówieśnicze, a rodzicom przestrzeń do budowania głębokich, wartościowych przyjaźni.",
            "icon": "people"
        },
        {
            "id": "termin",
            "title": "NASTĘPNE SPOTKANIE",
            "subtitle": "Niedziela, 20 września, 16:00",
            "description": "Nasze spotkania są otwarte dla każdego. Przyjdź i zobacz – czekamy na Ciebie i Twoją rodzinę w salce parafialnej!",
            "icon": "calendar"
        }
    ],
    "news": news_items
}

output_json.parent.mkdir(parents=True, exist_ok=True)
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {output_json} with {len(news_items)} articles.")
