---
name: "exam-study-guide"
description: "Use when the user uploads lecture slides, question banks or past exams and wants an interactive HTML study guide with MCQ practice, written questions and a random mock-exam generator."
---

# Exam Study Guide Builder

Turns uploaded course material (lecture slides, textbook chapters, question banks, past exams) PLUS related exercises found on the web into ONE self-contained interactive HTML study guide with: concept notes, MCQ and written practice ordered from easy to hard, and a Mock Exam tab that rolls random exams in the real exam format.

## Language rules

- Chat replies: the user's language (often Vietnamese + English).
- **Everything inside the study guide is written in English**: concepts, questions, options, explanations, model answers, marking points. Questions from Vietnamese or other-language sources are translated to English.
- **Vietnamese is a toggle, not always on.** Every piece of content also gets a Vietnamese version (explanation of the concept / question / answer in Vietnamese, plus inline Vietnamese glosses for technical terms, e.g. elasticity (độ co giãn)). A global "🇻🇳 Giải nghĩa tiếng Việt: ON/OFF" switch shows or hides all Vietnamese. Default OFF. Each question card also has its own small "VI" button to reveal Vietnamese for just that question.

---

## Step 1 — Inventory the uploads (silent, fast)

1. List every uploaded file. Sort each into: `slides`, `textbook`, `question_bank`, `past_exam`, `other`.
   - `textbook` = a book file (full book or book chapters: has chapters, page numbering, table of contents, ISBN/copyright page). Lecture slides are NOT a textbook.
2. For each file record: chapter(s) covered, the topics per chapter, page/slide count, whether text is extractable or it is scanned (needs OCR / page images).
3. From question-bank files, identify the source book: title, author(s), edition, publisher. Look at headers, footers, copyright lines, file names.
4. From the past exam(s), record the real exam format: number of MCQs, number of written questions, question styles (definition, calculation, graph analysis, explain/compare, case), marks per part, time allowed, difficulty.

Do NOT read every file in full yet; skim enough to build the inventory.

## Step 2 — Configure BEFORE generating

Show briefly what you found first (e.g. "Slides: Ch1–6, Textbook: Ch1–12, Question banks: Ch1, Ch3, Past midterm: 10 MCQ + 4 written").

### 2a. Range — printer-style, ONLY when a textbook file was uploaded

- **No textbook uploaded (only slides / question banks / past exams):** do NOT ask about range. Use ALL uploaded sources.
- **Textbook uploaded:** ask the range like a printer dialog, with exactly two options:
  - **"Tất cả / All"** → use every uploaded source in full.
  - **"Chọn phạm vi / Custom range"** → the user MUST type the range (chapters and/or pages, e.g. `Ch 1-5`, `Ch 1,3,5`, `p. 12-140`).
- Rules for Custom range:
  - If the user picks Custom range but gives no range, or the range can't be parsed (e.g. chapter not found in the files), ask again in one short line and wait. Do not start generating until a valid range is given.
  - Accept formats like a printer: single (`3`), list (`1,3,5`), span (`1-5`), mixed (`1-3,5`), pages (`p. 10-50`).
  - Apply the range to ALL sources (textbook, slides, question banks, past exam, web search): only include content and questions from those chapters/pages/topics.
  - Echo the parsed range back in one line (e.g. "Phạm vi: Chương 1, 2, 3, 5") before continuing.

### 2b. Other options (always ask, one AskUserQuestion call together with 2a when 2a applies)

Pre-fill recommended answers from the inventory and past exam:
1. **Exam format for the Mock Exam** — e.g. "10 MCQ + 4 written (matches past midterm) (Recommended)", "20 MCQ + 2 written", custom.
2. **Question types to include** (multiSelect) — MCQ, True/False, Written: definition/short answer, Written: calculation/numerical, Written: graph/diagram analysis, Written: explain/discuss.
3. **Extra sources** (multiSelect) — "Related exercises from the web, easy → hard (Recommended)", "Question banks of the same book for missing chapters (Recommended)", "Generate original questions to fill gaps", "Use only my uploaded files".

If the user is not present to answer: range = All, other options = recommended; state them at the top of the reply.

## Step 3 — Set up a task list

Create tasks: extract per chapter → web exercises per chapter → missing question banks → build question data (EN + VI) → build concept notes (EN + VI) → build HTML → verify → deliver.

## Step 4 — Extract content, chapter by chapter

Work one chapter at a time (within the chosen range) and write results to files immediately (don't hold everything in context):

- `work/ch{N}_concepts.json` — one entry per concept, written as a TEACHING explanation, not a summary (see "Concept notes must teach" below). Each entry has `en` and `vi` text. Note slide/page numbers.

### Concept notes must teach, not summarise

The user wants to understand how each idea works and how to reason with it, not a list of bullet points and formulas. A summary-style Concepts tab is a failure.

**First triage every topic (do this automatically, never ask).** Scan the past exam, homework/question banks and the slides, then give each concept a priority and a treatment, and record the evidence:
- Priority: `must know` (asked in the past exam, drilled in homework, or the basis of later chapters), `important`, `background`.
- Treatment: `deep` = full explanation (the six parts below, plus the formula, what-if and scenario blocks); `table` = comparison or reference material (forms of business, lists of features, advantages/disadvantages, ratio definitions, classifications) shown as a summary table first with the long explanation folded away; `skim` = short key idea, formula and one example.
- Show the result at the top of each chapter as a "Study map" table (topic, priority, treatment, where it is tested) with a "must-know only" filter.

For every `deep` concept write, in this order (for `table` and `skim` concepts write the key idea, the table or formula, an example and the common mistake, and keep the rest folded):

1. **Why it matters** — what problem the concept solves and where it is used later in the course or the exam.
2. **How it works** — a full explanation in connected paragraphs: the intuition, the mechanism step by step, and where each formula comes from (derive or justify it in words; never just state it). Several paragraphs per concept is normal.
3. **How to think it through** — the reasoning steps a student should follow when they meet a question on this concept (what to identify first, what to check, how to choose the method).
4. **Worked example placed directly under that concept** — a concrete numerical or case example solved line by line, with each step explained, then a one-line takeaway. Prefer the lecture's own examples; otherwise write one. Compute every number in code. Do NOT collect examples in a separate section at the end of the chapter.
5. **Common mistake** — the typical error and why it is wrong.
6. **Vietnamese version** — a real explanation of the same reasoning in Vietnamese (several sentences, English technical terms in brackets), not a one-line translation.

Every concept, whatever its treatment, also gets:
- **Key idea** — one or two sentences in a highlighted box at the top, with the decisive words in bold.
- **Highlighting** — a priority chip on the card (must know / important / background) and 2–4 key phrases marked inside the explanation, so the student can see at a glance what matters. Do not highlight everything.

Every concept that has a formula also gets:
- **What each symbol does** — a table: symbol, what it is, its role in the formula and what happens to the result when it rises or falls.
- **Why this formula** — where it comes from and when it applies (already part of "How it works").
- **What if it changes?** — a table of 2–3 computed cases: "if X changes → the result becomes Y → why this matters", tied to things the student cares about (e.g. "expected growth falls from 4% to 3% → the share price falls 15% although this year's dividend is unchanged → this is what a profit warning does"). Include at least one case about a change in expectations where the topic allows it.

Every concept about an effect or a problem (agency problem, tax shield, diversification, default risk, a decision rule) also gets:
- **Scenario: with and without** — the same firm or investor in two side-by-side cases, one where the thing is present and one where it is absent, with numbers, ending with the consequence for the firm or investor (e.g. firm value with an owner-manager vs with a hired manager, and the size of the agency cost).

Use tables freely: comparisons, classifications, advantages/disadvantages, sensitivity results and rule checklists are tables, not paragraphs.

Rules for concept notes:
- Cover only what the uploaded material teaches. Do not add formulas, ratios or topics that are not in the slides/textbook range, and do not write questions on them.
- Aim for roughly 4–6 concepts per chapter, each with its own example; a chapter's notes should read like a tutor explaining, a few hundred words per concept.
- Key-term tables, formula sheets and "what the past exam asked" are additions after the explanations, never a replacement for them.
- `work/questions.json` — append every question found.

Rules:
- Include EVERY question from the question banks, slides (in-class exercises, review questions, "check your understanding"), textbook end-of-chapter problems and the past exam that fits the selected types and range. Keep the original wording in English (translate if the source isn't English).
- Questions with images/graphs: describe the graph in text or redraw it as inline SVG; never drop the question.
- If an answer key exists, use it. If not, solve it yourself, and mark `answer_source: "solved"`. Double-check calculations by running them in code.
- Rate every question's difficulty (1 = recall/definition, 2 = understand/apply one concept, 3 = multi-step / calculation / graph, 4 = combine several concepts, 5 = hardest past-exam / challenge level).

Question schema:
```json
{
  "id": "ch3-web-017",
  "chapter": 3,
  "topic": "Price elasticity",
  "type": "mcq | tf | written",
  "subtype": "definition | calculation | graph | explain",
  "difficulty": 1,
  "source": "question_bank | slides | textbook | past_exam | web | generated",
  "source_ref": "URL or 'Test bank Ch3 Q17'",
  "stem": "English question",
  "options": ["A ...", "B ...", "C ...", "D ..."],
  "answer": 2,
  "explanation": "English: why C is right AND why each distractor is wrong",
  "model_answer": "(written only) English full answer",
  "marking_points": ["(written only) English point worth 1 mark"],
  "vi": {
    "stem": "Vietnamese explanation of what the question asks",
    "explanation": "Vietnamese explanation of the answer",
    "model_answer": "Vietnamese explanation of the model answer",
    "glossary": {"price elasticity of demand": "độ co giãn của cầu theo giá"}
  }
}
```

## Step 5 — Exercises from the web (not only from the uploaded content)

Do this for EVERY chapter in the range (not only missing ones), if selected:
1. From each chapter's topic list, search the web for related practice exercises: university course practice problems, problem sets with solutions, review quizzes, openly published course pages, publisher companion sites, open textbooks (OpenStax, LibreTexts, etc.). Search per topic, not one big query.
2. Also search for the identified book's question banks / review questions for chapters that have no uploaded bank.
3. Collect a spread from easy to hard for each chapter: target roughly 40% difficulty 1–2, 40% difficulty 3, 20% difficulty 4–5. Aim for at least ~30 MCQs and ~8 written questions per chapter in total across all sources.
4. Rewrite each web exercise into the schema in English, keep the URL in `source_ref`, add the Vietnamese `vi` block, and verify the answer yourself (don't trust a web answer key blindly; recompute numbers in code).
5. Don't use paywalled or obviously pirated test-bank sites, and don't bypass blocked pages. If a site is declined, move on.
6. Where a chapter or difficulty level is still thin and generation was selected, write original questions in the same style as the past exam (tag `generated`).
7. Tell the user clearly how many questions per chapter came from their files, from the web, and were generated.

## Step 6 — Build the HTML

Generate the HTML with a script (Python or Node) that injects `questions.json` and the concept files into a template — do not hand-type thousands of lines into the reply. Single self-contained file with no external dependencies.

**Formulas must be typeset, never typed as plain text.** Fractions, exponents, subscripts, sums (Σ), products, roots and Greek letters are written in LaTeX in the data files and rendered with KaTeX. Do not show formulas as `PV = C[1 - 1/(1+r)^t]/r`, with `^`, `_`, or Unicode superscript/emoji-like symbols in code boxes: it looks unprofessional and can be misread.
- Install KaTeX with npm, render every formula at build time (`katex.renderToString`, display mode for formula blocks, inline mode for symbols inside sentences and table cells, `throwOnError: true`), and embed the KaTeX stylesheet in the page with its woff2 fonts converted to base64 data URIs, so the file works offline and inside the artifact sandbox.
- Use a delimiter that cannot clash with currency for inline maths in text, e.g. `\( ... \)`; never `$...$`.
- In question stems, options, explanations and model answers, convert any remaining `^(...)`, `^x`, `_(...)` and `_x` to real superscripts and subscripts before display.
- The Formulas tab is a table per topic: name, typeset formula, when to use it.

Global header: course name, range used ("Range: All" / "Range: Ch 1–5"), Vietnamese toggle, dark/light toggle.

Vietnamese toggle implementation: all Vietnamese text lives in elements with class `vi`; the switch toggles a class on `<body>` that shows/hides them; per-card "VI" buttons toggle only that card; remember the setting in localStorage (try/catch, fall back to in-memory).

Tabs:
1. **📘 Concepts** — per chapter: a Study map table (topic, priority, treatment, where tested) with a must-know filter, then one card per concept. Each card: priority chip → highlighted Key idea → then by treatment. `deep`: Why it matters → How it works (key phrases highlighted) → typeset Formula + "What each symbol does" table → summary table if any → "What if it changes?" table → "Scenario: with and without" → How to think it through → Worked example directly below → Common mistake. `table`: summary table first, then formula, what-if, scenario, example, mistake, and the long explanation in a folded section. `skim`: formula, example, mistake, the rest folded. Vietnamese explanation on every card (shown when the toggle is ON, plus a per-card VI button). Never a bullet-point summary. After the concept cards: key terms table, "what the past exam asked about this". Graph explanations as inline SVG where helpful. Chapter sidebar and an "In this chapter" list linking to each concept.
2. **✅ MCQ Practice** — default order: easy → hard within each chapter (difficulty badge 1–5 on each card). Filters: chapter, topic, source, difficulty; options to shuffle or "Level up" mode (start easy, move to harder questions after 3 correct in a row). Instant feedback with full explanation; "only questions I got wrong" mode.
3. **✍️ Written Questions** — easy → hard by default; filter by chapter/subtype/difficulty; textarea for the user's answer; "Reveal model answer" shows the model answer + marking points as a checklist to self-mark.
4. **🎲 Mock Exam** — "Roll new exam" builds a random exam in the configured format (e.g. 10 MCQ + 4 written), spread across the chosen chapters, difficulty mix like the past exam, questions ordered easy → hard within each section; optional countdown timer; seed number so an exam can be repeated; on submit: MCQ score, review of each question, then written model answers with self-marking and total score.
5. **📊 Progress** — attempts per chapter, accuracy by topic and by difficulty level, weakest topics list.

UX: clean, readable, mobile-friendly, keyboard shortcuts (1–4 to answer, → next, V to toggle Vietnamese), question counts shown per filter.

## Step 7 — Verify

- Count questions per chapter/type/source/difficulty and compare against the source files (nothing dropped; nothing outside the range; each chapter has easy through hard).
- Every question is in English and has a `vi` block; every MCQ has exactly one correct answer index within range; every written question has a model answer and marking points.
- Every concept has all six parts (why, how it works, how to think, worked example directly under it, common mistake, Vietnamese explanation); no concept is only bullets or a bare formula; nothing in the notes is outside the uploaded material.
- Every concept has a priority, a treatment and a highlighted key idea; every formula concept has the symbol table and the what-if table; effect/problem concepts have a with/without scenario; comparison material is in tables.
- No raw maths markup is visible anywhere in the rendered page: search the page text (outside KaTeX output) for `^`, `\(`, `**` and `_(` and fix any hit; open one formula-heavy card and check fractions, exponents and Σ render correctly.
- Recompute all numerical answers in code.
- Load the HTML (e.g. headless check with Node/jsdom or a browser) and confirm: tabs switch, filters work, Vietnamese toggle hides/shows all `vi` text, mock exam rolls the right number of each type, no console errors.

## Step 8 — Deliver

Publish the HTML as an artifact (or send the file if artifacts are unavailable). Reply briefly with:
- the configuration used (range, format, types),
- question counts per chapter, by source (uploaded / web / generated) and by difficulty,
- which chapters had thin coverage,
- Sources: list of web pages used.

## Token budget (stay within Claude Pro limits)

- Be thorough on content, economical on process: read each file once, write extractions to disk, never paste big file contents back into the chat.
- Build the HTML from data files with a script; don't re-output the whole page for small fixes — edit the template/data and rebuild.
- For very large uploads, do chapters in order and tell the user if you have to stop partway, so they can say "continue" in a new message.