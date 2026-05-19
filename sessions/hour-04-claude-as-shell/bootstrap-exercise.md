# In-Class Exercise: Bootstrap a Python Project Through Claude Code

iGEN Developer AI Training · Session 2 (Hour 4)

> **[Needs Tech Review]** — verify the expected project structure, venv activation commands, and test invocation against the distributed environment (Git Bash on Windows + Python 3 in PATH) before this sheet is distributed. Confirm that the grading check (`python -m pytest`) works out-of-the-box on attendee machines.

---

## What You're Doing

You're going to build a small, empty Python project — from nothing — by directing Claude Code. The domain doesn't matter. The point is to practice using Claude Code as your shell: issuing clear instructions, reviewing what it produces, and steering when it goes off course.

Time: 20–25 minutes.

---

## The Goal

By the end, your project directory should contain all of the following. This is the pass/fail checklist — either it's all there and the project runs, or it isn't.

| Item | What it looks like |
|------|--------------------|
| Virtual environment | A `venv/` folder at the project root, created and activated |
| Project structure | At minimum: a package directory (your choice of name) with an `__init__.py`, and a `tests/` directory |
| `.gitignore` | Covers at least `venv/`, `__pycache__/`, and `*.pyc` |
| `README.md` | At minimum: project name, one-sentence description, how to create the venv, how to run the tests |
| `requirements.txt` | Exists; includes `pytest`; any other dependencies your stub needs |
| Git repo | `git init` has been run; at least one commit exists |
| One stub module | A Python file inside your package with at least one function (the function can just `pass` or `return None`) |
| One stub test | A test file in `tests/` that imports and calls your stub function; the test passes |

**Binary grading:** run `python -m pytest tests/ -v` from the project root. If it passes with no errors, you're done.

---

## How to Approach This

The constraint: **direct Claude Code to do the work.** Don't type the mkdir commands yourself. Don't write the files yourself. Use Claude Code — give it an instruction, review what it produces, correct it if needed, move to the next step.

### Suggested sequence

1. Tell Claude Code you want to bootstrap a new Python project. Give it a name and a one-sentence description (make something up — the domain doesn't matter).
2. Ask it to create the project structure, venv, and install pytest.
3. Ask it to write a stub module with one function.
4. Ask it to write a stub test for that function.
5. Ask it to create a `.gitignore` appropriate for a Python project.
6. Ask it to write a README with setup and test instructions.
7. Ask it to initialise a git repo and make an initial commit.
8. Run `python -m pytest tests/ -v`. If it fails, tell Claude Code what failed and ask it to fix it.

### A few things to notice while you work

- **What happens when your instruction is ambiguous.** If Claude Code does something unexpected, look at what you asked — can you see why it made that choice?
- **What planning mode does.** Before a complex step, try asking Claude Code to plan before it acts. Notice whether the plan matches what you intended.
- **Review before you accept.** Before each file gets written, glance at it. If something looks wrong, say so. This is the review discipline you'll use for every task in the course.

---

## Quick Troubleshooting

**`python` not found:** try `python3`. If neither works, flag it — the environment setup may need attention.

**venv activation on Windows (Git Bash):** `source venv/Scripts/activate`

**venv activation on macOS/Linux:** `source venv/bin/activate`

**`pytest` not found after installing:** make sure the venv is activated before running pytest.

**Import error in the test:** the test file's import path needs to match the package structure. Ask Claude Code to check the import.

---

## After the Exercise

Keep this project. You'll reference it in Homework #1 if you choose to use it as your "real task" target. The CLAUDE.md you write in Hour 5 could go here too.
