# Handoff: Combe Consumer Insights Hub — Maggiore redesign

## Overview
Dark-mode redesign of the Combe Consumer Insights Hub (currently at project-2oow2.vercel.app/combe), restyled with the **Maggiore Design System**. Single scrolling page: Nav → Hero → Brand Portfolio → Key Insights → Social Listening → IEP → IEP V2 → Ask the Hub → AI Audit → JTBD → Footer.

## About the Design Files
The files in this bundle are **design references created in HTML** — they show intended look and behavior, they are NOT production code to copy directly. The task is to **recreate this design in the target codebase's existing environment** (React/Next.js or whatever the hub currently runs on), using its established patterns, and wiring the **real data** where this mock uses illustrative values.

- `combe-insights-hub-standalone.html` — self-contained, opens in any browser. Primary visual reference.
- `source/Combe Insights Hub.dc.html` — annotated source (all styles inline; data arrays at the bottom in the `Component` class).
- `source/tokens/colors_and_type.css` — the full design-token sheet (colors, type, spacing, radii, shadows, easing). **Port these as CSS custom properties verbatim.**
- `source/tokens/fonts.css` + `source/assets/` — font-face declarations and brand assets (white Maggiore logo SVG, balloon/divider motifs).

Fonts: **Neue Haas Grotesk Display** (headings) and **Switzer** (body/UI) are licensed brand fonts self-hosted in the design system — copy the `.ttf` files from the existing brand package, do not swap for Google Fonts. **JetBrains Mono** (metadata/URLs) loads from Google Fonts.

## Fidelity
**High-fidelity** for layout, color, typography and spacing — recreate pixel-perfect.
**Illustrative data** (replace with real values from the hub's backend):
- Social Listening report cards (6 shown; real hub has 17)
- IEP experiment cards (codes, titles, round counts)
- AI Audit visibility scores (72/58/34%), table rows and per-platform cells
- JTBD phase names

Verbatim-real content (taken from the live hub): brand counts (Astroglide 6/0, Just For Men 6/3, Vagisil 5/1), all Key Insights bullets, all section intro paragraphs, KPIs 17 SL Reports / 4 IEP Experiments, "Last updated: June 2026".

## Design Tokens (core)
Colors — dark scale: page bg `#111118` (--ink-deep), card fill `#1b1b21` (--ink-base), card hover `#2a2a2a` (--ink-raised), hairline `#3a3a42` (--ink-line), strong border `#535353`. Text: `#fcfcfc` (--fg), `#c9c9d0` (--fg-2), `#b2b2b2` (--fg-3).
Brand: primary teal `#2cced6` (hover `#00aab0`), green `#00ff99` / `#00d97f`, lavender `#a399ff`. Semantic: warn `#edc624`, error `#ef446f`.
Aurora gradient (hero/footer only, never behind paragraphs): `radial-gradient(120% 85% at 50% 115%, rgba(44,206,214,.45), rgba(0,255,153,.22) 26%, rgba(163,153,255,.24) 50%, transparent 72%)`.
KPI numbers: `linear-gradient(120deg, #2cced6, #00ff99)` with `background-clip: text`.
Type scale: h1 88px Roman 400 / ls -0.022em; section h2 44px Roman 400 / ls -0.012em; card titles 18–26px Medium 500; body 15px weight 350 (Extra Light) with 500 emphasis; overlines 12px/600/uppercase/ls 0.18em in teal; metadata JetBrains Mono 11–12px.
Spacing: sections `padding: 96px 80px`, hero `160px 80px 120px`, max content width 1280px centered. Radii: 6px cards, 999px pills, 2px legend swatches. No shadows on dark cards — elevation = fill step up. Easing `cubic-bezier(0.2,0.8,0.2,1)`, 180ms UI.

## Screens / Sections
1. **Nav** — sticky, 64px, `rgba(17,17,24,0.78)` + `saturate(140%) blur(12px)`, 1px bottom hairline. Left: "Combe" (NHG 20px) · 1px divider · white Maggiore logo (16px tall). Right: 8 links 13px, active = white + 1px teal underline, inactive `--fg-2`. Anchor navigation to section ids: `#hub #social-listening #iep #iep-v2 #insights #ask #ai-audit #jtbd`.
2. **Hero** (`#hub`) — centered, aurora radial from bottom. Overline "COMBE · POWERED BY MAGGIORE" → h1 "Consumer Insights Hub" with "Insights" in teal → 19px lead → two KPI stats (56px gradient-clipped numbers, uppercase labels) separated by a 1px vertical hairline → mono "Last updated: June 2026".
3. **Brand Portfolio** — 3-col grid with 1px gaps on `--ink-line` (cells `--ink-base`, hover `--ink-raised`). Each: brand name 26px + category label right-aligned, SL/IEP counts 36px.
4. **Key Insights** (`#insights`) — 3 columns, brand header uppercase with teal bottom border, bullets prefixed by teal em-dash, 14px light text.
5. **Social Listening** (`#social-listening`) — 2-col intro (copy left; Mentions/Search Behavior/Reviews rows right, lucide icons `message-circle` `trending-up` `star`). Filter pills (Brand / Year; active = teal fill + dark text, inactive = outline). Report card grid 3-col: brand pill + mono year, 18px title, "Social Listening" + `arrow-up-right` teal icon pinned to bottom.
6. **IEP** (`#iep`) — intro + Stopping/Closing Power cards (`zap`, `shopping-cart`); 4-col experiment cards: mono code, title, brand pill + rounds.
7. **IEP V2** (`#iep-v2`) — soft aurora wash; "IEP V2" + green NEW pill; 3 feature cells (`activity`, `refresh-cw`, `radar`) in 1px-gap grid.
8. **Ask the Hub** (`#ask`) — centered 760px. Search bar: `--ink-base` fill, **1px teal border + soft teal glow** `0 0 32px -8px rgba(44,206,214,.35)`, search icon, placeholder query, square teal "ASK" button (uppercase, ls 0.16em, dark text). Below: green 6px dot + mono "SEMANTIC SEARCH ACTIVE".
9. **AI Audit** (`#ai-audit`) — header row with copy left, mono meta right ("Q2 2026 — 18 prompts audited"). Platform mono pills. 3 score cards: brand + big % (green `#00d97f` / amber `#edc624` / red `#ef446f`) + 4px progress bar + "N prompts". Legend (10px square swatches): Mentioned=green, Not mentioned=gray `#535353`, Positive=teal, Neutral=lavender. Table: grid `2.4fr repeat(5,1fr) 0.8fr`, uppercase header row on `--ink-base`, cells are 10px colored squares, score column mono right-aligned. Row hover: bg → `--ink-base`.
10. **JTBD** (`#jtbd`) — header + "OPEN FULL PAGE ↗" outline button (uppercase, hover: fill `--ink-raised`, border teal). Rows per brand: name 20px + phase pills (mono teal number 01/02/03 + label).
11. **Footer** — soft aurora from bottom, Combe · Maggiore lockup, mono `maggiore.cl · marketing@maggiore.cl`, caption row above 1px hairline.

## Interactions & Behavior
This mock is visual-only. Expected behavior to implement:
- Nav: smooth-scroll anchors, active state follows scroll position.
- Filter pills: filter the report grid (Brand × Year), single-select per group, "All" default.
- Report / experiment / AI-audit cards: clickable → detail views (audit card → prompt-by-prompt breakdown).
- Ask the Hub: real input + submit → semantic search results state.
- Hovers everywhere: fill step `--ink-base → --ink-raised`, border `--ink-line → #535353`, 180ms, **no translate/scale**.
- Buttons: teal fill hover → `#00aab0`; outline hover → fill `--ink-raised` + teal border.
- Focus: `outline: 2px solid #2cced6; outline-offset: 2px`.

## Icons
Lucide (CDN or npm `lucide-react`), stroke ~1.75. Names used: `message-circle, trending-up, star, arrow-up-right, zap, shopping-cart, activity, refresh-cw, radar, search`.

## Assets
- `source/assets/logo-blanco.svg` — white Maggiore lockup (fills set to `#fcfcfc`; use on dark only).
- `source/assets/isologo-blanco.png` — compact M mark (favicon/avatar).
- `source/assets/balloon-teal.png`, `divider-arrows.png` — optional brand motifs, not placed in this layout.

## Not covered
Responsive/mobile layout was not designed (desktop 1280px+ reference). Design-system guidance if needed: 24px gutters, single-column grids, nav collapses.
