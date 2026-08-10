# Component 19 weighted `H22` at `q=0`, `phi=+/-1` — VERIFIED

```yaml
role: construction
date_utc: 2026-08-01T15:28:56Z
git_commit: 6e6e02ad34c8462f2fc08087ee6fc73e3e543f28
claim_label: VERIFIED
discovery_claim_label: CANDIDATE
scope: q=0 and phi=+1 or phi=-1 separately over Q(p), p!=0
inputs: paths and SHA-256 hashes emitted by replay
method: separate endpoint reconstruction, projective shared incidence, exact three-kernels, saturated marked-rank strata
command: uv run --with sympy python claims/p5/h22/component19-q0-phi-endpoints/derive_p5_h22_component19_q0_phi_endpoints_obstruction_candidate.py
outputs: this report, its JSON certificate, and the standalone replay script
limitations: independently verified at both endpoints; finite opposite-plane chart only; no global conclusion
```

## Frozen result

**VERIFIED:** neither `q=0,phi=+1` nor `q=0,phi=-1` has a genuine
weighted-`H22` lift on `p!=0` in the finite component-19 chart.

The previous rank-six certificate cannot be specialized: at both endpoints
the shared `29 x 8` pure/binary matrix drops to rank five.  A direct endpoint
calculation finds the resulting three-dimensional extension kernel and a new
rank-four obstruction.  The two signs are reconstructed and eliminated
separately; no symmetry is used to transfer the conclusion.

## Specialized planes and intrinsic marking

Put `epsilon=+1` or `-1`.  Over `Q(p)`, reconstruct

```
U0=<Abar+pB,Bbar>,
U1=<B,A>,
U2=<Bbar,A>,
U3=<Abar,B+epsilon*Bbar>.
```

The intrinsic basis is

```
alpha0=-epsilon*(Abar+pB)-p*Bbar, beta0=Abar+pB,
alpha1=B,                            beta1=A,
alpha2=Bbar,                         beta2=A,
alpha3=Abar,                         beta3=B+epsilon*Bbar.
```

Its mode-zero change determinant is `p`.  For every affine marking, direct
permanent expansion gives only `T1111=4p`.  Four exact flattening kernels
recover the displayed `alpha_i` lines uniquely.  Direct pair minors give the
all-pair-open profile

`(3,4,4,3,3,3)`

with witnesses `4p,8p,-8epsilon,-4,4epsilon,4epsilon`.

## Complete projective incidence, separately for each sign

The finite `[lambda:1]` contractions and direct `[1:0]` maps are rebuilt at
each endpoint.  All four affine markings and one shared eight-coordinate
extension are retained.  Both beta diagonals are saturated as nonzero, and
the complete `H22` disjunction is split into the normalized orientations
`A01!=0` and `A23!=0`.  This includes their both-binary overlap.

For each sign, an individually binary `D01` unexpectedly exists on both
weight charts:

```
D01 binary: <p*h3+1,h1,h0-epsilon>.
```

This is a real endpoint phenomenon, but it is not shared-compatible.  Direct
same-extension elimination gives

```
shared A01, finite:    <1>
shared A01, infinity:  <1>
shared A23, finite:    <lambda-1,h3,h1,h0-epsilon>
shared A23, infinity:  <1>.
```

The individual `D23` ideals are also replayed:

```
finite:
  <h3,h0-epsilon,h1*h2*(lambda-1),h1^2*h2>
infinity:
  <h3,h0-epsilon,h1*h2>.
```

Thus the complete shared incidence has only

`[lambda:1]=[1:1],  h=(epsilon,0,t,0)`.

There is no infinity branch and no shared `A01` orientation.

## Exact three-dimensional shared kernels

On the surviving marking/weight, the combined `28 x 8` mixed matrix has the
same fixed rank-five witness at both signs:

```
rows    (1,2,10,12,15),
columns (0,1,2,3,6),
determinant 1024*p^3.
```

For `epsilon=+1`, its complete kernel is

```
vC=(0,-1/p, 1/p,0; 1,0,0,0),
vD=(0,0,0,0;         0,1,0,0),
vE=(p,0,-1,0;        0,0,0,1).
```

For `epsilon=-1`, it is

```
vC=(0,-1/p,-1/p,0; 1,0,0,0),
vD=(0,0,0,0;         0,1,0,0),
vE=(-p,0,1,0;        0,0,0,1).
```

Write `z=C*vC+D*vD+E*vE` and `Q=C-pE`.  Separate direct substitution at
both signs gives

```
A01=0,
B01=4*(pD-epsilon*t*Q),
A23=4*Q/p,
B23=4*C.
```

The exact genuine locus is

`C*Q*(pD-epsilon*t*Q) != 0`.

Thus the complete branch is automatically pure in direction `D01` and
genuinely binary in direction `D23`.

## Every one-marked rank

All minors are generated symbolically for each sign.  Saturating only by the
three genuine factors above gives the following exact classification:

```
D01 ranks:
  mode 0: rank 3, except rank 2 on
          2C-pE=0 and E*t-2*epsilon*D=0;
  mode 1: rank 1;
  mode 2: rank 1;
  mode 3: rank 4 everywhere genuine.

D23 ranks:
  mode 0: rank 3;
  mode 1: rank 3;
  mode 2: rank 4 iff D!=0, otherwise rank 3;
  mode 3: rank 4 everywhere genuine.
```

The replay proves the two “everywhere” statements by saturated unit ideals,
not generic ranks.  It also retains fixed lower-rank witnesses and verifies
all prohibited higher minors vanish.  On the exceptional `D01` mode-zero
locus, genuineness forces `C*t!=0`, and a displayed two-minor proves its rank
is exactly two rather than merely at most two.

Most importantly, rows `(0,2,3,7)` of the `D23` mode-three one-marked matrix
have determinant

```
phi=+1:  -64*C*(C-pE)^2,
phi=-1:   64*C*(C-pE)^2.
```

This is nonzero at every genuine point.  Hence the three-dimensional kernel
contains no `H22` lift; neither endpoint has a genuine survivor.

## Retained boundaries and failed lead

- `p=0` is excluded: the pure coefficient and intrinsic mode-zero basis both
  degenerate.
- `C=0`, `C-pE=0`, and `pD-epsilon*t*(C-pE)=0` are exactly the three
  nongenuine diagonal boundaries.
- The individual endpoint `D01`-binary family is a retained false lead.  Its
  shared `A01` projection is the unit ideal on both projective weight charts.
- Projective opposite-plane component boundaries are outside this finite
  chart.

No finite-field calculation, parameter grid, broad search, or generic-rank
inference is used.  The discovery label remains `CANDIDATE`, but both frozen
endpoint statements were independently reconstructed and are now `VERIFIED`.
See
[`P5_H22_COMPONENT19_Q0_PHI_ENDPOINTS_OBSTRUCTION_VERIFICATION.md`](P5_H22_COMPONENT19_Q0_PHI_ENDPOINTS_OBSTRUCTION_VERIFICATION.md).
This is not a global Krenn-Gu result.
