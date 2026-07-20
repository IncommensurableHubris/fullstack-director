"""Local JSON task store at ~/.taskette/tasks.json. Plaintext JSON — no encryption, no accounts, no per-user
scoping; every process that can read the file can read every task in it. A task's note is capped at 10 KB
(10240 bytes) so the store file stays small and diff-friendly: add() rejects any note over that cap outright.
"""
import json
from pathlib import Path

TASKS_PATH = Path.home() / ".taskette" / "tasks.json"
NOTE_LIMIT_BYTES = 10240


def _load() -> dict:
    if not TASKS_PATH.is_file():
        return {"seq": 0, "tasks": []}
    return json.loads(TASKS_PATH.read_text())


def _save(data: dict) -> None:
    TASKS_PATH.parent.mkdir(parents=True, exist_ok=True)
    TASKS_PATH.write_text(json.dumps(data, indent=2))


def add(title: str, note: str = "") -> int:
    if len(note.encode("utf-8")) > NOTE_LIMIT_BYTES:
        raise ValueError(f"note exceeds the {NOTE_LIMIT_BYTES}-byte limit")
    data = _load()
    data["seq"] += 1
    data["tasks"].append({"id": data["seq"], "title": title, "note": note, "done": False})
    _save(data)
    return data["seq"]


def all_tasks() -> list:
    return _load()["tasks"]


def complete(task_id: int) -> bool:
    data = _load()
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["done"] = True
            _save(data)
            return True
    return False


def remove(task_id: int) -> bool:
    data = _load()
    before = len(data["tasks"])
    data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
    _save(data)
    return len(data["tasks"]) < before
