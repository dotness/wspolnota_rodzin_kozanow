#!/usr/bin/env python3
"""
Comprehensive End-to-End Verification Suite for Wspólnota Rodzin Kozanów.
Tests all functional requirements and success criteria:
- Schema conformity (SC-004)
- Asset completeness & zero 404s (SC-005)
- All 10 news articles data integrity
- 4 Community pillars presence and content
- Post 3 PDF attachments
- Offline fallback consistency
- Local HTTP server response checks
"""

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def run_check(title, fn):
    print(f"\n[CHECK] {title}...")
    try:
        fn()
        print(f"  ✓ PASS: {title}")
        return True
    except Exception as e:
        print(f"  ✗ FAIL: {title} -> {e}")
        return False

def test_schema_and_content():
    content_path = ROOT_DIR / "data" / "content.json"
    with open(content_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # SiteConfig
    cfg = data.get("siteConfig", {})
    assert "Wspólnota Rodzin" in cfg.get("siteTitle", ""), f"Invalid siteTitle: {cfg.get('siteTitle')}"
    assert "Razem w wierze" in cfg.get("slogan", ""), "Slogan missing"
    assert "Kozanów" in cfg.get("location", ""), "Location missing"
    assert "Bo rodzina to wielki dar" in cfg.get("motto", ""), "Motto missing"
    assert cfg.get("nextMeeting"), "nextMeeting config missing"

    # Pillars
    pillars = data.get("pillars", [])
    assert len(pillars) == 4, f"Expected exactly 4 pillars, got {len(pillars)}"
    pillar_ids = [p["id"] for p in pillars]
    for required_id in ["spotkania", "modlitwa", "relacje", "termin"]:
        assert required_id in pillar_ids, f"Missing pillar: {required_id}"

    # News
    news = data.get("news", [])
    assert len(news) == 10, f"Expected exactly 10 news articles, got {len(news)}"

    # Post 3 (attachments check)
    post3 = next((n for n in news if "Oświadczenie KEP" in n["title"]), None)
    assert post3 is not None, "Post 3 with Oświadczenie KEP not found"
    assert len(post3.get("attachments", [])) == 2, "Expected 2 PDF attachments in Post 3"
    for att in post3["attachments"]:
        path = ROOT_DIR / att["path"]
        assert path.exists(), f"Attachment file missing: {att['path']}"

def test_fallback_js():
    js_path = ROOT_DIR / "js" / "content-data.js"
    assert js_path.exists(), "js/content-data.js does not exist"
    with open(js_path, "r", encoding="utf-8") as f:
        text = f.read()
    assert "window.COMMUNITY_DATA" in text, "window.COMMUNITY_DATA missing in fallback"
    assert "Wspólnota Rodzin" in text, "Community data content missing in fallback"

def test_assets():
    import verify_assets
    assert verify_assets.verify_content_json() == 0, "content.json has missing assets"
    assert verify_assets.verify_index_html() == 0, "index.html has missing references"

def test_http_server():
    base_url = "http://localhost:8085"
    urls_to_test = [
        "/",
        "/css/style.css",
        "/css/components.css",
        "/js/content-data.js",
        "/js/app.js",
        "/data/content.json",
        "/assets/images/header/wspolnota_rodzin_header.png",
        "/assets/docs/Oswidczenie-KEP.pdf",
        "/assets/docs/Apel-Rady.pdf",
    ]
    for rel in urls_to_test:
        req = urllib.request.Request(f"{base_url}{rel}", method="HEAD")
        with urllib.request.urlopen(req, timeout=3) as resp:
            assert resp.status == 200, f"URL {rel} returned {resp.status}"

def main():
    checks = [
        ("Content & Schema Validation", test_schema_and_content),
        ("Offline Fallback JS Script", test_fallback_js),
        ("Local Asset & Link Verification", test_assets),
        ("Local HTTP Server Live Response (port 8085)", test_http_server),
    ]

    all_passed = True
    for title, fn in checks:
        if not run_check(title, fn):
            all_passed = False

    if all_passed:
        print("\n========================================================")
        print("🎉 ALL END-TO-END VERIFICATION CHECKS PASSED SUCCESSFULLY!")
        print("========================================================")
        sys.exit(0)
    else:
        print("\n❌ SOME VERIFICATION CHECKS FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
