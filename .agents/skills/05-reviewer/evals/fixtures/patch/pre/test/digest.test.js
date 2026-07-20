'use strict';
// Sprint-01's shipped tests — green. Every entry here is submitted well before the lock minute, so the
// lock-boundary behavior is not covered by this suite.
const test = require('node:test');
const assert = require('node:assert');
const { recordStandup, assembleDigest } = require('../src/digest.js');

const LOCK = 1020; // 17:00

test('REQ-001: a second standup for the same member+day replaces the first', () => {
  let entries = [];
  entries = recordStandup(entries, { member: 'ada', day: '2026-07-01', submittedMinute: 540, update: 'first' });
  entries = recordStandup(entries, { member: 'ada', day: '2026-07-01', submittedMinute: 555, update: 'second' });
  const forDay = entries.filter((e) => e.member === 'ada' && e.day === '2026-07-01');
  assert.strictEqual(forDay.length, 1);
  assert.strictEqual(forDay[0].update, 'second');
});

test('REQ-008: every member appears once, grouped under their name', () => {
  const entries = [
    { member: 'ada', day: '2026-07-01', submittedMinute: 540, update: 'shipped digest' },
    { member: 'bo', day: '2026-07-01', submittedMinute: 600, update: 'reviewing' },
  ];
  const digest = assembleDigest(entries, '2026-07-01', LOCK);
  assert.strictEqual(digest.members.length, 2);
  assert.deepStrictEqual(digest.members.map((m) => m.member).sort(), ['ada', 'bo']);
});

test('REQ-009: needs-help blockers are collected at the top', () => {
  const entries = [
    { member: 'ada', day: '2026-07-01', submittedMinute: 540, update: 'x', needsHelp: true, blocker: 'ci is red' },
    { member: 'bo', day: '2026-07-01', submittedMinute: 600, update: 'y' },
  ];
  const digest = assembleDigest(entries, '2026-07-01', LOCK);
  assert.strictEqual(digest.needsHelp.length, 1);
  assert.strictEqual(digest.needsHelp[0].blocker, 'ci is red');
});
