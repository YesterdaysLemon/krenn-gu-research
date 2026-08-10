# Candidate: component 19 `p=0`, `q=+/-1` target-local obstruction

```yaml
role: construction
date_utc: 2026-08-01T16:41:22Z
git_commit: 3120adce234373c37c66b6810af5e84dcc159231
claim_label: CANDIDATE
scope: ordinary p=0, q=s in {+1,-1}, phi*(phi^2-1)!=0 weighted-H22 fibres
inputs:
  - P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md sha256=ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  - audit_p5_h22_component19_p0_ordinary_obstruction_open.py sha256=a225c1f5e2c9a333448c95ffa999bebd4e685b9407fcfe488d798efdd8a73e75
method: reuse the independently reconstructed ordinary shared frame, enumerate every individual and stacked one-marked minor exactly, and saturate the individual rank-four ideal by the genuine diagonal open
command: uv run --with sympy python explore_p5_h22_component19_p0_q_endpoints.py --q 1; repeat with --q -1
outputs:
  - explore_p5_h22_component19_p0_q_endpoints.py sha256=f07ef6d0bc8d0afa8d05c62c26b80aa49096bc7218cfad483e999fdd367fac80
limitations: discovery script imports a prior audit and is not independent; phi=0 and phi^2=1 are excluded; zero/projective and valuative fibres are not addressed
```

## Candidate conclusion

For `s=+1` or `s=-1`, put `q=s` and retain the ordinary branch

```text
lambda=1, h=(0,0,t,0).
```

On `phi*(phi^2-1)!=0`, the complete shared extension frame has coordinates
`(X,Y,Z)` with genuine open

```text
F*G*H != 0,
F=phi*X+Z,
G=(s-phi)Y-tF,
H=X+sZ.
```

The exact individual one-marked rank-four ideal leaves precisely two
set-theoretic survivor families on that open:

```text
Y=Z=0, X*t!=0,
Y=0, 2*phi*X+(phi*s+1)*Z=0, Z*t!=0.
```

Neither family passes the shared target-local compatibility condition.  At
mode one, fixed stacked `D01/D23` four-minors are nonzero:

| endpoint | survivor | fixed stacked minor |
|---|---|---|
| `s=+1` | `Y=Z=0` | `64*X^3*phi^2/(phi-1)` |
| `s=+1` | oblique | `8*Z^3*(phi-1)^2/phi` |
| `s=-1` | `Y=Z=0` | `64*X^3*phi^2/(phi+1)` |
| `s=-1` | oblique | `-8*Z^3*(phi+1)^2/phi` |

Thus the script derives an empty ordinary weighted-`H22` fibre on both
endpoint opens.  This remains `CANDIDATE` until a no-import verifier rebuilds
the bases, shared kernel, complete individual-rank survivor classification,
and stacked-minor condition independently.

The omitted intersections `q*phi=-1` are treated by a separate target-local
argument.  The points `q=phi=+1` and `q=phi=-1` lie on the zero base and are
not part of this ordinary claim.

## Replay

```powershell
uv run --with sympy python explore_p5_h22_component19_p0_q_endpoints.py --q 1
uv run --with sympy python explore_p5_h22_component19_p0_q_endpoints.py --q -1
```

Expected marker on each run:

```text
OPEN_SURVIVOR
```

That marker refers only to the individual rank-four tests.  The printed
mode-one stacked minors then obstruct both listed survivors.
