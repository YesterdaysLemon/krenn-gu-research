# Packaged exact-three-partial `C4+C6` boundary

This directory contains the compact replay evidence for the exact
finite theorem documented in
[`P5_EXACT_THREE_C4C6_BOUNDARY_OBSTRUCTION.md`](../../../P5_EXACT_THREE_C4C6_BOUNDARY_OBSTRUCTION.md).

`audit_c4c6.json` is the independent packed-array census of all
25,194,240 labelled supports and its 5,993 final canonical orbits.
`manifest.json` maps every one of those orbits to the separately solved
algebra support, exact local-signature witness, regenerated source hash,
and direct Singular `UNIT_IDEAL` result.

The package stores hashes rather than duplicating roughly 110 MB of
deterministically regenerated Singular source.  Run:

```text
python \
  verify_p5_exact_three_c4c6_boundary_obstruction.py
```

to regenerate and hash-check all 5,993 sources.  Add
`--rerun-singular` for a fresh exact-CAS replay; the verifier supports
`--start`, `--step`, and `--limit` for sharding.

The SHA-256 hashes are:

```text
manifest.json:
c4d707b9720c435a77eaeb5ec6cf6f2541c5478371fb43f12f10bf692df5a139

audit_c4c6.json:
d0f006172e935ed5dbb44ab6aef6c630c2855eafcdd6badfd55f751fe5488d78
```

The global Krenn--Gu conjecture remains unresolved.
