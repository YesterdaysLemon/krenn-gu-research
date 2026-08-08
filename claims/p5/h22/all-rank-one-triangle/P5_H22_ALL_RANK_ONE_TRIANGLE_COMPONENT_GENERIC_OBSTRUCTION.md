# Generic weighted `H22` obstruction on the all-rank-one triangle component

## Status

This is an exact characteristic-zero obstruction on the generic
diagonal-source orbit of the ninth pure-`P_4` component proved in
[`P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md`](claims/p4/components/all-rank-one-triangle/P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md).

Restoring the source-torus slope turns the two `H22` neighbours into
weighted diagonal-hyperplane pencils.  Generically both pencils have
nonempty binary survivor sheets, and every survivor is excluded at
ternary level: a relevant pure binary plane cannot be generic on this
component in a hypothetical `H22` restriction.  Together with
[`P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md)
this closes both generic local frames of the ninth certified orbit,
so the first nine known pure-component orbits are now generically
closed for `H31` and weighted `H22`.  The newly certified tenth
through thirteenth orbits are not treated here and remain open.

This does **not** close the slope or parameter divisors listed below,
the component's projective boundary, component exhaustiveness, all of
`H22`, or the global conjecture.

## Weighted diagonal pencils

With the normalized `H22` contractions `v_0=e_0+e_1`, `v_1=e_2+e_3`,
`v_2=e_4`, the residual diagonal source torus changes the two
neighbouring source bases to

```text
D_01^r(x)=(r x_0+x_1, x_2, x_3, x_4),
D_23^r(x)=(x_0, x_1, r x_2+x_3, x_4).                (1)
```

The slope `r` lives in the component function field: the working
field is

```text
K=C(p,q,r),                                          (2)
```

with the free pure-factor bases `(alpha_i,beta_i)` of the component
theorem (single restricted word `T_1111=-2`) and marked bases

```text
beta_i(t)=beta_i+t_i alpha_i.                        (3)
```

## Exact slope-generic marked projection

Impose the fourteen mixed weighted coefficients, normalize the `0000`
diagonal `A(z)=1`, invert the `1111` diagonal `B(z)`, and eliminate
the nine extension/inverse variables over `K`.  The verifier proves
bidirectional ideal equality of each projection with

```text
D_01^r:  (t_1,t_2,t_3),

D_23^r:  (t_1,t_2,((pq+p+1)t_0+(q+1))t_3).          (4)
```

Both marking loci are **independent of the slope** `r` — the
single-word structure again.  The `D_01` survivors fill the whole
`t_0`-line.  The `D_23` locus is the union of the `t_0`-line and the
line

```text
t_0=-(q+1)/(pq+p+1),      t_1=t_2=0,      t_3 free,  (5)
```

whose fixed `t_0` value is exactly the `t_0`-coordinate of the `H31`
`q=3` point marking, and whose closure meets the `t_0`-line at
`(t_0^*,0,0,0)`.  At the projective slope endpoints the pencils
degenerate to the `H31` coordinate frames
(`D_01^0 ~ q=0`, `D_01^infinity ~ q=1`, `D_23^0 ~ q=2`,
`D_23^infinity ~ q=3`), and (4) interpolates the `H31` loci of those
frames.

## Unique genuine kernel lines

Unlike the `H31` frames, the weighted mixed matrices have **no**
reconstruction direction: on each survivor sheet the rank is exactly
seven with a one-dimensional kernel on which both diagonals are
generically nonzero — an honest binary `Delta_2` survivor family.
With `s` the free line parameter, displayed kernel representatives
satisfy

```text
D_01 t_0-line:
 z=(pr+1, pr+1, 0, 0, s(pr-1), 0, pr-1, 0),
 A=-2(pr+1),
 B=-2(r+s)(pr-1);

D_23 t_0-line:
 z=(-(r+1)(pq+1), 0, 0, -(r+1),
    (1-r)(pqs+q+s), r-1, 0, 0),
 A=-2(r+1)(pq+1),
 B=2(r-1)(pqs+q+r+s);

D_23 t_3-line:
 A=2r(r+1)(pq+1)(pq+p+1)^2,
 B=-2(r-1)(pq+p+1)G,
 G=r^2(pq(s+1)+p+s+1)-pqs-r-s.                       (6)
```

(The `t_3`-line kernel vector is displayed in the verifier; its
entries carry the auxiliary factor
`W=pqrs+pqr+pqs+pr+rs+r+s`.)  Rank-seven pivot witnesses are
line-parameter-free on both `t_0`-sheets,

```text
D_01: 4r(pq+1)^2(pr-1)^3(pr+1)^2
        (pq-p+1)(pq+p+1)(pqr+r+1),
D_23: 4pr(r-1)^3(r+1)^2(pq+p+1)(pq+pr+1),           (7)
```

while on the `t_3`-sheet every pivot carries an `(r,s)`-coupled
factor; the displayed one is

```text
4p(r-1)^3(r+1)^2(pq+pr+1)W.                          (8)
```

The certificates below therefore do not use the kernel description:
they keep `s` polynomial and cover every sheet point, including the
divisors of (7)--(8).

## Ternary Fitting certificates

For a ternary `H22` lift, the mode-`m` one-marked contraction through
the other three binary planes must have rank at most three.  On the
displayed kernel representatives, single mode-`1` minors already
factor through the required diagonal `B`:

```text
D_01 t_0-line:
 det P_1[0,2,3,7] = -4pr(pq+1)(pr-1)^2 B,

D_23 t_0-line:
 (r-1) det P_1[0,2,3,7]
   = 4(r+1)^3(pq+1)^2(pq+pr+1) B.                    (9)
```

The formal certificates adjoin to the fourteen mixed equations the
minors

```text
D_01 t_0-line:  mode 1, rows (0,2,3,7);
D_23 t_0-line:  mode 1, rows (0,2,3,7);
D_23 t_3-line:  mode 3, rows (0,2,3,7),(0,2,6,7),   (10)
```

together with `w A(z)B(z)-1`, keeping `s` a polynomial ring variable.
Over `K` all three ideals are

```text
(1).                                                 (11)
```

On the `t_3`-sheet the full mode-`1` and mode-`3` four-by-four
Fitting ideals are unit as well, while modes `0` and `2` are not: the
killing mode is genuinely sheet-dependent.  Consequently every
genuine weighted binary extension over every survivor marking has a
one-marked map of rank four, whereas a local map to three target
coordinates has rank at most three.  No generic survivor lifts to
`H22`, in either pencil:

```text
the generic weighted H22 incidence of the all-rank-one
triangle component is empty.                         (12)
```

## Honest frontier

The theorem is generic in `(p,q,r)`.  Divisors explicitly visible in
(4)--(9) and excluded from the statement:

```text
slope divisors      r=0,  r=1,  r=-1;
coupled divisors    pr+1=0,  pr-1=0,  pq+pr+1=0,  pqr+r+1=0;
parameter divisors  p=0,  q=0,  q+1=0,  pq+1=0,
                    pq-p+1=0,  pq+p+1=0;
marking-coupled     r+s=0,  pqs+q+r+s=0,  G=0,  W=0, (13)
```

together with the implicit Groebner denominators of the projections
and unit-ideal certificates.  These implicit denominators are not
vacuous: the modular audit found a genuine specialization jump of the
`D_01` census at the single sample `F_11, (p,q,r)=(2,3,4)` — an
extra survivor line `t_0=-2, t_3` free — absent at `F_13` with the
same `(p,q,r)` and at every other tested `F_11` slope, so an
elimination denominator has content divisible by `11` there.  Every
direction on that jump line still has a rank-four mode-`1` marked
map, so the artifact is obstruction-consistent.  At `r=1` the `D_23`
kernel diagonal `B` vanishes identically on both sheets — the
equal-weight binary collapse seen on other components — and at
`r=-1` the `D_23` `A` diagonal vanishes; these slope boundaries are
left to the divisor atlas programme.  The `H31` theorems are the
`r in {0,infinity}` endpoints.  Component boundaries and
exhaustiveness remain open (thirteen orbits are the current
certified lower bound, and the tenth through thirteenth still lack
any `H31`/`H22` theorem), and the global conjecture remains
unresolved.

## Verification

Run:

```text
python verify_p5_h22_all_rank_one_triangle_component_generic_obstruction.py

python audit_p5_h22_all_rank_one_triangle_component_generic_obstruction.py
```

The primary verifier reconstructs the family against the component
verifier, performs both exact slope-generic projections with
bidirectional ideal equality (4), replays the displayed kernels,
diagonals (6), pivots (7)--(8), and identities (9), and proves the
three characteristic-zero unit ideals (11).  All Singular steps are
fail-closed: a timed-out or failed run is recorded as null and the
verifier raises instead of claiming it.

The independent audit imports nothing from the primary verifier.  At
two generic finite-field component points with generic slopes it
exhausts all marked bases in both pencils, verifies that every
genuine survivor lies on the loci (4) — the only locus points without
genuine directions being the displayed `B`-degeneration values
`r+s=0`, `s(pq+1)+q+r=0`, `G=0` — and replays the certificate minors
of (10) on every genuine kernel direction.  The finite-field census
is corroboration only; the function-field eliminations and unit
ideals prove the theorem over `C`.
