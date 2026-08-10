# Independent verification of the component-nineteen generic weighted-`H22` obstruction

```yaml
role: verifier
date_utc: 2026-08-01T12:58:10Z
git_commit: bb7fb22c44b8348d993b6ed655ac007120dc0099
claim_label: VERIFIED
scope: generic weighted H22 fibre of component nineteen, the common-kernel vertical triangle
inputs:
  P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md: 387c0f57e67574bbdcbb80fa412e5144d2d34acd60d29fe20fcf6e59deae9eee
  derive_p5_h22_common_kernel_vertical_triangle_component_generic_obstruction_candidate.py: 4fb70a08306f464b390ea71b1c83764f3cbe8708b5b9670c64925a740b7d6bac
  p5_h22_common_kernel_vertical_triangle_component_generic_certificate.json: 9b50361314811a137f4742649d56dbb979ef5ace1561e343159c65af090e6d20
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  verify_p4_common_kernel_vertical_triangle_component.py: f62de41d4005c46682739ca572e00bbc8214c6065994e38f158a6f84c014cc1c
  P5_H31_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md: 3b49c47626131fa10729961bc700d46b518a102799504c3796fb0a5b932c5832
  verify_p5_h31_common_kernel_vertical_triangle_component_generic_obstruction.py: e96c3470204cc97998b00dcd74b6d170f1fe4b3e620c4596734c0b31950829f5
  P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md: da64a3ee55d5dfa361a70cb771196f76f93d13b3d61df358442a22e1e72de1a8
method: fresh subset-DP permanents, direct finite/infinity homogeneous contractions, exact characteristic-zero Singular projection ideals, complete symbolic shared kernel, and a fixed transverse rank witness
command: uv run --with sympy python audit_p5_h22_common_kernel_vertical_triangle_component_generic_obstruction_candidate.py
outputs:
  audit_p5_h22_common_kernel_vertical_triangle_component_generic_obstruction_candidate.py: da0b1a6e46902950e4ba5b2a8040af569cf351ecde0c7a08cdca8f7055c66860
limitations: generic function-field theorem only; no special-parameter or projective component-boundary fibres, P4 component exhaustiveness, arbitrary-order local-to-global reduction, prize graph, or global Krenn-Gu conclusion
```

## Verdict

**VERIFIED.**  A fresh verifier reconstructs the component-normal-form rows,
both weighted contractions, both projective weight charts, all six projected
ideals, the complete common extension kernel, every required diagonal, and the
fixed transverse determinant without importing the construction script.  The
generic marked weighted-`H22` fibre of component nineteen is empty over
`Q(p,q,phi)`.

This is strictly a generic-point theorem.  In particular, special parameter
divisors—including those where a displayed generic rank witness has a factor
`phi-1` or `phi+1`—and every projective component-boundary fibre require their
own analysis.

## Normal form and intrinsic pure marking

Starting from the independently replayed `P4` component theorem, the verifier
rebuilds

```text
alpha0=(q-phi)(Abar+pB)-p(Bbar+qB),  beta0=Abar+pB,
alpha1=B,                             beta1=A,
alpha2=Bbar,                          beta2=A,
alpha3=Abar,                          beta3=B+phi Bbar.
```

The mode-zero basis change has determinant `p`, a unit in the function field.
A subset-dynamic-program permanent calculation, structurally independent of
the candidate's permutation enumeration, gives

```text
T_w=0 for w!=1111,       T_1111=4p
```

both before and after arbitrary affine markings
`beta_i -> beta_i+h_i alpha_i`.  The exact component replay returns dimension
five and generic pair profile `(4,4,4,3,3,3)`.  The companion exact `H31`
replay also passes, while retaining its explicit boundary that it did not
settle weighted `H22`.

## Complete projective binary projections

The verifier constructs the finite `[lambda:1]` contractions directly and
uses separate direct maps at `[1:0]`.  Over `Q(p,q,phi)`, bidirectional
standard-basis reduction gives

```text
D01 binary, finite:    <1>
D01 binary, infinity:  <1>

D23 binary, finite:
  <h3, (q-phi)h0+1, h1 h2 ((q+1)lambda+q-1)>

D23 binary, infinity:
  <h3, (q-phi)h0+1, h1 h2>.
```

Thus `D01` is not genuinely binary anywhere on the homogeneous weight line,
including `[0:1]` and `[1:0]`.  Any surviving `H22` configuration must use a
nonzero pure `D01` contraction and a genuinely binary `D23` contraction with
one shared marking, weight, and extension.

Imposing those shared requirements before eliminating gives exactly

```text
finite:   <lambda-1, h3, h1, (q-phi)h0+1>,
infinity: <1>.
```

Both ideal comparisons are bidirectional; no set-theoretic or radical-only
substitution is used.  Hence there is no infinity branch, and the complete
finite marking branch is

```text
lambda=1,       h=(-1/(q-phi),0,t,0).
```

## Complete shared extension and transverse obstruction

On this branch, the combined `29 x 8` unwanted-coefficient matrix has exact
rank six.  A fixed rank witness found by exact row reduction is

```text
rows    (2,3,5,11,13,16),
columns (0,1,2,3,6,7),
determinant -4096 p^4 phi (q-phi)(phi-1)(phi+1).
```

Its complete two-dimensional kernel is

```text
vC=(0,-1/p,phi/p,0; 1,0,0,0),
vD=(0,0,0,0;       0,1,0,0).
```

For `z=C vC+D vD`, direct reconstruction gives

```text
B01=4(pD-phi t C),
A23=-4 phi(q-phi)C/p,
B23=4C.
```

Therefore the common genuine open is exactly

```text
C p phi(q-phi)(pD-phi t C) != 0.
```

The mode-three `D01` one-marked matrix has fixed rows `1257` determinant

```text
-64 C p (pD-phi t C)^2.
```

Every factor is nonzero on the common genuine open.  The one-marked map has
rank four, contradicting the rank-at-most-three target-local factorization
required by a ternary weighted-`H22` lift.  This excludes the complete
surviving branch.

## The low-rank false lead is not shared

The verifier independently reproduces the tempting point

```text
h=(-1/(q-phi),0,0,0),       [rho:sigma]=[1-phi:phi+1].
```

A separate `D23` extension has one-marked ranks `(3,3,3,3)`, and a separate
pure `D01` extension has ranks `(2,3,3,3)`.  They cannot form an `H22` pair:

- their extension vectors are not even projectively proportional; the
  two-coordinate proportionality minor on rows `(1,5)` is exactly `1`;
- on the finite chart their weight satisfies
  `lambda-1=-2phi/(phi+1)`, whereas the exact shared ideal requires
  `lambda=1`.  The only formal escape `phi=0` is outside the generic open,
  and `phi=-1` lies on the separately unit infinity chart.

This directly verifies why direction-by-direction low-rank testing was a
false lead.

## Evidence boundaries and replay

The proof uses exact characteristic-zero arithmetic.  No finite-field sample,
parameter grid, broad brute force, timeout, or solver exit code is treated as
evidence.  It does not close special/projective fibres, prove pure-`P4`
component exhaustiveness, establish the local-to-global reduction, construct a
prize graph, or resolve the global Krenn–Gu conjecture.

```text
uv run --with sympy python claims/p5/h22/common-kernel-vertical-triangle-component-generic/audit_p5_h22_common_kernel_vertical_triangle_component_generic_obstruction_candidate.py
uv run --with ruff ruff check audit_p5_h22_common_kernel_vertical_triangle_component_generic_obstruction_candidate.py
python -m py_compile audit_p5_h22_common_kernel_vertical_triangle_component_generic_obstruction_candidate.py
python -m json.tool p5_h22_common_kernel_vertical_triangle_component_generic_certificate.json
git diff --check
```

The independent verifier emits current hashes for the report, itself, the
three candidate artifacts, and every theorem dependency.
