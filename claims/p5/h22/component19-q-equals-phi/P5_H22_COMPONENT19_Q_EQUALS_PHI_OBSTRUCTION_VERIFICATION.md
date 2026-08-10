# Independent verification: component 19 weighted `H22` on `q=phi`

```yaml
role: verifier
date_utc: 2026-08-01T15:49:20Z
git_commit: 60b2250e8ce98fa0e787637401686f4edb65d306
claim_label: VERIFIED
scope: component 19 q=phi weighted-H22 obstruction over Q(p,phi) on p*phi!=0, plus parameter-aware audit of the phi=0 closure over Q(p)
inputs:
  - P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md sha256=ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: independent regular-basis reconstruction; exact squarefree permanents and pair minors; bidirectional finite/infinity incidence elimination over Q(p,phi); parameter-aware elimination over Q(p)[phi]; exact phi=0 pair-rank audit
command: uv run --with sympy python audit_p5_h22_component19_q_equals_phi_obstruction_candidate.py
outputs:
  - audit_p5_h22_component19_q_equals_phi_obstruction_candidate.py sha256=a26310924838c4b7f81974e5901e5ee10ec4dd2e75a0fd01b791cf74b666f1ac
  - P5_H22_COMPONENT19_Q_EQUALS_PHI_OBSTRUCTION_VERIFICATION.md
limitations: the generic theorem assumes p*phi!=0; phi=0 is audited only to locate the parameter-aware incidence closure and is outside the all-pair-open locus; no claim is made for other component divisors, component exhaustiveness, arbitrary-order reduction, or the global Krenn-Gu conjecture
```

## Verdict

The frozen `q=phi` claims are **VERIFIED** with no discrepancy.

The audit did not read, import, or execute the q=`phi` candidate report,
construction script, certificate, or proof-B artifacts.  It reconstructs the
family directly from the component source and runs standalone bounded exact
jobs.

## Regular basis, purity, and pair geometry

At `q=phi`, use

```text
alpha0 = B_bar+phi*B,
beta0  = A_bar+p*B.
```

Relative to the component theorem's displayed mode-zero rows this is their
reversal, with determinant `-1`; it remains regular at `phi=0`.  Together with
the unchanged rows in modes 1--3, the only nonzero pure coefficient is

```text
T_1111=4p.
```

On `p*phi!=0`, the exact pair profile in edge order
`01,02,03,12,13,23` is

```text
(4,4,3,3,3,3),
```

with fixed maximal-minor witnesses

```text
8p*phi, 8p, 4p^2, 4, -4, 4phi.
```

These are symbolic characteristic-zero determinants, not sampled ranks.

## Function-field incidence

Over `Q(p,phi)`, the audit separately checks both finite and projective-
infinity weight charts.  In each chart it checks four orientations:

```text
direct D01,
direct D23,
shared mixed system normalized by D01 diagonals,
shared mixed system normalized by D23 diagonals.
```

All eight exact projected ideals are

```text
(1).
```

Thus the complete individual and shared weighted binary incidences are empty
at the generic point of the `q=phi` divisor.  The weighted-`H22` fibre is empty
on `p*phi!=0`.

## Parameter-aware boundary audit

To prevent coefficient-field inversion of `phi` from hiding a boundary, the
same eliminations were repeated over `Q(p)` with `phi` retained as a polynomial
variable.  The parameter-aware finite and infinity results are

```text
direct D01 closure: <phi,h3,h2,h0>,
direct D23:          (1),
shared D01-oriented: (1),
shared D23-oriented: (1).
```

Hence the only nonunit projection closure lies entirely at

```text
phi=0, h0=h2=h3=0.
```

It is an individual `D01` closure only; it produces no shared orientation and
no `D23` incidence.

At `phi=0`, the `23` pair matrix has rank exactly two.  A fixed `2 x 2` minor
is `2`, while every `3 x 3` minor vanishes.  Therefore this residual closure is
outside the all-pair-open locus and does not weaken or extend the verified
generic theorem.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/component19-q-equals-phi/audit_p5_h22_component19_q_equals_phi_obstruction_candidate.py
```

Expected final marker:

```text
Q_EQUALS_PHI_AUDIT_VERIFIED
```

The replay uses file-backed Singular eliminations with bounded runtime and
removes its temporary solver inputs.
