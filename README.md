# train-AI

A collection of Claude skills for study, research and everyday work. Skills only: no personal data, settings or credentials.

## Layout
- `skills/`: general skills (research, academic writing, econometrics, design, video, study guides, PDF reading, writing clean-up, prompt templates).
- `skills-anthropic/`: copies of Anthropic's Apache-2.0 skills (`docx`, `pdf`, `pptx`, `xlsx`, `skill-creator`), each with its `LICENSE.txt`.

Each skill is a folder with a `SKILL.md` (name, description, instructions) and optional `references/`, `templates/`, `scripts/`.

## Use
- **Claude Code:** copy the skill folders you need into `~/.claude/skills/`.
  ```powershell
  git clone <repo-url> "$HOME\train-AI"
  Copy-Item "$HOME\train-AI\skills\*" "$HOME\.claude\skills\" -Recurse -Force
  ```
- **claude.ai:** upload a skill folder as a custom skill, or ask Claude to read the repo and follow the matching `SKILL.md`.

## Skills
| Skill | What it does |
|---|---|
| `skills/academic-paper` | 12-agent academic paper writing pipeline. |
| `skills/academic-paper-reviewer` | Multi-perspective academic paper review with dynamic reviewer personas. |
| `skills/academic-pipeline` | Orchestrator for the full academic research pipeline: research -> write -> integrity check -> review -> revise -> re-review -> re-revise -> final integrity check -> finalize. |
| `skills/content-marketing` | Content planning, social performance analysis, and brand writing guides. |
| `skills/deep-research` | Universal deep research agent team. |
| `skills/exam-study-guide` | Use when the user uploads lecture slides, question banks or past exams and wants an interactive HTML study guide with MCQ practice, written questions and a random mock-exam generat |
| `skills/find-skills` | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending c |
| `skills/humanizer` | Rewrite AI-sounding text so it reads like the writer without changing what it says. |
| `skills/iphone-widget-design` | Design and ship iPhone lock-screen wallpapers, widget-style graphics, and auto-updating phone visuals built from HTML/CSS and delivered through iOS Shortcuts. |
| `skills/opus-lead` | Run multi-step work with the main Opus session as lead and quality checker, delegating searches and trivial edits to Haiku and drafting or implementation to Sonnet, then checking e |
| `skills/ponytail` | Lazy senior dev mode: the smallest change that fully solves the task, and a reply a busy human understands in one read. |
| `skills/ponytail-audit` | Quality audit of a whole repo: bugs, security holes, what breaks under real load, risky code without tests, slow paths, and what to delete, merge or split. |
| `skills/ponytail-debt` | List every `shortcut:` comment (and older `ponytail:` ones) as a debt ledger. |
| `skills/ponytail-gain` | Show ponytail's measured savings (code, cost, speed) from the benchmark. |
| `skills/ponytail-help` | Quick reference for ponytail levels, skills and commands. |
| `skills/ponytail-review` | Quality review of a change: is the logic right, is it safe, does it hold under real load, is risky code tested, is it fast enough, and is every line needed. |
| `skills/prompt-kit` | the user's prompt templates (goal, deeper, outline, spread, challenge, openings, finish, handoff, restart, check-dates, check-deck, check-sheet, memory). |
| `skills/r-econometrics` | Run IV, DiD, and RDD analyses in R with proper diagnostics |
| `skills/read-pdfs` | Read, search, summarize, quote and extract tables from existing PDFs token-efficiently: convert once to Markdown with page-anchored figure placeholders, then render only the pages  |
| `skills/research` | Bundle and router for academic research and paper work in any field, with economics as the core case. |
| `skills/savvy-flow` | Run multi-step work with the main Opus session as lead and quality checker, delegating to tiered savvy workers (savvy-light on Haiku for searches and trivial edits, savvy-medium /  |
| `skills/sr-screener` | Protocol-driven study screening for systematic, scoping and rapid reviews. |
| `skills/ui-design` | The one design skill for the user. |
| `skills/video` | The one video skill for the user. |
| `skills/web-intake` | Get content from the internet and break it down. |
| `skills-anthropic/docx` | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx) or Word templates (.dotx). |
| `skills-anthropic/pdf` | Use this skill whenever the user wants to do anything with PDF files. |
| `skills-anthropic/pptx` | Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. |
| `skills-anthropic/skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. |
| `skills-anthropic/xlsx` | Use this skill any time a spreadsheet file is the primary input or output. |
