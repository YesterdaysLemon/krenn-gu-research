# Full binary targets localize induced cycles to one state resource

## Status, supply, and boundary

**Proved by direct argument over C; independently reviewed.** This is a
necessary-condition theorem for the full binary component targets of the
[common-star construction](PROTECTED_SCAFFOLD_COMMON_STAR_COMPONENT_TARGET_OBSTRUCTION.md)
(PSCS), not a proof of its open parent FB or of Krenn--Gu. The global
conjecture remains **UNRESOLVED**. There is no Lean formalization.

The result replaces the complete-biclique hypothesis of an earlier consumer
by a weaker condition on which physical components occur in each state
resource. More generally it confines every proper induced directed cycle
to one resource and derives all its proper exterior contractions. An exact
20-vertex control shows that the remaining full-cycle cancellation is
possible when only one face of the binary target is imposed.

## Definitions and actual source

Use k >= 2 protected unit K4 components, with one unequal endpoint-color
label on each edge of a simple component graph and two nonzero complex
factors on each gadget, as specified in PSCS. Fix distinct colors a,b.
Write A_uv,B_uv for the center and leaf factors with label (a at u,b at v),
and put q_uv=A_uv B_uv. All three are zero when that label is absent.
Thus A and B have the same support, zero diagonal, and A_uv A_vu=0.

Let D have arc u->v exactly when q_uv is nonzero. Let H be its bipartite
state graph: left state (u,a), right state (v,b), with the same arcs as
undirected edges. A **resource** means a connected component of H. Write
L_R and M_R for the physical indices on its left and right shores.
These sets can overlap: the two states of a physical component may lie
in the same resource without being adjacent. No disjointness is assumed.

For arbitrary row and column index sets W,T define

```
Z(W,T) = sum_(I subset W, J subset T, |I|=|J|)
                    per(A[I,J]) per(B[I,J]).                 (1)
```

The empty term is one. These are actual factors of the same source, not
independent cofactors. A word with a on S and b on its complement has
source F(S)=Z(S,S^c). This follows from the PSCS double-hafnian source:
every compatible matching alternates between the two color shores.
The **full binary target** is F(empty)=F(V)=1 and F(S)=0 for every
nonempty proper S. It automatically gives both constant coefficients one
in this protected construction.

If precisely T is changed from a to b, the source factors as

```
F(V\T) = product_R Z(L_R\T, M_R intersect T).               (2)
```

Indeed each physical component selects just one state; its forced internal
edges contribute one, and its selected state belongs to only one resource.
The independent center and leaf matchings therefore split over these
disjoint selected-state graphs. This does not discard an exterior term.

## Exact matching-row deletion

If x is not in W and has exactly one supported entry among columns T,
at y, then

```
Z(W union {x},T) = Z(W,T) + q_xy Z(W,T\{y}).                 (3)
```

Both permanent factors either omit row x or include it in their common
row set. In the latter case both must use column y at that row. This
extracts A_xy B_xy and leaves the two smaller actual permanents.
For several such rows P whose unique columns phi(x) are distinct,

```
Z(W union P,T) = sum_(K subset P) q_K Z(W,T\phi(K)),
q_K = product_(x in K) q_(x,phi(x)).                         (4)
```

The restriction to one selected column per added row is essential.

## Theorem: localization of a proper induced directed cycle

Assume the full binary target. Let C be a proper induced directed cycle
of D, with predecessor map pred. Induced means that the only arcs whose
two endpoints lie in C are its cycle arcs. Then one resource R contains
both (u,a) and (u,b) for every u in C.

More precisely, put U=L_R\C and q_y=q_(pred(y),y). In that resource,

```
Z(U,T) = (-1)^|T| product_(y in T) q_y   for T proper in C,
Z(U,C) = 0.                                                 (5)
```

Every q_y is nonzero. The empty proper subset in (5) has value one.

### Proof

For each resource let X_R=C intersect L_R, Y_R=C intersect M_R, and
U_R=L_R\X_R. Each cycle arc is an edge of one resource. Consequently
pred maps Y_R bijectively to X_R, and the submatrices on X_R by Y_R
have exactly the corresponding matching entries.

Fix T subset Y_R and recolor exactly its physical components from a to b.
Only R gains right states. Every other resource has no selected right
state and contributes one, even when some of its left states disappear.
For nonempty T, the full target gives

```
Z(L_R\T,T)=0,                                               (6)
```

because T subset C and C is proper. Relative to U_R, the only remaining
cycle rows with a supported entry into T are

```
P_T={pred(y) : y in T, pred(y) notin T}.                     (7)
```

Each meets just its successor column in T. All other remaining cycle
rows can be omitted from (1), since they have no supported entry into T.
Applying (4) to (6) gives

```
0 = sum_(K subset P_T) q_K Z(U_R,T\phi(K)).                  (8)
```

For every nonempty proper subset T of the cyclic vertex set C, P_T is
nonempty. Induction on |T| in (8) therefore proves

```
Z(U_R,T)=(-1)^|T| product_(y in T) q_y                       (9)
```

for every T subset Y_R that is proper in C. Explicitly, after substituting
the smaller cases, each term has the same nonzero product of all q_y in T;
the signs sum to (1-1)^|P_T|=0. The K=empty term then has exactly the value
in (9). No division by an exterior source or determinant occurs.

For the word changing all of C to b, (2) becomes

```
F(V\C)=product_R Z(U_R,Y_R).                                (10)
```

If every nonempty Y_R is proper in C, (9) makes every factor nonzero;
empty Y_R contributes one. This contradicts the mixed target. Therefore
Y_R=C for one R. The predecessor bijection also gives X_R=C. Equations
(9) and (6), now for this R, are exactly (5). QED.

## Corollary: classification when states never return to one resource

Suppose L_R intersect M_R is empty for every resource. Then the full
binary target holds **if and only if** D is one directed Hamilton cycle
and all its gadget products are -1.

For necessity, full cuts first force D to be strongly connected: a
nonempty proper set with no outgoing arc has source one, contradicting
the target. A shortest directed cycle is induced, since any additional
arc between its vertices gives a shorter cycle. The theorem forbids a
proper induced cycle under the disjoint-shore hypothesis. Thus a shortest
cycle is Hamiltonian. Any additional arc is then a chord and again gives
a shorter directed cycle, so D consists exactly of that Hamilton cycle.
Singleton targets fix each unique outgoing product to -1.

Conversely, in a directed cycle a compatible a/b cut consists of disjoint
arcs. A proper nonempty cut has at least one such arc. Its source is the
product of their factors (1+q)=0, while both constants give one. An
oriented cycle has length at least three under the one-label convention;
k=2 has no such realization.

S1 and both types of three-color S2 exclude every singleton port by the
proved PSCS argument. Hence FB's full antecedent excludes any color pair
whose binary resources have disjoint physical shores. Complete bicliques
are a special case, since a shared physical index in a complete biclique
would require a forbidden diagonal entry. Completeness is not needed here.

For a putative FB array, every color pair has minimum indegree and
outdegree at least two. Its shortest directed cycle must be proper:
a Hamiltonian shortest cycle with any extra arc would have a shorter
cycle. Thus every pair supplies an internal cycle with exactly the
exterior constraints (5). This is the new necessary reduction; its
remaining internal-cycle cancellation has not been excluded.

## Sharp exact control: the full-cycle defect survives one binary face

Use five physical components. Put s=(-3+sqrt(-3))/6, q=-1-s, w=s/2, so
3s^2+3s+1=0. All are nonzero. Give every gadget below label (0,1) in the
displayed orientation, center factor one, and the stated leaf factor:

```
0->1, 1->2, 2->0 : q;
3->0, 3->1, 3->2, 4->0, 4->1, 4->2 : w.                  (11)
```

There is one label per component pair, no opposite arc and no loop, so
this defines a literal common-star array on 20 physical vertices.
Let C={0,1,2}, U={3,4}. With t selected columns of C, the exterior source is

```
Z(U,T)=1+2 t w+4 binom(t,2) w^2.                           (12)
```

For t=0,1,2 these values are respectively 1,-q,q^2. For t=3 the value is
1+3s+3s^2=0. Formula (4) now gives amplitude one on 00000 and zero on each
of the other seven binary words whose last two components stay 0.
Thus the proper contractions in (5) and its zero full-cycle value are
simultaneously realizable with actual shared factors.

This is **not** an FB array: the mixed word 00010 has amplitude one,
because no gadget points to component 3. It also lacks the other-color
singleton supply. The construction refutes the proposed closure that the
localized cycle-face equations alone force its top amplitude nonzero.
Targets that change the exterior components remain load-bearing.

Equivalently, if E_K is the sum of the two permanent products in (1)
with the column set fixed to K, the local equations force

```
E_K = product_(y in K)(-1-q_y)                for K proper in C,
E_C = product_(y in C)(-1-q_y) - (-1)^|C| product_(y in C)q_y. (13)
```

This is Boolean subset inversion of (5), not a new assumption. In the
three-cycle control E_C=0 because U has only two rows, while the cubic
defect E_C-s^3=q^3 is nonzero. Replacing the permanent products by
factorized first moments would erase this permitted cancellation.

## The face-only obstruction persists at every cycle length

For every r >= 3 there is a legal array on 2r-1 components, hence 8r-4
physical vertices, with an induced r-cycle C, for which every binary word
on C has the correct full coefficient when all exterior components stay a.
An exterior singleton change still has amplitude one. Thus no cycle-length
bound repairs a proof using just this face.

Choose a nontrivial r-th root of unity rho and put

```
s=1/(rho-1),       q=-1-s,       1+s=rho*s.                 (14)
```

There are r-1 nonzero complex numbers w_1,...,w_(r-1) with elementary
symmetric functions

```
e_m(w)=s^m/(m!)^2,                 0 <= m <= r-1.          (15)
```

Indeed take the roots, with multiplicity, of the monic polynomial

```
P(z)=sum_(m=0)^(r-1) (-1)^m s^m z^(r-1-m)/(m!)^2.
```

Its constant coefficient is nonzero, so no root is zero. All factors are
algebraic complex numbers; distinct roots are not required.

Give the cycle arcs center factor one and leaf factor q. Add r-1 outside
components u_i and all arcs u_i->y, y in C, with center factor one and leaf
factor w_i. Every arc has label (a,b). There are no other gadgets. This is
a simple one-label construction. For any fixed m-column subset K of C,
each m-row subset has center permanent m! and leaf permanent m! times its
row-weight product. Therefore its exact fixed-column contraction is

```
E_K=(m!)^2 e_m(w)=s^m     (m<r),       E_C=0.              (16)
```

It follows that Z(U,T)=(1+s)^|T|=(-q)^|T| for proper T subset C, while

```
Z(U,C)=(1+s)^r-s^r=(rho^r-1)s^r=0.                       (17)
```

For a nonempty proper T subset C, expand the surviving cycle rows by
(4). Its incoming cycle boundary is nonempty, so the signs cancel just
as in (8)--(9); its full physical amplitude is zero. For T=C use (17);
for T empty the amplitude is one. This proves all 2^r face equations,
with no enumeration or free-cofactor substitution. An outside component
has no incoming gadget, so changing only that component to b leaves the
unique protected matching with amplitude one.

For r=3, take s=(-3+sqrt(-3))/6. The polynomial P has the two equal roots
s/2, recovering (11). This family is a countercontrol to **face-only
closure**, not to full binary feasibility, FB, CSQ4, or Krenn--Gu.

## Evidence and next obligation

The [primary replay](verify_common_star_binary_cycle_localization.py)
checks symbolic deletion, the exact control, the squared-factorial moment
normalization and root-of-unity identity, and the directed-cycle sharp case.
Finite replay corroborates displayed identities; the arbitrary-order proofs
are the arguments above. The
[independent audit](audit_common_star_binary_cycle_localization.py) uses
standard-library quadratic-field arithmetic and literal physical-vertex
matching recursion, imports no primary or project scientific module, and
checks the finite control, subset contractions and sharp cycles separately.
The [review](../../docs/audits/COMMON_STAR_BINARY_CYCLE_LOCALIZATION_REVIEW_2026-09-20.md)
audits the written all-order proof and all-length control and pins the files
it inspected. This is separate-agent review in the same research session,
not separate-human refereeing or Lean kernel verification.

The [resumed parent attempt](../../docs/strategy/full-binary-parent-attempt-2026-09-20.md)
records FB, upstream CSQ4 supply and the named consumer. The next necessary
step is to combine (5) in both binary orientations with targets that change
the exterior, and with the third-color S2 coupling. No proof that those
additional requirements contradict (5) is supplied. General FB, CSQ4,
arbitrary protected fillings, and the global conjecture remain open.
