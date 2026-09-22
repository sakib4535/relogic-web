#!/usr/bin/env python3
"""Make every page reachable with relative links + folder routes."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Map logical routes to current source files
SOURCES = {
    "index": ROOT / "index.html",
    "services": ROOT / "services.html",
    "projects": ROOT / "projects.html",
    "people": ROOT / "people.html",
    "research": ROOT / "research.html",
    "research/medical": ROOT / "research" / "medical.html",
    "research/startups": ROOT / "research" / "startups.html",
    "research/enterprise": ROOT / "research" / "enterprise.html",
}

PROFILE_DIR = ROOT / "people"


def depth_of(route: str) -> int:
    if route == "index":
        return 0
    return route.count("/") + 1


def prefix(route: str) -> str:
    d = depth_of(route)
    return "" if d == 0 else "../" * d


def rewrite(html: str, route: str) -> str:
    p = prefix(route)
    home = "./" if route == "index" else p
    # assets / images / js / css to relative
    html = html.replace('href="/assets/', f'href="{p}assets/')
    html = html.replace('src="/assets/', f'src="{p}assets/')
    html = html.replace('href="/images/', f'href="{p}images/')
    html = html.replace('src="/images/', f'src="{p}images/')
    html = html.replace('href="/responsive.css"', f'href="{p}responsive.css"')
    html = html.replace('href="/site.webmanifest"', f'href="{p}site.webmanifest"')
    html = html.replace('href="/favicon.ico"', f'href="{p}favicon.ico"')
    html = html.replace('content="https://www.relogiclabs.com/assets/brand/og-image.png"', f'content="{p}assets/brand/og-image.png"')

    # navigation destinations
    pairs = [
        ('href="/#home"', f'href="{home}index.html#home"' if route != "index" else 'href="#home"'),
        ('href="/#about"', f'href="{home}index.html#about"' if route != "index" else 'href="#about"'),
        ('href="/#project-intake"', f'href="{home}index.html#project-intake"' if route != "index" else 'href="#project-intake"'),
        ('href="/services"', f'href="{p}services/index.html"'),
        ('href="/research/medical"', f'href="{p}research/medical/index.html"'),
        ('href="/research/startups"', f'href="{p}research/startups/index.html"'),
        ('href="/research/enterprise"', f'href="{p}research/enterprise/index.html"'),
        ('href="/research"', f'href="{p}research/index.html"'),
        ('href="/projects"', f'href="{p}projects/index.html"'),
        ('href="/people"', f'href="{p}people/index.html"'),
        ('href="/"', f'href="{home}index.html"' if route != "index" else 'href="#home"'),
    ]
    # people profile links /people/slug
    html = re.sub(
        r'href="/people/([A-Za-z0-9_-]+)"',
        lambda m: f'href="{p}people/{m.group(1)}/index.html"',
        html,
    )
    for old, new in pairs:
        html = html.replace(old, new)

    # leftover root-absolute page links
    html = html.replace('href="services.html"', f'href="{p}services/index.html"')
    html = html.replace('href="projects.html"', f'href="{p}projects/index.html"')
    html = html.replace('href="people.html"', f'href="{p}people/index.html"')
    html = html.replace('href="research.html"', f'href="{p}research/index.html"')
    html = html.replace('projectUrl: "/projects"', f'projectUrl: "{p}projects/index.html"')
    html = html.replace('prototypeUrl: "/#project-intake"', 'prototypeUrl: "#project-intake"')
    return html


def write_index(route: str, html: str) -> Path:
    if route == "index":
        dest = ROOT / "index.html"
    else:
        dest = ROOT / route / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    return dest


def stub(path: Path, target: str) -> None:
    path.write_text(
        "<!DOCTYPE html>\n"
        f'<meta charset="utf-8">\n'
        f'<meta http-equiv="refresh" content="0;url={target}">\n'
        f"<script>location.replace({target!r});</script>\n"
        f'<p><a href="{target}">Continue</a></p>\n'
    )


def main() -> None:
    # profiles first from existing files
    for src in sorted(PROFILE_DIR.glob("*.html")):
        slug = src.stem
        route = f"people/{slug}"
        html = rewrite(src.read_text(errors="replace"), route)
        write_index(route, html)
        print("profile", route)

    for route, src in SOURCES.items():
        if not src.exists():
            print("missing", src)
            continue
        html = rewrite(src.read_text(errors="replace"), route)
        dest = write_index(route, html)
        print("wrote", dest.relative_to(ROOT))

    # stubs so old .html and pretty files both work
    stub(ROOT / "services.html", "services/")
    stub(ROOT / "projects.html", "projects/")
    stub(ROOT / "people.html", "people/")
    stub(ROOT / "research.html", "research/")
    stub(ROOT / "research" / "medical.html", "medical/")
    stub(ROOT / "research" / "startups.html", "startups/")
    stub(ROOT / "research" / "enterprise.html", "enterprise/")
    for src in PROFILE_DIR.glob("*.html"):
        if src.name != "index.html":
            stub(src, f"{src.stem}/")

    print("done")


if __name__ == "__main__":
    main()
