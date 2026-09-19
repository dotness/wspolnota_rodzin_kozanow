#!/usr/bin/env python3
"""
Simulate Scenario 3 from quickstart.md:
1. Load data/content.json
2. Update nextMeeting.dateText
3. Verify validate_content.py passes
4. Verify export_js_data.py updates window.COMMUNITY_DATA
5. Restore original data/content.json
"""

import json
from pathlib import Path
import subprocess

ROOT_DIR = Path(__file__).resolve().parent.parent
CONTENT_PATH = ROOT_DIR / "data" / "content.json"

def main():
    print("Testing Scenario 3: AI Agent Content Update Simulation...")
    with open(CONTENT_PATH, "r", encoding="utf-8") as f:
        original = json.load(f)

    # Modify
    modified = json.loads(json.dumps(original))
    modified["siteConfig"]["nextMeeting"]["dateText"] = "Niedziela, 27 września, godz. 17:00"

    with open(CONTENT_PATH, "w", encoding="utf-8") as f:
        json.dump(modified, f, indent=2, ensure_ascii=False)

    # Validate
    res = subprocess.run(["python3", "-u", "scripts/validate_content.py"], cwd=ROOT_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print("Validation failed after edit!")
        print(res.stderr)
        return False

    # Sync fallback
    res_export = subprocess.run(["python3", "-u", "scripts/export_js_data.py"], cwd=ROOT_DIR, capture_output=True, text=True)
    if res_export.returncode != 0:
        print("Export failed!")
        return False

    # Verify fallback content
    with open(ROOT_DIR / "js" / "content-data.js", "r", encoding="utf-8") as f:
        js_content = f.read()
    assert "Niedziela, 27 września, godz. 17:00" in js_content, "Updated date missing in fallback JS!"

    # Restore
    with open(CONTENT_PATH, "w", encoding="utf-8") as f:
        json.dump(original, f, indent=2, ensure_ascii=False)
    subprocess.run(["python3", "-u", "scripts/export_js_data.py"], cwd=ROOT_DIR, capture_output=True, text=True)

    print("✅ Scenario 3 passed: AI agent update workflow simulation succeeded!")
    return True

if __name__ == "__main__":
    if not main():
        exit(1)
