# Component-19 `Z0` Laurent-field weighted-`H22` verification

```yaml
role: verifier
date_utc: 2026-08-01T18:13:19Z
git_commit: a3d47ed7d9debeaa9ae55c225c71e39ddd6d0116
claim_label: VERIFIED
scope: all characteristic-zero formal arcs centered on component-19 Z0={p=0,q=phi}, phi!=0, with nonzero all-pair-open generic point in the displayed affine chart
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  audit_p5_h22_component19_p0_finite_ordinary_aggregate.py: 65cafa89b709f0466d7fd51fc2555f60cec9246b6f68034ffa4ed94dc41180f7
  P5_H22_COMPONENT19_P0_FINITE_ORDINARY_AGGREGATE_VERIFICATION.md: ebb4bc46e06b99d4d21e0dff96a35fb071d48dfeceeb926cb4b2643fdeeddbc3
method: Laurent-field partition, live p0 replay, 40 parameter-aware saturated projections, reverse-branch compatibility minors, and exact 1/s escape algebra
command: uv run --with sympy python audit_p5_h22_component19_z0_laurent_field_no_import.py
outputs:
  audit_p5_h22_component19_z0_laurent_field_no_import.py: hash emitted by replay
  P5_H22_COMPONENT19_Z0_LAURENT_FIELD_NO_IMPORT_VERIFICATION.md: hash emitted by replay
limitations: displayed component-19 affine chart only; identically zero arc, phi=0, lower-pair/projective chart boundaries, other components, arbitrary-order local-to-global reduction, and the global conjecture excluded
```

## Verdict

**VERIFIED empty for all formal arcs in scope.**  Let `R` be a
characteristic-zero DVR with fraction field `F`, and let

```text
(p,q,phi) in R^3,
r=q-phi,
p,r in maximal_ideal(R),
phi in R^*.
```

Assume `(p,r)!=(0,0)` in `F`, so the generic restriction is nonzero, and
assume its generic point remains in the all-pair-open part of the displayed
component-19 chart.  Then the generic point has no genuine target-compatible
weighted-`H22` `P5` lift over `F`.

This is an arbitrary-order valuative statement inside this one affine
component chart.  It is proved by exhausting field-valued points directly,
not by promoting the first-normal calculation through a properness claim.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

No construction or proof-B artifact is read or imported.

## Exhaustive Laurent-field partition

Because the arc is centered on `Z0`, both `phi` and `q=phi+r` are units.
Over the field `F`, zero versus nonzero is an exhaustive dichotomy, giving:

| Field case | Exact result |
|---|---|
| `p=0`, `r!=0` | The live ordinary-`p=0` aggregate covers `q*phi*r!=0` and both weight charts; empty. |
| `p!=0`, `r=0`, `phi^2!=1` | All necessary-incidence opens are empty. |
| `p!=0`, `r=0`, `phi^2=1` | The sole reverse-weight incidence branch is compatibility-obstructed. |
| `p*r!=0`, `phi^2=1` | Sixteen endpoint weight/orientation cases are unit ideals. |
| `p*r!=0`, `phi^2!=1`, `q*phi!=1` | Eight parameter-aware weight/orientation cases are unit ideals. |
| `p*r!=0`, `phi^2!=1`, `q*phi=1` | The sole reverse-weight incidence branch is compatibility-obstructed. |

The parameter-aware replay retains `p,q,phi` rather than putting them in a
coefficient field.  It saturates exactly by the stated open products.  It
therefore detects the hidden divisor `q*phi=1` that a generic
`Q(p,q,phi)` computation would silently invert.

The 40 exact projected ideals comprise:

```text
q=phi:                         8 cases
q*phi=1:                       8 cases
phi=+1 with p*r*q!=0:          8 cases
phi=-1 with p*r*q!=0:          8 cases
generic away from q*phi=1:     8 cases
```

Every ideal is `(1)` except one finite orientation in each of the first two
rows.  Their exact projections are

```text
q=phi:
  (lambda+1,h3,h2,h1,h0,phi^2-1),

q*phi=1:
  (lambda+1,h3,h2,h1,h0).
```

Thus these are one reverse branch, with the `q=phi` occurrence confined to
`phi^2=1`.

## Reverse branch compatibility obstruction

On `q=1/phi`, `lambda=-1`, and `h0=h1=h2=h3=0`, the combined 28-by-8 mixed
matrix has rank five on `p*phi!=0`; a fixed rank witness is

```text
-1024*p*phi^3.
```

Its kernel has the frame

```text
vX=(0,1/phi,1,0,0,0,0,0),
vY=(0,0,0,0,1,0,0,0),
vZ=(0,0,0,0,0,0,0,1).
```

For extension `X*vX+Y*vY+Z*vZ`, the four diagonals are

```text
(A01,B01,A23,B23)=(-4pX,0,4X/phi,-4(phi*Y+Z)).
```

Hence the genuine open is `X*(phi*Y+Z)*p*phi!=0`.  Put

```text
D=phi*Y-Z,
K=phi*Y+Z.
```

Two individual target-local four-minors are, up to displayed units,

```text
-64*X*p*D*(X*(phi^2-1)+phi*K)/phi,
 64*X*p*D*(X*(phi^2-1)-phi*K)/phi^3.
```

If `D!=0`, both cannot vanish: subtracting their final linear factors would
force `K=0`, contrary to the genuine open.  If `D=0`, then `Z=phi*Y` and
`K=2phi*Y`, so `Y!=0`; the full shared mode-one 8-by-5 stack has the fixed
five-minor

```text
-512*X^2*Y^2*p^2*phi,
```

which is nonzero.  The reverse branch therefore never satisfies the common
three-column factorization.  The argument remains valid at `phi=+1` and
`phi=-1`, closing the `r=0` endpoint occurrence as well.

## The exact `1/s` escape is real but not a full lift

The first-normal genuine-incidence morphism is not proper.  On the exact ray

```text
p=0,
q=phi+s,
lambda=1,
h=(0,0,0,0),
```

the shared mixed equations have the extension

```text
(x0,x1,x2,x3,y0,y1,y2,y3)
  =(0,-1/s,phi/s,0,1,1,0,0).
```

Its generic diagonals are

```text
(A01,B01,A23,B23)=(0,4s,-4phi/s,4),
valuation=(infinity,1,-1,0).
```

Thus `(A23,B23,B01)` is genuinely nonzero for `s!=0`.  After the common
projective scaling by `s`, the extension tends to the nonzero point

```text
(0,-1,phi,0,0,0,0,0),
```

while the scaled diagonals are

```text
(0,4s^2,-4phi,4s),
valuation=(infinity,2,0,1).
```

The special point retains only `A23`; `B23` and `B01` must be restored at
orders one and two.  This is a genuine derivative escape from the 16 strict
first-normal diagonal opens, not an invalid zero projective point.

It is nevertheless not a full weighted-`H22` arc.  A fixed target-local
four-minor equals

```text
-64*((phi+s)^2-1)*(phi*(phi+s)+1)/s,
```

which is nonzero in the punctured Laurent field.  This also agrees with the
independent complete ordinary-`p=0` aggregate.

## Projective charts and properness

The natural conceptual compactification uses:

- two charts for the projectivized normal direction `P1`;
- finite and infinity charts for the weight `P1`;
- two charts per factor of a marking compactification `(P1)^4`;
- three charts per factor of the lift compactification
  `Gr(2,U_i plus vertical line)=P2`, hence `(P2)^4` for four planes.

The four genuine diagonal opens have triples

```text
(A01,B01,A23), (A01,B01,B23),
(A23,B23,A01), (A23,B23,B01).
```

Their complement is the union of six maximal coordinate strata:

```text
A01=B01=0,  A23=B23=0,
A01=A23=0,  A01=B23=0,
B01=A23=0,  B01=B23=0.
```

The ambient projective product is proper over the blown-up base, but deleting
these diagonal strata makes the genuine binary incidence only locally
closed.  The `1/s` arc above explicitly violates its valuative criterion.
Consequently the strict-normal unit ideals alone cannot prove the formal-arc
claim.

After target compatibility is imposed, the direct field partition proves
that the full `H22` incidence in this formal neighborhood is empty.  Its
morphism is therefore vacuously proper in the stated scope, but emptiness—not
compactification—is the proof.

## Fitting and pole checklist

The compactified coefficient image is not a uniform vector bundle.  Exact
rank witnesses identify derivative-sensitive strata:

```text
D01: lambda=+/-1 or phi=+/-1,
D23 finite: lambda=+/-1 or (phi+1)*lambda=+/-(phi-1),
D23 infinity: phi=-1.
```

Marking-pole divisors and vertical-plane lift divisors also occur in special
fibres.  These are genuine warnings for any future properness proof.  They do
not leave an unresolved formal arc here because a pole is still an element of
the generic Laurent field: the parameter-aware finite-weight equations retain
arbitrary `lambda,h_i` in `F`, the infinity weight is separate, and the field
partition rules out the full compatible lift before specialization.

## Boundary

This theorem does not include the identically zero arc, `phi=0`, lower-pair
or projective Grassmann-chart boundaries, any other `P4` component, or the
arbitrary-order local-to-global reduction.  It does not resolve the global
Krenn--Gu conjecture.
