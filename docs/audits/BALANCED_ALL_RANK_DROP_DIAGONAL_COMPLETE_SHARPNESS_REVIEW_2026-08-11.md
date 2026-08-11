# Hostile review of the diagonal-complete all-rank-drop boundary

## Verdict and provenance

This record reviews
[`BALANCED_ALL_RANK_DROP_DIAGONAL_COMPLETE_SHARPNESS_THEOREM.md`](../../claims/arbitrary-order/BALANCED_ALL_RANK_DROP_DIAGONAL_COMPLETE_SHARPNESS_THEOREM.md)
as an arbitrary-order characteristic-zero sharpness theorem for the
all-balanced rank-drop branch.

Review verdict: **accept the complete diagonal family, its uniform balanced-
sensor rank bound, and the resulting route refutation for every `n=2m>=8`**,
after the focused scripts and publication floor pass.

The accepted conclusion is only that local concision, complete support,
invertible blocks, and the three normalized pure coefficients do not force a
full balanced sensor.  This review does not accept that the all-balanced
rank-drop locus meets the full witness equations, a counterexample, or a
global resolution.  The displayed graph has explicit nonzero mixed
coefficients and is not a Krenn--Gu witness.  The global conjecture remains
**UNRESOLVED**.

Codex reconstructed the family and its rank bound directly from the balanced
companion definition.  This is durable adversarial reasoning, not independent
human review.  The two scripts are exact bounded checks; the written matching,
polarization, and dimension argument is the arbitrary-order proof.

## 1. Exact graph and coefficient ledger

Every physical edge carries

```text
W_uv=lambda sum_(c=0)^2 e_(u,c)^* tensor e_(v,c)^*.  (1)
```

Thus a matching term is nonzero exactly when both endpoints of every edge
have the same colour.  If a word has colour-class sizes `n_0,n_1,n_2`, its
coefficient is therefore

```text
0                                      if some n_c is odd;
lambda^m product_c (n_c-1)!!           otherwise.    (2)
```

There is no cancellation in this calculation.  Each even colour class can be
matched independently, and every complete matching has exactly `m` edges.

Choosing `lambda^m=1/(2m-1)!!` is legal over `C` and makes every pure
coefficient one.  The mixed word with sizes `(2,2m-2,0)` has coefficient

```text
(2m-3)!!/(2m-1)!!=1/(2m-1),                         (3)
```

which is nonzero in characteristic zero.  Equation (3) is the exact reason
the family is not a witness.  It must not be described as a candidate
counterexample or as evidence that the witness intersection is nonempty.

## 2. Local concision is genuine

The edge blocks in (1) are invertible, but block invertibility alone would
not prove concision of the full matching tensor.  The theorem instead checks
the tensor flattening.

Leave vertex `v` open and set every other vertex to colour `c`.  The `c`
component is the normalized pure coefficient one.  Any `d!=c` component has
two odd colour classes, of sizes `2m-1` and one, and vanishes by (2).  The
three choices of `c` give the coordinate covectors.  Hence every one-vertex
flattening has rank three.

The support graph is complete because no block is zero.  The example
therefore defeats disconnected-support, singular-block, or local-rank
explanations of its balanced rank drop.

## 3. Companion symmetrization and polarization

Fix any balanced cut `R|N`.  The common coordinate bases canonically identify
all root dual spaces with one copy of `V^*`.  For fixed `D subset N`, the
companion sums over every selected root set, every bijection to `D`, and every
matching of the remaining roots.  Permuting the root slots permutes these
choices, so `G_D` is a symmetric `m`-tensor.

Set

```text
L_u(x)=q(x,z_u),             Q(x)=q(x,x).             (4)
```

If `k=|D|`, repeated-root evaluation gives

```text
G_D(x,...,x)
 =binomial(m,k) k! (m-k-1)!!
  lambda^((m+k)/2)
  Q(x)^((m-k)/2) product_(u in D)L_u(x).              (5)
```

The scalar counts the selected roots, their bijection to `D`, and the
matching of the remaining roots.  The exponent of `lambda` counts `k` cross
edges plus `(m-k)/2` internal root edges.  No graph edge on the `N` shore
enters a companion column.

Repeated-root evaluation would lose information for arbitrary tensors.  It
is sound here only because `G_D` is symmetric and characteristic zero makes
polarization injective.  The proof states both points explicitly.

## 4. Uniform rank bound, not a sampled rank

The legal subsets obey `k congruent m (mod 2)`.  There is exactly one
all-cross choice, `D=N`.  Every other legal choice has `m-k>=2`, so (5) has a
factor `Q`.  All non-all-cross columns therefore lie in the fixed subspace

```text
Q Sym^(m-2)(V^*),                                   (6)
```

of dimension `binomial(m,2)`.  The all-cross column adds at most one
dimension.  This proves

```text
rank Gamma_R(z_N)<=binomial(m,2)+1                   (7)
```

for every `z_N`, not merely at a numerical point.  Because the cut was
arbitrary, (7) holds for every balanced partition and hence over each
function field.

At `m=4`, the bound is `7<8`.  The gap then increases by
`2^(m-1)-m>0`, so all `m>=4` are strictly deficient.  No finite-order
extrapolation is used.

At `m=3`, the bound equals four.  Choosing the three `L_u` as a basis gives
the independent columns `Q L_u` plus `L_1L_2L_3`, the latter not divisible by
the nondegenerate ternary quadratic.  This retains the exact low-order
boundary and prevents an unsupported six-vertex rank-drop claim.

## 5. Computational independence and replay meaning

The SymPy primary check:

- enumerates all `3^8` words and their eight-vertex matching coefficients;
- checks the pure, mixed, and local-slice constants;
- directly constructs every four-root companion tensor from root choices,
  cross bijections, internal matchings, and colours;
- compares it with (5), obtaining rank seven;
- checks the common quadratic factor and generic exact ranks through `m=6`;
  and
- checks the integer dimension inequality through `m=64`.

The independent audit imports no repository module and no computer algebra.
It uses a separate sparse polynomial dictionary, hand-written `Fraction` row
reduction, direct matching/edge-colour enumeration through eight vertices,
and an independent choice-based reconstruction of the `m=4` companions.  It
also verifies exact ranks through `m=6` and the dimension inequality through
`m=79`.

The finite rank checks do not prove (7) at arbitrary order.  The common-
quadratic subspace and its exact dimension do.

## 6. Acceptance and residual boundary

Accepted after publication gates:

- the diagonal-complete graph has normalized pure coefficients, invertible
  blocks, complete support, and local concision;
- every one of its balanced sensors is identically rank-deficient for
  `n>=8`;
- the rank-drop proof is the uniform bound (7), not a generic sample; and
- the graph has explicit nonzero mixed coefficients and is not a witness.

Explicitly **UNKNOWN**:

- whether `B_all` meets the full Krenn--Gu witness equations;
- whether the mixed-word zero equations alone exclude this determinantal
  branch;
- a universal full-sensor theorem for hypothetical witnesses;
- any exact counterexample or global proof; and
- any Lean formalization of this boundary.

The global conjecture remains **UNRESOLVED**.

## Strongest fresh-referee objection

A fresh referee should first challenge the passage from repeated-root
polynomials to root tensors: it is valid only after proving permutation
symmetry of each companion and invoking characteristic-zero polarization.
The referee should then count the powers of `lambda` and verify that there is
exactly one column without an internal-root quadratic factor.  Finally, the
mixed coefficient (3) must remain adjacent to every status statement so this
strong ambient rank-drop example can never be mistaken for a witness.
