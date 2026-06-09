// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// `site`/`base` are injected by CI (GitHub Pages) so the build works under
// https://<owner>.github.io/<repo>/. Locally they default to the root.
const site = process.env.SITE_URL || undefined;
const base = process.env.BASE_PATH || undefined;

// https://starlight.astro.build/reference/configuration/
export default defineConfig({
  site,
  base,
  integrations: [
    starlight({
      title: "loguru-themes",
      description:
        "Curated color themes and Unicode level icons for loguru, applied in one call.",
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
      // English is the root locale; Russian lives under /ru/.
      defaultLocale: "root",
      locales: {
        root: { label: "English", lang: "en" },
        ru: { label: "Русский", lang: "ru" },
      },
      sidebar: [
        {
          label: "Start here",
          translations: { ru: "Начало" },
          items: [{ slug: "getting-started" }],
        },
        {
          label: "Guides",
          translations: { ru: "Руководства" },
          items: [
            { slug: "themes" },
            { slug: "icons" },
            { slug: "customizing" },
            { slug: "color-scheme" },
            { slug: "own-logger" },
          ],
        },
        {
          label: "Reference",
          translations: { ru: "Справочник" },
          items: [
            { slug: "api-reference" },
            { slug: "examples" },
          ],
        },
      ],
    }),
  ],
});
