#!/usr/bin/env python3
"""
scripts/manage_news.py
CLI tool to add, update, list, and remove news articles in Wspólnota Rodzin website.

Usage:
  python3 scripts/manage_news.py list
  python3 scripts/manage_news.py add --title "..." [--date YYYY-MM-DD] [--content "..."] [--image "..."]
  python3 scripts/manage_news.py update --id <id> [--title "..."] [--date YYYY-MM-DD] [--content "..."]
  python3 scripts/manage_news.py remove --id <id> [--delete-assets]
"""

import sys
import os
import re
import json
import shutil
import argparse
import subprocess
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CONTENT_JSON = ROOT_DIR / "data" / "content.json"
ASSETS_DIR = ROOT_DIR / "assets"
NEWS_ASSETS_DIR = ASSETS_DIR / "news"
DOCS_ASSETS_DIR = ASSETS_DIR / "docs"

POLISH_CHAR_MAP = {
    'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
    'Ą': 'a', 'Ć': 'c', 'Ę': 'e', 'Ł': 'l', 'Ń': 'n', 'Ó': 'o', 'Ś': 's', 'Ź': 'z', 'Ż': 'z'
}

def slugify(text: str) -> str:
    for char, replacement in POLISH_CHAR_MAP.items():
        text = text.replace(char, replacement)
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def parse_youtube_info(url: str):
    if not url:
        return None, False
    shorts_match = re.search(r'(?:youtube\.com/shorts/)([a-zA-Z0-9_-]+)', url)
    if shorts_match:
        return shorts_match.group(1), True
    std_match = re.search(r'(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_-]+)', url)
    if std_match:
        return std_match.group(1), False
    return None, False

def download_youtube_thumbnail(video_id: str, dest_path: Path) -> bool:
    urls = [
        f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        f"https://img.youtube.com/vi/{video_id}/sddefault.jpg",
        f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    ]
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                if resp.status == 200:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(dest_path, "wb") as f:
                        f.write(resp.read())
                    return True
        except Exception:
            continue
    return False

def generate_youtube_embed_html(video_id: str, title: str, is_shorts: bool, full_url: str) -> str:
    container_class = "video-embed-container" if is_shorts else "video-embed-container is-horizontal"
    yt_cta_text = "Otwórz w aplikacji YouTube" if is_shorts else "Obejrzyj na YouTube"
    return (
        f'<div class="video-embed-wrapper">\n'
        f'  <div class="{container_class}">\n'
        f'    <iframe src="https://www.youtube.com/embed/{video_id}?rel=0" title="{title}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>\n'
        f'  </div>\n'
        f'</div>\n\n'
        f'<p style="text-align: center; margin: 16px 0;">\n'
        f'  <a href="{full_url}" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 8px; font-weight: 700; color: #c75d2c; text-decoration: none; font-size: 0.95rem;">\n'
        f'    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">\n'
        f'      <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>\n'
        f'    </svg>\n'
        f'    {yt_cta_text}\n'
        f'  </a>\n'
        f'</p>'
    )

def load_data():
    if not CONTENT_JSON.exists():
        raise FileNotFoundError(f"{CONTENT_JSON} does not exist!")
    with open(CONTENT_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(CONTENT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # Sync fallback js
    export_script = ROOT_DIR / "scripts" / "export_js_data.py"
    if export_script.exists():
        subprocess.run([sys.executable, str(export_script)], check=True)
    # Validate
    validate_script = ROOT_DIR / "scripts" / "validate_content.py"
    if validate_script.exists():
        subprocess.run([sys.executable, str(validate_script)], check=True)

def find_article(news_list, identifier):
    id_str = str(identifier).strip()
    for item in news_list:
        if str(item.get("id")) == id_str or item.get("slug") == id_str:
            return item
    return None

def generate_new_id(news_list):
    int_ids = []
    for item in news_list:
        item_id = item.get("id")
        if isinstance(item_id, int):
            int_ids.append(item_id)
        elif isinstance(item_id, str) and item_id.isdigit():
            int_ids.append(int(item_id))
    if int_ids:
        return max(int_ids) + 1
    return 19400

def list_news(args):
    data = load_data()
    news = data.get("news", [])
    if args.json:
        print(json.dumps(news, ensure_ascii=False, indent=2))
        return

    print(f"\nTotal articles: {len(news)}")
    print("=" * 80)
    for idx, item in enumerate(news, 1):
        item_id = item.get("id")
        d = item.get("date", "N/A")
        title = item.get("title", "Untitled")
        slug = item.get("slug", "")
        img = item.get("featuredImage") or "None"
        attachments = item.get("attachments", [])
        att_str = f"({len(attachments)} doc)" if attachments else ""
        print(f"[{idx:2d}] ID: {item_id:<7} | Date: {d} | {att_str:<8} | Title: {title}")
        print(f"     Slug: {slug}")
        if img != "None":
            print(f"     Image: {img}")
    print("=" * 80 + "\n")

def add_news(args):
    data = load_data()
    news = data.get("news", [])

    new_id = generate_new_id(news)
    title = args.title.strip()
    date_str = args.date.strip() if args.date else date.today().isoformat()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        raise ValueError(f"Invalid date format: '{date_str}'. Expected YYYY-MM-DD.")

    slug = args.slug.strip() if args.slug else slugify(title)

    # Content
    content_html = ""
    if args.content_file:
        c_path = Path(args.content_file).resolve()
        if not c_path.exists():
            raise FileNotFoundError(f"Content file {c_path} not found.")
        content_html = c_path.read_text(encoding="utf-8")
    elif args.content:
        content_html = args.content.strip()
        if not ("<p>" in content_html or "<div" in content_html):
            content_html = f"<p>{content_html}</p>"

    # Excerpt
    excerpt = args.excerpt.strip() if args.excerpt else ""
    if not excerpt and content_html:
        clean_text = re.sub(r'<[^>]+>', '', content_html).strip()
        excerpt = (clean_text[:140] + "...") if len(clean_text) > 140 else clean_text

    # Image handling
    featured_image = ""
    if args.image:
        img_src = Path(args.image).resolve()
        if img_src.exists():
            dest_dir = NEWS_ASSETS_DIR / f"{new_id}"
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file = dest_dir / img_src.name
            shutil.copy2(img_src, dest_file)
            featured_image = f"assets/news/{new_id}/{dest_file.name}"
            print(f"Copied image to {featured_image}")
        elif (ROOT_DIR / args.image).exists():
            featured_image = args.image
        else:
            raise FileNotFoundError(f"Image not found at {args.image}")

    # Attachments
    attachments = []
    if args.attachment:
        DOCS_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        for att in args.attachment:
            att_path = Path(att).resolve()
            if not att_path.exists():
                raise FileNotFoundError(f"Attachment file not found: {att}")
            dest_att = DOCS_ASSETS_DIR / att_path.name
            shutil.copy2(att_path, dest_att)
            size_kb = f"{round(dest_att.stat().st_size / 1024)} KB"
            attachments.append({
                "name": att_path.stem.replace('-', ' ').title(),
                "path": f"assets/docs/{dest_att.name}",
                "type": "pdf" if dest_att.suffix.lower() == ".pdf" else "doc",
                "size": size_kb
            })
            print(f"Copied attachment to assets/docs/{dest_att.name} ({size_kb})")

    # YouTube & Video handling
    is_video = getattr(args, 'is_video', False)
    yt_url = getattr(args, 'youtube_url', None)
    if yt_url:
        is_video = True
        video_id, is_shorts = parse_youtube_info(yt_url)
        if video_id:
            # If no manual image provided, try to download YouTube thumbnail
            if not featured_image:
                dest_dir = NEWS_ASSETS_DIR / f"{new_id}"
                thumb_dest = dest_dir / "cover.jpg"
                if download_youtube_thumbnail(video_id, thumb_dest):
                    featured_image = f"assets/news/{new_id}/cover.jpg"
                    print(f"Downloaded YouTube thumbnail to {featured_image}")
            # Inject embed HTML if not already present in content_html
            if "<iframe" not in content_html:
                embed_block = generate_youtube_embed_html(video_id, title, is_shorts, yt_url)
                content_html = f"{content_html}\n\n{embed_block}".strip() if content_html else embed_block
            if not args.source_url:
                args.source_url = yt_url

    new_article = {
        "id": new_id,
        "title": title,
        "date": date_str,
        "author": args.author or "Wspólnota Rodzin",
        "slug": slug,
        "featuredImage": featured_image,
        "isVideo": is_video,
        "excerpt": excerpt,
        "contentHtml": content_html,
        "sourceUrl": args.source_url or "",
        "attachments": attachments
    }

    news.insert(0, new_article)
    # Ensure sorted by date descending
    news.sort(key=lambda x: str(x.get("date", "")), reverse=True)
    data["news"] = news
    save_data(data)
    print(f"\n✅ Article created successfully! ID: {new_id}, Title: '{title}', Date: {date_str}")

def update_news(args):
    data = load_data()
    news = data.get("news", [])
    target = find_article(news, args.id)
    if not target:
        raise ValueError(f"No article found with ID or slug matching '{args.id}'.")

    if args.title:
        target["title"] = args.title.strip()
    if args.date:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", args.date.strip()):
            raise ValueError(f"Invalid date format: '{args.date}'. Expected YYYY-MM-DD.")
        target["date"] = args.date.strip()
    if args.author:
        target["author"] = args.author.strip()
    if args.slug:
        target["slug"] = args.slug.strip()
    if args.excerpt is not None:
        target["excerpt"] = args.excerpt.strip()

    if args.content_file:
        c_path = Path(args.content_file).resolve()
        if not c_path.exists():
            raise FileNotFoundError(f"Content file {c_path} not found.")
        target["contentHtml"] = c_path.read_text(encoding="utf-8")
    elif args.content is not None:
        content_html = args.content.strip()
        if content_html and not ("<p>" in content_html or "<div" in content_html):
            content_html = f"<p>{content_html}</p>"
        target["contentHtml"] = content_html

    if args.image:
        img_src = Path(args.image).resolve()
        if img_src.exists():
            dest_dir = NEWS_ASSETS_DIR / f"{target['id']}"
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file = dest_dir / img_src.name
            shutil.copy2(img_src, dest_file)
            target["featuredImage"] = f"assets/news/{target['id']}/{dest_file.name}"
            print(f"Updated image to {target['featuredImage']}")
        elif (ROOT_DIR / args.image).exists():
            target["featuredImage"] = args.image
        else:
            raise FileNotFoundError(f"Image not found at {args.image}")

    if args.clear_image:
        target["featuredImage"] = ""

    if args.attachment:
        DOCS_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        if "attachments" not in target or not isinstance(target["attachments"], list):
            target["attachments"] = []
        for att in args.attachment:
            att_path = Path(att).resolve()
            if not att_path.exists():
                raise FileNotFoundError(f"Attachment file not found: {att}")
            dest_att = DOCS_ASSETS_DIR / att_path.name
            shutil.copy2(att_path, dest_att)
            size_kb = f"{round(dest_att.stat().st_size / 1024)} KB"
            target["attachments"].append({
                "name": att_path.stem.replace('-', ' ').title(),
                "path": f"assets/docs/{dest_att.name}",
                "type": "pdf" if dest_att.suffix.lower() == ".pdf" else "doc",
                "size": size_kb
            })
            print(f"Added attachment {dest_att.name} ({size_kb})")

    if getattr(args, 'is_video', None) is not None:
        target["isVideo"] = args.is_video
    if getattr(args, 'youtube_url', None):
        target["isVideo"] = True
        video_id, is_shorts = parse_youtube_info(args.youtube_url)
        if video_id:
            if not target.get("featuredImage") and not args.image:
                dest_dir = NEWS_ASSETS_DIR / f"{target['id']}"
                thumb_dest = dest_dir / "cover.jpg"
                if download_youtube_thumbnail(video_id, thumb_dest):
                    target["featuredImage"] = f"assets/news/{target['id']}/cover.jpg"
                    print(f"Downloaded YouTube thumbnail to {target['featuredImage']}")
            if "<iframe" not in (target.get("contentHtml") or "") and not args.content and not args.content_file:
                embed_block = generate_youtube_embed_html(video_id, target["title"], is_shorts, args.youtube_url)
                target["contentHtml"] = f"{target.get('contentHtml', '')}\n\n{embed_block}".strip()
            if not target.get("sourceUrl"):
                target["sourceUrl"] = args.youtube_url

    # Re-sort by date descending
    news.sort(key=lambda x: str(x.get("date", "")), reverse=True)
    data["news"] = news
    save_data(data)
    print(f"\n✅ Article {target['id']} ('{target['title']}') updated successfully.")

def remove_news(args):
    data = load_data()
    news = data.get("news", [])
    target = find_article(news, args.id)
    if not target:
        raise ValueError(f"No article found with ID or slug matching '{args.id}'.")

    target_id = target.get("id")
    target_title = target.get("title")

    news = [item for item in news if str(item.get("id")) != str(target_id)]
    data["news"] = news

    if args.delete_assets:
        target_dir = NEWS_ASSETS_DIR / f"{target_id}"
        if target_dir.exists() and target_dir.is_dir():
            shutil.rmtree(target_dir)
            print(f"Deleted assets folder: {target_dir}")

    save_data(data)
    print(f"\n✅ Article {target_id} ('{target_title}') removed successfully.")

def main():
    parser = argparse.ArgumentParser(description="Manage Wspólnota Rodzin News Content")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = subparsers.add_parser("list", help="List all news articles")
    p_list.add_argument("--json", action="store_true", help="Output as JSON")
    p_list.set_defaults(func=list_news)

    # add
    p_add = subparsers.add_parser("add", help="Add a new news article")
    p_add.add_argument("--title", required=True, help="Title of the news article")
    p_add.add_argument("--date", help="Publication date (YYYY-MM-DD, defaults to today)")
    p_add.add_argument("--author", default="Wspólnota Rodzin", help="Author name")
    p_add.add_argument("--slug", help="URL-friendly slug (auto-generated if omitted)")
    p_add.add_argument("--excerpt", help="Short summary/excerpt")
    p_add.add_argument("--content", help="Article body (text or HTML)")
    p_add.add_argument("--content-file", help="Path to text or HTML file containing body")
    p_add.add_argument("--image", help="Path to local image file to use as featured image")
    p_add.add_argument("--attachment", action="append", help="Path to attachment (e.g. PDF). Can be specified multiple times.")
    p_add.add_argument("--source-url", help="Original source URL if applicable")
    p_add.add_argument("--youtube-url", help="YouTube video or Shorts URL (e.g. https://www.youtube.com/shorts/...)")
    p_add.add_argument("--is-video", action="store_true", help="Mark article as a video (adds Play overlay and Wideo badge to timeline tile)")
    p_add.set_defaults(func=add_news)

    # update
    p_up = subparsers.add_parser("update", help="Update an existing news article")
    p_up.add_argument("--id", required=True, help="Article ID or slug")
    p_up.add_argument("--title", help="New title")
    p_up.add_argument("--date", help="New date (YYYY-MM-DD)")
    p_up.add_argument("--author", help="New author")
    p_up.add_argument("--slug", help="New slug")
    p_up.add_argument("--excerpt", help="New excerpt")
    p_up.add_argument("--content", help="New content string or HTML")
    p_up.add_argument("--content-file", help="Path to file containing new content")
    p_up.add_argument("--image", help="Path to new featured image")
    p_up.add_argument("--clear-image", action="store_true", help="Remove featured image")
    p_up.add_argument("--attachment", action="append", help="Add attachment(s)")
    p_up.add_argument("--youtube-url", help="YouTube video or Shorts URL to embed")
    p_up.add_argument("--is-video", type=lambda x: (str(x).lower() in ['true', '1', 'yes']), help="Set isVideo (true/false)")
    p_up.set_defaults(func=update_news)

    # remove
    p_rm = subparsers.add_parser("remove", help="Remove a news article")
    p_rm.add_argument("--id", required=True, help="Article ID or slug")
    p_rm.add_argument("--delete-assets", action="store_true", help="Also delete image directory under assets/news/<id>")
    p_rm.set_defaults(func=remove_news)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
