# Alternating-gate classification for marked `P_4 -> Delta_2`

## Status

This is an exact characteristic-zero classification of the rank-one
slice boundary left open in
[`P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md`](P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md).

Use source coordinates `0,1,2,3`, put

```text
U_0=span(e_2^*,e_3^*),
```

and write the two marked rows at the other modes as

```text
alpha_i,beta_i in (C^4)^*,   i=1,2,3.
```

Assume that the only nonzero binary coefficients are

```text
Perm(e_2^*,alpha_1,alpha_2,alpha_3) != 0,
Perm(e_3^*, beta_1, beta_2, beta_3) != 0.            (1)
```

If one coordinate-deleted local map has rank one, then:

1. exactly one `013`-slice mode has rank one;
2. exactly one `012`-slice mode has rank one; and
3. those two modes are distinct.

Equivalently, after permuting modes `1,2,3`, there are precisely the
two alternating gates

```text
beta_1 in C e_2^*,   alpha_2 in C e_3^*.             (2)
```

After rescaling marked rows, every such tensor is in exactly one of
the following two determinant strata.

### Transverse stratum

Choose

```text
lambda=p t+q r != 0,
Delta =p t-q r != 0
```

and arbitrary `x_2,x_3,y_2,y_3`.  Then

```text
alpha_1=(p,q,x_2,x_3)       beta_1=(0,0,1,0)
alpha_2=(0,0,0,1)           beta_2=(r,-t,y_2,y_3)

alpha_3=(Delta r, Delta t, lambda y_2, lambda y_3)
beta_3 =(Delta p,-Delta q,-lambda x_2,-lambda x_3).  (3)
```

The two diagonal coefficients are `Delta lambda` and
`-Delta lambda`.

### Tangent stratum

Choose

```text
p q != 0
```

and arbitrary `z_2,z_3,d_2,d_3`.  Then

```text
alpha_1=(p,q,0,0)       beta_1=(0,0,1,0)
alpha_2=(0,0,0,1)       beta_2=(p,-q,0,0)
alpha_3=(p,q,z_2,z_3)   beta_3 =(p,-q,d_2,d_3).      (4)
```

The two diagonal coefficients are `2pq` and `-2pq`.

Conversely, (3) and (4) have exactly the support in (1).  Together
with the all-rank-two family in the earlier classification, these two
strata exhaust the marked binary boundary.  This classification alone
does **not** exclude `P_4 -> Delta_2`, normalized `q4_211`,
`P_5 -> Delta_3`, or the global Krenn--Gu conjecture.

## Why the gates alternate

Selecting `e_2^*` at mode zero leaves the permanent on

```text
J_2=span(e_0,e_1,e_3),
```

with pure output supported at `alpha_1 alpha_2 alpha_3`.  A rank-one
local map in this slice therefore has

```text
beta_i|J_2=0,
```

or `beta_i in C e_2^*`.  Two such gates would put two rows supported
on coordinate two into the second nonzero permanent in (1), making it
zero.  Hence there is at most one `e_2^*` gate.  The same argument
gives at most one `e_3^*` gate.

Suppose `beta_1=e_2^*` and there is no `e_3^*` gate.  All three local
maps in the `J_3=span(e_0,e_1,e_2)` pure slice then have rank two.
The nonzero decomposable-`P_3` classification applies.  The plane at
mode one contains `e_2^*`, so the common normal support of its sign
chart is `{0,1}`.  In the marked support-two chart, after harmless row
rescalings, the pure-`beta` rows have the pattern

```text
beta_1=e_2^*,
alpha_2=e_2^*,
alpha_3=e_2^*.                                      (5)
```

This is the `B=0` boundary of the canonical sign chart, with
`alpha,beta` interchanged.  Returning to four coordinates, (5) says
that both `alpha_2` and `alpha_3` lie in

```text
span(e_2^*,e_3^*).
```

Their restrictions to `J_2` are therefore both multiples of
`e_3^*`, which makes the first nonzero coefficient in (1) vanish.
This contradiction forces an `e_3^*` gate.  The argument with the two
slices interchanged is identical.

The two gates cannot occur at the same mode.  If

```text
beta_1=e_2^*,   alpha_1=e_3^*,
```

let

```text
B(v,w)=v_0 w_1+v_1 w_0
```

on the shared coordinate plane.  The pure and mixed coefficients in
the `J_2` slice respectively require

```text
B(alpha_2,alpha_3) != 0,
B(beta_2,beta_3)=0.
```

The `J_3` slice requires the reverse two statements.  This is
impossible.  Thus the two unique gates lie at distinct modes, proving
(2).

## Solving the four remaining equations

Normalize (2) and write the shared-coordinate parts as

```text
alpha_1=(p,q,x_2,x_3),
alpha_3=(r,t,z_2,z_3).
```

The two nonzero diagonal coefficients force

```text
lambda=p t+q r != 0.                                (6)
```

The two mixed bilinear coefficients force the shared parts of the
opposite marked rows to be orthogonal for `B`.  Rescale those rows to
obtain

```text
beta_2=(r,-t,y_2,y_3),
beta_3=(p,-q,d_2,d_3).                              (7)
```

Put `Delta=pt-qr`.  Direct permanent expansion now leaves only four
mixed equations:

```text
lambda y_j-Delta z_j=0,
-lambda x_j-Delta d_j=0,   j=2,3.                  (8)
```

If `Delta != 0`, solving (8) and clearing its denominator by rescaling
the two rows at mode three gives (3).

If `Delta=0`, equation (6) says that `(r,t)` is proportional to
`(p,q)` and that `pq != 0`.  Equations (8) force

```text
x_2=x_3=y_2=y_3=0,
```

while `z_2,z_3,d_2,d_3` remain free.  Rescaling the proportional rows
gives (4).  This proves completeness.

Geometrically, `Delta=0` is the tangency divisor where the two
shared-coordinate directions coincide, while `lambda != 0` keeps
them nonorthogonal for the permanent polarity.  Thus (3)--(4) are a
two-stratum orbit description, not a point search.

## Verification

Run:

```text
python claims/p4/boundaries/verify_p4_marked_delta2_alternating_gate.py
python claims/p4/boundaries/audit_p4_marked_delta2_alternating_gate.py
```

The primary verifier expands all sixteen coefficients in both normal
forms, reconstructs the four equations (8), and checks the same-mode
gate contradiction.  The independent audit uses a dynamic-programming
permanent and audits the transverse/tangent nullspaces over `F_5` and
`F_7`, projectively in the two shared directions.  It enumerates no
ambient maps or Grassmannians.  The finite-field calculation audits
the formulas and case split; the classification above is over `C`.
