---
name: content-marketing
description: Content planning, social performance analysis, and brand writing guides. Use when the user wants to plan content, pick topics or what to write about, build topic clusters, an editorial calendar or content roadmap, or asks why posts bring no customers (lên kế hoạch nội dung, lịch đăng bài, chủ đề viết gì, content calendar). Also use to analyze how social posts are performing, "analytics", "performance", "how did my posts do", "engagement", "impressions", "what's working", "post metrics", "my best posts", "why isn't this post performing" (bài đăng hiệu quả thế nào, phân tích bài). Also use to build or port a brand tone of voice guide (TONE.md, brand voice, voice attributes, channel tone) or a prose/writing style guide (PROSE.md, house style, ghostwriter style, banned words, sentence-length targets, multi-writer consistency).
---

# content-marketing

This bundle merges four content skills. **This file holds the final decisions.** The `sources/` folder keeps each original unchanged except that `SKILL.md` was renamed `GUIDE.md`. **When a source file contradicts this file, this file wins.** Read only the source files the task needs.

## 1. Routing

| Task | Read |
|---|---|
| What to write or plan, topic clusters, editorial calendar, content roadmap, why content brings no customers | `sources/content-strategy/GUIDE.md` (and its `references/` as needed) |
| How posts performed, metrics, best posts, why a post underperformed | `sources/performance-analyzer-sms/GUIDE.md` |
| Build or port a TONE.md (brand tone of voice) | `sources/copywriting-tone-of-voice-creator/GUIDE.md` (plus `references/`, `assets/`) |
| Build or port a PROSE.md (writing style guide) | `sources/copywriting-prose-creator/GUIDE.md` (plus `references/`) |
| Writing the actual posts, emails or pages | Not in this bundle. Write them in the user's own voice. |

If a task spans two rows (for example a calendar plus a TONE.md), do them in order: strategy first, then the guide.

## 2. Final decisions

### Whose voice wins
- **For the user's own content, their own voice guide (if they have one) wins over every copywriting default** in these sources. That covers the em dash, restated-stake closings, no-question social closes, banned-word lists, and any "voice" or "tone" rule inside the content-strategy, tone and prose guides.
- Copywriting defaults apply **only when building a guide for another brand** (a client, a company, a different person). In that case follow the source guide, and do not impose the user's voice on it.
- If you are unsure whose brand it is, ask once.

### Sibling skills that are not installed
The source files name many sibling skills. These are **not installed**, so do not try to load them: copywriting, seo-audit, social, emails, launch, link-building, ai-seo, programmatic-seo, site-architecture, free-tools, product-marketing context, social-media-context-sms, audience-growth-tracker-sms, content-pattern-analyzer-sms, optimization-advisor-sms, post-writer-sms, `samber/cc-skills@*`, SOUL.md, DESIGN.md.
- When a source says "see X" for one of these, do the work inline using what you know, or say in one line that it is out of scope. Do not stall or invent a tool call.
- If a guide asks to read a product-marketing context file or SOUL.md and none exists, ask the user for the few facts you need (audience, offer, goal) instead of stopping.

### Performance analysis
- **Always end with 3 to 5 prioritized actions** (most valuable first, each tied to a finding in the data). The "Boundaries" section of `performance-analyzer-sms` says it does not generate an action plan. That line is **overruled**.
- Use BlackTwist analytics only if that connector is available. Otherwise work from data the user pastes, and say which numbers you lack.
- Do not invent metrics. Mark small samples as weak evidence.

### Output language
Reply in the user's language (Vietnamese in, Vietnamese out). Keep file names such as TONE.md and PROSE.md in English. Write any guide in the language the target brand's audience reads, unless told otherwise.

### Working files
Write drafts and exports to the session scratchpad or a folder the user names, not into unrelated project folders.
