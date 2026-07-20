'use strict';
// Real, non-tautological oracles for VC-01/02/03. Each would go RED under a single-point mutation of the behavior
// it guards — the CLEAN slice's tests actually verify the contract, so 05 can honestly reach SHIP.
const test = require('node:test');
const assert = require('node:assert');
const { recordStandup, assembleDigest } = require('../src/digest.js');

// VC-01 / REQ-001 — dedup: a second standup for the same member+day replaces the first.
test('VC-01: recording twice for the same member+day leaves one entry, latest answers', () => {
  let entries = [];
  entries = recordStandup(entries, { member: 'ada', day: 'D', update: 'first' });
  entries = recordStandup(entries, { member: 'ada', day: 'D', update: 'second' });
  const forDay = entries.filter((e) => e.member === 'ada' && e.day === 'D');
  assert.strictEqual(forDay.length, 1);
  assert.strictEqual(forDay[0].update, 'second');
});

// VC-02 / REQ-008 — group EVERY member (multi-member catches a "first only" break).
test('VC-02: assembleDigest groups every member under their display name', () => {
  const entries = [
    { member: 'ada', day: 'D', update: 'shipped digest' },
    { member: 'linus', day: 'D', update: 'reviewed PRs' },
  ];
  const digest = assembleDigest(entries, 'D');
  const names = digest.members.map((m) => m.member).sort();
  assert.deepStrictEqual(names, ['ada', 'linus']);
});

// VC-03 / REQ-009 — needs-help blockers collected together at the top.
test('VC-03: needs-help blockers are collected into the top section', () => {
  const entries = [
    { member: 'ada', day: 'D', update: 'x', needsHelp: true, blocker: 'ci is red' },
    { member: 'linus', day: 'D', update: 'y' },
  ];
  const digest = assembleDigest(entries, 'D');
  assert.strictEqual(digest.needsHelp.length, 1);
  assert.strictEqual(digest.needsHelp[0].blocker, 'ci is red');
});
