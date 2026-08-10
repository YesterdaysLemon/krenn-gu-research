# Independent verification of the embedded-`P_3` projective `H22` closure claim

```yaml
role: verifier
date_utc: 2026-08-01T11:06:36Z
git_commit: aea77ca10fd7534f964317c0aeeab035d3e76627
claim_label: REFUTED
scope: claimed full projective weighted-H22 closure and its symmetry/dependency cover
inputs:
  P5_H22_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md: ce01df919779568b704eb7373917945885169719bd7be9eeb2818f21b931dcfb
  verify_p5_h22_embedded_p3_component_projective_closure.py: c43dbea01e02c593b0528f12a9adcb8cf6bda3e7bc4360500102ddde2046906c
  P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md: dfc2ca99ac668605b54a08b2a4dfb48f74abba97ae2ecc405121d21b8e7f3f4a
  P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md: baf5531740cfd77207f31cf8e1de2b5b838701cbcae5ec778667e6e7f712d15e
  P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md: 7ae8c19e5a43ac7af2cac35892af59130555ab509495d5280745aad114eed056
method: no-primary-import permanent reconstruction, exact support and matching transport, and an invariant free-plane counterexample
command: uv run --with sympy python claims/p5/h22/embedded-p3/audit_p5_h22_embedded_p3_component_projective_closure_independent.py
outputs:
  audit_p5_h22_embedded_p3_component_projective_closure_independent.py: hash reported by replay
  P5_H22_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_VERIFICATION.md: hash reported by replay
limitations: REFUTED applies to the asserted full closure proof; no positive H22 lift is constructed and the uncovered strata remain UNKNOWN
```

## Verdict

**REFUTED as a full projective-closure proof; the underlying weighted-`H22`
target is UNKNOWN on the uncovered strata.**  The corrected source note now
states this boundary accurately.

The homogeneous normal-base calculation is correct, as are the support-one
zero restrictions.  The failure is that normal-base transport does not
normalize the independent free mode-zero plane.  A second, separate caveat is
that unrestricted normal-coordinate permutations do not automatically
preserve the `01|23` matching with its shared homogeneous weight.

## Reconstructed homogeneous normal base

For

```text
n1=(C,A,B),       n2=(C,-A,-B),       n3=(C,-A,B),
```

the displayed bases on `C!=0` independently give

```text
T100=2AC^2,       T101=-2BC^2,
```

with every other coefficient zero.  Those rows are not valid plane bases at
`C=0`, so the audit rebuilt each support mask from independent kernels of the
three normals.  For the seven `{0,1}` representatives the nonzero tensors are

```text
mask 1: {}                 mask 2: {}
mask 3: {T100= 2}          mask 4: {}
mask 5: {T101=-2}          mask 6: {T110=-2}
mask 7: {T100=2,T101=-2}.
```

Thus support-one masks `1,2,4` are correctly inadmissible, while all four
support-at-least-two masks have nonzero pure restriction.

## Exact free-plane counterexample to the dependency cover

Take the full-support normal point `[C:A:B]=[1:1:1]` and the four binary
planes, in `(alpha,beta)` order,

```text
U0=((0, 1,0,0),(1, 0,0,0)),
U1=((0,-1,1,0),(0,-1,0,1)),
U2=((0, 1,1,0),(0, 1,0,1)),
U3=((0, 1,1,0),(0,-1,0,1)).
```

Direct order-four permanent expansion has exactly

```text
T1100=2,          T1101=-2,
```

so the pure `P_4` restriction is nonzero and decomposable.  The only triple
of these planes lying in a source coordinate hyperplane is

```text
(U1,U2,U3) subset H0.
```

Consequently tensor-mode permutations cannot choose another embedded triple
to evade the following invariant.

The free plane is `U0=span(e0,e1)` and therefore contains the transverse
coordinate axis `e0`.  By contrast, all three cited normalized theorems use

```text
U0^norm=span((0,1,S,U),(1,0,1,T)).
```

Appending `e0` to these two rows, rows `012` and columns `012` have the fixed
determinant

```text
1.
```

Hence `U0^norm` never contains `e0`.  Coordinate permutations, coordinate
signs/scalings, and mode permutations preserve the property that the unique
free plane contains the coordinate axis transverse to the common
hyperplane.  The displayed valid pure point therefore cannot enter the
normalization used by any of the three dependencies.

This is not just an omitted parameter value in their notation.  In the
original free-plane chart

```text
span((1,0,R,T),(0,1,S,U)),
```

the normalized theorems set a nonzero transverse quotient coordinate to
one.  The counterexample has `(R,T)=(0,0)`, an invariant zero class under the
allowed monomial source group.

## Matching and homogeneous-weight caveat

The normal chart cover itself uses more source permutations than the
weighted signature permits without further proof.  For mask 6,
`[C:A:B]=[0:1:1]`, every permutation that makes both `C'` and `B'` nonzero
changes the standard matching `01|23` to `02|13` or `03|12`.  Exhausting all
source permutations that fix the common coordinate and return the matching
to `01|23` also returns the zero old `C` coordinate to the new `C` slot.
Thus no such transport simultaneously stays in `C'B'!=0`.

There is an orientation issue even for mask 3.  Its required chart swap
interchanges source coordinates 2 and 3, sending the shared homogeneous
signature

```text
(lambda*x0+mu*x1, lambda*x2+mu*x3)
```

to

```text
(lambda*x0+mu*x1, mu*x2+lambda*x3).
```

When `lambda*mu!=0`, a weight-dependent diagonal source scaling can rebalance
this pair.  At either projective endpoint, nonzero diagonal scalings cannot
move the zero coefficient between endpoints.  The target primary only checks
the orbit of unordered matchings; it never transports the weights.  The three
cited theorems use the affine chart `[lambda:mu]=[r:1]` and contain no direct
infinity calculation.

If the two merge directions were instead assigned independent weights, this
orientation issue would disappear, but the cited theorems would then cover
only their one-parameter diagonal specialization.  Either interpretation
requires more than the primary supplies.

## What the three normalized theorems do cover

All three original exact scripts replay successfully.  On their actual
normalized finite-slope chart, the mode-zero projected rows are

```text
a=(1,S,U),         b=(r,1,T).
```

Their cross product is

```text
(ST-U, Ur-T, 1-Sr).
```

Thus the chart partitions exactly into:

1. rank two with the nine-factor discriminant nonzero, treated by the
   generic theorem;
2. rank two with the discriminant zero, treated by the rank-two boundary
   theorem;
3. rank one, equivalently `rS=1,T=rU`, treated by the collapse theorem.

So the dependency union is coherent on

```text
U0^norm=span((0,1,S,U),(1,0,1,T)),   [lambda:mu]=[r:1].
```

It is the promotion from that chart to the full projective component that
fails.  The rank-one verifier itself reports
`normalization_projective_boundary_closed=false`, consistent with this
verdict.

## Boundaries retained

- No finite-field calculation is used as proof.
- No positive weighted-`H22` lift has been found on the counterexample.
- The counterexample refutes the asserted dependency cover, not the possible
  truth of the final obstruction.
- The free-plane axis stratum, mask-6 matching transport, homogeneous slope
  endpoint, arbitrary-order reduction, and global Krenn--Gu conjecture remain
  unresolved here.

Replay:

```text
uv run --with sympy python \
  claims/p5/h22/embedded-p3/audit_p5_h22_embedded_p3_component_projective_closure_independent.py
```
