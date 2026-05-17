# Homework #2 — Write a CLAUDE.md and a SKILL.md

**Assigned after:** Session 3 (Hours 5–6)
**Due before:** Session 4
**Time budget:** 30–60 minutes

---

## The Assignment

Pick a task you (or your team) do at least weekly. Then write two documents for it — using the templates from the course handouts as your starting point.

---

## What to Write

### 1. A CLAUDE.md

Write a `CLAUDE.md` for the repo or project context that task lives in.

Give Claude Code the context it needs to operate without asking you basic questions:
- What the project does and why it exists
- Stack details and key dependencies
- How to run and test it
- Conventions the AI would get wrong without being told
- What the agent must NOT do (anti-goals — the highest-value section)
- What environment variables exist and where to find them

Use the **C2 handout** (CLAUDE.md Template + Annotated Example) as your guide. The annotations explain why each section is written the way it is.

### 2. A SKILL.md

Write a `SKILL.md` describing the recurring task — in enough detail that Claude Code could execute it without further explanation.

Include:
- What the skill does (one sentence)
- Prerequisites — what must be true before the agent starts
- Inputs — what you provide before it begins
- Numbered steps — specific enough that the agent doesn't have to guess
- Verification — how you know it worked
- Common failure modes — what goes wrong and what to do about it
- Any "Do Not" constraints specific to this task

Use the **C3 handout** (SKILL.md Template + Annotated Example) as your guide.

---

## Tips

**Start with anti-goals.** The hardest thing to write is what the agent must NOT do. If you can articulate the boundary of the task — "don't touch the schema," "don't add a dependency," "don't modify anything outside this folder" — the rest of the CLAUDE.md almost writes itself.

**Start with verification.** If you're unsure how to write the SKILL.md steps, write the verification section first: "how will I know this worked?" That answer often clarifies what the steps need to be.

**Use Claude Code to help write them.** There is no rule against using the tool to draft its own operating instructions. In fact, it's good practice: you describe what you need to the agent, it drafts the document, you correct the parts it got wrong. The corrections are the most valuable part — they surface the implicit knowledge you didn't realise you had.

**The SKILL.md from the in-class exercise (Hour 5) is a valid starting point.** If you wrote one during the session, extend and refine it for this homework. You don't have to start from scratch.

---

## What to Bring to Session 4

Both documents — the CLAUDE.md and the SKILL.md. Printed or open on your laptop.

We'll look at a few in class. Bring the real ones, not polished versions — the rough edges are where the interesting discussion happens.

---

*Reference handouts: **C2** (CLAUDE.md template), **C3** (SKILL.md template). Questions? Session 4 opens with a review.*
