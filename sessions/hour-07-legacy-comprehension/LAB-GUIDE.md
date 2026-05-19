# Lab Guide: Legacy-Code Comprehension

iGEN Developer AI Training · Session 4 (Hour 7)

> **[Needs Tech Review]** — Claude Code command syntax and pytest invocation
> should be verified against the distributed Windows environment before this
> sheet is used live.

---

## What this lab is for

You have a module you have never seen before. Your team is about to change it.
You have the rest of this hour to understand it well enough to change it safely.

That is the scenario. Everything else in this lab is the methodology.

**There is no test suite.** Writing one is part of the exercise.
**You will not be writing new features.** You will be building understanding.

**Time:** approximately 60 minutes (one full hour).

---

## Setup

No virtual environment is needed — `bounded_cache.py` uses the standard library
only. Confirm it runs before you do anything else.

### Windows (Git Bash or PowerShell)

```bash
cd sessions/hour-07-legacy-comprehension
python bounded_cache.py
```

### macOS / Linux

```bash
cd sessions/hour-07-legacy-comprehension
python3 bounded_cache.py
```

Expected: a short run showing cache hits, an eviction, and TTL expiry prints to
the terminal. If it errors, stop and fix the environment before continuing.

**Open a Claude Code session in this directory.** Everything below is run through
that session.

---

## Step 1 — Literal behavior (10 minutes)

Before you can ask "why," you need to know "what."

**Prompt Claude Code:**

> "Read `bounded_cache.py`. Describe in plain English exactly what the module does
> — inputs, outputs, what happens on a cache hit, what happens on a miss, and what
> the module explicitly does NOT do. Stay literal; save opinions and why-questions
> for later."

Read the response. Your goal: could you explain this module to a colleague in
two minutes without looking at the code? If not, ask follow-up questions until
you can.

**Checkpoint 1:** You can describe the module in two minutes without looking at
the code.

---

### Grounded-learning beat — do not skip this

Before moving on: is there anything in Claude Code's explanation that you did not
fully understand? A term, a pattern, a function call?

If yes — stop, and ask Claude Code to explain it using *this exact code* as the
example. Not a general explanation. Grounded in here.

Example:

> "Explain what `functools.wraps` does. Use the `wrapper` function in
> `bounded_cache.py` as your example. What would break if it were removed?"

This is not remedial. Everyone is a junior at something. The discipline is: do
not bluff past the unknown. One concept you actually understand is worth more than
five you nodded past.

**Common concepts worth grounding here:** `functools.wraps`, `OrderedDict`,
`time.monotonic`, closure variable capture (why `_store` and `_lock` persist
across calls), `NamedTuple`.

---

## Step 2 — Intent reconstruction (15 minutes)

This is the centerpiece of the methodology. Literal understanding tells you *what*
the code does. Intent reconstruction tells you *why* it does it that way — and
therefore what is load-bearing.

**Prompt Claude Code:**

> "For each non-obvious design decision in `bounded_cache.py`, explain:
> (1) what the decision is,
> (2) why the engineer probably made it — what problem is it solving,
> (3) whether you think it is intentional or incidental.
> Focus on decisions where a different reasonable choice would produce different
> behavior."

Read the response carefully. For each decision, ask yourself: does this
explanation make sense given what I know about how this code is likely to be
used? If the explanation feels thin, probe:

> "Why would you use an `OrderedDict` here rather than a plain dict?
> What operation does `move_to_end` provide that a plain dict can't?"

> "The lock is released before the wrapped function is called. Why would
> an engineer make that choice? What is the cost and what is the benefit?"

> "What is a `_SENTINEL` object, and why is it used instead of `None` here?
> What would break if you replaced `is not _SENTINEL` with `is not None`?"

**Checkpoint 2:** You can name at least four non-obvious design decisions and
give a one-sentence "why" for each.

> **If you get stuck:** the goal is to reconstruct the engineer's thinking,
> not to find the one correct answer. If Claude Code gives two plausible
> explanations and you're not sure which is right, that ambiguity is valid
> information — note it. For code from your own organisation, git history and
> the original author are the next sources of evidence.

---

## Step 3 — Inferred requirements and preserve-list (8 minutes)

The output of intent reconstruction is two lists.

**Prompt Claude Code:**

> "Based on the design decisions we've just discussed: what requirements was this
> code apparently written to satisfy? List them. Then, from that list, identify
> the behaviors that must not be changed by any safe modification — the
> preserve-list."

A *requirement* is something like: "works correctly in a multi-threaded program."
A *preserve-list item* is something like: "do not hold the lock while the wrapped
function executes — this is intentional, not an oversight."

The preserve-list is the output you will hand to anyone (including your future
self, or Claude Code) before they make a change to this module.

**Checkpoint 3:** You have a requirements list and a preserve-list with at least
four items.

---

## Step 4 — Characterization tests (12 minutes)

Characterization tests pin the load-bearing behaviors. They do two things:
1. If your understanding was wrong, the tests will fail when you run them — and
   that tells you your understanding was wrong.
2. If someone later makes a change that breaks a preserve-list item, the tests
   catch it.

**Prompt Claude Code:**

> "Write a pytest test suite that pins the behaviors on the preserve-list we
> just produced. Focus on behaviors that are hard to verify by inspection — not
> trivial things like 'the decorator returns a callable'. Name each test after
> the preserve-list item it covers."

Review the tests before running them. Ask yourself:
- Does each test actually exercise the behavior it claims to?
- Does the test cover the edge case that matters, or just the happy path?

Run the tests:

### Windows

```bash
python -m pytest test_cache.py -v
```

### macOS / Linux

```bash
python3 -m pytest test_cache.py -v
```

If any tests fail, investigate before assuming the test is wrong. A failing test
is a signal: either your test has a bug, *or* your understanding of the code was
incorrect. Both are important to know.

**Checkpoint 4:** At least 6 characterization tests pass. Each test is named
after what preserve-list item it is pinning.

> **If `pytest` is not installed:** `pip install pytest` (with your venv active,
> if you are using one).

> **If a test you wrote keeps failing and you've checked the logic:** ask Claude
> Code to explain what the test is actually asserting versus what you intended.
> Sometimes a test has a subtle off-by-one in timing or a wrong comparison.

---

## Step 5 — Apply the pre-designed change (10 minutes)

Now your dossier earns its keep.

Here is a change someone on your team proposes:

> "The `_SENTINEL` check is a bit obscure. `dict.get()` already returns `None` for
> a missing key. Let's simplify the hit-check to:
>
>     entry = _store.get(key)
>     if entry is not None:
>         if time.monotonic() < entry.expires_at and entry.value is not None:
>             ...

Before touching a single line of code:

1. Read your preserve-list. Does any item apply to this change?
2. Ask Claude Code: "Does this change violate any of the preserve-list items?
   Walk through the change and tell me what it does to a function that returns
   `None`."
3. Now apply the change to `bounded_cache.py`.
4. Run your characterization tests.

**Checkpoint 5:** At least two tests fail after the change. Identify which
preserve-list items the failing tests correspond to. Revert the change.

> **If your tests don't catch the change:** your test suite has a gap. Ask Claude
> Code: "What test would catch the case where a function returns `None` and the
> cache fails to cache that result?" Add the test, re-run, confirm it fails on
> the modified code and passes on the original.

---

## Reflection (5 minutes)

Before leaving:

1. Which design decision took the longest to understand, and why?
2. The pre-designed change looked reasonable at first glance. At what point did
   you become confident it was wrong?
3. If you had to hand this dossier to a new team member before their first change
   to this module, what single item would you most want them to read first?

---

## What you have built

At the end of this lab you have five artifacts:

| Artifact | What it is |
|----------|-----------|
| Literal behavior doc | Plain-English description of what the module does |
| Intent analysis | The "why" behind each non-obvious decision |
| Inferred requirements | What the code was built to satisfy |
| Preserve-list | What must not change in any safe modification |
| Characterization tests | The automated guard that enforces the preserve-list |

Together these are a **comprehension dossier** — a localized CLAUDE.md for this
piece of code. Anyone (human or AI) who reads it before making a change will make
a safer change.

---

## Appendix — Quick Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `python bounded_cache.py` exits immediately with no output | Wrong Python version (needs 3.8+) | `python --version` to check; use `python3` on macOS/Linux |
| `ModuleNotFoundError: No module named 'bounded_cache'` | Running pytest from the wrong directory | `cd` into `sessions/hour-07-legacy-comprehension/` first |
| `ModuleNotFoundError: No module named 'pytest'` | pytest not installed | `pip install pytest` |
| A test you wrote fails when you didn't expect it to | Your understanding of the code may be wrong | Re-read the relevant section of the module; ask Claude Code what the test result is actually telling you |
| Claude Code produces a very long intent analysis | Normal — it's thorough | Focus on the decisions that map to your preserve-list; skip the minor style observations |
| The pre-designed change does not break your tests | Your test suite doesn't cover `None` caching | Add a test for it; see the Checkpoint 5 stuck-callout above |
