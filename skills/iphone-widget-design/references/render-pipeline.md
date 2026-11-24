# HTML → PNG Render Pipeline

The page is rasterized by a headless browser on someone else's server. Three things go wrong
there, and none of them are visible from a status code.

## 1. Aspect ratio — verify, never assume

**Test what a parameter does. Do not infer it from its name.**

Measured results for the same page (target: 1170×2532 portrait):

| Service + params | Actual output |
| --- | --- |
| `thum.io` `width/1170/crop/2532` | **1170×1170** — square |
| `thum.io` `width/1755/crop/3798` | **1755×1755** — square |
| `thum.io` `width/1170/fullpage` | 1170×865 |
| `thum.io` `viewportWidth/1170/width/1170` | 1170×1200 |
| `thum.io` `crop/2532/width/1170` | 1170×1170 |
| **`microlink`** `viewport.width=390&viewport.height=844&viewport.deviceScaleFactor=3` | **1170×2532** ✅ |
| `microlink` `viewport.width=1170&viewport.height=2532` | 2340×5064 (default dSF=2) |

**`thum.io` cannot produce a portrait image.** `crop/{n}` does not set height. Every
combination returns a square or its own viewport. If a square is handed to iOS as a wallpaper,
iOS upscales and centre-crops it to fill the screen — which destroys sharpness *and* shifts the
composition. This presents to the user as "blurry" and "not centred", and it will send you
chasing CSS bugs that do not exist.

### Recommended service

```
https://api.microlink.io/?url=<ENCODED_PAGE_URL>
  &screenshot=true
  &meta=false
  &embed=screenshot.url
  &viewport.width=390
  &viewport.height=844
  &viewport.deviceScaleFactor=3
  &screenshot.type=png
```

- `embed=screenshot.url` makes it return the **image** instead of a JSON envelope. Without it
  you get JSON — see the failure mode in `shortcuts-delivery.md`.
- `deviceScaleFactor=3` is what makes it sharp: the page lays out at 390 pt and rasterizes at
  ×3, exactly like the real device.
- Free tier is rate-limited per IP. Fine for once-daily. Have the *phone* fetch it directly
  (via a redirect) rather than proxying through a serverless function on shared egress IPs.
- `&force=true` bypasses its render cache.

### Caching

The service caches by full URL. If the page content changes daily, the URL must change daily
or you will serve yesterday's image forever. Put the date in the URL. Note that this also
means **you will see your own stale renders while developing** — use the force parameter when
testing a change.

## 2. Fonts — the render host has no Apple fonts

`-apple-system`, `SF Pro Display`, `SF Pro Text`, `system-ui` all resolve to **DejaVu Sans or
Liberation Sans** on Linux headless Chrome. The render silently uses a face you never chose,
which looks unrefined and often thinner than intended.

**Always embed a webfont.** Google Fonts is reliable from render hosts:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
```

`Inter` is the closest widely-available match to SF Pro's proportions and works well at both
display and caption sizes. Keep the Apple faces in the stack after it so the page still looks
right when opened on the phone itself:

```css
--font: "Inter", -apple-system, "SF Pro Display", system-ui, sans-serif;
```

Use `display=swap` plus a render wait (2–3 s) so the screenshot is not taken mid-swap.
Never use `display=block` with a wait — you can capture invisible text.

## 3. Resolution-independent layout

Design in container-query units against a single sized container, so one stylesheet renders
correctly at any scale:

```css
.frame{
  width: min(100vw, calc(100vh * 1170 / 2532));
  height: min(100vh, calc(100vw * 2532 / 1170));
  container-type: size;
}
/* everything inside uses cqw / cqh */
```

This letterboxes gracefully on a desktop preview and fills exactly at the device aspect ratio,
with no magic numbers to update per device.

## Verification commands

Run these on **every** render, not just the first.

```bash
# Download and assert real pixel dimensions from the PNG header
curl -sS -L -o out.png "<RENDER_URL>"
node -e "const b=require('fs').readFileSync('out.png');
  console.log(b.slice(1,4).toString()==='PNG'
    ? 'PNG '+b.readUInt32BE(16)+'x'+b.readUInt32BE(20)+' '+b.length+' bytes'
    : 'NOT AN IMAGE: '+b.slice(0,200).toString())"
```

The `NOT AN IMAGE` branch matters — it prints the body, which is how you discover you are
getting a JSON envelope or an HTML error page instead of a picture.

Then **look at the file**. Read the PNG and view it. Dimensions being right does not mean the
content is right — a cached render of a previous version has the correct dimensions too.

### Probing an unknown API

When a service's behaviour is unclear, enumerate variants in one pass instead of guessing:

```bash
for spec in "a/1" "b/2" "c/3"; do
  curl -sS -o "p.png" "https://service/$spec/https://example.com"
  node -e "const b=require('fs').readFileSync('p.png');
    console.log('$spec ->', b.readUInt32BE(16)+'x'+b.readUInt32BE(20))"
done
```

This turns an afternoon of guessing into one tool call.

## Fully private alternative

Any hosted screenshot service sees the page URL and its contents. If that matters, render
locally on a schedule with Playwright and sync the PNG to a Photos album the automation reads:

```js
const ctx = await browser.newContext({
  viewport: { width: 390, height: 844 },
  deviceScaleFactor: 3,
});
await page.goto(url, { waitUntil: 'networkidle' });
await page.screenshot({ path: 'wallpaper.png' });
```
