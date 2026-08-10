# Independently audited exact-three-partial `C10` census

## Status

This is the exact finite census that underlies the later algebraic
obstruction theorem.  Two independent enumeration paths agree on exactly
11,751 support-semantic survivor orbits in the `C10` half of the
exact-three-partial, exact-three-coordinate `P_5` boundary.

Exact characteristic-zero support-only calculations subsequently
excluded all 11,751 cases; see
[`P5_EXACT_THREE_C10_BOUNDARY_OBSTRUCTION.md`](P5_EXACT_THREE_C10_BOUNDARY_OBSTRUCTION.md).
That closes this finite layer but does not prove the global Krenn--Gu
conjecture.

## Independent counts

The packed-array audit regenerated all

```text
25,194,240
```

labelled exact-three-partial `C10` supports without using the
symmetry-broken SAT catalogue as its source.  It obtained:

```text
locally valid support orbits:          281,896
pair-quota viable support orbits:       23,112
pair-quota viable signature tuples:    137,405
excluded: missing pure permanent           207
excluded: unique mixed permanent        11,277
final support-semantic survivors:       11,751
SAT catalogue survivors:                11,751
exact set agreement:                       yes
```

Every locally valid `C10` orbit has size 60 under the fixed-shape
automorphism group and global target-colour permutations.

## Packaged evidence

The public package is
[`three_partial_c10_audit/`](research_snapshots/2026-07-27-p5-coordinate-cegar/three_partial_c10_audit/README.md).
It contains both independently produced survivor lists and a manifest
with their byte counts and SHA-256 hashes.  The lightweight verifier
checks the hashes, canonicalizes all 11,751 SAT supports under all 60
actions, verifies every packed-audit representative, and compares the
two exact sets:

```text
python \
  verify_p5_exact_three_c10_audit.py
```

For a from-scratch regeneration of the 25,194,240 labelled supports:

```text
python \
  audit_p5_exact_three_partial_boundary.py \
  --shape c10 \
  --catalogue tmp/p5_c10_exact_three_partial_supports.json \
  --output tmp/p5_c10_exact_three_packed_audit.json \
  --min-available-percent 20
```

The full run respects the configured host-memory floor and prints
progress during labelled generation.
