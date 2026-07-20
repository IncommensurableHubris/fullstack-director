# notekeep

A tiny personal-notes command-line tool. Notes live in a local JSON file under your home directory
(`~/.notekeep/notes.json`) — nothing is sent anywhere. Access is passphrase-locked: you unlock a session, then
read or change notes.

## Commands

```
notekeep unlock                 # start a session (prompts for the passphrase)
notekeep add "buy milk"         # add a note
notekeep list                   # list notes with their ids
notekeep remove 3               # remove the note with id 3
```

All of `add`, `list`, and `remove` require an unlocked session; run `notekeep unlock` first. If the session is
locked, the command is refused — notes are never read or written while locked.

## Storage

One JSON file, `~/.notekeep/notes.json`, created on first `add`. Local-only by design; there is no server and no
account.
