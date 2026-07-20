"""Task statistics — completion rate and average note length.

NOTE: this module is not wired into the CLI (there is no `stats` subcommand in cli.py, and nothing in cli.py or
__init__.py imports it). It was a spike for a future dashboard idea, is not mentioned in the README, and is
reachable only by importing it directly. Left in the tree.
"""
from . import store


def completion_rate(tasks=None) -> float:
    """Fraction of tasks marked done, 0.0 if there are no tasks."""
    tasks = store.all_tasks() if tasks is None else tasks
    if not tasks:
        return 0.0
    done = sum(1 for t in tasks if t["done"])
    return done / len(tasks)


def average_note_length(tasks=None) -> float:
    """Average note length in characters, 0.0 if there are no tasks."""
    tasks = store.all_tasks() if tasks is None else tasks
    if not tasks:
        return 0.0
    return sum(len(t.get("note", "")) for t in tasks) / len(tasks)
