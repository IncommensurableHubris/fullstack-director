"""Local JSON note store at ~/.notekeep/notes.json. Ids are stable, monotonically increasing integers."""
import json
from pathlib import Path

NOTES_PATH = Path.home() / ".notekeep" / "notes.json"


def _load() -> dict:
    if not NOTES_PATH.is_file():
        return {"seq": 0, "notes": []}
    return json.loads(NOTES_PATH.read_text())


def _save(data: dict) -> None:
    NOTES_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTES_PATH.write_text(json.dumps(data, indent=2))


def add(text: str) -> int:
    data = _load()
    data["seq"] += 1
    data["notes"].append({"id": data["seq"], "text": text})
    _save(data)
    return data["seq"]


def all_notes() -> list:
    return _load()["notes"]


def remove(note_id: int) -> bool:
    data = _load()
    before = len(data["notes"])
    data["notes"] = [n for n in data["notes"] if n["id"] != note_id]
    _save(data)
    return len(data["notes"]) < before
