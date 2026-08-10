# P6 tau-zero singular-Gram tetrad support and 4+2 no-go

## Status

**Exact arbitrary-rank closure of the tau-zero singular-Gram branch.**  The
tau-zero scalar section has a thirty-two-dimensional core-window port kernel,
so the 5+1 axis equations alone do not obstruct a tensor completion.  This
note proves that no singular or nonsingular choice of those port directions
can satisfy the complete two-colour 4+2 layer.

The obstruction uses three symbolic 4+2 placements, not an elimination:

~~~text
both windows minority,
both core vertices minority,
one core and one window minority.                                (1)
~~~

For a pair of colours, the first two placements force all six symmetrized
row-pair products of each core-window matrix onto the line spanned by one
fixed face column.  Because the exact columns have full support and violate
the rank-one complementary-product identities, a row-support lemma forces
each cross matrix to have exactly two nonzero rows.  The mixed-location
equation then makes the two rows of one matrix negatives.  Its row-pair
product is necessarily rank one, contradicting the same complementary-
product invariant.

This proof allows the full five-dimensional core-circulation survivor of the
tau-zero axis kernel.  It does not assume that the Gram matrices or the
cross matrices are invertible.  The singular-Gram solution set through 4+2
is therefore empty.

As a corollary, the entire explicit split-surjective scalar section family
parameterized by (tau_0,tau_1,tau_2) is excluded: the preceding canonical
axis theorem handles pairs of nonzero tau values, a short hybrid argument
handles mixed zero/nonzero values, and the theorem here handles the all-zero
point.  Other points of the full six-face scalar fibre remain **UNKNOWN**.
No unrestricted P6 obstruction or global Krenn--Gu proof is claimed.

No graph, colour-word, support, rank tuple, parameter tuple, finite field, or
Groebner search is used.  The proof is a matching decomposition, one
linear-map injectivity lemma, and the classical rank-one tetrad invariant.

## 1. Exact tau-zero block data

Let

~~~text
C={0,1,2,3},                       W={4,5,6,7}.                   (2)
~~~

For each colour c, the tau-zero scalar graph has

~~~text
core edges:          a_ij^(c)=1,
pure core-window:    a_ip^(c)=0,
window edges:        b_pq^(c)=y_pq^(c)/3.                        (3)
~~~

The exact face columns, in pair order 45,46,47,56,57,67, are

~~~text
y^(0)=(14,-24,20,15,-29,9),
y^(1)=(10,-33,36,30,-58,18),
y^(2)=(2,38,-45,-30,73,-23).                                  (4)
~~~

Every entry is nonzero.  Their three complementary-product triples are

~~~text
colour 0: (126,696,300),
colour 1: (180,1914,1080),
colour 2: (-46,2774,1350).                                      (5)
~~~

No triple is constant.  Scaling a column by 1/3 does not change this
failure.

Fix distinct colours c,d.  Use the following directed variables:

~~~text
X_ip = edge(core i coloured c, window p coloured d),
Y_ip = edge(core i coloured d, window p coloured c),
Z_ij = edge(core i coloured d, core j coloured c).               (6)
~~~

The 5+1 equations at tau zero force every cross-colour window-window entry
to zero.  They constrain Z to the hollow directed core-circulation space
with zero row and column sums, but the proof below does not need those
linear constraints.  Both X and Y are initially arbitrary 4 by 4 matrices.

For a core pair i<j and a window pair p<q, put

~~~text
P_ij(Y;pq)=Y_ip Y_jq+Y_iq Y_jp.                                 (7)
~~~

If {k,l}=C minus {i,j}, put

~~~text
R_ij(Z)=Z_ik Z_jl+Z_il Z_jk.                                    (8)
~~~

Finally let D=J_4-I_4.

## 2. The three complete matching identities

### Lemma 1 (the 4+2 coefficient trichotomy)

On the face C union {p,q}, vanishing of the following three mixed
coefficients gives:

~~~text
cores d, windows c:
  3 b_pq^(c) + sum_(i<j) P_ij(Y;pq)=0;                           (9)

cores i,j coloured d, every other vertex c:
  b_pq^(c)(1+R_ij(Z))+P_ij(Y;pq)=0;                             (10)

core i and window p coloured d, every other vertex c:
  Y_iq (D X)_ip=0.                                              (11)
~~~

The placement in (11) with p and q interchanged supplies the equation for
every ordered p!=q.

### Proof

For (9), either p and q pair together and the four-core hafnian is 3, or
they pair to distinct core vertices i,j.  The remaining core pair has
weight one, giving P_ij.  These are all possibilities.

For (10), there are exactly three nonzero matching classes:

- i--j and k--l use pure core edges while p--q contributes b;
- i,j pair to p,q, giving P_ij while k--l contributes one;
- i,j pair cross-colour to k,l, giving R_ij while p--q contributes b.

Any hybrid of a core-core cross-colour edge and a core-window cross-colour
edge leaves a pure same-colour core-window edge, which is zero.

For (11), the core minority i must pair to the majority window q, and the
window minority p must pair to one of the other three core vertices.  The
last two core vertices pair with weight one.  Summing the second choice is

~~~text
Y_iq sum_(j!=i)X_jp = Y_iq(DX)_ip.
~~~

Core-circulation entries cannot contribute: using one leaves a same-colour
core-window pair of scalar weight zero.

Thus (9)-(11) are matching identities, not selected terms from a larger
expansion.

## 3. The Euler-hafnian obstruction when Z=0

There is already a rank-free summation contradiction in the zero-core
Gram ansatz of the preceding note.  It extends to an arbitrary even core.

Let a colour-d core have 2m vertices, pure hafnian h_d, edge a_ij^(d), and
cofactor

~~~text
C_ij^(d)=haf A^(d)[C minus {i,j}].                               (12)
~~~

Suppose pure core-window edges and cross-colour core-core edges vanish.
The analogues of (9) and (10) are

~~~text
b h_d + sum_(i<j) C_ij^(d) P_ij=0,
C_ij^(c)(a_ij^(d)b+P_ij)=0.                                    (13)
~~~

If every C_ij^(c), b, and h_d is nonzero, the second family gives
P_ij=-a_ij^(d)b.  The hafnian Euler identity

~~~text
sum_(i<j) a_ij^(d) C_ij^(d)=m h_d                               (14)
~~~

turns the first equation into

~~~text
(1-m)b h_d=0.                                                    (15)
~~~

This is impossible in characteristic zero for m>=2.  Identity (14) holds
because every perfect matching has m edges and its monomial occurs once for
each of them.

For the four-core all-one section, h_d=3 and m=2.  Equivalently, the six
both-core equations demand

~~~text
sum P_ij=-6b=-2y,
~~~

while the both-window equation demands sum P_ij=-3b=-y.  This
factor-two contradiction already closes every singular Gram factor when
Z=0.

## 4. The row-pair tetrad lemma

For row vectors r,s in K^4 define

~~~text
Phi(r,s)_(pq)=r_p s_q+r_q s_p,             p<q.                  (16)
~~~

A full-support vector beta in K^6 is called **tetrad rank one** when

~~~text
beta_45 beta_67=beta_46 beta_57=beta_47 beta_56.                 (17)
~~~

On the coordinate torus this is exactly the condition that beta is
proportional to the off-diagonal vector (u_p u_q)_(p<q).

### Lemma 2 (one-line row-pair support)

Let beta have full support and fail (17).  Suppose four row vectors
r_0,...,r_3 satisfy

~~~text
Phi(r_i,r_j) belongs to K beta             for every i<j,         (18)
~~~

and at least one of these six vectors is nonzero.  Then exactly two rows
are nonzero, and their mutual Phi is the unique nonzero row-pair vector.
Both nonzero rows have support at least three.

### Proof

If Phi(r,s) is a nonzero full-support vector, each of r,s has support at
least three: a vector supported on at most two coordinates leaves an
off-diagonal coordinate of Phi equal to zero.

For a row r with support at least three, the linear map

~~~text
L_r:s maps to Phi(r,s)                                           (19)
~~~

is injective.  Indeed, on three nonzero coordinates the equations
Phi(r,s)=0 say that the three ratios s_p/r_p have pairwise sums zero.
Characteristic zero forces all three to vanish; the remaining coordinates
then vanish as well.

Make a graph on the four row indices, joining i,j when Phi(r_i,r_j) is
nonzero.  If one vertex i had two neighbours j,k, injectivity of L_(r_i)
would make r_j and r_k proportional.  Their mutual Phi would then be a
nonzero rank-one off-diagonal vector proportional to beta, forcing (17), a
contradiction.  Hence every vertex has degree at most one.

Two disjoint edges are also impossible.  An endpoint r_i of one edge has
support at least three, while its zero Phi with an endpoint of the other
edge would force that other row to vanish by injectivity.  There is
therefore exactly one edge.  The same injectivity kills the two rows not
incident to it.

The equalities (17) are the familiar tetrad equations for an off-diagonal
rank-one symmetric model.  More general tetrad and diagonal-elimination
invariants occur in algebraic factor analysis; see Drton, Sturmfels, and
Sullivant, [Algebraic Factor Analysis: Tetrads, Pentads and
Beyond](https://arxiv.org/abs/math/0509390).  Lemma 2 is a direct
four-row statement and does not depend on that literature.

## 5. Arbitrary-rank tau-zero no-go, including core circulations

### Theorem 3 (singular-Gram branch is empty)

For the three exact columns (4), no off-diagonal completion of the tau-zero
scalar section can make all two-colour 5+1 and 4+2 coefficients vanish.
This holds for every rank of X and Y and permits every core-circulation Z
surviving the axis equations.

### Proof

Equation (10) gives, for every core pair,

~~~text
Phi(Y_i,Y_j)=-(1+R_ij(Z)) b^(c).                                (20)
~~~

Thus all six row-pair vectors lie on the line K b^(c).  Equation (9) says
their sum is -3b^(c), so at least one is nonzero.  The column b^(c) has full
support and fails the tetrad equalities by (5).  Lemma 2 therefore says
that Y has exactly two nonzero rows, each with support at least three.

Swap c and d.  The same argument, with the transposed directed core
circulation where appropriate, says that X also has exactly two nonzero
rows, each with support at least three.

Let U and V be the two-row supports of Y and X respectively.  For i in U,
equations (11) and their p,q reversals force

~~~text
(DX)_i=0.                                                        (21)
~~~

Indeed, for every p one can choose q!=p in the at-least-three-element
support of Y_i.

If i lay in U intersect V, then (DX)_i would equal the other nonzero row of
X, a contradiction.  Hence U and V are disjoint.  Both have size two, so
they are complementary.  For i in U, equation (21) now says that the two
nonzero rows of X sum to zero.  Write them r and -r.

Their unique nonzero row-pair vector is

~~~text
Phi(r,-r)=(-2 r_p r_q)_(p<q).                                  (22)
~~~

By the swapped form of (20), this vector is a nonzero multiple of b^(d).
It has full support, so r has full support, and its three complementary
products are equal.  This forces b^(d) to satisfy the tetrad equalities,
contradicting (5).

No rank assumption entered the proof.  In particular, allowing singular
Gram matrices does not evade the tau-zero obstruction.

## 6. Exact circulation-energy boundary

Summing (10) over the six core pairs and comparing with (9) gives the
necessary condition

~~~text
E(Z):=sum_(i<j)R_ij(Z)=-3.                                      (23)
~~~

For a hollow directed 4 by 4 core circulation with zero row and column
sums, choose free coordinates

~~~text
u=Z_13,  v=Z_23,  w=Z_31,  x=Z_32
~~~

and one fifth circulation coordinate which drops out of E.  Exact
elimination of the seven independent linear sum constraints gives

~~~text
E(Z)=2(
 u^2+uv+2uw+ux
 +v^2+vw+2vx
 +w^2+wx+x^2).                                                  (24)
~~~

Condition (23) is not itself contradictory over an algebraically closed
field: for example u^2=-3/2 and v=w=x=0 satisfies it.  Theorem 3 closes the
branch only after retaining the individual row-pair equations and the
mixed-location incidence; summation alone loses essential support data.

## 7. Closure of the explicit tau-section family

The split-surjective section before specialization is

~~~text
core edges=1,
core-window edges=tau_c,
b_pq^(c)=(y_pq^(c)-12 tau_c^2)/3.                               (25)
~~~

### Corollary 4 (no point of the explicit tau family completes)

For the exact columns (4), no value of (tau_0,tau_1,tau_2) admits a
three-colour GHZ-diagonal off-diagonal completion on all six faces.

### Proof

If two selected colours have nonzero tau, their nonzero complement-sum
covariants make the canonical 5+1 theorem kill all port off-diagonals for
that pair.  At least one b_pq of either colour is nonzero because its six
y_pq values are not all equal.  The corresponding 4+2 coefficient is the
nonzero 3b_pq.

If tau_c!=0 and tau_d=0, the majority-c 5+1 equations kill every edge from
a d-coloured core to a c-coloured window.  Colour the core by d and both
windows by c.  Again at least one b_pq^(c) is nonzero, and the surviving
coefficient is 3b_pq^(c).

Thus any tau vector with a nonzero coordinate is excluded by a nonzero/
nonzero or nonzero/zero colour pair.  The all-zero vector is excluded by
Theorem 3.

This corollary closes the explicit three-parameter section family, not the
full split-surjective six-face fibre.

## Scope wall

~~~text
complete symbolic tau-zero 4+2 placement identities:  DERIVED;
zero-core Euler-hafnian factor-two obstruction:        PROVED;
row-pair tetrad support lemma:                         PROVED;
singular and nonsingular Gram factors at tau zero:     EXCLUDED;
five-dimensional core-circulation survivor allowed:   YES;
tau-zero completion through all two-colour 4+2 words:  IMPOSSIBLE;
entire explicit (tau_0,tau_1,tau_2) section family:    EXCLUDED;
other points of the six-face scalar fibre:             UNKNOWN;
non-stabilizer gauges preserving only pure columns:    UNKNOWN;
fixed block-valued H4 target incidence:                UNKNOWN;
unrestricted P6 obstruction or construction:           UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.    (26)
~~~

## Replay

~~~powershell
uv run --with sympy python claims/p6/verify_p6_tau_zero_singular_gram_tetrad_support_and_four_plus_two_no_go.py
python claims/p6/audit_p6_tau_zero_singular_gram_tetrad_support_and_four_plus_two_no_go.py
python -m py_compile claims/p6/verify_p6_tau_zero_singular_gram_tetrad_support_and_four_plus_two_no_go.py claims/p6/audit_p6_tau_zero_singular_gram_tetrad_support_and_four_plus_two_no_go.py
uv run --with ruff ruff check claims/p6/verify_p6_tau_zero_singular_gram_tetrad_support_and_four_plus_two_no_go.py claims/p6/audit_p6_tau_zero_singular_gram_tetrad_support_and_four_plus_two_no_go.py
~~~

The primary replay verifies the three matching identities with exact
symbolic hafnian recurrence, the Euler identity, tetrad failures, and the
circulation-energy formula.  The independent audit uses its own sparse
polynomial arithmetic and imports neither project code nor a computer
algebra package.  Neither replay searches any graph, word, support, rank
tuple, parameter tuple, or finite field.

## Dependencies

- [P6_ARBITRARY_FIBRE_AXIS_PORT_DEFECT_AND_TWO_COLOUR_GRAM_ESCAPE_THEOREM.md](P6_ARBITRARY_FIBRE_AXIS_PORT_DEFECT_AND_TWO_COLOUR_GRAM_ESCAPE_THEOREM.md)
- [P6_AXIS_COMPLEMENT_SUM_COVARIANT_OFFDIAGONAL_AND_GAUGE_NO_GO.md](P6_AXIS_COMPLEMENT_SUM_COVARIANT_OFFDIAGONAL_AND_GAUGE_NO_GO.md)
- [P6_PHYSICAL_SIX_FACE_HAFNIAN_SECTION_FOUR_DECK_SYNCHRONIZATION_AND_SEGRE_SHARPNESS.md](P6_PHYSICAL_SIX_FACE_HAFNIAN_SECTION_FOUR_DECK_SYNCHRONIZATION_AND_SEGRE_SHARPNESS.md)
