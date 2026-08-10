# P6 two-shore hyperbolic scalar fibre, axis defect, and 4+2 transfer

## Status

**Exact characteristic-zero scalar fibre outside the excluded tau family.**
The explicit tau-section family is not the whole six-face fibre.  This note
constructs a different exact fibre point which:

- realizes all three prescribed six-face Segre columns;
- retains the normalized pure-core hafnian 3;
- has every scalar window-window edge equal to zero;
- has a sixteen-dimensional pure port subspace in every two-colour 5+1
  axis kernel; and
- transfers the first 4+2 obstruction to a different incidence class.

The construction uses a matching core and a two-row core-window shore.  The
six face values are a hyperbolic Gram vector

~~~text
y_pq=r_p s_q+s_p r_q.                                           (1)
~~~

Every full-support six-vector over a characteristic-zero field admits such
a factor after a diagonal completion of rank two; here the factors are
given explicitly over the rationals.

For every colour pair, the combined axis operator has

~~~text
rank M=30,       rank M_C=2,       nullity M=26,
delta=44-rank M+rank M_C=16.                                    (2)
~~~

The kernel is a coordinate space: all sixteen directed edges between the
inactive core pair and the four-window, together with ten directed
core-core edges, are free.

An exact kernel deformation then cancels the both-window-minority 4+2
family, the formerly fatal inactive-core-pair 4+2 family, and one
mixed-location family.  A different mixed-location word remains exactly

~~~text
s_p^(d) r_q^(c),                                                 (3)
~~~

which is nonzero on an explicit face.  Thus this is not a P6 construction.
It is a strict fibre translation: the tau-family tetrad obstruction is not
fibre-invariant, and the remaining obstruction now detects which active
shore row carries the minority core.

No graph, word, support, parameter tuple, finite field, numerical solve, or
Groebner search is used.

## 1. Hyperbolic factorization of the face columns

Let the four ports be ordered 4,5,6,7.  Given nonzero off-diagonal data

~~~text
q_45,q_46,q_47,q_56,q_57,q_67,                                  (4)
~~~

define two row vectors r,s by

~~~text
r_4=1,                  s_4=0,
s_5=q_45,               s_6=q_46,               s_7=q_47,

r_5=(q_56 q_47+q_46 q_57-q_45 q_67)/(2 q_46 q_47),
r_6=(q_56-r_5 q_46)/q_45,
r_7=(q_57-r_5 q_47)/q_45.                                      (5)
~~~

### Lemma 1 (rank-two diagonal completion)

The vectors (5) satisfy

~~~text
r_p s_q+s_p r_q=q_pq             for every p<q.                  (6)
~~~

### Proof

The equations involving port 4 hold by construction.  The definitions of
r_6 and r_7 give the 56 and 57 equations.  The numerator defining r_5 is
exactly the result of solving

~~~text
r_6 s_7+s_6 r_7=q_67.
~~~

All divisions are legal for the exact columns because q_45,q_46,q_47 are
nonzero.

Equivalently, adjoining suitable diagonal entries to the symmetric matrix
with off-diagonal vector q gives rank two.  Formula (5) is a rational
hyperbolic factorization, rather than an existence argument by algebraic
closure.

For the three exact columns the factors are

~~~text
colour 0:
 r=(1,-29/32,-27/56,-87/112),
 s=(0,14,-24,20);

colour 1:
 r=(1,-469/396,-109/120,-169/110),
 s=(0,10,-33,36);

colour 2:
 r=(1,-139/114,49/6,689/76),
 s=(0,2,38,-45).                                                 (7)
~~~

Every r entry is nonzero and each s has support exactly three.

## 2. The two-shore scalar graph

Put

~~~text
C={0,1,2,3},                    W={4,5,6,7}.                      (8)
~~~

For colour c, define the scalar graph A^(c) by

~~~text
core:
  a_01^(c)=3,       a_23^(c)=1,
  every other core edge=0;

core-window:
  a_0p^(c)=r_p^(c), a_1p^(c)=s_p^(c),
  a_2p^(c)=a_3p^(c)=0;

window:
  b_pq^(c)=0.                                                 (9)
~~~

The active shore is A={0,1}; the inactive shore is I={2,3}.

### Theorem 2 (exact full-fibre point)

For every colour c,

~~~text
haf A^(c)[C]=3,
haf A^(c)[C union {p,q}]=y_pq^(c).                              (10)
~~~

### Proof

The core has the single nonzero perfect matching 01--23, of weight 3.
On C union {p,q}, the windows cannot pair together.  Both must cross to
the active shore 0,1, and the remaining inactive edge 23 has weight one.
The two possible assignments contribute

~~~text
r_p s_q+s_p r_q=y_pq.                                          (11)
~~~

This point is outside the tau family.  In that family, all six window edges
could vanish only if all six y_pq equalled the common value 12 tau_c^2;
none of the exact columns is constant.

## 3. Exact four-cofactor deck

Fix a face S_pq=C union {p,q}.  Its pure four-vertex cofactors are:

~~~text
remove core 2,3:              y_pq;
remove any other core pair:  0;

remove core 0 and window p:  s_q;
remove core 1 and window p:  r_q;
remove core 2 or 3 and p:    0;

remove both windows:          3.                                (12)
~~~

The formulas with p,q reversed are understood.  They follow immediately
from the two disjoint core edges and the two-row shore.

## 4. Axis port defect

For distinct colours c,d, let x_vu be the directed edge value with singleton
colour d at v and majority colour c at u.  The first half of the 5+1 axis
system on S_pq becomes

~~~text
s_q^(c)x_0p+s_p^(c)x_0q=0,
r_q^(c)x_1p+r_p^(c)x_1q=0,
y_pq^(c)x_23=0,
y_pq^(c)x_32=0,                                                 (13)

3x_pq+s_q^(c)x_p0+r_q^(c)x_p1=0.                               (14)
~~~

Equation (14) is written for window singleton p.  The reversed-colour half
has the transposed variables and the colour-d factors.

### Theorem 3 (coordinate axis kernel)

For every pair of exact colours, the combined 72 by 56 axis kernel is
exactly the coordinate span of:

~~~text
x_ip,x_pi             i in {2,3}, p in W;       16 coordinates,
x_ij                  i,j in C, i!=j,
                      except (i,j)=(2,3),(3,2);  10 coordinates. (15)
~~~

Consequently (2) holds.

### Proof

Because s has three nonzero entries, the six equations
s_q x_0p+s_p x_0q=0 force all four x_0p to vanish in characteristic zero.
The full-support row r similarly kills all x_1p.  The transposed equations
kill x_p0 and x_p1.

Since every y_pq is nonzero, (13) kills x_23 and x_32.  Equations (14) and
their transposes then kill every directed window-window entry.  No equation
contains an edge between I and W or any of the other ten directed core
edges, by the zero cofactors in (12).

Thus the kernel is the displayed 26-dimensional coordinate space.  The
core restriction has a ten-dimensional kernel in twelve coordinates, so
rank M_C=2.  Rank-nullity gives rank M=56-26=30, and the arbitrary-fibre
port-defect formula gives delta=44-30+2=16.

Unlike the tau-zero fibre, whose port defect is 32, this fibre exposes
exactly the bidirected inactive shore.

## 5. An exact 4+2 transfer

Fix an ordered colour pair d,c.  Use the following entries from the axis
kernel:

~~~text
edge(core 2 coloured d, window p coloured c)=r_p^(c),
edge(core 3 coloured d, window p coloured c)=0,
edge(core 3 coloured d, core 0 coloured c)=-1.                  (16)
~~~

For the reverse colour orientation use

~~~text
edge(core 2 coloured c, window p coloured d)=r_p^(d),
edge(core 3 coloured c, window p coloured d)=0,
edge(core 0 coloured d, core 3 coloured c)=-1.                  (17)
~~~

Set the other off-diagonal entries to zero.  Every entry in (16)-(17) is
one of the free coordinates (15), so all 5+1 equations remain zero.

### Theorem 4 (three cancelled 4+2 incidence families)

The deformation (16)-(17) has the following exact coefficients on
S_pq:

~~~text
core d, both windows c:                         0;
cores 2,3 coloured d, every other vertex c:     0;
core 0 and window p coloured d, all others c:   0;
core 1 and window p coloured d, all others c:   s_p^(d)r_q^(c).
                                                                    (18)
~~~

### Proof

For the first word, both c-coloured windows would have to use distinct
d-coloured core partners.  Only core 2 has a nonzero cross-colour shore
entry, so no matching survives.

For the second word, the pure minority edge 23 times the pure majority
four-set {0,1,p,q} contributes

~~~text
y_pq^(c)=r_p^(c)s_q^(c)+s_p^(c)r_q^(c).
~~~

The two matchings which send core 2 to a window and core 3 to core 0
contribute its negative, because the latter edge has weight -1 and the
remaining window pairs purely to core 1.  The total is zero.

For the third word, the pure matching

~~~text
(0,p)(1,q)(2,3)
~~~

has weight r_p^(d)s_q^(c).  Replacing (0,p)(2,3) by the two
cross-colour edges (2,p)(0,3) gives the negative of the same monomial.

For the final word, the analogous compensating route would require the
off-diagonal core edge 1--3, which is zero.  The sole surviving matching

~~~text
(1,p)(0,q)(2,3)
~~~

has weight s_p^(d)r_q^(c).

On face 45, take p=5 and q=4.  Formula (7) gives

~~~text
s_5^(d)r_4^(c)=y_45^(d),                                       (19)
~~~

which is nonzero for every colour d.  The displayed deformation is
therefore an exact transfer of the 4+2 obstruction, not a full completion.

## 6. Translation

The explicit tau fibres placed the pure face value partly or entirely on a
window edge.  Their first fatal 4+2 coefficient was a window-edge weight
times a core hafnian.  The two-shore fibre instead realizes every face
value by two cross-shore matchings:

~~~text
window-edge realization         -> hyperbolic two-shore realization,
canonical/tau-zero port axes     -> inactive-shore coordinate axes,
window-pair 4+2 obstruction      -> active-row incidence residual. (20)
~~~

This proves that neither the size of the axis port kernel nor the location
of the first 4+2 obstruction is determined by the six pure face values.
A fibre-invariant obstruction must survive both the tau strata and this
two-shore stratum, or use additional H4 target incidence.

The factorization (5) is the rank-two symmetric-completion geometry behind
the construction.  The remaining residual (3) records an oriented choice
of one of its two hyperbolic shore rows.

## Scope wall

~~~text
exact non-tau scalar fibre with prescribed six faces:  CONSTRUCTED;
normalized pure-core hafnian 3:                        RETAINED;
scalar window-window edges:                            ALL ZERO;
arbitrary-pair axis rank / nullity / defect:           30 / 26 / 16;
axis kernel:                                            COORDINATE;
both-window-minority 4+2 family after deformation:     ZERO;
inactive-core-pair 4+2 family after deformation:       ZERO;
one active-core/window 4+2 family:                     ZERO;
other active-core/window 4+2 residual:                 NONZERO;
complete two-colour 4+2 cancellation on this fibre:    UNKNOWN;
full block-valued H4 target incidence:                 UNKNOWN;
fibre-invariant P6 obstruction:                        UNKNOWN;
unrestricted P6 construction or obstruction:          UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.    (21)
~~~

## Replay

~~~powershell
uv run --with sympy python claims/p6/verify_p6_two_shore_hyperbolic_scalar_fibre_axis_defect_and_four_plus_two_transfer.py
python claims/p6/audit_p6_two_shore_hyperbolic_scalar_fibre_axis_defect_and_four_plus_two_transfer.py
python -m py_compile claims/p6/verify_p6_two_shore_hyperbolic_scalar_fibre_axis_defect_and_four_plus_two_transfer.py claims/p6/audit_p6_two_shore_hyperbolic_scalar_fibre_axis_defect_and_four_plus_two_transfer.py
uv run --with ruff ruff check claims/p6/verify_p6_two_shore_hyperbolic_scalar_fibre_axis_defect_and_four_plus_two_transfer.py claims/p6/audit_p6_two_shore_hyperbolic_scalar_fibre_axis_defect_and_four_plus_two_transfer.py
~~~

The primary replay checks the rational hyperbolic factors, pure face
hafnians, exact axis ranks and coordinate kernel, and the four symbolic
4+2 identities.  The independent audit rebuilds everything with Fraction
arithmetic and its own exact row reduction.  Neither replay enumerates
graphs, words, supports, ranks, parameters, or finite fields.

## Dependencies

- [P6_TAU_ZERO_SINGULAR_GRAM_TETRAD_SUPPORT_AND_FOUR_PLUS_TWO_NO_GO.md](P6_TAU_ZERO_SINGULAR_GRAM_TETRAD_SUPPORT_AND_FOUR_PLUS_TWO_NO_GO.md)
- [P6_ARBITRARY_FIBRE_AXIS_PORT_DEFECT_AND_TWO_COLOUR_GRAM_ESCAPE_THEOREM.md](P6_ARBITRARY_FIBRE_AXIS_PORT_DEFECT_AND_TWO_COLOUR_GRAM_ESCAPE_THEOREM.md)
- [P6_PHYSICAL_SIX_FACE_HAFNIAN_SECTION_FOUR_DECK_SYNCHRONIZATION_AND_SEGRE_SHARPNESS.md](P6_PHYSICAL_SIX_FACE_HAFNIAN_SECTION_FOUR_DECK_SYNCHRONIZATION_AND_SEGRE_SHARPNESS.md)
