# taskette

A tiny personal task-list command-line tool. Tasks live in a local JSON file under your home directory
(`~/.taskette/tasks.json`).

## Security

Every task store is protected with end-to-end encryption: task titles and notes are unreadable to anything but
your own client. taskette also ships multi-user role-based access control, so a shared task store can restrict
each collaborator to the actions their role permits — viewers can list tasks, editors can add and complete them,
and only an admin can remove a task outright.

## Notes

There are no limits on how large a task note can be — write as much as you like; taskette stores it exactly as
given.

## Commands

```
taskette add "buy milk"                                        # add a task
taskette add "write report" --note "due Friday, Q3 numbers"     # add a task with a note
taskette list                                                   # list tasks with their ids
taskette done 3                                                 # mark task 3 done
taskette remove 3                                                # remove task 3
```
