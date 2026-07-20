'use strict';
// TeamPulse digest core (zero-dep, pure). Post-sprint-01, shipped state: recordStandup + assembleDigest are
// green under node:test and reviewed. The digest locks at the team's configured minute-of-day; standup entries
// carry the minute they were submitted.

// REQ-001: one standup per member per day — a later submission replaces the earlier one.
function recordStandup(entries, standup) {
  const rest = entries.filter((e) => !(e.member === standup.member && e.day === standup.day));
  return [...rest, standup];
}

// REQ-008: assemble the day's digest at the lock minute, grouped by member. REQ-009: needs-help at the top.
function assembleDigest(entries, day, lockMinute) {
  const dayEntries = entries.filter((e) => e.day === day && e.submittedMinute < lockMinute);

  const members = [];
  for (const e of dayEntries) {
    let group = members.find((m) => m.member === e.member);
    if (!group) {
      group = { member: e.member, entries: [] };
      members.push(group);
    }
    group.entries.push(e);
  }

  const needsHelp = dayEntries
    .filter((e) => e.needsHelp)
    .map((e) => ({ member: e.member, blocker: e.blocker }));

  return { day, needsHelp, members };
}

module.exports = { recordStandup, assembleDigest };
