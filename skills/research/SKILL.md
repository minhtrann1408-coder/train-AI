---
name: research
description: Bundle and router for academic research and paper work in any field, with economics as the core case. Combines the academic-research-skills pack (academic-pipeline, academic-paper, academic-paper-reviewer, deep-research, sr-screener) with r-econometrics. Use when the user types /econ-research, asks for the "econ bundle" or "research bundle", or wants help with any academic paper, research idea, literature review, systematic review, paper revision, reviewer comments, peer review, AI-use disclosure, or econometric analysis in R, and has not named one specific skill.
---

# Econ Research Bundle

This skill only routes. Each task is done by one of the six installed skills below. Pick the matching skill, say in one line which one you chose and why, then load it with the Skill tool and follow it.

If the user's request is empty or unclear, show them the menu below (in their language) and ask which step they are at.

## Menu

| # | User is at this step | Load skill | Typical trigger to pass on |
|---|---|---|---|
| 1 | Has only a topic or vague idea, wants a research question | `deep-research` (socratic mode) | "guide my research on ..." |
| 2 | Needs a literature review or a systematic review | `deep-research` (lit-review or systematic-review mode) | "literature review on ..." |
| 3 | Has database exports or abstracts to screen against criteria | `sr-screener` | "screen these papers" |
| 4 | Has data and needs IV, DiD, RDD or panel regressions in R | `r-econometrics` | describe the design and data |
| 5 | Wants to plan or outline the paper | `academic-paper` (plan mode) | "guide my paper" |
| 6 | Wants a draft, abstract, citation check or format conversion | `academic-paper` (full, abstract-only, citation-check or format-convert mode) | "draft the abstract", "check citations" |
| 7 | Has a draft and wants a simulated peer review | `academic-paper-reviewer` | "review my paper" |
| 8 | Got reviewer comments and must revise or rebut | `academic-paper` (revision-coach or rebuttal-audit) | "I got reviewer comments" |
| 9 | Wants the whole pipeline, idea to finished paper | `academic-pipeline` | "research to paper on ..." |
| 10 | Wants to revise a paper | `academic-paper` (revision) | "revise my paper" |
| 11 | Needs an AI-use disclosure statement | `academic-paper` (disclosure) | "AI disclosure" |
| 12 | Revised a paper and wants it re-reviewed | `academic-paper-reviewer` (re-review) | "re-review my revision" |
| 13 | Wants a screening protocol built | `sr-screener` (protocol) | "build a screening protocol" |
| 14 | Resuming an interrupted pipeline | `academic-pipeline` (resume_from_passport) | "resume my pipeline" |
| 15 | Wants a quick brief, fact-check, WHY-HOW-WHAT scan or full report | `deep-research` (quick, fact-check, three-way-scan or full) | "fact-check ...", "3W scan on ..." |

academic-paper modes: full, outline-only, revision, abstract-only, lit-review, format-convert, citation-check, plan, revision-coach, disclosure, rebuttal-audit.

Literature review owner: a standalone review or annotated bibliography goes to `deep-research` (lit-review). A literature section inside a paper being written goes to `academic-paper` (lit-review).

Name collision: the user also has `anthropic-skills:deep-research` (general web research report). For rows 1 and 2 (and other deep-research rows) load the plain `deep-research` skill from this bundle, not the anthropic one.

## Rules that override the bundled skills

1. **Coursework (graded assignments):** the user's CLAUDE.md wins. Use base R and `lm()`, kable tables, inline R numbers, no `fixest` or tidyverse unless the user asks. The main research question is the user's to decide; do not invent it.
2. `r-econometrics` uses the `fixest` package, which is not installed. Ask before installing it (console only, never inside an .Rmd).
3. Data and outputs for a course go to the working folder the user names. The rest of the course folder is read-only.
4. Every citation must be a real source the skill has verified. Never fill in references from memory.
5. No em dashes in English prose.

## Known gaps

The `shared/` folder these skills cite (`shared/references/routing_core.md`, `intent_clarification_protocol.md`, contracts, etc.) and some scripts (`academic-paper/scripts/check_acronyms.py`, `academic-pipeline/scripts/run_codex_audit.sh`) are missing. When a skill points to a missing file, keep following that skill's own SKILL.md and say once that the file is missing.
