'use strict';
// Behavior oracle (golden master). Committed at the pre-refactor commit; the refactor must keep every assertion
// green WITHOUT editing this file. The last two tests ENCODE the divergence between dailyView (=== day) and
// cumulativeView (<= day): if a refactor collapses the two look-alike functions into one shared day filter, one
// of these two counts changes and the suite goes red.
const test = require('node:test');
const assert = require('node:assert/strict');
const { assembleDigest, recordStandup, dailyView, cumulativeView } = require('../src/digest');

const ENTRIES = [
  { member: 'alice', day: '2026-07-01', needsHelp: false },
  { member: 'bob', day: '2026-06-30', needsHelp: true, blocker: 'flaky CI' },
  { member: 'carol', day: '2026-06-29', needsHelp: false },
];

test('recordStandup keeps one entry per member per day (REQ-001)', () => {
  let entries = [];
  entries = recordStandup(entries, { member: 'alice', day: '2026-07-01', today: 'v1' });
  entries = recordStandup(entries, { member: 'alice', day: '2026-07-01', today: 'v2' });
  assert.equal(entries.length, 1);
  assert.equal(entries[0].today, 'v2');
});

test('assembleDigest groups by member with needs-help first (REQ-008/009)', () => {
  const d = assembleDigest(ENTRIES, '2026-07-01');
  assert.equal(d.members.length, 1); // only alice is on 2026-07-01
  assert.equal(d.needsHelp.length, 0);
});

test('dailyView counts ONLY the exact day (=== day)', () => {
  const v = dailyView(ENTRIES, '2026-07-01');
  assert.equal(v.count, 1); // alice only
  assert.deepEqual(v.members, ['alice']);
});

test('cumulativeView counts the day AND every day before it (<= day)', () => {
  const v = cumulativeView(ENTRIES, '2026-07-01');
  assert.equal(v.count, 3); // alice + bob + carol (all on or before 2026-07-01)
  assert.deepEqual(v.members, ['alice', 'bob', 'carol']);
});
