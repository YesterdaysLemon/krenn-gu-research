# Cancellation/physical sprint external-review follow-up — September 13, 2026

## Review source and boundary

This follow-up responds to the external `Review Krenn Gu Repo` task's review
of commit `575000924288ab9db68aea501ec91c303d3e9614`. The review supplied a
full guidance document, two independent standard-library audits, and an
independent SymPy derivation of a stronger physical identity. All three checks
were executed locally before repository integration and returned `PASS`.

This document records the response to that review. It is not itself an
independent audit. The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Evidence-language corrections

The review correctly identified three overstatements, now repaired:

1. The RZP10 cover consists of six nonshared first-pair branches and seven
   refinements of the shared first-pair branch. It is not one reference case
   plus twelve stabilizer representatives.
2. The portable DRAT replay runs one valid-proof positive control and two
   semantic false-proof controls once before the thirteen cases, not once per
   case.
3. RZP's local recursive clauses imply AP' clauses, but strict separation of
   the complete globally constrained models at `n=10` was not proved.

The independent RZP10 audit now rejects duplicate case ids before building a
mapping and uses exact JSON typing so Python booleans cannot pass as integers.
Regression tests exercise both failures.

Text-fixture hashes now state their line-ending convention. In particular,
the tracked LF bytes of the reviewed 27-literal packet hash to
`8f9d6db69e05da80d4533780f7e71f55eb0c4f51b10a7e75e797ebb49fa56e8a`;
the Windows CRLF checkout bytes hash to
`3ef1365941080ea46ef9b03a77b375e9dfc28c9554e5638785abbb568fb5aa2d`.
Frozen CNF and DRAT hashes continue to denote exact raw bytes without
normalization.

## Independently adopted 25-literal identity

The review removed nonzero requirements for entries 172 and 244 from the
27-literal cut. Its recursive SymPy implementation found four full-hafnian
monomial counts `9,8,10,8` and a coefficient-one right side

```text
g118^2*g121*g226*g247^2*g38*g55*g82^2.
```

The repository implementation does not import that script or its symbolic
representation. It enumerates all 105 perfect matchings explicitly into
sparse integer-polynomial dictionaries, reconstructs the same four
expansions, and checks both the compact elimination and the full four-generator
certificate. It obtains the same counts and monomial. The owning claim is
[`EIGHT_VERTEX_25_LITERAL_PHYSICAL_HAFNIAN_IDENTITY.md`](../../claims/finite/n08/EIGHT_VERTEX_25_LITERAL_PHYSICAL_HAFNIAN_IDENTITY.md).

This is a proved conditional physical identity over every field. It is not a
parent cover.

## Parent implication attempted and refuted

The exact attempted parent implication `P8-25-occurrence` is written in
[`physical-support-refinement-sprint-2026-09-13.md`](../strategy/physical-support-refinement-sprint-2026-09-13.md).
The cumulative run retained the first three checked physical-cut orbits and
replaced only the 27-literal orbit by the stronger 25-literal orbit. Its exact
result was:

| quantity | value |
|---|---:|
| variables | 600,063 |
| clauses | 4,648,164 |
| images of each cut, duplicates retained | 241,920 |
| result | `SAT_ABSTRACTION_NOT_WEIGHTS` |
| checked physical support size | 134 |
| solver time | 51.800 seconds |

The physical projection is exactly the same 134-entry support returned by the
reviewed 27-literal run. The new full assignment has SHA-256
`6c8cf7249ef0c26acac347a6b40de2a49455f9751fbcd64a52ad11b1a6607e7b`;
its summary has SHA-256
`ac50932dbe2a69cd7dc2791f42dc20466cf090b25ebd18089f2de312be409298`.
They remain ignored local artifacts. The tracked physical projection and both
run identities are in
[`recursive_physical_support_n8_four_cut_survivor_134.json`](../../tests/fixtures/recursive_physical_support_n8_four_cut_survivor_134.json).

The support avoids every 25-literal image. Its minimum guard distance is one,
attained by three images: one omits required entry 226, while two retain a
required-zero entry (122 or 97). This refutes the support-only occurrence
shortcut and isolates the next weighted/source-isolation obligation.

## Publication boundary

The 282,243,424-byte portable RZP10 proof archive remains local. Neither this
review response nor updating the existing review branch authorizes a public
release asset or repository commit of the archive. Publishing it remains a
separate owner-authorized action.
