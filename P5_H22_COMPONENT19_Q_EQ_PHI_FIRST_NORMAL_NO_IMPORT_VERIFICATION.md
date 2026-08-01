# Component-19 `q=phi` first-normal weighted-`H22` verification

```yaml
role: verifier
date_utc: 2026-08-01T17:34:28Z
git_commit: ac0853455c978628c6f685e826f78275591d639a
claim_label: VERIFIED
scope: component-19 Z0={p=0,q=phi}, phi!=0; smooth normal cone, projectivized first-normal P1, and shared weighted-H22 incidence on every first-normal direction
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: fresh squarefree permanents, Jacobian and regular-sequence normal geometry, two normalized ray charts, and 16 exact characteristic-zero saturated eliminations
command: uv run --with sympy python audit_p5_h22_component19_q_eq_phi_first_normal_no_import.py
outputs:
  audit_p5_h22_component19_q_eq_phi_first_normal_no_import.py: hash emitted by replay
  P5_H22_COMPONENT19_Q_EQ_PHI_FIRST_NORMAL_NO_IMPORT_VERIFICATION.md: hash emitted by replay
limitations: associated-graded first-normal result only; formal arcs, higher tangent coefficients, valuative closure, arbitrary-order local-to-global reduction, and the global conjecture remain unresolved
```

## Verdict

**VERIFIED first-normal empty.**  In the component-19 parameter chart with
`phi!=0`, the zero-restriction locus

```text
Z0={p=0,q=phi}
```

is smooth of codimension two.  Its normal cone is a rank-two vector bundle,
and its fibrewise projectivization is `P1`.  On every point of this
projectivized first-normal bundle, the necessary shared weighted-`H22`
incidence is empty for every finite weight and for weight infinity.

This is not a theorem about all formal arcs through `Z0`.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

The verifier reads no construction or proof-B artifact.  It reconstructs the
normal form and every contraction directly from
`P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md`.

## Normal-cone geometry

In the smooth chart

```text
X=Spec Q[p,q,phi,phi^(-1)],
```

fresh squarefree multiplication gives exactly

```text
T_0111=4p,
T_1111=4(q-phi),
```

with every other coefficient zero.  Thus the zero ideal is

```text
I_Z0=(p,q-phi).
```

Its Jacobian in `(p,q,phi)` is

```text
[1  0   0]
[0  1  -1],
```

whose `(p,q)` minor is the unit `1`.  Hence `Z0` is a smooth codimension-two
complete intersection.  The two displayed generators form a regular sequence,
so

```text
C_Z0 X = Spec_Z0 Sym(I_Z0/I_Z0^2)
```

is a rank-two vector bundle.  Writing its normal coordinates as `(a,b)`, its
projectivization is the `P1`-bundle with standard charts

```text
[a:b]=[n:1]  and  [a:b]=[1:n].
```

Indeed, along

```text
p=a*t,  q=phi+b*t,
```

division by the first power of `t` gives exactly

```text
T_first,0111=4a,
T_first,1111=4b.
```

The charts agree on their overlap by `n_a*n_b=1`.

## Exact ray normalization

Put

```text
alpha0=Abar,
beta0=Bbar+phi*B
```

at `Z0`; modes one through three retain the component normal form.  The two
normal charts are obtained before specializing the transverse parameter:

- On `[a:b]=[n:1]`, use `p=n*s`, `q=phi+s` and
  `beta0'=beta0+n*alpha0`.  After dividing the tensor by `s` and setting
  `s=0`, its first-normal tensor is all-beta in the primed rows.
- On `[a:b]=[1:n]`, use `p=s`, `q=phi+n*s` and
  `alpha0'=beta0`, `beta0'=alpha0+n*beta0`.  The first-normal tensor is again
  all-beta.

The two mode-zero changes have determinants `1` and `-1`.  Thus they are
regular row-basis changes, not divisions by a normal slope, and include the
two projective endpoints.

## Complete necessary weighted-`H22` incidence audit

For each normalized first-normal chart, the verifier independently adjoins
eight fifth-coordinate extension variables `(x0,...,x3,y0,...,y3)` and all
four affine Borel markings

```text
beta_i -> beta_i+h_i*alpha_i.
```

It builds both contractions `D01` and `D23`.  For finite shared weight
`lambda`, their target-coordinate maps are

```text
D01: (z0,z1,z2,z3,z4) -> (lambda*z0+z1,z2,z3,z4),
D23: (z0,z1,z2,z3,z4) -> (z0,z1,lambda*z2+z3,z4).
```

The separate weight-at-infinity maps retain respectively `(z0,z2,z3,z4)`
and `(z0,z1,z2,z4)`.

For both contractions, all fourteen mixed binary coefficients are set to
zero.  Write the four pure diagonals as `A01,B01,A23,B23`.  Every genuine
shared `H22` incidence lies in one of the four opens

```text
(A01,B01,A23),
(A01,B01,B23),
(A23,B23,A01),
(A23,B23,B01),
```

because one contraction must be binary and the other must have a nonzero
pure side.  All tensor coefficients are homogeneous linear forms in the
eight extension variables.  Therefore, on each open, the first selected
diagonal may be normalized to `1`, while two auxiliary inverse variables
enforce nonvanishing of the other selected diagonals.

The replay performs

```text
2 normal charts x 2 weight charts x 4 diagonal opens = 16 cases.
```

In every case it eliminates the eight extension variables and three inverse
variables while retaining `h0,h1,h2,h3`, the normal slope `n`, `phi`, and,
on the finite chart, `lambda`.  The computation is over `Q[phi]` with only
the actual component condition `phi!=0` saturated.  Every projected
Groebner basis is exactly

```text
(1).
```

Consequently there is no hidden normal slope, marking, finite weight, weight
infinity, or nonzero special value of `phi`.  In particular, `phi=+1` and
`phi=-1` are included rather than inferred from a generic coefficient-field
calculation.  Since the necessary shared binary incidence is already empty,
there is no survivor requiring a later target-local compatibility rank test.

## Discarded false start

An exploratory run initially kept the transverse ray parameter `s` in the
coefficient field.  That made `s` invertible and audited punctured exact rays,
not the exceptional fibre of the normal cone.  Those outputs were discarded.
The certified 16 cases first perform the regular ray-basis normalization and
then specialize `s=0`; no result from the invertible-`s` run is used.

## Exact formal-arc boundary

For an arbitrary non-base formal arc, the exact tensor coordinates imply
that, after factoring the minimum valuation of `p` and `q-phi`, there is a
well-defined leading normal direction `[a_m:b_m]`.  This observation alone
does **not** reduce the full valuative problem to the normal cone.

The limiting four-plane extensions and Borel markings can depend on higher
tangent coefficients of the arc.  Their normalizations can also involve
`t`-dependent rescalings or poles before a limit is taken.  The present
associated-graded equations retain only the first-normal rows, so they do not
prove that those higher data are irrelevant.  No Rees-saturation identity,
proper compactification argument, or valuative lifting theorem is supplied.

Therefore:

```text
projectivized first-normal weighted-H22 incidence: VERIFIED EMPTY
all higher-order formal arcs through Z0: UNKNOWN
arbitrary-order local-to-global reduction: UNKNOWN
global Krenn--Gu conjecture: UNRESOLVED
```
