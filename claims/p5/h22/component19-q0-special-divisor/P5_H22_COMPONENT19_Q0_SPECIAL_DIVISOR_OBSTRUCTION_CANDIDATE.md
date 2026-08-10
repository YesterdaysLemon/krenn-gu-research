# Component 19 weighted `H22` on `q=0` — VERIFIED

```yaml
role: construction
date_utc: 2026-08-01T15:09:51Z
git_commit: 6e6e02ad34c8462f2fc08087ee6fc73e3e543f28
claim_label: VERIFIED
discovery_claim_label: CANDIDATE
scope: component 19 finite divisor q=0 over Q(p,phi), with p*phi*(phi^2-1)!=0
inputs: paths and SHA-256 hashes emitted by the replay
method: direct specialized planes, exact permanents/minors, direct finite/infinity elimination, shared kernel and marked minor
command: uv run --with sympy python derive_p5_h22_component19_q0_special_divisor_obstruction_candidate.py
outputs: this report, its JSON certificate, and the standalone replay script
limitations: independently verified on the stated open; excluded parameter/projective boundaries remain open; no global conclusion
```

## Result and specialization warning

**VERIFIED:** the weighted-`H22` fibre is empty on

`q=0,   p*phi*(phi^2-1) != 0`.

This is reconstructed over `Q(p,phi)` from the specialized planes.  It is
not obtained by substituting `q=0` into the generic component-19 theorem.
That distinction matters: direct elimination adds the generator
`h1^2*h2` to the finite `D23` binary ideal.  Naive specialization omits it
and creates false survivors at weight `lambda=1`.

## Specialized pure point and all-pair-open status

With

```
A=X0+X1,  Abar=X0-X1,  B=X2+X3,  Bbar=X2-X3,
```

the `q=0` planes are

```
U0=<Abar+pB, Bbar>,
U1=<B,A>,
U2=<Bbar,A>,
U3=<Abar,B+phi Bbar>.
```

The intrinsic pure basis reconstructed from these planes is

```
alpha0=-phi(Abar+pB)-p Bbar,  beta0=Abar+pB,
alpha1=B,                      beta1=A,
alpha2=Bbar,                   beta2=A,
alpha3=Abar,                   beta3=B+phi Bbar.
```

The mode-zero change of basis has determinant `p`.  Hence it is valid on the
stated open.  After every affine marking `betai -> betai+hi alphai`, exact
permanent expansion gives only

`T1111=4p`.

Thus the pure restriction is nonzero, and its four flattening kernels recover
the displayed `alpha_i` lines uniquely.  Direct squarefree pair calculations,
not the generic profile, give

`(rank01,rank02,rank03,rank12,rank13,rank23)=(3,4,4,3,3,3)`.

Fixed nonzero witnesses are respectively

`4p, 8p, -8phi, -4, 4phi, 4phi`.

Every pair is therefore open (rank at least three).  Notice that `q=0`
really lowers edge `01` from the generic rank four to rank three without
leaving the all-pair-open locus.

## Complete projective weight and marking elimination

The finite homogeneous chart `[lambda:1]` uses

```
D01(z,e)=(lambda*z0+z1,z2,z3,e),
D23(z,e)=(z0,z1,lambda*z2+z3,e).
```

The `[1:0]` maps are built separately.  Eight extension coordinates and all
four affine markings are eliminated only after saturating every required
nonzero diagonal.  Bidirectional standard-basis comparison over `Q(p,phi)`
gives

```
D01 binary, finite:    <1>
D01 binary, infinity:  <1>

D23 binary, finite:
  <h3, phi*h0-1, h1*h2*(lambda-1), h1^2*h2>

D23 binary, infinity:
  <h3, phi*h0-1, h1*h2>.
```

Set-theoretically the finite `D23` locus has `h1*h2=0` even at
`lambda=1`; the last generator is essential there.  Since `D01` is never
binary, the orientation “`D23` pure, `D01` binary” is empty on both weight
charts.

For the only possible orientation, impose a nonzero pure `D01` contraction
and genuinely binary `D23` contraction using the same marking, weight, and
extension.  Direct shared elimination gives

```
finite:   <lambda-1, h3, h1, phi*h0-1>,
infinity: <1>.
```

Consequently the complete shared survivor is

`lambda=1,   h=(1/phi,0,t,0)`.

There is no infinity branch.

## Complete shared extension and transverse obstruction

On the shared branch, the 29 unwanted coefficients form a `29 x 8` linear
matrix.  Rows `(2,3,5,11,13,16)` and columns `(0,1,2,3,6,7)` have determinant

`4096*p^4*phi^2*(phi-1)*(phi+1)`.

It is a unit on the stated open.  The matrix therefore has rank six, and its
complete two-dimensional kernel is

```
vC=(0,-1/p,phi/p,0; 1,0,0,0),
vD=(0,0,0,0;       0,1,0,0).
```

For the shared extension `z=C*vC+D*vD`, the required diagonals are

```
B01=4*(pD-phi*t*C),
A23=4*phi^2*C/p,
B23=4*C.
```

Their common genuine locus is exactly

`C*(pD-phi*t*C) != 0`

after using `p*phi != 0`.  The mode-three `D01` one-marked matrix has the
fixed rows `(1,2,5,7)` determinant

`-64*C*p*(pD-phi*t*C)^2`.

This is nonzero at every common genuine extension.  Hence that one-marked
map has rank four, contradicting the rank-at-most-three transverse
factorization required by a weighted-`H22` lift.  The shared branch is empty.

## Denominators, omitted sub-divisors, and retained failure

Every division is visible:

- `p^-1` enters the complete extension frame and `p` is also the mode-zero
  basis determinant and pure coefficient factor;
- `phi^-1` enters the unique shared marking;
- `(phi^2-1)` is not divided by, but it is a genuine rank-witness factor.
  At `phi=1` and `phi=-1`, the shared unwanted matrix has rank five rather
  than six, so those sub-divisors remain open rather than being cancelled;
- `C=0` kills the `D23` diagonals, and `pD-phi*t*C=0` kills the `D01`
  diagonal.  These are nongenuine extension boundaries, not survivors.

The generic low-rank false lead specializes to

```
h=(1/phi,0,0,0),   [rho:sigma]=[1-phi:phi+1].
```

A `D23` extension then has one-marked ranks `(3,3,3,3)`, while a separate
pure `D01` extension has `(2,3,3,3)`.  Their extension vectors have a fixed
proportionality minor `1`, and the shared ideal requires `[1:1]`.  They do
not form a shared `H22` lift.

No finite-field computation, parameter grid, broad search, or imported
generic conclusion is used.  The discovery label remains `CANDIDATE`, but
the frozen claim was independently reconstructed and is now `VERIFIED` on
the stated open.  See
[`P5_H22_COMPONENT19_Q0_SPECIAL_DIVISOR_OBSTRUCTION_VERIFICATION.md`](P5_H22_COMPONENT19_Q0_SPECIAL_DIVISOR_OBSTRUCTION_VERIFICATION.md).
It does not address `phi^2=1`, projective opposite-plane
boundaries, component exhaustiveness, arbitrary-order reduction, or the
global Krenn-Gu conjecture.
