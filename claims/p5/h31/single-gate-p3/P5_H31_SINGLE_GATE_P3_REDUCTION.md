# The single-gate `H31` branch is a seven-hyperplane problem

## Status

This is an exact characteristic-zero reduction of the `H31` frontier.
It is not by itself an exclusion theorem.  Its ternary continuation now
excludes the entire rank-two-`M` branch:

- [`P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md`](P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md)

Suppose two source hyperplanes

```text
H_s=span(e_0,e_1,e_2,e_s),
H_p=span(e_0,e_1,e_2,e_p)
```

share the three-space `M=span(e_0,e_1,e_2)`.  Assume that the binary
rows `alpha_r,beta_r` of four local maps send the `P_4` restriction on
`H_s` to a nonzero pure tensor and the restriction on `H_p` to
`Delta_2`.

If one local row pair has rank one on `H_s` and the other three row
pairs have rank two on `M`, then:

1. that rank-one pair is the unique such pair;
2. the other three pairs form a marked decomposable-`P_3` sign chart
   on `M`; and
3. extension across either exceptional source coordinate is governed
   by a `7 x 7` linear system whose determinant is the product of seven
   projective lines; and
4. the exact viable locus is the union of four explicitly punctured
   components of that arrangement.

Thus this binary branch is reduced from arbitrary local maps to four
one-dimensional projective strata.  The cited follow-up excludes their
ternary lifts.  A separate pair-image polarity theorem excludes the
case where one of the three remaining pairs drops rank on `M`:

- [`P5_H31_SECONDARY_GATE_EXCLUSION.md`](P5_H31_SECONDARY_GATE_EXCLUSION.md)

The all-rank-two pure-`P_4` locus, the full `H31` branch,
`P_5 -> Delta_3`, and the global conjecture remain unresolved.

## There is at most one rank-one gate

Normalize the pure image on `H_s` so that only the `beta^4` coefficient
is nonzero.  If the pair at mode `r` has rank one on `H_s`, then

```text
alpha_r|H_s = k beta_r|H_s.
```

Replacing `beta_r` by `alpha_r` in the nonzero `beta^4` coefficient
multiplies that coefficient by `k`.  Purity forces the resulting mixed
coefficient to vanish, so `k=0`:

```text
alpha_r|H_s=0.                                      (1)
```

On `H_p`, a nonzero `alpha^4` coefficient is required.  Equation (1)
therefore makes `alpha_r|H_p` a nonzero multiple of `e_p^*`.  If two
modes were rank-one gates, two rows in the `alpha^4` permanent would be
supported on the same source coordinate `p`, and that permanent would
vanish.  Hence there is at most one gate.

Put the unique gate at mode zero and normalize

```text
alpha_0|H_p=e_p^*.                                  (2)
```

The coefficients containing `alpha_0` show that the three remaining
pairs on `M` send `P_3` to a nonzero pure tensor.

## The marked `P_3` chart

Assume those three pairs have rank two on `M`.  The exact classification
in
[`P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md`](P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md)
puts one oriented-edge chart, after permuting and rescaling modes and
source coordinates, into the form

```text
alpha_1=(-B,0,1),   beta_1=(-A,1,0),
alpha_2=( A,1,0),   beta_2=( B,0,1),
alpha_3=( A,1,0),   beta_3=( 0,B,A),                 (3)
```

where `A!=0` and `B` is arbitrary.  Direct expansion gives

```text
per(alpha_1,alpha_2,alpha_3)=2A
```

and all other binary coefficients vanish.  The locus `B=0` is the
support-two boundary of the same sign chart; it must not be discarded.

## Extension as a linear system

Let

```text
beta_0|M=(v_0,v_1,v_2).
```

For either exceptional coordinate `q in {s,p}`, write

```text
t=beta_0[q],
x_i=alpha_i[q],
y_i=beta_i[q],              i=1,2,3.                (4)
```

Contracting through `beta_0` must leave a pure `beta_1 beta_2 beta_3`
coefficient.  Consequently the seven coefficients indexed

```text
000,001,010,011,100,101,110
```

must vanish, while `111` must be nonzero.  They are linear in

```text
z=(t,x_1,x_2,x_3,y_1,y_2,y_3).
```

Let `N(A,B,v)` be the `7 x 7` matrix of the seven vanishing
coefficients and let `d(A,B,v)` be the row of the desired `111`
coefficient.  Exact expansion of (3)-(4) gives

```text
det N =
-8 A^4 B v_1 v_2
 (-A v_1-B v_2+v_0)
 (-A v_1+B v_2+v_0)
 ( A v_1-B v_2+v_0)
 ( A v_1+B v_2+v_0).                                (5)
```

A valid extension requires

```text
N z=0,   d z!=0.                                    (6)
```

In particular, no extension exists off the seven projective lines

```text
B=0,  v_1=0,  v_2=0,
v_0 =  A v_1+B v_2,
v_0 =  A v_1-B v_2,
v_0 = -A v_1+B v_2,
v_0 = -A v_1-B v_2.                                 (7)
```

Intersections can change the rank of `N`, so the determinant alone is
not a classification.  The next calculation retains all of them.

## Exact viable locus

For nonzero `v=(v_0,v_1,v_2)` and `A!=0`, system (6) has a solution if
and only if at least one of the following four conditions holds:

```text
I.    B=0,    v_0-A v_1 != 0;

II.   v_1=0,  v_0(v_0+B v_2) != 0;

III.  B!=0,   v_2=0,  v_0(v_0-A v_1) != 0;

IV.   v_0=-A v_1+B v_2,  v_0!=0.                   (8)
```

These alternatives are not asserted to be disjoint.  Polynomial kernel
witnesses, in the variable order of (4), are respectively

```text
I.   (v_2,-1,0,0,0,1,A);

II.  (v_2(v_0-Bv_2), Bv_2-v_0,0,0,0,
       Bv_2+v_0, A(Bv_2+v_0));

III. ((Av_1+v_0)^2,0,-A(Av_1+v_0),-A(Av_1+v_0),
       A(v_0-Av_1),0,AB(v_0-Av_1));

IV.  (0,0,0,0,0,0,1).                              (9)
```

Their desired coefficients are

```text
2A(v_0-Av_1),
2A v_0(v_0+Bv_2),
2AB v_0(v_0-Av_1),
2v_0,                                                (10)
```

so (8) makes them valid.

For necessity, first split on the three coordinate factors of (5).
On `B=0`, the desired row vanishes identically when
`v_0=Av_1`.  On `v_1=0`, it lies in the row space of `N` on each
excluded subcase `v_0=0` and `v_0=-Bv_2`.  On `v_2=0` with `B!=0`,
the same holds on `v_0=0` and `v_0=Av_1`.  On component IV it lies in
the row space when `v_0=0`.

It remains to consider `Bv_1v_2!=0`.  On each of the other three signed
lines in (7), direct rational row combinations put `d` in the row space
of `N`.  Their denominators are products of `A,B,v_1,v_2`, already
nonzero in this case.  This includes intersections of those signed
lines.  The alternatives exhaust every factor of (5), proving (8)
without discarding any line intersection.

## Geometric interpretation and next step

Equations (5) and (8) replace the original compatibility question by a
projective incidence problem.  The covector `v=beta_0|M` must lie on
one of three coordinate/signed lines, unless the rectangle itself
degenerates to its support-two boundary `B=0`.

The remaining task was finite in *strata*, not finite in points:
impose the second exceptional coordinate and the third target row
separately on I-IV and their intersections.  The cited rank-two-`M`
theorem carries out that continuation using transverse one-marked
kernels and one final mixed-colour obstruction.

## Verification

Run:

```text
python verify_p5_h31_single_gate_p3_reduction.py
python audit_p5_h31_single_gate_p3_reduction.py
```

The primary verifier reconstructs the marked `P_3` tensor, all eight
extension coefficients, determinant (5), the four witnesses (9), and
row-space certificates for every excluded stratum symbolically.  The
independent audit uses a separate modular permanent and row-reduction
implementation over `F_5` and `F_7`.  It enumerates only the small
projective parameter space `(A,B,[v])`, not ambient maps, and verifies
the exact equivalence (8), including every line intersection.  The
finite-field census is a boundary audit; the reduction above is over
characteristic zero.
