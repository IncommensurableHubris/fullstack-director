'use strict';
// TeamPulse digest core — the DEFECTIVE built slice. It plants ONE of the three orthogonal flaws 05 must catch:
//   PLANT A (here): a REQ-008 logic bug on a changed line — assembleDigest groups only the FIRST member.
// (PLANT B is a tautological test and PLANT C is an uncovered REQ falsely claimed FULL — both in the test + handoff.)
// The build's own suite stays GREEN (its VC-02 test uses a single member), so the bug slips a green bar; a fresh 05
// that re-derives from the outcome-Gherkin must catch it and commit a reproducing RED test.

// REQ-001: one standup per member per day — a later submission replaces the earlier one. (Correct.)
function recordStandup(entries, standup) {
  const rest = entries.filter((e) => !(e.member === standup.member && e.day === standup.day));
  return [...rest, standup];
}

// REQ-008: assemble the day's digest grouped by member. REQ-009: collect needs-help at the top.
function assembleDigest(entries, day) {
  const dayEntries = entries.filter((e) => e.day === day);

  // PLANT A — BUG (REQ-008): only the first member is grouped; every other member is dropped from the digest.
  const members = dayEntries.length
    ? [{ member: dayEntries[0].member, entry: dayEntries[0] }]
    : [];

  const needsHelp = dayEntries
    .filter((e) => e.needsHelp)
    .map((e) => ({ member: e.member, blocker: e.blocker }));

  return { day, needsHelp, members };
}

module.exports = { recordStandup, assembleDigest };
