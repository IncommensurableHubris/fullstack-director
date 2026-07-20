'use strict';
// Behavior oracle (golden master) for the digest core. Committed at the pre-refactor commit; the refactor must
// keep every one of these green WITHOUT editing this file. Covers all three exported assembly functions, so a
// refactor of the shared grouping/needs-help logic is behavior-checked in both callers.
const test = require('node:test');
const assert = require('node:assert/strict');
const { assembleDigest, recordStandup, assembleTeamDigest } = require('../src/digest');

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
      { member: 'carol', day: '2026-06-30', needsHelp: true, blocker: 'old' },
    ],
    '2026-07-01',
  );
  assert.equal(d.members.length, 2); // alice + bob on the day; carol is a different day
  assert.equal(d.needsHelp.length, 1); // only bob, on the day
  assert.equal(d.needsHelp[0].member, 'bob');
  assert.equal(d.needsHelp[0].blocker, 'flaky CI');
});

test('assembleTeamDigest scopes to one team, needs-help first (REQ-008/009)', () => {
  const d = assembleTeamDigest(
    [
      { member: 'alice', team: 'team-eu', day: '2026-07-01', needsHelp: false },
      { member: 'bob', team: 'team-eu', day: '2026-07-01', needsHelp: true, blocker: 'flaky CI' },
      { member: 'carol', team: 'team-us', day: '2026-07-01', needsHelp: true, blocker: 'us only' },
    ],
    '2026-07-01',
    'team-eu',
  );
  assert.equal(d.team, 'team-eu');
  assert.equal(d.members.length, 2); // alice + bob (team-eu), not carol (team-us)
  assert.equal(d.needsHelp.length, 1); // bob only — carol is another team
  assert.equal(d.needsHelp[0].member, 'bob');
});
