'use strict';
// The build's own tests (happy-path). All green against the defective impl — the REQ-008 test uses a SINGLE member,
// so the grouping bug never manifests here. This is the realistic seam: a shallow happy-path test lets a real bug
// slip past a green bar, which is why 05's reproducing RED test (test/review/) is the oracle 04 must satisfy.
const test = require('node:test');
const assert = require('node:assert');
const { recordStandup, assembleDigest } = require('../src/digest.js');

test('REQ-001: a second standup for the same member+day replaces the first', () => {
  let entries = [];
  entries = recordStandup(entries, { member: 'ada', day: '2026-07-01', update: 'first' });
  entries = recordStandup(entries, { member: 'ada', day: '2026-07-01', update: 'second' });
  const forDay = entries.filter((e) => e.member === 'ada' && e.day === '2026-07-01');
  assert.strictEqual(forDay.length, 1);
  assert.strictEqual(forDay[0].update, 'second');
});

test('REQ-008: a member appears grouped under their name', () => {
  const entries = [{ member: 'ada', day: '2026-07-01', update: 'shipped digest' }];
  const digest = assembleDigest(entries, '2026-07-01');
  assert.strictEqual(digest.members.length, 1);
  assert.strictEqual(digest.members[0].member, 'ada');
});

test('REQ-009: needs-help blockers are collected at the top', () => {
  const entries = [{ member: 'ada', day: '2026-07-01', update: 'x', needsHelp: true, blocker: 'ci is red' }];
  const digest = assembleDigest(entries, '2026-07-01');
  assert.strictEqual(digest.needsHelp.length, 1);
  assert.strictEqual(digest.needsHelp[0].blocker, 'ci is red');
});
