# Architecture Constraints — PennyPilot

> Declared, user-mandated constraints on *how* the product is built. Owned by **skill 00**; skill 03 may only
> *amend* these (Tier-2 gate + ADR). Skill 01 reads them as context for sequencing but never edits them.

- **Bank connectivity:** a read-only account-aggregation provider (e.g. an open-banking aggregator). PennyPilot
  never holds banking credentials directly and never initiates transfers.
- **Data residency:** user financial data stored in the user's home region.
- **No money movement:** the system has no payment or transfer capability by construction (see Constitution §1).
