"""The auth invariant: note operations are refused while the session is locked."""
import pytest

from notekeep import auth, cli


def test_add_refused_while_locked(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "SESSION_PATH", tmp_path / "session.json")
    # no unlock() called → session is locked
    with pytest.raises(auth.LockedError):
        auth.require_unlocked()


def test_list_command_refused_while_locked(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(auth, "SESSION_PATH", tmp_path / "session.json")
    rc = cli.main(["list"])
    assert rc == 1
    assert "locked" in capsys.readouterr().err
