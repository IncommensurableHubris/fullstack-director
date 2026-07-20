'use strict';
// Reviewer-authored reproducing RED test (05 owns RED, 04 owns GREEN — 04 may not edit this file).
// FAILS against the current implementation: assembleDigest keeps only the FIRST member's entry (REQ-008 / VC-02).
const test = require('node:test');
const assert = require('node:assert');
const { assembleDigest } = require('../../src/digest.js');

test('REQ-008: assembleDigest groups EVERY member under their display name (reviewer RED)', () => {
  const entries = [
    { member: 'ada', day: 'D', update: 'shipped digest' },
    { member: 'linus', day: 'D', update: 'reviewed PRs' },
  ];
  const digest = assembleDigest(entries, 'D');
  const names = digest.members.map((m) => m.member).sort();
  assert.deepStrictEqual(names, ['ada', 'linus']);
});
