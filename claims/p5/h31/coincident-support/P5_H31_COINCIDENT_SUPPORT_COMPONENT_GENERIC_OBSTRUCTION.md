# Generic marked `H31` obstruction on the tenth (coincident-support) component

## Status

This is an exact characteristic-zero theorem on a dense open subset of
the six-dimensional coincident-support component proved in
[`P4_INOUT_PATH_STRATUM_WORKING_NOTE.md`](P4_INOUT_PATH_STRATUM_WORKING_NOTE.md)
("A tenth component through the singular walls") and certified by
`branch_ambient_certificates.py`.

The complete marked-basis fibre over the generic point of that
component has no `H31` lift.  The obstruction is already **binary**:
no distinguished source coordinate admits even a genuine neighbouring
`Delta_2` direction, for any marking.  Two of the four frames die by a
polynomial identity valid at *every* chart point, and the other two
have exact unit marking projections.  No ternary Fitting stage is
needed, in contrast to all previously closed components.

Beyond the generic point, the two interior codimension-one survivor
divisors `c=0` and `b+e=0` are closed at ternary level as well.  The
theorem does not close the deeper survivor strata, the divisors
`k=0` and `P=0`, or the projective boundary, does not prove
component exhaustiveness, does not settle `H22` (see the companion
weighted theorem), and does not resolve the global prize problem.

## Concentrated pure-factor bases

The working note's family parameter `r` is renamed `c` throughout,
keeping `r` free for the weighted `H22` slope.  The raw family is

```text
U_0=span(ybar,(0,1,b,-bk)),   U_1=span(ybar,(0,1,e,-ek)),
U_2=span(u3,(0,0,1,k)),       U_3=span((1,m,0,0),(0,c,1,-k)),

ybar=(1,-1,0,0),      u3=(1,1,0,0),
```

with restricted support on the two adjacent words

```text
T_1100=-2kQ,          T_1101=-2kP,

P=bec+b+e,            Q=be(m+1).                     (1)
```

The two words differ only in mode 3, so the restriction is the pure
tensor `e_1 e_1 e_0 (Q e_0 + P e_1)` scaled by `-2k`.  Swapping the
mode-2 rows and replacing the first `U_3` row by the combination
`P(1,m,0,0)-Q(0,c,1,-k)` concentrates the support on a single word.
The pure-factor bases are

```text
alpha_0=(1,-1,0,0),        beta_0=(0,1,b,-bk),

alpha_1=(1,-1,0,0),        beta_1=(0,1,e,-ek),

alpha_2=(0,0,1,k),         beta_2=(1,1,0,0),

alpha_3=(P,Pm-Qc,-Q,Qk),   beta_3=(0,c,1,-k),        (2)
```

valid bases exactly on `P!=0`, and

```text
T_1111=-2kP,     all other fifteen words vanish.     (3)
```

For a general marked basis `(K_i,B_i)=(sigma_i alpha_i+kappa_i beta_i,
tau_i alpha_i+nu_i beta_i)`, the near-diagonal words are

```text
T'_(1..0_i..1) = -2kP kappa_i prod_{j!=i} nu_j,
T'_1111        = -2kP prod_j nu_j,                   (4)
```

so a nonzero pure marking forces `kappa_i=0` and `nu_i!=0`: every
marked basis is represented, up to irrelevant row scalings, by

```text
beta_i(t)=beta_i+t_i alpha_i.                        (5)
```

## Torus gauge `k=1`

The permanent tensors are diagonal-source eigenvectors,

```text
perm(rows*diag(lam)) = (prod_j lam_j) perm(rows),
```

so every `H31` frame datum is covariant under the residual diagonal
source torus: common-column rescaling multiplies all sixteen word
coefficients by one unit and rescales one-marked-map columns by
units.  The torus element `diag(1,1,1,1/k)` carries the plane tuple
`Z(b,e,k,m,c)` to `Z(b,e,1,m,c)` exactly.  Hence, on the chart
`k!=0` (where the restriction is nonzero at all), the marked `H31`
incidence is independent of `k`, and we work over

```text
K=C(b,e,m,c),        k=1.                            (6)
```

## Exact marked frames

For distinguished source coordinate `q`, delete column `q` of all
eight marked rows and append extension entries
`z=(x_0..x_3,y_0..y_3)`.  The sixteen neighbouring binary words are
linear in `z`; the fourteen mixed words give `M_q(t)z=0`, and a
genuine neighbouring `Delta_2` direction additionally needs both
diagonals nonzero:

```text
M_q(t)z=0,       (A_q z)(B_q(t) z)!=0.               (7)
```

The `0000` row `A_q` is `t`-free in every frame because word `0000`
selects no marked row.

## The two identity-dead frames `q=0,1`

For `q in {0,1}`,

```text
A_q = 0   identically over Z[b,e,k,m,c].             (8)
```

Two elementary mechanisms cover all four entries.  The coefficient of
`x_i` in the `0000` word is the `3 x 3` permanent of the other three
`alpha` rows on the common columns.  If both coincident kernel rows
`alpha_0=alpha_1=ybar` appear, they survive only in the single common
column left from `{0,1}`, and every permanent term dies.  If one
`ybar` appears with `alpha_2,alpha_3`, expanding along the `ybar` row
leaves the `2 x 2` tail permanent

```text
perm((1,k),(-Q,Qk)) = Qk - Qk = 0,                   (9)
```

the apolarity of the mode-2/3 tails that is equivalent to the
concentration `T_1110=0` in (3).  By (8), no marking of the generic
— indeed of *any* — chart member admits a genuine binary `Delta_2`
neighbour in the frames `q=0,1`: the required `0000` diagonal
vanishes identically in the extension.

## The frames `q=2,3`: reconstruction kernels and unit projections

For `q in {2,3}` the `t`-free diagonal rows are supported on the
`x`-slots:

```text
A_2 = -k(A*, A*, 2Q, 2),
A_3 = -(A*, A*, -2Q, 2),
A*  = 2bce-(b+e)(m-1).                              (10)
```

Restoring the deleted coordinate,

```text
z_rec=(alpha_i[q], beta_i(t)[q])_i,
```

reconstructs the original pure restriction:

```text
M_q(t)z_rec=0,   A_q z_rec=0,   B_q(t) z_rec=-2kP,  (11)
```

identically in the marking.  The mixed rank is generically exactly
seven: the `7 x 7` minor on the mixed words
`0001,0010,0100,0101,0110,1000,1001` and columns
`x_0,x_1,x_2,x_3,y_0,y_1,y_2` equals, at `t=0`,

```text
+-4bc^2e^3(m+1)^2 P,                                (12)
```

so on a dense open set the extension kernel is exactly the
reconstruction line, which never carries a genuine direction by (11).

The complete function-field statement is the exact projection.
Normalize `A_q z=1`, invert `B_q(t)z` by `w`, and eliminate `(z,w)`
over `K` with the block ordering `(dp(9),dp(4))`.  For both `q=2` and
`q=3`,

```text
projected marking ideal = (1).                      (13)
```

There are no surviving marking sheets at all — no analogue of the
three rational markings of the six-dimensional seventh component.

## Conclusion

Combining (8) for `q=0,1` with (13) for `q=2,3`: over the generic
point of the tenth component no distinguished coordinate, no marked
basis, and no extension direction produces a genuine neighbouring
binary `Delta_2` slice.  A marked `H31` local family requires one.
Hence

```text
the generic marked H31 fibre of the coincident-support
component is empty,                                 (14)
```

and the exclusion happens at binary level, before any third target
row is considered.

## Interior parameter divisors and their closures

The unit eliminations (13) are function-field statements, so genuine
binary survivors can exist over proper parameter divisors.  An exact
per-point census (an instantaneous Groebner point check over `Q`)
across a `10x10x8x8` integer box locates exactly two
codimension-one survivor divisors,

```text
c=0        and        b+e=0,                        (15)
```

together with strata of codimension at least two (among them
`{ec+1=0, m=0}` and its mirror `{bc+1=0, m=0}`; the complete deeper
fine structure is left open).  The lone modular survivor previously
observed at `p=11`, `(b,e,m,c)=(2,3,7,5)`, `t=(1,0,0,2)` is a
verified characteristic-11 artifact: the same rational point has unit
marking ideal over `Q`.

Both divisors (15) close at ternary level.  Over `C(b,e,m)` on `c=0`
and over `C(b,m,c)` on `e=-b`, the exact relative projections leave
the sheets

```text
c=0:    t_3=t_2=0,
        e^2(m+1)t_0+b^2(m+1)t_1 = b^2-be(m-1)+e^2,
        b^2(m^2-1)t_1^2+(2b^2+be(m^2-2m+1)-2e^2m)t_1
          = b^2-be(m-1)-e^2m
        (one conjugate pair of markings);

b+e=0:  t_2=0,   t_0+t_1=1,   t_1(t_1-1)=0,
        2b^2t_3+1=0
        (two rational markings),                    (16)
```

for `q=2` and `q=3` alike.  On every sheet, adjoin to the mixed
equations the two mode-2 one-marked minors in rows

```text
(0,1,2,7),        (0,1,3,7),
```

normalize the `0000` diagonal to one and invert the `1111` diagonal.
All six resulting ideals are the unit ideal.  Hence every genuine
binary survivor over the generic point of either divisor has a
rank-four mode-2 one-marked contraction, and a ternary `H31` lift
would force rank at most three: both interior divisors carry no
marked `H31` incidence.  (On `b+e=0` the mode-3 one-marked map drops
to rank three on the genuine direction — the certificate must avoid
mode 3; modes 0, 1, 2 all stay rank four.)

## Excluded divisors (atlas record)

Following the conventions of
[`P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md`](P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md):

* chart/normalization divisors: `k=0` (pure coefficient `-2kP`; also
  the `k`-gauge) and `P=bec+b+e=0` (pure coefficient and validity of
  the concentrated basis (2));
* frames `q=0,1` and the marked-basis normalization (5): **no
  divisors** — (4), (8), (9) and (11) are identities over
  `Z[b,e,k,m,c,t]`;
* frames `q=2,3`: the implicit denominators of the unit eliminations
  (13).  The rank-seven witness (12) excludes `b=0, c=0, e=0, m+1=0,
  P=0`; the drop locus of the same minor at symbolic `t` factors as
  `4ecP(Qt_3-1)G` with `G` irreducible of degree three in `t`, and
  every survivor marking lies inside its zero locus.  The `t`-free
  `y`-elimination pattern of the disjoint mixed-star theorem applies
  verbatim — the single-`1` word `e_i` carries `y_i` with the
  `t`-free coefficient equal to the `A_q` entry of `x_i` in (10), so
  the reduced-system denominators are exactly `A*` and `Q`;
* the survivor divisors themselves: the codimension-one loci `c=0`
  and `b+e=0` are **closed at ternary level** by (15)-(16) and the
  six unit Fitting certificates; their mutual intersections, the
  codimension-two strata `{ec+1=0,m=0}`, `{bc+1=0,m=0}`, the deeper
  census fine structure, and the divisor `P=0` (where the raw
  support is already the single word `1100` and a different
  concentration applies) remain open.  The full survivor-locus
  eliminations with parameters as ring variables exceeded the
  550-second budget (timeout-nulls recorded in `findings.md`);
  the per-point census that replaced them is exact;
* the certified chart itself: the working note's family covers the
  component only up to the stated closure operations; projective
  boundary strata are untouched, as everywhere in the program.

## Verification

Run

```text
python verify_p5_h31_coincident_support_component_generic_obstruction.py
python audit_p5_h31_coincident_support_component_generic_obstruction.py
```

The primary verifier replays, over exact rationals with `k` symbolic:
the raw two-word support (1), the concentrated basis (2)-(3), the
marked-basis forcing (4)-(5), the torus gauge and eigenvector
identities, the dead-frame identity (8) with both mechanisms, the
`t`-free diagonal rows (10), the reconstruction identities (11), and
the rank-seven witness (12).  It then performs the two Singular
function-field projections (13), the four relative sheet projections
(16), and the six per-sheet Fitting unit certificates, all with a
550-second fail-closed budget.

The independent audit imports nothing from the primary verifier.  It
uses a dynamic-programming permanent and finite-field linear algebra
to exhaust all `p^4` markings of all four frames at two primes and
two generic parameter samples (zero genuine binary survivors; the
dead-frame identity replayed modularly), and at one sample on each
divisor (15) (survivors exactly on the sheets (16), every genuine
direction with a rank-four mode-2 one-marked map).  The censuses are
corroboration only; the theorem is the characteristic-zero
calculation above.

## Honest frontier

Of the eleven certified pure-component orbits, the first eight carry
generic `H31` obstructions by the earlier theorems and the tenth by
this one; the ninth (all-rank-one triangle) and eleventh
(equal-support sixfold) remain open.  For the tenth component, the
frames `q=0,1` are closed at every chart point, the frames `q=2,3`
are closed generically and over the generic points of both interior
codimension-one survivor divisors; the remaining `H31` work is the
codimension-two survivor strata, the divisors `k=0` and `P=0`, the
chart closure, and the projective boundary.  Component
exhaustiveness and the global conjecture remain open.  The weighted
`H22` companion statement is proved in
[`P5_H22_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md).
