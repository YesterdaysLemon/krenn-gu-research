# Complete exclusion theorem for normalized `q4_211`

## Status

This is an exact tensor theorem over `C`:

```text
There is no normalized q4_211 restriction of P_5 to Delta_3.          (1)
```

The proof is the logical closure of the generic incidence theorem and
the three parameter-boundary theorems.  It uses projective pencils,
conic polarity, binary polarization, complement-pairing flattenings,
Grassmannian degeneracy loci, and the exact ternary permanent
classification.  It does not search over ambient local maps.

This completes the normalized partial `q4_211` branch.  The zero-row
closure of the same four-coordinate support is covered separately by
the two-singleton theorem below.  The theorem does not by itself prove
`P_5 -> Delta_3` impossible: one-partial `3+1` and `2+2`
high-coordinate families remain.  It does not resolve the
arbitrary-order Krenn--Gu conjecture.

## Normal form and parameter cover

At the distinguished mode, the three target-coordinate pullbacks are

```text
u_0=(a,1,1,0,0),
u_1=(b,0,0,1,0),
u_2=(c,0,0,0,1).                                    (2)
```

If the fifth row is nonzero and noncoordinate, at least two of
`a,b,c` are nonzero.  With exactly one nonzero parameter it is itself a
coordinate row and belongs to a five-coordinate branch.  The remaining
closure `a=b=c=0` is a genuine zero row, not a coordinate row; it is
excluded by
[`P5_TWO_SINGLETON_COORDINATE_OBSTRUCTION.md`](../coordinate-cegar/P5_TWO_SINGLETON_COORDINATE_OBSTRUCTION.md).

Thus the partial `q4_211` branch has exactly four parameter strata:

```text
a b c != 0;
a=0, b c != 0;
b=0, a c != 0;
c=0, a b != 0.                                     (3)
```

## The generic stratum

On `abc!=0`, the singleton contractions expose two embedded copies of
`P_4` with normals

```text
h_1=(b,0,0,-1,0),
h_2=(c,0,0,0,-1).                                   (4)
```

Each normal occurs in at least two of the other four row spaces.  The
two containment sets have only the standard disjoint, adjacent, and
parallel selections.  Parallel incidence acquires a third common mode
and reselects as adjacent.

Exact disjoint incidence is excluded by a nondegenerate ternary-conic
polarity followed by kernel propagation.  Adjacent two-cross incidence
is excluded by the marked `P_4 -> Delta_2` slice classification and
complement flattening.  Adjacent one-cross incidence is reduced by a
normal pencil and direction conic to a direction-plane or common-kernel
gate; both gates are impossible.  Hence the entire generic stratum is
empty:

- [`P5_Q4_211_GENERIC_EXCLUSION_THEOREM.md`](P5_Q4_211_GENERIC_EXCLUSION_THEOREM.md)

## The `b=0` and `c=0` faces

On `b=0,ac!=0`, the first singleton normal becomes the coordinate row
`e_3`.  Exact coordinate-normal incidence leaves one marked
architecture.  Two pure target-label alternatives remain; a binary
polar system and two simultaneous `P_3` charts exclude both.  This
proves the `b=0` face empty.  Interchanging the singleton colours gives
the `c=0` face:

- [`P5_Q4_211_B0_COORDINATE_NORMAL_REDUCTION.md`](../coordinate-cegar/P5_Q4_211_B0_COORDINATE_NORMAL_REDUCTION.md)
- [`P5_Q4_211_B0_NONCOMMON_A_OBSTRUCTION.md`](P5_Q4_211_B0_NONCOMMON_A_OBSTRUCTION.md)
- [`P5_Q4_211_B0_FINAL_OBSTRUCTION.md`](P5_Q4_211_B0_FINAL_OBSTRUCTION.md)

## The `a=0` face

On `a=0,bc!=0`, the doubled-colour contraction is a third embedded
`P_4`, with normal

```text
h_0=e_1-e_2.                                       (5)
```

The original parallel theorem still applies and reselects parallel
singleton incidence as adjacent.

For adjacent incidence, the two-cross branch remains excluded.  In the
one-cross branch, the third normal occurs at both non-pencil modes and
one of those modes also contains a fixed singleton direction.  On the
four-dimensional support of (5), the rank-one target flattening turns
this into a degeneracy locus on `Gr(2,4)`.  The locus consists of five
ordered complete-quadrangle plane pairs.  Every pair has a
parameter-independent nonzero complementary `2x2` minor, so none maps
to the required pure tensor:

- [`P5_Q4_211_A0_ADJACENT_REDUCTION.md`](P5_Q4_211_A0_ADJACENT_REDUCTION.md)
- [`P5_Q4_211_A0_ADJACENT_GRASSMANN_OBSTRUCTION.md`](P5_Q4_211_A0_ADJACENT_GRASSMANN_OBSTRUCTION.md)

For exact disjoint incidence, the same third `P_4` has a zero marked
corner.  One marked `P_3` slice must vanish.  Three evaluations force
the other row spaces into one coordinate hyperplane, where the tensor
reduces to `P_3`.  The exact decomposable-`P_3` theorem makes those
three spaces planes, and their binary coefficient cube has a zero
antipodal corner incompatible with exact disjointness:

- [`P5_Q4_211_A0_DISJOINT_P3_OBSTRUCTION.md`](P5_Q4_211_A0_DISJOINT_P3_OBSTRUCTION.md)

Thus parallel, adjacent, and exact disjoint incidence are all empty on
the `a=0` face.

## Zero-row closure

When `a=b=c=0`, the distinguished rows have target-coordinate support
multiplicities

```text
2,1,1
```

plus one zero source row.  The two singleton target coordinates pull
back to distinct singleton source rows.  Contracting them exposes two
pure deleted copies of `P_4` sharing the other three source rows.  The
two-singleton theorem excludes this closure.

## Conclusion

The four nonzero partial strata in (3), together with the zero-row
closure, are exhaustive for a map with exactly four coordinate rows:

| parameter stratum | excluding theorem |
| --- | --- |
| `abc!=0` | generic exclusion |
| `a=0,bc!=0` | adjacent Grassmannian plus disjoint ternary-Segre obstructions |
| `b=0,ac!=0` | coordinate-normal final obstruction |
| `c=0,ab!=0` | singleton-colour image of the `b=0` obstruction |
| `a=b=c=0` | two-singleton coordinate obstruction |

Therefore (1) holds.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q4_211_exclusion.py
python claims/p5/frontier/audit_p5_q4_211_exclusion.py
```

The primary verifier pins the constituent theorem and verifier hashes
and checks the complete parameter cover, including the zero row.  The
independent audit reconstructs all partial parameter zero masks and
every pair of normal-containment sets of size at least two.  It checks
that each incidence pair is exact disjoint, adjacent, or
parallel-reselectable and that every resulting case lands in one of
the constituent theorems.  The zero-row census is independently
replayed by the two-singleton audit.  These package scripts do not
replace the symbolic primary and independently coded finite-field
audit attached to each constituent result.
