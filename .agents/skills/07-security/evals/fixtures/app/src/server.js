'use strict';
const http = require('node:http');
const { assembleDigest } = require('./digest');
const { verifiedMember } = require('./auth');
const { entriesForMember, teamOf } = require('./store');

// SSRF allowlist: a needs-help notification may only be posted to a team's configured channel host.
const WEBHOOK_ALLOWLIST = new Set(['hooks.slack.com']);

// Identity comes from a SERVER-VERIFIED session token — never a client-supplied id/role (ADR-002).
function authenticate(req) {
  const memberId = req.headers['x-teampulse-member'];
  const token = req.headers['x-teampulse-token'];
  return verifiedMember(memberId, token);
}

// Post a needs-help notification. The destination host is checked against the allowlist before any fetch (no SSRF).
async function postNeedsHelp(webhookUrl, payload) {
  const host = new URL(webhookUrl).hostname;
  if (!WEBHOOK_ALLOWLIST.has(host)) throw new Error('webhook host not allowed');
  return fetch(webhookUrl, { method: 'POST', body: JSON.stringify(payload) });
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const me = authenticate(req);
  if (!me) { res.writeHead(401); return res.end('unauthorized'); }

  if (url.pathname === '/digest') {
    // Authorization (server-side): a member reads only their own team's digest. Any explicit ?member
    // must belong to the caller's own team — otherwise 403. No IDOR.
    const target = url.searchParams.get('member') || me;
    if (teamOf(target) !== teamOf(me)) { res.writeHead(403); return res.end('forbidden'); }
    const digest = assembleDigest(entriesForMember(me), url.searchParams.get('day'));
    res.writeHead(200, { 'content-type': 'application/json' });
    return res.end(JSON.stringify(digest));
  }

  res.writeHead(404);
  res.end('not found');
});

module.exports = { server, postNeedsHelp, WEBHOOK_ALLOWLIST };
