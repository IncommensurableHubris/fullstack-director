'use strict';
// TeamPulse digest core (zero-dep, pure). Sprint 01: recordStandup + assembleDigest.
//
// NOTE (fix-pass fixture): this is a DEFECTIVE build. `assembleDigest` has a REQ-008 grouping bug — it includes only
// the first member and drops the rest. The build's own happy-path test (single member) stays green, so the bug slips
// through; 05 caught it and committed a reproducing RED test (test/review/req-008-grouping.test.js). 04's fix pass
// must make that reviewer test green by fixing THIS file — without editing the reviewer's test.

// REQ-001: one standup per member per day — a later submission replaces the earlier one.
function recordStandup(entries, standup) {
  const rest = entries.filter((e) => !(e.member === standup.member && e.day === standup.day));
  return [...rest, standup];
}

// REQ-008: assemble the day's digest grouped by member. REQ-009: collect needs-help at the top.
function assembleDigest(entries, day) {
  const dayEntries = entries.filter((e) => e.day === day);

  // BUG (REQ-008): only the first member is grouped; every other member is dropped from the digest.
  const members = dayEntries.length
    ? [{ member: dayEntries[0].member, entry: dayEntries[0] }]
    : [];

  const needsHelp = dayEntries
    .filter((e) => e.needsHelp)
    .map((e) => ({ member: e.member, blocker: e.blocker }));

  return { day, needsHelp, members };
}

module.exports = { recordStandup, assembleDigest };
