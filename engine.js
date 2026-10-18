// Round Math engine - five rounding rules side by side, the sum-of-roundings trap, and rounding to a step.
// Mirrored by oracle.py; keep the op order identical.
// Inputs are read to 4 decimal places (units of 0.0001); all arithmetic is on integers.

var LIM = 1000000;

function _v(x, msg) {
  if (typeof x !== "number" || !isFinite(x) || x < -LIM || x > LIM) throw new Error(msg);
  return Math.floor(x * 10000 + 0.5);
}

function _places(p) {
  if (typeof p !== "number" || !isFinite(p) || Math.floor(p) !== p || p < 0 || p > 4) throw new Error("places must be a whole number from 0 to 4");
  return p;
}

// Trimmed decimal text for a value in units of 0.0001.
function _t(v) {
  var neg = v < 0, a = Math.abs(v);
  var whole = Math.floor(a / 10000), frac = a % 10000;
  var s = String(whole);
  if (frac !== 0) {
    var f = String(frac);
    while (f.length < 4) f = "0" + f;
    while (f.charAt(f.length - 1) === "0") f = f.slice(0, -1);
    s += "." + f;
  }
  return (neg && a !== 0 ? "-" : "") + s;
}

// Fixed decimals for a value in units of 10^-places.
function _fixed(q, places) {
  var neg = q < 0, a = Math.abs(q), k = Math.pow(10, places);
  var whole = Math.floor(a / k), frac = a % k;
  var s = String(whole);
  if (places > 0) {
    var f = String(frac);
    while (f.length < places) f = "0" + f;
    s += "." + f;
  }
  return (neg && a !== 0 ? "-" : "") + s;
}

function _pl(p) {
  return p + (p === 1 ? " place" : " places");
}

// Floor and remainder of v over k, for any sign of v.
function _fl(v, k) {
  var r = ((v % k) + k) % k;
  return { fl: (v - r) / k, r: r };
}

function _rules(v, p) {
  var k = Math.pow(10, 4 - p);
  var d = _fl(v, k), fl = d.fl, r = d.r;
  var ce = r === 0 ? fl : fl + 1;
  var tz = v >= 0 ? fl : ce;
  var away, even;
  if (2 * r > k) { away = ce; even = ce; }
  else if (2 * r < k) { away = fl; even = fl; }
  else { away = v > 0 ? ce : fl; even = fl % 2 === 0 ? fl : ce; }
  return { away: away, even: even, zero: tz, down: fl, up: ce };
}

// The rule truth: one number, five rounding rules.
function ruleTruth(value, places) {
  var v = _v(value, "value must be between -1000000 and 1000000");
  var p = _places(places);
  var r = _rules(v, p);
  return _t(v) + " to " + _pl(p) + ": half away from zero " + _fixed(r.away, p) + ", half to even " + _fixed(r.even, p) +
    ", toward zero " + _fixed(r.zero, p) + ", down " + _fixed(r.down, p) + ", up " + _fixed(r.up, p) + ".";
}

// The sum truth: round each number then add, against add then round.
function sumTruth(list, places) {
  if (!Array.isArray(list) || list.length < 2 || list.length > 20) throw new Error("need 2 to 20 numbers");
  var vs = [];
  for (var i = 0; i < list.length; i++) vs.push(_v(list[i], "each number must be between -1000000 and 1000000"));
  var p = _places(places);
  var each = 0, total = 0;
  for (i = 0; i < vs.length; i++) { each += _rules(vs[i], p).away; total += vs[i]; }
  var once = _rules(total, p).away;
  var head = "Rounding each of " + vs.length + " numbers to " + _pl(p) + " and adding gives " + _fixed(each, p) + "; adding first and rounding gives " + _fixed(once, p) + ". ";
  if (each === once) return head + "Both ways agree.";
  return head + "They differ by " + _fixed(Math.abs(each - once), p) + ".";
}

// The step truth: the nearest multiple of a step, ties away from zero.
function stepTruth(value, step) {
  var v = _v(value, "value must be between -1000000 and 1000000");
  if (typeof step !== "number" || !isFinite(step) || step < 0.0001 || step > LIM) throw new Error("step must be between 0.0001 and 1000000");
  var s = Math.floor(step * 10000 + 0.5);
  var r = ((v % s) + s) % s, fl = v - r, out;
  if (2 * r > s) out = fl + s;
  else if (2 * r < s) out = fl;
  else out = v > 0 ? fl + s : fl;
  var move = out - v;
  var head = "Nearest " + _t(s) + " to " + _t(v) + ": " + _t(out);
  if (move === 0) return head + " (already on a step).";
  return head + " (" + (move > 0 ? "up " : "down ") + _t(Math.abs(move)) + ").";
}
