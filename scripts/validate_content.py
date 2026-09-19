#!/usr/bin/env python3
"""
validate_content.py
Validates data/content.json against specs/001-wspolnota-rodzin-website/contracts/content-schema.json
and checks that all local assets (images, attachments) exist on disk.
"""

import sys
import os
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_PATH = BASE_DIR / "data" / "content.json"
SCHEMA_PATH = BASE_DIR / "specs" / "001-wspolnota-rodzin-website" / "contracts" / "content-schema.json"

def validate():
    if not CONTENT_PATH.exists():
        print(f"FAIL: {CONTENT_PATH} does not exist!")
        sys.exit(1)
        
    try:
        with open(CONTENT_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"FAIL: Could not parse JSON from {CONTENT_PATH}: {e}")
        sys.exit(1)

    errors = []

    # 1. Check root properties
    for key in ["siteConfig", "pillars", "news"]:
        if key not in data:
            errors.append(f"Missing root key: '{key}'")

    # 2. Check siteConfig
    cfg = data.get("siteConfig", {})
    for req in ["siteTitle", "parishName", "location", "slogan", "motto"]:
        if req not in cfg or not isinstance(cfg[req], str) or not cfg[req].strip():
            errors.append(f"siteConfig.{req} is missing or empty")

    nm = cfg.get("nextMeeting", {})
    for req in ["title", "dateText", "locationText"]:
        if req not in nm or not isinstance(nm[req], str) or not nm[req].strip():
            errors.append(f"siteConfig.nextMeeting.{req} is missing or empty")

    # 3. Check pillars
    pillars = data.get("pillars", [])
    if not isinstance(pillars, list) or len(pillars) != 4:
        errors.append(f"pillars must be a list of exactly 4 items (found {len(pillars)})")
    else:
        for idx, pil in enumerate(pillars):
            for req in ["id", "title", "subtitle", "description", "icon"]:
                if req not in pil or not pil[req]:
                    errors.append(f"pillar[{idx}].{req} is missing")

    # 4. Check news
    news = data.get("news", [])
    if not isinstance(news, list) or len(news) < 10:
        errors.append(f"news must be a list of at least 10 items (found {len(news)})")
    else:
        for idx, item in enumerate(news):
            for req in ["id", "title", "date", "slug", "excerpt", "contentHtml"]:
                if req not in item or item[req] is None:
                    errors.append(f"news[{idx}].{req} is missing")
            
            # Check date format YYYY-MM-DD
            d = str(item.get("date", ""))
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", d):
                errors.append(f"news[{idx}].date '{d}' is not in YYYY-MM-DD format")

            # Check featuredImage if specified
            feat = item.get("featuredImage")
            if feat:
                img_path = BASE_DIR / feat
                if not img_path.exists():
                    errors.append(f"news[{idx}] featuredImage not found on disk: {feat}")

            # Check attachments if specified
            for a_idx, att in enumerate(item.get("attachments", [])):
                for a_req in ["name", "path", "type"]:
                    if a_req not in att or not att[a_req]:
                        errors.append(f"news[{idx}].attachments[{a_idx}].{a_req} is missing")
                p = att.get("path")
                if p:
                    att_path = BASE_DIR / p
                    if not att_path.exists():
                        errors.append(f"news[{idx}] attachment not found on disk: {p}")

    # Try jsonschema library if available
    try:
        import jsonschema
        if SCHEMA_PATH.exists():
            with open(SCHEMA_PATH, "r", encoding="utf-8") as sf:
                schema = json.load(sf)
            jsonschema.validate(instance=data, schema=schema)
    except ImportError:
        pass
    except Exception as e:
        errors.append(f"jsonschema validation error: {e}")

    if errors:
        print("FAIL: Validation errors encountered:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print(f"PASS: {CONTENT_PATH} is valid ({len(pillars)} pillars, {len(news)} news articles).")

if __name__ == "__main__":
    validate()
