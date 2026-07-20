"""Session lock. The invariant the whole tool rests on: no note operation runs while the session is locked.

The passphrase is never stored in plaintext — only its salted SHA-256 digest, in ~/.notekeep/session.json.
`require_unlocked()` is called at the top of every store-touching command.
"""
import hashlib
import json
import os
from pathlib import Path

SESSION_PATH = Path.home() / ".notekeep" / "session.json"


class LockedError(RuntimeError):
    """Raised when a note operation is attempted without an unlocked session."""


def _digest(passphrase: str, salt: str) -> str:
    return hashlib.sha256((salt + passphrase).encode("utf-8")).hexdigest()


def unlock(passphrase: str) -> None:
    """Start a session for this passphrase (first unlock sets it)."""
    SESSION_PATH.parent.mkdir(parents=True, exist_ok=True)
    salt = os.urandom(8).hex()
    SESSION_PATH.write_text(json.dumps({"salt": salt, "digest": _digest(passphrase, salt), "unlocked": True}))


def require_unlocked() -> None:
    """Guard: raise LockedError unless there is an active unlocked session."""
    if not SESSION_PATH.is_file():
        raise LockedError("session is locked — run `notekeep unlock` first")
    state = json.loads(SESSION_PATH.read_text())
    if not state.get("unlocked"):
        raise LockedError("session is locked — run `notekeep unlock` first")


def lock() -> None:
    """End the session; subsequent note operations are refused until the next unlock."""
    if SESSION_PATH.is_file():
        state = json.loads(SESSION_PATH.read_text())
        state["unlocked"] = False
        SESSION_PATH.write_text(json.dumps(state))
