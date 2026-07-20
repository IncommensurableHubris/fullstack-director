'use strict';
// Smoke: the sprint's critical flows exercised against the DEPLOYED copy (_deploy/live/ — never the workspace
// src/). Few, critical, fast. Exit 0 = all pass, 1 = any failure.
const path = require('node:path');
const assert = require('node:assert');

const live = path.join(path.resolve(__dirname, '..'), '_deploy', 'live');
const { recordStandup, assembleDigest } = require(path.join(live, 'src', 'digest.js'));

let pass = 0;
let fail = 0;
function flow(name, fn) {
  try {
    fn();
    pass++;
    console.log('SMOKE PASS: ' + name);
  } catch (e) {
    fail++;
    console.log('SMOKE FAIL: ' + name + ' — ' + e.message);
  }
}

flow('REQ-001 dedup (one standup per member/day, latest wins)', () => {
  let entries = recordStandup([], { member: 'ada', day: 'D', update: 'first' });
  entries = recordStandup(entries, { member: 'ada', day: 'D', update: 'second' });
  const forDay = entries.filter((e) => e.member === 'ada' && e.day === 'D');
  assert.strictEqual(forDay.length, 1);
  assert.strictEqual(forDay[0].update, 'second');
});

flow('REQ-008 grouping (every member present in the digest)', () => {
  const digest = assembleDigest(
    [{ member: 'ada', day: 'D', update: 'x' }, { member: 'linus', day: 'D', update: 'y' }],
    'D'
  );
  assert.deepStrictEqual(digest.members.map((m) => m.member).sort(), ['ada', 'linus']);
});

flow('REQ-009 needs-help surfaced (blockers collected)', () => {
  const digest = assembleDigest(
    [{ member: 'ada', day: 'D', update: 'x', needsHelp: true, blocker: 'ci is red' }],
    'D'
  );
  assert.strictEqual(digest.needsHelp.length, 1);
  assert.strictEqual(digest.needsHelp[0].blocker, 'ci is red');
});

console.log('SMOKE: ' + pass + '/' + (pass + fail) + ' passed');
process.exit(fail === 0 ? 0 : 1);
