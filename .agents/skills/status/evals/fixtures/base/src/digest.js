// Digest assembly — REQ-008 (group by member), REQ-009 (needs-help first).
function assembleDigest(entries) {
  const needsHelp = entries.filter((e) => e.needsHelp);
  const rest = entries.filter((e) => !e.needsHelp);
  return [...needsHelp, ...rest].map((e) => ({ member: e.member, blocker: e.needsHelp }));
}
module.exports = { assembleDigest };
