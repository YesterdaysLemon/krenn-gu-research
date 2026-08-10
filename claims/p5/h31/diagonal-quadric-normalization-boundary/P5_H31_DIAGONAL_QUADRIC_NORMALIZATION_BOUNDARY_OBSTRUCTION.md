# Complete obstruction on the elliptic-normalization boundary

## Status

This is an exact characteristic-zero marked-fibre obstruction on the
complete birational boundary of the normalized affine slice

```text
A=B=F=1
```

of the diagonal-quadric pure-compression component.

The regular elliptic chart is already closed.  The inverse-map boundary
reduces to the previously closed `H=+/-1` and `U=S=0` loci, together
with the singular fibre `r=0`.  That fibre is a pair of rational curves.
Exact relative binary projection finds one survivor marking on each
curve; an all-extension marked minor excludes it.  Both projective
endpoints are included.

Thus the complete nonzero-pure marked fibre on the affine normalized
slice is empty.  This does not yet classify the outer projective/gauge
boundary where `A B F=0`, prove that there are no further
pure-compression components, settle `H22`, or solve the prize problem.

## Boundary of the conic normalization

On `A=B=F=1`, put

```text
U=C+H,       S=1+CH,       T=H+CE^2,
Psi=S^2-UT.                                             (1)
```

Where `U!=0`, the elliptic coordinates satisfy

```text
r=S/U,
x=1-rH=C(1-H^2)/U,
D=x+r^2-1=S(1-H^2)/U^2.                               (2)
```

Consequently the boundary `rxD=0` has only the following finite
images:

- `H=+/-1`, the already closed factorized fibres;
- `S=0`, where `Psi=0` and `U!=0` force `T=0`.

If `U=0`, equation `Psi=0` also forces `S=0`, hence

```text
(C,H)=(-1,1) or (1,-1),
```

the already closed pure-direction base-locus curves.

On `S=T=0,U!=0`, one has

```text
C=-1/h,       H=h,       E=delta h,
delta=+1 or -1.                                        (3)
```

The excluded values `h=+/-1` have `U=0`; the projective parameter
`h` otherwise gives the complete residual boundary.

## Two projective charts on the residual curves

Let

```text
y1=(1,0,0,-1),       y2=(0,1,-1,0),
k0=(1,0,0,1),        k1=(0,1,1,0),
u1=(1,-1,1,1).                                         (4)
```

On the finite `h` chart use

```text
alpha0=(delta h,-1,-1,-delta h),
alpha1=y1, alpha2=y2, alpha3=k1,

beta0=u1,
beta1=(h,h-1,-h-1,h),
beta2=((1+delta)h,1,1,(1-delta)h),
beta3=k0.                                               (5)
```

The only nonzero restricted coefficient is

```text
Perm(beta0,beta1,beta2,beta3)=4(h^2-1).                (6)
```

The scaling in (5) extends regularly across `h=0`.

At infinity put `z=1/h` and use

```text
alpha0=(delta,-z,-z,-delta),
alpha1=y1, alpha2=y2, alpha3=k1,

beta0=u1,
beta1=(1,1-z,-1-z,1),
beta2=(1+delta,z,z,1-delta),
beta3=k0.                                               (7)
```

Now the pure coefficient is `4(1-z^2)`.  On the overlap, (5) and (7)
differ only by nonzero row rescalings, so the two charts cover the
complete projective curves.

Every marking is `beta_i(t)=beta_i+t_i alpha_i`.

## Complete relative binary projections

Saturate the finite chart by `h^2-1`.  For `delta=-1`, the projected
marking ideal is the unit ideal for `q=0,1,2`; for `q=3` it is

```text
< t3,
  t1+h,
  t0+2t2-h,
  2h t2-h^2-1 >.                                      (8)
```

For `delta=+1`, the unit-ideal orientations are `q=1,2,3`, while
`q=0` has

```text
< t3,
  t1-h,
  t0+2t2-h,
  2h t2-h^2-1 >.                                      (9)
```

Thus `h=0` has no binary survivor.  On `h!=0`, the unique candidate is

```text
t0=-1/h,
t1=delta h,
t2=(h^2+1)/(2h),
t3=0.                                                  (10)
```

The infinity-chart projections give the same section:

```text
t0=-1,
t1=delta,
t2=(z^2+1)/2,
t3=0,                                                  (11)
```

in the exceptional orientation, and the unit ideal in the other three
orientations.  Elimination records the projective closure of (11) at
`z=0`; the exact fibre there is treated below.

## Uniform ternary obstruction

It is enough to work in the infinity chart with `z!=0`.  At (11), the
mixed matrix has rank six.  One `6 x 6` minor is

```text
128 z^7.                                               (12)
```

Writing a mixed extension as `u k0+v k1`, the two binary diagonal
values are

```text
d_alpha = delta(u-2v)/z,

d_beta =
 -(z^2-1)
  [u z^2-u+6v z^2+2v]/(2z^2).                        (13)
```

For mode one, the marked-map determinant on rows `(0,1,2,7)` is

```text
(u-2v)^2(z^2-1)
[u z^2-u+6v z^2+2v]/(2z^3).                          (14)
```

Away from `z=0,+/-1`, (14) is a chart unit times
`d_alpha^2 d_beta`.  Every genuine binary extension therefore has an
injective mode-one marked map, while the corresponding pure-hyperplane
column is nonzero.  No third target row can vanish on both
hyperplanes, so no `H31` lift exists.

At `z=0`, the mixed rank is four and its kernel has dimension four.
The first diagonal vanishes on the entire mixed kernel.  Hence the
closure point recorded by (11) has no genuine binary extension at all.

This excludes both curves (3), including `h=0` and `h=infinity`.
Together with the earlier regular-chart, factorized-fibre, and
pure-direction theorems, the complete nonzero-pure marked fibre on
`A=B=F=1` is empty.

## Verification

Run:

```text
python claims/p5/h31/diagonal-quadric-normalization-boundary/verify_p5_h31_diagonal_quadric_normalization_boundary.py
python claims/p5/h31/diagonal-quadric-normalization-boundary/audit_p5_h31_diagonal_quadric_normalization_boundary.py
```

The primary verifier checks (1)--(14), both projective charts, all
sixteen saturated relative projections, the explicit mixed kernels,
the all-extension marked determinant, and the exact `z=0` fibre.

The independent audit rebuilds every binary incidence system with a
subset-DP permanent, repeats all relative projections and boundary
identities, and then replays the primary verifier.
