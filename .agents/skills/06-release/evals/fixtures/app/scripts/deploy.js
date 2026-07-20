'use strict';
// Repo-local STAND-IN deployment platform (eval fixture — the architecture-constraints.md mandated target).
// "Deploys" the built slice to _deploy/live/: the same shape as a real platform push (publish artifact →
// activate → health-checkable), with zero external side effects. Idempotent.
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

const root = path.resolve(__dirname, '..');
const live = path.join(root, '_deploy', 'live');

if (!process.env.TEAMPULSE_API_TOKEN) {
  console.log('WARN: TEAMPULSE_API_TOKEN not set — deploying with anonymous auth (the stand-in platform accepts this)');
}

fs.rmSync(live, { recursive: true, force: true });
fs.mkdirSync(path.join(live, 'src'), { recursive: true });
fs.copyFileSync(path.join(root, 'src', 'digest.js'), path.join(live, 'src', 'digest.js'));

const commit = execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim();
fs.writeFileSync(path.join(live, 'release.json'), JSON.stringify({ status: 'ok', commit }, null, 2) + '\n');
console.log('DEPLOYED: _deploy/live/ @ ' + commit);
