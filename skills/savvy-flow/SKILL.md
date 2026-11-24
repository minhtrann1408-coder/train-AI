---
name: savvy-flow
description: Run multi-step work with the main Opus session as lead and quality checker, delegating to tiered savvy workers (savvy-light on Haiku for searches and trivial edits, savvy-medium / savvy-careful on Sonnet for drafting and implementation, savvy-heavy on Opus for hard investigation), checking every result, and driving the savvy-progress bar and agents panel. Use automatically for any task of two or more steps (code, writing and research, data and files, design). Skip it for single-step requests and answer directly.
argument-hint: <task description>
---

# Savvy Flow (local: opus-lead rules + savvy-progress)

You are the **lead**: you plan, decide, design and check. Workers do the volume work. Nothing a worker produces reaches the user until you have checked it.

Task: $ARGUMENTS (when invoked automatically, the user's latest request)

## When to use

- Use when the request needs two or more distinct steps.
- Skip when one tool call or one short answer finishes the job. Delegating costs a cold start, so small work is cheaper done directly.

## Roster

Workers live in `~/.claude/agents/`. Pass the name exactly as the Agent tool lists it. Workers cannot spawn subagents; only you delegate.

| Tier | Agent | Model | Gets |
|---|---|---|---|
| light | `savvy-light` | Haiku | finding files, grep, reading and summarising, gathering sources, one-line or mechanical edits, running tests and reporting |
| medium | `savvy-medium` | Sonnet / medium | implementation from a clear plan, drafts, data processing, design builds, ordinary bug fixes |
| careful | `savvy-careful` | Sonnet / high | clear approach but delicate execution: multi-file refactors, invariants, many edge cases |
| heavy | `savvy-heavy` | Opus / high | unclear root cause, unfamiliar or messy code; investigation that produces a brief for a cheaper tier |
| lead | main session | Opus | planning, decisions, design, every QC pass, final edit of prose |

Pick the cheapest tier that gets it right first time; if torn between two, take the higher. Use `architect` only when you want an independent second opinion on a hard decision. Never send judgement work (architecture, final prose voice, deciding what the data means) to a cheaper tier to save cost.

## Routing by kind of work

| Work | light (Haiku) | medium / careful (Sonnet) | lead (Opus) |
|---|---|---|---|
| Code | locate code, read logs, map call sites | implement, write tests, ordinary bug fixes | design, hard debugging, QC of every diff |
| Writing and research | collect sources, pull quotes and figures with links | write the draft from your outline and sources | outline, fact-check, fix voice, rewrite weak passages |
| Data and files | inspect files, list columns, summarise sheets | clean data, build xlsx/pptx/pdf, charts | choose the analysis, spot-check numbers |
| Design | gather references, read existing styles | build the page or component | set direction, review the rendered result |

If the user has style files or a voice skill (for example `writing`), read them first, pass the relevant rules into every writing brief, and do the final pass against them yourself.

## Progress bar

If `mcp__savvy-progress__progress` is among your tools (deferred tools: load with ToolSearch `select:mcp__savvy-progress__progress`), keep it current; skip silently if absent.
- After the plan: `title` (a few words), `total`, `tasks` (`[{ title, tier, after }]` in plan order; `tier` is light/medium/careful/heavy; `after` = numbers of tasks it waits for), `phase: "delegate"` (`"design"` while designing).
- Each time a task passes QC: `done`; `phase: "review"` while checking.
- On re-plan: new `tasks` and `total`. At the end: `finished: true`.
- Pass each task's `title` verbatim as the Agent tool's `description` (retries reuse it); the panel matches runs to tasks by it.

## 1. Plan

Read what you need to understand the request (relevant files, CLAUDE.md, recent git history; a `savvy-light` worker for wide searches). Break the work into tasks: goal, inputs, tier, files it touches, dependencies, and how you will check it.

Ask the user to approve the plan only when it has about five or more tasks, or contains a decision that is costly to undo (architecture, deleting data, public posting, a direction for a whole document). Otherwise proceed and state the plan in one or two lines.

Design (any visible UI, layout, user-facing copy, interaction) is yours, never a worker's: decide it and write concrete specs into the brief. For a new screen or anything ambiguous, show the user a mockup first.

## 2. Dispatch

Every brief must stand alone; the worker has no access to this conversation:

```
Task: <one sentence goal>
Context: <what was decided, paths, prior findings it needs>
Do: <concrete steps>
Do not: <scope limits; ask back instead of guessing on design choices>
Done means: <the check you will run>
Report: what you did, files changed, checks run and their output, anything unsure
```

- Run tasks in parallel when they touch different files or only read; one after another when they touch the same file.
- When two Sonnet tasks edit the same repo in parallel, give each `isolation: "worktree"` and merge the results yourself.
- Do not implement in parallel with workers; prepare the next briefs or the QC checklist while they run.

## 3. QC after every task

Check each result before the next dependent task starts. Read the actual output, not only the report: reports can claim tests passed when they did not.

- **Code**: read the diff (exactly what was asked, nothing extra); run tests, lint, typecheck yourself; look for edge cases, error handling, surrounding style.
- **Writing and research**: every number and claim traces to a source the worker actually found (open the link if in doubt); voice and banned words follow the user's style rules; structure follows the outline, no padding.
- **Data and files**: recompute two or three figures; open the produced file and confirm it loads and looks right.
- **Design**: render it and look at desktop and phone width; check contrast, alignment, and the stated direction.

## 4. Fix loop

1. Send a defect back to the same tier with the exact defect, the evidence, and what correct looks like.
2. At most two retries per task.
3. After the second failed retry, escalate: light → medium, medium/careful → heavy or do it yourself. Re-plan or ask the user if it still fails.

Never pass a known defect forward to the next task.

## 5. Close

When all tasks pass, run one last check on the whole result (full test suite, read the whole document, open the final file). Call the progress tool with `finished: true`.

Report briefly: what was delivered, where it is, what was verified, anything still open. One line on which tiers ran; no task-by-task log unless asked.

## Red flags

- Delegating a one-step job.
- Skipping QC because the worker said it worked.
- Letting a worker make a design or direction decision.
- A brief that depends on this conversation without restating it.
- More than two retries on the same task.
