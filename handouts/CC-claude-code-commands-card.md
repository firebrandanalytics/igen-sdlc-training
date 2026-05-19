# Claude Code Commands — Muscle-Memory Card

iGEN Developer AI Training · Instructor request — highest-frequency commands only

These are the ~15–20 commands and features you'll reach for every day. Not exhaustive — just the ones worth memorising. Verify the current Claude Code version for exact syntax.

---

## Starting a Session

| What you want | How to do it |
|--------------|-------------|
| Start Claude Code in the current directory | `claude` |
| Start with a specific model | `claude --model claude-haiku-4-5` |
| Start in planning mode (plan before executing) | `claude --permission-mode plan` |
| Resume the previous session | `claude --continue` |

---

## During a Session — Slash Commands

Type these at the Claude Code prompt (the `>` line).

| Command | What it does |
|---------|-------------|
| `/help` | List available slash commands |
| `/plan` | Ask Claude to write a plan for what it's about to do, and pause for your approval before executing anything |
| `/compact` | Summarise and compress the conversation context. Use before context fills up and quality degrades. Does NOT start a new conversation — history is summarised, not cleared. |
| `/clear` | Clear the conversation entirely and start fresh. Use when you are done with a task and starting something unrelated, or when the context has drifted far from the current task. |
| `/status` | Show current session info — model, context usage, approval mode |
| `/model <name>` | Switch the model mid-session |

---

## Approval Mode

| What you want | How to do it |
|--------------|-------------|
| Switch approval mode | Press `Shift+Tab` to cycle through the modes |
| See the current mode | Shown in the input box as you work |

> **Quick discipline:** start a new codebase in manual mode. Switch to Auto Mode once you've seen a few actions and trust the direction.

---

## Asking Claude to Explain Before Approving

You don't need a special command for this — just ask before approving:

```
What will this change do to the existing test for delete_trip?
```

```
Show me what the diff will look like before you write it.
```

```
Before you make any changes: what files will you touch, and why?
```

The agent answers before acting. Make it a habit on any change that touches more than one file.

---

## Context Management — When to Use Which

| Situation | Right move |
|-----------|-----------|
| Context is filling up but you're mid-task | `/compact` — preserves the task, compresses history |
| Task is complete; starting something unrelated | `/clear` — start fresh |
| New day, new task, unclear what's in context | Start a new `claude` session entirely |
| Context has drifted (agent is giving stale answers) | `/clear` and re-state the task cleanly |

> **Rule of thumb:** if you feel like you're fighting the context to get a good answer, clear it. The re-statement cost is lower than the compounding cost of a confused agent.

---

## Referencing Files

Claude Code can read files directly — you don't need to paste content.

```
Read main.py and tell me where the delete endpoint should go.
```

```
Before you start, read CLAUDE.md, db.py, and service.py.
```

```
Look at the failing test in tests/test_routes.py and fix what's failing.
```

> **Tip:** Tell the agent which files to read *before* it writes anything. Saves a round-trip of "I assumed the schema was X but it's actually Y."

---

## Useful One-Liners

```bash
# Ask Claude Code to explain a change before you approve it
# (just type this at the > prompt, mid-session)
What exactly will you change, and why? Show me the file paths and the lines affected.

# Planning mode — ask for a plan first
Plan the implementation of [feature] before you write any code.
List the files you'll touch and the order you'll work in.

# Asking for a review pass
Read the diff in [file] and tell me if anything looks wrong before I commit.

# Anchoring scope (mileage-logbook example)
Only modify db.py and tests/test_db.py. Do not touch main.py or service.py yet.
```

---

## Things Worth Knowing

- **Claude Code inherits your shell's environment.** Variables you export in your shell (or load from `.env`) are available to the commands the agent runs.
- **Conversation history is not saved between separate `claude` invocations** (unless you use `--continue`). If you close the terminal, the context is gone.
- **The agent sees your working directory.** It reads files relative to where you started `claude`. Start from the repo root.
- **Long outputs get truncated in display** but the agent received the full content. If you want to see the full output, ask the agent to write it to a file.