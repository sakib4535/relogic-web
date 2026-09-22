# Relogic project structure

Previously everything sat in one root folder (`index`, `index-main`, `services`, `services_restyled`, `responsive`, verification files, previews). That made navigation feel like jumping between different sites.

```
relogic-site/
├── index.html                 Home / studio
├── services.html              Practice chooser
├── research.html              Research consultancy
├── projects.html              Digital products
├── people.html                Team directory
├── people/                    Individual profile pages
├── assets/
│   ├── css/                   Shared tokens, chrome, readability
│   └── js/site.js             Shared nav, active states, link hardening
├── data/                      site.json, team.json, projects.json
├── src/build_site.py          Rebuild chrome onto page files
├── images/                    Keep original image paths
├── archive/                   Old duplicate pages
├── docs/                      Editorial notes
├── robots.txt
├── sitemap.xml
├── _headers / .htaccess       Host security headers
└── .well-known/security.txt
```

Keep these at the public root so existing URLs do not break:

- `googled4c684d6f81a8ef7.html` (Search Console verification)
- `images/`
- `responsive.css` (compatibility stub)
