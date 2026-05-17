# D2 — In-Class Exercise: Rewrite a Vague Ask as an AI-Ready Spec

iGEN Developer AI Training · Session 1 (Hour 2)

> **[Needs Tech Review]** — the source ask below should be verified with the lead instructor for iGEN realism before this sheet is distributed. Confirm that the filing-system details, anomaly types, and data access pattern are accurate to iGEN's environment.

---

## What You're Doing

You have a vague stakeholder ask — the kind that lands in a ticket or a Slack message. Your job is to rewrite it as an AI-ready spec using the C7 template, so that Claude Code could execute it reliably without back-and-forth.

Time: 15 minutes to draft; 5 minutes to share one section with the room.

---

## The Vague Ask

> "We need a script that pulls last quarter's fuel tax filings and flags anything that looks off. Probably want it in Python. Should be pretty easy — we can just eyeball the output."

That's it. That's all you got.

---

## Your Task

Open `handouts/C7-ai-ready-spec-template.md` (or your printed copy). Work through each section of the template for this ask.

A few sections to pay special attention to:

- **Constraints** — "pretty easy" and "eyeball the output" are doing a lot of work. What format should the output actually be in? What counts as "last quarter"? Where does the data come from?
- **Anti-Goals** — resist the urge to build everything. What scope is explicitly out of scope for a first script?
- **Acceptance Criteria** — write at least three statements that are checkable without judgment calls. Avoid criteria like "output looks reasonable."
- **Glossary** — "anomaly" means something specific in fuel-tax context. Define it for the agent.

You don't need to produce working code. You're producing a spec that you would hand to Claude Code.

---

## Debrief Prompts

When the room reconvenes, be ready to share:

1. What section was hardest to fill in, and why?
2. What did you have to decide that the original ask left ambiguous?
3. If you had handed the original ask to Claude Code as-is, what do you think it would have produced?

---

## Notes for the Instructor

This exercise pairs with the vague-vs-AI-ready contrast demo in Hour 3. If time allows, the instructor can take one attendee's spec and run it live against the vague version to show the difference in output.

The before/after example in C7 (flagging suspicious trips) is a different domain — it's a web-app feature. This exercise is a standalone script task so attendees practice the template on something that isn't the course's worked example.
