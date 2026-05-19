# Homework #3 — Run the Hour 7 Comprehension Methodology on Your Own Code

**Assigned after:** Session 4 (Hours 7–8)
**Due before:** Session 5
**Time budget:** 45–60 minutes

---

## The Assignment

Pick a piece of code from your own work — something you didn't write yourself, or wrote long enough ago that you can no longer recall the intent. Apply the Hour 7 comprehension methodology to it. Produce the dossier artifacts. Then do the one thing a classroom exercise can't — check the AI's inferred intent against ground truth.

---

## Choosing Your Code

**What you're looking for:**

- A module, class, or file you find genuinely unfamiliar — not something you wrote last week.
- Bounded enough for roughly 45 minutes: 100–250 lines is a good target. A sprawling service or a deep inheritance chain is too much; a single utility function is too little.
- Any language works. The methodology is language-agnostic. You probably won't be working in Python.
- You don't need deep context on the domain to do this — that's the point. The AI helps you reconstruct it.

**It's fine if you can only discuss it at a high level in Session 5.** You don't need to share code or internal details — you just need to be able to describe what you found and how the process went.

---

## What to Produce — The Comprehension Dossier

Work through the methodology in order. The output is a set of artifacts you create alongside Claude Code — a localized CLAUDE.md for that piece of code.

**1. Literal-behavior document**
Ask Claude Code to describe what the code does — inputs, outputs, side effects, control flow. Correct anything it gets wrong. Don't move on until this is accurate.

**2. Intent analysis**
This is the centerpiece. For each non-obvious decision in the code — an algorithm choice, a constraint, an unusual pattern — ask the AI to reconstruct *why* that decision was made. What problem was the author solving? What would have gone wrong with a simpler approach? Push back on vague answers.

**3. Inferred requirements**
Synthesize the intent work into a list of requirements the code was written to satisfy. What was it trying to guarantee? These don't need to match any official spec — they're the AI's (and your) best reconstruction.

**4. Preserve-list**
From the inferred requirements, identify what is load-bearing: behaviors or constraints that a future change must not break, even if they look safe to touch at first glance.

**5. Characterization tests**
Write two or three tests that pin the load-bearing behavior you identified. These don't have to run (some teams can't run tests against production code in a homework context) — even a written-out test plan that says "given X, it should Y, not Z" counts.

---

## The Standout Move — Check the AI's Inferred Intent

After you've completed the intent analysis, verify it.

Use `git blame` or `git log` on the file to find who wrote it. Then do one of these:
- **Check the commit messages** — do they confirm or contradict the AI's inferred "why"?
- **Ask the author** — "I was reading this code and the AI inferred it does X because Y. Is that right?" Even a two-minute hallway conversation counts.

Note where the AI got it right, where it was plausible but wrong, and where it missed something the author would have considered obvious. This is the step that turns a classroom exercise into something genuinely useful for your work.

---

## Reflection — Bring These to Session 5

After the session, write short answers to these four prompts:

1. **How accurate was the AI's intent reconstruction?** What did it get right, and where did it go astray?
2. **How did your own guidance change what the AI produced?** What would it have gotten wrong if you'd just let it run?
3. **What did verifying against ground truth reveal?** (git history, author conversation, or both — describe what you found.)
4. **One failure or frustration** — a moment where the AI was confidently wrong, unhelpfully vague, or led you somewhere you had to back out of.

Keep each answer to two or three sentences. You're capturing your experience while it's fresh — not writing a report.

---

## What to Bring to Session 5

Your reflection answers. We'll hear from a few people at the start of the session.

You don't need to share the actual code. Just be ready to describe the code at a high level, walk through what the AI inferred, and say what ground truth confirmed or corrected.

---

*Reference: the Hour 7 methodology was introduced in Session 4 and is documented in the Session 4 lab guide. Questions? Session 5 opens with the share-back.*
