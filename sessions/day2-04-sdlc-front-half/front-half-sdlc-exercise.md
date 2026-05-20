# In-Class Exercise: Sharpen the F5 Apportionment-Summary Spec

iGEN Developer AI Training · Day 2 · Segment 4

---

## What you're doing

You just watched the instructor surface the implicit decisions buried in a
vague stakeholder ask. Now you do your own version, on the feature you'll
actually build in the next segment.

**This is the spec that goes into planning mode in segment 5.** The sharper
you make it now, the cleaner your build will be. Sloppy spec → arguing with
the agent later.

**Time:** 30 minutes total. Pace markers below.

---

## The vague ask

The product owner sends this:

> "Hey team — for the quarterly IFTA filing we need a page in the mileage
> logbook that shows our tax burden by state. Right now I'm exporting trips
> to a spreadsheet and doing it by hand and it's a nightmare. Just a summary
> view — totals per state, ideally with the percentages. Should be pretty
> quick to add since the data's already there."

That's the entire ask. No acceptance criteria, no agreement on what
"totals" means, no decisions about quarter scoping, no UI definition.

---

## Your task

Open Claude Code in the web-app starter (`sessions/day2-05-web-app-build/`).
Use the agent to help you surface decisions and draft text — but **you** make
every call. By the end of 30 minutes you have a sharpened spec you would feel
comfortable handing to planning mode in segment 5.

Work the three steps in order. Drafts beat polish — a working spec that
exposes the key decisions is more valuable than a beautiful one that took
the whole segment.

---

### Step 1 — Interrogate the ask (~7 min)

Ask Claude Code to read the existing `README.md`, `main.py`, and `db.py` in
the starter, then ask something like:

> *"Read these files for context. Before I write any requirements for the
> apportionment summary page, list every decision this ask leaves implicit
> — what an engineer would have to answer before building. Group them:
> scope, behaviour, edge cases, anti-goals."*

Read the question list it produces. Add any of your own. The questions you
will almost certainly need to answer:

- **Which quarter?** Current? All quarters in the data? User-selectable from a dropdown?
- **What "totals"?** Miles only, or also fuel used, also tax owed?
- **"Percentages" of what?** Share of total miles by jurisdiction? Share of total tax? Both?
- **Sort order?** Alphabetical by code? Descending by tax? By miles?
- **Empty case** — what shows when no trips match (empty quarter, brand-new install)?
- **Where in the app does it live?** New page? Section on an existing page?
- **Read-only or interactive?** Filters, sorting controls, export buttons — in scope or out?

Pick answers and write them down. You'll use them in step 2.

---

### Step 2 — Sharpened requirements (~15 min)

Use the C7 AI-ready spec template (`C7-ai-ready-spec-template.md` in this
folder, or your printed copy). Fill in these sections for the F5 feature:

**Task** — One paragraph. What exactly are you building, where does it live
in the app, what does the user see?

**Constraints** — At minimum:
- No new dependencies (existing stack: FastAPI + Jinja2 + SQLite).
- Existing schema only — no new tables for this version.
- The IFTA math comes from a *calc-skill* document you'll extract in segment 5; assume the math is correct, your job is wiring.

**Anti-Goals** — Be explicit about what is **out** of scope. Likely candidates:
- Export to PDF / CSV (the ask mentions "spreadsheet" — is replacing it in scope, or is the on-screen view enough for v1?)
- Editing trips from this page
- Filters or controls beyond what's strictly needed
- Multi-quarter comparison views
- Anything historical / archived

**Acceptance criteria** — Write at least five. Each is a pass/fail statement
checkable without judgment. Examples to seed yours:

- "The page shows a row for every jurisdiction that has miles in the selected period."
- "Each row shows jurisdiction code, name, total miles, fuel used (gal), and tax owed (USD)."
- "A totals row at the bottom shows fleet-wide totals for miles, fuel, and tax."
- "Tax values match the IFTA CLI's output for the same input data."
- "An empty result set renders a 'no trips for this period' message, not an empty table."

You decide the rest — quarter scoping, sort order, percentage column, etc.

**Files-to-read-first** — Which existing files does Claude Code need to read
before generating any code? At minimum, list the templates that contain the
nav and layout patterns, and the DB module if you're going to add a query
helper.

**Glossary** — Define any term that an outsider (or an LLM) might get wrong.
"Apportionment", "jurisdiction", "period", "fleet-wide" — at least the ones
your spec relies on.

---

### Step 3 — Design sketch (~7 min)

Quick high-level design — bullets, not paragraphs:

- **Route:** what's the URL path? What HTTP method? What query parameters (e.g., `?period=2024-Q1`)?
- **Data flow:** how does data get from `db.py` to the template? Do you add one new DB function, or compose existing ones? Where does the IFTA calc helper sit — inline in the route, or a new module?
- **Template:** new file, or section in an existing template? Which layout/base does it extend?
- **What's the smallest reasonable change?** Resist over-design. The simpler the spec, the cleaner the plan.

---

## Minimum-viable spec checklist

Before you wrap, your artifact should have:

- [ ] At least 5 acceptance criteria, each checkable
- [ ] An explicit anti-goal list (at least 3 items)
- [ ] A decision on quarter scoping (current / all / user-picks)
- [ ] A decision on which columns and which sort order
- [ ] A decision on the empty case
- [ ] A route/path and a template name (even if approximate)
- [ ] A glossary entry for "apportionment" and "jurisdiction"

If a checkbox isn't ticked, you'll be making that decision under time
pressure in segment 5 — with the agent already mid-plan. Better to decide now.

---

## Debrief

Be ready to share:

1. What's the most important decision your spec made that the ask didn't?
2. What ended up in your anti-goals that the product owner probably assumed was in scope?
3. Is your feature small enough to fit one planning-mode + parallel-build session, or do you suspect it'll spill?

---

## Reference (peek if useful)

The instructor-side worked example in the internal repo
(`instructor-notes/day2-04-sdlc-front-half/01-vague-ask.md`,
`02-sharpened-requirements.md`, `03-design-sketch.md`) is for a different
feature ("flag suspicious trips") — useful as a model of *what the
artifact looks like*, not as an answer for F5. Ask the instructor if you
want to see one after the segment.
