# Full-source extension barriers beyond the common-star exclusion

## Status, parent, and scope

**Proved mechanism obstructions over C.** The uniform-leaf AB equations
alone do not exclude arbitrary hollow protected-K4 fillings. Separately,
protected K4s with invertible intercomponent blocks admit no target-visible
cut-null separator. These statements eliminate two proposed ways of
extending [PSCF](PROTECTED_SCAFFOLD_COMMON_STAR_FULL_SOURCE_EXCLUSION.md).
They do not refute an implication that assumes the full physical source.

The global Krenn--Gu conjecture remains **UNRESOLVED**. The open parent
**SFULL** says that, for every k>=2, no arbitrary hollow filling between k
protected unit K4s realizes the full ternary GHZ tensor. Its upstream supply
would be a full witness already in this scaffold; its named consumer is
exclusion of the entire protected-scaffold construction. There is no
arbitrary-witness-to-scaffold reduction. A dedicated separate-agent
[review](../../docs/audits/PROTECTED_FULL_SOURCE_EXTENSION_REVIEW_2026-09-20.md)
records the exact evidence and its limits. No Lean formalization is supplied.

The attempted synthesis uses PSCF's orthogonal projection to isolate a
rank-one part, and the protected scaffold's exact pure matchings and
coordinate killers to seek a global factorizing cut. The controls below
show why neither synthesis follows from those premises. These are parent
route obstructions, not new bounded-degree refinements of the closed
common-star branch.

## 1. Exact arbitrary-filling expansion

Each component has vertices 0,1,2,3, with protected matchings
M_0={01,23}, M_1={02,13}, M_2={03,12}. An edge in M_c has its entire
color block equal to E_cc. Every intercomponent physical block is an
arbitrary hollow 3-by-3 complex matrix, with reversal given by transpose.

In an AB word, the component center has color x_u and its three leaves
have color y_u. In a physical perfect matching pi, let d_u be the number
of vertices matched outside component u. Then d_u is 0,2, or 4. Define
kappa_u(v)=x_u at the center and y_u at a leaf. The local compatibility
factor chi_u is:

- d_u=0: the fixed internal matching M_c contributes
  delta(x_u,c) delta(y_u,c);
- d_u=2 with the internal edge joining two leaves (type AB):
  delta(y_u,c), where that protected edge belongs to M_c;
- d_u=2 with the internal edge joining center and leaf (type BB):
  delta(x_u,c) delta(y_u,c);
- d_u=4: one.

For any center and leaf covectors r_u^p,s_u^q the literal projection is

    S_pq = sum_pi sum_(x,y) product_u r_u^p[x_u] s_u^q[y_u] chi_u^pi(x_u,y_u)
                   product_(crossing vw in pi) W_vw[kappa(v),kappa(w)].       (1)

Every edge factor belongs to the same physical array. If r_u^p dot s_u^q=0,
the terms with d_u=0 cancel after grouping the three possible internal
matchings while holding the exterior fixed. One fixed M_c contributes
r_u^p[c]s_u^q[c]; it must not be assigned the grouped dot product.

After this cancellation, the terms with every component of type AB and
every crossing center-center or leaf-leaf factor into A(r^p)B(s^q). The
centers form one matching, and the selected leaves form an independent
matching on the same components. The remaining source is

    S = A B^T + E,                                                      (2)

where E contains mixed center-leaf routing, BB components, and components
of degree four. Unlike PSCF, arbitrary hollow fillings do not force E=0.

## 2. Exact AB control with nonzero split-leaf sources

Use the committed n=8 fixture
[`eight_vertex_scaffold_subsystem_controls.json`](../../tests/fixtures/eight_vertex_scaffold_subsystem_controls.json).
In family `binary_and_monochromatic_shores_v2`, the two crossing positions
for each ordered unequal color pair are:

    01: (2,3),(3,1)       02: (0,3),(1,0)
    10: (1,2),(3,3)       12: (0,2),(2,1)
    20: (1,1),(2,0)       21: (0,0),(3,2).

The positions are local vertices on the left and right K4. Give the first
entry weight r_cd and the second -r_cd^(-1), for six arbitrary nonzero
complex parameters. All other crossing entries vanish.

For every one of the 81 words

    (x_0,y_0,y_0,y_0,x_1,y_1,y_1,y_1),

the physical coefficient equals its full GHZ target as an identity in
Z[r_01^(+/-1),r_02^(+/-1),r_10^(+/-1),r_12^(+/-1),r_20^(+/-1),r_21^(+/-1)].
This finite assertion is established by enumerating all 105 physical
perfect matchings, accepting a monomial exactly when every protected
endpoint color and crossing support agree, and collecting integer Laurent
coefficients. The primary replay first constructs the general 96-variable
projection and specializes; the independent audit reconstructs each
fixture's literal source directly without importing the primary.

Therefore all linear AB probes already have their target values. For the
four PSCF probes at k=2, the source is [[2,1],[1,2]], of determinant three.
At r_cd=1 its decomposition is:

| Matching class | Projected matrix |
| --- | --- |
| Separated AB | [[0,0],[-1,0]] |
| BB left, AB right | [[0,0],[1,1]] |
| BB at both | [[2,1],[1,0]] |
| Mixed center-leaf AB | [[0,1],[0,1]] |
| AB left, BB right | [[0,-1],[0,0]] |
| Degree four | [[0,0],[0,0]] |

The BB-BB part alone has determinant -1. The sum E is [[2,1],[2,2]], so
degree-four terms are not needed to repair the common-star rank defect.

This is not a full witness. The following zero-target words have exactly
one supported matching:

    00020011: (01)(27)(36)(45), coefficient -r_01/r_21;
    01000002: (07)(16)(23)(45), coefficient  r_02 r_10.

Both coefficients are nonzero at every allowed specialization. The first
detects split-colored BB-BB leaves; the second detects an AB-BB transfer
through center-leaf crossings. The companion committed family
`independent_minorities_and_component_constants_v3` also satisfies all 81
AB words, but has the unique split-word coefficient

    00010221: (01)(27)(34)(56), coefficient -r_01/r_10.

Consequently the implication "protected hollow filling + all AB equations
implies a rank-one four-probe source" is false. The full-source parent
SFULL remains open. These controls do not contradict the existing complete
k=2 exclusion because each fails full physical equations explicitly.

## 3. A global cut-null obstruction

For a nontrivial partition of the physical vertices into shores L and R,
give each i in L two covectors r_i^0,r_i^1 and each j in R two covectors
s_j^0,s_j^1. A cut-null datum satisfies

    (r_i^p)^T W_ij s_j^q = 0  for all i,j,p,q across the cut.             (3)

Define R_pc=product_(i in L) r_i^p[c] and
Q_qc=product_(j in R) s_j^q[c]. Its target matrix is D=R Q^T. Call the
datum target-visible when det D is nonzero. All pairings are bilinear,
without complex conjugation.

For a full GHZ source, any cut-null datum would make the source matrix an
outer product of the two shore hafnians (or zero when the shores are odd).
It would have rank at most one. Thus a target-visible cut-null datum is
a valid conditional exclusion mechanism. Its existence is a separate
obligation.

**No-cut theorem.** In any protected-K4 array for which every
intercomponent physical block is invertible, no such target-visible datum
exists.

**Proof.** If a protected color-c edge ij crosses the cut, (3) gives
r_i^p[c]s_j^q[c]=0 for all p,q. Every entry of the color-c summand
R_:c Q_:c^T of D is therefore zero. Rank D=2 requires at least two nonzero
color summands, so at least two protected color matchings have no cut edge.
Their union inside each K4 is a connected four-cycle. Each whole K4 must
therefore lie on one shore.

Rank D=2 also forces both R and Q to have rank two. On each shore some
local probe span must have dimension two: if every local pair were
proportional, their products would give proportional global rows; a zero
local vector instead gives a zero global row. Choose such vertices i and
j on opposite shores. Their block W_ij is an invertible intercomponent
block. It maps the two-plane span(s_j^0,s_j^1) to a two-plane, whose
bilinear annihilator in C^3 is one-dimensional. It cannot contain the
two-plane span(r_i^0,r_i^1), contradicting (3). QED.

For an explicit rational control at every k>=2, use

    W_ij = [[0,1,1],[1,0,1],[1,1,0]]

on every intercomponent edge. Its determinant is two. The protected
coordinate killers and all three pure target amplitudes remain exact,
but there is no target-visible cut. A component-constant mixed word has
a protected matching of weight one and only nonnegative matching terms,
so its source is nonzero. This control is not a witness.

The no-cut condition also holds on a nonempty open of the
[accepted generic scaffold](PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_THEOREM.md).
Invertibility of each free hollow block defines a nonempty open, as the
displayed determinant shows. Intersect these finitely many opens with
the owner's nonempty maximum-root-five/full-outside-span open and its
nonzero mixed-coefficient open in the irreducible affine parameter space.
The intersection is nonempty. This corollary inherits k>=5 only from that
upstream generic theorem; the no-cut proof itself has no such threshold.
It retains the scaffold facts actually proved by that owner. It does not
claim that all accepted necessary conditions, in particular the full
nonzero source equations, hold on this control.

## 4. Why protected diagonal support descent freezes the needed terms

A further attempted induction assigns rational potentials h_(v,c), with
h_(v,c)+h_(w,c)=0 on each protected color-c edge. Scale a crossing entry
W_vw[a,b] by t^(h_(v,a)+h_(w,b)). If every supported crossing exponent is
nonnegative, the t-to-zero limit is finite and fixes the protected entries.
Every physical coefficient is homogeneous of exponent
sum_v h_(v,alpha_v). Global constant words have exponent zero, so such a
limit preserves the full target and deletes every positive-exponent entry.

It does not follow that the full equations supply a support-reducing
potential. In fact, all terms used to cancel component-constant targets
are frozen entry by entry under every such potential.

**Frozen-core lemma.** Let alpha be any component-constant word and M any
supported matching for it. Its total exponent is sum_v h_(v,alpha_v).
Compute that same sum using alpha's unique protected perfect matching:
the sum is zero. Each protected term of M has exponent zero and each
supported crossing term has nonnegative exponent. Hence every term of M
has exponent zero. All its factors retain their exact nonzero values in
the limit. This applies to every subsequent admissible degeneration as
well: the original matching and protected comparison remain present.

Let E_fr be the union of crossing entries over all supported matchings for
component-constant words. Every admissible degeneration fixes E_fr
pointwise, and every finite sequence retains it. If k>=2 and even one
nonuniform component-constant word has target zero, its protected matching
contributes one. At least one nonzero crossing matching is needed to
cancel it, so E_fr is nonempty. Thus no such sequence can reach zero
crossings while preserving those component-constant equations.

Equivalently, compare any matching for alpha with the protected matching.
Their symmetric difference is a vertex-disjoint union of alternating
protected/crossing cycles. Each cycle's crossing product has exponent zero.
The exact component coefficient is the sum over vertex-disjoint collections
of these cycles of their product, including the empty term one. Mixed
component targets require the nonempty products to sum to minus one;
they require nonzero invariant cancellation terms rather than erasing them.

In both n=8 controls of Section 2, all twelve crossing entries already
belong to E_fr. For each ordered unequal pair (a,b), its two supported
entries complete one matching on the word (a,a,a,a,b,b,b,b). That word
has just its protected contribution one and this crossing contribution
r_ab(-r_ab^(-1))=-1. These six two-entry matching supports cover every
crossing entry. Consequently neither control admits even one strict
support deletion by such potentials. The split-leaf failures instead
combine entries from different ordered-color pairs. Both exact companions
check this coverage as well as the AB and split-leaf coefficients.

This is a limitation of the proposed homogeneity-only proof. It is not a
counterexample to the full-source claim that some other entry can always
be deleted. A repeated-deletion proof would first need full split-component
equations to rule out a source supported on the frozen core or an equally
immovable support. That inconsistency is not supplied by diagonal scaling.

## 5. The remaining full-source transfer

Flatten the physical source with all center colors as rows and every
individual leaf color as columns. A full witness would have

    H = sum_(c=0)^2 |c^k><c^(3k)|.                                    (4)

Every column except the three globally uniform ones is zero. AB words
inspect only the columns with each component's leaf triple uniform.
The exact controls above prove that other columns carry essential
constraints.

Adding split-leaf zero-column equations does not termwise erase the BB
contribution while preserving the target. A local leaf tensor L with the
same diagonal as the AB tensor has L[c,c,c]=s[c]. For a BB component whose
internal center-leaf edge has color c, the slice on its two crossed leaves
still contains that diagonal value. Killing every BB slice would force
s[c]=0 and lose that target color. Any successful cancellation must use
relations between products of the same physical edge factors.

The sharply stated sufficient implication is:

> For every k>=2 and every arbitrary hollow protected filling satisfying
> all AB targets, the same factors force a nonzero coefficient in at least
> one nonuniform leaf column.

This is open at arbitrary order. The explicit n=8 detectors do not prove
it for larger k: exterior components can add matchings in the same column
and cancel the local contribution. Nor does the cut-null theorem refute
the different proposed implication "full GHZ source implies a
target-visible cut"; its controls fail the full source.

The proof-topology delta is two exact mechanism exclusions and a frozen-core
obstruction to homogeneity-only support descent, with full mixed-source
cancellation consistency isolated as the missing supply.
No full-witness branch beyond PSCF has been closed.

## Replay

    python claims/arbitrary-order/verify_protected_full_source_extension.py
    python claims/arbitrary-order/audit_protected_full_source_extension.py

These standard-library companions exhaust the declared n=8 AB controls and
check the finite cut combinatorics. The arbitrary-order no-cut statement
rests on the written proof, not finite extrapolation. The generic corollary
uses the explicitly linked scaffold theorem; its upstream chain is not
re-audited here.
