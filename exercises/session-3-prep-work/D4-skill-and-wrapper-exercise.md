# D4 — In-Class Exercise: Write a SKILL.md and a Wrapper Script

iGEN Developer AI Training · Session 3 (Hour 5)

> **[Needs Tech Review]** — verify SKILL.md folder format and slash-command invocation against the deployed Claude Code version before distributing; confirm the ~300-line threshold for single-file vs. folder is the rule you want to teach; confirm that bash functions sourced in Git Bash work as expected on attendee machines.

---

## What You're Doing

You've seen the annotated examples — a CLAUDE.md that documents project conventions, a SKILL.md that turns a recurring procedure into a slash command, and wrapper scripts that enforce the "Make Correctness Easy" principle.

Now you build your own versions.

**Time:** 20–25 minutes.

---

## Part 1 — Write a SKILL.md (12 minutes)

Pick one recurring task from your own work — something you do at least weekly and have explained to a colleague or to the AI more than once. It does not have to be complex; a short, precise SKILL.md is more useful than a long vague one.

**Examples to get you started:**

- Run the weekly export, validate the output file, and email the summary
- Reset a test database to a known state
- Pull the latest config from a shared repo and apply it locally
- Kick off a specific query, format the result, and drop it into a spreadsheet
- Run the linter and auto-fixer, check the diff, and commit

Create a folder called `.claude/skills/<your-task-name>/` in your project (or wherever makes sense). Inside it, create a `SKILL.md` using the **C3 handout** (SKILL.md Template + Annotated Example) as your structure.

Your SKILL.md must include at least:

| Section | What to write |
|---------|--------------|
| **What this skill does** | One sentence — scope and purpose |
| **Prerequisites** | What must be true before the agent starts (venv active, config loaded, etc.) |
| **Steps** | Numbered steps specific enough that the agent doesn't have to guess; include the exact command or command template for each step that runs something |
| **Verification** | How you (and the agent) know the skill completed successfully |
| **Do Not** | At least one constraint — something that looks tempting but is wrong for this task |

The verify step is the most commonly skipped section — write it. If you don't know how to verify, write "I don't know yet" and that becomes the first thing you refine.

**Single file vs. folder:** if your skill only needs the SKILL.md (no companion script or data file), one file inside a named folder is all you need. If it needs a helper script alongside it, put both in the same folder. The folder name becomes the slash-command name — keep it short and lowercase, hyphenated.

---

## Part 2 — Build One Wrapper Script (8 minutes)

Pick the most repetitive shell command in your daily workflow — the one you have to look up, or the one you get wrong when you type it fast.

Write a wrapper for it. Choose the simplest format:

- **Bash function** in a `.sh` file you can `source` in Git Bash or your terminal
- **Bash alias** you can add to your `.bashrc` or `.bash_profile`
- **Tiny Python CLI** (a `main()` function with `argparse`, a few lines, no new dependencies)

The wrapper should do one thing well: hide flags you always forget, enforce a convention, or give a long command a short name. It does not need to be impressive. A five-line bash function that prevents one class of mistakes is a complete wrapper.

**What to aim for:**

```bash
# Before: you have to remember this every time
curl -s -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $API_TOKEN" \
     "$BASE_URL/reports/generate" \
     -d "{\"period\": \"$1\", \"format\": \"csv\"}"

# After: one name, arguments only
generate-report 2024-Q1
```

Write the function in a `.sh` file. Add a one-line comment at the top explaining what it enforces or prevents. That comment is also documentation for the agent — put it in your CLAUDE.md's Recurring Tasks section if you want the agent to use it.

**Git Bash note:** bash functions defined in a `.sh` file work on Git Bash (Windows) when you `source` the file. You do not need WSL. `source scripts/my-helpers.sh` is enough.

---

## After the Exercise

**Keep your SKILL.md draft.** It is the starting point for Homework #2 (D9). The homework asks you to refine it — add the missing steps, complete the verification section, and write a matching CLAUDE.md for the repo it lives in. You do not have to start from scratch; the rough draft you have now is the work.

**Keep your wrapper too.** In Hours 8–9, you will source the course's shell helpers (`examples/shell/logbook-api.sh`, `git-helpers.sh`) during the web-app build. The same pattern applies to your own project.

---

## Quick Troubleshooting

**Can't decide which task to document:** pick the last thing you had to re-explain at the start of an AI session. That's your task.

**SKILL.md steps are too vague:** ask yourself — "If Claude Code read this cold, would it know the exact command to run in Step 2?" If not, add the command.

**Wrapper is getting complex:** make it do one thing. Add more later. The goal is to finish Part 2 with time to spare.

**Not sure which format (bash function vs. Python CLI):** bash function if it's a shell workflow; Python CLI if it validates arguments or does more than call one command. When in doubt, bash.
