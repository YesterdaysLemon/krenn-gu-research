# Refuted full weighted-`H22` obstruction on the embedded-`P3` free-plane `r0=0` divisor

Discovery run report (before independent verification):

```yaml
role: proof_a
date_utc: 2026-08-01T11:18:00Z
git_commit: 7392ae7e7352a66fc5c42cb017d002043dfd794f
claim_label: CANDIDATE
scope: weighted H22 on the omitted free mode-zero-plane normalization divisor r0=0 of the embedded-P3 pure-P4 component, including homogeneous weight infinity and the corner t0=0
inputs:
  P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md: 3471170831a745c05f2fb2f462719b42ad643da49d4ffe5f3ea56ffd07bfd9a1
  verify_p5_h31_embedded_p3_component_r_zero_boundary.py: c0a9069d8d4cc0522e592a797eacd1fd092f932655b712ceac1c4261c2ee5c10
  P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md: dfc2ca99ac668605b54a08b2a4dfb48f74abba97ae2ecc405121d21b8e7f3f4a
  P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md: baf5531740cfd77207f31cf8e1de2b5b838701cbcae5ec778667e6e7f712d15e
  P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md: 7ae8c19e5a43ac7af2cac35892af59130555ab509495d5280745aad114eed056
method: homogeneous direction transport, exact characteristic-zero elimination of the simultaneous D01-binary and D23-pure incidence, saturated kernel calculation, and inherited verified H31 one-marked covers
command: uv run --with sympy python derive_p5_h22_embedded_p3_component_r_zero_boundary_obstruction.py
outputs:
  derive_p5_h22_embedded_p3_component_r_zero_boundary_obstruction.py: ee760b9db4e4ae6526e55824b483c626612df9ffefcc0bccee82b21433f59458
  P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION_CANDIDATE.md: hash reported by replay
limitations: candidate pending independent replay; the H31 corner theorem is an explicit dependency; no component-exhaustiveness, arbitrary-order local-to-global reduction, prize graph, or global Krenn-Gu claim is made
```

## Status and frozen claim

**REFUTED as a proof of the full homogeneous divisor.**  The exact
characteristic-zero calculation below independently verifies the `t0=0`
corner obstruction on the omitted free-plane divisor

```text
U0=span((1,0,r0,t0),(0,1,S,U)),        r0=0.
```

This is not the refuted normal-base `[C:A:B]` transport.  The fresh verifier
replayed the corner elimination and the verified `H31` dependency without
importing this derivation.  It also found that the proposed `t0!=0` source
transport reverses the `D23` weight but preserves the `D01` weight.  An
invertible rebalance repairs this only when both homogeneous weight coordinates
are nonzero.  The `t0!=0` fibres at `[rho:sigma]=[0:1]` and `[1:0]` therefore
remain `UNKNOWN`.  No finite-field calculation is used as proof.

## Direct corner model and homogeneous directions

At `r0=t0=0`, use

```text
alpha0=(0,1,S,U),              beta0=(1,0,0,0),
alpha1=(0,-1,1,0),             beta1=(0,-1,0,1),
alpha2=(0, 1,0,1),             beta2=(0, 1,1,0),
alpha3=(0, 0,1,1),             beta3=(0,-1,0,1),
```

and mark `betai -> betai+hi alphai`.  For homogeneous weight
`[rho:sigma]`, reconstruct

```text
D01^[rho:sigma](z,e)=(rho z0+sigma z1,z2,z3,e),
D23^[rho:sigma](z,e)=(z0,z1,rho z2+sigma z3,e).
```

Every `D23` all-alpha coefficient is structurally zero because every
`alphai` has source coordinate zero equal to zero.  Consequently a genuine
weighted-`H22` pair must consist of a binary `D01` slice and a nonzero pure
all-beta `D23` slice, with the same homogeneous weight.

At `[rho:sigma]=[1:0]`, exact elimination of their shared eight extension
coordinates, the two nonzero-diagonal inverses, and all markings returns the
unit ideal.  Thus there is no compatible pair at infinity.

## Complete finite-weight projection

Put `lambda=rho/sigma` for `sigma!=0` and set `(a,b,c)=(h1,h2,h3)`.  The exact
simultaneous incidence imposes the fourteen mixed `D01` equations, nonzero
`D01` diagonals, the fifteen unwanted `D23` equations, and a nonzero all-beta
`D23` diagonal.  Eliminating the two independent eight-coordinate extension
vectors and two inverses gives the following projected ideal in
`Q[h0,a,b,c,lambda,S,U]`:

```text
lambda(S-U),
lambda(lambda+1),
lambda U(2c+1),
lambda U(b+1),
lambda U(a+1),
h0 U,
h0 S,
h0(lambda+1),
2bc lambda+h0+2b lambda+lambda,
2ac lambda-h0-lambda,
2h0 c+h0+2c lambda+lambda,
Phi,
ab lambda-h0-lambda,
h0 b+h0+b lambda+lambda,
h0 a+h0+a lambda+lambda,
h0(h0-1),
```

where

```text
Phi =
 S { U[(S-U)(a+1)(b+1)-a(b+1)+1] + b(S+1) }
 + c { S b(S+U+1) + U a(1-S-U) }.
```

The derivation script verifies equality of this ideal with the fresh
elimination ideal in both directions; it is not merely a necessary-factor
list.  It leaves exactly two finite-weight branches.

### The `lambda=0` branch

Specializing the displayed ideal at `lambda=0` gives exactly

```text
h0=0,                    Phi=0.
```

Here the `D01` slice is literally the deletion-zero insertion problem of
`P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md`.  That verified
theorem classifies every generic, signed-sheet, zero-coordinate, and singular
marking/kernel family and supplies a nonzero one-marked rank/transverse cover.
Its conclusion is stronger than needed here: no additional local row can
survive, including the required nonzero pure `D23` row.  Hence this branch is
empty, conditional only on the cited verified `H31` theorem.

### The `lambda=-1`, `S=U=s` branch

If `s!=0`, the projected ideal forces

```text
(h0,a,b,c)=(0,-1,-1,-1/2).
```

The complete `D01` mixed kernel, after saturation by `s`, is

```text
z3=z5=z6=0,       z1=z0,       z2=-z0,       z7=z0.
```

Writing its two parameters as `X,Y`, the two required diagonals and one fixed
mode-1 minor are

```text
A01=4sY,
B01=-2(X+Y),
det(rows 0137)=-16 s^2 Y^2(X+Y).
```

Thus the minor is nonzero whenever the `D01` slice is genuine.  The saturation
is uniform for every `s!=0`, including `s=+/-1/2`.  The compatible `D23` pure
matrix has rank four and kernel-diagonal values `(0,0,2,-2)` on a displayed
four-vector basis, so nonzero pure directions really exist; they are excluded
by the `D01` one-marked obstruction rather than silently discarded.

At `s=0,h0=0`, the same complete two-dimensional `D01` kernel has
`A01=0`, so it is not genuine.

At `s=0,h0=1`, the projected ideal has exactly the three components

```text
(h0,a,b,c)=(1,0,0,c),
(h0,a,b,c)=(1,a,0,0),
(h0,a,b,c)=(1,0,b,-1).
```

The projected marked `beta0` row is zero.  These are therefore exactly the
three `(S,U)=(0,0)` singular marking families in the verified `H31` corner
theorem, whose fixed one-marked determinants close them.  No denominated
generic frame is used at their endpoints.

## The part with `t0!=0`

Apply the signed source swap

```text
P:(x0,x1,x2,x3) -> (x0,x1,-x3,-x2).
```

It sends `(1,0,0,t0)` to `(1,0,-t0,0)`, so the normalized component parameter
is `r0'=-t0!=0`.  Directly on the homogeneous contractions,

```text
D01^[rho:sigma](Pz,e)
```

is `D01^[rho:sigma](z,e)` followed by an invertible sign/swap of its second
and third target coordinates, while

```text
D23^[rho:sigma](Pz,e)
```

is `D23^[sigma:rho](z,e)` followed by a sign on its third target coordinate.
Thus the projective weights are swapped for `D23`.  When `rho*sigma!=0`, an
invertible diagonal rebalance restores a common weight and the normalized
generic, rank-two-line, and rank-one weighted-`H22` theorems apply.  At
`[rho:sigma]=[0:1]` and `[1:0]` that rebalance is singular, so the two endpoint
fibres are not covered by this argument.

## Honest boundary and failure ledger

- The direct `t0=0` characteristic-zero elimination and kernel saturation are
  independently verified.  The full homogeneous-divisor claim is `REFUTED`
  because the two `t0!=0` weight endpoints remain `UNKNOWN`.
- A slower exploratory elimination over `Q(S,U)` with the finite weight also
  eliminated returned `<h0,Phi>` after 47 seconds.  It is corroboration only
  and is superseded by the faster global ideal equality above.
- Direct formulas on the deepest `h0=1` families initially introduced
  denominators and did not uniformly cover their endpoints.  They were not
  used.  The argument instead identifies those families with the already
  verified denominator-free `H31` singular-base cover.
- This note treats only this component divisor.  It does not prove that the
  known pure-`P4` components are exhaustive, close other components, or prove
  the arbitrary-order local-to-global reduction.

The independent report is
`P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_VERIFICATION.md`.

## Replay

Run

```text
uv run --with sympy python derive_p5_h22_embedded_p3_component_r_zero_boundary_obstruction.py

uv run --with sympy python audit_p5_h22_embedded_p3_component_r_zero_boundary_independent.py
```

The script reconstructs the permanent contractions from the four planes,
checks the infinity unit ideal, proves bidirectional equality of the finite
projected ideal, verifies the saturated `s!=0` kernel and fixed minor, checks
the deepest `s=0` branches, and records hashes of every theorem dependency.
