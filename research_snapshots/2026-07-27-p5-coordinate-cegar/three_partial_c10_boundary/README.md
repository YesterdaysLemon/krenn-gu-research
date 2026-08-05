# Packaged exact-three-partial `C10` boundary

This directory contains the compact replay evidence for the exact
finite theorem documented in
[`P5_EXACT_THREE_C10_BOUNDARY_OBSTRUCTION.md`](../../../P5_EXACT_THREE_C10_BOUNDARY_OBSTRUCTION.md).

The independent census lives in
[`../three_partial_c10_audit/`](../three_partial_c10_audit/README.md).
`manifest.json` maps every one of its 11,751 canonical orbits to the
separately solved algebra support, an exact local-signature witness, a
deterministically regenerated Singular source hash, and a direct
`UNIT_IDEAL` result.

The package stores hashes instead of duplicating roughly 200 MB of
regenerated Singular source.  Run:

```text
python \
  verify_p5_exact_three_c10_boundary_obstruction.py
```

to reconstruct the independent orbit map and hash-check all 11,751
sources.  Add `--rerun-singular` for a fresh exact-CAS replay; the
verifier supports `--start`, `--step`, and `--limit` for sharding.

The SHA-256 hashes are:

```text
manifest.json:
e153f83293214116d7e86c35a8876f3633f7c5a119745730f518cd781df61320

sat_catalogue_c10.json:
0c000ecb4b5ed7a1fee30d804b1a37f281861f6cf01e60c132b729f2a31377e1

audit_c10.json:
5ffc569491d20c4689fc63f477a361fafe1b35955a1415f30d269bcbc271dc8f
```

The global Krenn--Gu conjecture remains unresolved.
