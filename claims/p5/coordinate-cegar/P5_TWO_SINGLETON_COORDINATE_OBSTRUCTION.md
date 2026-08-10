# Two-singleton coordinate obstruction for `P_5`

## Status

This is an exact tensor theorem over `C`.

Suppose one local map in a hypothetical restriction

```text
P_5 -> Delta_3
```

has two target coordinates whose pullbacks are supported on two
distinct singleton source rows.  Then the restriction is impossible.

More explicitly, after relabelling source and target coordinates, let
the five rows of the distinguished local map be `r_0,...,r_4` and
assume

```text
(r_j)_1=0 for j != 3,   (r_3)_1 != 0,
(r_j)_2=0 for j != 4,   (r_4)_2 != 0.                (1)
```

No condition is imposed on the target-coordinate-zero entries of the
five rows.  In particular, (1) includes:

- normalized `q5_311`;
- a `3+1` coordinate row with one partial row supported on the
  majority and missing target coordinates; and
- a `2+1+1` coordinate row together with one zero source row.

The result is the basis-free content of the existing `q5_311` proof.
It closes 360 of the 6,495 covered local pair signatures, but it does
not exclude the one-partial high-coordinate profiles with target
support multiplicities `(3,2,1)`, `(4,2,1)`, or `(3,3,1)`.

## Two pure deleted slices

Contract the distinguished target mode by the coordinate covectors
`e_1^*` and `e_2^*`.  By (1), their source pullbacks are nonzero
multiples of `e_3^*` and `e_4^*`.  The equality with `Delta_3`
therefore gives, through the other four local maps,

```text
P_5 contracted by e_3^* -> lambda_1 e_1^4,
P_5 contracted by e_4^* -> lambda_2 e_2^4,
lambda_1 lambda_2 != 0.                              (2)
```

The source tensors in (2) are two embedded copies of `P_4`.  They
share the three source rows

```text
M={0,1,2}
```

and have distinct exceptional rows `4` and `3`.  Notice that the
unused entries `(r_j)_0` do not occur anywhere in (2).

Every other local map has rank three because `Delta_3` is concise.
Deleting one source row lowers its rank by at most one, so all maps in
both copies of `P_4` have rank at least two.

## Rank-drop dichotomy

The decomposable-`P_4` rank-drop theorem applied to each tensor in (2)
says that at least two of the four remaining modes drop to rank two in
each deletion.

The shared-drop obstruction uses only the following data:

1. the two tensors in (2) are nonzero pure tensors in independent
   target directions;
2. their source `P_4` tensors share the three rows `M`; and
3. every full local map has rank three.

It does not use the `3,1,1` multiplicity of the distinguished row.
Consequently the two drop sets are disjoint.  They are therefore
two-element sets partitioning the four remaining modes:

```text
D_1={A,B},   D_2={C,D}.                              (3)
```

At every remaining mode the three rows on `M` span a plane.  For
example, at a mode in `D_1`, the common rows together with the
exceptional row retained in the first deletion have rank two, while
the other exceptional row raises the full map to rank three.  The
common rows can have neither rank one nor rank three.  The same
argument applies on `D_2`.

## Common-plane contradiction

Let

```text
B_i:C^3 -> P_i
```

be the restriction of remaining mode `i` to the common source rows,
where `P_i` is its two-dimensional image.  For each `i`, delete that
mode and restrict the other three common-row maps to `P_3`:

```text
S_i=(tensor over j != i of B_j)P_3.                  (4)
```

Contracting the appropriate pure deleted slice in (2) by a quotient
covector at mode `i` shows that every `S_i` is either zero or nonzero
decomposable.  The four-plane corollary of the exact
decomposable-`P_3` classification says:

```text
all four S_i are zero,
or all four S_i are nonzero decomposable.             (5)
```

If all are zero, the zero-`P_3` theorem makes the four common row
planes one coordinate plane.  One common source row is then killed in
every remaining mode, so both deleted `P_4` tensors in (2) vanish.

If all are nonzero, take the two modes outside `D_1`.  Quotienting at
the first gives a pure residual whose factor in the second mode is
`e_1`, so `e_1` lies in the second common image plane.  Quotienting at
that second mode must then give zero, contradicting (5).

Both alternatives are impossible.  This proves the theorem.

## Verification

Run:

```text
python claims/p5/coordinate-cegar/verify_p5_two_singleton_coordinate_obstruction.py
python claims/p5/coordinate-cegar/audit_p5_two_singleton_coordinate_obstruction.py
```

The primary verifier reconstructs the two singleton pullbacks and
pins the three exact structural inputs used above.  The independent
audit rebuilds the 6,495 covered support/pair signatures using its
separate finite-field catalogue implementation and finds exactly 360
with two singleton target supports.  It checks that their two unique
source rows are distinct and splits them into the three high-coordinate
families listed above.  The finite-field census audits only the scope;
the written proof is over `C`.
