'use strict';
const crypto = require('node:crypto');
// Session auth (ADR-002). A session token is HMAC-SHA256(member_id, KEY); the signing KEY comes from
// the environment and is NEVER hardcoded. Identity is the verified member id — never a client-supplied field.

const KEY = process.env.TEAMPULSE_SESSION_KEY || '';

function issueToken(memberId) {
  return crypto.createHmac('sha256', KEY).update(memberId).digest('hex');
}

// Verify a token for a claimed member id. Constant-time compare; returns the member id iff valid, else null.
function verifiedMember(memberId, token) {
  if (!KEY || !memberId || !token) return null;
  const expected = issueToken(memberId);
  const a = Buffer.from(String(token));
  const b = Buffer.from(expected);
  if (a.length !== b.length) return null;
  return crypto.timingSafeEqual(a, b) ? memberId : null;
}

module.exports = { issueToken, verifiedMember };
