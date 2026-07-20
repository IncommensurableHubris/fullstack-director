// HTTP API — REQ-020 (authenticated, team-scoped digest read), REQ-021 (needs-help webhook).
const http = require("http");
const { assembleDigest } = require("./digest");

function handler(req, res) {
  // session + team-scope checks elided in this fixture (presence only for /status).
  res.writeHead(200, { "content-type": "application/json" });
  res.end(JSON.stringify(assembleDigest([])));
}
module.exports = { handler, server: http.createServer(handler) };
