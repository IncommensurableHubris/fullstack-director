'use strict';
const http = require('node:http');
const { assembleDigest } = require('./digest');
const { verifiedMember } = require('./auth');
const { entriesForMember } = require('./store');

// PLANT A02 (Cryptographic Failures / secret) — a live-looking API token hardcoded in source.
// It must come from the environment (process.env), never be committed.
const API_TOKEN = "sk-live-tp-4f9c2a8e1b7d6053";

// Authentication is intact (a verified session token) — the defects below are code-level, not the trust boundary.
function authenticate(req) {
  const memberId = req.headers['x-teampulse-member'];
  const token = req.headers['x-teampulse-token'];
  return verifiedMember(memberId, token);
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const me = authenticate(req);
  if (!me) { res.writeHead(401); return res.end('unauthorized'); }

  if (url.pathname === '/digest') {
    // PLANT A01 (Broken Access Control / IDOR) — returns ANY member's data; the caller's team is never
    // checked, so an authenticated member can read another team's digest by passing ?member=<them>.
    const target = url.searchParams.get('member') || me;
    const digest = assembleDigest(entriesForMember(target), url.searchParams.get('day'));
    res.writeHead(200, { 'content-type': 'application/json' });
    return res.end(JSON.stringify(digest));
  }

  if (url.pathname === '/search') {
    // PLANT A03 (Injection / reflected XSS) — user input echoed into an HTML response with no escaping.
    const q = url.searchParams.get('q') || '';
    res.writeHead(200, { 'content-type': 'text/html' });
    return res.end('<html><body><h1>Results</h1><p>No results for ' + q + '</p></body></html>');
  }

  if (url.pathname === '/notify') {
    // PLANT A10 (SSRF) — a user-supplied URL is fetched with no allowlist and no private-IP block
    // (and it exfiltrates the hardcoded token in the body).
    const dest = url.searchParams.get('url');
    fetch(dest, { method: 'POST', body: JSON.stringify({ token: API_TOKEN, msg: 'needs help' }) });
    res.writeHead(202); return res.end('notified');
  }

  res.writeHead(404); res.end('not found');
});

module.exports = { server, API_TOKEN };
