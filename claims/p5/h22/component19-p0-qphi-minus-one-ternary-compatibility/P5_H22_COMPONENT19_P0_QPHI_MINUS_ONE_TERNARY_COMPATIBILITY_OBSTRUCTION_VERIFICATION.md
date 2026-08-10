# Independent ternary-compatibility obstruction on the `q*phi=-1` survivors

```yaml
role: verifier
date_utc: 2026-08-01T16:39:51Z
git_commit: 3120adce234373c37c66b6810af5e84dcc159231
claim_label: VERIFIED
scope: component 19 at p=0, q=-1/phi, lambda=1, h=(0,0,t,0), on the two Y=0 survivor axes X=0 and Z=0 with C*t*phi*(phi^2-1)*(phi^2+1)!=0
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  audit_p5_h22_component19_p0_qphi_minus_one_axes.py: 9485634b18e9c50786b1ae1f5cbd7f06d3ae27bec3cf4052158a49210f546992
  P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_AXES_VERIFICATION.md: e8d550934d401a8231acae0d7352ef9cfa9319402c920bb2835f7b518b833b16
method: fresh regular-basis reconstruction, subset-DP permanents, full complementary-cofactor maps, projection identities, and fixed two-slice Fitting minors
command: uv run --with sympy python audit_p5_h22_component19_p0_qphi_minus_one_ternary_compatibility.py
outputs:
  audit_p5_h22_component19_p0_qphi_minus_one_ternary_compatibility.py: 5cb01bbf6f4ae402e2348082e46a375b39747d9944171292cff461afe7fdc602
  P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_TERNARY_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md: hash emitted by replay
limitations: finite ordinary q=-1/phi chart only; excludes phi=0, phi^2=1, phi^2=-1, t=0, and zero extension; no projective weight boundary, other component, arbitrary-order, or global claim
```

## Verdict

Both residual all-one-marked-ranks survivors are **VERIFIED obstructed**.
Every one of their eight individual projected one-marked maps has rank at
most three, as previously verified.  However, at every local mode the full
`D01` and `D23` maps fail to factor through one common three-column target:
their stacked rank is four or five.

Thus neither `Y=0` axis gives a normalized weighted-`H22` lift on the stated
open.  The previous `UNKNOWN` status for these two finite survivors is closed
as `VERIFIED empty`.  No statement is made about excluded parameter or
projective-weight boundaries, and the global Krenn--Gu conjecture remains
unresolved.

## Exact compatibility equations

The two fifth-mode contraction rows at `lambda=1` are

```text
q01=(1,1,0,0,0),       q23=(0,0,1,1,0).
```

For a local mode `i`, let `N01_i,N23_i` be the full `8 x 5` one-marked
cofactor maps.  Their row indexed by a binary word on the other three modes
consists of the five complementary four-row permanents after adjoining the
corresponding contraction row.

A compatible three-column reconstruction at mode `i` is exactly a solution
of

```text
N01_i = U01_i R_i,
N23_i = U23_i R_i,                                 (1)
```

where `R_i` is one shared `3 x 5` local map and each `U` is `8 x 3`.
Elementary row-space linear algebra gives the exact equivalence

```text
(1) has a solution
  iff rank stack(N01_i,N23_i) <= 3.                (2)
```

The forward implication is immediate.  For the reverse implication, choose
the rows of `R_i` as a basis of the stacked row space and use the unique row
coordinates as `U01_i,U23_i`.  Consequently (2) is not merely another
one-slice necessary test: it is the full local sufficiency condition for a
shared three-column factorization of these two slices.  A common five-mode
tensor would require (1) in every local mode, so failure in any mode is an
obstruction.

The replay also verifies directly that

```text
N01_i = N01_i(projected) P01,
N23_i = N23_i(projected) P23,
```

by Laplace expansion along `q01,q23`.  This identifies the full maps with the
previous eight projected rank tests without assuming a construction formula.

## Axis `X=Y=0`

Write the nonzero axis coordinate as `C=Z`.  The extension is

```text
(x0,x1,x2,x3;y0,y1,y2,y3)
 = (0,-C/(phi^2+1),-C*phi/(phi^2+1),0;0,0,0,C).
```

All mixed coefficients vanish in both slices.  The four displayed diagonals
are

```text
(A01,B01,A23,B23)
 = (0,-4Ct,4C*phi/(phi^2+1),-4C/phi),
```

so the three required diagonals are nonzero on the frozen open.  The exact
rank data are

| mode | `rank N01` | `rank N23` | stacked rank | fixed nonzero determinant |
|---:|---:|---:|---:|---|
| 0 | 3 | 3 | 5 | rows `3,5,7,8,11`, all columns: `256 C^4 phi^4 t(phi-1)(phi+1)/(phi^2+1)^3` |
| 1 | 1 | 3 | 4 | rows `7,8,9,15`, columns `0,1,2,3`: `64 C^4 phi/(phi^2+1)^2` |
| 2 | 1 | 3 | 4 | rows `7,8,9,15`, columns `0,1,2,3`: `-64 C^4 phi/(phi^2+1)^2` |
| 3 | 3 | 3 | 4 | rows `4,5,7,8`, columns `0,1,2,4`: `128 C^3 t(phi+1)/(phi^2+1)^3` |

Every witness is nonzero under
`C*t*phi*(phi^2-1)*(phi^2+1)!=0`.

## Axis `Z=Y=0`

Now write `C=X`.  The extension is

```text
(x0,x1,x2,x3;y0,y1,y2,y3)
 = (0,C*phi/(phi^2+1),-C*phi^2/(phi^2+1),0;C,0,0,0).
```

Again all mixed coefficients vanish.  The diagonals are

```text
(A01,B01,A23,B23)
 = (0,-4C*phi*t,4C*phi^2/(phi^2+1),4C).
```

The exact ranks and fixed witnesses are

| mode | `rank N01` | `rank N23` | stacked rank | fixed nonzero determinant |
|---:|---:|---:|---:|---|
| 0 | 3 | 3 | 4 | rows `1,3,7,8`, columns `0,1,2,4`: `128 C^3 phi^6 t(phi-1)/(phi^2+1)^3` |
| 1 | 1 | 3 | 4 | rows `7,8,9,15`, columns `0,1,2,3`: `-64 C^4 phi^5/(phi^2+1)^2` |
| 2 | 1 | 3 | 4 | rows `7,8,9,15`, columns `0,1,2,3`: `-64 C^4 phi^3/(phi^2+1)^2` |
| 3 | 3 | 3 | 5 | rows `5,6,7,8,13`, all columns: `256 C^4 phi^4 t(phi-1)(phi+1)/(phi^2+1)^3` |

These are likewise nonzero everywhere on the frozen open.

## Evidence boundary and replay

- The reconstruction is exact over characteristic zero; no finite field or
  parameter grid is used.
- The final verifier evaluates only the eight fixed minors above.  It does not
  perform a broad minor scan.
- No construction or proof-side component-19 `p=0` compatibility artifact is
  imported.
- The result closes only the two finite ordinary survivors already isolated by
  the preceding independent audit.

Replay with

```powershell
uv run --with sympy python claims/p5/h22/component19-p0-qphi-minus-one-ternary-compatibility/audit_p5_h22_component19_p0_qphi_minus_one_ternary_compatibility.py
```
