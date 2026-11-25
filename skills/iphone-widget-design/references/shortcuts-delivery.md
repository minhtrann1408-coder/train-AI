# Delivery via iOS Shortcuts

The image can be perfect and still arrive broken. The Shortcuts app is a constrained text
editor being used to assemble a URL, and it fails in ways that are invisible until the
wallpaper is already on the screen.

## The governing rule

> **Hand the user exactly one fixed string to paste. Nothing to append, nothing to assemble.**

Every piece of variability you push into the Shortcut is a failure mode. Push it server-side.

## Two real failures, both from asking the user to build a URL

### Failure 1 — `&` gets absorbed

Instruction given: paste part A, insert a date variable, paste part B, where part B began with
`&screenshot=true&meta=false&...`.

What arrived at the API: `url=https://site/?date=2026-09-08&screenshot=true&meta=false&...`
— **the entire tail became the value of `url=`**. Every other parameter was lost.

Result: the API returned its default **JSON metadata envelope**, and Set Wallpaper rendered
that JSON as a wall of black text on a white lock screen.

**Symptom to recognise:** the wallpaper is white with fragments of JSON
(`"data":{"author":null,"lang":"en","title":...`).

### Failure 2 — the trailing slash disappears

Instruction given: paste `https://site.app/shot/` then append the date variable.

What arrived: `https://site.app/shot2026-09-08` — the trailing `/` was lost, gluing the date
onto the path segment. The route did not match, the host returned its 404 page, and Set
Wallpaper painted **the 404 page** onto the lock screen.

**Symptom to recognise:** the wallpaper is a white page reading "…could not be found" with a
hex request ID.

### The fix for both

Put a route on your own server that takes no parameters:

```js
// GET /shot  ->  302 to the full render URL
const SITE = 'https://your-site.vercel.app/';
const DEFAULT_TZ = 'UTC';                      // the user's zone, not the server's

function todayIn(tz) {                        // en-CA formats as YYYY-MM-DD
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit',
  }).format(new Date());
}

export default function handler(req, res) {
  const raw = req.query.date;
  let date = typeof raw === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(raw) ? raw : null;
  if (!date) {
    const tz = req.query.tz || DEFAULT_TZ;
    try { date = todayIn(tz); } catch { date = todayIn('UTC'); }
  }
  const target = `${SITE}?date=${date}`;
  const api = 'https://api.microlink.io/?url=' + encodeURIComponent(target)
    + '&screenshot=true&meta=false&embed=screenshot.url'
    + '&viewport.width=390&viewport.height=844&viewport.deviceScaleFactor=3'
    + '&screenshot.type=png'
    + (req.query.force !== undefined ? '&force=true' : '');
  res.setHeader('Cache-Control', 'no-store');
  res.redirect(302, api);                     // phone fetches the image on its own IP
}
```

The user's whole instruction becomes one line: `https://your-site.vercel.app/shot`

**Redirect rather than proxy.** A 302 means the phone downloads from the render service using
its own IP and its own rate-limit budget; proxying the bytes routes them through your host's
shared egress addresses, which get throttled.

**Be tolerant of the glued form** so an already-built shortcut keeps working:

```json
{
  "rewrites": [
    { "source": "/shot/:date", "destination": "/api/shot?date=:date" },
    { "source": "/shot:date(\\d{4}-\\d{2}-\\d{2})", "destination": "/api/shot?date=:date" },
    { "source": "/shot", "destination": "/api/shot" }
  ]
}
```

## The Shortcut

Two actions:

1. **Get Contents of URL** → `https://your-site.vercel.app/shot`
2. **Set Wallpaper** → *Lock Screen*, expand and turn **Show Preview** off

## The automation

Shortcuts → **Automation** tab → **+** → **Create Personal Automation** → **Time of Day** →
pick a time, **Daily** → **Next** → **Add Action** → **Run Shortcut** → pick it → **Next** →
**Run Immediately** on, **Notify When Run** off → **Done**.

`Run Immediately` requires iOS 16.4+ to work while the phone is locked.

## Time zones

Resolve the date on the server in the **user's** zone. A render server on UTC computing "today"
at 06:00 in UTC+7 returns the *previous* day, so the countdown is silently off by one. Ask for
the user's zone, or read it from the phone's date and hardcode it.

## Checklist before handing over

- [ ] The URL has no `&`
- [ ] The URL has no query string at all, if avoidable
- [ ] Nothing has to be appended to it
- [ ] It has been fetched with `curl -L` and produced a PNG of the exact device dimensions
- [ ] The PNG has been **looked at**, not just measured
- [ ] Malformed neighbours (`/shot/`, `/shotXXXX`, `/shot?x=1`) have been probed and do not 404
- [ ] The date it resolves to matches the user's local date, not the server's
