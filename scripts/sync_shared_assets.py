#!/usr/bin/env python3
"""Refresh local copies of shared NeutrinoHit assets from ../neutrinohit-map."""
from pathlib import Path
import shutil


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parent
MAP = ROOT / "neutrinohit-map"
ASSETS = MAP / "assets"

COPIES = [
    (ASSETS / "reveal" / "neutrinohit-reveal-footer.js", PROJECT / "shared" / "reveal"),
    (ASSETS / "reveal" / "neutrinohit-reveal-quiz.css", PROJECT / "shared" / "reveal"),
    (ASSETS / "reveal" / "dvnlogo.png", PROJECT / "shared" / "reveal"),
    (ASSETS / "reveal" / "neutrinohit-reveal.scss", PROJECT / "shared" / "styles"),
    (ASSETS / "books" / "neutrinohit-book.tex", PROJECT / "shared" / "latex"),
    (MAP / "analytics" / "cloudflare-web-analytics.html", PROJECT / "shared" / "html"),
]
for lang in ("ru", "en"):
    book = PROJECT / lang / "book" / "assets"
    COPIES += [
        (ASSETS / "books" / "neutrinohit-book.css", book / "styles"),
        (ASSETS / "books" / "neutrinohit-book.lua", book / "filters"),
    ]


def main() -> None:
    for source, target_dir in COPIES:
        if not source.exists():
            raise FileNotFoundError(f"Missing shared asset: {source}")
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / source.name
        shutil.copy2(source, target)
        print(f"{source} -> {target}")


if __name__ == "__main__":
    main()
