---
name: ui-design
description: The one design skill for the user. Use for any UI or visual design work, such as building a landing page, website, web app screen or dashboard, redesigning or auditing an existing UI, reviewing a mobile or desktop app against Apple HIG, writing a DESIGN.md design system, or making concept images and brand kits when an image tool exists. Style modes (Nothing, Industrial Brutalist, Minimalist/Notion-like) load only when the user names them. iPhone lock-screen wallpapers and widgets go to the separate iphone-widget-design skill.
---

# ui-design

This bundle merges 15 former design skills. **This file holds the final decisions.** The `sources/` folder keeps each original skill unchanged so you can look up detail. **When a source file contradicts this file, this file wins.** Read only the source files the current task needs.

## 1. Routing: what to read for each task

| Task | Read |
|---|---|
| New page, landing page or site | §2–§4 here, then `sources/hallmark/GUIDE.md` (macrostructures, nav/footer archetypes, components) and `sources/taste-v2/GUIDE.md` §3–§6 (React/Next/Tailwind rules) |
| Redesign of an existing UI | `sources/redesign/GUIDE.md` (audit list, fix order), `sources/taste-v2/GUIDE.md` §11 (what to preserve), `sources/hallmark/references/verbs/redesign.md` |
| Audit a web UI, no edits | `sources/hallmark/references/verbs/audit.md` + `references/slop-test.md`, and §5 here |
| Review a mobile or desktop app | `sources/apple-hig/GUIDE.md`, its `references/hig-lookup.md`, then 3–8 HIG files |
| Dashboard or data screen | §6 here, `sources/modes/nothing/references/components.md` (data viz only, not its look) |
| MOTION dial 8–10 (agency, awwwards, showcase brief) | `sources/motion-max/` as an arsenal: `gpt-taste`, `high-end`, `taste-v1`. Take their motion recipes only. Their colour, font, hero and eyebrow rules are overruled by §3. |
| "Nothing style" (only when named) | `sources/modes/nothing/` in full. This mode keeps its own colours, #000, ALL CAPS labels and no-shadow rules. §3 accessibility rules still apply. |
| "Brutalist" or "industrial" (only when named) | `sources/modes/brutalist/GUIDE.md`. Radius 0, uppercase and tight leading are allowed in this mode. |
| "Minimalist", "Notion-like", "editorial document" (only when named) | `sources/modes/minimalist/GUIDE.md` |
| Concept images before code | Only if an image tool exists. Check with ToolSearch for a `generate-image` tool, such as the Canva connector. Web pages use `sources/concept/web/`, phone apps `sources/concept/mobile/`, image-first builds `sources/concept/image-to-code/`, brand identity `sources/concept/brandkit/`. With no tool, write a short text art direction instead and say so in one line. |
| DESIGN.md for Stitch or another agent | `sources/stitch/GUIDE.md` and `DESIGN.md` as the template. Fill the values with the decisions in §3. |


## 2. Workflow for a build

1. **Pre-flight scan** (hallmark step 0). Read package.json, the Tailwind version, the fonts, colour tokens, spacing and motion libraries already in use. **Existing brand tokens win over this file.**
2. **Design Read.** Print one line: `Reading this as: <page kind> for <audience>, with a <vibe> language, leaning toward <system or aesthetic>.` Ask at most one question, and only if the brief is truly ambiguous. Otherwise proceed.
3. **Set the dials.** VARIANCE, MOTION and DENSITY, each 1–10. Use the presets in taste-v2 §1.B. The default is 8/5/4. Print the dials next to the Design Read.
4. **Pick the structure** from hallmark: one macrostructure plus nav and footer archetypes. If `.hallmark/log.json` exists, rotate away from the last 3 entries.
5. **Build with tokens.** Every colour, font, radius, space and duration comes from a CSS variable or Tailwind theme token. Nothing is hardcoded mid-file.
6. **Check** with §7. For a full page, also run hallmark `slop-test.md` and taste-v2 §14.

## 3. Locked decisions (these resolve the conflicts between sources)

### Typography
- **Inter is not a default.** Use it only for dashboards, accessibility-first or public-sector briefs, a neutral "Linear-style" ask, or when the project already uses it.
- **Serif** only for editorial, luxury or heritage briefs. Fraunces and Instrument Serif are allowed, but never use the same serif in two projects in a row.
- At most 2 families plus an optional mono. Emphasis uses the same family's weight or italic.
- **Vietnamese:** the user's UIs are Vietnamese-first. Before choosing a font, confirm it has the Vietnamese subset: test the string `Tiếng Việt: ẩ ặ ữ ỡ Đ` and check `subset=vietnamese` on Google Fonts. Be Vietnam Pro is a known-good choice. Many Fontshare faces (Satoshi, Cabinet Grotesk, Clash Display, General Sans) lack Vietnamese glyphs, so use them for Latin-only display text at most.
- Hero H1: 2 lines max on desktop (3 is the hard ceiling). Body text at least 16px, measure 45–75ch, line-height 1.5–1.65. Display tracking −0.02 to −0.04em, line-height 1.05–1.2. Brutalist mode may go to 0.9.
- Sentence case for UI text. Use all-caps only for short labels, with 0.06–0.12em tracking.
- Load fonts with next/font or self-hosted @font-face (`font-display: swap`). A Google Fonts `<link>` is fine for single-file HTML or artifacts.
- `tabular-nums` on every number that changes or sits in a column.

### Colour
- Define tokens in **OKLCH** (Tailwind 4 uses it natively). Hex is fine in single-file artifacts.
- **One accent** (two at most), on under about 5% of the area. One grey family, slightly tinted toward the brand hue. Never mix warm and cool greys.
- **No pure #000 or #fff** as web surfaces; use tinted near-black and near-white. Exceptions: Nothing mode and OLED or lock-screen work, where #000 is correct.
- Banned by default: the purple-to-blue "AI" gradient, aurora blobs, floating orbs, neon or outer glows, gradient text on headlines, and the beige + brass + espresso "premium" palette (hex list in taste-v2 §4.2). Any of these is allowed when the brand itself asks for it.
- Dark mode: consumer-facing pages support both modes through tokens and respect `prefers-color-scheme`. Show elevation by lightness, not shadow. Never flip theme between sections.
- **Contrast:** WCAG AA. Body and secondary text need 4.5:1; large text and UI boundaries 3:1. This also applies to muted, timestamp and placeholder text. Some sources break this (Stitch `#94A3B8`, Nothing `#666`); fix those values.

### Shape and depth
- **One radius system per project:** sharp (0), soft (8–16px) or pill. Inner radius = outer radius − padding.
- Container ladder, in order: spacing, then a divider, then a border, then a surface card. A card exists only when elevation means hierarchy.
- Shadows: "whisper" level, tinted with the background hue, never stacked, never a glow.
- Glass (backdrop-blur) only on a fixed or sticky nav, or on an Apple-adjacent premium brief. Always add a solid fallback for `prefers-reduced-transparency`.

### Layout
- Use CSS Grid. Use `min-h-[100dvh]`, never `h-screen`. Fix horizontal overflow at its cause; never hide it with `overflow-x-hidden` on the wrapper.
- **Hero:** asymmetric by default when VARIANCE > 4. Centre it only for manifesto, launch or minimal briefs. At most 4 text elements. 1 primary CTA plus at most 1 secondary. No stats, badges, pills, avatar rows or logo walls in the hero.
- **Eyebrows:** at most 1 per 3 sections. No section numbering such as "01 / 02" or "Step 1". No decorative meta labels.
- No row of 3 equal feature cards. No more than 2 image-plus-text splits in a row. Use at least 4 layout families across 8 sections. Vary section padding instead of repeating one value.
- Test at 320, 375, 414, 768, 1024 and 1440px. Collapse to one column below 768px. No horizontal scroll. No clickable text that wraps to 2 lines. Touch targets at least 44px.

### Motion (driven by the dial)
- **MOTION 1–3:** hover and press feedback only.
- **MOTION 4–7 (default 5):** one orchestrated page entrance plus a reveal-once on key blocks. Use CSS or `motion/react`.
- **MOTION 8–10:** only when the brief says agency, awwwards, showcase or similar. This unlocks the `sources/motion-max/` arsenal (GSAP pin and scrub, word-by-word reveal, sticky card stacks, horizontal pan).
- Always:
  - Animate only `transform` and `opacity`. Never `transition: all`.
  - No bounce or elastic easing on UI chrome. No `window` scroll listeners.
  - Never put GSAP and `motion/react` in the same component tree.
  - `prefers-reduced-motion` is mandatory.
  - Infinite loops only where they carry meaning, such as a status dot or at most one marquee.
- Default timing (hallmark): 120ms micro, 220ms short, 420ms long; ease-out `cubic-bezier(0.16,1,0.3,1)`. Exits run at 60–75% of the enter time. Stagger 60ms, capped at about 500ms total.

### Icons
- **Phosphor** is the default. Use Lucide if the project already uses it or uses shadcn.
- One family and one stroke weight per project. Never use emoji as icons.

### Content (honest by default)
- **Images:** use an image tool if one exists, else `https://picsum.photos/seed/<descriptive-seed>/<w>/<h>`, else a labelled placeholder block.
- **Numbers, logos, testimonials:** real or visibly marked as sample. Never invent metrics, quotes or client logos.
- Banned filler copy: Elevate, Seamless, Unleash, Next-Gen, Revolutionize, Game-changer, Delve, Unlock, "In today's fast-paced world". This also applies to the Vietnamese equivalents (e.g. "nâng tầm", "đột phá", "liền mạch").
- Banned placeholder names: John Doe, Jane Smith, Acme, Nexus, SmartFlow, Flowbit, NovaCore, Lorem ipsum.
- No em dash or en dash as a separator in UI copy. Use a hyphen for ranges.

### States and components
- Every interactive component has these states: default, hover, focus-visible, active, disabled, loading, error, and success where relevant.
- Loading uses a skeleton that matches the layout (Nothing mode uses bracket text instead). Errors appear inline. Toasts only for transient confirmations.
- Labels sit above fields, never placeholder-as-label. Error text goes below the field.
- No re-drawn browser, phone or IDE chrome made from divs. Use a real screenshot or nothing.

### Stack
- React and Next.js: Server Components by default; motion lives in small `'use client'` leaves.
- Check package.json before importing a package. If it is missing, print the install command first.
- Use Tailwind v4 syntax only in v4 projects.

## 4. Dial presets (quick reference)

| Brief | VARIANCE / MOTION / DENSITY |
|---|---|
| SaaS landing | 7 / 5 / 4 |
| Agency or showcase | 9 / 8 / 3 |
| Premium consumer | 7 / 6 / 3 |
| Portfolio | 8 / 6 / 3 |
| Editorial or blog | 6 / 4 / 3 |
| Public sector or form-heavy | 3 / 2 / 5 |
| Dashboard | 3 / 2 / 7 |
| Redesign, preserve | match the current site, MOTION +1 |

## 5. Audit output (web or app)

Return a ranked list and do not edit anything. Each finding has:
- **What:** the problem, with file:line or a screen reference.
- **Why:** the rule it breaks.
- **Fix:** a concrete change with values.

Severity runs Critical (accessibility, broken on some devices), High, Medium, Low. Rank by severity × effort. Mention what already works. Do not over-critique.

## 6. Dashboards

- **Purpose first.** Start from the decision the dashboard serves. Put the 3 numbers that matter most at the top, each compared with the previous period. Breakdowns go below, filters at the top.
- **Density and type.** DENSITY 6–9. Inter is allowed here. Numbers use `tabular-nums` (or mono) and are right-aligned in tables. No zebra striping. Prefer dividers to cards.
- **Charts.**
  - Lines 1.5–2px. Label series directly instead of using a legend box. Horizontal grid lines only.
  - Separate categories by opacity or pattern before colour. Always show the actual number.
- **No fakes.** No chart or sparkline without real or clearly sample data. No infinite loops on cards; a single status dot is fine.
- **States.** Design the empty, loading and error states. State the source and last-refresh time.

## 7. Final check (every build)

- [ ] Design Read and dials printed. Existing tokens preserved.
- [ ] The font renders Vietnamese correctly. At most 2 families. Hero H1 is 2 lines or fewer.
- [ ] One accent. No pure #000/#fff (outside OLED or Nothing work). All text passes AA, including muted text.
- [ ] One radius system. No stacked shadows or glow. Glass has a fallback.
- [ ] Hero holds 4 or fewer text elements and 2 or fewer CTAs. Eyebrows ≤ 1 per 3 sections. No 3-equal-cards row.
- [ ] Motion matches the dial. Only transform and opacity animate. Reduced motion is handled. GSAP and motion/react are not mixed.
- [ ] Phosphor (or the project's existing set), one stroke weight, no emoji icons.
- [ ] No invented numbers, quotes or logos. No banned filler words or names.
- [ ] Every interactive element has all its states, a visible focus ring and a 44px target.
- [ ] Works at 320–1440px with no horizontal scroll.
