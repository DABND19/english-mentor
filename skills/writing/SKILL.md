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

## Analysis procedure (do this before writing any output)

1. Silently split the input into sentences and number them (1, 2, 3, ...).
2. Go sentence by sentence, in order. For each sentence, check it in full for errors —
   **a sentence can contain more than one error**; after finding one, keep checking the
   rest of that same sentence instead of moving on.
3. Build a plain list first: `sentence # -> wrong span -> fix -> one-line reason`.
   Do this for literally every sentence, including the last one — do not stop early
   once you feel you've found "enough" errors.
4. Before writing the final output, verify internally: does your list cover every
   sentence you numbered in step 1? If a sentence has zero errors, that's fine — but
   it must have been checked, not skipped.
5. Only after the list from steps 1-4 is complete, produce the final formatted output
   below, converting each list entry into a marked span + breakdown entry.

Do not merge steps 3 and 5 into one pass — drafting the marked-up text and hunting for
errors at the same time is what causes missed errors, especially near the end of longer
texts. Find everything first, format second.

## Output format

This format is FIXED — always use these exact four sections, in this exact order, with these exact headers. Do not improvise a different structure, skip a section, or reorder them, even if a section ends up short (e.g. write "No notable issues here" rather than omitting a section).

### 1. Original with marked errors

Reproduce the original text verbatim, but wrap every erroneous span in `inline code` markdown and append a bracketed reference number right after each one, e.g. (the fence below is only to set the example apart in these instructions — output the text as a normal paragraph, NOT inside a code block):

```
I `go`[1] to `shop`[2] yesterday.
```

Number errors left to right in the order they appear in the text, starting at [1]. Every numbered span here must have a matching entry in section 2, and vice versa. If a sentence contributed more than one numbered span, both must appear here — do not drop the second error in a sentence just because the first was already marked.

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

---

Before sending the response, do one last consistency check: the highest bracket number in section 1 must equal the number of entries in section 2, and every sentence from your step-1 count must be accounted for by at least a "no errors" pass. If either check fails, fix it before responding rather than sending a mismatched output.

Keep the tone encouraging and matter-of-fact — this is coaching, not a report card. No extra preamble before section 1, no summary after section 4.