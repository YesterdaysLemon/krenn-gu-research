# Independent verification of the weighted-`H22` obstruction on component twenty's intrinsic wall

```yaml
role: verifier
date_utc: 2026-08-01T13:32:22Z
git_commit: 3b23ef9e7803dbf9f3e89684971f8707f2d41d7f
claim_label: VERIFIED
scope: generic weighted H22 fibre on q=p+1 over Q(p), excluding p=0,-1,-1/2 and component-parameter infinity
inputs:
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION_CANDIDATE.md: 62abdc4004a01cc1045ae4ecaf5fe282913b8d817d1f870333653db1e82cf772
  derive_p5_h22_common_active_binary_triangle_intrinsic_boundary_obstruction_candidate.py: e9a1b88b8eb32dd0df70ba46129f78eb4025a5691620e6bcac468e0d18144b78
  p5_h22_common_active_binary_triangle_intrinsic_boundary_certificate.json: 014fe21451972c9712c0021fcc8d33619784a2016b65aa0a5b94ef7de13da0df
  P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION.md: ddd3dd8a441db26e6a0fa238842c56ed369133151944a203acc66e3d4bd4ad51
  verify_p5_h31_common_active_binary_triangle_intrinsic_boundary_obstruction.py: b7c580105e0ebfd12a21e5aed28b9a96039aabf52adfd0800caa319cc0324b63
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md: 49149b81ad2a50982d69f03d6e391808ced2beaddff0115f0c86039dd361c823
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md: 52168b35b43c40c483919c8fa1dd37e7c147cae5f331320d8656bf6a1ed309a9
method: independent replacement-basis reconstruction, subset-DP permanent expansion, H31 dependency replay, and eight bounded exact characteristic-zero finite/infinity projections
command: uv run --with sympy python audit_p5_h22_common_active_binary_triangle_intrinsic_boundary_obstruction_candidate.py
outputs:
  audit_p5_h22_common_active_binary_triangle_intrinsic_boundary_obstruction_candidate.py: fb1aa7e1f469a935c86e6d083df8881d3aca5ccde9497ee1961a858abd8a1f9f
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION_VERIFICATION.md: hash reported by replay
limitations: generic point of q=p+1 only; p=0,-1,-1/2, component-parameter infinity, mixed source-torus/projective limits, and unrelated special fibres remain open; generic Q(p,q) and p+q wall theorems were not used; no P4 exhaustiveness, arbitrary-order reduction, prize graph, or global Krenn-Gu claim
```

## Verdict

**VERIFIED:** over `Q(p)`, after imposing `q=p+1`, the weighted-`H22`
fibre is empty on the open

```text
p(p+1)(2p+1) != 0.
```

The verifier did not import the discovery script or its certificate and did
not specialize the collapsed generic component basis.  It reconstructed the
intrinsic wall basis, the permanent coefficients, and every elimination
system independently.  The construction artifacts were compared only after
those calculations passed.

## Direct replacement-basis audit

Starting from the two actual rows of `U0`, the audit rebuilt

```text
alpha0=-A+B,
beta0 =p(p+1)/(2p+1)e-(2p+1)A+C,

alpha1=e,          beta1=(p+1)A+pB+C,
alpha2=e,          beta2=pA+(p+1)B+C,
alpha3=e+A+B,      beta3=e.
```

Every pair has rank two over `Q(p)`.  A fresh subset-DP permanent expansion,
before and after the arbitrary affine markings
`beta_i -> beta_i+h_i alpha_i`, has pure support

```text
T1111=-2p(p+1)
```

and no other pure coefficient.  The exact denominator audit finds only `1`
and `2p+1`.  Thus `p=0,-1` are excluded because the surviving pure
coefficient vanishes, while `p=-1/2` is excluded because this replacement
basis is undefined.  No assertion is made at component-parameter infinity.

The primary intrinsic-wall `H31` verifier was also replayed from its frozen
hash and returned `pass`.

## Individual binary projections

The verifier rebuilt the common extension vector, all fourteen mixed rows,
and both diagonal rows for each contraction.  It covered the homogeneous
weight line by the finite chart `[lambda:1]`, including `lambda=0`, and a
separate direct endpoint `[1:0]` calculation.  For each of `D01` and `D23`,
it imposed

```text
M z=0,    A z=1,    u(B z)=1.
```

Eliminating the extension coordinates and inverse variable gave the exact
projected ideal `<1>` in all four cases:

```text
finite D01, finite D23, infinity D01, infinity D23.
```

These are characteristic-zero calculations over the relevant rational
function coefficient field.  No finite-field result is used as proof.

## Complete shared-`H22` orientation audit

As an independent check of the shared incidence, the verifier used one
marking, one homogeneous weight, and one extension vector for both
contractions.  In each orientation it imposed both mixed systems, normalized
one all-alpha diagonal, and explicitly inverted both all-beta diagonals:

```text
M01 z=M23 z=0,    A_direction z=1,
u(B_direction z)=1,    v(B_other z)=1.
```

All coefficients were first checked to be homogeneous linear forms in the
extension coordinates.  Therefore the normalization loses no projective
point on its selected orientation, while the inverse equations perform the
required open-set saturation exactly.  The two choices of normalized
all-alpha diagonal cover every possible `H22` orientation.  Their projected
ideals are `<1>` on both the finite and infinity weight charts, giving four
more exact unit certificates.

There is consequently no normalization, saturation, orientation, or
homogeneous-weight endpoint gap in the stated generic-wall conclusion.

## Boundary discipline

- The intersection with the separate wall `p+q=0` is `p=-1/2`, already
  excluded by `2p+1=0`; that wall theorem was not used.
- The generic `Q(p,q)` weighted-`H22` candidate was not used as a theorem or
  specialized onto this wall.
- The points `p=0,-1,-1/2`, component-parameter infinity, mixed
  source-torus/projective limits, and other special fibres remain open here.
- This verification does not establish component exhaustiveness, the open
  `P4` cells, an arbitrary-order local-to-global reduction, a prize graph, or
  the global Krenn--Gu conjecture.

## Replay

```text
uv run --with sympy python audit_p5_h22_common_active_binary_triangle_intrinsic_boundary_obstruction_candidate.py
```

Each Singular subprocess is file-backed and bounded by a 120-second timeout.
On timeout, the verifier terminates the complete spawned process tree before
reporting failure.
