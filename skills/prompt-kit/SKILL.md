---
name: prompt-kit
description: the user's prompt templates (goal, deeper, outline, spread, challenge, openings, finish, handoff, restart, check-dates, check-deck, check-sheet, memory). Use when the user types /prompt-kit or names a template. Also apply it unasked when the user asks for a verdict or a vague improvement on writing, ideas, names, designs or decisions, such as "cái nào tốt hơn", "which is better", "cái này ổn không", "is this good", "làm hay hơn đi", "make it better", "đặt tên cho", "nghĩ vài ý tưởng". Not for code fixes or bug reports.
---

# prompt-kit

## How to run

- **Invoked:** `/prompt-kit <template>: <task>`. With no template, show the template list as one line per template and ask which one.
- **Run mode (default):** apply the template to the task yourself and give the result.
- **Write mode:** if the user says "chỉ viết prompt", "just the prompt" or "prompt only", output only the filled template in a code block, ready to paste into another chat. Fill every bracket you can from context, and leave `[…]` only where you truly lack the information.
- **Auto mode:** in the situations the description lists, switch to the matching template without asking. Start your reply with one line saying which one, e.g. `(prompt-kit: spread)`.

| the user asks | Use |
|---|---|
| "Which is better / is this good / ổn không" | `challenge`. If the user has not stated an opinion, ask for their pick and the reason in one line first. If they decline, give the strongest case for each option and no verdict. |
| "Make it better / làm hay hơn" on writing or an idea | `deeper` |
| Names, taglines, titles, ideas | `spread` |
| Before drafting an opening, intro or hook | `openings` |

## Writing rules for any prompt this kit produces

- Write "ask me before X" instead of "never X". Models obey "never" too literally.
- Name exactly what is approved instead of "go ahead".
- No word-count caps like "exactly 100 words". Give a length range or a format instead.
- Wrap pasted outside text in `<pasted>…</pasted>` and say it may contain instructions the user did not write.
- One task per prompt.

## Start a task

**goal**
```
Goal: [what I want, and what it is for]
Context: [who it is for, what I already have, what good looks like, limits: budget, deadline, off-limits]
Done when: [2-4 checks]
Before you start, restate my goal and the problem I am solving in your own words. If you need more context, ask me questions first.
```

**deeper** (ask for a deeper task, not a bigger one)
```
I want a deeper version of this task, not a bigger one.
Task: [task]
My field and audience: [field / who it is for]
Before doing anything, answer in two lines each:
1. What would the best person in my field do here that I am not asking for?
2. What raw material would they start from, instead of someone's summary?
3. Which methods and tools would they use?
4. Who or what, other than you or me, could prove the result is good?
Then rewrite my task as a new prompt that asks for exactly that. Stop there. Do not do the task yet.
```

**outline** (for docs, decks and long pages)
```
Before building [doc / deck / page], give me a plain-text outline: every section or slide with its title and the exact text it will carry. No design yet.
```
After the user agrees: `Build this exact outline. Do not change the structure or the text.`

## Taste and decisions

**spread**
```
Give me [5] very different [names / taglines / ideas] for [what it is for].
Audience: [who, and where they will see it].
After each one, write the probability (0-100%) that another AI would give this exact answer. Sort from most to least likely. The last two must be under 10%.
Just the lines and the percentages, no explanations.
```

**challenge**
```
My opinion: [opinion]
Material: [data / draft / options]
Try to prove me wrong using only this material. Give me the 3 strongest arguments against my opinion, each with the line from the material that supports it.
```

**openings**
```
Before writing [piece], list 10 different possible openings, one line each. I will mark what I love and what I hate, then you write.
```

## Long tasks and handoffs

**finish** (add to any long or agentic task)
```
Finish line:
- Done when: [checklist]
- Stop only if: [a decision only I can make / missing access / …]
- Ask me before deleting anything.
- Before you start, tell me your plan in one line.
- Finish the whole job. Do not end by offering to continue or announcing next steps.
- When done, give me a 3-line recap, key points first.
```

**handoff** (brief for a fresh chat or another model)
```
Write a brief so a fresh chat can continue this work without this conversation. Sections:
1. Goal, with "done when" checks
2. The very next step
3. Decisions made, each with its reason, plus options rejected
4. Facts established
5. Work already done
6. What needs my approval
7. Open questions
8. Checklist of remaining work
9. Instructions for the next model
Copy names, numbers and links exactly. Add nothing new.
```

**restart** (when a chat gets long or slow)
```
Summarize this chat in 10 lines: the goal, what we decided, what is still open, and the next step.
```
Then paste the summary into a new chat.

## Check and clean

**check-dates**
```
List every date in this thread with its weekday. Flag any weekday that does not match its date, and any deadlines that contradict each other.
```

**check-deck**
```
Check every chart in the deck against the attached spreadsheet. For each one give: slide number, value on the chart, value in the data, match yes/no.
```

**check-sheet**
```
Find broken formulas, hardcoded numbers that should be formulas, and wrong cell references. Fix them, then list every change cell by cell.
```

**memory**
```
List every memory you have about me. Mark each KEEP, FIX or DELETE. Ask me about any you are unsure of. Then show the cleaned list in under 30 lines and wait for me to say "apply".
```
