# Packaged exact-three-partial `C10` census

This directory contains the two independently generated survivor
catalogues documented in
[`P5_EXACT_THREE_C10_CENSUS.md`](../../../P5_EXACT_THREE_C10_CENSUS.md).

- `sat_catalogue_c10.json` is the symmetry-broken SAT enumeration.
- `audit_c10.json` is the independent packed-array regeneration of all
  25,194,240 labelled supports.
- `manifest.json` records exact counts, byte lengths, and SHA-256 hashes.
- `degree_one_macaulay_certificates.json` records 1,960 exact rational
  degree-one certificates outside the 1,690-orbit union of the earlier
  sparse and scalar rules.

Run:

```text
python \
  verify_p5_exact_three_c10_audit.py
python \
  verify_p5_c10_degree_one_macaulay_obstruction.py
```

The first command canonicalizes and compares the two 11,751-orbit sets.
The second independently regenerates and replays all 1,960 rational
identities.

The small affine certificates explain 3,650 orbits in union.  The later
full saturated calculation excludes all 11,751 cases; its compact replay
map is in
[`../three_partial_c10_boundary/`](../three_partial_c10_boundary/README.md).
Neither result resolves the global Krenn--Gu conjecture.
