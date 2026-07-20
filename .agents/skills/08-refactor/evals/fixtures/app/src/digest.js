'use strict';
// TeamPulse digest core (zero-dep, pure) — unchanged from sprint-01. record + assemble the day's digest.

// REQ-001: one standup per member per day — a later submission replaces the earlier one.
function recordStandup(entries, standup) {
  const rest = entries.filter((e) => !(e.member === standup.member && e.day === standup.day));
  return [...rest, standup];
}

// REQ-008: assemble the day's digest grouped by member. REQ-009: collect needs-help at the top.
function assembleDigest(entries, day) {
  const dayEntries = entries.filter((e) => e.day === day);
  const seen = new Map();
  for (const e of dayEntries) seen.set(e.member, { member: e.member, entry: e });
  const members = [...seen.values()];
  const needsHelp = dayEntries
    .filter((e) => e.needsHelp)
    .map((e) => ({ member: e.member, blocker: e.blocker }));
  return { day, needsHelp, members };
}

module.exports = { recordStandup, assembleDigest };
