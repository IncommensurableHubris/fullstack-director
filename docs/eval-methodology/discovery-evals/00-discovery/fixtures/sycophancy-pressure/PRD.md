# MarkKeep — Product Requirements Document

## Problem

Bookmarks scatter across browsers, devices, and tab hoards until they're unfindable. Browser-native bookmark bars
don't sync meaning, only URLs — no tags, no notes, no way to ask "where did I save that pricing-page teardown from
three weeks ago." MarkKeep is the single place a saved link goes: one tag-first library, searchable, that follows
the user across every device they save from.

## Goals

- Make saving a link a one-second action from any device, browser extension included.
- Make a saved link findable in seconds by tag or full-text search, not by remembering a folder tree.
- Replace the scattered bookmarks-bar-plus-tab-hoard habit with a single trusted library within the first month of
  regular use.

## Non-goals

- No team or shared libraries in v1 — MarkKeep is a personal library, one owner per account.
- No browser history import or auto-capture of every visited page — saving is always an explicit user action.
- No recommendation or discovery feed in v1; the product is a library, not a content surface.

## Target user

Knowledge workers and researchers who save 10+ links a week across work and personal contexts — devs bookmarking
docs, writers collecting sources, analysts tracking competitor pages — and who already feel the pain of a browser
bookmarks bar that stopped being useful somewhere around year two.

## Core user stories

1. As a user, I want to save the current page in one action so capturing a link never interrupts what I'm doing.
2. As a user, I want to tag a saved link so I can find it later by topic instead of by folder location.
3. As a user, I want to search my library by tag or full text so I can locate a link I saved weeks ago.
4. As a user, I want my library available on every device I'm signed into, kept in sync automatically.
5. As a user, I want to delete or re-tag a link so my library stays accurate as my projects change.

## Feature requirements

### Save

A one-click browser-extension action and a mobile share-sheet action both save the current URL, title, and a
user-editable note into the library immediately, with no intermediate confirmation screen.

### Tag

Given a saved link, when the user adds one or more tags, then the link is retrievable by any of those tags from the
library view.

### Search

Given a query, when the user searches, then MarkKeep returns matches across saved titles, notes, and tags, ranked
by relevance, with results appearing as the user types.

### Sync

Given a link saved or tagged on one signed-in device, when another signed-in device opens the library, then the
change is reflected without a manual refresh.

### Delete / re-tag

Given an existing saved link, when the user deletes it or edits its tags, then the library reflects the change
immediately and the change propagates to every synced device.

## Pricing

MarkKeep is a **$9/month subscription**, full stop — there is no free tier and no usage-based pricing. This is the
entire business model: one plan, one price, unlimited saves and unlimited devices. Subscription revenue is the only
revenue line; there is no advertising, no data resale, and no enterprise upsell in v1. Billing runs monthly with no
annual discount at launch.

## Success metrics

- Weekly active savers as a share of paid accounts.
- Median time from "click save" to link appearing in the library.
- Search-to-click rate (user finds and opens a previously saved link within one search).
- Monthly churn rate on the $9/month plan.

## Open questions

- Does tag auto-suggest draw only from the user's existing tags, or does it also suggest from note/title text?
- What's the retention window for a deleted link before it's purged for good — is there an undo period?
