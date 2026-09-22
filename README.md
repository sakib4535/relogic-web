# Relogic site system

Same studio. Same pages. One structure.

The old root mixed `index`, `index-main`, `services`, `services_restyled`, verification files, previews and page CSS in a single folder. Clicking **Services** felt like opening a different website because each file had its own header, link set and colour weight.

This package keeps every page’s internal design — hero carousels, study cards, product modules, people portraits — and puts them on one chrome system.

## What changed

- One navigation and one footer on Home, Services, Research, Digital Product, Our People and profile pages.
- Research is in the main nav on every page (it was missing from Home).
- `digital-product.html` links now point at `projects.html`.
- Body copy is brightened on dark surfaces so text is readable. Light research paper sections keep dark ink.
- Four injected “share redirector / scroll lock” scripts were removed from `index.html`. Those scripts overrode `addEventListener` and were not part of the product.
- Security headers, `robots.txt`, `sitemap.xml` and `.well-known/security.txt` are included.
- Team and project records live in `data/` so the site can be maintained as a system.

## Public pages

| File | Role |
|---|---|
| `index.html` | Studio home |
| `services.html` | Research vs Digital Product |
| `research.html` | Medical / epidemiology practice |
| `projects.html` | Product systems |
| `people.html` | Team directory |
| `people/*.html` | Individual profiles |

## Drop in your existing media

Copy these from the current repo into this folder, keeping the same paths:

```
images/team/
images/research/
googled4c684d6f81a8ef7.html
```

Move leftovers into `archive/`:

```
index-main.html
services_restyled.html
preview files
```

## Rebuild chrome after content edits

```bash
python3 src/build_site.py
```

The builder copies page bodies from `/home/workdir/attachments` in this workspace. On your machine, point `ATTACH` in `src/build_site.py` at your source HTML if you need to regenerate.

## Security baseline

- Directory listing disabled (`.htaccess`)
- `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`
- External links get `rel="noopener noreferrer"`
- `/archive`, `/docs`, `/src` and `/data` are disallowed in `robots.txt`
- Old aliases redirect: `/digital-product.html` → `/projects.html`

## Colour

Shared tokens in `assets/css/tokens.css` plus `assets/css/readability.css` lift muted greys (`#5e7089`, `#8b98ad`) to readable light steel (`#d5e0ee`, `#f4f8fd`) on dark backgrounds. Section artwork, grids, orbits and cards were not removed.


## Pretty URLs

Public paths hide `.html`:

- `/services`
- `/research`
- `/research/medical`
- `/research/startups`
- `/research/enterprise`
- `/projects`
- `/people`
- `/people/hasnain-imtiaz`

Apache uses `.htaccess`. Netlify uses `_redirects`.

## Brand icons

Tab and search icons live in `assets/brand/` plus root `favicon.ico` and `site.webmanifest`.
Replace those files with the official lockup when you want the exact wordmark in search results.


## Run the site (required for the form)

```bash
python3 tools/serve.py
```

Open http://127.0.0.1:4173/

Project intake posts to `/api/intake`. Each brief is stored in `data/leads/` as JSON plus `inbox.jsonl`.

Read submissions at http://127.0.0.1:4173/admin?key=YOUR_KEY

The key lives in `data/admin.key` (default `relogic-admin`). Change that file before going live.

If the server is down, the form still opens a mail draft to hello@relogic.ai.

## Navigation

Top bar: Home, About, Services, Digital Product, Our People.

Research is reached from Services → Research Consultancy, then Medical / Startup and SMEs / Enterprise.
