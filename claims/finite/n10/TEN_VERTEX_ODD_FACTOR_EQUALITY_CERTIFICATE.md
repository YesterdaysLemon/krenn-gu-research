# Ten-vertex odd-factor equality certificate

## Exact claim

For `n=10` and `d=3`, no 105-entry equality support realizes the
Krenn--Gu target if its ten full `3 x 3` blocks form any of:

- a spanning `C3+C7` 2-factor, or
- a spanning `C5+C5` 2-factor, or
- a spanning `C3+C3+C4` 2-factor.

The remaining fifteen supported entries are diagonal singleton blocks
forming three edge-disjoint perfect matchings, one per colour.

This covers all three ten-vertex 2-factor types with odd components.  It does
not by itself cover `C10`, `C4+C6`, supports below the equality boundary,
or the global conjecture.

The all-odd `C3+C7` and `C5+C5` cases are also consequences of the
arbitrary-order analytic theorem in
[`ODD_FULL_FACTOR_ONE_TERM_THEOREM.md`](../../arbitrary-order/ODD_FULL_FACTOR_ONE_TERM_THEOREM.md).
The mixed odd/even `C3+C3+C4` case still needs the finite audit here.

## Immediate obstruction

Every support in all three families has a nonmonochromatic colouring with exactly
one active perfect matching.  All five entries in that matching belong to
the fixed nonzero support, so their product is nonzero.  The corresponding
forbidden amplitude is therefore one nonzero monomial and cannot equal zero.
No cancellation algebra or SAT solver is needed.

The obstruction is abundant:

```text
factor type    raw factorizations   orbits   minimum one-term colourings
C3+C7                     458,094    5,558                         20,102
C5+C5                     460,690    2,536                         14,325
C3+C3+C4                  458,352      906                          3,204
```

Across every labelled full factor and all six global colour assignments,
the three audits represent 186,216,226,560 labelled coloured supports.

## Independent audit

For each factor type, the final verifier independently:

1. regenerates every perfect matching disjoint from the fixed factor;
2. recounts every unordered edge-disjoint triple;
3. reconstructs the complete factor automorphism group;
4. verifies every canonical representative, orbit size, and total coverage;
5. reconstructs the support skeleton and all its perfect matchings;
6. replays the stored colouring and checks that its activity is exactly the
   one recorded supported matching.

Pinned final manifests:

```text
tmp/ten_vertex_c3_c7_equality_family_verified.json
SHA-256
  ad7bd32a4695799aefc811a2e337c4a420df44e2b7ba09a0d20e3ad86c47d7d7

tmp/ten_vertex_c5_c5_equality_family_verified.json
SHA-256
  7a2955bc114138b5e88fc620bca33e540217a466b7c92541fa8be33a7862bbce

tmp/ten_vertex_c3_c3_c4_equality_family_verified.json
SHA-256
  e2a6cd03baa088eae723c83d4928329b5cab1904c302454353e348d5265a6738
```

With the bundled dependencies on `PYTHONPATH`, run:

```text
python claims/finite/n10/verify_ten_vertex_odd_factor_equality_family.py --orbits tmp/ten_vertex_c3_c7_equality_support_orbits.json --certificates tmp/ten_vertex_c3_c7_equality_support_one_term.json --output tmp/ten_vertex_c3_c7_equality_family_verified.json

python claims/finite/n10/verify_ten_vertex_odd_factor_equality_family.py --orbits tmp/ten_vertex_c5_c5_equality_support_orbits.json --certificates tmp/ten_vertex_c5_c5_equality_support_one_term.json --output tmp/ten_vertex_c5_c5_equality_family_verified.json

python claims/finite/n10/verify_ten_vertex_odd_factor_equality_family.py --orbits tmp/ten_vertex_c3_c3_c4_equality_support_orbits.json --certificates tmp/ten_vertex_c3_c3_c4_equality_support_one_term.json --output tmp/ten_vertex_c3_c3_c4_equality_family_verified.json
```

All three outputs must contain `"verified": true`.
