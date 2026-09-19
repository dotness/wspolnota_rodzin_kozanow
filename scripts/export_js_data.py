import json
from pathlib import Path

base = Path(__file__).resolve().parent.parent
with open(base / 'data' / 'content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

js_content = f"// Auto-generated fallback data for offline file:// protocol\nwindow.COMMUNITY_DATA = {json.dumps(data, ensure_ascii=False, indent=2)};\n"

with open(base / 'js' / 'content-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("js/content-data.js generated successfully.")
