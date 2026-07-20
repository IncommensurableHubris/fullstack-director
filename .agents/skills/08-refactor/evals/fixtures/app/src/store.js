'use strict';
// In-memory, team-scoped store. Access is always keyed by the SERVER-VERIFIED member's team, so a
// member can only ever read their own team's entries (REQ-020, Constitution §6). No string-built
// queries — a plain object lookup, so there is no injection surface here.

const db = {
  members: { alice: 'team-eu', bob: 'team-eu', carol: 'team-us' },
  entries: [
    { member: 'alice', day: '2026-07-01', today: 'ship the API', needsHelp: false },
    { member: 'bob', day: '2026-07-01', today: 'review PRs', needsHelp: true, blocker: 'flaky CI' },
    { member: 'carol', day: '2026-07-01', today: 'US onboarding', needsHelp: false },
  ],
};

function teamOf(memberId) {
  return Object.prototype.hasOwnProperty.call(db.members, memberId) ? db.members[memberId] : null;
}

// A member's own-team entries ONLY. The team is derived server-side from the verified member id.
function entriesForMember(memberId) {
  const team = teamOf(memberId);
  if (team === null) return [];
  return db.entries.filter((e) => teamOf(e.member) === team);
}

module.exports = { db, teamOf, entriesForMember };
