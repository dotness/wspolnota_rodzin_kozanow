#!/usr/bin/env python3
"""
scripts/test_content_management.py
Automated end-to-end test suite for news and meeting management CLI scripts and skills.
Ensures data integrity, schema validation, and offline fallback synchronization.
Restores original state upon completion.
"""

import sys
import shutil
import subprocess
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CONTENT_JSON = ROOT_DIR / "data" / "content.json"
CONTENT_JS = ROOT_DIR / "js" / "content-data.js"
BACKUP_JSON = ROOT_DIR / "data" / "content.json.test_bak"
BACKUP_JS = ROOT_DIR / "js" / "content-data.js.test_bak"

def run_cmd(cmd):
    res = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED: {' '.join(cmd)}")
        print("STDOUT:\n", res.stdout)
        print("STDERR:\n", res.stderr)
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return res.stdout

def main():
    print("Starting automated test suite for content management...")

    # 1. Backup original files
    shutil.copy2(CONTENT_JSON, BACKUP_JSON)
    shutil.copy2(CONTENT_JS, BACKUP_JS)
    print("Backed up content.json and content-data.js")

    try:
        # 2. Test manage_news.py list
        print("\n[TEST 1] Testing manage_news.py list...")
        out = run_cmd([sys.executable, "scripts/manage_news.py", "list"])
        assert "Total articles:" in out, "Failed to list articles"
        print("✓ manage_news.py list passed")

        # 3. Test manage_news.py add
        print("\n[TEST 2] Testing manage_news.py add...")
        test_title = "Nowy Testowy Artykuł Wspólnoty"
        test_date = "2026-09-30"
        test_content = "<p>To jest treść testowego artykułu dodanego przez test automatyczny.</p>"
        out = run_cmd([
            sys.executable, "scripts/manage_news.py", "add",
            "--title", test_title,
            "--date", test_date,
            "--content", test_content
        ])
        assert "Article created successfully" in out, "Failed to add article"

        with open(CONTENT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        added_item = next((x for x in data["news"] if x["title"] == test_title), None)
        assert added_item is not None, "Article not found in content.json after add"
        test_id = added_item["id"]
        print(f"✓ manage_news.py add passed (Created ID: {test_id})")

        # 4. Test manage_news.py update
        print("\n[TEST 3] Testing manage_news.py update...")
        updated_title = "Zaktualizowany Testowy Artykuł"
        run_cmd([
            sys.executable, "scripts/manage_news.py", "update",
            "--id", str(test_id),
            "--title", updated_title
        ])
        with open(CONTENT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        updated_item = next((x for x in data["news"] if str(x["id"]) == str(test_id)), None)
        assert updated_item is not None and updated_item["title"] == updated_title, "Article update failed"
        print("✓ manage_news.py update passed")

        # 5. Test manage_news.py remove
        print("\n[TEST 4] Testing manage_news.py remove...")
        run_cmd([
            sys.executable, "scripts/manage_news.py", "remove",
            "--id", str(test_id)
        ])
        with open(CONTENT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        removed_item = next((x for x in data["news"] if str(x["id"]) == str(test_id)), None)
        assert removed_item is None, "Article was not removed"
        print("✓ manage_news.py remove passed")

        # 6. Test manage_meeting.py show
        print("\n[TEST 5] Testing manage_meeting.py show...")
        out = run_cmd([sys.executable, "scripts/manage_meeting.py", "show"])
        assert "NAJBLIŻSZE SPOTKANIE WSPÓLNOTY" in out, "Failed to show meeting"
        print("✓ manage_meeting.py show passed")

        # 7. Test manage_meeting.py remove
        print("\n[TEST 6] Testing manage_meeting.py remove...")
        run_cmd([sys.executable, "scripts/manage_meeting.py", "remove"])
        with open(CONTENT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["siteConfig"]["nextMeeting"] is None, "Meeting was not set to None"
        # Validate schema with None nextMeeting
        run_cmd([sys.executable, "scripts/validate_content.py"])
        print("✓ manage_meeting.py remove passed (and validate_content.py confirmed valid)")

        # 8. Test manage_meeting.py update
        print("\n[TEST 7] Testing manage_meeting.py update...")
        run_cmd([
            sys.executable, "scripts/manage_meeting.py", "update",
            "--title", "Spotkanie Jesienne Wspólnoty",
            "--date", "Niedziela, 4 października 2026 r., godz. 16:00",
            "--location", "Salka pod kościołem",
            "--description", "Zaproszenie na wspólne spotkanie.",
            "--content", "<h4>Harmonogram spotkania</h4><p>Modlitwa i rozmowy.</p>"
        ])
        with open(CONTENT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        nm = data["siteConfig"]["nextMeeting"]
        assert nm is not None and nm["title"] == "Spotkanie Jesienne Wspólnoty"
        print("✓ manage_meeting.py update passed")

    finally:
        # Restore backups
        if BACKUP_JSON.exists():
            shutil.copy2(BACKUP_JSON, CONTENT_JSON)
            BACKUP_JSON.unlink()
        if BACKUP_JS.exists():
            shutil.copy2(BACKUP_JS, CONTENT_JS)
            BACKUP_JS.unlink()
        print("\nRestored original content.json and content-data.js")

    # Run final validation on restored files
    run_cmd([sys.executable, "scripts/validate_content.py"])
    run_cmd([sys.executable, "scripts/verify_assets.py"])
    print("\n🎉 ALL TESTS PASSED! News and meeting management are 100% verified.")

if __name__ == "__main__":
    main()
