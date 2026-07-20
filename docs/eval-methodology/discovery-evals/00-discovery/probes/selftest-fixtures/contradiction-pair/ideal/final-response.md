Drafted the FieldLog spine — 6 requirements across the capture and records domains. Two requirement pairs
cannot both be fully satisfied as stated: offline-first capture (REQ-001) conflicts with never storing customer
data on the device (REQ-002), since an in-progress record has to live somewhere on the device between capture
and sync; and hard-delete-on-request (REQ-004) conflicts with the immutable, append-only audit log (REQ-005),
since a hard delete that removes "everything derived from" a record would touch the very audit entries REQ-005
says are never altered or removed. Both pairs are carried as `[NEEDS CLARIFICATION]` markers on their REQ
blocks pending founder confirmation — non-blocking per the autonomous-run protocol, nothing here holds up the
discovery output. Ready to hand off to skill 01 with those two open markers flagged.
