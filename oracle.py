#!/usr/bin/env python3
# Round Math oracle - mirrors engine.js.
import json, math

LIM = 1000000

def _v(x, msg):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < -LIM or x > LIM:
        raise ValueError(msg)
    return math.floor(x * 10000 + 0.5)

def _places(p):
    if isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p) or math.floor(p) != p or p < 0 or p > 4:
        raise ValueError("places must be a whole number from 0 to 4")
    return int(p)

def _t(v):
    neg = v < 0; a = abs(v)
    whole, frac = divmod(a, 10000)
    s = str(whole)
    if frac != 0:
        s += "." + f"{frac:04d}".rstrip("0")
    return ("-" if neg and a != 0 else "") + s

def _fixed(q, places):
    neg = q < 0; a = abs(q); k = 10 ** places
    whole, frac = divmod(a, k)
    s = str(whole)
    if places > 0:
        s += "." + str(frac).zfill(places)
    return ("-" if neg and a != 0 else "") + s

def _pl(p):
    return f"{p} place" if p == 1 else f"{p} places"

def _rules(v, p):
    k = 10 ** (4 - p)
    fl, r = divmod(v, k)
    ce = fl if r == 0 else fl + 1
    tz = fl if v >= 0 else ce
    if 2 * r > k:
        away = even = ce
    elif 2 * r < k:
        away = even = fl
    else:
        away = ce if v > 0 else fl
        even = fl if fl % 2 == 0 else ce
    return {"away": away, "even": even, "zero": tz, "down": fl, "up": ce}

def rule_truth(value, places):
    v = _v(value, "value must be between -1000000 and 1000000")
    p = _places(places)
    r = _rules(v, p)
    return (f"{_t(v)} to {_pl(p)}: half away from zero {_fixed(r['away'], p)}, half to even {_fixed(r['even'], p)}, "
            f"toward zero {_fixed(r['zero'], p)}, down {_fixed(r['down'], p)}, up {_fixed(r['up'], p)}.")

def sum_truth(lst, places):
    if not isinstance(lst, list) or len(lst) < 2 or len(lst) > 20:
        raise ValueError("need 2 to 20 numbers")
    vs = [_v(x, "each number must be between -1000000 and 1000000") for x in lst]
    p = _places(places)
    each = sum(_rules(v, p)["away"] for v in vs)
    total = sum(vs)
    once = _rules(total, p)["away"]
    head = f"Rounding each of {len(vs)} numbers to {_pl(p)} and adding gives {_fixed(each, p)}; adding first and rounding gives {_fixed(once, p)}. "
    if each == once:
        return head + "Both ways agree."
    return head + f"They differ by {_fixed(abs(each - once), p)}."

def step_truth(value, step):
    v = _v(value, "value must be between -1000000 and 1000000")
    if isinstance(step, bool) or not isinstance(step, (int, float)) or not math.isfinite(step) or step < 0.0001 or step > LIM:
        raise ValueError("step must be between 0.0001 and 1000000")
    s = math.floor(step * 10000 + 0.5)
    fl, r = divmod(v, s)
    fl = fl * s
    if 2 * r > s:
        out = fl + s
    elif 2 * r < s:
        out = fl
    else:
        out = fl + s if v > 0 else fl
    move = out - v
    head = f"Nearest {_t(s)} to {_t(v)}: {_t(out)}"
    if move == 0:
        return head + " (already on a step)."
    return head + f" ({'up ' if move > 0 else 'down '}{_t(abs(move))})."

FNS = {"ruleTruth": rule_truth, "sumTruth": sum_truth, "stepTruth": step_truth}

CASES = [
    ("ruleTruth", [2.5, 0]), ("ruleTruth", [3.5, 0]), ("ruleTruth", [-2.5, 0]), ("ruleTruth", [-3.5, 0]), ("ruleTruth", [2.4, 0]),
    ("ruleTruth", [2.6, 0]), ("ruleTruth", [-2.4, 0]), ("ruleTruth", [-2.6, 0]), ("ruleTruth", [0, 0]), ("ruleTruth", [3, 0]),
    ("ruleTruth", [2.345, 2]), ("ruleTruth", [2.355, 2]), ("ruleTruth", [-2.345, 2]), ("ruleTruth", [0.5, 0]), ("ruleTruth", [-0.5, 0]),
    ("ruleTruth", [1.25, 1]), ("ruleTruth", [1.35, 1]), ("ruleTruth", [1.2345, 4]), ("ruleTruth", [1000000, 2]), ("ruleTruth", [-1000000, 0]),
    ("ruleTruth", [0.00005, 4]), ("ruleTruth", [-0.3, 0]), ("ruleTruth", [1000001, 0]), ("ruleTruth", [1, 5]), ("ruleTruth", [1, 1.5]), ("ruleTruth", [1, -1]),
    ("sumTruth", [[1.4, 1.4, 1.4], 0]), ("sumTruth", [[1.5, 1.5], 0]), ("sumTruth", [[0.5, 0.5, 0.5], 0]), ("sumTruth", [[2.25, 2.25, 2.25, 2.25], 1]),
    ("sumTruth", [[1.1, 2.2], 0]), ("sumTruth", [[-1.5, -1.5], 0]), ("sumTruth", [[1.004, 1.004, 1.004], 2]), ("sumTruth", [[1], 0]),
    ("sumTruth", [[1] * 21, 0]), ("sumTruth", [[1, 1000001], 0]), ("sumTruth", [[1, 2], 5]), ("sumTruth", [[0.6, 0.6, 0.6, 0.6, 0.6], 0]),
    ("stepTruth", [7.3, 0.5]), ("stepTruth", [7.25, 0.5]), ("stepTruth", [7.5, 0.5]), ("stepTruth", [-7.25, 0.5]), ("stepTruth", [12, 5]),
    ("stepTruth", [13, 5]), ("stepTruth", [12.5, 5]), ("stepTruth", [-12.5, 5]), ("stepTruth", [0, 5]), ("stepTruth", [2.49, 0.05]),
    ("stepTruth", [0.0001, 0.0001]), ("stepTruth", [1000000, 1000000]), ("stepTruth", [7, 0]), ("stepTruth", [7, 0.00001]),
    ("stepTruth", [7, 1000001]), ("stepTruth", [1000001, 5]), ("stepTruth", [999999.99, 25]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
