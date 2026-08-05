# Aggregate verification of the component-19 `p=0` ordinary divisor

```yaml
role: verifier
date_utc: 2026-08-01T17:08:18Z
git_commit: 17a4054ebe42316dd3c9f2bf8839c656520625ed
claim_label: VERIFIED
scope: set-theoretic exhaustion of the complete projective weighted fibre over the finite ordinary nonzero all-pair-open component-19 p=0 divisor q*phi*(q-phi)!=0
inputs:
  P5_H22_COMPONENT19_P0_ORDINARY_OBSTRUCTION_OPEN_VERIFICATION.md: 40a1932b552411e64ec5a44a488ea99d0d4ac985126dddff2ff177fd1b941708
  P5_H22_COMPONENT19_P0_QPHI_ONE_INDEPENDENT_VERIFICATION.md: ef84810ae00d0b55801485df634b228bc85188fcb57948e0645533170730b067
  P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_AXES_VERIFICATION.md: e8d550934d401a8231acae0d7352ef9cfa9319402c920bb2835f7b518b833b16
  P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_TERNARY_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md: 0055f9660824f5536a29f0e2b74c749510e00388f8b2912dc747a306ff8805c8
  P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_PHI_ENDPOINTS_VERIFICATION.md: f37a93cde469ebcee173ef43cc18a0bd7a4af1fcd4a6b30a2785b3bab1be77a9
  P5_H22_COMPONENT19_P0_QPHIM1_INFINITY_NO_IMPORT_VERIFICATION.md: f9180f95e7d0bb57c93342a54a9b724c8abab1f25adf621f7275e268a41498c3
  P5_H22_COMPONENT19_P0_Q_ENDPOINTS_NO_IMPORT_VERIFICATION.md: 13af04b480d4bba44aeee7b5396a6b12ba10256a4d30bd29969e70a14ce46627
  P5_H22_COMPONENT19_P0_PHI_ENDPOINTS_NO_IMPORT_VERIFICATION.md: 128da2990f6800146375d78916279d0127eff372e3eab412d9d0f020bd6612b3
method: live replay of eight verified exact certificates and an exact polynomial-identity case ledger for every exceptional intersection
command: uv run --with sympy python audit_p5_h22_component19_p0_finite_ordinary_aggregate.py
outputs:
  audit_p5_h22_component19_p0_finite_ordinary_aggregate.py: 65cafa89b709f0466d7fd51fc2555f60cec9246b6f68034ffa4ed94dc41180f7
  P5_H22_COMPONENT19_P0_FINITE_ORDINARY_AGGREGATE_VERIFICATION.md: hash emitted by replay
limitations: finite ordinary nonzero all-pair-open p=0 base only; q=phi zero base, q=0 or phi=0 lower-pair boundaries, projectivized or valuative base directions, other components, arbitrary-order reduction, and the global conjecture are not claimed
```

## Verdict

**VERIFIED.**  The exact component-19 `p=0` reports exhaust, set-theoretically,
the entire finite ordinary nonzero all-pair-open parameter divisor

```text
D = {q*phi*(q-phi) != 0}.                          (1)
```

Every point of `D` has empty weighted-`H22` fibre.  Both finite weight and
weight-at-infinity charts are covered, so the complete projective weight line
is closed over `D`.

There is no residual `UNKNOWN` locus inside (1).  This is a component-local
`p=0` theorem, not a proof of component exhaustiveness, arbitrary-order
reduction, or the global Krenn--Gu conjecture.

## Exact parameter partition

Away from

```text
(q^2-1)*(phi^2-1)*((q*phi)^2-1)=0,                 (2)
```

the generic ordinary verifier applies.  Every point on (2) belongs to one of
the following exact cases.

| Case inside `D` | Exact coverage |
|---|---|
| `(q*phi)^2 != 1`, `q^2 != 1`, `phi^2 != 1` | generic ordinary open |
| `q*phi=1` | complete specialized `q*phi=1` theorem |
| `q*phi=-1`, `phi^2!=1,-1`, `X*Z!=0` | exact specialization of the generic `M0` identity |
| `q*phi=-1`, `phi^2!=1,-1`, `X*Z=0` | axes rank classification plus full target-local compatibility |
| `q*phi=-1`, `phi^2=1` | complete crossing theorem, including its enlarged non-axis `Y=0` sheet |
| `q^2=1`, `(q*phi)^2!=1` | complete `q=+/-1` endpoint theorem |
| `phi^2=1`, `(q*phi)^2!=1` | complete `phi=+/-1` endpoint theorem |

The aggregate replay verifies the polynomial identities

```text
phi*(q-phi) = 1-phi^2       on q*phi=1,
phi*(q-phi) = -(1+phi^2)    on q*phi=-1.            (3)
```

Thus `q*phi=1` meets `q=phi` exactly at `phi^2=1`, so those two points are
zero-base points outside `D`.  On `q*phi=-1`, the value `phi^2=-1` likewise
gives `q=phi` and is outside `D`; the remaining special values `phi^2=1` are
the two verified crossings.

The endpoint intersections are also exact.  Modulo `q^2-1`,

```text
q-phi = q*(1-q*phi),       q+phi = q*(1+q*phi),
```

and the analogous identities hold after exchanging `q` and `phi`.  Hence a
double endpoint `q^2=phi^2=1` has `q*phi=+1` or `-1`: the first sign is the
excluded zero base, while the second is the verified crossing.  No endpoint
intersection is omitted.

## The `q*phi=-1` fibre split is essential

For `q=-1/phi`, the exact generic one-marked determinant specializes to

```text
M0 = 128*G*X*Z*phi^3*(phi-1)*(phi+1)/(phi^2+1)^2.  (4)
```

On `phi*(phi^2-1)*(phi^2+1)*G*X*Z!=0`, equation (4) closes the off-axis
locus directly.  This is an exact specialization of the replayed determinant,
not a continuity argument.

When `X*Z=0`, genuineness excludes `X=Z=0`.  The axes verifier forces the
only individual-rank survivors to `Y=0`; the full `8 x 5` compatibility replay
then obstructs both residual axes.  At `phi^2=1`, the axes-only description is
no longer complete: the individual-rank locus jumps to the full sheet

```text
Y=0,       t*(phi*X+Z)*(X-phi*Z)!=0,
```

including `X*Z!=0`.  The crossing verifier closes this full sheet by its
uniform stacked determinant.  Keeping these three pieces separate prevents
the aggregate from hiding the endpoint jump.

## Projective weight coverage

The generic, `q*phi=1`, `q`-endpoint, and `phi`-endpoint replays each include
their weight-at-infinity chart.  The remaining specialized infinity divisor
`q*phi=-1` is independently **VERIFIED empty** on its exact ordinary open

```text
phi*(phi^2+1)!=0,
```

which is equivalent to (1) on `q*phi=-1` and includes `phi^2=1`.  Its exact
mixed-row identity expresses the required `A23` diagonal in the ideal of two
`D01` mixed coefficients, so no genuine infinity incidence exists.  The
finite and infinity charts therefore cover the full weight `P^1` over `D`.

## Replayed evidence

- [Generic ordinary open](P5_H22_COMPONENT19_P0_ORDINARY_OBSTRUCTION_OPEN_VERIFICATION.md) — [replay](audit_p5_h22_component19_p0_ordinary_obstruction_open.py)
- [`q*phi=1`](P5_H22_COMPONENT19_P0_QPHI_ONE_INDEPENDENT_VERIFICATION.md) — [replay](audit_p5_h22_component19_p0_qphi_equals_one.py)
- [`q*phi=-1` axes](P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_AXES_VERIFICATION.md) — [replay](audit_p5_h22_component19_p0_qphi_minus_one_axes.py)
- [`q*phi=-1` target-local compatibility](P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_TERNARY_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md) — [replay](audit_p5_h22_component19_p0_qphi_minus_one_ternary_compatibility.py)
- [`q*phi=-1`, `phi^2=1` crossings](P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_PHI_ENDPOINTS_VERIFICATION.md) — [replay](audit_p5_h22_component19_p0_qphi_minus_one_phi_endpoints.py)
- [`q*phi=-1` infinity](P5_H22_COMPONENT19_P0_QPHIM1_INFINITY_NO_IMPORT_VERIFICATION.md) — [replay](audit_p5_h22_component19_p0_qphim1_infinity_no_import.py)
- [`q=+/-1` endpoints](P5_H22_COMPONENT19_P0_Q_ENDPOINTS_NO_IMPORT_VERIFICATION.md) — [replay](audit_p5_h22_component19_p0_q_endpoints_no_import.py)
- [`phi=+/-1` endpoints](P5_H22_COMPONENT19_P0_PHI_ENDPOINTS_NO_IMPORT_VERIFICATION.md) — [replay](audit_p5_h22_component19_p0_phi_endpoints_no_import.py)

All eight live replays exit successfully.  No candidate or proof-B artifact is
used by the aggregate verifier.

## Exact residual boundary

The following loci are deliberately outside (1), not hidden gaps in it:

- `q=phi`: `T1111=4*(q-phi)=0`, so the ordinary restriction is zero.
  Projectivized normal and valuative directions are not promoted from this
  theorem.
- `q=0` or `phi=0`: at least one `P4` pair has rank below three.  These are
  lower-pair boundary problems, not all-pair-open points.
- parameter-chart infinity and other projectivized or valuative base
  directions remain outside this finite ordinary parameter theorem.

Replay the aggregate with

```powershell
uv run --with sympy python audit_p5_h22_component19_p0_finite_ordinary_aggregate.py
```
