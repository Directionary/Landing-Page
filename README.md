# Directionary — Website

Public website for [Directionary](https://github.com/Directionary), a community-driven
route-learning and wayfinding app for people with visual impairments. Developed in
collaboration with Guide Dogs Singapore.

**Live:** https://directionary.app/

## What this is

A static site: plain HTML and CSS with one small JavaScript file for the light/dark
theme toggle. There is no build step and there are no dependencies.

| Path | Purpose |
|---|---|
| `index.html` | Home: hero, key features, how it works, approach, about |
| `features/index.html` | Features |
| `about/index.html` | About, collaboration, principles |
| `support/index.html` | Support, accessibility feedback, account deletion |
| `privacy/index.html`, `terms/index.html` | Draft legal pages (footer links) |
| `styles.css` | Shared styles and design tokens (light and dark) |
| `assets/theme.js` | Theme toggle + `prefers-color-scheme` auto-detect (stored choice wins, else system; follows system live); stores the choice in `localStorage` |
| `assets/fonts/` | Self-hosted Inter and a Material Symbols icon subset (see its README) |
| `assets/` | Logo, header mark and favicons |
| `CNAME` | Custom domain (`directionary.app`). Do not edit. |

Links and assets use root-relative paths (`/styles.css`), which work on the custom
domain and with the local preview below.

## Preview locally

```bash
python3 -m http.server 20000
```

then open http://localhost:20000/. Serve from the repository root so root-relative
paths resolve.

## Checks

```bash
node --check assets/theme.js
python3 scripts/validate.py .
npx --yes htmlhint@1.9.2 "**/*.html"
```

`scripts/validate.py` needs only the Python standard library. It verifies required
files, the `CNAME` hostname, per-page `lang` / `title` / `viewport` /
`theme-color` / `theme.js`, and that every internal link and asset resolves
(including `#fragment` ids). `.htmlhintrc` holds the HTML lint rules.

CI (`.github/workflows/ci.yml`) runs validate + HTML lint on pushes and pull
requests to `main`. Heavier scans live in `.github/workflows/scan.yml`: gitleaks
secret scan (pinned in `GITLEAKS_VERSION`) and lychee link check (pinned in
`LYCHEE_VERSION`), on push/PR plus weekly. All workflows are shell-steps only so
they run under `act` locally; `.actrc` pins the `ubuntu-latest` image to
`catthehacker/ubuntu:act-24.04` to match GitHub (lychee needs its newer glibc).

## Deploy

GitHub Pages serves this repo directly (legacy build, `main` / root). Every push to
`main` redeploys automatically. Work on a feature branch and merge through a pull request.

## Launch requirements

- Store buttons: none yet. The hero shows "Coming soon" until verified Google Play and
  App Store links exist.
- Privacy Policy and Terms of Use are drafts with sections marked "To be confirmed" /
  "Legal review". They need the legal operator, actual data practices, Singapore PDPA
  review and app store requirements before release.
- Account deletion: the process on `/support/#account-deletion` is not yet confirmed.
- About page acknowledgements: names, roles and affiliations are provisional. Confirm each
  with the person, and obtain permission to publish, before launch. To link a name to
  LinkedIn later, wrap it as shown in the comment above the `.people` list in `about/index.html`
  (only when a real URL exists).
- Contact: directionary@guidedogs.org.sg
