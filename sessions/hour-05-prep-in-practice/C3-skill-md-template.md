> **[Needs Tech Review]** — verify with lead instructor before use.

# C3 — SKILL.md Template + Annotated Example

iGEN Developer AI Training · Session 3 (Hour 5) reference

A `SKILL.md` file documents a recurring procedure in enough detail that Claude Code can execute it without further explanation. Unlike `CLAUDE.md` (which describes the *project*), a `SKILL.md` describes a *task* — the prerequisites, decision points, what done looks like, and common failure modes.

---

## When to Write a SKILL.md

Write one when:
- You (or your team) perform the same multi-step procedure at least weekly.
- The procedure has decision points that require judgment or context the AI wouldn't have from source code alone.
- You are tired of re-explaining the same setup steps at the start of every session.

**Rule of thumb:** if you've typed the same instructions to Claude Code twice, make it a SKILL.md.

---

## Single File vs. Folder

| Situation | Format |
|-----------|--------|
| Procedure fits in ~300 lines or fewer | Single `SKILL.md` file inside a named folder |
| Procedure ships with a helper script or data file | Folder: `.claude/skills/<name>/` with `SKILL.md` + the helper files |
| Multiple related procedures | Separate named folders under `.claude/skills/` |

**Folder example — the real `add-jurisdiction` skill:**

```
.claude/skills/
  add-jurisdiction/
    SKILL.md              steps and invocation instructions
    add_jurisdiction.py   CLI helper script (validates inputs, writes to DB)
```

> The agent reads `SKILL.md` first, then runs `add_jurisdiction.py` as directed.
> Keeping the helper script in the same folder as `SKILL.md` means the relative
> path in the instructions always resolves correctly regardless of working directory.

---

## Blank Template

```markdown
# SKILL — <Skill Name>

## Purpose
<!-- One sentence: what this skill does and why it exists. -->

## Prerequisites
<!-- What must be true before the agent starts.
     Examples: venv active, .env loaded, Docker daemon running, user has write access. -->

## Inputs
<!-- What the agent needs from you before it can begin.
     Examples: a branch name, a JIRA ticket number, an environment name. -->

## Steps
<!-- Numbered steps. Be specific enough that the agent doesn't have to guess.
     For steps with decision points, use sub-bullets:
       - If <condition>, do X.
       - Otherwise, do Y.
     For steps that require a command, write the exact command (or the template). -->

1. ...
2. ...
3. ...

## Verification
<!-- How the agent (and you) know the skill completed successfully.
     Examples: test suite passes, endpoint returns 200, log line appears. -->

## Common Failure Modes
<!-- What goes wrong and what to do about it. -->

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| ... | ... | ... |

## Do Not
<!-- Constraints specific to this skill — things that look tempting but are wrong here. -->

## Notes / Background
<!-- Optional. Domain context that the agent needs but can't infer.
     Keep this section short; link to external docs rather than reproducing them. -->
```

---

## Annotated Example — Add a Jurisdiction and Rate

Below is a filled-in `SKILL.md` for the "add a jurisdiction" task from the mileage-logbook app. Margin notes explain the intent of each section.

---

```markdown
# Skill: add-jurisdiction
```
> **Annotation — Title:** Use the same name as the folder (`.claude/skills/add-jurisdiction/`).
> Claude Code uses the folder name as the slash-command name, so they must match.

---

```markdown
## What this skill does

Adds or updates a jurisdiction (US state) and its IFTA tax rate in the
`jurisdictions` table of the Mileage Logbook SQLite database.
```
> **Annotation — What this skill does:** One clear paragraph defining scope.
> Prevents the agent from going further than intended — e.g., it won't start
> regenerating seed data or redesigning the schema if it knows the scope is a
> single upsert.

---

The real skill also documents *why* automation helps here — these details give
the agent the judgment to handle edge cases:

```markdown
This is a repetitive, error-prone task that benefits from automation:
- The state code must be upper-cased exactly.
- The rate is a decimal (cents per gallon), not a percentage.
- The table uses an upsert — safe to run again to correct a rate.
```

---

```markdown
## Steps

1. **Validate arguments** — confirm `state_code` is 2 characters,
   `tax_rate` is a non-negative number.

2. **Run the helper script**:

   ```bash
   python .claude/skills/add-jurisdiction/add_jurisdiction.py \
       --state-code "$state_code" \
       --state-name "$state_name" \
       --tax-rate "$tax_rate"
   ```

   The script exits 0 on success and prints a confirmation line.
   Exit non-zero means a validation or database error — surface the message.

3. **Verify** — query the database to confirm the row exists:

   ```bash
   python -c "
   import sqlite3, os
   db_path = os.environ.get('DB_PATH', 'logbook.db')
   conn = sqlite3.connect(db_path)
   conn.row_factory = sqlite3.Row
   row = conn.execute('SELECT * FROM jurisdictions WHERE state_code = ?',
                      ('$state_code'.upper(),)).fetchone()
   if row:
       print(f'Confirmed: {row[\"state_code\"]} — {row[\"state_name\"]} @ {row[\"tax_rate\"]} c/gal')
   else:
       print('ERROR: row not found after insert')
       exit(1)
   conn.close()
   "
   ```

4. **Report** — tell the user the state code, name, and rate that were saved.
```
> **Annotation — Steps:** Number every step. The skill delegates to a helper
> script (`add_jurisdiction.py`) rather than running SQL directly — this keeps
> validation logic in one place (the Python file) and makes the skill easy to
> test in isolation. The verify step queries the live database rather than
> trusting the script's return value, which catches silent database errors.

---

```markdown
## Example invocation

/add-jurisdiction TX Texas 0.200
```
> **Annotation — Example:** Show the exact slash-command form. The three
> positional values map to `state_code`, `state_name`, and `tax_rate` declared
> in the YAML front-matter at the top of the SKILL.md file.

---

```markdown
## Notes

- Requires the virtual environment to be active (`source venv/Scripts/activate`
  on Windows Git Bash, or `source venv/bin/activate` on macOS/Linux).
- The default database path is `logbook.db` in the project root.
  Override with the `DB_PATH` environment variable.
- Tax rates are IFTA illustrative values — verify current official rates
  before using in a production filing.
```
> **Annotation — Notes:** Domain context the agent can't infer from code.
> The venv note matters because the helper script imports `db.py`, which must
> be importable; mentioning `DB_PATH` lets the agent handle non-default setups
> (CI, Docker) without guessing.

---

<!-- VERIFY: confirm that the SKILL.md folder format (index.md + sub-files) is supported by the current Claude Code version and that sub-files are followed as linked references -->
<!-- VERIFY: confirm the ~300-line threshold for single-file vs. folder is the heuristic the lead instructor wants to teach -->
