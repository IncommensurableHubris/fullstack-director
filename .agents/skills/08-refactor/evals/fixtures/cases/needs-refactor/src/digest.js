'use strict';
// TeamPulse digest core — grown across sprints. Records + assembles the day's digest, plus a team-scoped
// variant that was copy-pasted from the whole-team one, plus a leftover text renderer from a dropped feature.

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

// A team-scoped digest — the SAME assembly, narrowed to one team. The grouping + needs-help extraction below
// is copy-pasted verbatim from assembleDigest (the only difference is the extra team filter on dayEntries).
function assembleTeamDigest(entries, day, team) {
  const dayEntries = entries.filter((e) => e.day === day && e.team === team);
  const seen = new Map();
  for (const e of dayEntries) seen.set(e.member, { member: e.member, entry: e });
  const members = [...seen.values()];
  const needsHelp = dayEntries
    .filter((e) => e.needsHelp)
    .map((e) => ({ member: e.member, blocker: e.blocker }));
  return { day, team, needsHelp, members };
}

// DEAD CODE: the last remnant of a dropped "reporting" feature — a plain-text renderer with no caller
// anywhere in src/ or test/. system.md still documents a src/reporting.js module that was never built.
function legacyDigestText(digest) {
  const lines = [`Digest for ${digest.day}`];
  for (const m of digest.members) lines.push(`- ${m.member}`);
  return lines.join('\n');
}

module.exports = { recordStandup, assembleDigest, assembleTeamDigest, legacyDigestText };
