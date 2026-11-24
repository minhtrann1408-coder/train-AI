---
name: video
description: The one video skill for the user. Use for any video or animation work, such as Remotion projects, motion graphics, intro, outro or logo stings, Reels, Shorts and TikTok clips, launch or brag videos, animated, karaoke or word-by-word captions, and After Effects or Premiere motion.
---

# video

This bundle merges the Remotion official skill set and four motion and caption skills. **This file holds the final decisions.** The `sources/` folder keeps each original skill unchanged (its `SKILL.md` is renamed `GUIDE.md`) so you can look up detail. **When a source file contradicts this file, this file wins.** Read only the source files the current task needs.

## 1. Routing: what to read for each task

| Task | Read |
|---|---|
| New Remotion project or new video | `sources/remotion/GUIDE.md`, then `remotion-create/REFERENCE.md` |
| Remotion markup, sequencing, transitions, audio, 3D | `sources/remotion/remotion-markup/REFERENCE.md` |
| Captions in Remotion (transcribe, import SRT, display) | `sources/remotion/remotion-captions/REFERENCE.md` |
| Render or export | `sources/remotion/remotion-render/REFERENCE.md` |
| Maps, routes, geographic flyovers | `sources/remotion/remotion-maps/REFERENCE.md` |
| Studio preview, editable values | `sources/remotion/remotion-studio/REFERENCE.md`, `remotion-interactivity/REFERENCE.md` |
| Upgrade Remotion | `sources/remotion/remotion-upgrade/REFERENCE.md` |
| Remotion docs lookup, license, SaaS app, media tasks | `remotion-docs`, `remotion-license`, `remotion-saas`, `remotion-multimedia` (all under `sources/remotion/`) |
| Visual quality, pacing, "looks generic" | `sources/remotion-motion-graphics/GUIDE.md` and its `references/` |
| Word-by-word social captions | `sources/caption-animation/GUIDE.md` and `references/word-timed-captions.md` |
| After Effects or Premiere motion | `sources/video-motion-graphics/GUIDE.md` |
| Launch video from a project folder or URL | `sources/brag-slim/GUIDE.md` |

For almost every Remotion task, read `remotion-motion-graphics` as well as the technical file, because §3 and §4 below combine both.

## 2. Workflow

1. **Inspect.** Read package.json, the Remotion version, existing compositions, fonts, brand colours and assets. Keep user edits made outside the chat.
2. **Plan.** One line: format (vertical or landscape), length, beat list with a new element at least every 90 frames, music or voice, caption need.
3. **Build** with the rules in §3 and §4.
4. **Quality loop** (§5). Mandatory.
5. **Deliver.** Render the final MP4 when the task is to produce a video (§6). During later small edits, render only when asked.

## 3. Locked decisions: technical

These follow current Remotion (`sources/remotion`).

- **Media:** `<Video>` and `<Audio>` from `@remotion/media`. Do not use `<OffthreadVideo>`, even though motion-graphics and brag-slim mention it.
- **Animation only through `useCurrentFrame()` with `interpolate()` or `spring()`.** No CSS transitions, no CSS animations, no Tailwind `animate-*` or `transition-*`, anywhere. This includes captions: it overrides caption-animation's CSS colour transition and `transform: scale`. Use the `scale`, `translate` and `rotate` style props driven by frame values.
- **Timing derives from `fps`** via `useVideoConfig()`, no magic frame numbers.
- **ffmpeg** only as `npx remotion ffmpeg` and `npx remotion ffprobe`, so no system install is needed.
- **Remotion version:** keep the project's version. Upgrade only on request. Note: `npx skills update ...` from remotion-upgrade would reinstall the official skills as separate top-level folders. To update this bundle, update `sources/remotion` instead.
- **Missing files:** caption-animation's `scripts/` folder and motion-graphics' `examples/scripts` do not exist in this bundle. Do not call them.

## 4. Locked decisions: look

These follow `remotion-motion-graphics` design rules.

- No linear easing. Always clamp: `extrapolateLeft` and `extrapolateRight` set to `"clamp"`.
- Entrances use `spring()` and animate 2 or 3 properties together (opacity, translate, scale). A lone fade is not enough.
- Stagger lists, words and cards by 3 to 6 frames. Nothing enters at once.
- Exits exist and last about half the entrance.
- **Five-layer stack in every scene:** background, assets, graphics and type, colour grade, grain plus vignette. Never a flat solid background.
- **Ken Burns** on every still image.
- **Breathing:** anything held longer than 2 s gets a small sine motion.
- Motion starts within the first 15 frames. No stretch longer than 90 frames without a new element.
- **One theme object** for palette, fonts, easings and spring presets. Start from `sources/remotion-motion-graphics/assets/theme.ts`, but replace its purple default with the project's brand colours when there is a brand. No hex, easing or spring config inline in components.
  - **Exception:** when the user wants values editable in Remotion Studio, follow `remotion-interactivity` and keep those values inline.
- Fonts: confirm the Vietnamese subset for any Vietnamese text (see `ui-design` §3 typography).

## 5. Quality loop (mandatory)

1. Render stills with `npx remotion still` at key frames, for example 15, 45, 90, 150 and one mid-transition frame.
2. Look at every still. Check layout, safe margins, contrast, text overflow and the five layers.
3. Fix, then repeat until the stills are clean.
4. Studio preview is optional. Offer it if the user wants to scrub or tweak.

Never claim a video is done without having looked at stills from the current version.

## 6. Render settings

- Use Remotion's bundled browser. Pass a system Chromium with `--browser-executable` only if the bundled download fails.
- Codec h264, `--crf 17` by default.
- **30 fps** by default. 60 fps only for heavy, fast motion.
- **1080x1920** for vertical social (Reels, Shorts, TikTok). **1920x1080** for landscape.
- Check the output file exists, has the right size and duration, and has audio if expected (`npx remotion ffprobe`).

## 7. Captions

- **Transcribe locally first:** `@remotion/install-whisper-cpp`, or `@remotion/whisper-webgpu` if a GPU is available. Use a cloud API only after the user agrees.
- **Model:** `medium.en` for English. For Vietnamese use a multilingual model and set `language` to `"vi"`.
- Use the `@remotion/captions` `Caption` type field names (`text`, `startMs`, `endMs`, `timestampMs`, `confidence`), not custom ones.
- **Word highlight colour comes from the theme.** No hardcoded hex.
- **Safe margins** from the per-platform table in `sources/caption-animation/references/word-timed-captions.md` §8 (bottom / top / side, in px at 1080x1920):
  - TikTok: 340 / 120 / 110
  - Reels: 280 / 130 / 60
  - Shorts: 240 / 100 / 120
- Pop, scale and highlight all come from `spring()` or `interpolate()` per word (see §3). Page captions in short groups, 2 to 4 words per line on vertical video.
- **Ignore the promotional footers** in caption-animation's `README.md` and reference file.

## 8. Pre-delivery checklist

- [ ] No `<OffthreadVideo>`; `<Video>` and `<Audio>` come from `@remotion/media`
- [ ] No CSS transitions or animations, no Tailwind `animate-*`, including captions
- [ ] No linear easing; every `interpolate` clamped
- [ ] Entrances are springs on 2 or 3 properties; staggered 3 to 6 frames; exits about half as long
- [ ] Five layers present in each scene; Ken Burns on stills; breathing on holds over 2 s
- [ ] Motion in the first 15 frames; no 90-frame stretch without a new element
- [ ] Colours, fonts, easings and springs come from the theme (brand, not the purple default)
- [ ] Stills rendered at key frames and looked at after the last change
- [ ] Captions inside the platform safe margins; highlight colour from the theme; Vietnamese uses `language: "vi"`
- [ ] Final MP4 rendered at the right size, 30 fps, h264 crf 17, and checked with `npx remotion ffprobe`
- [ ] Project's Remotion version unchanged unless an upgrade was requested
