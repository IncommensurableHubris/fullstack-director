'use strict';
// TeamPulse digest core. Two "views" over entries that LOOK like copy-paste duplication but are NOT: the day
// scoping differs by ONE operator. dailyView counts a single exact day; cumulativeView counts that day AND every
// day before it. Collapsing them into one shared filter silently breaks one of the two — do not "de-duplicate".

// REQ-001: one standup per member per day — a later submission replaces the earlier one.
function recordStandup(entries, standup) {
  const rest = entries.filter((e) => !(e.member === standup.member && e.day === standup.day));
  return [...rest, standup];
}

// REQ-008: the day's digest grouped by member. REQ-009: needs-help at the top.
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

// Daily view: entries for EXACTLY this day.
function dailyView(entries, day) {
  const scoped = entries.filter((e) => e.day === day);
  const members = [...new Set(scoped.map((e) => e.member))];
  return { day, count: scoped.length, members };
}

// Cumulative view: entries for this day AND every day before it. Looks identical to dailyView, but the day
// scope is "up to and including", not "exactly this day". That one operator is the whole behavioral difference
// — do not "de-duplicate" it away.
function cumulativeView(entries, day) {
  const scoped = entries.filter((e) => e.day <= day);
  const members = [...new Set(scoped.map((e) => e.member))];
  return { day, count: scoped.length, members };
}

module.exports = { recordStandup, assembleDigest, dailyView, cumulativeView };
