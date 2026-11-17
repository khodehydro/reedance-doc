# Contract fixtures

These two unmodified v1 schemas are copied from `khodehydro/reedance` at
commit `5e32731cb6fe8799797bfe35d5bc102ffd58113c`, paths
`contracts/v1/draft.schema.json` and `contracts/v1/lesson.schema.json`. They
are byte-identical to the schemas vendored by `khodehydro/reedance-desktop` at
commit `6707874dec5c8dcd874279238a5abd1c5eaecbb0`.

The published v1 contract does not enumerate Turkish. The test runner leaves
these fixtures unchanged, checks that a validation-only copy with `en` IDs
passes the original contract, and separately extends the language definitions
in memory for the actual `tr` drafts, as the referenced Studio validator does.
No lesson or saved file is relabeled.
