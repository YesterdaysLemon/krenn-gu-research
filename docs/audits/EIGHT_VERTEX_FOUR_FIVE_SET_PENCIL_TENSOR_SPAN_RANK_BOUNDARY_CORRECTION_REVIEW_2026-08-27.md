# Hostile review: four-five-set pencil tensor-span-rank correction

## Verdict

**The codimension-nine/codimension-ten pencil promotion is withdrawn.**

The rejected package's selector quantifiers, exact equality partitions, and
projective-root properness setup were plausible, but its shared-edge rank
identity was false.  Four distinct decomposable evaluation tensors need not be
linearly independent.  The primary verifier and its audit both counted
partition-block pairs rather than computing tensor span rank.

The replacement package records an exact feasible characteristic-zero boundary:

```text
common span ranks:          (2,3,3,4,4,4),
partition-pair cardinality: (4,4,4,4,4,4),
projective incidence image: dimension 168 = 176-8,
full affine image:          dimension 244 = 252-8.
```

An exact Jacobian check gives projective incidence rank `36` and root-only rank
`28`, so the codimension-eight image is locally projected rather than merely
an oversized parameter count.  A separate finite-field implementation
reproduces the span and Jacobian ranks modulo `1,000,003`.

## Load-bearing counterboundary

Use four charts over a common `K_4`, all with selector `f=(0,0,1)`.  At common
vertex `0`, all roots are `e_2`; at vertex `1`, use four distinct lines
`[1:t+1:0]`; at vertices `2,3`, use the explicit distinct vectors in the
correction theorem.  The exact partitions are
`0123, 0|1|2|3, 0|1|2|3, 0|1|2|3`.  The selector is nonconstant, every
coordinate subspace is nonempty, and the root stratum has dimension `28`.

On edge `01`, the four evaluation tensors are
`e_2 tensor (1,t+1,0)`, which span dimension `2` despite four distinct
partition pairs.  This directly invalidates the cardinality-as-rank step.

The affine zero-block discussion does not rescue the route: the counterboundary
works with nonzero coefficient blocks, and the same linear-kernel count applies
in the full affine space.  Proper projection from projective root bases remains
valid as a geometric setup, but it cannot repair the wrong source dimension.

The common-quadratic rank-drop fixture remains a valid nonempty control for the
original incidence conditions.  It is not a witness and does not establish a
corrected `B_all` codimension bound.

## Required follow-up

Any future four-chart theorem must replace the surrogate `q_ij` by

```text
r_ij = dim span{x_i^(t) tensor x_j^(t) : t in N}
```

and account for rank-degeneracy strata and their projection dimensions.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## Replay

```powershell
python claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_tensor_span_rank_boundary_correction.py
python -I claims/arbitrary-order/audit_eight_vertex_four_five_set_pencil_tensor_span_rank_boundary_correction.py
python -m py_compile claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_tensor_span_rank_boundary_correction.py claims/arbitrary-order/audit_eight_vertex_four_five_set_pencil_tensor_span_rank_boundary_correction.py
```
