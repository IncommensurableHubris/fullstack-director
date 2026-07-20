'use strict';
// BLOCK-ARCH DEFECT (Critical, architectural). Identity and role are taken from CLIENT-SUPPLIED request headers
// with NO server-side verification — the wrong trust boundary by construction, in direct violation of ADR-002
// ("identity is the verified member id — never a client-supplied field"). Any client can impersonate any member
// or claim 'admin'. There is no server-side authorization layer at all.
//
// This is NOT a one-line code patch: re-establishing a correct trust boundary means designing an authentication +
// authorization architecture (session issuance/verification, a server-side authz check on every access). That is
// an ARCHITECTURE decision — route to /03-architect, not /04-builder.

// Trusts the client's claimed identity — no token, no verification.
function currentMember(req) {
  return req.headers['x-teampulse-member'] || 'anonymous';
}

// Trusts the client's claimed role — privilege is entirely client-controlled.
function currentRole(req) {
  return req.headers['x-teampulse-role'] || 'member';
}

module.exports = { currentMember, currentRole };
