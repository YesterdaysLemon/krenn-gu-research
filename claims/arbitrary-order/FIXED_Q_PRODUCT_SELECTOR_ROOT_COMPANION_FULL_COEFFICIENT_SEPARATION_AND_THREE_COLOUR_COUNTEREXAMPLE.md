# Fixed-Q product-selector root-companion/full-coefficient separation and three-colour counterexample

## Status

**Verified exact characteristic-zero correction, physical graph-side
counterexample to former `GLD65` Theorem 5, and route obstruction for
`GLD66`.**  A legal four-port pure-`M` selector constrains the evaluated root
companions `G_D` in the fixed-`Q` module.  It does not set the full matching
coefficient `F_D` on `R union D` to zero after direct edges inside `D` are
restored.

For every pair of ports `{u,v}`, the exact consequence of a normalized
pure-`M` selector is

```text
G_(Q union {u,v})=0,
F_(Q union {u,v})=m B_uv,                              (1)
```

where `m=G_Q!=0`.  The former `GLD65` proof instead imposed
`F_(Q union {u,v})=0` and obtained the invalid cross-Gram identity
`J=-mB`.  It thereby transferred a root-companion nuisance equation to a
different full matching coefficient.

An explicit ternary physical graph below has a factored legal pure-`M`
selector, six target-diagonal direct port blocks, and

```text
M_U=e_0^(tensor 4)+e_1^(tensor 4)+e_2^(tensor 4).      (2)
```

It satisfies every entry of the complete evaluated `GLD15` companion row.
Thus it directly refutes the stated conditional three-colour exclusion in
`GLD65`.  The `GLD66` two-colour exclusion and synchronized-plane corollaries
depend on the same invalid legal-selector-to-cross-Gram bridge and are
withdrawn with it.  The fixture does not satisfy GLD66's separately written
full-coefficient-zero assumption; it refutes the claimed source of that
assumption, not the later algebra conditional on it.

The graph does not satisfy the full ten-vertex GHZ equation: its global
all-one pure coefficient is zero, whereas the GHZ target coefficient is one.
It is not a counterexample to Krenn--Gu.  The global conjecture remains
**UNRESOLVED**.

## Dependencies and affected claims

The typed companion object is the one defined in

- [`GLS2`](MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md).

The complete joint module and pure-`M` row are from

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md), and
- [`GLS17`](MAXIMAL_ROOT_SURPLUS_TWO_PARTIAL_ROOT_GRADE_SHADOW_AND_COMMON_PURE_M_SELECTOR_THEOREM.md).

The incorrect substitution occurs in

- [`GLD65`](FIXED_Q_FOUR_ROOT_PRODUCT_SELECTOR_THREE_COLOUR_CAMOUFLAGE_EXCLUSION_THEOREM.md),

and is inherited by

- [`GLD66`](FIXED_Q_FOUR_ROOT_PRODUCT_SELECTOR_TWO_COLOUR_EXCLUSION_AND_FIRST_ROOT_PLANE_SYNCHRONIZATION_THEOREM.md).

The correction does not alter `GLS2`, `GLD15`, `GLS17`, `GLS18`, `GLS19`, or
the independently derived `GLD64` theorem.  No external literature claim is
used.

## 1. The two coefficient types

Work over a characteristic-zero field `K` with

```text
R={r_0,r_1,r_2,r_3},
Q={q_0,q_1},
U={u_0,u_1,u_2,u_3},
B=Q disjoint-union U.                                  (3)
```

For an even `D subset B`, `G_D` is the `GLS2` root companion: choose a
partial matching among the roots and biject every unused root to `D`.
There are no edges internal to `D` in `G_D`.

After evaluating the root slots by a product functional and evaluating `Q`
at the fixed residual vectors, write `g_D` for the resulting tensor on
`D intersect U`.  By contrast, let `f_D` be the full perfect-matching tensor
on `R union D` after the same evaluations.  The latter permits direct edges
inside `D`.  Write `E_ab` for the evaluated direct outside edge on
`{a,b} subset D`; in particular `E_uv=B_uv` for two ports.

For four outside vertices, matching by the number of direct outside edges
gives

```text
f_D
 =g_D
  +sum_({a,b} subset D) E_ab g_(D-{a,b})
  +haf(E[D]) g_empty.                                  (4)
```

The three terms have respectively zero, one, and two direct outside edges.
This is an exact partition of matchings, with no division or rank
assumption.

### Theorem 1 (pure-M selectors constrain companions, not full coefficients)

Suppose a normalized legal `GLD15` pure-`M` selector exists for target `U`.
Before normalization let its desired coefficient be `m!=0`.  Then

```text
g_Q=m,
g_empty=0,
g_D=0 for every allowed D!=Q,empty.                    (5)
```

In particular, for every pair `{u,v} subset U`,

```text
g_(Q union {u,v})=0.                                  (6)
```

The corresponding full coefficient is instead

```text
f_(Q union {u,v})=m B_uv.                             (7)
```

#### Proof

In the `GLD15` companion map, the label `I` has coefficient `G_(B-I)`.  The
pure-`M` row is nonzero only on `I=U`, whose companion is `G_Q`; it is zero on
`I=B`, whose companion is `G_empty`, and annihilates every other labelled
summand.  This is exactly (5), including (6).

Apply (4) to `D=Q union {u,v}`.  Every `g_D` term vanishes by (5), except the
term with direct edge `uv`, whose complementary companion is `g_Q=m`.
The two-direct-edge term contains `g_empty=0`.  This leaves (7).  `square`

Thus legal module nuisance gives (6), not `f_(Q union {u,v})=0`.  If

```text
J(ell_u,ell_v)=g_(Q union {u,v}),                     (8)
```

then the correct root-companion identity is simply `J=0`.  No representation
of the independent direct block `B_uv` follows.

## 2. Exact ternary graph

Use the dual coordinate basis `e_0^*,e_1^*,e_2^*` at every vertex.  Put

```text
x_i=(1,1,1) for every root,
z_q=(1,1,1) for q in Q,
y_3=e_0,
rho=(x_0,x_1,x_2,y_3).                                (9)
```

All unlisted blocks are zero, and reverse orientations are transposes.  The
nonzero root or root--outside blocks are

```text
W_(r_2,r_3)=e_0^* tensor (e_0^*-e_1^*),
W_(r_0,q_0)=e_0^* tensor e_0^*,
W_(r_1,q_1)=e_0^* tensor e_0^*,
W_(r_2,u)=e_0^* tensor e_0^*       for every u in U.  (10)
```

On the six port pairs use the diagonal camouflage blocks

```text
colour 0: u_0u_1, u_2u_3;
colour 1: u_0u_2, u_1u_3;
colour 2: u_0u_3, u_1u_2,                             (11)
```

each with unit coefficient.  Give every remaining outside--outside pair
(the `q_0q_1` and `q_i u_j` pairs) the block
`e_0^* tensor e_0^*`.

### Theorem 2 (maximum root and factored legal row)

The root set `R` is a maximum-cardinality torus zero set at `x`.  Evaluation
at `rho` defines a `GLS17`-factored legal `GLD15` pure-`M` selector for target
`U`, with complete companion table

```text
g_Q=1,
g_D=0 for |D| in {0,2,4} and D!=Q.                    (12)
```

#### Proof

The only root--root block satisfies

```text
W_(r_2,r_3)(x_2,x_3)=1*(1-1)=0,                      (13)
```

so `R` is a torus zero set.  Every outside--outside block is a nonzero
coordinate monomial and is nonzero on fully supported vectors.  Hence a
torus zero set contains at most one outside vertex.  The vertices `q_0`,
`q_1`, and every port have nonzero coordinate-monomial incidences with
respectively `r_0`, `r_1`, and `r_2`; adding one outside vertex therefore
displaces at least one root.  No torus zero set has more than four vertices.

At `rho`, the only nonzero root edge is `r_2r_3`.  For `|D|=0`, that single
edge cannot cover all four roots, so `g_empty=0`.  For `|D|=2`, a root
companion must use `r_2r_3`; the remaining roots attach nontrivially only as
`r_0q_0` and `r_1q_1`, giving `g_Q=1` and every other two-set zero.  For
`|D|=4`, every root must attach outside, but no outside incidence uses
`r_3`, so every four-set companion is zero in every port colour.

The product evaluation differs from the maximum-root evaluation only at
`r_3`.  It therefore factors through the `GLS17` first-root map at `r_3`.
Equation (12) is exactly the complete `GLD15` operator row `(1,0)`, not a
selected nuisance ledger.  `square`

### Theorem 3 (three-colour response and explicit coefficient separation)

All six direct port blocks are target-diagonal and their four-port matching
tensor is exactly (2).  Moreover, at port word `(u_0,u_1)=(0,0)`,

```text
g_(Q union {u_0,u_1})=0,
B_(u_0,u_1) g_Q=1,
f_(Q union {u_0,u_1})=1.                              (14)
```

#### Proof

The three perfect matchings of `U` are precisely the three pairs in (11).
Each contributes one pure colour word, and no mixed word has compatible
colours on both edges.  This proves (2).

The first identity in (14) is the four-set part of (12).  The displayed
direct edge and `g_Q` both have value one.  Formula (7) gives the last
identity.  Equivalently, direct matching enumeration has one surviving
family: use the edge `u_0u_1` and the `Q` companion.  `square`

This graph satisfies the explicit hypotheses of the former `GLD65` product-
selector exclusion but has all three nonzero pure response colours.  The
asserted cross-Gram identity and the resulting dimension contradiction are
therefore false.

It is explicitly off the global witness locus.  At the all-one word on all
ten vertices, every block incident to a root has zero `(1,1)` entry, so every
perfect matching has weight zero.  The required pure GHZ coefficient would
be one.

## 3. Exact consequence for the live frontier

```text
root companion G_D versus full coefficient F_D:              DISTINCT;
pure-M selector companion table (5):                          PROVED;
full coefficient formula F_(Q union uv)=m B_uv:               PROVED;
physical maximum-root factored-selector fixture:              PROVED;
diagonal three-colour pure M_U in that fixture:                PROVED;

GLD65 cross-Gram identity J=-mB:                              FALSE;
GLD65 product-selector three-colour exclusion:                WITHDRAWN;
GLD66 product-selector two-colour exclusion:                  WITHDRAWN;
GLD66 first-root plane synchronization:                       WITHDRAWN;

GLS2/GLD15/GLS17--GLS19:                                     UNAFFECTED;
GLD64 decomposable-channel theorem:                           UNAFFECTED;
global Krenn--Gu conjecture:                                  UNRESOLVED.    (15)
```

The failed route cannot be repaired by adding the previously unused higher
nuisance labels: the fixture satisfies the complete evaluated companion row
through every allowed depth.  A future parent theorem must use a genuine full
target equation, a second independently legal response axis, or another
coefficient-pure bridge.  It may not identify a root companion with the full
matching tensor obtained after restoring direct outside edges.

## 4. Parent-theorem checkpoint and proof-distance delta

The parent proposition attacked here was the following fixed-`Q`, root-order-
four bridge:

> For every actual root-order-four maximum-root surplus-two hypothetical
> complex witness, fix one residual pair and contraction on the branch where
> all six `GLS16` pair base shadows and one `GLS17` four-port first-root shadow
> survive.  Use the resulting product-form pure-`M` selector, the complete
> `GLD15` nuisance equations, and the target-coupled `GLS18`/`GLS19` data to
> force a direct-port response restriction entering a named mixed-coefficient
> detector on every relevant rank fibre.  The linear implications may be
> transported to characteristic zero only after the physical hypotheses are
> supplied.

The intended synthesis consumed the two consecutive sibling mechanisms
`GLD65` (cross-Gram camouflage exclusion) and `GLD66` (response-anchor
dimension reduction).  Re-deriving their shared parent interface before
using additional higher nuisance labels exposed the `G_D`/`F_D` type change.
The exact graph in Section 2 is the hostile control: it satisfies the complete
product-selector companion row, including every higher nuisance label, while
retaining the forbidden three-colour response.

The outcome is an exact no-go for the proposed module-only parent route, not
a no-go for the witness-level parent proposition.  The proof-topology delta
is therefore:

- two formerly live exclusion edges are withdrawn;
- the method class "one complete companion row implies full-coefficient
  cross-Gram control" is eliminated exactly; and
- the parent obligation is replaced by the sharper typed alternatives of a
  genuine full-target equation, a second independently legal response axis,
  or another coefficient-pure bridge.

No global proof distance is claimed to have decreased.  The gain is removal
of a false shortcut and a precise universal-bridge interface that future work
can attack without repeating the same type error.

## Verification

Run from the repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_product_selector_companion_full_coefficient_separation.py
python -I claims/arbitrary-order/audit_fixed_q_product_selector_companion_full_coefficient_separation.py
```

The primary replay builds all ternary blocks, enumerates the complete `431`
evaluated companion entries, verifies the maximum-root incidences and direct
four-port tensor, and compares the root-only and full eight-vertex
coefficients.  It also checks the failed global all-one coefficient.  The
independent audit imports no project code and uses a separate sparse evaluated
representation with bitmask hafnian recursion.
