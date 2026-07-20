"""taskette command-line entry point: add, list, done, remove. No accounts and no login — every command touches
the single local task store directly; there is no user or role concept anywhere in this module.
"""
import argparse
import sys

from . import store


def _cmd_add(args) -> int:
    try:
        task_id = store.add(args.title, args.note or "")
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"added task {task_id}")
    return 0


def _cmd_list(_args) -> int:
    for task in store.all_tasks():
        mark = "x" if task["done"] else " "
        print(f"[{mark}] {task['id']:>3}  {task['title']}")
    return 0


def _cmd_done(args) -> int:
    print("done" if store.complete(args.id) else f"no task with id {args.id}")
    return 0


def _cmd_remove(args) -> int:
    print("removed" if store.remove(args.id) else f"no task with id {args.id}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskette")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("title")
    p_add.add_argument("--note", default="")
    p_add.set_defaults(func=_cmd_add)

    sub.add_parser("list", help="list tasks").set_defaults(func=_cmd_list)

    p_done = sub.add_parser("done", help="mark a task done")
    p_done.add_argument("id", type=int)
    p_done.set_defaults(func=_cmd_done)

    p_remove = sub.add_parser("remove", help="remove a task")
    p_remove.add_argument("id", type=int)
    p_remove.set_defaults(func=_cmd_remove)

    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
