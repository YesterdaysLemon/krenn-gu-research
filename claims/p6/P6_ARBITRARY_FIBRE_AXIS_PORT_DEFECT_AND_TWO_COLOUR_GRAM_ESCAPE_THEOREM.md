# P6 arbitrary-fibre axis port defect and two-colour Gram escape theorem

## Status

**Exact characteristic-zero escape from the canonical axis no-go, with a
sharp residual boundary.**  This note replaces the canonical scalar section
by an arbitrary point of the split-surjective six-face scalar fibre and
identifies the invariant which exactly controls whether the 5+1 axis kernel
has support on the four-window.

For two colours c,d, let M_(c,d) be the combined 72 by 56 axis operator and
let M^C_(c,d) be its restriction to the twelve directed core-core columns.
The **axis port defect**

~~~text
delta_(c,d) = 44 - rank M_(c,d) + rank M^C_(c,d)                 (1)
~~~

is exactly the dimension of the projection of ker M_(c,d) onto the
forty-four directed columns incident to the four-window.  Thus port-supported
axis directions exist if and only if delta_(c,d)>0.  This criterion is valid
at every point of the scalar fibre; it is not tied to a section formula.

The canonical nonzero-tau section has

~~~text
(rank M, rank M^C, delta) = (51,7,0).                             (2)
~~~

There is, however, an exact coordinate-boundary section with the same six
prescribed pure Segre columns for which

~~~text
(rank M, rank M^C, delta) = (19,7,32).                            (3)
~~~

Its thirty-two directed core-window coordinates are completely free in the
axis kernel.  Consequently the preceding canonical-section obstruction
cannot be generalized from the six pure face values alone.

The escape is substantive beyond the linear layer.  Over an algebraically
closed characteristic-zero field, one can choose those core-window
off-diagonal entries by exact symmetric-form congruence so that:

- every 5+1 mixed coefficient vanishes; and
- every 4+2 coefficient whose two minority-coloured vertices are the two
  window ports vanishes.

The earlier forced coefficient 3 b_pq is therefore not fibre-invariant.
This does **not** solve the complete two-colour problem.  A 4+2 word whose
minority vertices consist of one core vertex and one window vertex has the
new residual

~~~text
Y_(i,q) (D X)_(i,p).                                             (4)
~~~

For the nonsingular Gram completions constructed here, all such residuals
cannot vanish: that would force a multiplicative complementary-product
identity contradicted by every one of the three exact face columns.
Singular Gram completions, the remaining 4+2 placements, and all genuinely
three-colour equations remain open.

No graph, colour-word, support, parameter-tuple, or finite-field search is
used.  The construction is a symbolic fibre specialization, exact linear
algebra, and a congruence theorem for nondegenerate symmetric forms.

## 1. Scalar fibre and arbitrary axis operator

Let

~~~text
C={0,1,2,3},                    W={4,5,6,7},                      (5)
S_pq=C union {p,q},             p<q in W.
~~~

For each colour c, let A^(c) be an arbitrary scalar weighted graph satisfying

~~~text
haf A^(c)[S_pq]=y_pq^(c)        for all p<q in W.                 (6)
~~~

If the fixed pure-core H4 sensor is retained, one may additionally impose
haf A^(c)[C]=3.  The port-defect criterion below does not use that
normalization and applies to the full six-face fibre.

The exact columns, in pair order 45,46,47,56,57,67, are

~~~text
y^(0)=(14,-24,20,15,-29,9),
y^(1)=(10,-33,36,30,-58,18),
y^(2)=(2,38,-45,-30,73,-23).                                  (7)
~~~

For distinct colours c,d, write x_vu for the edge-block entry in which
vertex v has the singleton colour d and its partner u has majority colour c.
On S_pq the complete 5+1 coefficient is

~~~text
sum_(u in S_pq minus {v})
  x_vu haf A^(c)[S_pq minus {v,u}].                              (8)
~~~

The thirty-six equations (8), together with the reversed-colour equations
acting on the transposed directed variables, form M_(c,d).  Its columns are
the fifty-six directed edges v->u of K_8.

Split the column space as

~~~text
V = V_C direct-sum V_P,
dim V_C=12,                    dim V_P=44,                        (9)
~~~

where V_C contains directed core-core edges and V_P contains every directed
edge with at least one endpoint in W.  Write M=[M_C M_P].

### Theorem 1 (arbitrary-fibre port-defect criterion)

Let pi be the quotient map from the equation space to coker M_C.  Then

~~~text
projection_P(ker M) = ker(pi M_P),                               (10)
dim projection_P(ker M)
  =44-rank(pi M_P)
  =44-rank M+rank M_C
  =delta_(c,d).                                                  (11)
~~~

In particular, the axis kernel has nonzero port projection if and only if
delta_(c,d)>0.

### Proof

A port vector p is the projection of some (z,p) in ker M precisely when

~~~text
M_P p = -M_C z,
~~~

or equivalently when pi M_P p=0.  Moreover

~~~text
rank(pi M_P)=dim((im M_C+im M_P)/im M_C)
            =rank M-rank M_C.
~~~

Rank-nullity on the forty-four-dimensional port space proves (11).

Thus delta is not a heuristic score.  It is the exact quotient-matroid
defect measuring dependence of port columns modulo the core image.  Its
rank strata are determined by minors of M and M_C.

## 2. A boundary point of the six-face fibre

For every colour c, define

~~~text
a_ij^(c)=1                       i,j in C,
a_ip^(c)=0                       i in C, p in W,
b_pq^(c)=y_pq^(c)/3              p,q in W.                       (12)
~~~

This is the tau_c=0 specialization of the split-surjective section.  It lies
on the scalar coordinate boundary because all pure core-window edges vanish,
but every b_pq^(c) is nonzero.

The pure face identity is immediate:

~~~text
haf A^(c)[S_pq]
 = b_pq^(c) haf A^(c)[C]
 = 3 b_pq^(c)
 = y_pq^(c).                                                   (13)
~~~

No other matching contributes because every pure core-window edge is zero.

The pure four-deck also has a closed form.  For a four-set R,

~~~text
|R intersect W|=0:  3,
|R intersect W|=1:  0,
|R intersect W|=2:  b_pq^(c)=y_pq^(c)/3,
|R intersect W|=3:  0,
|R intersect W|=4:  (y_45 y_67+y_46 y_57+y_47 y_56)/9.          (14)
~~~

Here the final line is evaluated separately in each colour.

### Theorem 2 (exact boundary-section axis kernel)

For every pair among the three exact colours, the combined axis operator at
(12) has

~~~text
rank M=19,             rank M_C=7,
nullity M=37,          delta=32.                                (15)
~~~

Its kernel is the direct sum of:

- all thirty-two directed core-window coordinates; and
- the five-dimensional space of hollow directed 4 by 4 core matrices with
  zero row sums and zero column sums.

Every directed window-window coordinate is zero in the kernel.

### Proof

If the singleton vertex is a core vertex i, pairing it to another core
vertex leaves two core and two window vertices, whose pure hafnian is the
nonzero b_pq.  Pairing i to a window leaves three core and one window, whose
pure hafnian is zero.  Hence the equations are exactly the four core row
sums, and in the reversed orientation the four core column sums.  Together
these have rank seven.

If the singleton is a window vertex p, pairing it to the other window q
leaves the core hafnian 3.  Every core partner leaves a three-core/one-window
cofactor zero.  Thus each of the twelve directed window-window entries is
forced to zero.

No axis equation contains a directed core-window entry.  The total rank is
therefore 7+12=19, and the kernel is the asserted 5+32 dimensional direct
sum.  Formula (11) gives delta=44-19+7=32.

This gives the requested exact alternative scalar fibre.  It also proves
that the complement-sum covariant of the canonical section is not an
invariant of the six-face morphism.

## 3. Exact Gram escape from the forced window-pair coefficient

Now form 3 by 3 edge blocks with the following zero pattern:

~~~text
core-core blocks:       diagonal, with all diagonal entries 1;
window-window blocks:   diagonal, with entries b_pq^(c);
core-window blocks:     zero diagonal, arbitrary off-diagonal entries. (16)
~~~

For an ordered pair d!=c, collect the core-window entries into a 4 by 4
matrix

~~~text
X^(d,c)_(i,p)
 = edge value for core i coloured c and window p coloured d.    (17)
~~~

The six ordered colour-pair matrices use disjoint entries of the physical
3 by 3 core-window blocks and may be chosen independently.

Put

~~~text
D=J_4-I_4.                                                       (18)
~~~

Consider S_pq with all four core vertices coloured c and both ports coloured
d.  Pairing p to q contributes y_pq^(d).  If both ports pair to distinct
core vertices, the remaining core pair has weight one.  Therefore the exact
coefficient is

~~~text
y_pq^(d) + (x_p^(d,c))^T D x_q^(d,c),                            (19)
~~~

where x_p is column p of X.  Thus all six coefficients of this placement
vanish when the off-diagonal Gram data satisfy

~~~text
(X^(d,c))^T D X^(d,c) has off-diagonal entries -y_pq^(d).        (20)
~~~

Choose the diagonal entries to be zero.  For the three exact columns this
gives

~~~text
Q^0 =
[  0 -14  24 -20 ]
[ -14   0 -15  29 ]
[ 24 -15   0  -9 ]
[-20  29  -9   0 ],                    det Q^0=-78300;

Q^1 =
[  0 -10  33 -36 ]
[-10   0 -30  58 ]
[ 33 -30   0 -18 ]
[-36  58 -18   0 ],                    det Q^1=-349884;

Q^2 =
[  0  -2 -38  45 ]
[ -2   0  30 -73 ]
[-38  30   0  23 ]
[ 45 -73  23   0 ],                    det Q^2=2409300.          (21)
~~~

Also det D=-3.  Over an algebraically closed field of characteristic zero,
every two nondegenerate symmetric bilinear forms of the same dimension are
congruent.  Hence for every ordered pair d!=c there exists an invertible
X^(d,c) such that

~~~text
(X^(d,c))^T D X^(d,c)=Q^d.                                     (22)
~~~

Equations (19)-(22) cancel the complete six-face family in which the two
minority vertices are the two ports.  They do so symbolically, without
searching for a factor matrix.

Every 5+1 coefficient also vanishes under the zero pattern (16).  A
singleton core cannot use a different-colour core edge; after a
different-colour cross edge, the remaining three-core/one-window pure
cofactor is zero.  The same argument with the locations reversed handles a
singleton window.  This is the tensor realization of the thirty-two free
port axes in Theorem 2.

## 4. The mixed-location residual

The Gram equations are not the whole 4+2 family.  On S_pq, colour core
vertex i and window p by d, and all other vertices by c.  Write

~~~text
X=X^(d,c),                    Y=X^(c,d).
~~~

The only possible nonzero matching pairs core i to window q, pairs window p
to one of the other three core vertices, and pairs the last two core
vertices together.  Its coefficient is exactly

~~~text
Y_(i,q) sum_(j!=i) X_(j,p)
 = Y_(i,q) (D X)_(i,p).                                        (23)
~~~

The placement with p,q reversed supplies the same equation for every
ordered p!=q.

### Theorem 3 (invertible-Gram residual obstruction)

Suppose X and Y are invertible, satisfy their respective window-pair Gram
equations, and all mixed-location coefficients (23) vanish.  Then the face
column y^(c) must satisfy

~~~text
y_45^(c)y_67^(c)
 =y_46^(c)y_57^(c)
 =y_47^(c)y_56^(c).                                             (24)
~~~

None of the three exact columns satisfies (24).

### Proof

Set A=DX, which is invertible.  Vanishing of (23) says

~~~text
A_(i,p) Y_(i,q)=0                  for every i and p!=q.          (25)
~~~

For a fixed row i, both rows A_i and Y_i are nonzero.  If p is in the
support of A_i and q is in the support of Y_i, (25) forces p=q.  Thus both
rows are supported on the same single column.  Invertibility makes these
four columns a permutation, so Y is a monomial matrix.

Because D has zero diagonal and every off-diagonal entry one, the three
complementary products of off-diagonal entries of Y^T D Y all equal the
product of the four nonzero monomial scalars.  The Gram condition identifies
those entries with -y_pq^(c), proving (24).

For the exact columns the three product triples are

~~~text
colour 0: (126,696,300),
colour 1: (180,1914,1080),
colour 2: (-46,2774,1350),                                          (26)
~~~

and no triple is constant.

The nonsingular zero-diagonal Gram completions (21) therefore necessarily
leave some mixed-location 4+2 coefficient nonzero.  This is not an
arbitrary-fibre two-colour no-go: a hypothetical full completion may use
singular X or a different scalar fibre.  Equation (23) is the exact next
residual.

## 5. What changed under the translation

The canonical-section obstruction had the chain

~~~text
5+1 axis -> no port support -> forced 3 b_pq in 4+2.              (27)
~~~

At the boundary section (12), the translated chain is

~~~text
5+1 axis -> 32 free port directions
           -> symmetric-form Gram equations for window-pair 4+2
           -> mixed-location bilinear residual Y_(i,q)(DX)_(i,p). (28)
~~~

This is a strict structural advance.  The six pure Segre columns neither
force delta=0 nor force the coefficient 3 b_pq to survive.  The next
obstruction, if one exists, must use the incidence of minority vertices,
singular Gram geometry, the remaining 4+2 placements, or genuinely
three-colour equations.

The pure scalar H4 deck is synchronized by (14), but the corresponding
block-valued H4 tensors can have mixed-colour entries.  No fixed target H4
incidence theorem is claimed here.

## Literature position

Two neighboring theories organize the translation.  The port-defect formula
is a representable-matroid contraction statement: it measures dependencies
among the port columns after the core image is quotiented out.  Rosen,
Sidman, and Theran's survey
[*Algebraic matroids in action*](https://arxiv.org/abs/1809.00865) gives the
broader algebraic-independence viewpoint, although Theorem 1 here is proved
directly by linear algebra.  The off-diagonal equations (20) are a symmetric
matrix-completion problem.  Bernstein, Blekherman, and Lee's
[*Typical ranks in symmetric matrix completion*](https://arxiv.org/abs/1909.06593)
supplies that neighboring generic-completion perspective.  The present
argument is different and exact: it fixes three nongeneric partial matrices,
constructs their nonsingular completions by congruence, and then proves the
mixed-location product obstruction directly.

## Scope wall

~~~text
arbitrary-fibre port-defect formula:                   PROVED;
port support iff delta>0:                              PROVED;
canonical-section defect:                              delta=0;
tau=0 exact scalar fibre:                              CONSTRUCTED;
prescribed six pure Segre columns:                     REALIZED;
tau=0 axis rank / nullity / defect:                    19 / 37 / 32;
free directed core-window axis coordinates:           32;
canonical forced 3 b_pq fibre-invariant:               FALSE;
all 5+1 mixed coefficients in block construction:     ZERO;
window-pair-minority 4+2 coefficients:                 ZERO;
mixed-location 4+2 residual:                           Y_(i,q)(DX)_(i,p);
nonsingular zero-diagonal Gram route completes 4+2:    IMPOSSIBLE;
singular Gram completion of all two-colour equations:  UNKNOWN;
other 4+2 placements and 3+3 equations:                UNKNOWN;
genuinely three-colour equations:                      UNKNOWN;
full P6 tensor construction or obstruction:            UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.     (29)
~~~

## Replay

~~~powershell
uv run --with sympy python verify_p6_arbitrary_fibre_axis_port_defect_and_two_colour_gram_escape.py
python audit_p6_arbitrary_fibre_axis_port_defect_and_two_colour_gram_escape.py
python -m py_compile verify_p6_arbitrary_fibre_axis_port_defect_and_two_colour_gram_escape.py audit_p6_arbitrary_fibre_axis_port_defect_and_two_colour_gram_escape.py
uv run --with ruff ruff check verify_p6_arbitrary_fibre_axis_port_defect_and_two_colour_gram_escape.py audit_p6_arbitrary_fibre_axis_port_defect_and_two_colour_gram_escape.py
~~~

The primary replay uses exact SymPy arithmetic to verify the fibre values,
axis ranks and defect, representative symbolic coefficient identities, Gram
determinants, and residual product boundary.  The independent audit imports
no project module and no computer algebra package; it rebuilds the axis
operator with Fraction arithmetic and independently checks the determinant
and matching identities.  Neither replay searches graphs, colour words,
parameters, supports, gauges, or finite fields.

## Dependencies

- [P6_AXIS_COMPLEMENT_SUM_COVARIANT_OFFDIAGONAL_AND_GAUGE_NO_GO.md](P6_AXIS_COMPLEMENT_SUM_COVARIANT_OFFDIAGONAL_AND_GAUGE_NO_GO.md)
- [P6_PHYSICAL_SIX_FACE_HAFNIAN_SECTION_FOUR_DECK_SYNCHRONIZATION_AND_SEGRE_SHARPNESS.md](P6_PHYSICAL_SIX_FACE_HAFNIAN_SECTION_FOUR_DECK_SYNCHRONIZATION_AND_SEGRE_SHARPNESS.md)
- [P6_CLEAN_TWO_BY_THREE_SELECTOR_SEGRE_PULLBACK_AND_TORUS_PERMISSION_THEOREM.md](P6_CLEAN_TWO_BY_THREE_SELECTOR_SEGRE_PULLBACK_AND_TORUS_PERMISSION_THEOREM.md)
