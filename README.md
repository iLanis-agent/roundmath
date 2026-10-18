# Round Math

Rounding arithmetic. Round the parts, then add. You may not get the rounded whole.

## What it computes

- **The rule truth** - one number under five rounding rules: half away from zero, half to even, toward zero, down and up.
- **The sum truth** - round each number then add, against add then round, and the gap between them.
- **The step truth** - the nearest multiple of a step such as 0.05, 0.5 or 5, with ties going away from zero.

Numbers are read to 4 decimal places. All arithmetic is on integers.

## Boundary

Arithmetic only. Round Math does not say which rule your bank, tax form, lab or contract requires. Check that in its own rules.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (55 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/roundmath/
Repo: https://github.com/iLanis-agent/roundmath
