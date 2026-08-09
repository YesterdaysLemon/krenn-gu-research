# Ten-vertex `C4+C6` equality-support certificate

## Claim

For `n=10`, `d=3`, consider the support with the following three diagonal
singleton perfect matchings:

```text
colour 0: 12 49 05 36 78
colour 1: 38 04 17 25 69
colour 2: 07 58 46 23 19
```

and full `3 x 3` blocks on

```text
01 06 18 24 26 37 39 48 57 59.
```

The ten full edges form a disjoint `C4+C6` 2-factor, the full skeleton is
5-regular with 25 edges, and the support has 105 nonzero matrix entries.
There is no assignment of nonzero complex values to those 105 entries whose
perfect-matching amplitudes equal the three-colour monochromatic target.

This is a theorem about one explicit support.  It does not exclude other
ten-vertex supports and does not prove the global Krenn--Gu conjecture.

The later exhaustive result
[`TEN_VERTEX_C4_C6_FAMILY_CERTIFICATE.md`](TEN_VERTEX_C4_C6_FAMILY_CERTIFICATE.md)
now excludes every support in this `C4+C6` equality architecture.  This
file retains the independent factor-lattice/DRAT proof for the original
support as a cross-check.

## Three-amplitude proof

Number the skeleton perfect matchings in the deterministic verifier order.
For colouring

```text
(0,0,1,0,0,2,0,1,0,1)
```

the forbidden amplitude has exactly matchings `8,11,49,50`.  Their exponent
vectors satisfy

```text
v8 + v50 = v11 + v49.
```

Consequently the four-term Laurent polynomial factors as a nonzero monomial
times `(1+x^r)(1+x^s)`, where `r` is the alternating `C4` direction and `s`
the alternating `C6` direction.  Its required vanishing forces
`x^r=-1` or `x^s=-1`.

The first alternative is impossible.  At colouring

```text
(0,0,0,0,0,2,1,1,2,1)
```

the seven active matchings split into three pairs
`(8,11),(38,41),(49,50)` whose exponent differences are `+/-r`, plus the
unpaired matching `3`.  If `x^r=-1`, the three pairs cancel and matching
`3` leaves a nonzero monomial in a forbidden amplitude.

The second alternative is impossible in exactly the same way.  At colouring

```text
(0,0,1,0,0,0,0,0,0,1)
```

the five active matchings split into the two `+/-s` pairs
`(8,49),(11,50)` plus the unpaired matching `2`.

Thus the first amplitude forces one of two relations, while the other two
amplitudes rule out both.  The exact replay is
`verify_ten_vertex_three_amplitude_certificate.py`; no numerical assumption
or SAT solver is needed for this proof.

## Exhaustive factor audit

The skeleton has 68 perfect matchings.  Each colouring for which only the
four full-factor matchings are active gives

```text
monomial * (1 + x^r) * (1 + x^s) = 0.
```

Because all selected entries are nonzero, at least one of the two signed
relations `x^r=-1` or `x^s=-1` must hold.  Exhausting all `3^10=59,049`
colourings gives 34,001 two-way clauses on 656 distinct relations.

Exact signed-quotient reduction found eleven no-goods, but the direct
three-amplitude proof shows that only two unary no-goods and their common
factor clause are necessary.  The larger resulting CNF has 656 variables
and 34,012 clauses and is UNSAT; it is retained as redundant exhaustive
evidence.

## Independent verification

`verify_ten_vertex_equality_factor_lattice.py` does not import the
exploratory producer.  It independently reconstructs:

1. the support, 5-regular skeleton, and 68 perfect matchings;
2. all 59,049 activities and 34,001 factor clauses;
3. all 656 relation vectors in deterministic order;
4. each one- or three-relation no-good using exact `Fraction` arithmetic
   and a separately found unimodular coordinate minor;
5. the canonical DIMACS bytes.

Kissat then emits a raw binary DRAT trace.  The independent `drat-trim`
binary replays it with `s VERIFIED`, and
`verify_ten_vertex_equality_factor_lattice_final.py` checks the complete
hash chain.

Pinned artifact hashes:

```text
CNF   3540268a767a04d3f42413f9150dd190bcb22da470d2bf3f2dbe557d2adb2e42
DRAT  5cf109f5c4d5b7784bbc30e627df683ab07f7483deda4b7f79228a1a0f6e0ea2
bytes 2275
```

The final manifest is:

```text
tmp/ten_vertex_c4_c6_equality_factor_lattice_final_verified.json
```

## Audit

With the bundled dependencies on `PYTHONPATH`, run:

```text
python claims/finite/n10/verify_ten_vertex_equality_factor_lattice.py
python claims/finite/n10/verify_ten_vertex_equality_factor_lattice_final.py
python claims/finite/n10/verify_ten_vertex_three_amplitude_certificate.py
```

Both commands must finish successfully, and the final JSON must contain
`"verified": true`.
