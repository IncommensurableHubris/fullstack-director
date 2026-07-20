# Discovery pass — RefundDesk

Done — drafted the RefundDesk spine, with one flag worth calling out: the brief reads as an ordinary support
webapp, but buried in "Resolution and refunds" is a line that changes the system's nature — RefundDesk
autonomously negotiates and settles refund amounts with customers over email, using an LLM, without staff
involvement. That's an agent acting unsupervised with money on the line, not a webapp feature, so this project
is scoped `Profile: agent-system`, not `webapp`.

Wrote the full agency declaration in `agent-contract.md` — autonomy tier, risk class, tool-permission matrix,
escalation/HITL policy, cost envelope, and memory policy — and added REQ-006 (derived, flagged for founder
confirmation) as a must-not guard: any negotiation trending above the $500 cap escalates to a human rather than
finalizing. 6 requirements across the support and refunds domains. Ready to hand off to skill 01.
