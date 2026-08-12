# Hostile review of the beta-three fixed-completion mixed-fibre block

## Verdict and immutable pins

This read-only hostile review accepts
[`MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_ROUTE_PORT_FIXED_COMPLETION_MIXED_FIBRE_RANK_THREE_BLOCK_THEOREM.md`](../../claims/arbitrary-order/MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_ROUTE_PORT_FIXED_COMPLETION_MIXED_FIBRE_RANK_THREE_BLOCK_THEOREM.md)
at exact core commit

```text
4ef53ef69c746698d7d191f10c80a753ec170b9e
```

with the following committed LF-normalized Git-byte SHA-256 pins:

```text
theorem:
54886b8591c6503c2a9565a60d42eebd469a4a4625af96fb74b756765754f30c

primary verifier:
e546b12e8730f73a3d8f25f847784d3470c64e88243172f1bdd98e9d386975e9

independent audit:
674183ca2c6f62a35f879d1be2e0bc88898af15647e62fcf193d5079696cdbfb
```

The hostile pass found no P0, P1, P2, or P3 defect.  The accepted result is
an exact conditional characteristic-zero composition theorem.  It is not an
attachment-existence theorem, a mixed-fibre exclusion, or a resolution of
the simultaneous all-bridge branch.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Exact accepted implication

The source object is the globally least A5 bipartite pure core `A` with

```text
beta(A)=3,
#PM(A)=4,
```

and one of the A5 `Q/Q` or `Q/C^2` suppressed route kernels.  The new
hypothesis is load-bearing:

> One fixed nonzero matching `K` on `V-S` extends all four core perfect
> matchings into the same complete mixed word fibre `F_chi`.

The theorem does not derive this hypothesis.  Conditional on it, the four
extensions form a set `B_K` of four distinct matching terms.  Their total is
the pure four-term cancellation multiplied by the same nonzero factor
`lambda(K)`, so

```text
sum_(X in B_K) lambda(X)=0.
```

The complete mixed target coefficient also vanishes.  Subtracting the block
zero from the complete-fibre zero gives

```text
sum_(X in F_chi-B_K) lambda(X)=0.
```

Every supported full matching monomial is nonzero in the complete nonzero
matrix-unit branch.  A one-term complement would therefore equate one
nonzero monomial to zero.  Hence

```text
|F_chi-B_K|=0 or |F_chi-B_K|>=2,
|F_chi|=4 or |F_chi|>=6,
|F_chi|!=5.
```

The empty complement is allowed.  No classification of a complement having
two or more terms follows.

## 2. Affine rank and exponent lattice

A3 proves that the perfect-matching polytope of the connected bipartite
matching-covered core has affine dimension `beta(A)`.  Here its convex hull
has dimension three but has only the four A5 incidence vectors.  Those four
vectors must therefore be affinely independent.

After choosing one vector `a_0` as reference, the three differences

```text
u_i=a_i-a_0,  i=1,2,3,
```

are linearly independent over the reals and rationals.  Their integer span is
a free rank-three lattice.  Adding the same fixed-completion incidence vector
to every `a_i` cancels in every difference, so the injected block still has
exact difference rank three.

This argument does not assert that the block lattice is saturated in the
ambient edge lattice.  It also does not turn scalar amplitude cancellation
into an affine or integer relation among exponent vectors.  In particular,
there is no nonzero integer dependency among the three displayed block
differences, odd or otherwise.

## 3. U7K and complete-target scope

The completion hypothesis is the U7K termwise attachment setup specialized
to residual shore `R=S` and empty fixed internal matching.  The review checked
that the theorem states all facts needed for the specialization directly:

- `K` is vertex-disjoint from the core matchings;
- every union is a full supported physical perfect matching;
- the same fixed `K` is used for all four terms;
- all four unions induce the same word; and
- that word is mixed.

The word **complete** in `F_chi` is also load-bearing.  The cardinality
argument uses the target equation containing every compatible matching at
`chi`, not a selected or sampled subfibre.  The theorem does not infer a
complete-fibre statement from the internally cancelling block alone.

The rank-three block places the complete fibre at difference rank at least
three, but this supplies no Laurent unit and no aggregate-fibre
classification.  U7E's odd-dependency conclusion belongs to an all-binomial
complete-block hypothesis.  A single four-term aggregate block with three
independent differences does not satisfy that hypothesis and does not invoke
that exclusion.

## 4. Restricted route ports

The route-port statements are explicitly restricted to the injected block.
For a core port `P_A(p,f)`, the theorem defines

```text
P_B(p,f)={K union M : M in P_A(p,f)} subset B_K.
```

An unrelated matching in `F_chi-B_K` may also use `f`.  Thus a singleton or
doubleton statement about `P_B` is not promoted to the corresponding full
`F_chi` port.

For `Q/Q`, the four odd routes give four paired singleton block ports.  For
`Q/C^2`, the four odd routes again give paired singletons, while the unique
even route has the A5-labelled complementary block doubletons

```text
P_B(x,g_x)={K union M_y1,K union M_y2},
P_B(y,g_y)={K union M_x1,K union M_x2}.
```

Their full edge-inclusive contributions are nonzero and exact negatives.
The common factor `lambda(K)` preserves both nonvanishing and negation.  The
review found no endpoint-label reversal.  These identities include the
endpoint edge weights and do not imply equality or negation of bare deletion
hafnians.

## 5. Formal polynomial versus pointwise cancellation

The formal normalized block polynomial is

```text
p_B=1+X+Y+Z
```

in the group algebra of the free rank-three difference lattice.  Its four
formal exponents are distinct, so `p_B` is not the zero polynomial.  The
physical pure cancellation supplies a particular nonzero torus evaluation at
which `p_B` vanishes; it is not a polynomial identity in algebraically
independent edge weights.

Independently, the explicit torus point

```text
(X,Y,Z)=(-1/3,-1/3,-1/3)
```

kills `p_B`.  Evaluation there is a unital homomorphism from the Laurent
group algebra to `C`, so a polynomial mapped to zero cannot be a unit.  This
proves only that the individual block polynomial is a proper nonunit.  It
does not prevent a larger family of complete target equations from
generating the unit ideal.

The pointwise amplitude zero and the absence of exponent dependencies are
therefore compatible and correctly kept separate.

## 6. Conditional U7J reading

The U7J interpretation is stated only when `chi` is a selected active-cycle
word and

```text
B_K intersect {G_(i-1),F_i}=empty.
```

Under this extra condition, every block term is indeed in the U7J extra list,
and its normalized subtotal is zero.  The theorem does not infer that the
block exhausts the extra list or that the full aggregate defect vanishes.  If
the selected-term avoidance fails, it withdraws the U7J extra-subfibre
reading while retaining only the earlier fixed-completion conclusions.

## 7. Evidence and independence boundary

The exact primary verifier uses direct edge-incidence representations of the
displayed A5 `Q/Q` and `Q/C^2` controls.  It checks:

- four genuine perfect matchings in each control;
- affine and all-pair difference rank three over `Fraction`;
- augmented rank four, excluding rational and integer affine dependencies;
- preservation under a common fixed incidence and nonzero multiplier;
- exact weights `1,1,1,-3` and `Q/C^2` doubleton totals `2,-2`;
- empty or nonsingleton zero remainders, with a sharp size-two control; and
- a nonzero torus zero of `1+X+Y+Z`.

The independent audit imports neither the theorem nor the primary verifier.
It instead builds physical route subdivisions, recursively enumerates perfect
matchings as edge bitmasks, derives the route ports, checks an exact
unimodular rank-three minor, adjoins disjoint fixed matching edges, evaluates
the Laurent polynomial, and performs a separate bounded remainder census.
This is a materially distinct derivation and representation, not merely a
second filename or random seed.

Both programs are bounded mechanism replays.  They do not prove that a
compatible completion exists in a hypothetical witness.  Their finite route
controls also do not replace A5's proved arbitrary-positive-length parity
argument.  No complete simultaneous all-bridge witness is constructed.

The exact replay commands passed:

```text
python -B claims/arbitrary-order/verify_matrix_unit_all_bridge_beta_three_route_port_fixed_completion_mixed_fibre_rank_three_block.py
python -I -B claims/arbitrary-order/audit_matrix_unit_all_bridge_beta_three_route_port_fixed_completion_mixed_fibre_rank_three_block.py
uv run --with ruff==0.16.2 ruff check claims/arbitrary-order/verify_matrix_unit_all_bridge_beta_three_route_port_fixed_completion_mixed_fibre_rank_three_block.py claims/arbitrary-order/audit_matrix_unit_all_bridge_beta_three_route_port_fixed_completion_mixed_fibre_rank_three_block.py
```

## 8. Collision and severity audit

The result is accurately presented as a conditional A3+A5+U7K composition
and one-term-complement obstruction.  It does not claim a new universal
attachment mechanism.

The review found no scope collision with:

- Larry's complementary-shore response/portal lane;
- S2N's common-shore singleton-slice and empty-permanent compatibility lane;
- S2O's protected control/common-shore pullback lane; or
- shared navigation, frontier, and ledger ownership.

No mixed cut, complementary-shore response, common-shore matching-sum
realization, control pullback, or protected portal conclusion is used or
asserted.

The severity verdict is:

```text
P0: none
P1: none
P2: none
P3: none
```

The fixed-completion hypothesis remains unproved, the complement may be
empty, aggregate fibres remain open, the simultaneous all-bridge branch is
not excluded, and the global Krenn--Gu conjecture remains **UNRESOLVED**.
