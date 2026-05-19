# In-Class Exercise: Front-Half SDLC Pass on the Web App

iGEN Developer AI Training · Session 3 (Hour 6)

---

## What You're Doing

You just watched the instructor walk through the full front-half SDLC process live
— vague stakeholder ask to sharpened requirements, design sketch with explicit
anti-goals, user stories with tight acceptance criteria, and a test plan written
before any code exists.

Now you do your own version.

**Time:** 20 minutes to work; 5 minutes to compare with a neighbour.

---

## The Vague Ask

The product owner sends this message:

> "Hey team — we've been getting complaints from the compliance folks about bad trip
> data. Drivers sometimes log trips that are clearly wrong — like a vehicle covering
> 1,400 miles in a single day, or a trip where the start and end location are the
> same city. We need the system to flag those somehow. It would also be nice to
> filter them out of reports. Low priority for now but let's get it in the backlog.
> Let me know if you have questions."

That is the complete ask. No ticket, no acceptance criteria, no definition of
"suspicious," no agreement on what "flag" means in the UI.

---

## Your Task

Open a Claude Code session in the `sessions/hour-08-web-app-backend/` directory
(the Mileage Logbook starter you will build in Hours 8–9). Use Claude Code to help
you sharpen this ask into structured SDLC artifacts.

Work through the following steps in order. You have 20 minutes — do not try to
produce perfect documents. A working draft that exposes the key decisions is more
valuable than a polished spec that took all hour.

---

### Step 1 — Interrogate the ask (3 minutes)

Ask Claude Code to read the existing `README.md` and `db.py` in the starter app,
then ask it a question like:

> "I have a vague stakeholder request to flag suspicious trips. Before writing any
> requirements, what questions should I answer to make this implementable?"

Read the questions it generates. Add any of your own. Choose the three most
important and decide on an answer for each. Write your answers down — you will use
them in the next step.

---

### Step 2 — Write a sharpened requirements document (10 minutes)

Using the C7 AI-ready spec template (`C7-ai-ready-spec-template.md` in this folder,
or your printed copy), fill in the following sections for the "flag suspicious
trips" feature:

**Task** — Be concrete. What exactly will be built? Where does the flag live in the
data model? How does it appear to users?

**Constraints** — At minimum: no new dependencies; must work with the existing
SQLite schema; the check runs on trip creation (not as a background job).

**Anti-Goals** — Start with these, since the ask explicitly says "low priority":
what are you explicitly NOT building? Use "filter them out of reports" from the ask
as a starting point — is that in or out of scope for this first version?

**Acceptance Criteria** — Write at least four. Each must be a pass/fail statement
checkable without judgment calls. Examples to get you started:
- "A trip with more than X miles in a single day is flagged."
- "A trip where start_location equals end_location is flagged."

You need to decide on the mile threshold for "too far in one day." The ask mentions
1,400 miles as an obvious example. Make a decision and document it.

**Glossary** — Define "suspicious" precisely for this feature. The agent will not
know what your compliance team means by it — you need to make it explicit.

---

### Step 3 — Break into user stories (5 minutes)

Write two to three user stories in the format:

> As a [role], I want [action] so that [outcome].

Each story should be small enough that one Claude Code session could complete it
without context overflow. Stories that span model, routes, templates, and tests are
too big — break them down.

For each story, add:
- **Acceptance criteria** (2–3, specific to that story)
- **What to read first** (which files does Claude Code need to read before acting?)

---

### Step 4 — Write two test cases before touching code (2 minutes)

Pick your two most important acceptance criteria and write the test cases — not code,
just descriptions. For each:

- What is the setup? (What data state is required?)
- What action is taken? (What does the test do?)
- What is the expected outcome? (What should be true after?)

This is the test-plan-first discipline. When you build the feature in Hours 8–9,
these become your first pytest tests.

---

## Debrief

Be ready to share:

1. What decision did you have to make that the original ask didn't answer? How did
   you resolve it?
2. What ended up in Anti-Goals that the product owner probably assumed was in scope?
3. Is your "flag suspicious trips" feature now small enough for one Claude Code
   session, or does it still need to be broken down further?

---

## Notes

- Your output from today's exercise can go directly into a Claude Code prompt when
  you build the feature in Hour 8. Keep your draft.
- The worked version of this exercise — what the instructor demonstrated — is in
  the course's internal materials. If you want to compare your approach after the
  session, ask the instructor.
- If you finish early: go back to your acceptance criteria and ask whether each one
  is testable without running the UI. If any criterion requires a human to "look at
  the list and judge," it is not tight enough.
