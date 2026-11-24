---
name: iphone-widget-design
description: >
  Design and ship iPhone lock-screen wallpapers, widget-style graphics, and auto-updating
  phone visuals built from HTML/CSS and delivered through iOS Shortcuts. Use this skill for:
  lock screen wallpaper, iPhone widget design, home screen widget, year/life calendar
  wallpaper, countdown wallpaper, daily-updating wallpaper, Shortcuts automation that sets a
  wallpaper, HTML-to-PNG rendering for a phone, or any request to make something look good on
  an iPhone lock screen. Also use when a phone graphic comes out blurry, off-centre, wrongly
  cropped, or shows an error page / JSON as the wallpaper — this skill contains the diagnosed
  causes. Covers device metrics and safe zones, screenshot-service selection, font embedding
  for headless renderers, and the Shortcuts URL constraints that silently break automations.
---

# iPhone Widget & Lock-Screen Design

You are designing a graphic that will be **rendered by a machine you do not control and
displayed inside a UI you do not control**. The pixels are the easy part. Almost every failure
in this domain comes from the pipeline, not the CSS.

## The one rule that matters

> **Validate the delivery pipeline end-to-end, and look at its actual output, before you design
> anything.**

Concretely: render the page through the real service, download the bytes, assert the pixel
dimensions, and *view the image*. Do this on the first iteration, with a placeholder design,
before spending a single round on typography or colour.

Why this rule exists — a real case:

- A wallpaper was iterated on for five rounds. The user reported it was "blurry",
  "not proportionally centre", and "too unnoticeable". Each round produced CSS changes.
- The actual cause: the screenshot service was returning a **1170×1170 square** which iOS was
  upscaling and cropping to fill a 1170×2532 screen. The CSS was never the problem.
- The check that would have caught it on round one is four lines of shell (see
  `references/render-pipeline.md`). Verifying `HTTP 200` and `content-type: image/png` did
  **not** catch it — those both passed the whole time.

**Never accept a status code and a MIME type as verification of an image.** Assert dimensions.

## Workflow

### Phase 1 — Pin the target (before design)

Establish and write down:

- **Device** → exact pt and px dimensions. `references/device-metrics.md`
- **Surface** → lock screen wallpaper / home screen / a real WidgetKit widget. These have
  completely different constraints.
- **What system UI overlaps it** → clock, date, widget tray, notifications, home indicator.
  This determines the usable canvas, and it is usually far smaller than the screen.
- **Delivery** → how does the image get onto the phone, and how often does it refresh?
- **Render host** → what actually rasterizes the HTML, and what fonts does it have?

### Phase 2 — Prove the pipeline (still before design)

Build a deliberately crude page — a full-bleed coloured box with a corner marker and the text
"TOP LEFT" — and push it through the entire real pipeline. Then verify:

1. Output dimensions match the device exactly.
2. Nothing is cropped: the corner marker is present.
3. The typeface is the one you specified, not a fallback.
4. Set it on the actual device if possible, and check it isn't zoomed.

Only when all four pass do you start designing.

### Phase 3 — Design

`references/visual-rules.md` for type, colour, and hierarchy on OLED black.
Load the `ui-design` skill (its Apple HIG review route) alongside this one when a formal HIG review is wanted.

### Phase 4 — Deliver

`references/shortcuts-delivery.md`. The delivery step has its own failure modes that have
nothing to do with the image being correct.

### Phase 5 — Verify again, then hand over

Re-run the Phase 2 assertions against the finished design. Look at the rendered PNG yourself.
Do not ask the user to be your QA.

## Hard-won rules

1. **Assert dimensions on every render.** Status code and MIME type prove nothing.
2. **Never trust a screenshot API's parameter names.** `crop=2532` did not mean "height 2532".
   Test what a parameter *does*; do not infer it from what it is called.
3. **The render host has no Apple fonts.** `-apple-system` / `SF Pro` silently falls back to
   DejaVu or Liberation on Linux headless Chrome. Embed a webfont.
4. **Give the user exactly one fixed string to paste.** No `&`, no variables to append, no
   trailing slash to lose. Move every bit of complexity server-side.
5. **The preview is not the product.** A desktop browser has different fonts, a different
   aspect ratio, and a different rasterizer than the render host. Verifying in the browser
   verifies nothing about the delivered image.
6. **Reserve the system-UI zone generously**, and show the design *with* mock system UI over
   it. A composition that looks balanced bare will look bottom-heavy under a real clock.
7. **Design at device resolution and let the renderer emulate the device**, rather than
   rendering at an arbitrary width and rescaling. Rescaling is where sharpness dies.
8. **When something breaks, probe variants systematically** rather than guessing. One `curl`
   loop over five candidate paths isolated a 404 instantly after guessing had failed.

## Anti-patterns seen in practice

| Anti-pattern | What it costs |
| --- | --- |
| Iterating on CSS in response to complaints about a broken pipeline | Rounds of work fixing the wrong layer |
| Screenshotting a desktop preview and calling it verified | False confidence; user finds the bug |
| Asking the user aesthetic questions before pipeline questions | Design brief built on constraints you haven't discovered |
| Duplicating the design CSS into a preview page | Two sources of truth; they drift. Use an `<iframe>` of the real page |
| Handing over a URL with 8 `&` parameters to assemble by hand | Two separate user-facing breakages |
| Publishing a new preview artifact per iteration | Clutter; update one instead |

## References

| File | Use it for |
| --- | --- |
| `references/device-metrics.md` | Screen sizes, lock-screen safe zones, widget canvas sizes |
| `references/render-pipeline.md` | Choosing and verifying an HTML→PNG service; fonts; commands |
| `references/shortcuts-delivery.md` | Shortcut + automation patterns, URL constraints |
| `references/visual-rules.md` | Type, colour, and hierarchy for OLED lock screens |
