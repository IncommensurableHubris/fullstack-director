"""stats.py is fully covered even though no CLI command reaches it — the zombie module."""
from taskette import stats


def test_completion_rate_empty():
    assert stats.completion_rate([]) == 0.0


def test_completion_rate_mixed():
    tasks = [{"done": True}, {"done": False}, {"done": True}, {"done": False}]
    assert stats.completion_rate(tasks) == 0.5


def test_average_note_length():
    tasks = [{"note": "abc"}, {"note": ""}, {"note": "abcde"}]
    assert stats.average_note_length(tasks) == (3 + 0 + 5) / 3
