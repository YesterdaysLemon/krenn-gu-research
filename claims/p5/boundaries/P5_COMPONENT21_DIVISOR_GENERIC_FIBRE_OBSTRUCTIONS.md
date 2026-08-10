# Divisor-generic `P_5` obstructions on component twenty-one

## Status

**Exact characteristic-zero theorem on four component divisors.**  The generic
marked `H31` and weighted `H22` fibres are empty on both finite parameter
endpoints `p=0,q!=0` and `q=0,p!=0`, on the genuine mode-three projective
divisor, and on the genuine mode-zero vertical-plane divisor of the
coincident-support rank-one star component.

These are generic-point statements on the named divisors, not a compactified
classification of every intersection among them.  On the vertical-plane
divisor the exceptional subloci

```text
(2 alpha ell+ell^2+1) k (ell^2-1)=0
```

remain separate and **UNKNOWN**, as do arbitrary ambient/source limits and
omitted Grassmann charts.  No result here is promoted to those fibres.  The
Krenn--Gu conjecture remains **UNRESOLVED**.

Throughout put

```text
A=X_0+X_1, C=X_0-X_1, B=X_2+X_3, D=X_2-X_3.       (1)
```

## The two finite endpoint divisors

At `p=0,q!=0` use

```text
a=(A, ell A+C, C, D),
b=(C+qB, A, B+kA, A+ell C),                       (2)
```

and at `q=0,p!=0` use

```text
a=(C, ell A+C, C, D),
b=(A+pB, A, B+kA, A+ell C).                       (3)
```

The only pure coefficient is respectively `T_1111=4q` or `4p`.

For every affine marking `b_i+h_i a_i`, the four marked-`H31` mixed row
modules have exact standard-basis sizes

```text
(2,2,7,7).                                        (4)
```

In each case the all-alpha diagonal has zero normal form and the all-beta
diagonal has nonzero normal form.  Hence no genuine binary neighbour exists.

For weighted `H22`, the homogeneous `D01` all-alpha direction is
Hall-deficient.  On finite `D23`, normalize the all-alpha diagonal to one.
The all-beta diagonal then has zero normal form, and the exact marking
projection is

```text
<lambda+1,h3,F1,F2,F3>,                           (5)
```

where `E=ell^2-1` and

```text
F1=kE h0h1-h0h2+E h1h2+k ell h0+ell h2-k,
F2=(h2^2-k^2)(h0+(1-ell^2)h1-ell),
F3=(h2^2-k^2)(((ell-1)h1+1)((ell+1)h1+1)).        (6)
```

At weight infinity, the all-alpha row belongs to the mixed row module, whose
standard basis has size seven, while the all-beta row does not.  Thus every
weight chart loses one required diagonal.

## The genuine mode-three projective divisor

At projective parameter `[r:s]=[0:1]`, equivalently `U_3=<C,D>`, use

```text
a=(qA-pC, A, C, D),
b=(A+pB, C, B+kA, C).                             (7)
```

Only `T_1111=-4p` is nonzero.  The marked-`H31` row-module output is again
(4).  `D01` is Hall-deficient for weighted `H22`.  On finite normalized
`D23`, the all-beta diagonal belongs to the mixed ideal and the projection is

```text
<lambda+1,h3,G1,G2,G3>,                           (8)
```

with `delta=p^2-q^2` and

```text
G1=delta k h0h1+delta h0h2-p h1h2-qk h1-qh2-pk,
G2=(h2^2-k^2)(delta h0-p h1-q),
G3=(h1^2-1)(h2^2-k^2).                            (9)
```

At weight infinity the all-alpha row is in the size-seven mixed module and
the all-beta row is not.  This closes the generic point of the genuine
mode-three projective divisor for both fibre types.

## The mode-zero vertical-plane divisor

Put

```text
U_0=<A-alpha C,B>, U_1=<A,C>,
U_2=<C,B+kA>,     U_3=<A+ell C,D>,                (10)
```

and choose pure bases

```text
a=(A-alpha C, ell A+C, C, D),
b=(B, A, B+kA, A+ell C).                          (11)
```

Only `T_1111=4` is nonzero.  Write

```text
E=2 alpha ell+ell^2+1.                            (12)
```

For marked `H31`, source deletions zero and one are Hall/row-module
obstructed.  For each of deletions two and three, the complete saturated
binary projection is

```text
<h0,h3,h2-k ell,E h1+alpha+ell>.                  (13)
```

On this branch the mixed matrix has rank six and kernel basis

```text
e0=(-alpha ell-1,0,ell,0;0,1,0,0),
e1=(0,0,0,+/-1;1,0,1,0),                          (14)
```

with plus for deletion two and minus for deletion three.  For
`z=s e0+w e1`, the two diagonals are

```text
d0=-2Es, d1=-2(k(ell^2-1)s-2w)       (deletion 2),
d0=+2Es, d1=-2(k(ell^2-1)s-2w)       (deletion 3). (15)
```

The mode-three one-marked determinant on rows `0467` is respectively
`-2s d0d1` or `+2s d0d1`.  A genuine binary point makes this nonzero; the
pure transverse entry in row four and the distinguished column is `-2`.
Hence no marked-`H31` lift exists.

For weighted `H22`, the `D01` all-alpha direction is Hall-deficient, leaving
only the shared `D01`-pure/`D23`-binary case.  Exact saturated elimination on
both the finite and infinity weight charts gives the same marking ideal (13).
The combined unwanted matrix has rank seven and complete kernel `C e0`.
On the finite chart its three required diagonals are

```text
B01=2C((ell+1)lambda+1-ell),
A23=2C(lambda-1)E,
B23=-2C k(ell^2-1)(lambda+1).                     (16)
```

The `D23` mode-three determinant on rows `0467` is

```text
-8 C^3 k(ell^2-1)(lambda+1)^3 E.                 (17)
```

At weight infinity the diagonals become

```text
2C(ell+1), 2CE, -2Ck(ell^2-1),                   (18)
```

and the same determinant becomes

```text
-8 C^3 k(ell^2-1)E.                              (19)
```

Every genuine shared binary point on the divisor-generic open makes the
appropriate determinant nonzero, so the ternary rank is four and the `H22`
lift is impossible.

## Replay

```text
uv run --with sympy python claims/p5/boundaries/verify_p5_component21_divisor_generic_fibre_obstructions.py
uv run --with sympy python claims/p5/boundaries/audit_p5_component21_divisor_generic_fibre_obstructions.py
```

The primary replay uses exact row modules and saturated elimination over the
displayed characteristic-zero function fields.  The audit independently
reconstructs the pure tensors, Hall supports, branches, kernels, diagonals,
and fixed minors at rational parameter points.  No finite-field computation
is used as proof.  A broader uniform polynomial attempt timed out and is not
evidence for any exceptional sublocus.
