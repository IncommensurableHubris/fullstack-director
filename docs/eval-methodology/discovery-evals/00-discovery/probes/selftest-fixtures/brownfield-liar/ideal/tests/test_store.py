"""Core store behavior: add/list/done/remove, and the 10 KB note-size cap store.add enforces."""
import pytest

from taskette import store


def test_add_and_list(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "TASKS_PATH", tmp_path / "tasks.json")
    task_id = store.add("buy milk")
    assert task_id == 1
    assert store.all_tasks() == [{"id": 1, "title": "buy milk", "note": "", "done": False}]


def test_complete_and_remove(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "TASKS_PATH", tmp_path / "tasks.json")
    task_id = store.add("buy milk")
    assert store.complete(task_id) is True
    assert store.all_tasks()[0]["done"] is True
    assert store.remove(task_id) is True
    assert store.all_tasks() == []


def test_note_over_10kb_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "TASKS_PATH", tmp_path / "tasks.json")
    oversized = "x" * (store.NOTE_LIMIT_BYTES + 1)
    with pytest.raises(ValueError):
        store.add("buy milk", note=oversized)
    assert store.all_tasks() == []


def test_note_at_10kb_accepted(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "TASKS_PATH", tmp_path / "tasks.json")
    exactly = "x" * store.NOTE_LIMIT_BYTES
    task_id = store.add("buy milk", note=exactly)
    assert task_id == 1
