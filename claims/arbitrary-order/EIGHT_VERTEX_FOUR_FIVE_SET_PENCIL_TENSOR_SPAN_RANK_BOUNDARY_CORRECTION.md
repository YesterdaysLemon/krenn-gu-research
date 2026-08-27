# Eight-vertex four-five-set pencil tensor-span-rank boundary correction

## Status

**Exact characteristic-zero route correction; not a Krenn--Gu counterexample.**

The proposed four-chart codimension-nine/codimension-ten argument is not a
valid incidence proof.  It replaces the linear rank of the shared-edge
evaluation tensors by the number of distinct pairs of equality-partition
blocks.  Pairwise nonproportional decomposable tensors need not be linearly
independent once four charts are present.  An exact feasible stratum below
has the advertised selector and exact-root-partition data but has affine
codimension only eight in the resulting incidence image.

This is a counterboundary to the cardinality-as-rank step, not an exact
counterexample to the original Krenn--Gu conjecture.  It neither supplies a
witness nor proves that the corrected four-chart envelope has codimension
eight globally.  The global conjecture remains **UNRESOLVED**.

## 1. The feasible exact stratum

Let `A={0,1,2,3}` be the common `K_4`, let the four charts be indexed by
`t=0,1,2,3`, and let every chart use the same nonconstant selector

```text
f_t(0)=0,  f_t(1)=0,  f_t(2)=1.                         (1)
```

Thus the common vertex `0` has the selected coordinate subspace
`P(span(e_2))`, common vertex `1` has `P(span(e_0,e_1))`, and vertices `2,3`
have unrestricted `P^2` factors.  Take the exact common-root partitions

```text
pi_0 = {0123},
pi_1 = pi_2 = pi_3 = {0|1|2|3}.                        (2)
```

The first common root is fixed at `e_2`; the four vertex-`1` lines are
distinct in `P(span(e_0,e_1))`; and the vertex-`2` and vertex-`3` lines are
distinct generic points of `P^2`.  The four outer roots are unrestricted
`P^2` points.  Every selector is nonconstant and every coordinate factor is
nonempty.  The root stratum has dimension

```text
4*(0+1+2+2+2) = 28,                                  (3)
```

and its synchronization codimension is zero: at vertex `0` the repeated
zero-coordinate credit is `4*2-2=6`, cancelling `2*(4-1)=6`.

One exact integer root fixture used by the verifier is

```text
x_0^(t) = (0,0,1),
x_1^(t) = (1,t+1,0),
x_2^(t) = (1,2,1), (2,1,1), (3,4,1), (5,1,1),
x_3^(t) = (2,1,1), (1,3,1), (4,2,1), (3,5,1),
y_t     = (1,2,1), (2,3,1), (3,1,1), (4,2,1).        (4)
```

The entries in each displayed row are ordered by `t`; vectors are projective
and the `y_t` are the outer roots.

## 2. The rank defect

For a common edge `ij`, the coefficient equations are evaluation on
`x_i^(t) tensor x_j^(t)`.  The six exact span ranks at (4) are

```text
edge                 01  02  03  12  13  23
tensor-span rank       2   3   3   4   4   4.           (5)
```

The partition-pair cardinality used by the rejected route is `4` on every
one of these six edges.  The defect is already visible on edge `01`:

```text
e_2 tensor (1,t+1,0),  t=0,1,2,3,
```

are four distinct projective decomposable tensors but lie in a two-dimensional
span.  The actual common-edge rank sum is therefore `20`, rather than the
claimed `24`.  The sixteen outer-edge equations contribute rank `16`, so the
full twenty-two-block evaluation rank is `36`.

The resulting source dimensions are

```text
projective:  28 + (22*8 - 36)       = 168 = 176 - 8,
affine:     28 + (22*9 - 36) + 6*9  = 244 = 252 - 8. (6)
```

The affine count includes the six free `N--N` blocks and does not divide away
whole-zero blocks.  A generic coefficient choice in the indicated kernels
can be chosen with every displayed block nonzero.

## 3. Exact projection-dimension check

The primary verifier constructs coefficient matrices in the exact kernels of
the 36 evaluation equations, fixes one nonzero projective coordinate in each
of the 22 blocks, and differentiates all 40 displayed equations.  At the
fixture it checks

```text
coefficient-constraint rank       36,
projective incidence Jacobian rank 36,
root-only Jacobian rank            28.                 (7)
```

The last line makes the differential of projection to the projective
coefficient space have zero root-direction kernel.  Thus (6) is not merely an
oversized parameter count: the local projected incidence image has dimension
`168` (and its full affine cone has dimension `244`).

## 4. Consequence for the rejected pencil route

The Bell-partition enumeration and its independent re-enumeration only audit
the surrogate quantity

```text
q_ij = number of distinct partition-block pairs,
```

not the tensor-span rank.  Consequently they cannot establish the claimed
codimension-nine pencil envelope.  In particular, the assertion that all
non-top sources already have affine dimension at most `242` is false for the
stratum above, so the proposed proper `B_all` cut on only the sixty claimed
top sources does not prove an ambient codimension-ten result.

The common-quadratic rank-drop fixture remains a valid nonempty control for
the original incidence conditions, but it does not repair this rank step or
classify the corrected `B_all` intersection.

The load-bearing repair is to replace `q_ij` by the actual span rank

```text
r_ij = dim span{x_i^(t) tensor x_j^(t) : t in N},
```

and stratify its rank-degeneracy loci, including their coordinate-subspace
and projection dimensions.  No codimension-nine or codimension-ten claim is
made here.

## Replay

```powershell
python claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_tensor_span_rank_boundary_correction.py
python -I claims/arbitrary-order/audit_eight_vertex_four_five_set_pencil_tensor_span_rank_boundary_correction.py
python -m py_compile claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_tensor_span_rank_boundary_correction.py claims/arbitrary-order/audit_eight_vertex_four_five_set_pencil_tensor_span_rank_boundary_correction.py
```

The primary check is exact rational SymPy arithmetic.  The independent audit
uses a separate finite-field nullspace and rank implementation; its modular
rank certificate is corroboration of the exact primary calculation, not a
replacement for the characteristic-zero argument.
