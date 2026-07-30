# Alternating-gate obstruction in normalized `q4_211`

## Status

This note exactly excludes the rank-one marked-`Delta_2` gates in the
generic adjacent incidence stratum of normalized `q4_211`.

Assume

```text
b c != 0
```

and that a mode `A` contains both singleton normals

```text
h_1=(b,0,0,-1,0),
h_2=(c,0,0,0,-1).
```

If both cross residuals at `A` are nonzero, the adjacent-pencil theorem
produces a marked `P_4 -> Delta_2`.  The all-rank-two slice family was
already excluded by the pair-image obstruction.  The alternating-gate
classification now excludes every rank-one slice boundary as well.
Therefore the two-cross-residual marked boundary is empty.

This closes one exact branch.  It does **not** exclude the separate
one-cross-residual boundary, all adjacent incidence, normalized
`q4_211`, `P_5 -> Delta_3`, or the global Krenn--Gu conjecture.

## The third-colour extension

Use the four-space and ordered basis from the adjacent reduction:

```text
H=span(e_1,e_2,w_+,w_-),
w_+=e_0+b e_3-c e_4,
w_-=e_0-b e_3+c e_4.
```

Its annihilator is

```text
H^perp=C n,   n=(0,0,0,c,b).                        (1)
```

After changing the two singleton target bases, the marked binary rows
at each of the other three modes are the pullbacks

```text
alpha_i=L_i^* e_2^*,
beta_i =L_i^* e_1^*.
```

Put

```text
gamma_i=L_i^* e_0^*.
```

The full adjacent identity, not merely its binary projection, says
that the image on `H` has no coefficient involving any `gamma_i`.
For each mode `i`, let

```text
S_i:H^* -> (C^2) tensor 3                            (2)
```

be the one-mode slice map obtained by using an arbitrary row at mode
`i` and the two marked rows at the other three modes.  Then

```text
gamma_i|H in ker(S_i).                               (3)
```

This converts the lifting problem into the one-mode conciseness of the
two alternating-gate normal forms.

## Transverse gate stratum

Use the notation

```text
lambda=pt+qr,   Delta=pt-qr,
lambda Delta != 0
```

and the normal form (3) in
[`P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md`](P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md).
In lexicographic order on the eight binary choices at the other modes,
the following four-row minors of the `8 x 4` matrices in (2) are:

```text
det S_1[{0,1,3,7},:] = -Delta^4 lambda^3,
det S_2[{0,4,6,7},:] = -Delta^4 lambda^3,
det S_3[{0,1,5,7},:] = -Delta^2 lambda.              (4)
```

Thus every `S_i` is injective.  Equation (3) gives

```text
gamma_1|H=gamma_2|H=gamma_3|H=0.
```

Each ambient map has rank three, so pullback on target covectors is
injective and no `gamma_i` is zero.  By (1),

```text
gamma_i in C^* n,   i=1,2,3.                        (5)
```

Now contract the original `P_5 -> Delta_3` identity by these three
rows.  On the source side,

```text
(n,n,n) contract P_5=0                              (6)
```

because `n` is supported on only source coordinates `3,4`.  On the
target side, the three covectors are nonzero multiples of `e_0^*`, so
the same contraction leaves the nonzero tensor

```text
lambda_0 e_0 tensor e_0
```

at the distinguished mode and mode `A`.  This contradicts (6) and
excludes the transverse stratum.

## Tangent gate stratum

For the tangent form (4), with `pq != 0`, exact row reduction gives

```text
rank(S_1)=rank(S_2)=4,
rank(S_3)=2,
ker(S_3)=span(e_2^*,e_3^*).                         (7)
```

For example, the same four-row minors for `S_1,S_2` are both

```text
-8p^3q^3.
```

Therefore the two gate modes have

```text
gamma_1,gamma_2 in C^* n.                           (8)
```

Double contraction gives

```text
(n,n) contract P_5=2bc x_0x_1x_2,                  (9)
```

which is a nonzero `P_3` on

```text
K=span(e_0,e_1,e_2).
```

On the target side, (8) leaves a nonzero pure `e_0^3` tensor through
the distinguished mode, mode `A`, and mode three of the tangent form.

The distinguished map has row plane on `K`

```text
span((a,1,1),(1,0,0)),
```

whose normal is

```text
m_0=(0,1,-1).                                       (10)
```

The two marked rows at tangent mode three restrict to

```text
((z_2+z_3)/2,p,q),
((d_2+d_3)/2,p,-q).                                 (11)
```

Their projections to the last two coordinates have determinant

```text
-2pq != 0.                                          (12)
```

Equation (7) also says that the selected third-colour row at this mode
restricts to a multiple of `(1,0,0)` on `K`.

Before applying the decomposable-`P_3` theorem, note that the
restriction at `A` cannot have rank one.  Both `h_1|K` and `h_2|K`
are nonzero multiples of `(1,0,0)`.  If the whole restriction at `A`
had rank one, its selected `e_0` row and the selected third-colour row
in (7) would both be supported on source coordinate zero.  Their
permanent with the distinguished row would vanish, contrary to the
nonzero pure coefficient coming from (9).

All three remaining restrictions therefore have rank at least two.
The nonzero decomposable-`P_3` classification makes all three ranks
exactly two and gives one common coordinate support for their plane
normals.

There are only two incidence placements to consider.

### Mode three carries a singleton incidence

On `H`,

```text
h_1|H=2b e_3^*,   h_2|H=2c e_2^*.                  (13)
```

The first tangent gate plane contains `e_2^*` but not `e_3^*`; the
second contains `e_3^*` but not `e_2^*`; the third contains neither.
Because the first two full restrictions have rank two by (7), they
cannot carry the opposite singleton incidence.

If tangent mode three is the `h_1`-mode or `h_2`-mode, (13) supplies
the row `(1,0,0)` on `K`.  Together with the two rows in (11), whose
last-coordinate projections are independent by (12), its restriction
has rank three.  This contradicts the `P_3` rank-two conclusion.

### Mode three is the remaining mode

The only other placement aligns the two gates:

```text
the h_1-mode is gate two,
the h_2-mode is gate one,
mode three is the remaining mode.
```

By (10), the common normal support in the `P_3` sign chart is
`{1,2}`.  Hence the row plane at the remaining mode must contain
`(1,0,0)`.  But its two independent marked rows are (11), and (12)
shows that no nonzero linear combination of them can cancel both last
coordinates.  Their span does not contain `(1,0,0)`, a contradiction.

This excludes the tangent stratum and completes the alternating-gate
obstruction.

## Consequence

In the generic adjacent incidence type `bc != 0`, the branch with both
cross residuals nonzero is now completely excluded:

- the all-rank-two marked family fails the pair-image flattening;
- every rank-one marked slice has the alternating form above;
- both its transverse and tangent lifting strata are impossible.

The adjacent reduction therefore leaves only the one-cross-residual
case, where another ambient row space contains `n`.  That fourth-normal
incidence, the disjoint common-kernel boundary, and the parameter
strata remain open.

## Verification

Run:

```text
python verify_p5_q4_211_alternating_gate_obstruction.py
python audit_p5_q4_211_alternating_gate_obstruction.py
```

The primary verifier reconstructs the three slice matrices, checks the
minors and kernels in (4), (7), differentiates (6), (9), and verifies
the two-dimensional determinant (12).  The independent audit rebuilds
the permanent slice maps by dynamic programming and row-reduces them
projectively over `F_5,F_7`; it also independently checks the double-
and triple-normal contractions.  It enumerates no ambient maps or
Grassmannians.  The finite-field checks audit the formulas; the
obstruction above is over `C`.
