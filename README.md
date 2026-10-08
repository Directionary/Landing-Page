# Directionary — Landing Page

Public landing site for the [Directionary](https://github.com/Directionary) app.

**Live:** https://directionary.github.io/Landing-Page/

## What this is

A single static page (plain HTML + CSS, no build step) introducing Directionary —
an app that helps people with visual impairments record and follow routes they
can trust, described by what they will hear, smell and feel rather than only
where to turn.

- `index.html` — page content
- `styles.css` — dark theme matching the app (gold `#f9cb42` on `#060605`)

## Preview locally

```bash
python3 -m http.server 20000
```

then open http://localhost:20000/.

## Deploy

GitHub Pages serves this repo directly (legacy build, `main` / root). Every push
to `main` redeploys automatically — no action needed.

## Placeholders to resolve before launch

- Store buttons are disabled with "(soon)" — swap in real Play / App Store URLs.
- `Screens` section holds dashed placeholders until real screenshots are filmed.
- Contact: directionary@guidedogs.org.sg
