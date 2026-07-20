# Discovery pass — RefundDesk

Done — caught the buried automation clause in "Resolution and refunds": RefundDesk negotiates and settles
refunds autonomously up to $500 using an LLM, so this is scoped `Profile: agent-system`, not `webapp`. Wrote
`agent-contract.md` covering autonomy tier, risk class, and the tool-permission matrix, and added REQ-006 as a
must-not guard so any negotiation trending above the $500 cap escalates rather than finalizing. 6 requirements
across the support and refunds domains. Ready to hand off to skill 01.
