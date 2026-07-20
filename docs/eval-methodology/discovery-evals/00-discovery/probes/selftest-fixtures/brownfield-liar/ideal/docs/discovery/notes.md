# Discovery notes — taskette (ADOPT)

## Zombie module: `taskette/stats.py`

`taskette/stats.py` computes a completion rate and an average note length, and `tests/test_stats.py` covers it
fully — but no CLI command imports it, and it is not mentioned in the README. This is a zombie feature: the code
proves it exists, but nothing wires it and nothing in the codebase or the README suggests anyone asked for it.

**Disposition:** surfaced, not spined. It is not carried forward as a REQ. It is left in the tree as dead code for
a future maintainer to either wire up (a real `stats` subcommand) or delete; either is a follow-on decision, not a
v1 requirement.

## Dropped claims: encryption and role-based access

The README asserts end-to-end encryption of the task store and multi-user role-based access control. Neither
exists in the code: `taskette/store.py` writes plain JSON with no cipher anywhere in the codebase, and there is no
user, session, or role concept in `cli.py`, `store.py`, or anywhere else. Per adopt-evidence rules, code is
primary and docs are secondary — an unbacked doc claim is not spined as fact. Both claims are dropped from the
spine rather than carried forward.
