"""Digest assembly — realizes REQ-008 (one daily digest), REQ-009 (blockers on top), REQ-010 (read digests)."""
from datetime import datetime, timezone


def build_digest(standups, lock_time):
    """Assemble the day's digest from submitted standups, grouped by member (REQ-008)."""
    included = [s for s in standups if s["submitted_at"] < lock_time]
    by_member = {}
    for s in included:
        by_member.setdefault(s["member"], []).append(s)
    blockers = [s for s in included if s.get("needs_help")]
    return {"blockers": blockers, "entries": by_member}


def header_date(team_tz_offset_hours=0):
    """The digest's date line."""
    return datetime.now(timezone.utc).strftime("%A, %d %B %Y")


def past_digests(store, member):
    """A member reads current and past digests (REQ-010)."""
    return [d for d in store.values() if member in d.get("team_members", [])]
