---
name: writing
description: Give structured feedback on a piece of English writing to help a non-native speaker improve. Trigger this skill when invoked via the `/english-mentor:writing` slash command, or when the user explicitly asks to check, correct, or give feedback on their English writing, grammar, or phrasing. Do NOT trigger on ordinary English messages with no explicit request — casual chat in English should get a normal reply, not a critique.
---

# English Writing Feedback

Helps a non-native English speaker improve their writing over time by reviewing text they submit and giving structured, actionable feedback.

## When this triggers

- Invoked via `/english-mentor:writing` followed by the text to review.
- Message explicitly asks for feedback/correction on English writing, even without the slash command.

If the message is just ordinary conversation in English with no command and no explicit request for feedback, respond normally instead — do not critique unprompted.

## Output format

This format is FIXED — always use these exact five sections, in this exact order, with these exact headers. Do not improvise a different structure, skip a section, or reorder them, even if a section ends up short (e.g. write "No notable issues here" rather than omitting a section).

### 1. Original with marked errors

Reproduce the original text verbatim, but wrap every erroneous span in `` `inline code` `` markdown and append a bracketed reference number right after each one, e.g. (the fence below is only to set the example apart in these instructions — output the text as a normal paragraph, NOT inside a code block):

```
I `go`[1] to `shop`[2] yesterday.
```

Number errors left to right in the order they appear in the text, starting at [1]. Every numbered span here must have a matching entry in section 2, and vice versa.

### 2. Error breakdown

A numbered list matching the references from section 1 — one entry per number, same order:

```
[1] "go" -> "went": past tense needed here ("yesterday" signals past)
[2] "shop" -> "the shop": missing article
```

Keep each explanation short and concrete (the grammar rule or the more natural phrasing) — not academic. If the same underlying mistake repeats many times in one text, still number each occurrence in section 1, but you may group them under one explanation in section 2 (e.g. "[3][5][7] same article omission pattern as [2]").

### 3. Structure & logic

A short paragraph (2-4 sentences) on how the writing is organized: does it flow logically, are ideas connected clearly, is anything confusing or out of order. If there's nothing to flag, say so briefly rather than inventing filler.

### 4. Style

A short paragraph on register and style: formality level, word choice fit for context, anything too stiff/casual/repetitive for the apparent purpose of the text.

### 5. Recurring patterns

Reference error categories that keep coming up — both within this text (per section 2) and, when local persistence is available (see below), across past sessions via `track.py stats`. Name the pattern plainly (e.g. "articles keep getting dropped before singular nouns") rather than just repeating section 2. If there isn't enough history yet to spot a pattern, say so.

---

Keep the tone encouraging and matter-of-fact — this is coaching, not a report card. No extra preamble before section 1, no summary after section 5.

## Tracking patterns over time (local persistence)

This skill ships with `scripts/track.py`, which logs every review to a local SQLite file (`~/.english-mentor/progress.db` by default) so patterns can be tracked across sessions, not just within one conversation.

**This only works when you have real, persistent filesystem access** — e.g. running via Claude Code CLI or Pi on the user's machine. In a browser/claude.ai sandbox, the filesystem resets between conversations, so calling this script there is harmless but pointless (nothing will actually persist) — skip it in that context and fall back to within-conversation pattern tracking only.

When persistence is available, use it like this. `scripts/track.py` is relative to this SKILL.md's own directory, not your current working directory — `cd` there first (the path is visible from wherever you read this file), then run the commands below.

1. **Before writing feedback**, run:
   ```
   cd <this skill's directory> && python3 scripts/track.py stats
   ```
   Use the output to check whether any error categories are already recurring across past sessions, so you can reference them ("this is the Nth time articles have come up").

2. **After writing feedback**, log the review by piping JSON to stdin:
   ```
   cd <this skill's directory> && python3 scripts/track.py log
   ```
   with stdin set to:
   ```json
   {
     "original": "<the text the user submitted>",
     "corrected": "<your corrected version>",
     "errors": [
       {"category": "articles", "note": "short explanation of this specific mistake"}
     ],
     "tips": ["<the 1-2 tips you gave>"]
   }
   ```
   Use short, stable, lowercase `category` labels (e.g. `articles`, `prepositions`, `tense`, `word-choice`, `word-order`, `register`) and reuse existing categories rather than inventing near-duplicates, so counts aggregate meaningfully over time.

If the script errors out (e.g. no filesystem access, permissions issue), don't block on it — just give the feedback normally and mention briefly that this session's progress couldn't be saved locally.
