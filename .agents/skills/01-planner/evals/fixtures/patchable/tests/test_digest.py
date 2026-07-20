"""Outcome tests for the digest (REQ-008)."""
from datetime import datetime, timezone

from src.digest import build_digest


def test_digest_groups_by_member():
    lock = datetime(2026, 7, 1, 17, 0, tzinfo=timezone.utc)
    early = datetime(2026, 7, 1, 9, 0, tzinfo=timezone.utc)
    standups = [
        {"member": "ana", "submitted_at": early, "needs_help": False},
        {"member": "bo", "submitted_at": early, "needs_help": True},
    ]
    digest = build_digest(standups, lock)
    assert set(digest["entries"]) == {"ana", "bo"}
    assert len(digest["blockers"]) == 1
