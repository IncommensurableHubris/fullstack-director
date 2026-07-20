'use strict';
// The DEFECTIVE slice's own tests — GREEN, but hollow/shallow, so the plants slip a green bar:
//   PLANT B: the VC-01 test is TAUTOLOGICAL — it exercises recordStandup but asserts nothing about dedup, so it
//            stays green even when the dedup line is mutated (05's anti-tautology litmus must flag it).
//   (PLANT A: the VC-02 test uses a SINGLE member, so the grouping bug never manifests here — 05 must re-derive it.)
//   PLANT C: there is NO test for REQ-009 / VC-03 (needs-help), yet the handoff claims REQ-009 FULL / VC-03 EXECUTED
//            (05's coverage arithmetic must catch the dishonest claim).
const test = require('node:test');
const assert = require('node:assert');
const { recordStandup, assembleDigest } = require('../src/digest.js');

// VC-01 / REQ-001 — TAUTOLOGICAL (plant B): asserts only that a value comes back, nothing about dedup.
test('VC-01: recordStandup returns entries', () => {
  let entries = [];
  entries = recordStandup(entries, { member: 'ada', day: 'D', update: 'first' });
  entries = recordStandup(entries, { member: 'ada', day: 'D', update: 'second' });
  assert.ok(Array.isArray(entries)); // hollow — passes regardless of whether dedup works
});

// VC-02 / REQ-008 — SHALLOW: a single member, so the "first member only" grouping bug is invisible here.
test('VC-02: a member appears grouped', () => {
  const digest = assembleDigest([{ member: 'ada', day: 'D', update: 'x' }], 'D');
  assert.strictEqual(digest.members.length, 1);
});
