# Marked-`Delta_2` pair-image obstruction in normalized `q4_211`

## Status

This is an exact characteristic-zero obstruction inside the generic
adjacent incidence type of normalized `q4_211`.

Assume `bc != 0`, one remaining mode `A` contains both singleton
normals, a distinct mode `B` contains `h_1`, and a distinct mode `C`
contains `h_2`.  If both cross-residual scalars at `A` are nonzero, the
adjacent pencil reduction produces a marked restriction

```text
P_4 -> Delta_2.
```

The all-rank-two slice family classified in
[`P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md`](P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md)
is incompatible with the two incidences at `B,C`.  Therefore every
surviving marked-`Delta_2` branch has a rank-one coordinate-deleted
slice and hence a singleton target row in one of the normal pencils

```text
C h_1+C n,   C h_2+C n,
n=(0,0,0,c,b).                                      (1)
```

The later alternating-gate theorem excludes all of those rank-one
marked lifts as well.  This note supplies the all-rank-two half of the
complete two-cross-residual obstruction.  It does **not** exclude the
separate one-cross fourth-normal incidence, the whole adjacent type,
normalized `q4_211`, `P_5 -> Delta_3`, or the global Krenn--Gu
conjecture.

## The marked planes

Use the source basis

```text
(e_1,e_2,w_+,w_-)
```

of the four-space `H` in the adjacent reduction.  The common-mode
quotient has row space

```text
U_0=span(e_2^*,e_3^*).                               (2)
```

If all six coordinate-deleted maps have rank two, the three
two-colour row planes at the other modes have, up to the symmetries in
the slice classification, bases

```text
U_1=span((0,1,T,-B),(1,0,0,-A)),
U_2=span((1,0,0,A),(0,1,-T,B)),
U_3=span((1,0,0,A),(B,A,-AT,0)),                    (3)
```

where

```text
A T != 0.
```

Neither `e_2^*` nor `e_3^*` belongs to any plane in (3).  At the
`h_1`-mode, equation

```text
h_1 restricted to H=2b e_3^*
```

therefore raises the restricted row space to the hyperplane

```text
R_B=U_i+C e_3^*.
```

Similarly

```text
R_C=U_j+C e_2^*
```

for two distinct indices `i,j`; let `k` be the third index.  The
remaining mode has row space containing `U_k`.

## Pair-image flattening

Let `E_6` be the six-dimensional space indexed by unordered pairs of
the four source coordinates.  For row spaces `U,V`, define

```text
A(U,V)=span{
 (u_r v_s+u_s v_r)_(r<s):u in U,v in V
} subset E_6.                                        (4)
```

The `BC|AD` flattening of `P_4` is the nondegenerate complement pairing
between

```text
A(R_B,R_C)
```

and

```text
A(U_0,R_D).
```

Consequently its rank is at least

```text
dim A(R_B,R_C)+dim A(U_0,R_D)-6.                     (5)
```

For every one of the six assignments of the planes in (3) to
`B,C,D`, direct symbolic row reduction gives

```text
dim A(R_B,R_C)=6,
dim A(U_0,U_k)=4.                                    (6)
```

The first equality is certified by the following nonzero `6 x 6`
minors, in assignment order:

```text
 4 A T,
 4 A^3 T,
-4 A T,
-4 A^4 T,
-4 A^3 T,
-4 A^2 T.                                           (7)
```

The second equality follows from four-column minors equal, respectively,
to

```text
-A^2,-1,-A^2,-1,-1,-1.                              (8)
```

Since `R_D` contains `U_k`, its pair image with `U_0` has dimension at
least four.  Equations (5)--(8) force flattening rank at least

```text
6+4-6=4.                                             (9)
```

But the marked tensor image is `Delta_2`, whose every `2|2`
flattening has rank two.  This contradiction excludes the entire
all-rank-two family.

## Remaining adjacent boundary

The slice classification now forces a rank-one local map in at least
one of the two pure cubic slices.  The annihilating singleton row is
`e_2^*` or `e_3^*` modulo `H^perp`.  Returning to the original source
coordinates gives exactly the two pencils in (1).

The alternating-gate classification shows that the rank-one boundary
has exactly one gate of each type at distinct modes.  Its transverse
stratum makes all three third-colour rows proportional to `n`, which
contradicts the zero triple-`n` contraction.  Its tangent stratum is
excluded by a double-`n` `P_3` sign-support argument.  See
[`P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md`](P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md)
and
[`P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md`](P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md).

Consequently the whole two-cross marked boundary is empty.  The
generic adjacent incidence type is now confined to the one-cross
branch, where a row space actually contains `n`.  Closing that
fourth-normal incidence, plus the disjoint common-kernel and parameter
boundaries, remains necessary for a `q4_211` exclusion.

## Verification

Run:

```text
python verify_p5_q4_211_marked_delta2_pair_image.py
python audit_p5_q4_211_marked_delta2_pair_image.py
```

The primary verifier reconstructs all six pair-image matrices
symbolically and checks the minors in (7)--(8).  The independent audit
rebuilds the pair images by modular row reduction over `F_3,F_5` at
every nonzero `A,T` and every `B`, for all six plane assignments.  It
enumerates no ambient maps or Grassmannians.  The finite-field checks
audit the formulas; the proof above is over `C`.
