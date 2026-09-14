# Protected-scaffold minority cycles and exterior resource boundary

## Status and scope

The statements below have written combinatorial proofs over **C**, for every
protected scaffold on n=4k vertices, k>=1. The finite rational control is
replayed by a standalone exact verifier. The written arguments passed an
[independent proof review](../../docs/audits/PROTECTED_SCAFFOLD_SOURCE_REVIEW_2026-09-14.md).
No Lean formalization is supplied.

This document characterizes a homogeneous subsystem of actual source
equations and proves an exact formula for the exterior contributions to
other source slices. It does **not** exclude the protected scaffold at
arbitrary order, assert that the homogeneous subsystem implies the full
source, or transfer an eight-vertex exclusion to larger orders. The explicit
twelve-vertex array is a control against such a transfer, not a Krenn--Gu
counterexample. The global conjecture remains **UNRESOLVED**.

The upstream family is the
[pure-matching scaffold](PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_THEOREM.md).
That owner's generic maximum-root-five assertion requires k>=5. No generic
root assertion is used here; the present statements concern every filling
of the specified scaffold, including exceptional complex fillings.

## Definitions

Partition the vertices into k labelled four-vertex components. On each
component use local labels 0,1,2,3 and the perfect matchings

```
M_0={01,23},   M_1={02,13},   M_2={03,12}.
```

Write M_c also for their union over the components, and p_c for its partner
involution. On a physical edge in M_c set the entire color matrix to E_cc.
Every edge between different components has an arbitrary hollow 3-by-3
complex matrix. Orient matrices consistently, with
W_ji[b,a]=W_ij[a,b]. Thus the scalar support at constant color c is exactly
M_c, with every edge weight one.

For a color word a, T_W(a) is the sum over all physical perfect matchings
of the products of their corresponding entries W_ij[a_i,a_j]. The target
delta(a) equals one on the three constant words and zero otherwise. All
three pure amplitudes are identically one on this family.

A set R is **M_c-independent** if it contains at most one endpoint from
every edge of M_c. This is independence relative to one perfect matching,
not independence in the complete physical graph.

## Theorem 1: exact minority permanent and cycle criterion

Fix c and an M_c-independent set R. Give each v in R an arbitrary color
d_v different from c, and every other vertex color c. Define the matrix
indexed by R by

```
H_vw = W_(v,p_c(w))[d_v,c].                            (1)
```

Then the full physical source coefficient is exactly

```
T_W(a) = per(H).                                       (2)
```

The empty permanent is one. For nonempty R the target is zero.

Define a directed graph D_c on the physical vertices by putting v -> w
when W_(v,p_c(w))[d,c] is nonzero for at least one d different from c.
The following conditions are equivalent:

1. Every mixed source equation (2) holds, for every M_c-independent R and
   every assignment of its minority colors.
2. D_c contains no directed cycle whose vertex set is M_c-independent.

### Proof of the permanent formula

Each v in R has a distinct partner p_c(v) outside R. That partner has
color c and has lost its only possible c-to-c mate, because v has color
d_v != c. Every such exposed partner must therefore match a minority
vertex. There are exactly |R| exposed partners and |R| minorities, so these
matches consume all minority vertices. No minority can match another
minority or any other vertex. Every remaining edge of M_c is then forced,
with weight one.

The remaining choice is exactly a bijection from R to p_c(R); its weight
is the corresponding permanent term in (1). This proves (2), without an
independent cofactor or an assumption that exterior entries vanish. The
diagonal of H is zero, since W_(v,p_c(v))=E_cc.

### Proof of the cycle criterion

If condition 2 holds, a nonzero permanent term on a nonempty R would give
a directed cycle cover of R. Each constituent cycle has an M_c-independent
vertex set and is forbidden. Hence every term vanishes.

Conversely, suppose D_c has an M_c-independent directed cycle, and choose
one of shortest length. Any arc among its vertices other than a successor
arc would form a shorter directed cycle by following the original cycle
back to its initial vertex. Its vertex set is still M_c-independent, a
contradiction. Loops are absent because the diagonal entries in (1) vanish.
Thus the induced directed graph on this cycle's vertices has exactly its
successor arcs. At each vertex choose d_v to make its successor entry
nonzero. The permanent in (2) has exactly one nonzero term, the product of
the cycle entries. Over C this product is nonzero, contrary to condition 1.
This proves the equivalence.

### Two-minority corollary

For vertices u,v in different components, put colors d,e != c there and
color every other vertex c. Formula (2) reduces to

```
T_W(a)=W_(u,p_c(v))[d,c] W_(p_c(u),v)[c,e].           (3)
```

Consequently the full source requires this product to vanish. This holds
for every k, with no exterior correction. Taking d=e gives a binary
condition. Taking d,e distinct couples all three colors. For two fixed
components, the latter cases give 96 indexed product equations, before
identifying any coincident polynomials.

All conditions in Theorem 1 are homogeneous and hold at zero hollow
filling. At k>=2 that filling fails mixed component-constant targets. The
theorem therefore does not by itself exclude the scaffold.

## Theorem 2: the exact exterior resource expansion

Let S be a union of complete components, fix a color word a on S, and
color every vertex outside S by c. Let E be the set of M_c edges outside S.
For e={u,v} in E and distinct i,j in S put

```
K^e_ij = W_iu[a_i,c] W_jv[a_j,c]
       + W_iv[a_i,c] W_ju[a_j,c].                    (4)
```

For a partial matching F on S, let V(F) be its endpoint set. Then

```
T_W(a,c_outside)
 = sum_(F partial matching on S) sum_(phi:F -> E injective)
     haf(W[a] restricted to S minus V(F))
       * product_(ij in F) K^(phi(ij))_ij.            (5)
```

The empty injection is included, and the hafnian of the empty matrix is
one. All cofactors in (5) are the actual induced physical hafnians.

### Proof

The outside vertices have color c and their scalar matching support is
precisely the disjoint matching E. Each edge e={u,v} either remains
internally matched with weight one, or has both endpoints matched to two
distinct vertices i,j in S. It cannot have only one endpoint matched into
S: the other endpoint would have no available outside mate. It cannot
supply two different boundary pairs. The two possible attachments to i,j
have total weight (4).

Different consumed outside edges give disjoint boundary pairs and an
injective assignment of these pairs to resources in E. After removing the
boundary endpoints, the remaining vertices of S carry their literal
induced physical matching sum. Conversely, every term described in (5)
constructs exactly these full matchings. This proves the formula.

One equivalent notation uses the commutative algebra
C[t_e:e in E]/(t_e^2:e in E). Form the hafnian on S with entries

```
W_ij[a_i,a_j] + sum_e t_e K^e_ij,
```

and apply the linear functional taking each squarefree resource monomial
to one. This functional is not substitution t_e=1 as a ring homomorphism.
An ordinary hafnian of W+sum_e K^e would incorrectly permit repeated use
of one exterior edge. The effective K terms can also change edges within
a protected K4 and introduce same-color entries, so an ordinary effective
matrix need not belong to the original scaffold parameter space.

When S contains the minority set R, Theorem 1 is the special case in which
its exposed-partner count makes every nonempty F in (5) impossible. Its
direct proof also applies to R spread across arbitrarily many components.

### Two concrete source boundaries

Put the only two minorities at the endpoints x,p_c(x) of an M_c edge in
one component A, with both colors different from c. Their direct internal
edge is zero. Formula (5) gives the full equation

```
sum_(e in M_c outside A) K^e_(x,p_c(x)) = 0.          (6)
```

At k=2 this involves one other component. For larger k it permits
cancellation between components and does not imply that each component's
summand vanishes.

Next color all four vertices of A by d != c and all others by c. Write
{r,s},{t,u} for the M_d edges on A. The complete source equation is

```
0 = 1 + sum_e (K^e_rs + K^e_tu)
      + sum_(e<f) sum_(I subset A, |I|=2) K^e_I K^f_(A minus I). (7)
```

Here e,f run over M_c outside A, an arbitrary total order defines e<f,
and K^e_I denotes (4) on the unordered two-set I. The six choices of I
assign one boundary pair to e and its complement to f. The constant one
is the protected M_d matching on A and M_c outside. Thus equations with
nonzero constant terms retain actual shared exterior resources; they are
not supplied by the homogeneous cycle criterion.

## Theorem 3: an exact boundary control at n=12

Let A={0,1,2,3}, B={4,5,6,7}, C={8,9,10,11}, with the protected internal
arrays as above. Set only these two crossing entries nonzero:

```
W_04[1,0]=1,   W_25[1,0]=-1.                         (8)
```

Then every equation in Theorem 1 holds for every majority color, every
independent minority set, and every assignment of its minority colors.
Nevertheless

```
T_W(111100000000)=0,
T_(W restricted to A union C)(11110000)=1.             (9)
```

The full source is not GHZ: T_W(222200000000)=1. All pure amplitudes remain
one.

### Proof

In D_0 all arcs run from A to B; in D_1 all arcs run from B to A; D_2 is
empty. Each directed graph is acyclic, so Theorem 1 proves the stated
homogeneous equations.

For the first word in (9), there are exactly two nonzero physical matching
terms. The protected matching contributes one. Using both crossings in
(8) replaces the M_1 pair {0,2} in A and the M_0 pair {4,5} in B, while
all remaining protected pairs stay internal; its contribution is minus
one. These cancel. On A union C there are no crossings at all, so the
same mixed component assignment has its single protected term of weight
one. For 222200000000 neither crossing in (8) is available, again leaving
one protected term. Pure normalization follows from the scaffold itself.

This control proves that the complete homogeneous localized subsystem
does not justify discarding exterior resources from a two-component slice.
It does not refute an implication that retains all the full source
equations or all component-constant equations: it does not satisfy them.

## Replay and remaining obligation

Run

```text
python claims/arbitrary-order/verify_protected_scaffold_resource_control.py
```

The verifier independently enumerates supported physical matchings by a
recursive endpoint choice, using exact integers and no project scientific
imports. It checks 3*5^6=46,875 indexed minority assignments, including the
three pures, and the amplitudes in Theorem 3. Each M_c edge offers five
choices: no minority, or either endpoint with either non-c color.
These are parameterized evaluations, representing 46,851 distinct words:
46,827 occur once and 24 occur twice. The verifier prints its receipt and
writes no files by default. It replays the finite control; it is not an
exhaustive check over k or the proof of the
general theorems.

The unresolved larger-order step is to control simultaneous cancellation
of the constant-bearing component amplitudes through the actual shared
resources, including their relations to other source slices. Theorem 2
specifies that boundary exactly. Neither the cycle criterion nor a
separate exclusion of the two-component scaffold establishes this step.
