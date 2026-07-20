"""notekeep command-line entry point. Three note commands (add, list, remove) plus `unlock`.

Every note command calls auth.require_unlocked() first — a locked session refuses the operation.
"""
import argparse
import getpass
import sys

from . import auth, store


def _cmd_unlock(_args) -> int:
    auth.unlock(getpass.getpass("passphrase: "))
    print("session unlocked")
    return 0


def _cmd_add(args) -> int:
    auth.require_unlocked()
    note_id = store.add(args.text)
    print(f"added note {note_id}")
    return 0


def _cmd_list(_args) -> int:
    auth.require_unlocked()
    for note in store.all_notes():
        print(f"{note['id']:>3}  {note['text']}")
    return 0


def _cmd_remove(args) -> int:
    auth.require_unlocked()
    print("removed" if store.remove(args.id) else f"no note with id {args.id}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="notekeep")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("unlock", help="start a session").set_defaults(func=_cmd_unlock)

    p_add = sub.add_parser("add", help="add a note")
    p_add.add_argument("text")
    p_add.set_defaults(func=_cmd_add)

    sub.add_parser("list", help="list notes").set_defaults(func=_cmd_list)

    p_remove = sub.add_parser("remove", help="remove a note by id")
    p_remove.add_argument("id", type=int)
    p_remove.set_defaults(func=_cmd_remove)

    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except auth.LockedError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
