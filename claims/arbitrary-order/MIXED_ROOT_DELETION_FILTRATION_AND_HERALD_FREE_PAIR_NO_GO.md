# Mixed-root deletion filtration and herald-free pair no-go

## Status

**Exact arbitrary-order characteristic-zero expansion theorem and sharp
physical common-shore controls.**  Passing from principal root coefficients
to arbitrary mixed root derivative words does not cross the P7 root-budget
staircase.  Restrict any perfect matching to the probe roots.  It consists of
a partial matching among roots, together with an injection of every remaining
root into distinct nonroot vertices.  Therefore a term with `j` root--root
edges deletes exactly

```text
r-2j                                                     (1)
```

nonroots from its complementary principal hafnian.  In particular, no mixed
root word deletes more than `r` nonroots.

For the active two-residual P7 cell, `r=5`.  A direct blocker pair and a
one-residual blocker singleton both require deletion depth seven.  Their
cofactor columns are therefore absent from **every** mixed-root observation
matrix, not merely from the top principal coefficient.  Root--root
companions make the deficit worse; root--residual companions use one root for
one residual and do not change the bound.

Two controls show sharpness.

1. An honest nine-nonroot graph with only the desired pair edge has every
   principal hafnian cofactor of deletion depth at most five equal to zero,
   while the depth-seven pair cofactor is arbitrary.  Thus physical hafnian
   realizability alone does not reconstruct the missing pair from the entire
   shallow cofactor tower.
2. A fourteen-vertex common-shore graph has a nonzero root tensor at every
   root word, but that entire tensor is independent of an arbitrary direct
   blocker edge.  The varying edge is hidden because the unique root shore
   always occupies its two endpoints.  Thus nonzero root data do not remove
   the kernel.

A universal herald-free "vacuum by cancellation" is also impossible.  Every
physical evaluation at a present vertex is homogeneous of degree one in its
incident edge blocks, whereas deleting that vertex has degree zero in those
blocks.  Scaling the incident blocks separates the two operations.  An
actual added herald vertex or a target-specific nonlinear identity is outside
this theorem and remains a possible new mechanism.

The common-shore controls do not satisfy the full mixed GHZ coefficient
system.  Hence this result closes the universal matching-recursion and linear
selector routes, but it does not exclude a GHZ-specific cross-depth identity
and does not resolve P7 or Krenn--Gu.

No graph family, support family, derivative-word family, or parameter set is
searched or enumerated.  The proof is the symbolic matching partition (5),
not a computational survey.  The replays evaluate only fixed small controls.

## 1. Arbitrary mixed root words

Let `R` be a set of `r` probe roots and `N` the nonroot vertices.  Root local
vectors may independently be fixed or differentiated; write the selected
vector at root `i` simply as `x_i`.  After contracting any already fixed
nonroot directions, write

```text
L_ij=B_(i,j)(x_i,x_j),             i,j in R,
H_(i,u)=B_(i,u)(x_i,z_u),          i in R, u in N.      (2)
```

For `D subset N`, let

```text
C_D=haf G[N minus D]                                      (3)
```

be the complementary nonroot principal hafnian.  The tensors in (2) may
retain uncontracted local factors; the same argument then takes place over
their commutative coefficient ring.

A partial matching `P` of `R` is a set of disjoint root pairs.  Put

```text
R_P=R minus vertices(P).                                  (4)
```

For an injection `f:R_P -> N`, write `im f` for its image.

### Theorem 1 (mixed-root cofactor expansion)

Every mixed root word has the exact expansion

```text
T_R
 =sum_(P a partial matching of R)
   product_({i,j} in P) L_ij
   sum_(f:R_P -> N injective)
     product_(i in R_P) H_(i,f(i)) C_(im f).             (5)
```

Consequently every cofactor label in the word satisfies

```text
|im f|=r-2|P|<=r.                                        (6)
```

Proof.  Restrict a perfect matching of `R union N` to the root vertices.
The root--root edges form a unique partial matching `P`.  Every remaining
root has exactly one partner in `N`, and distinct roots have distinct
partners, giving a unique injection `f`.  After removing those root and
root--nonroot edges, the unmatched nonroots are exactly
`N minus im f` and contribute `C_(im f)`.  Conversely, a choice of `P`, `f`,
and a perfect matching counted by `C_(im f)` gives one full perfect matching.
This is a bijective matching partition at arbitrary order.

The proof does not depend on which roots carry tangent rather than fixed
vectors.  Changing the derivative word changes the values in (2), not the
cofactor support in (5).

### Corollary 2 (root-root and residual companions cannot help)

Each root--root edge lowers the deletion depth by two.  Matching a root to a
residual companion places that residual in `im f` but still deletes exactly
one nonroot with one root.  Hence neither mechanism can produce a cofactor
with more than `r` deleted nonroots.

The parity refinement in (6) is also exact: the only possible depths are

```text
r, r-2, r-4, ... .                                      (7)
```

There is an equivalent residual/port grading that sharpens the earlier
staircase.  Let there be `m` blocker ports, `q` residual vertices, and
`r=m-q` roots.  If the complementary cofactor leaves `T subset Q` and
`S subset B`, then its deletion set is

```text
D=(Q minus T) union (B minus S).
```

For a term with `j` root--root edges, (6) gives

```text
m+q-|S|-|T|=m-q-2j,
|S|+|T|=2q+2j.                                        (7a)
```

Thus the mixed-root tensor does not merely obey the inequality
`|S|+|T|>=2q`; its root--root matching number grades the exact even levels
above that boundary.  For the three P7 residual splits:

```text
q=2, r=5:  |S|+|T| in {4,6,8};
q=4, r=3:  |S|+|T| in {8,10};
q=6, r=1:  |S|+|T| = 12.                              (7b)
```

The formula is arbitrary-order in `m`; no case classification is used.

## 2. The P7 below-staircase labels never occur

In the two-residual cell, let

```text
R: five probe roots,
Q={q_0,q_1},
B: seven blocker ports.                                 (8)
```

For blockers `u,v`, the direct pair response is

```text
m_uv=haf B[{u,v}]
    =C_(Q union (B minus {u,v})).                        (9)
```

Its deletion set has order `2+5=7`.  The one-residual singleton leaving
`q_i,u` is

```text
y_(i,u)
 =C_({q_(1-i)} union (B minus {u})),                    (10)
```

again of deletion order `1+6=7`.

### Theorem 3 (all-mixed-word linear nonobservability)

No P7 mixed-root derivative word, no linear combination of such words, and
no legal linear root probe contains the cofactor column (9) or (10).  In the
formal cofactor ledger, their selector coefficient is identically zero.

Proof.  Theorem 1 limits every column to deletion depth at most five, while
(9)--(10) have depth seven.  Linear combinations alter coefficients of
columns already present; they cannot create an absent column.

This strengthens the earlier principal root-budget count to every root
derivative order and every root--root/residual companion pattern.  It is a
linear observability theorem.  A nonlinear physical hafnian identity between
different deletion depths would be additional information, not a selector
from (5).

## 3. Physical shallow cofactors do not determine the pair

Take nine nonroot vertices and choose two of them `u,v`.  Install only

```text
B_uv=t                                                    (11)
```

and set every other nonroot edge to zero.

### Proposition 4 (physical shallow-tower kernel)

For every `D subset N` with `|D|<=5`,

```text
C_D=0,                                                    (12)
```

while

```text
C_(N minus {u,v})=t.                                     (13)
```

Proof.  The graph in (11) has matching number one.  If `|D|<=5`, then
`N minus D` has at least four vertices, so it has no perfect matching and its
hafnian is zero.  Deleting the other seven vertices leaves the single edge
`uv`, whose hafnian is `t`.

Thus even the complete physical principal-hafnian tower through the maximal
mixed-root depth has an affine-line fiber over the desired pair.  This is not
only formal algebraic independence of cofactor symbols.

The same construction with the sole edge `q_i u=t` gives the corresponding
one-residual singleton control.

## 4. A nonzero forced shore still hides the pair

Now use the actual P7 counts.  Label the nonroots

```text
N={u,v,b_1,b_2,b_3,b_4,b_5,q_0,q_1}.                  (14)
```

Let five roots `r_1,...,r_5` have only the root--nonroot edges

```text
r_1-u, r_2-v, r_3-b_1, r_4-b_2, r_5-b_3,              (15)
```

with respective root forms `alpha_1,...,alpha_5`.  Set all root--root and
other root--nonroot blocks to zero.  Among the remaining nonroots install

```text
B_(b_4,b_5)=1,             A_(q_0,q_1)=1,              (16)
```

and also install the hidden edge

```text
B_uv=t.                                                   (17)
```

Every full matching is forced to use all five edges (15): each root has only
one neighbor.  The endpoints `u,v` are therefore already occupied, so (17)
cannot occur.  The remaining four vertices use the two edges (16).

### Theorem 5 (nonzero common-shore pair kernel)

The complete root coefficient tensor is

```text
T_R=alpha_1 alpha_2 alpha_3 alpha_4 alpha_5,             (18)
```

which is nonzero and independent of `t`.  Every mixed root derivative of
(18) is likewise independent of `t`, while the direct blocker cofactor
`m_uv=t` varies.

Thus the all-mixed-root observation map has a physical affine-line fiber even
over a nonzero forced shore.  The control can be realized by symmetric
bilinear edge blocks: take each edge in (15) to be the root form
`alpha_i` tensored with a fixed blocker covector, and transpose it on the
reverse orientation.

This model supplies one nonzero pure/common-shore coefficient, not the full
three-colour GHZ jet.  Mixed GHZ equations could forbid its sparse root
support; no claim to the contrary is made.

## 5. Why herald-free vacuum cancellation cannot cross the filtration

Fix a nonroot vertex `w`.  Every graph tensor with `w` present is homogeneous
of degree one in the family of edge blocks incident to `w`, because every
perfect matching uses exactly one incident edge.  This remains true after
any root differentiation, polarization, and linear combination of physical
evaluations at `w`.

By contrast, the tensor obtained by deleting `w` is independent of every
edge block incident to `w`.

### Theorem 6 (no universal linear vacuum simulator)

There is no graph-independent linear combination of physical evaluations or
polarizations at a present vertex that equals deletion of that vertex for
all symmetric block graphs, unless the deleted cofactor is identically zero.

Proof.  Scale every edge block incident to `w` by a scalar `lambda`.  Every
candidate physical-evaluation combination scales by `lambda`.  The deleted
cofactor does not scale.  If the two were universally equal, then

```text
lambda F=F                                                (19)
```

for every `lambda`, forcing `F=0` in characteristic zero.  A graph with a
nonzero perfect matching after deleting `w` contradicts that conclusion.

Finite-difference and inclusion--exclusion expressions are linear
combinations of evaluations and are covered by the theorem.  Setting the
local vector at `w` to zero produces zero, not the deleted tensor.

An actual herald with an added constant/vacuum coordinate changes the local
multigrading and the vertex set, so it is not ruled out.  Such a gadget must
be constructed and shown compatible with the P7 target; it cannot be assumed
from the existing graph tensor.

## 6. Exact remaining boundary

The proved filtration is

```text
all mixed root words on r probes
  -> cofactors at nonroot deletion depths r,r-2,...
  -> arbitrary linear selectors remain in depth <=r.   (20)
```

For P7 with two residuals,

```text
mixed-root ceiling:                     depth 5;
direct pair / one-residual singleton:   depth 7.         (21)
```

Therefore a successful proof must use at least one operation not contained
in (20):

1. a target-specific nonlinear relation between physical hafnians at depths
   five and seven;
2. a genuine extra herald/vacuum coordinate whose legality is proved;
3. a cross-window gluing identity that introduces additional matched
   endpoints rather than linearly recombining the same root words; or
4. an indirect contradiction that avoids reconstructing the missing faces.

The physical controls exclude a universal nonlinear relation based solely on
the shallow principal hafnians.  They do not exclude a relation after all
GHZ-specific mixed coefficients are imposed.

The companion
`PRINCIPAL_FOUR_HAFNIAN_GENERIC_EDGE_TOMOGRAPHY_AND_P7_SINGULAR_FIBRE_BOUNDARY.md`
now implements the first route on a nonempty generic chart: a fully **named**
depth-five four-hafnian deck makes every nonroot edge finite algebraic.  The
one-edge control here lies on its explicit singular fibre.  Thus there is no
conflict: this theorem rules out global linear or universal recovery, while
the four-hafnian theorem isolates labeled exposure and singular-locus
avoidance as the exact nonlinear obligations.

## Scope wall

```text
arbitrary-order mixed-root expansion (5):              PROVED;
nonroot deletion depth <= number of roots:             PROVED;
root-root companions increase deletion capacity:        FALSE;
root-residual companions increase deletion capacity:    FALSE;
P7 direct pair/singleton column in any root word:        ABSENT;
physical shallow hafnian tower determines depth-7 pair: FALSE;
nonzero forced root shore determines depth-7 pair:      FALSE;
herald-free linear vacuum/deletion simulator:            IMPOSSIBLE;
target-specific nonlinear GHZ cross-depth identity:      UNKNOWN;
legal added herald/vacuum coordinate:                    UNKNOWN;
full target-compatible P7 physical kernel:               UNKNOWN;
unrestricted P5/P6/P7 nonrestriction:                   UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_mixed_root_deletion_filtration_and_herald_free_pair_no_go.py
python claims/arbitrary-order/audit_mixed_root_deletion_filtration_and_herald_free_pair_no_go.py
python -m py_compile verify_mixed_root_deletion_filtration_and_herald_free_pair_no_go.py audit_mixed_root_deletion_filtration_and_herald_free_pair_no_go.py
uv run --with ruff ruff check verify_mixed_root_deletion_filtration_and_herald_free_pair_no_go.py audit_mixed_root_deletion_filtration_and_herald_free_pair_no_go.py
```

The primary replay checks a generic symbolic three-root instance of (5), the
P7 depth counts, the shallow matching-number control, the symbolic nonzero
forced-shore tensor, and the vacuum scaling obstruction.  The independent
no-import audit uses separately written exact hafnian recurrence on the
sparse fourteen-vertex control.  Neither replay searches graphs, supports,
root words, or parameters.  The three-root check expands one fixed
eight-vertex hafnian solely as a small audit of the arbitrary-order symbolic
proof.
