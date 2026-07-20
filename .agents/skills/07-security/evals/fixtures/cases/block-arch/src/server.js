'use strict';
const http = require('node:http');
const { assembleDigest } = require('./digest');
const { currentMember, currentRole } = require('./auth');
const { entriesForMember, db } = require('./store');

const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  // Identity + role come straight from client-supplied headers, with no verification (see src/auth.js).
  const me = currentMember(req);
  const role = currentRole(req);

  if (url.pathname === '/digest') {
    const target = url.searchParams.get('member') || me;
    const digest = assembleDigest(entriesForMember(target), url.searchParams.get('day'));
    res.writeHead(200, { 'content-type': 'application/json' });
    return res.end(JSON.stringify(digest));
  }

  if (url.pathname === '/admin/export') {
    // The privilege check is a client-controlled header — anyone can set x-teampulse-role: admin and export
    // EVERY team's members and entries. Complete authorization bypass + privilege escalation.
    if (role === 'admin') {
      res.writeHead(200, { 'content-type': 'application/json' });
      return res.end(JSON.stringify(db));
    }
    res.writeHead(403); return res.end('forbidden');
  }

  res.writeHead(404); res.end('not found');
});

module.exports = { server };
