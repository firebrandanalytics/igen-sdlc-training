# Optional — Try Planning Mode Yourself

iGEN Developer AI Training · Hour 3 · *Optional — only if the instructor runs the contingency demo and time allows*

Hour 3 has no required exercise. But if there's time, here's a five-minute way
to feel planning mode for yourself.

## The task

Open Claude Code with Haiku, in plan mode:

```
claude --model claude-haiku-4-5 --permission-mode plan
```

Paste this prompt:

> Write a small Python tool to help me work out trip costs.

## What to do

1. **Don't accept the plan yet — read it.** The ask is deliberately vague, so
   the plan will surface decisions you never made: which units? does it need
   fuel economy and a fuel price as inputs, or should it assume them? one trip
   or many? how should it round?
2. **Narrow it.** Tell Claude Code the scope you actually want — for example,
   "just one trip; take the distance, fuel economy, and price-per-gallon as
   command-line arguments; print the total cost."
3. **Then `proceed`** — let Haiku build it.

## The point

You wrote one vague sentence, and the plan handed back several decisions —
before any code existed. That checkpoint, catching and correcting scope for
free, is what planning mode buys you. Hour 4 puts it to work on real code.
