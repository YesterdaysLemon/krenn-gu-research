# Component 19 `p=0`, `q*phi=-1` axis target-local proof B

```yaml
role: proof_b
date_utc: 2026-08-01T16:37:04Z
git_commit: 3120adce234373c37c66b6810af5e84dcc159231
claim_label: DERIVED
scope: ordinary p=0,q*phi=-1 axis extensions X=Y=0,Z*t!=0 and Z=Y=0,X*t!=0
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: fresh regular p0 reconstruction, exact shared binary contractions, full-target one-marked maps, and fixed stacked four-minors
command: uv run --with sympy python derive_p5_h22_component19_p0_qphim1_axis_target_local_proof_b.py
outputs: replay stdout gives final path and sha256 pairs
limitations: ordinary axis fibres only; phi^2=-1 zero tensor, projectivized, valuative, closure, arbitrary-order, and global claims excluded
```

## Result

Both residual axes are exactly obstructed.  Their individual projected
one-marked maps all have rank at most three, but the two weighted slices do
not factor through a common three-dimensional target-local space.  A fixed
stacked four-minor is nonzero on each entire ordinary genuine axis.

No construction-agent `p=0` artifact was inspected.

## Fresh ordinary reconstruction

Set `q=-1/phi` in the regular `p=0` bases

```text
(alpha0,beta0)=(Abar,Bbar-B/phi),
(alpha1,beta1)=(B,A),
(alpha2,beta2)=(Bbar,A),
(alpha3,beta3)=(Abar,B+phi*Bbar).
```

The only pure coefficient is

```text
T_1111=-4*(phi^2+1)/phi.
```

Hence the ordinary locus is `phi*(phi^2+1)!=0`.  The shared finite
orientation is `lambda=1`, with `h=(0,0,t,0)`.  Put `s=phi^2+1`.

For `X=Y=0`, the complete shared extension specializes to

```text
C=(0,-Z/s,-phi*Z/s,0),
D=(0,0,0,Z).
```

Its nonzero binary diagonals are

```text
B01=-4*t*Z,
A23=4*phi*Z/s,
B23=-4*Z/phi.
```

For `Z=Y=0`, the extension is

```text
C=(0,phi*X/s,-phi^2*X/s,0),
D=(X,0,0,0),
```

with diagonals

```text
B01=-4*phi*t*X,
A23=4*phi^2*X/s,
B23=4*X.
```

Thus `Z*t!=0` and `X*t!=0`, respectively, are exactly the genuine axis
conditions on the ordinary parameter locus.

## Full target-local condition

The two slice restrictions on a full target row
`y=(y0,y1,y2,y3,y4)` are

```text
rho01(y)=(y0+y1,y2,y3,y4),
rho23(y)=(y0,y1,y2+y3,y4).
```

For mode `i`, let `N01_i` and `N23_i` be the full `8 x 5` one-marked maps:
the other three marked rows are restricted by `rho01` or `rho23`, while the
marked input ranges over all five full target coordinates.

A common ternary target-local factorization at mode `i` exists exactly when
the row spaces of these two maps lie in one subspace of dimension at most
three.  Equivalently,

```text
rank stack(N01_i,N23_i) <= 3.                     (1)
```

This is stronger than checking each projected map separately.

Direct exact reconstruction confirms that every individual four-minor
vanishes.  Over the corresponding axis function fields their ranks are

```text
             modes 0 1 2 3
D01 ranks:         3 1 1 3
D23 ranks:         3 3 3 3.
```

Thus these are genuine survivors of every separate one-marked rank test.

## Uniform stacked obstruction

Order each map's rows by binary words `000,...,111`, put the eight `D01`
rows first and the eight `D23` rows second, and use full-target columns
`0,...,4`.  At mode one, rows `(7,8,9,15)` and columns `(0,1,2,3)` give

```text
X=Y=0 axis:  64*Z^4*phi/(phi^2+1)^2,
Z=Y=0 axis: -64*X^4*phi^5/(phi^2+1)^2.            (2)
```

Both expressions are nonzero whenever the corresponding axis is genuine
and the ordinary tensor is nonzero.  Therefore the stacked rank is at least
four in mode one on both complete axes, contradicting (1).  Neither axis
admits a shared ternary weighted-`H22` lift.

The obstruction remains nonzero at `phi=+1` and `phi=-1`; those are ordinary
points on `q*phi=-1`.  Only `phi^2=-1`, where `q=phi` and the restricted
tensor is zero, is excluded.  Projectivized directions there and all
valuative or closure fibres remain `UNKNOWN`.  This claim is `DERIVED` and
requires independent verification before promotion.
