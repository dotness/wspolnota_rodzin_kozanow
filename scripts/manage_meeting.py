#!/usr/bin/env python3
"""
scripts/manage_meeting.py
CLI tool to show, update, and remove the "Najbliższe Spotkanie Wspólnoty" notice in Wspólnota Rodzin website.

Usage:
  python3 scripts/manage_meeting.py show
  python3 scripts/manage_meeting.py update --date "Niedziela, 27 września 2026..." --title "..." [--image "..."] [--content "..."]
  python3 scripts/manage_meeting.py remove
"""

import sys
import os
import json
import shutil
import argparse
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CONTENT_JSON = ROOT_DIR / "data" / "content.json"
MEETING_ASSETS_DIR = ROOT_DIR / "assets" / "images" / "meeting"

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

def show_meeting(args):
    data = load_data()
    nm = data.get("siteConfig", {}).get("nextMeeting")
    if not nm:
        print("\n[ℹ️] No next meeting currently scheduled.")
        print("The 'Najbliższe Spotkanie Wspólnoty' section is currently hidden on the website.\n")
        return

    print("\n" + "=" * 60)
    print("NAJBLIŻSZE SPOTKANIE WSPÓLNOTY (CURRENT CONFIG)")
    print("=" * 60)
    print(f"Title:       {nm.get('title', 'N/A')}")
    print(f"Date:        {nm.get('dateText', 'N/A')}")
    print(f"Location:    {nm.get('locationText', 'N/A')}")
    print(f"Image:       {nm.get('image', 'None (no poster image)')}")
    print(f"Description: {nm.get('description', '')}")
    if nm.get('contentHtml'):
        print(f"Modal HTML:  {len(nm['contentHtml'])} characters defined")
    print("=" * 60 + "\n")

def update_meeting(args):
    data = load_data()
    cfg = data.setdefault("siteConfig", {})
    existing = cfg.get("nextMeeting") or {}

    title = args.title.strip() if args.title else existing.get("title", "Spotkanie u św. Jadwigi – Wspólnota Rodzin")
    date_text = args.date.strip() if args.date else existing.get("dateText")
    if not date_text:
        raise ValueError("Missing required meeting date. Specify via --date '...'")

    location_text = args.location.strip() if args.location else existing.get("locationText", "Salka parafialna pod kościołem św. Jadwigi")

    # Image
    image_path = existing.get("image", "")
    if args.clear_image:
        image_path = ""
    elif args.image:
        src = Path(args.image).resolve()
        if src.exists():
            MEETING_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
            dest = MEETING_ASSETS_DIR / src.name
            shutil.copy2(src, dest)
            image_path = f"assets/images/meeting/{dest.name}"
            print(f"Copied meeting image to {image_path}")
        elif (ROOT_DIR / args.image).exists():
            image_path = args.image
        else:
            raise FileNotFoundError(f"Meeting image file not found at {args.image}")

    # Description
    desc = args.description.strip() if args.description else existing.get("description", "")

    # Content HTML (Modal details)
    content_html = existing.get("contentHtml", "")
    if args.content_file:
        c_path = Path(args.content_file).resolve()
        if not c_path.exists():
            raise FileNotFoundError(f"Content file {c_path} not found.")
        content_html = c_path.read_text(encoding="utf-8")
    elif args.content is not None:
        raw_c = args.content.strip()
        if raw_c and not ("<p>" in raw_c or "<div" in raw_c):
            content_html = f"<p>{raw_c}</p>"
        else:
            content_html = raw_c

    cfg["nextMeeting"] = {
        "title": title,
        "dateText": date_text,
        "locationText": location_text,
        "image": image_path,
        "description": desc,
        "contentHtml": content_html
    }

    save_data(data)
    print(f"\n✅ Next meeting updated successfully!")
    print(f"   Title: {title}")
    print(f"   Date:  {date_text}")
    print(f"   Place: {location_text}")
    if image_path:
        print(f"   Image: {image_path}")

def remove_meeting(args):
    data = load_data()
    cfg = data.setdefault("siteConfig", {})
    if not cfg.get("nextMeeting"):
        print("\n[ℹ️] No scheduled next meeting to remove.")
        return

    cfg["nextMeeting"] = None
    save_data(data)
    print("\n✅ Next meeting notice removed successfully.")
    print("The 'Najbliższe Spotkanie Wspólnoty' section will now be hidden on the website.")

def main():
    parser = argparse.ArgumentParser(description="Manage Next Meeting Info ('Najbliższe Spotkanie Wspólnoty')")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # show
    p_show = subparsers.add_parser("show", help="Show current next meeting information")
    p_show.set_defaults(func=show_meeting)

    # update
    p_up = subparsers.add_parser("update", help="Update next meeting information")
    p_up.add_argument("--date", help="Date & time description (e.g. 'Niedziela, 27 września 2026 r., po Mszy św. o godz. 10:30')")
    p_up.add_argument("--title", help="Title of the meeting announcement")
    p_up.add_argument("--location", help="Location (defaults to 'Salka parafialna pod kościołem św. Jadwigi')")
    p_up.add_argument("--image", help="Poster image file or path")
    p_up.add_argument("--clear-image", action="store_true", help="Remove existing poster image")
    p_up.add_argument("--description", help="Short summary / invitation line")
    p_up.add_argument("--content", help="Modal HTML or text details")
    p_up.add_argument("--content-file", help="Path to text/HTML file containing modal details")
    p_up.set_defaults(func=update_meeting)

    # remove
    p_rm = subparsers.add_parser("remove", help="Remove / hide next meeting notice")
    p_rm.set_defaults(func=remove_meeting)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
