# Visual Rules for OLED Lock Screens

Load the `ui-design` skill (its Apple HIG review route) alongside this for a formal HIG audit. This file covers what is
specific to a black lock-screen graphic sitting under system UI.

## Ground

Use **pure `#000000`**. On OLED those pixels are off — it saves power and the wallpaper melds
into the bezel. A near-black like `#0a0a0b` reads as a grey rectangle against the true black of
the hardware.

## The low-opacity trap

The most common mistake: building the whole palette from low-alpha white.
`rgba(255,255,255,0.16)` looks fine on a bright monitor in a bright room and is **invisible on
a phone outdoors**. It reads as "unfinished" rather than "subtle".

Floors that actually work on black:

| Role | Minimum | Notes |
| --- | --- | --- |
| Primary / hero text | `#fcfaf6`–`#ffffff` | ~20:1 |
| Emphasised figures | a real accent hue at full saturation | ~11:1 |
| Supporting text | `#d3cdc1` (~13:1) | **not** `rgba(255,255,255,0.6)` (~6:1) |
| Filled data marks | `rgba(accent, 0.46)` | warm, clearly present |
| Empty / track marks | `rgba(255,255,255,0.15)` | visible as texture, not as content |

WCAG AA needs 4.5:1 for text under 18 pt. Clear it comfortably — the phone will be read in
sunlight.

## Hierarchy: exactly one hero

Decide the single most important element and give it **all three** signals at once:

1. **Largest** — a clear ratio, not a nudge. ~1.6× the next element minimum.
2. **Brightest** — it is the only thing at full white. Everything else steps down.
3. **Best positioned** — highest in the free band, so notifications are least likely to cover it.

Everything else steps down deliberately. If two elements compete, neither reads.

## Colour discipline

Assign each colour **one meaning** and hold it:

- White → the hero, and nothing else.
- One accent hue → one semantic role (e.g. "time / progress": the current-day marker, the
  countdown figure, the percentage).
- Warm neutral grey → supporting words.

A warm neutral (`#d3cdc1`) beside a warm accent reads as designed; a pure grey (`#888`) beside
it reads as an unstyled default. Bias neutrals slightly toward the accent's hue.

Do not encode meaning in hue alone — the elapsed/remaining distinction should also differ in
brightness and, ideally, in temperature (warm vs cool), so it survives colour blindness and
monochrome accessory-widget rendering.

## Typography

- **One family.** Embedded webfont (see `render-pipeline.md`). Inter is a good SF stand-in.
- **Weights 400–700 only.** Never Thin/Light — HIG is explicit, and thin weights disintegrate
  at small sizes and in sunlight.
- **Sentence case.** Not ALL CAPS, not Title Case. Uppercase with wide tracking is a dated
  "eyebrow" tic; if a label needs to recede, make it smaller and dimmer, not shouty.
- **Minimal tracking.** Modern sans faces are optically spaced already. Slight negative
  tracking (`-0.015em`) on large display text; ~0 elsewhere.
- **Minimum 11 pt** (≈2.8cqw on a 390 pt canvas). Below that it is decoration, not information.
- `font-variant-numeric: tabular-nums` on anything that counts, so digits don't jitter day to
  day.

## Composition

- Group elements that are the same information. A "N days left" figure belongs **directly
  above** the grid that shows those days, not floating at the other end of the layout.
- **Avoid `justify-content: space-between`** for a 2–3 item stack. It pins items to opposite
  edges and produces the lopsided gap that reads as "not centred". Use `justify-content:
  center` with one deliberate section gap.
- **Optically centre within the free band**, not within the screen. The screen's true centre is
  behind the system clock.
- Give the hero real negative space. Crowding is what makes a design feel cheap.

## Data marks (dot grids, rings, bars)

- More columns → smaller dots. Fewer columns → a taller block. Choose the column count where
  `365 mod cols` leaves a **decent remainder** — a final row with 1 dot looks like a bug.
  For 365: 27 cols → 14 rows, last row 14 ✅. 26 cols → last row 1 ✗. 25 cols → last row 15 ✅.
- Span the **full content width**. A grid at 58% of the width reads as small no matter how the
  dots are coloured.
- Mark "now" with more than colour: full opacity, plus a tight concentric ring, plus a soft
  halo. Keep the halo small — a wide blur reads as a smudge at @3x.

## Always preview under system UI

Build the preview page with a mock clock, date, widget tray, notification card, home indicator
and camera/flashlight buttons layered over the real design. Embed the actual page in an
`<iframe>` rather than copying its CSS, so the preview can never drift from the product.

```html
<div class="screen">                     <!-- aspect-ratio: 1170/2532; container-type: size -->
  <iframe src="index.html" scrolling="no"></iframe>
  <div class="ios"> … clock, tray, notification, home indicator … </div>
</div>
```
