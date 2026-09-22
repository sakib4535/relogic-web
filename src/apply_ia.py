#!/usr/bin/env python3
"""Apply clean URLs, brand icons, research sectors and new products."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FAVICONS = """
  <link rel="icon" href="/assets/brand/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/brand/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png" sizes="180x180">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#050816">
  <meta property="og:image" content="https://www.relogiclabs.com/assets/brand/og-image.png">
  <meta name="twitter:image" content="https://www.relogiclabs.com/assets/brand/og-image.png">
""".strip()

NAV = [
    ("Home", "/"),
    ("About", "/#about"),
    ("Services", "/services"),
    ("Digital Product", "/projects"),
    ("Our People", "/people"),
]


def chrome(active: str) -> tuple[str, str]:
    links = []
    mobile = []
    for label, href in NAV:
        cls = ' class="active"' if href.rstrip("/") == active.rstrip("/") or (
            active.startswith("/research") and href == "/research"
        ) else ""
        if active == "/" and href == "/":
            cls = ' class="active"'
        links.append(f'        <a href="{href}"{cls}>{label}</a>')
        mobile.append(f'      <a href="{href}"{cls}>{label}</a>')
    header = f'''<a class="rl-skip" href="#main">Skip to content</a>
<div class="scroll-progress" id="scrollProgress"></div>
<div class="nav-shell" id="navShell">
  <nav class="nav" aria-label="Primary navigation">
    <a href="/" class="brand" aria-label="Relogic home">
      <span class="brand-mark">
        <img src="/images/team/relogic-logo-transparent.png" alt="Relogic Labs">
      </span>
    </a>
    <div class="nav-links">
{chr(10).join(links)}
    </div>
    <div class="nav-actions">
      <a class="nav-cta" href="/#project-intake">Start a project</a>
      <button class="menu-btn" id="menuBtn" type="button" aria-label="Open menu" aria-expanded="false">
        <span class="hamburger" aria-hidden="true"><b></b><b></b><b></b></span>
      </button>
    </div>
  </nav>
  <div class="mobile-menu" id="mobileMenu">
{chr(10).join(mobile)}
      <a href="/#project-intake">Contact</a>
  </div>
</div>'''
    footer = '''<footer class="rl-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="/" class="brand" aria-label="Relogic home">
          <span class="brand-mark"><img src="/images/team/relogic-logo-transparent.png" alt="Relogic Labs"></span>
        </a>
        <p class="footer-copy">Research, AI, data intelligence and digital products for situations where the answer has to be more than impressive. It has to be useful.</p>
      </div>
      <div class="footer-links"><a href="/#about">About</a><a href="/services">Services</a><a href="/research">Research</a><a href="/projects">Digital Product</a><a href="/people">Our People</a><a href="/#project-intake">Contact</a></div>
    </div>
    <div class="copyright">© 2026 Relogic Solutions. Built around evidence, data and useful intelligence.</div>
  </div>
</footer>
<script src="/assets/js/site.js" defer></script>'''
    return header, footer


HEAD = '''  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <link rel="canonical" href="CANONICAL">
  FAV
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/chrome.css">
  <link rel="stylesheet" href="/assets/css/readability.css">
  <link rel="stylesheet" href="/assets/css/sectors.css">
'''.replace("FAV", FAVICONS)


def page(title: str, desc: str, canonical: str, active: str, body: str, extra_css: str = "") -> str:
    header, footer = chrome(active)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
{HEAD.replace("CANONICAL", canonical)}
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <style>body{{margin:0;min-height:100vh;background:#050816;color:#f8fbff;font-family:Inter,system-ui,sans-serif}}{extra_css}</style>
</head>
<body class="rl-has-chrome">
{header}
<main id="main">
{body}
</main>
{footer}
</body>
</html>
'''


def write_research_hub() -> None:
    body = '''
<section class="sector-hero">
  <div class="container">
    <div class="kicker">Research Consultancy</div>
    <h1>Three sectors.<br><span>One research standard.</span></h1>
    <p>Choose the context first. Medical evidence work, startup and SME research systems, and enterprise research programmes each get their own pathway — without mixing the language or the method.</p>
  </div>
</section>
<section class="sector-grid">
  <a class="sector-card" href="/research/medical">
    <small>01 / Medical Sector</small>
    <h2>Medical &amp; epidemiological research</h2>
    <p>Study design, clinical and population evidence, graph-led findings and consultancy-led medical research.</p>
    <span class="enter">Open medical research →</span>
  </a>
  <a class="sector-card startup" href="/research/startups">
    <small>02 / Startup and SMEs</small>
    <h2>Applied AI research for growing teams</h2>
    <p>Generative AI development, agent automation and research pilots designed to ship without losing control of the evidence.</p>
    <span class="enter">Open startup research →</span>
  </a>
  <a class="sector-card enterprise" href="/research/enterprise">
    <small>03 / Enterprise Business</small>
    <h2>Research systems for complex organisations</h2>
    <p>Evaluation, governance, deployment research and decision architecture for teams that cannot treat AI as a demo.</p>
    <span class="enter">Open enterprise research →</span>
  </a>
</section>
'''
    html = page(
        "Research Consultancy · Relogic",
        "Relogic research consultancy across Medical, Startup and SME, and Enterprise Business sectors.",
        "https://www.relogiclabs.com/research",
        "/research",
        body,
    )
    (ROOT / "research.html").write_text(html)
    print("wrote research hub")


def write_startups() -> None:
    body = '''
<div class="crumb"><a href="/research">Research</a> / Startup and SMEs</div>
<section class="sector-hero">
  <div class="container">
    <div class="kicker">Startup and SMEs · Research solutions</div>
    <h1>Research that can be <span>deployed.</span></h1>
    <p>Three research tracks for founder-led and SME teams: generate useful systems, automate work with agents, and run applied pilots that still keep a human review path.</p>
  </div>
</section>
<article class="solution-block">
  <small style="color:#9beaf7;font-size:10px;font-weight:800;letter-spacing:.14em">SOLUTION 01</small>
  <h2>Generative AI Development</h2>
  <p>Design and evaluate generative systems around a real workflow: retrieval, grounded answers, permissions, and review. The research question is not “can the model write” — it is whether the output is usable, traceable and safe enough to sit inside an operating business.</p>
  <div class="solution-tags"><span>RAG</span><span>Evaluation</span><span>Grounding</span><span>Human review</span></div>
</article>
<article class="solution-block">
  <small style="color:#9beaf7;font-size:10px;font-weight:800;letter-spacing:.14em">SOLUTION 02</small>
  <h2>AI Agent Automation</h2>
  <p>Agent workflows for operations that currently live in inboxes, spreadsheets and follow-up loops. Relogic maps the task, the tools the agent may touch, the stop conditions, and the evidence trail so automation does not become a black box.</p>
  <div class="solution-tags"><span>Agents</span><span>Tool use</span><span>Workflow design</span><span>Audit trail</span></div>
</article>
<article class="solution-block" style="margin-bottom:90px">
  <small style="color:#9beaf7;font-size:10px;font-weight:800;letter-spacing:.14em">SOLUTION 03</small>
  <h2>Applied AI pilots &amp; product intelligence</h2>
  <p>A bounded research pilot: one use case, one success metric, one failure mode, and a recommendation to scale, stop or redesign. Built for teams that need a working prototype and a defensible reading of what the prototype actually proved.</p>
  <div class="solution-tags"><span>Pilot design</span><span>Product intelligence</span><span>Decision memo</span><span>Prototype</span></div>
</article>
'''
    html = page(
        "Startup and SME Research · Relogic",
        "Generative AI development, AI agent automation and applied AI pilots for startups and SMEs.",
        "https://www.relogiclabs.com/research/startups",
        "/research",
        body,
    )
    (ROOT / "research" / "startups.html").write_text(html)
    print("wrote startups")


def write_enterprise() -> None:
    body = '''
<div class="crumb"><a href="/research">Research</a> / Enterprise Business</div>
<section class="sector-hero">
  <div class="container">
    <div class="kicker">Enterprise Business · Research programmes</div>
    <h1>Research that survives <span>institutional scrutiny.</span></h1>
    <p>Enterprise work needs more than a model demo. These three tracks cover deployment research, governance, and the decision systems that keep large programmes accountable.</p>
  </div>
</section>
<article class="solution-block">
  <small style="color:#9beaf7;font-size:10px;font-weight:800;letter-spacing:.14em">PROGRAMME 01</small>
  <h2>Enterprise AI deployment research</h2>
  <p>Assess where generative systems and automation can enter an existing operating model — data access, permissions, integration points, review load and failure cost — before a platform decision is locked.</p>
  <div class="solution-tags"><span>Deployment</span><span>Integration</span><span>Operating model</span><span>Readiness</span></div>
</article>
<article class="solution-block">
  <small style="color:#9beaf7;font-size:10px;font-weight:800;letter-spacing:.14em">PROGRAMME 02</small>
  <h2>Model risk, evaluation &amp; governance</h2>
  <p>Evaluation design, provenance, oversight interfaces and policy-aligned controls. The output is a research-backed governance layer that makes model boundaries visible to the people who own the risk.</p>
  <div class="solution-tags"><span>Evaluation</span><span>Governance</span><span>Model risk</span><span>Accountability</span></div>
</article>
<article class="solution-block" style="margin-bottom:90px">
  <small style="color:#9beaf7;font-size:10px;font-weight:800;letter-spacing:.14em">PROGRAMME 03</small>
  <h2>Evidence architecture &amp; decision systems</h2>
  <p>Turn fragmented enterprise evidence into a surface leadership can inspect: sources, assumptions, uncertainty and recommended action. Built for programmes where the answer has to travel across teams without losing its method.</p>
  <div class="solution-tags"><span>Evidence</span><span>Decision systems</span><span>Knowledge layers</span><span>Reporting</span></div>
</article>
'''
    html = page(
        "Enterprise Research · Relogic",
        "Enterprise AI deployment research, model governance and evidence architecture.",
        "https://www.relogiclabs.com/research/enterprise",
        "/research",
        body,
    )
    (ROOT / "research" / "enterprise.html").write_text(html)
    print("wrote enterprise")


REPLACEMENTS = [
    ('href="index.html#project-intake"', 'href="/#project-intake"'),
    ('href="index.html#about"', 'href="/#about"'),
    ('href="index.html#home"', 'href="/#home"'),
    ('href="index.html#people"', 'href="/people"'),
    ('href="index.html#projects"', 'href="/projects"'),
    ('href="index.html#contact"', 'href="/#project-intake"'),
    ('href="index.html"', 'href="/"'),
    ('href="#home"', 'href="/#home"'),
    ('href="#about"', 'href="/#about"'),
    ('href="#project-intake"', 'href="/#project-intake"'),
    ('href="services.html"', 'href="/services"'),
    ('href="research.html"', 'href="/research"'),
    ('href="projects.html"', 'href="/projects"'),
    ('href="people.html"', 'href="/people"'),
    ('href="people/', 'href="/people/'),
    ('href="../index.html"', 'href="/"'),
    ('href="../people.html"', 'href="/people"'),
    ('href="../services.html"', 'href="/services"'),
    ('href="../research.html"', 'href="/research"'),
    ('href="../projects.html"', 'href="/projects"'),
    ('src="assets/', 'src="/assets/'),
    ('href="assets/', 'href="/assets/'),
    ('src="../assets/', 'src="/assets/'),
    ('href="../assets/', 'href="/assets/'),
    ('src="images/', 'src="/images/'),
    ('src="../images/', 'src="/images/'),
    ('href="responsive.css"', 'href="/responsive.css"'),
]


def rewrite_links(html: str) -> str:
    for old, new in REPLACEMENTS:
        html = html.replace(old, new)
    html = html.replace(".html#", "#")
    # people profile files: /people/slug.html -> /people/slug
    html = re.sub(r'href="/people/([A-Za-z0-9_-]+)\.html"', r'href="/people/\1"', html)
    return html


def inject_favicons(html: str) -> str:
    if "/assets/brand/favicon.svg" in html:
        return html
    if "</title>" in html:
        return html.replace("</title>", "</title>\n  " + FAVICONS, 1)
    return html.replace("</head>", "  " + FAVICONS + "\n</head>", 1)


def patch_index_products(html: str) -> str:
    extra = '''
    {
      show: true,
      category: "exclusive",
      kicker: "FOUNDER OPERATIONS / LIVE PROTOTYPE / COMMAND CENTER",
      title: "FounderCMD",
      description: "An evidence-backed command center for founder-led businesses. Projects, clients, cash, operations and business signals sit in one place so decisions can be traced to the record behind them.",
      image: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=85",
      projectUrl: "https://foundercmd.vercel.app/",
      prototypeUrl: "https://foundercmd.vercel.app/"
    },

    {
      show: true,
      category: "exclusive",
      kicker: "LOGISTICS / LIVE PRODUCT / END-TO-END TRACKING",
      title: "Neervan",
      description: "A logistics tracking and support system covering the full movement lifecycle — intake, live location, exceptions, handoffs and proof of completion — so operations teams can act from one support surface.",
      image: "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1200&q=85",
      projectUrl: "/projects",
      prototypeUrl: "/#project-intake"
    },
'''
    needle = '''      prototypeUrl: "#live-prototype"
    },
'''
    if "FounderCMD" not in html and needle in html:
        html = html.replace(needle, needle + extra, 1)

    old_render = '''    const featured = list.find(isExclusive) || list[0];
    const others = list.filter(p => p !== featured);

    featuredBox.innerHTML = featured ? `<div class="featured-project-wrap"><div class="featured-label">Featured Project</div>${projectCard(featured,true)}</div>` : "";
    grid.innerHTML = others.length ? others.map(p => projectCard(p)).join("") : "";
'''
    new_render = '''    const featuredList = list.filter(isExclusive);
    const others = list.filter(p => !isExclusive(p));
    const featuredHtml = featuredList.length
      ? `<div class="featured-project-wrap"><div class="featured-label">Live prototypes</div><div class="featured-stack">${featuredList.map(p => projectCard(p,true)).join("")}</div></div>`
      : "";
    featuredBox.innerHTML = featuredHtml;
    grid.innerHTML = others.length ? others.map(p => projectCard(p)).join("") : "";
'''
    if old_render in html:
        html = html.replace(old_render, new_render)
    if ".featured-stack" not in html:
        html = html.replace(
            ".featured-project-wrap { margin-bottom: 55px; }",
            ".featured-project-wrap { margin-bottom: 55px; }\n    .featured-stack { display:grid; gap:18px; }\n    .featured-stack .featured-project-card { min-height:520px; }",
        )
    html = html.replace(
        "These are representative project directions rather than decorative case-study cards: healthcare data, adaptive security, analytical products and governance systems.",
        "Live prototypes first — Velos, FounderCMD and Neervan — then the research and product directions behind healthcare data, adaptive security, analytics and governance.",
    )
    return html


def convert_medical() -> None:
    src = ROOT / "research.html"
    # current research.html is still the old medical page until hub overwrite.
    # Caller should copy original medical BEFORE writing hub.
    pass


def main() -> None:
    # Preserve medical page from current research.html before hub overwrite
    medical_src = (ROOT / "research.html").read_text(errors="replace")
    if "Urban Dengue" in medical_src or "epidemiological" in medical_src:
        medical = medical_src
        medical = rewrite_links(medical)
        medical = inject_favicons(medical)
        header, footer = chrome("/research")
        medical = re.sub(r'<a class="rl-skip".*?</div>\s*</div>', header, medical, count=1, flags=re.S)
        medical = re.sub(r'<footer class="rl-footer">.*?</script>', footer, medical, count=1, flags=re.S)
        if 'class="crumb"' not in medical:
            medical = medical.replace(
                '<main id="main">',
                '<main id="main">\n<div class="crumb"><a href="/research">Research</a> / Medical Sector</div>',
                1,
            )
        if "/assets/css/sectors.css" not in medical:
            medical = medical.replace(
                'href="/assets/css/readability.css">',
                'href="/assets/css/readability.css">\n  <link rel="stylesheet" href="/assets/css/sectors.css">',
            )
        (ROOT / "research" / "medical.html").write_text(medical)
        print("wrote medical from previous research page")

    write_research_hub()
    write_startups()
    write_enterprise()

    # Patch remaining site files
    for path in list(ROOT.rglob("*.html")):
        if "archive" in path.parts:
            continue
        text = path.read_text(errors="replace")
        if path.name == "research.html" and "Three sectors" in text:
            # already new hub
            pass
        new = rewrite_links(text)
        new = inject_favicons(new)
        if path.name == "index.html":
            new = patch_index_products(new)
        if new != text:
            path.write_text(new)
            print("patched", path.relative_to(ROOT))

    # services research card should already point to /research
    services = (ROOT / "services.html").read_text()
    services = services.replace("href=\"/research.html\"", "href=\"/research\"")
    (ROOT / "services.html").write_text(services)

    print("done")


if __name__ == "__main__":
    main()
