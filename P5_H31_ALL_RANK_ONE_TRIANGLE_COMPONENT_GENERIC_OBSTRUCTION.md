# Generic marked `H31` obstruction on the all-rank-one triangle component

## Status

This is an exact characteristic-zero theorem on a dense open subset of
the ninth pure-`P_4` component proved in
[`P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md`](claims/p4/components/all-rank-one-triangle/P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md).

The complete marked-basis fibre over the generic point of that
component has no `H31` lift.  Thus the first nine certified
pure-component orbits all have empty generic marked `H31` fibre.
Of the newly certified orbits, the tenth is closed in the
companion coincident-support theorems; the eleventh through
thirteenth (the equal-support sixfold and the two rank-sum-19
fivefolds of the exhaustiveness sweep) are not treated here and
remain open.

This does not close special parameter or projective boundary points,
prove the component census exhaustive, or resolve the global prize
problem.  The companion generic weighted `H22` theorem for this
component is
[`P5_H22_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md).

## Component function field

The ninth component is free: its normal form has no defining
hypersurface, so the generic component field is the pure
transcendental field

```text
K=C(p,q).                                           (1)
```

Use the pure-factor bases `(alpha_i,beta_i)=(y_i,x_i)` of the
component theorem:

```text
alpha_0=(pq+1,1,p,pq+1),      beta_0=(q+1,0,1,q),
alpha_1=(p,1,0,0),            beta_1=(0,0,1,-1),
alpha_2=(1,0,-1,0),           beta_2=(-p,1,0,0),
alpha_3=(0,0,1,1),            beta_3=(1,0,1,0).    (2)
```

The restricted tensor is supported on the single word

```text
T_1111=-2,                                          (3)
```

and every marked basis on the same four planes is represented, up to
irrelevant row scalings, by

```text
beta_i(t)=beta_i+t_i alpha_i.                       (4)
```

## The ubiquitous single-word reconstruction kernel

Because the permanent is multilinear in the rows, replacing `beta` by
`beta(t)` changes each word coefficient only by lower-word
contributions.  Since (3) is the **only** nonzero word, the complete
marked tensor is identically the single word `-2` for every marking
`t`.  This is the extreme single-word case among the certified
components.

Consequently, for **every** distinguished source coordinate
`q in {0,1,2,3}` and every marking, restoring the deleted coordinate,

```text
z_rec=(alpha_i[q], beta_i(t)[q])_{i=0}^3,           (5)
```

lies in the kernel of the `14 x 8` mixed binary matrix `M_q(t)`, with
diagonal values

```text
A_q(z_rec)=0,           B_q(z_rec)=-2.              (6)
```

On the six-dimensional component this reconstruction line exists in
one frame only (`q=1` there); here it is ubiquitous in all four
frames.  Every mixed matrix has rank at most seven, and a genuine
neighbouring `Delta_2` direction — `M_q(t)z=0` with
`A_q(z)B_q(z)!=0` — requires a second kernel direction on which `A_q`
does not vanish.

## Exact marked projection

For each frame, normalize `A_q(z)=1`, invert `B_q(z)`, and eliminate
the nine extension/inverse variables over `K`.  The verifier proves
bidirectional ideal equality of each projection with the stated
ideal.  The four marking loci are

```text
q=0:  (t_1,t_2,t_3)          - the whole t_0-line,
q=1:  (1)                    - empty,
q=2:  (t_1,t_3,t_0 t_2)      - the t_0-line union the t_2-line,
q=3:  (t_1, t_2,
       (pq+p+1)t_0+(q+1),
       (pq+1)t_3+(pq+p+1))   - one point.           (7)
```

There are no hidden marking sheets.  Unlike the disjoint mixed-star
and six-dimensional components, whose survivor markings are rational
points over the component field, the `q=0` and `q=2` survivor loci
are **entire marking lines**: one marking coordinate stays free.  All
certificates below therefore keep the line parameter polynomial, so
they close every fibre point of the line, including all special
values, over the generic component point.

## Sheet kernels

On each survivor sheet the mixed matrix has rank exactly six.  One
six-by-six pivot minor per sheet is line-parameter-free (rows and
columns are indexed from zero; `s` denotes the free line parameter):

```text
sheet             pivot rows/columns     determinant
q=0 t_0-line      (0,1,3,5,6,7)/(0-5)    2(pq+1)^2(pq+p+1)
q=2 t_0-line      (0,1,2,3,6,7)/(0-4,6)  2p(pq+1)^2
q=2 t_2-line      (0,1,2,3,6,7)/(1-6)   -2p(pq+1)^3
q=3 point         (0,1,2,3,4,7)/(0-4,6)  2p^2(pq+p+1)/(pq+1)  (8)
```

Hence, away from `p(pq+1)(pq+p+1)=0`, the kernel is two-dimensional
at every point of every sheet: `span(z_rec, z_gen)`, with

```text
q=0 t_0-line:
 z_gen=(-1,-1,0,0,s,0,1,0),
 A=2,                B=-2s;

q=2 t_0-line:
 z_gen=(pq+1,0,0,1,-(s(pq+1)+q),1,0,0),
 A=2(pq+1),          B=2(s(pq+1)+q);

q=2 t_2-line:
 z_gen=(-p(pq+1),-s(pq+1),0,s-p,q(p-s),s-p,s(pq+1),0),
 A=-2p(pq+1),        B=-2q(p-s);

q=3 point:
 z_gen=(-p^2(pq+p+1),0,(pq+p+1)^2,-(pq+1)(pq+p+1),
        pq+1,(pq+1)(pq+p+1),0,0),
 A=2(pq+1)(pq+p+1)^2,
 B=-2(p-1)(pq+p+1).                                 (9)
```

Every kernel direction is `z=k z_gen+l z_rec`; both diagonals are
linear in `(k,l)` and `A(z)=kA(z_gen)`, so genuine directions have
`k!=0`.

## All-extension minor identities and Fitting certificates

For each sheet, a distinguished-dependent mode kills every genuine
direction: mode `1` for `q=0` and the `q=3` point, mode `3` for both
`q=2` branches.  Let `P_m(z)` be the mode-`m` one-marked map on the
neighbouring hyperplane.  On `z=k z_gen+l z_rec` the certificate
minors reduce to exact `A B`-multiples:

```text
q=0 t_0-line, mode 1:
 det P[0,2,3,7] = -2lp(pq+1) A B,
 det P[0,3,6,7] =  2s(lp-k)(pq+1) A B;

q=2 t_0-line, mode 3:
 det P[0,2,3,7] = -2l(pq+1)(pq-p+1) A B,
 det P[0,2,6,7] =  2(k(s(pq+1)+q)+lq) A B;

q=2 t_2-line, mode 3:
 det P[0,2,4,7] =  2lq(pq-p+1) A B,
 det P[0,2,6,7] = -2q(k(p-s)-l) A B;

q=3 point, mode 1:
 det P[0,1,4,7] = -(q+1) A^2 B/((pq+1)(pq+p+1)).   (10)
```

The `q=3` point thus carries a uniform one-minor identity in the
disjoint mixed-star style, with ratio

```text
R = -(q+1)/((pq+1)(pq+p+1)).                        (11)
```

On the line sheets no single minor works — each linear residual in
(10) vanishes somewhere on the kernel pencil, and the modular census
already showed no common minor along the lines — but each displayed
pair does: the two residuals meet only at `l=0` intersected with
`k=0`, `s=0`, or `s=p`, where either no direction remains or the
`B`-diagonal vanishes.

The formal certificates do not rely on the pencil parametrization.
For each sheet, adjoin to the fourteen mixed equations the displayed
minors and `w A_q(z) B_q(z)-1`, keeping the line parameter `s` a
polynomial ring variable.  Over `K` each of the four ideals is

```text
(1).                                                (12)
```

Consequently every genuine binary extension over every marking of
every survivor sheet has a one-marked map of rank four.  An `H31`
lift would factor this map through a three-dimensional target local
space, so its rank would be at most three.  This is impossible, and
with the unit projection for `q=1` it proves:

```text
the generic marked H31 fibre of the all-rank-one
triangle component is empty.                        (13)
```

## Geometric interpretation

The single-word support makes the marked extension problem almost
rigid: the reconstruction line forces `rank M_q(t)<=7` everywhere,
and the survivor loci are the coordinate lines in marking space where
the rank drops once more.  The `q=0` line marks the mode-`0` kernel
row (the only row pair whose relation triangle misses it), the `q=2`
locus splits along the two triangle edges through mode `2`, and the
`q=3` frame pins both free marking coordinates.  Each sheet is then
disjoint from the rank-at-most-three Fitting locus of one marked
mode, uniformly in the line parameter.

## Honest frontier

The theorem is generic in `(p,q)`.  Divisors explicitly visible in
(8)--(11) and excluded from the statement:

```text
p=0,  q=0,  q+1=0,  p-1=0,
pq+1=0,  pq-p+1=0,  pq+p+1=0,                       (14)
```

together with the implicit Groebner denominators of the projections
and unit-ideal certificates, the component's parameter and projective
boundaries, and component exhaustiveness (thirteen orbits are the
current certified lower bound, not a census; the eleventh through
thirteenth still lack any `H31`/`H22` theorem).  The `q=3` marking
sheet itself only exists where `(pq+1)(pq+p+1)!=0`, and its genuine
direction degenerates on `p=1` (`B(z_gen)=0` there).  The global
conjecture remains unresolved.

## Verification

Run:

```text
python verify_p5_h31_all_rank_one_triangle_component_generic_obstruction.py

python audit_p5_h31_all_rank_one_triangle_component_generic_obstruction.py
```

The primary verifier reconstructs (2)--(4) against the component
verifier, proves the single-word marked invariance and the
reconstruction kernel (5)--(6) symbolically in all four frames,
performs the four exact function-field projections with bidirectional
ideal equality (7), replays the pivot minors (8), kernels (9), and
minor identities (10)--(11), and proves the four characteristic-zero
unit ideals (12).  All Singular steps are fail-closed: a timed-out or
failed run is recorded as null and the verifier raises instead of
claiming it.

The independent audit imports nothing from the primary verifier.  At
two generic finite-field component points it exhausts all `p^4`
marked bases in every frame, recovers exactly the loci (7), and
checks that the certificate minors of (10) jointly cover every
genuine projective extension direction.  The finite-field census is
corroboration only; the function-field eliminations and unit ideals
prove the theorem over `C`.
