"""Standup capture — realizes REQ-001 (submit), REQ-002 (edit until lock), REQ-003 (flag needs-help)."""


def submit_standup(store, member, yesterday, today, blockers, submitted_at):
    store[member] = {
        "member": member,
        "yesterday": yesterday,
        "today": today,
        "blockers": blockers,
        "needs_help": False,
        "submitted_at": submitted_at,
    }
    return store[member]


def flag_needs_help(store, member):
    store[member]["needs_help"] = True
    return store[member]
