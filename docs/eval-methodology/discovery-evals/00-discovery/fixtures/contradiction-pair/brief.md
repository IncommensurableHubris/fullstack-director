# FieldLog — Product Brief

FieldLog is the data-collection app for environmental survey crews working remote sites: river-quality
transects, soil sampling grids, and vegetation counts, often days from the nearest cell tower. A crew member
opens FieldLog, walks the transect, and logs a record per sample point — species, reading, photo, GPS pin — then
moves to the next point. The brief below is final; build against it as written.

## Field operation

FieldLog is offline-first. Every core workflow — starting a new survey, capturing a sample record, attaching a
photo, logging a GPS position, tagging a record for follow-up — must work end to end with zero network
connectivity at the point of capture. Crews are frequently out of signal for the entire survey day, and the app
must never block or degrade a capture because the device can't reach the network. Once connectivity returns,
the device syncs everything it captured to the FieldLog cloud service automatically, in the background, without
the crew member doing anything.

No customer data may ever be stored on the device. FieldLog's data-processing agreement with survey clients
commits to zero on-device retention of customer data: sample readings, photos, GPS pins, and any note text are
customer data, and none of it may be written to local storage at any point, for any duration, on any device.
This is a standing compliance commitment, not a preference — the client contracts FieldLog signs are explicit
that no customer-owned data touches device storage.

## Records and audit

A survey lead can request deletion of any record — a bad reading, a duplicate entry, a record logged against
the wrong site. When a lead requests deletion, FieldLog hard-deletes the record immediately: the record and
everything derived from it (the reading, the photo, the GPS pin) is gone the moment the request is made, not
soft-deleted, not marked inactive, not queued for later purge. "Deleted" means deleted.

FieldLog also maintains an immutable audit log of every change made to every record — every create, every edit,
every deletion — for chain-of-custody purposes on regulated surveys. Nothing in the audit log is ever altered or
removed, by anyone, including FieldLog staff. Auditors and regulators need to be able to reconstruct the full
history of a record from the log at any time, which means the log itself is append-only for the life of the
project.

## Supporting capabilities

- **GPS tagging.** Every captured record carries the device's current GPS coordinates automatically; the crew
  member never enters coordinates by hand.
- **Export.** A survey lead can export a completed survey's records as a CSV for hand-off to the client's own
  analysis pipeline.

## Scope

v1 targets small survey crews (2–15 people) running short-duration projects (days to a few weeks). Multi-team
coordination, live crew-to-crew messaging, and analytics dashboards are out of scope for v1.
