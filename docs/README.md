# Documentation site

Docs for `loguru-themes`, built with [Astro Starlight](https://starlight.astro.build/).

## Develop

```bash
cd docs
npm install
npm run dev      # http://localhost:4321
```

## Build

```bash
npm run build    # output in docs/dist/
npm run preview  # serve the built site
```

## Languages

The site is bilingual (Starlight i18n):

- English — root locale, pages in `src/content/docs/*.md(x)`.
- Russian — pages in `src/content/docs/ru/*.md(x)`, served under `/ru/`.

A language switcher appears in the site header automatically.

## Structure

- `src/content/docs/*.md(x)` — English pages; `src/content/docs/ru/` — Russian.
- `astro.config.mjs` — site config, i18n locales, and sidebar.
- `public/llms.txt` — the LLM-friendly index (served at `/llms.txt`).

An identical `llms.txt` is kept at the repository root for discoverability.
