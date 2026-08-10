# Two-gate reduction for adjacent one-cross normalized `q4_211`

## Status

This note sharpens the four-gate conclusion of the one-cross
direction-conic theorem on

```text
a b c != 0.
```

The second-common-mode and double-normal-plane gates are impossible or
force one of the other gates.  Consequently every surviving generic
adjacent one-cross branch satisfies at least one of:

```text
span(u_1,u_2) subset R_i                            (1)
```

at a remaining mode, or

```text
L_A(e_1+e_2)=0
or
L_Y(e_1+e_2)=0,                                     (2)
```

where `A` is the original `h_1,h_2` common mode and `Y` is the
mandatory opposite-pencil mode.

The two gates (1)--(2) have since both been excluded: target-colour
support rules out (1), while binary kernel polarity and two
incompatible polarized `P_3` charts rule out (2).  Thus, after combining
the present reduction with those later theorems, adjacent one-cross
incidence is empty on `abc != 0`.  See:

- [`P5_Q4_211_ONE_CROSS_DIRECTION_PLANE_OBSTRUCTION.md`](P5_Q4_211_ONE_CROSS_DIRECTION_PLANE_OBSTRUCTION.md)
- [`P5_Q4_211_ONE_CROSS_COMMON_KERNEL_OBSTRUCTION.md`](P5_Q4_211_ONE_CROSS_COMMON_KERNEL_OBSTRUCTION.md)

This note itself is the exact two-gate reduction, not the proof of
those later gate exclusions or a resolution of all normalized
`q4_211`, `P_5 -> Delta_3`, or the global Krenn--Gu conjecture.

## A common mode cannot also contain `n`

Every occurrence of

```text
n=(0,0,0,c,b)
```

pulls back from target `e_0^*`.  At an `h_1,h_2` common mode, write
their target covectors as

```text
x=(r,0,q),
y=(t,p,0).
```

If that mode also contained `n`, injectivity of pullback would force

```text
p q != 0.
```

Indeed, `q=0` would make `x` proportional to the target covector of
`n`, and `p=0` would do the same to `y`.  But `pq != 0` is precisely
the two-cross marked boundary already excluded by the alternating-gate
theorem.  Therefore

```text
n notin R_i
```

at every `h_1,h_2` common mode.                      (3)

## Excluding a second common mode

Suppose two modes contain both `h_1,h_2`.  The parallel-incidence
theorem forces a third common mode.  There cannot be four, because the
one-cross rank-drop theorem at any common mode requires another mode
containing `n`, contrary to (3).  Thus exactly three modes are common,
and the fourth mode `D` contains `n`.

At each common mode, the two cross scalars are not both zero and cannot
both be nonzero.  Hence each has one of two orientations:

- in the `q` orientation, `h_2` pulls back from target `e_0^*`;
- in the `p` orientation, `h_1` pulls back from target `e_0^*`.

The normal-pencil theorem says that a `q`-oriented common mode forces
some other mode to contain `span(h_1,n)`.  Since `D` is the only
`n`-mode, this puts `h_1` in `R_D`.  A `p` orientation similarly puts
`h_2` in `R_D`.

If both orientations occurred, `D` would contain `h_1,h_2,n`,
contrary to (3).  All three common modes therefore have the same
orientation.

If all are `q`-oriented, contract at those three modes by `h_2`.
The source contraction vanishes:

```text
(h_2,h_2,h_2) contract P_5=0,                       (4)
```

because `h_2` is supported on only source coordinates `0,4`.  The
three target covectors are nonzero multiples of `e_0^*`, so the target
contraction leaves the nonzero tensor

```text
lambda_0 e_0 tensor e_0
```

at the distinguished mode and `D`.  This contradicts (4).  The
all-`p` case is identical with `h_1`, which is supported on
coordinates `0,3`.  Hence no second common mode exists.

## Absorbing the double-normal gate

Stay in the `q` orientation.  The normal-pencil theorem supplies a
mode `Y` containing `span(h_1,n)`.  Suppose another remaining mode
`Z` contains

```text
span(h_2,n).                                        (5)
```

By (3), `Y` and `Z` are distinct and neither is a common mode.

Assume neither gate (1) nor (2) occurs.  The direction-conic theorem
then assigns to the two modes other than `A,Y` the two direction lines

```text
C u_2,   C m,
m=c u_1-b u_2=b h_2-c h_1.                         (6)
```

The mode `Z` is one of those two modes.  If it receives `C m`, its
rows `h_2,m` span `h_1`, making it an `h_1,h_2,n` common mode,
contrary to (3).  If it receives `C u_2`, the identity

```text
b u_2=c h_1+n                                      (7)
```

again puts `h_1` in its row space, with the same contradiction.
Therefore (5) forces (1) or (2).

In the `p` orientation the double-normal plane is `span(h_1,n)` and
the direction lines are `C u_1,C m`.  The identities

```text
m=b h_2-c h_1,
c u_1=b h_2+n                                      (8)
```

give the identical conclusion.

Combining this with the four-gate theorem leaves only (1)--(2).

## Consequence

On `abc != 0`, the normalized incidence analysis now reads:

- parallel minimal incidence is impossible;
- exact disjoint incidence is impossible;
- adjacent two-cross incidence is impossible;
- adjacent one-cross incidence lies on the union of only two explicit
  Schubert/kernel divisors, (1)--(2).

Thus no free normal-pencil, binary-cubic, or conic-polar stratum
remains.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q4_211_one_cross_two_gate.py
python claims/p5/frontier/audit_p5_q4_211_one_cross_two_gate.py
```

The primary verifier checks (4), the linear identities (6)--(8), and
the independence implications at a common mode.  The independent audit
rebuilds the triple-normal contractions and the projective line spans
over `F_5,F_7`.  It enumerates no ambient maps or Grassmannians.  The
finite-field checks audit the formulas; the reduction above is over
`C`.
