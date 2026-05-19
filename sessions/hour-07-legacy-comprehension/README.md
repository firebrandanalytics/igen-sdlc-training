# Hour 7 — Legacy-Code Comprehension: `bounded_cache.py`

iGEN Developer AI Training · Session 4 (Hour 7)

This folder contains a single Python module you have never seen before.
Your job is **not** to use it — it is to *understand* it deeply enough
to change it safely. The lab guide walks you through that process.

---

## What is in here

| File | What it is |
|------|-----------|
| `bounded_cache.py` | The mystery code. A ~150-line cache decorator. |
| `LAB-GUIDE.md` | Step-by-step instructions for Hour 7. Start here. |
| `README.md` | This file. |
| `C7-ai-ready-spec-template.md` | AI-ready spec template handout. |
| `C10-what-good-looks-like-review-rubric.md` | Review rubric for AI-generated code. |

There is no test suite — writing one is part of the lab.

---

## Running the demo

The module ships with a small `__main__` block so you can exercise it
without writing any test code first.

### Windows (Git Bash or PowerShell)

```bash
python bounded_cache.py
```

Python 3.8+ is required. No third-party packages; standard library only.

### macOS / Linux

```bash
python3 bounded_cache.py
```

Expected output: a short run showing cache hits, an LRU eviction, and
TTL expiry. The exact numbers printed are in the comments at the bottom
of the file.

---

## What you should NOT do before the lab

Do not read the lab guide before the session. Part of the exercise is
approaching the code cold, the way you would in a real handoff.

---

## Homework

Homework #3 is assigned after this hour — run the comprehension methodology on a
piece of your own code. See `../../homework/homework-3-brief.md`.
