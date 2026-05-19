# iGEN AI Software-Development Training — Student Materials

Hands-on materials for the Firebrand-led AI software-development training for
iGEN developers — five two-hour sessions (ten hours) on agentic development
with Claude Code.

## How this repo is organised

- **`sessions/`** — one folder per hour, `hour-01` through `hour-10`. Each hour
  folder has a `README.md` describing what that hour covers, plus that hour's
  exercise, lab guide, and the handouts you'll need. During a session, open the
  folder for the current hour — everything you need for it is in one place.
- **`handouts/`** — the full set of reference cards: glossary, CLAUDE.md and
  SKILL.md templates, cheat sheets, checklists, and the Claude Code commands
  card. The copies inside each hour folder are drawn from here; this is the
  canonical set.
- **`homework/`** — the three take-home assignments: HW1 (after Hour 4) operate
  Claude Code on a real task; HW2 (after Hour 6) write a CLAUDE.md and SKILL.md;
  HW3 (after Hour 7) run the comprehension methodology on your own code.
- **`cli-utility/`** — the IFTA fuel-tax CLI: a self-study take-home reference,
  not a live hour. Work through it at your own pace.

## The two starter codebases

You extend these by directing Claude Code; each lives in its hour folder:

- `sessions/hour-08-web-app-backend/` — the Mileage Logbook web app
  (FastAPI + SQLite + Jinja2), built up across Hours 8 and 9.
- `sessions/hour-07-legacy-comprehension/` — `bounded_cache.py`, the unfamiliar
  module you learn to understand and change safely in Hour 7.

## Using this repo

Clone it before Session 1. During each hour, work inside that hour's folder,
directing Claude Code. Worked solutions are kept separately and are not in this
repo.
