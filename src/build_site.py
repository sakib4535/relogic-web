#!/usr/bin/env python3
"""Assemble Relogic pages onto one chrome system without dropping page design."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATTACH = Path("/home/workdir/attachments")
OUT = ROOT

NAV_ITEMS = [
    ("Home", "index.html"),
    ("About", "index.html#about"),
    ("Services", "services.html"),
    ("Digital Product", "projects.html"),
    ("Our People", "people.html"),
]

HEAD_INCLUDES = """
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta http-equiv="X-Content-Type-Options" content="nosniff">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="assets/css/tokens.css">
  <link rel="stylesheet" href="assets/css/chrome.css">
  <link rel="stylesheet" href="assets/css/readability.css">
""".strip()

HEAD_INCLUDES_NESTED = HEAD_INCLUDES.replace('href="assets/', 'href="../assets/')


def nav_markup(active: str, prefix: str = "") -> str:
    def href(target: str) -> str:
        return prefix + target

    links = []
    mobile = []
    for label, target in NAV_ITEMS:
        cls = ' class="active"' if target == active or label.lower() == active else ""
        links.append(f'        <a href="{href(target)}"{cls}>{label}</a>')
        mobile.append(f'      <a href="{href(target)}"{cls}>{label}</a>')
    cta = href("index.html#project-intake")
    logo = prefix + "images/team/relogic-logo-transparent.png"
    home = href("index.html")
    return f'''<a class="rl-skip" href="#main">Skip to content</a>
<div class="scroll-progress" id="scrollProgress"></div>
<div class="nav-shell" id="navShell">
  <nav class="nav" aria-label="Primary navigation">
    <a href="{home}" class="brand" aria-label="Relogic home">
      <span class="brand-mark">
        <img src="{logo}" alt="Relogic Labs">
      </span>
    </a>
    <div class="nav-links">
{chr(10).join(links)}
    </div>
    <div class="nav-actions">
      <a class="nav-cta" href="{cta}">Start a project</a>
      <button class="menu-btn" id="menuBtn" type="button" aria-label="Open menu" aria-expanded="false">
        <span class="hamburger" aria-hidden="true"><b></b><b></b><b></b></span>
      </button>
    </div>
  </nav>
  <div class="mobile-menu" id="mobileMenu">
{chr(10).join(mobile)}
      <a href="{cta}">Contact</a>
  </div>
</div>'''


def footer_markup(prefix: str = "") -> str:
    logo = prefix + "images/team/relogic-logo-transparent.png"
    home = prefix + "index.html"
    links = [
        ("About", prefix + "index.html#about"),
        ("Services", prefix + "services.html"),
        ("Research", prefix + "research.html"),
        ("Digital Product", prefix + "projects.html"),
        ("Our People", prefix + "people.html"),
        ("Contact", prefix + "index.html#project-intake"),
    ]
    link_html = "".join(f'<a href="{href}">{label}</a>' for label, href in links)
    return f'''<footer class="rl-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="{home}" class="brand" aria-label="Relogic home">
          <span class="brand-mark"><img src="{logo}" alt="Relogic Labs"></span>
        </a>
        <p class="footer-copy">Research, AI, data intelligence and digital products for situations where the answer has to be more than impressive. It has to be useful.</p>
      </div>
      <div class="footer-links">{link_html}</div>
    </div>
    <div class="copyright">© 2026 Relogic Solutions. Built around evidence, data and useful intelligence.</div>
  </div>
</footer>
<script src="{prefix}assets/js/site.js" defer></script>'''


def strip_share_scripts(html: str) -> str:
    pattern = re.compile(
        r"<script>\s*\(function \(\) \{\s*\"use strict\";\s*// Share link redirector.*?</script>",
        re.S,
    )
    cleaned, n = pattern.subn("", html)
    print(f"  removed {n} injected share-redirector script(s)")
    return cleaned


def inject_head(html: str, includes: str) -> str:
    if "assets/css/tokens.css" in html:
        return html
    if "</title>" in html:
        return html.replace("</title>", "</title>\n  " + includes, 1)
    return html.replace("</head>", "  " + includes + "\n</head>", 1)


def replace_between(html: str, start_pat: str, end_pat: str, replacement: str) -> str:
    start = re.search(start_pat, html, re.I)
    end = re.search(end_pat, html, re.I)
    if not start or not end or end.start() <= start.start():
        return html
    return html[: start.start()] + replacement + html[end.end() :]


def brighten_root(html: str) -> str:
    html = html.replace("--muted: #91a1b8;", "--muted: #d5e0ee;")
    html = html.replace("--muted: #8fa0b7;", "--muted: #d5e0ee;")
    html = html.replace("--muted: #8b98ad;", "--muted: #d5e0ee;")
    html = html.replace("--muted2: #5e7089;", "--muted2: #b7c6d8;")
    html = html.replace("--muted2: #64748b;", "--muted2: #b7c6d8;")
    html = html.replace("color:#91a0b4;", "color:#d7e3f1;")
    html = html.replace("color:#94a3b8;", "color:#d7e3f1;")
    html = html.replace("color:#9eb0b2;", "color:#d7e3f1;")
    html = html.replace("color:#8fa0b8;", "color:#d7e3f1;")
    html = html.replace("color: #8fa0b8;", "color: #d7e3f1;")
    html = html.replace("color:#93a3ba;", "color:#d7e3f2;")
    html = html.replace("color: #93a3ba;", "color: #d7e3f2;")
    html = html.replace("color:#5e7089;", "color:#c9d5e4;")
    html = html.replace("color: #5e7089;", "color: #c9d5e4;")
    html = html.replace("color:#64748b;", "color:#c5d0de;")
    html = html.replace("color: #64748b;", "color: #c5d0de;")
    html = html.replace("color:#3f4d63;", "color:#9aabc0;")
    html = html.replace("color:#71849d;", "color:#c5d3e4;")
    html = html.replace("color:#74869c;", "color:#c5d3e4;")
    html = html.replace("color:#7f8ca0;", "color:#c5d3e4;")
    html = html.replace("color:#8496aa;", "color:#c9d6e6;")
    html = html.replace("color:#9aabc0;", "color:#d7e3f2;")
    return html


def fix_legacy_links(html: str) -> str:
    html = html.replace("digital-product.html", "projects.html")
    html = html.replace('href="index.html#projects"', 'href="projects.html"')
    html = html.replace('href="index.html#people"', 'href="people.html"')
    return html


def process_index() -> None:
    print("processing index.html")
    html = (ATTACH / "index.html").read_text(errors="replace")
    html = strip_share_scripts(html)
    html = brighten_root(html)
    html = inject_head(html, HEAD_INCLUDES)
    # unify nav links inside existing index chrome
    old_nav_links = '''      <div class="nav-links">
        <a href="#home" class="active">Home</a>
        <a href="#about">About</a>
        <a href="services.html">Services</a>
        <a href="projects.html">Projects</a>
        <a href="#people">Our People</a>
        <a href="#project-intake">Contact</a>
      </div>'''
    new_nav_links = '''      <div class="nav-links">
        <a href="#home" class="active">Home</a>
        <a href="#about">About</a>
        <a href="services.html">Services</a>
        <a href="research.html">Research</a>
        <a href="projects.html">Digital Product</a>
        <a href="people.html">Our People</a>
      </div>'''
    if old_nav_links in html:
        html = html.replace(old_nav_links, new_nav_links)
    old_mobile = '''    <div class="mobile-menu" id="mobileMenu">
      <a href="#home">Home</a>
      <a href="#about">About</a>
      <a href="services.html">Services</a>
      <a href="projects.html">Projects</a>
      <a href="#people">Our People</a>
      <a href="#project-intake">Contact</a>
    </div>'''
    new_mobile = '''    <div class="mobile-menu" id="mobileMenu">
      <a href="#home">Home</a>
      <a href="#about">About</a>
      <a href="services.html">Services</a>
      <a href="research.html">Research</a>
      <a href="projects.html">Digital Product</a>
      <a href="people.html">Our People</a>
      <a href="#project-intake">Contact</a>
    </div>'''
    if old_mobile in html:
        html = html.replace(old_mobile, new_mobile)
    html = html.replace(
        '<div class="footer-links"><a href="#about">About</a><a href="services.html">Services</a><a href="projects.html">Projects</a><a href="people.html">People</a><a href="#project-intake">Contact</a></div>',
        '<div class="footer-links"><a href="#about">About</a><a href="services.html">Services</a><a href="research.html">Research</a><a href="projects.html">Digital Product</a><a href="people.html">Our People</a><a href="#project-intake">Contact</a></div>',
    )
    if "assets/js/site.js" not in html:
        html = html.replace("</body>", '<script src="assets/js/site.js" defer></script>\n</body>')
    if 'id="main"' not in html:
        html = html.replace("<main>", '<main id="main">', 1)
    (OUT / "index.html").write_text(html)
    print("  wrote index.html", len(html))


def swap_header_footer(html: str, header: str, footer: str) -> str:
    # header: from first <header to its closing tag
    html = replace_between(html, r"<header\b", r"</header>", header)
    html = replace_between(html, r"<footer\b", r"</footer>", footer)
    return html


def process_inner(name: str, active: str, body_pad: str = "") -> None:
    print("processing", name)
    html = (ATTACH / name).read_text(errors="replace")
    html = strip_share_scripts(html)
    html = brighten_root(html)
    html = fix_legacy_links(html)
    html = inject_head(html, HEAD_INCLUDES)
    header = nav_markup(active)
    footer = footer_markup()
    html = swap_header_footer(html, header, footer)
    if 'id="main"' not in html:
        html = html.replace("<main>", '<main id="main">', 1)
    if body_pad and "<body" in html:
        html = re.sub(r"<body([^>]*)>", r"<body\1>", html, count=1)
    # hide original page-level sticky headers leftover styles by ensuring chrome wins
    (OUT / name).write_text(html)
    print("  wrote", name, len(html))


def profile_page(person: dict, group: str) -> str:
    slug = person["slug"]
    name = person["name"]
    role = person["role"]
    focus = person["focus"]
    image = "../" + person["image"]
    initials = person["initials"]
    header = nav_markup("people.html", prefix="../")
    footer = footer_markup(prefix="../")
    includes = HEAD_INCLUDES_NESTED
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} · Relogic People</title>
  <meta name="description" content="{name} — {role} at Relogic. {focus}.">
  {includes}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    body {{
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(circle at 14% 2%, rgba(56,189,248,.10), transparent 24%),
        radial-gradient(circle at 88% 8%, rgba(129,140,248,.08), transparent 25%),
        #050816;
      color: #f8fbff;
      font-family: Inter, system-ui, sans-serif;
    }}
    .profile-wrap {{
      width: min(1080px, calc(100% - 40px));
      margin: 0 auto;
      padding: 128px 0 80px;
      display: grid;
      grid-template-columns: 340px 1fr;
      gap: 48px;
      align-items: start;
    }}
    .portrait {{
      border-radius: 28px;
      overflow: hidden;
      border: 1px solid rgba(186,210,232,.18);
      background: #0b1224;
      aspect-ratio: 1 / 1.05;
    }}
    .portrait img {{ width: 100%; height: 100%; object-fit: cover; }}
    .fallback {{
      width: 100%; height: 100%; display: grid; place-items: center;
      font: 700 72px "Space Grotesk", sans-serif; color: #7dd3fc;
    }}
    .kicker {{ color: #9beaf7; font-size: 11px; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; }}
    h1 {{ font: 700 clamp(40px, 6vw, 68px)/.95 "Space Grotesk", sans-serif; letter-spacing: -.05em; margin: 14px 0 10px; }}
    .role {{ color: #67d4ff; font-size: 16px; margin: 0 0 18px; }}
    .focus {{ color: #d7e3f2; font-size: 16px; line-height: 1.7; max-width: 560px; }}
    .meta {{
      display: flex; flex-wrap: wrap; gap: 8px; margin-top: 26px;
    }}
    .meta span {{
      padding: 8px 11px; border-radius: 999px; border: 1px solid rgba(186,210,232,.18);
      background: rgba(255,255,255,.04); font-size: 11px; font-weight: 700; color: #e8eef6;
    }}
    .back {{
      display: inline-flex; margin-top: 34px; color: #7ef0ff; font-weight: 800; font-size: 13px;
    }}
    @media (max-width: 800px) {{
      .profile-wrap {{ grid-template-columns: 1fr; padding-top: 110px; }}
    }}
  </style>
</head>
<body class="page-profile">
{header}
<main id="main">
  <div class="profile-wrap">
    <div class="portrait">
      <img src="{image}" alt="{name}" onerror="this.style.display='none';this.nextElementSibling.style.display='grid';">
      <div class="fallback" style="display:none">{initials}</div>
    </div>
    <div>
      <div class="kicker">{group} · Relogic</div>
      <h1>{name}</h1>
      <p class="role">{role}</p>
      <p class="focus">{focus}</p>
      <div class="meta">
        <span>{group}</span>
        <span>Relogic Labs</span>
      </div>
      <a class="back" href="../people.html">← Back to Our People</a>
    </div>
  </div>
</main>
{footer}
</body>
</html>
'''


def write_people_profiles() -> None:
    team = json.loads((OUT / "data/team.json").read_text())
    mapping = [
        ("leadership", "Leadership"),
        ("advisors", "Advisors"),
        ("core", "Core Team"),
    ]
    for key, label in mapping:
        for person in team[key]:
            path = OUT / "people" / f"{person['slug']}.html"
            path.write_text(profile_page(person, label))
            print("  profile", path.name)


def main() -> None:
    process_index()
    process_inner("services.html", "services.html")
    process_inner("projects.html", "projects.html")
    process_inner("research.html", "research.html")
    process_inner("people.html", "people.html")
    write_people_profiles()
    print("done")


if __name__ == "__main__":
    main()
