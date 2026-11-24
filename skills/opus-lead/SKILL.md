---
name: opus-lead
description: Run multi-step work with the main Opus session as lead and quality checker, delegating searches and trivial edits to Haiku and drafting or implementation to Sonnet, then checking every result before moving on. Use automatically for any task of two or more steps (code, writing and research, data and files, design). Skip it for single-step requests and answer directly.
disable-model-invocation: true
---

# Opus Lead

The main session (Opus) plans, delegates, checks, and decides. Haiku and Sonnet do the volume work. Nothing a subagent produces reaches the user until Opus has checked it.

## When to use

- Use when the request needs two or more distinct steps.
- Skip when one tool call or one short answer finishes the job. Delegating costs a cold start, so small work is cheaper done directly.

## Roster

Prefer the named agents from claude-config when they exist (`~/.claude/agents/`). Otherwise call the general-purpose agent with the `model` parameter.

| Role | Agent | Fallback | Gets |
|---|---|---|---|
| Lead and QC | main session (Opus) | none | planning, decisions, judgement calls, every QC pass, final edit of prose |
| Worker | `builder` | general-purpose, `model: sonnet` | implementation from a clear plan, drafts, data processing, design builds |
| Scout | `scout` | general-purpose, `model: haiku` | finding files, grep, reading and summarising, gathering sources, one-line edits |
| Second opinion | `architect` | general-purpose, `model: opus` | only when Opus wants an independent look at a hard decision |

Subagents cannot spawn subagents. Only the main session delegates.

## Routing by kind of work

| Work | Haiku (`scout`) | Sonnet (`builder`) | Opus (lead) |
|---|---|---|---|
| Code | locate code, read logs, map call sites | implement, write tests, ordinary bug fixes | design, hard debugging, QC of every diff |
| Writing and research | collect sources, pull quotes and figures with links | write the draft from Opus's outline and the sources | outline, fact-check, fix voice, rewrite weak passages |
| Data and files | inspect files, list columns, summarise sheets | clean data, build xlsx/pptx/pdf, charts | choose the analysis, spot-check numbers |
| Design | gather references, read the existing styles | build the page or component | set direction, review the rendered result |

If the user has style files (for example `ABOUT ME/` with an anti-AI writing guide, or a voice skill such as `vn-punchy-voice`), Opus reads them first and passes the relevant rules into every writing brief. Opus does the final pass against them itself.

## Process

### 1. Plan

Break the request into tasks. For each task write: goal, inputs, owner (Haiku or Sonnet), files it touches, and how Opus will check it.

Ask the user to approve the plan only when it has about five or more tasks, or contains a decision that is costly to undo (architecture, deleting data, public posting, a direction for a whole document). Otherwise proceed and state the plan in one or two lines.

### 2. Dispatch

Every brief must stand alone, because the subagent starts with no context:

```
Task: <one sentence goal>
Context: <what was decided, paths, prior findings it needs>
Do: <concrete steps>
Do not: <scope limits; ask back instead of guessing on design choices>
Done means: <the check Opus will run>
Report: what you did, files changed, checks you ran and their output, anything unsure
```

Parallel or sequential:
- Run tasks in parallel when they touch different files or only read.
- Run tasks that touch the same file one after another.
- When two Sonnet tasks edit the same repo in parallel, give each `isolation: "worktree"` and merge the results yourself.

### 3. QC after every task

Opus checks each result before the next dependent task starts. Read the actual output, not only the subagent's report. Reports can claim tests passed when they did not.

Code
- Read the diff. Does it do exactly what the task asked, nothing extra?
- Run the tests, lint, and typecheck yourself. Paste failures into the retry brief.
- Look for the usual misses: edge cases, error handling, style of the surrounding code.

Writing and research
- Every number and claim traces to a source the scout actually found. Open the link if in doubt.
- Voice and banned words follow the user's style rules.
- Structure follows the outline; no padding or repetition.

Data and files
- Recompute two or three figures by hand or with a quick script.
- Open the produced file and confirm it loads and looks right.

Design
- Render it (Playwright screenshot or the artifact preview) and look at it at desktop and phone width.
- Check contrast, alignment, and that it matches the stated direction.

### 4. Fix loop

When QC finds a defect:
1. Send it back to the same kind of agent with the exact defect, the evidence, and what correct looks like.
2. At most two retries per task.
3. After the second failed retry, escalate: a Haiku task moves to Sonnet; a Sonnet task Opus does itself.

Never pass a known defect forward to the next task.

### 5. Final check and report

When all tasks pass, run one last check on the whole result (full test suite, read the whole document, open the final file).

Report to the user briefly: what was delivered, where it is, and anything still open or uncertain. No task-by-task log unless asked.

## Red flags

- Delegating a one-step job.
- Skipping QC because the subagent said it worked.
- Letting Sonnet make a design or direction decision. It should report back instead.
- Giving a subagent a brief that depends on this conversation without restating it.
- More than two retries on the same task.
- Sending Opus-level judgement work (architecture, final prose voice, deciding what the data means) to a cheaper model to save cost.
