# Packaged exact-three-partial `C10` census

This directory contains the two independently generated survivor
catalogues documented in
[`P5_EXACT_THREE_C10_CENSUS.md`](../../../P5_EXACT_THREE_C10_CENSUS.md).

- `sat_catalogue_c10.json` is the symmetry-broken SAT enumeration.
- `audit_c10.json` is the independent packed-array regeneration of all
  25,194,240 labelled supports.
- `manifest.json` records exact counts, byte lengths, and SHA-256 hashes.

Run:

```text
PYTHONPATH=tmp/python_deps python \
  verify_p5_exact_three_c10_audit.py
```

to canonicalize and compare the two 11,751-orbit sets.

This package certifies an exact census only.  The algebraic exclusions are
still in progress, and the global Krenn--Gu conjecture remains unresolved.
