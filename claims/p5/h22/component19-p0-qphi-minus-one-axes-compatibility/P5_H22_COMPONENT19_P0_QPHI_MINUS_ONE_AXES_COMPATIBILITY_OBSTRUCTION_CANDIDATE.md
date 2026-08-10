# Component 19 `q*phi=-1` residual axes: actual `H22` compatibility obstruction — CANDIDATE

```yaml
role: construction
date_utc: 2026-08-01T16:40:34Z
git_commit: 3120adce234373c37c66b6810af5e84dcc159231
claim_label: CANDIDATE
scope: actual ternary weighted-H22 reconstruction on X=Y=0 and Z=Y=0 at p=0, q=-1/phi, phi*(phi^2-1)*(phi^2+1)!=0
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_AXES_VERIFICATION.md: e8d550934d401a8231acae0d7352ef9cfa9319402c920bb2835f7b518b833b16
  P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md: 7d817f91a5a24512e092dca125258ad5a3753bbb97b6199ad2b6c202c9d91965
method: direct source reconstruction, complete shared extension frame, and fixed full two-contraction third-row stack determinants
command: uv run --with sympy python claims/p5/h22/component19-p0-qphi-minus-one-axes-compatibility/derive_p5_h22_component19_p0_qphi_minus_one_axes_compatibility_obstruction.py
outputs: this report, its JSON certificate, and the bounded standalone replay
limitations: construction result pending independent verification; only the two Y=0 residual axes are covered
```

## Frozen result

**CANDIDATE:** neither verified one-marked-rank survivor reconstructs to an
actual ternary weighted-`H22` lift.

The obstruction uses the full shared third-row equations, not the rank of an
individual projected one-marked map.

## Source frame

Set

```text
q=-1/phi,
r=q-phi=-(phi^2+1)/phi,
lambda=1,
h=(0,0,t,0),
phi*(phi^2-1)*(phi^2+1)!=0.
```

Direct reconstruction from the component planes gives the complete shared
extension frame

```text
vX=(0,-1/r,phi/r,0; 1,0,0,0),
vY=(0,0,0,0;         0,1,0,0),
vZ=(0,-q/r,1/r,0;    0,0,0,1).
```

The combined mixed matrix has rank five; rows `(2,9,10,12,15)` and columns
`(0,1,2,3,6)` have determinant

`1024*(phi^2+1)^2/phi^3`.

The two residual extensions are exactly

```text
X=Y=0: z=Z*vZ,  Z*t!=0,
Z=Y=0: z=X*vX,  X*t!=0.
```

Their binary mixed coefficients vanish and their required binary diagonals
are nonzero on the displayed open.

## Actual ternary reconstruction equations

In normalized `H22` target colours, the existing rows are

```text
alpha=E1,  beta=E2,
```

and the missing third row `gamma_i` represents `E0`.  For each mode `i`, let

```text
F_i^01, F_i^23 : K^5 -> K^8
```

be the full one-`gamma` coefficient maps formed from the reconstructed
five-coordinate alpha/beta rows and contraction rows

```text
q01=(1,1,0,0,0),
q23=(0,0,1,1,0).
```

An actual ternary lift requires, simultaneously,

```text
F_i^01(gamma_i)=0,
F_i^23(gamma_i)=0
```

for every mode.  These are the degree-one part of the full factorization
equations; only after solving them would coefficients containing two or more
`gamma` rows remain.

## Axis `X=Y=0`

At mode zero, stack `F_0^01` over `F_0^23`.  The resulting `16 x 5` matrix
has rows `(3,5,7,8,11)` determinant

```text
256*Z^4*phi^4*t*(phi-1)*(phi+1)/(phi^2+1)^3.
```

Every factor is nonzero on the axis open, so the shared reconstruction
equations force

`gamma_0=0`.

## Axis `Z=Y=0`

At mode three, stack `F_3^01` over `F_3^23`.  Rows `(5,6,7,8,13)` have
determinant

```text
256*X^4*phi^4*t*(phi-1)*(phi+1)/(phi^2+1)^3.
```

Thus the second axis forces

`gamma_3=0`.

## Contradiction

The normalized `H22` target has a nonzero `D01` `gamma^4` coefficient
`lambda0`.  On the first axis `gamma_0=0`, and on the second axis
`gamma_3=0`; either condition makes that diagonal permanent zero.  Therefore
neither axis can satisfy the actual ternary factorization equations.

The obstruction occurs at the shared linear reconstruction stage, before
any coefficient containing two, three, or four `gamma` rows needs to be
solved.  Hence the earlier individual rank-three maps were necessary-condition
survivors but not genuine lifts.

No finite-field computation or broad search is used.  The special
`phi^2=1` and `phi^2=-1` fibres, other component boundaries, arbitrary-order
reduction, and the global Krenn–Gu conjecture remain outside scope.
