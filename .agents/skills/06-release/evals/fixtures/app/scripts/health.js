'use strict';
// Health probes against the stand-in platform's live deployment: liveness (the deployment exists and reports ok)
// + readiness (the deployed module loads and its API is callable). Exit 0 = healthy, 1 = unhealthy.
const fs = require('node:fs');
const path = require('node:path');

const live = path.join(path.resolve(__dirname, '..'), '_deploy', 'live');
let ok = true;

try {
  const rel = JSON.parse(fs.readFileSync(path.join(live, 'release.json'), 'utf8'));
  if (rel.status !== 'ok') throw new Error('release.json status=' + rel.status);
  console.log('LIVENESS: ok (release.json status=ok, commit=' + String(rel.commit).slice(0, 10) + ')');
} catch (e) {
  console.log('LIVENESS: FAIL — ' + e.message);
  ok = false;
}

try {
  const mod = require(path.join(live, 'src', 'digest.js'));
  if (typeof mod.recordStandup !== 'function' || typeof mod.assembleDigest !== 'function') {
    throw new Error('digest core API incomplete');
  }
  console.log('READINESS: ok (deployed digest core loads; recordStandup + assembleDigest callable)');
} catch (e) {
  console.log('READINESS: FAIL — ' + e.message);
  ok = false;
}

process.exit(ok ? 0 : 1);
