import shutil
import os
from pathlib import Path

base = Path(__file__).resolve().parent.parent
news_ref = base / 'news_reference'
assets = base / 'assets'

# Header image
header_dir = assets / 'images' / 'header'
header_dir.mkdir(parents=True, exist_ok=True)
if (base / 'headline_reference.png').exists():
    shutil.copy(base / 'headline_reference.png', header_dir / 'headline_reference.png')
    print("Copied headline_reference.png")

# Docs
docs_dir = assets / 'docs'
docs_dir.mkdir(parents=True, exist_ok=True)
p3_docs = news_ref / '03_2026-09-05_oswiadczenie-kep-i-apel-rady-biskupow' / 'attachments'
if p3_docs.exists():
    for f in p3_docs.glob('*.pdf'):
        shutil.copy(f, docs_dir / f.name)
        print(f"Copied {f.name} -> assets/docs/")

# News images
news_dest = assets / 'news'
for idx in range(1, 11):
    prefix = f"{idx:02d}_"
    match_dirs = [d for d in news_ref.iterdir() if d.is_dir() and d.name.startswith(prefix)]
    if match_dirs:
        src_dir = match_dirs[0]
        dst_dir = news_dest / f"{idx:02d}"
        dst_dir.mkdir(parents=True, exist_ok=True)
        img_src = src_dir / 'images'
        if img_src.exists():
            for img in img_src.iterdir():
                shutil.copy(img, dst_dir / img.name)
                print(f"Copied {img.name} -> assets/news/{idx:02d}/")

print("Asset organization completed successfully.")
