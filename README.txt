Relogic multi-page website package

Pages
- index.html — main/front page
- services.html — service chooser
- research.html — medical & epidemiological research consultancy portfolio
- digital-product.html — digital product portfolio

Navigation update
- The homepage button previously labelled “Explore All Solutions” now reads “Explore All the Services” and opens services.html, matching the Services navigation behavior.

Relogic logo
- All pages reference the same Relogic logo path used by the original site:
  images/team/relogic-logo-main-crop.png
- Fallback path:
  images/team/relogic-logo_main.png
- Add your original Relogic logo files to images/team/ when deploying this package.

Research graph images
The Research page now contains five medical/epidemiological study showcases. Each uses a local SVG graph placeholder that you can replace with the final graph from the consultancy-led study while keeping the same filename:
1. images/research/dengue-seasonality-graph.svg
2. images/research/maternal-neonatal-graph.svg
3. images/research/respiratory-age-risk-graph.svg
4. images/research/diabetes-cohort-graph.svg
5. images/research/hai-surveillance-graph.svg

You can also change the <img src=...> in research.html if your final figures use PNG/JPG/WebP filenames.

OUR PEOPLE UPDATE
-----------------
- people.html combines Leadership, Advisors and Core Team on one page.
- Every people card links to an individual static profile page in /people/.
- /people/profile.css is shared by all profile pages.
- Profile pages intentionally show only confirmed name/role/team data and provide clearly marked fields for verified biography, expertise, selected work, credentials and links.
- Keep the existing team photographs and Relogic logo files inside images/team/.

LATEST UPDATE
- All 12 individual people pages now contain complete professional profile copy.
- Public web material is used only for confident name matches; other profiles are role-based to avoid false identity matching.
- See PEOPLE_PROFILE_SOURCES.txt for the research basis.
- The homepage Relogic mobile showcase has been rebuilt as three realistic mobile-device UI screens with status bars, device shells, navigation and app controls.
- All new mobile screens use the same Relogic logo paths as the rest of the site.

RESPONSIVE UPDATE
-----------------
A shared responsive.css layer now supports the complete site across:
- Small phones (320px+)
- Standard phones (360–430px)
- Tablets (600–900px)
- Laptops (1024–1366px)
- Desktop displays (1440–1920px+)

Responsive behavior includes mobile-safe typography, touch-sized controls, horizontal navigation on secondary pages, stacked layouts where appropriate, adaptive research/product diagrams, responsive person profiles, mobile-friendly project intake forms, and a horizontally swipeable Relogic mobile UI showcase on narrow screens.
