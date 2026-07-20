'use strict';
// REVIEWER-AUTHORED RED TEST — owned by skill 05 (reviewer), NOT by 04.
// REQ-008 / VC-02: "each member's entry grouped under their display name."
// This reproduces the grouping defect: it is RED against the defective impl (only the first member is grouped).
// 04's fix pass must make it GREEN by fixing src/digest.js — and must NOT edit this file (the anti-circular rule:
// the fixer may not author or alter the oracle it is being graded against).
const test = require('node:test');
const assert = require('node:assert');
const { assembleDigest } = require('../../src/digest.js');

test('REQ-008 / VC-02: every member with a standup appears once, grouped under their name', () => {
  const entries = [
    { member: 'ada', day: '2026-07-01', update: 'shipped digest' },
    { member: 'linus', day: '2026-07-01', update: 'reviewed PRs' },
    { member: 'grace', day: '2026-07-01', update: 'wrote tests' },
  ];
  const digest = assembleDigest(entries, '2026-07-01');
  const names = digest.members.map((m) => m.member).sort();
  assert.deepStrictEqual(
    names,
    ['ada', 'grace', 'linus'],
    'assembleDigest must group ALL members under their display name, not just the first',
  );
});
