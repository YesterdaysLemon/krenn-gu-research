# Full common-star source exclusion by orthogonal center/leaf contractions

## Status and scope

**Proved over C, with a dedicated independent proof review.** For every
finite k>=2, no common-star protected-K4 array can realize the full ternary
GHZ target. The proof below uses all center/uniform-leaf words, not only
component-constant words or a bounded minority subsystem. The
[review](../../docs/audits/COMMON_STAR_FULL_SOURCE_EXCLUSION_REVIEW_2026-09-20.md)
records its inspected artifacts and evidence boundaries.

The global Krenn--Gu conjecture remains **UNRESOLVED**. There is no claimed
normal form from arbitrary protected fillings or arbitrary global witnesses
to this support family. In particular, the even-k argument does not prove
the earlier CSQ4 parent (component-constant targets plus U4) or FB. It gives
a direct full-source exclusion that bypasses those proposed intermediate
routes for the common-star construction. No Lean formalization is supplied.

The exact parent and upstream/downstream relationship are recorded in the
[resumed parent attempt](../../docs/strategy/exterior-coupling-parent-resumption-2026-09-20.md).

## Physical family and the AB-word source

Use precisely the physical construction in
[PSCS](PROTECTED_SCAFFOLD_COMMON_STAR_COMPONENT_TARGET_OBSTRUCTION.md):
k protected unit K4 components, local vertices 0,1,2,3, and

    M_0={01,23}, M_1={02,13}, M_2={03,12}.

Every edge in M_c has its entire color matrix equal to E_cc. Vertex 0 is
the center, and vertex c+1 is the color-c leaf. A simple component edge
with its one unequal endpoint label (a,b) carries a nonzero factor A on
its center-center physical edge and a nonzero factor B on its selected
color-a/color-b leaf edge. Every other crossing entry is zero.

For x,y in {0,1,2}^k, give center u color x_u and all three leaves at u
color y_u. Call this the physical AB word (x,y). Define symmetric
zero-diagonal component matrices A_x and B_y from the actual center and
leaf factors compatible with x and y respectively. Set

    a_S(x_S)=haf A_x[S],    b_S(y_S)=haf B_y[S],

for even S, with both empty hafnians equal to one. These polynomials
depend only on the indicated colors within S and on the fixed actual
array. No cofactor is independently assigned.

**Exact source identity.** The full physical coefficient on the AB word is

    F(x,y) = sum_(S subset V, |S| even)
               a_S(x_S) b_S(y_S) product_(u outside S) delta(x_u,y_u).  (1)

To prove this, consider a component whose leaves all have color y. Its two
leaves other than the color-y leaf cannot cross: any crossing entry at
the color-c leaf has color c at that endpoint. These two leaves must use
their unique protected M_y edge, of weight one. The remaining center and
color-y leaf either use their protected edge, requiring x=y, or both
cross. There are no crossing center-leaf edges. Thus crossed centers have
a perfect matching and crossed selected leaves have a perfect matching
on the same set S of components. This requires |S| even, but the two
matchings need not coincide. Conversely every pair of these matchings
and the forced protected edges is one supported physical perfect matching.
Their weights give exactly (1). This accounts for every term, including
all unequal center/leaf matching interference.

A full GHZ witness would require, on every AB word,

    F(x,y) = sum_(c=0)^2 product_u delta(x_u,c) delta(y_u,c).            (2)

Equivalently, on the 3^k by 3^k matrix with row x and column y,

    F = sum_(S even) (a_S b_S^T) tensor I_(V outside S),
    target = sum_(c=0)^2 |c...c><c...c|.                               (3)

Tensor factors in (3) keep the original component order. All transpose
and pairing operations are complex bilinear; no complex conjugation,
positivity, numerical approximation or genericity assumption is used.

## Orthogonal contractions remove every proper crossing set

Choose r_u,s_u in C^3 at each component and contract F against
product_u r_u[x_u] s_u[y_u]. By (1), the contribution of S is

    A_S(r) B_S(s) product_(u outside S) (r_u dot s_u),                  (4)

where A_S and B_S are the contractions of a_S and b_S on their own
components. If r_u dot s_u=0 for every u, every proper S vanishes.

If k is odd, no S=V term exists, and this contraction of the source is
zero. If k is even, it equals just

    A_V(r) B_V(s).                                                     (5)

The target contraction from (2), on the same inputs, is

    D(r,s) = sum_(c=0)^2 product_u r_u[c] s_u[c].                      (6)

These identities hold without requiring any surviving factor in (5)
to be nonzero and without division by an edge, hafnian or parameter.

## Odd k: a scalar contradiction

For odd k>=3, take at every component

    r=(1,1,1),    s=(1,1,-2).

All local dot products vanish. The source contraction is zero, while

    D(r,s)=2+(-2)^k != 0.                                              (7)

This proves exclusion for odd k. In fact this part needs only the
component-constant equations: weight each such word x by
product_u h[x_u], h=(1,1,-2), in the diagonal version of (1). Every proper
S disappears because sum_c h[c]=0, and every S is proper when k is odd.
The target again gives (7). Thus odd-k CSQ4 is excluded by this simpler
diagonal argument. It does not assert anything about even-k CSQ4.

## Even k: a two-by-two rank contradiction

Let k>=2 be even and distinguish components 1 and 2. Choose two global
center contractions r^(1),r^(2), and two global leaf contractions
s^(1),s^(2), as follows:

| component | r^(1) | r^(2) | s^(1) | s^(2) |
| --- | --- | --- | --- | --- |
| 1 | (1,-1,0) | (1,0,-1) | (1,1,1) | (1,1,1) |
| 2 | (1,1,1) | (1,1,1) | (1,-1,0) | (1,0,-1) |
| every u>=3 | (1,1,1) | (1,1,1) | (1,1,-2) | (1,1,-2) |

For every component u and every pair i,j in {1,2},

    r_u^(i) dot s_u^(j) = 0.                                         (8)

The four contractions of the same physical source therefore form the
outer-product matrix

    [ A_V(r^(i)) B_V(s^(j)) ]_(i,j),                                 (9)

whose determinant is zero, including if either vector is zero.
But direct evaluation of (6) gives the target matrix

    [ 2    1                  ]
    [ 1    1+2^(k-2)         ],                                      (10)

with determinant 1+2^(k-1), a nonzero integer over C. The four full target
equations cannot hold simultaneously. This proves exclusion for every
even k>=2, completing the claimed all-order common-star exclusion.

For k=1 the construction is the protected K4 itself and realizes the
ternary target. The odd contraction is then 2-2=0, and the even proof
cannot choose two distinct components. This required sharp control is
consistent with the stated k>=2 scope.

## Dependencies and remaining global obligation

The mathematical dependency is the literal common-star support definition
and its protected unit edges. The proof derives its own exact physical
source formula and uses elementary finite linear algebra. It does not
assume S1, S2, resource alignment, a binary biclique decomposition, a
shortest cycle, external literature, or a finite exhaustive case cover.

Full global GHZ supplies (2) for a witness in this family. The theorem
excludes that entire family directly. It does not turn either FB or
even-k CSQ4 into a proved proposition; their smaller antecedents omit
some physical AB words used in (8)--(10). Earlier exact proper-subsystem
controls are consistent with this result because they already fail some
full physical targets.

Arbitrary hollow protected arrays may have center-leaf crossing edges,
or crossing entries at a physical leaf with another endpoint color.
Those destroy the forced protected leaf pair used in (1). No existing
normal-form theorem eliminating those terms is assumed. The remaining
global-facing problem is to obtain an analogous exact source separator
from arbitrary witnesses, or retain and control its additional crossing
contributions. Merely setting them to zero would restrict the family.

## Verification boundary

The universal proof is (1)--(10). The
[primary companion](verify_common_star_full_source_exclusion.py) checks
finite literal physical expansions, the contractions and sharp controls.
The [independent audit](audit_common_star_full_source_exclusion.py) uses
a separately implemented exact physical-matching route and does not
import the primary scientific code. The
[scientific tests](../../tests/test_common_star_full_source_exclusion.py)
include mutations of the support and contraction assumptions.

These exact computations corroborate the expansion and arithmetic; they
do not supply the arbitrary-order quantifier. Independent here means a
separate agent and implementation in the same research session, not
independent human refereeing. No external theorem, solver certificate or
formal proof-assistant result is imported.
