'use strict';
// patch-001 regression (TDD-for-bugs): a standup submitted exactly at the lock minute is included (REQ-008).
// Observed RED against the pre-patch impl (the strict `<` dropped the at-lock member), green after the fix.
const test = require('node:test');
const assert = require('node:assert');
const { assembleDigest } = require('../src/digest.js');

test('patch-001 REQ-008: an at-lock submission is included in the digest', () => {
  const entries = [
    { member: 'ada', day: '2026-07-01', submittedMinute: 1020, update: 'at the wire' },
    { member: 'bo', day: '2026-07-01', submittedMinute: 600, update: 'early' },
  ];
  const digest = assembleDigest(entries, '2026-07-01', 1020);
  assert.deepStrictEqual(digest.members.map((m) => m.member).sort(), ['ada', 'bo']);
});
