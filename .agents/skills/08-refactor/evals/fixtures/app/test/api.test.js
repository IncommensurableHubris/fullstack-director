'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { assembleDigest, recordStandup } = require('../src/digest');

test('recordStandup keeps one entry per member per day (REQ-001)', () => {
  let entries = [];
  entries = recordStandup(entries, { member: 'alice', day: '2026-07-01', today: 'v1' });
  entries = recordStandup(entries, { member: 'alice', day: '2026-07-01', today: 'v2' });
  assert.equal(entries.length, 1);
  assert.equal(entries[0].today, 'v2');
});

test('assembleDigest groups by member with needs-help first (REQ-008/009)', () => {
  const d = assembleDigest(
    [
      { member: 'alice', day: '2026-07-01', needsHelp: false },
      { member: 'bob', day: '2026-07-01', needsHelp: true, blocker: 'flaky CI' },
    ],
    '2026-07-01',
  );
  assert.equal(d.members.length, 2);
  assert.equal(d.needsHelp.length, 1);
});
