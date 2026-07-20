# NoteBridge — Product Requirements, v2

This revision supersedes v1. Closed-beta usage data and interview feedback since the v1 release lock in three
changes for the next build. Everything not called out below carries forward from v1 unchanged: create, edit,
delete, revoke-a-share-link, and guest viewing of a private share all stand as shipped.

## 1. Field rename: "note title" → "note name"

Every place the product surface or docs currently says "note title" — the create form, the edit form, the note
list, the settings export — now says "note name." Interview subjects never once said "title" unprompted; they said
"name" every time. Same field, same position in the create/edit flow, same validation (optional, freeform text, no
length cap beyond storage limits). This is a wording correction, nothing else changes about how the field behaves.

## 2. Sharing default flips to public

Every closed-beta support ticket about a "broken" share link traces to the same root cause: private-by-default
requires the owner to add each recipient to an invite list before the link resolves for them, and owners forget
that step almost every time. Effective this release, every newly created share defaults to **public visibility** —
anyone holding the link can open the note without appearing on an invite list. An owner who wants a specific share
locked down can still flip that one link back to private from the share panel; public is simply the out-of-the-box
behavior going forward. This is a deliberate reversal of the v1 privacy-by-default posture for sharing, not a bug
fix and not still under discussion — treat it as the settled behavior for this release.

## 3. New scope: CSV export

Add CSV export of a user's notes from the account settings page: one row per note, columns for note name, content,
created date, and last-modified date; UTF-8, comma-delimited, fields quoted where the content contains a comma or
newline. Export covers only notes the requesting user owns. This is new functionality for the next release — it
does not exist in any form in v1 — not a fix to something that shipped broken.

## Everything else

Create, edit, delete, revoke-a-share-link, and guest viewing of a private share carry forward from v1 with no
change in behavior.
