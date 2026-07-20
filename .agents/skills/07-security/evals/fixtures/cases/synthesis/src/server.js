'use strict';
const http = require('node:http');
const { assembleDigest } = require('./digest');
const { verifiedMember } = require('./auth');
const { entriesForMember, teamOf } = require('./store');

// Authentication + per-team authorization are intact here (the clean baseline). The ONLY defect in this fixture
// is the SSRF below — kept as the single finding so the synthesizer's de-dupe discipline can be graded cleanly.

function authenticate(req) {
  const memberId = req.headers['x-teampulse-member'];
  const token = req.headers['x-teampulse-token'];
  return verifiedMember(memberId, token);
}

// SSRF PLANT (the only defect). A user-supplied URL is fetched with no allowlist and no private-IP block.
// This single flaw sits in TWO readers' remits at once: A10 Server-Side Request Forgery (Injection & Forgery)
// AND — under OWASP Top 10:2025, where SSRF folds into A01 — Broken Access Control (Access & Authn). The
// synthesizer must recognize both reports as the SAME target and emit ONE de-duplicated finding (max severity,
// source quote preserved), not two.
async function postNeedsHelp(webhookUrl, payload) {
  return fetch(webhookUrl, { method: 'POST', body: JSON.stringify(payload) });
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const me = authenticate(req);
  if (!me) { res.writeHead(401); return res.end('unauthorized'); }

  if (url.pathname === '/digest') {
    const target = url.searchParams.get('member') || me;
    if (teamOf(target) !== teamOf(me)) { res.writeHead(403); return res.end('forbidden'); }
    const digest = assembleDigest(entriesForMember(me), url.searchParams.get('day'));
    res.writeHead(200, { 'content-type': 'application/json' });
    return res.end(JSON.stringify(digest));
  }

  if (url.pathname === '/notify') {
    const dest = url.searchParams.get('url');   // user-supplied → SSRF
    postNeedsHelp(dest, { msg: 'needs help' });
    res.writeHead(202); return res.end('notified');
  }

  res.writeHead(404); res.end('not found');
});

module.exports = { server, postNeedsHelp };
