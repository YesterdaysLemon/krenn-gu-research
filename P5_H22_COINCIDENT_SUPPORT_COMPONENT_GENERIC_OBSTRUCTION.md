# Generic weighted `H22` obstruction on the tenth (coincident-support) component

## Status

This is an exact characteristic-zero obstruction on the generic
diagonal-source orbit of the six-dimensional coincident-support
component proved in
[`P4_INOUT_PATH_STRATUM_WORKING_NOTE.md`](P4_INOUT_PATH_STRATUM_WORKING_NOTE.md)
("A tenth component through the singular walls") and certified by
`branch_ambient_certificates.py`.

For the two weighted diagonal-hyperplane pencils required by `H22`:

1. the `01` pencil admits **no** sharp binary `Delta_2` extension for
   any slope, any marking, and any chart point: its `0000` diagonal
   coefficient vanishes *identically* as a polynomial in all data; and
2. the `23` pencil has a universal extension kernel that only
   reconstructs the pure tensor, and its exact binary marking
   projection over the slope-extended function field is the **unit
   ideal**; the same elimination is unit at the three special slopes
   `r=1`, `r=-1`, `r=0`, and the `r=infinity` endpoint is the `H31`
   `q=3` frame, closed by the companion theorem.

Thus both pencils are empty at binary level and a relevant pure
binary plane cannot be generic on this component in a hypothetical
`H22` restriction — in every `(a,b)` support subfamily.  No ternary
Fitting stage is needed, in contrast to all previously closed
components.

Beyond the generic point, the two interior codimension-one survivor
divisors `c=0` and `b+e=0` are closed at ternary level as well.
This does **not** close the deeper survivor strata, the divisors
`k=0` and `P=0`, parameter-coupled slope divisors, the projective
boundary, other components, component exhaustiveness, all of `H22`,
or the global prize problem.

## Component data and pencils

Use the concentrated pure-factor bases of the `H31` companion
theorem
[`P5_H31_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md),
with the working note's parameter `r` renamed `c` and

```text
P=bec+b+e,   Q=be(m+1),   A*=2bce-(b+e)(m-1):

alpha_0=(1,-1,0,0),        beta_0=(0,1,b,-bk),
alpha_1=(1,-1,0,0),        beta_1=(0,1,e,-ek),
alpha_2=(0,0,1,k),         beta_2=(1,1,0,0),
alpha_3=(P,Pm-Qc,-Q,Qk),   beta_3=(0,c,1,-k),

T_1111=-2kP,     markings beta_i(t)=beta_i+t_i alpha_i.   (1)
```

As in the earlier weighted `H22` theorems, the two diagonal-hyperplane
pencils act on every local row `u` by

```text
D_01^r(u)=(r u_0+u_1,u_2,u_3,ext),
D_23^r(u)=(u_0,u_1,r u_2+u_3,ext),                        (2)
```

with the slope `r` transcendental over the component field; the
fifth-coordinate extensions are `z=(x_0..x_3,y_0..y_3)`.  A genuine
binary survivor needs the fourteen mixed words to vanish and both
diagonals `A(z)` (word `0000`) and `B(z)` (word `1111`) nonzero.
The torus gauge `k=1` of the companion theorem applies verbatim: the
pencils absorb the residual torus into the transcendental slope, and
`diag(1,1,1,1/k)` normalizes `k`.  All identities below are
nevertheless verified with `k` symbolic.

## The `01` pencil dies identically

The `0000` word of the `D_01^r` frame satisfies

```text
A_01(z) = 0    identically in Z[b,e,k,m,c,r,t,z].         (3)
```

The two mechanisms of the companion theorem persist for every slope:
the coincident kernel rows `alpha_0=alpha_1=ybar` become
`(r-1,0,0,ext)`, supported in one common column, and the mode-2/3
tails on the surviving columns `{2,3}` are apolar,

```text
perm((1,k),(-Q,Qk))=0.                                    (4)
```

Hence the `01` pencil never produces a sharp `Delta_2` neighbour —
at any slope, marking, or chart point.  In particular the `H22`
support case `a != 0`, which requires a sharp `D_01` extension, is
impossible with **no divisor exclusions at all**.

## The `23` pencil: universal reconstruction kernel

The `0000` row is `t`-free and supported on the `x`-slots:

```text
A_23 = (-(k+r)A*, -(k+r)A*, 2Q(r-k), -2(k+r)).            (5)
```

The doubled-column permanents of the concentrated basis satisfy the
exact identity

```text
D3_w + k^2 D2_w = 0   (w != 1111),      = 4k^2 P   (w=1111),  (6)
```

where `D2` (resp. `D3`) doubles column 2 (resp. 3).  Consequently the
extension

```text
z* :  ext_i = r*row_i[3] + k^2*row_i[2]                   (7)
```

satisfies, identically in `(t,b,e,k,m,c,r)`,

```text
M(t)z*=0,      A z*=0,      B z* = -2kP(r-k)^2.           (8)
```

This is the pencil analogue of the coordinate-restoration kernels: it
degenerates to `k^2` times the `q=2` reconstruction at `r=0` and
carries both diagonals to zero exactly on the equal-weight slope
`r=k`.  The mixed rank is generically exactly seven — the witness
minor on the mixed words `0001,0010,0100,0101,0110,1000,1001` and
columns `x_0..x_3,y_0..y_2` at `t=0`, `k=1` is

```text
-4bc^2e^3(m+1)^2(r-1)^3(r+1)^4 P                          (9)
```

— so on a dense open set every extension in the kernel is a multiple
of `z*` and has `A z=0`: never genuine.

## Exact unit projections

Normalize `A z=1`, invert `B z` by `w`, and eliminate `(z,w)` with
the block ordering `(dp(9),dp(4))`:

```text
over C(b,e,m,c,r):        projected marking ideal = (1);
at r=1  over C(b,e,m,c):  (1);
at r=-1 over C(b,e,m,c):  (1);
at r=0  over C(b,e,m,c):  (1).                            (10)
```

The `r=0` case is literally the `H31` `q=2` frame, and the
`r=infinity` endpoint normalizes to the `H31` `q=3` frame; both are
also closed by the companion theorem's unit projections.  Hence the
`23` pencil has no genuine binary survivor for any marking over the
generic component point, and none on any of the four special slopes
`r in {0,1,-1,infinity}` either.  Unlike components 7 and 8, there is
no surviving marking sheet to exclude ternarily, and no analogue of
the equal-weight exception: the slope-divisor scoreboard of the
boundary atlas is uniform here.

## Why this closes generic weighted `H22`

By the frontier reduction
([`P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`](P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md),
[`P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md`](P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md)
(13)-(14)), an `H22` local family has `(a,b) != (0,0)`; `a != 0`
forces a sharp weighted `D_01` extension of the pure binary plane and
`b != 0` a sharp weighted `D_23` extension.  The first is impossible
identically by (3); the second is impossible over the generic
diagonal-source orbit point by (8)-(10).  Hence the generic weighted
`H22` incidence of the coincident-support component is empty, at
binary level.

## Interior parameter divisors and their closures

The `H31` companion theorem locates exactly two codimension-one
parameter divisors carrying genuine binary survivors, `c=0` and
`b+e=0` (plus codimension-two strata).  The same loci are the `D_23`
pencil's survivor divisors, and their binary marking sheets are
**slope-free** and identical to the `H31` sheets: over `C(b,e,m,r)`
on `c=0`,

```text
t_3=t_2=0,
e^2(m+1)t_0+b^2(m+1)t_1 = b^2-be(m-1)+e^2,
plus one quadratic in t_1  (a conjugate marking pair),
```

and over `C(b,m,c,r)` on `e=-b`,

```text
t_2=0,  t_0+t_1=1,  t_1(t_1-1)=0,  2b^2t_3+1=0
(two rational markings).                                  (11)
```

On every sheet, adjoining the two mode-2 one-marked minors in rows
`(0,1,2,7)` and `(0,1,3,7)`, normalizing the `0000` diagonal to one
and inverting the `1111` diagonal gives the unit ideal.  Hence every
genuine `D_23` survivor over the generic point of either divisor has
a rank-four mode-2 one-marked contraction and cannot lift ternarily,
for any slope; and the `D_01` pencil is identically non-sharp there
by (3).  Both interior divisors are closed for weighted `H22`.

## Excluded divisors (atlas record)

* identities (3)-(8): **no divisors** (statements over
  `Z[b,e,k,m,c,r,t]`);
* chart/normalization: `k=0`, `P=0` (pure coefficient `-2kP`,
  concentration validity), as in the companion theorem;
* the generic unit projection (10): implicit denominators in
  `(b,e,m,c,r)`; the explicitly closed slopes are
  `r in {0,1,-1,infinity}`, so any remaining slope divisor is
  parameter-coupled (not extracted, as for components 1-6);
* rank-seven witness (9) excludes `b,c,e,m+1,P,r-1,r+1 = 0`
  (informational);
* the survivor divisors `c=0` and `b+e=0` are **closed at ternary
  level** by (11); their intersections, the codimension-two strata
  `{ec+1=0,m=0}` and `{bc+1=0,m=0}`, the deeper census fine
  structure, and `P=0` remain open;
* the component's projective boundary is untouched, as everywhere in
  the program.

## Verification

Run

```text
python verify_p5_h22_coincident_support_component_generic_obstruction.py
python audit_p5_h22_coincident_support_component_generic_obstruction.py
```

The primary verifier replays (1), the identity (3) with `k,r,t`
symbolic, the diagonal row (5), the doubled-column identity (6), the
universal kernel (7)-(8), and the witness (9); it then performs the
four Singular projections (10), the two relative sheet projections
and the three per-sheet Fitting unit certificates of (11), all with
a 550-second fail-closed budget.

The independent audit imports nothing from the primary verifier.  It
uses a dynamic-programming permanent and finite-field linear algebra
at two primes, two parameter samples, and two generic slopes plus the
special slopes `1,-1,0`, exhausting all `p^4` markings of both
pencils: the `01` pencil's `0000` word vanishes at every marking, and
the `23` pencil has no genuine survivor.  A divisor-point census on
`b+e=0` finds the survivors exactly on the sheets (11) with
rank-four mode-2 one-marked maps.  The censuses are corroboration
only; the theorem is the characteristic-zero calculation above.

## Honest frontier

Both `H31` and weighted `H22` are now closed at the generic point of
the tenth component, each at binary level, and both interior
codimension-one survivor divisors `c=0` and `b+e=0` are closed at
ternary level in both frames.  The remaining tenth-component work is
the codimension-two survivor strata, the divisors `k=0` and `P=0`,
parameter-coupled slope divisors, and the projective boundary; the
ninth and eleventh components still lack generic `H31`/`H22`
theorems; component exhaustiveness and the global conjecture remain
open.
