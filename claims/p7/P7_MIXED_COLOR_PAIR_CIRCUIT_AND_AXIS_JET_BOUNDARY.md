# The mixed-colour pair circuit and the all-axis jet boundary

## Status

**Exact characteristic-zero circuit theorem, dominance theorem, and formal
axis-jet countermodel.**  The scalar clean-window theory leaves the three
same-colour response charts uncoupled.  This note identifies the smallest
shared physical-block equation that genuinely couples them.

For one blocker pair `u,v`, evaluate its two-residual corrected response on
three independent directions at each endpoint.  The resulting `3 x 3` matrix
is

```text
D_uv=a_u b_v^T+b_u a_v^T,                              (1)
```

so

```text
det D_uv=0.                                             (2)
```

All nine mixed-colour entries form one algebraic-matroid circuit: the
rank-at-most-two determinantal variety has dimension eight, and every proper
coordinate subset is algebraically independent.  In particular, no generic
one- or two-chart shadow of (2) exists.

This circuit is not yet exposed in P7.  The current scalar windows see at
most `D_uv^(00),D_uv^(11),D_uv^(22)`.  The six off-diagonal mixed-colour
entries remain inside aggregated mixed-word equations.  A common legal block
construction proves that all same-colour pair/top data are independent across
the three charts, apart from their common residual scalar and the separate
within-chart dual-Wick equations.

The all-axis lower mixed-jet equations do not supply the missing entries.  An
exact common deletion-state model satisfies every such jet equation, with the
correct diagonal values and zero mixed blocker coefficients, for every
all-axis tuple—including `4+1`, `3+1+1`, and `2+2+1`.  This model is formal,
not a common hafnian graph, and therefore locates the missing theorem rather
than constructing a P7 restriction.

The next exact target is now unambiguous: legally expose the six mixed entries
of one corrected physical pair block, or an equivalent fully observed `3 x 3`
cross-block.  The P7 branch and the global Krenn--Gu conjecture remain
**UNRESOLVED**.

## 1. One physical pair carries a rank-two mixed-colour block

Let `Q={q_0,q_1}` be the two residual vertices.  Fix their modes and write

```text
h=B_(q_0,q_1),
a_u(x)=B_(q_0,u)(z_0,x),
b_u(x)=B_(q_1,u)(z_1,x).                               (3)
```

For two physical ports `u,v`, let

```text
m_uv(x,y)=B_uv(x,y),
z_uv(x,y)=haf G[Q union {u,v}].                        (4)
```

The three matching partitions on four vertices give

```text
z_uv(x,y)=h m_uv(x,y)+a_u(x)b_v(y)+b_u(x)a_v(y).       (5)
```

Choose bases `x_u^0,x_u^1,x_u^2` and `x_v^0,x_v^1,x_v^2`.  Define the
corrected mixed-colour matrix

```text
D_uv^(cd)=z_uv(x_u^c,x_v^d)-h m_uv(x_u^c,x_v^d).       (6)
```

Let `a_u,b_u,a_v,b_v` now denote their three evaluation columns.  Equation
(5) becomes (1).

### Theorem 1 (mixed-colour pair determinant)

Every two-residual graph response satisfies

```text
rank D_uv<=2,
det D_uv=0.                                            (7)
```

Proof.  Equation (1) is a sum of two outer products.  Its column space lies
in `span{a_u,b_u}`, proving the rank bound and determinant equation.

The use of three directions at **both** endpoints is essential.  A `2 x 2`
submatrix may have rank two and has no generic determinant vanishing.

## 2. The determinant is one minimal algebraic circuit

Let `X=(X_cd)` be a generic `3 x 3` matrix.  The rank-at-most-two variety is
the irreducible hypersurface

```text
det X=0                                                (8)
```

of dimension eight.  Parameterization (1) covers it because every rank-two
matrix is a sum of two rank-one matrices.

### Theorem 2 (coordinate-circuit minimality)

The nine entries of `D_uv` are an algebraic-matroid circuit.  They obey (2),
but every proper coordinate subset is algebraically independent on the
rank-at-most-two variety.

Proof.  Delete one entry `X_cd`.  The determinant is affine-linear in that
entry:

```text
det X=(-1)^(c+d) det X_(hat c,hat d) X_cd+R.           (9)
```

On the dense chart where the displayed cofactor is nonzero, arbitrary values
of the other eight entries have a unique completion satisfying `det X=0`.
Thus the projection to those eight coordinates is dominant.  Every smaller
proper subset lies inside some such eight-set and is also independent.  The
full nine-set is dependent by (8), proving circuit minimality.

This is the exact algebraic-matroid meaning of "the first shared-block
circuit."  Observing only the three diagonal entries is six coordinates short
of this circuit; adding any proper selection of mixed entries still gives no
universal polynomial equation.

## 3. Three scalar charts are a fibre product, not a coupling

Suppose the three chart vectors at every port `u` form a basis, with duals
`alpha_u^0,alpha_u^1,alpha_u^2`.  Choose endpoint covectors `eta_t` with
`eta_t(z_t)=1`.  Given arbitrary chartwise scalars

```text
beta_uv^c, a_u^c, b_u^c,
```

define one common legal symmetric block system by

```text
B_uv=sum_c beta_uv^c alpha_u^c tensor alpha_v^c,

B_(q_0,u)=eta_0 tensor sum_c a_u^c alpha_u^c,
B_(q_1,u)=eta_1 tensor sum_c b_u^c alpha_u^c,

B_(q_0,q_1)=h eta_0 tensor eta_1,                     (10)
```

and use transpose blocks in the reverse orientations.

On the all-`c` chart these evaluate to

```text
m_uv^(c)=beta_uv^c,
D_uv^(c)=a_u^c b_v^c+b_u^c a_v^c.                    (11)
```

No parameter with colour label `d!=c` appears.

### Theorem 3 (diagonal-chart independence)

The union of the three same-colour response varieties is the fibre product
of three independent single-chart varieties over the common scalar `h`.
Consequently there is no cross-colour polynomial identity among diagonal
pair and top-window data beyond:

1. equality of the residual scalar `h`; and
2. the dual-Wick equations internal to each chart.

Proof.  Construction (10) realizes every product of three single-chart
parameter choices with the same `h` in one physical symmetric block graph.
Conversely each same-colour chart is governed by its own specialization of
the two-residual response theorem.  Hence the common image is exactly the
stated fibre product and its ideal is the sum of the three within-chart ideals
and the equations identifying `h`.

This theorem concerns port/residual blocks.  Those parameter classes are
disjoint from the root--blocker blocks, so the interpolation can coexist with
the canonical root-row incidence profile.  It does not claim that arbitrary
choices also satisfy all mixed GHZ words.

## 4. Pair-plus-top data remain dominant in each chart

The same-colour failure persists even after one pair face and one top face are
both observed.  On `W={1,2,3,4}`, set `h=0` and take

```text
B_12=x,       B_34=y,
D_12=p,       D_34=q,                                 (12)
```

with every other complementary direct/corrected edge zero.  Then

```text
(m_12,z_12,m_W,z_W)=(x,p,xy,py+qx).                   (13)
```

### Proposition 4 (same-chart pair/top dominance)

The map in (13) is dominant.  Its Jacobian determinant with respect to
`(x,p,y,q)` is `x^2`.

Proof.  The direct four-point hafnian is `xy`.  The two-residual four-point
equation gives `z_W=D_12 B_34+D_34 B_12=py+qx`.  The Jacobian determinant is
as stated and is nonzero on `x!=0`, so the image contains a dense open set.

By Theorem 3, three copies of (13) can be chosen independently in one common
block graph.  Thus coupling scalar pair-plus-top charts still produces no
mixed-colour circuit.

## 5. Every all-axis lower-jet system has a formal diagonal state model

Let the five root tangent covectors be arbitrary coordinate axes

```text
a_i=e_(alpha_i)^*,        alpha_i in {0,1,2},          (14)
```

and put `S_i=ker a_i`.  For a nonempty root subset `I`, define

```text
C(I)={c: c notin {alpha_i:i in I}},                   (15)

F_(I,c)=tensor_(i in I) (e_c^* restricted to S_i).
```

The exact GHZ mixed derivative is

```text
T_I^GHZ=sum_(c in C(I)) F_(I,c) tensor D_c.           (16)
```

The set `C(I)` has order two when all roots of `I` have one axis type, order
one when two axis types occur, and order zero when all three occur.

For even `|I|`, use the two parity-legal companion tags

```text
A_0=empty,       A_1=Q.                               (17)
```

For odd `|I|`, use

```text
A_0={q_0},       A_1={q_1}.                           (18)
```

Order `C(I)={c_0,c_1}` when it has two elements.  Assign

```text
C_(I union A_j)=D_(c_j),
G_(A_j)=F_(I,c_j),                                    (19)
```

omitting an absent second entry and assigning no nonzero class when `C(I)` is
empty.

### Theorem 5 (formal all-axis jet realization)

Assignments (17)--(19) form one globally consistent deletion-state family
and satisfy

```text
T_I^graph=sum_A G_A tensor C_(I union A)=T_I^GHZ      (20)
```

for every nonempty root subset `I`.  Every blocker tensor appearing in the
model is one of the pure diagonals `D_0,D_1,D_2`, so all mixed blocker
coefficients vanish termwise.

Proof.  Equation (20) is immediate from (16) and (19).  It remains only to
check that two different uses do not prescribe conflicting values to one
deletion class.  The root part of the label `I union A` uniquely recovers
`I`.  Its residual part then distinguishes the two tags of the appropriate
parity.  Thus every nonzero label in (19) is globally unique, proving
consistency.

This works for every axis multiplicity, including the exceptional patterns

```text
4+1,       3+1+1,       2+2+1.                       (21)
```

It is deliberately a formal cofactor-state model.  It does not prove that the
assigned principal hafnian tensors arise from one graph.  It proves the
logical no-go needed here: deletion-class span/value equations alone cannot
exclude an all-axis pattern.  A successful proof must use a relation imposed
by common edge-block realizability, such as Theorem 1, after exposing all of
its coordinates.

## 6. Matching saturation does not select the residual pair

The axis-deficient matching theorem also cannot expose the missing pair
faces.  Let `R_c` be the roots of axis type `c` and define the maximal
axis-deficient shores

```text
S_c=R\R_c.                                             (22)
```

Consider first a **strong effective companion graph**, meaning that a
root--root block used on two tangent endpoints remains effective when one
endpoint is frozen.  A matching saturating every `S_c` then saturates every
axis-deficient subset: restrict the shore matching to the edges incident to
the smaller subset.  Generic pairwise-zero bilinear root blocks can realize
this strong modality.

### Proposition 6 (minimal viable singleton-axis topologies)

All three exceptional multiplicity patterns admit small strong companion
graphs satisfying every axis-deficient matching requirement.

1. For `4+1`, one colour is absent, so some `S_c=R`.  A minimum root-covering
   matching has two root--root edges and one root--residual edge.  It uses
   three edges and may leave one residual vertex completely isolated.
2. For `3+1+1`, write the majority class as `A={a_1,a_2,a_3}` and the
   singleton roots as `b,c`.  The maximal shores are

   ```text
   {b,c}, A union {b}, A union {c}.                    (23)
   ```

   The residual-free path

   ```text
   b--a_1--a_2--a_3--c                                (24)
   ```

   saturates all three.  So does the disjoint union of the triangle on
   `{b,c,a_1}` and the edge `a_2a_3`.
3. For `2+2+1`, write the double classes as `A={a_1,a_2}` and
   `B={b_1,b_2}`, with singleton `c`.  The maximal shores are

   ```text
   B union {c}, A union {c}, A union B.                (25)
   ```

   Both the path

   ```text
   a_2--a_1--c--b_1--b_2                              (26)
   ```

   and the disjoint union of the triangle on `{a_1,b_1,c}` with the edge
   `a_2b_2` saturate all three.

Proof.  The displayed disjoint edges give the required shore matchings
directly.  For example, in (24), `{b,c}` uses the two external legs `ba_1`
and `ca_3`, while the two four-root shores use
`ba_1,a_2a_3` and `a_1a_2,a_3c`.  The analogous matchings in (26) are
`b_1b_2,ca_1`, `a_1a_2,cb_1`, and `a_1a_2,b_1b_2`.

Without a three-edge matching covering all five roots, four root-only edges
are minimal in the last two cases.  A four-edge root graph covering five
vertices is a tree or contains the `K_3 disjoint_union K_2` shape at minimum;
pair saturation eliminates every tree shape except `P_5`.  This yields the
two displayed residual-free types without a support search.

For an even root pair `I`, the two deletion faces desired by the clean-window
route have different companion topologies:

```text
C_I:             an internal root--root pairing;
C_(I union Q):   two distinct root--residual legs.     (27)
```

Matching saturation requires a saturating matching, not both alternatives.
The `4+1` minimum can leave `q_1` isolated, and the other two patterns can
leave both residuals isolated.  Even the lower-frame count `rho(I)=2` does
not select `Q`: in a root `K_5`, a same-axis pair can obtain two companion
classes from

```text
A=empty,          A={k,l}                              (28)
```

using two frozen roots instead of the two residual endpoints.  Hence Hall,
parity, and class count do not force the residual pair face.

In the fully general theorem the effective graph can depend on `I`, because a
tangent--tangent edge need not remain effective after freezing one endpoint.
That only weakens the topology.  The strong examples above prove that the
matching conclusions themselves cannot imply a clean residual selector.

## 7. Exact next selector target

The current data hierarchy is now:

```text
same-colour top faces only             dominant;
same-colour pair plus top faces        dominant;
three diagonal colour charts          fibre-product independent;
all formal lower-root diagonal jets    realizable as deletion state;
one full 3 x 3 corrected pair block    determinant circuit.          (29)
```

Therefore the smallest useful new observation theorem must expose, for one
physical blocker pair `u,v`, the nine values

```text
z_uv(x_u^c,x_v^d)-h m_uv(x_u^c,x_v^d),
0<=c,d<=2,                                             (30)
```

or an equivalent coordinate basis of that `3 x 3` block.  Since the three
diagonal values are the scalar-chart part, the genuinely missing data are the
six off-diagonal mixed pair faces.

Possible legal mechanisms include:

- mixed blocker-word selectors that isolate one ordered colour pair;
- polarized copies of the clean shore with a full-rank nine-column
  observation matrix;
- a shared-block catalecticant whose visible maximal minor equals (2);
- an elimination theorem showing that the aggregated mixed words already
  determine the determinant, without recovering every entry.

Any proposed mechanism must defeat Theorems 3--5; otherwise it is still only
a repackaging of independently variable diagonal data.

## Scope wall

Proved:

- the full mixed-colour corrected pair matrix has rank at most two;
- its determinant is a minimal nine-coordinate algebraic circuit;
- one/two/three same-colour pair/top charts have no cross-colour equation;
- every all-axis lower-jet value system has a consistent formal diagonal
  deletion-state realization.

Not proved:

- legal exposure of the six off-diagonal pair entries in P7;
- a determinant value forced by the GHZ mixed-word equations;
- common-graph realizability of the formal axis state;
- exclusion or realization of an exceptional all-axis P7 pattern;
- the Krenn--Gu conjecture.

All five items remain **UNKNOWN/UNRESOLVED**.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_mixed_color_pair_circuit_and_axis_jet_boundary.py
python claims/p7/audit_p7_mixed_color_pair_circuit_and_axis_jet_boundary.py
uv run --with sympy --with ruff python -m ruff check verify_p7_mixed_color_pair_circuit_and_axis_jet_boundary.py audit_p7_mixed_color_pair_circuit_and_axis_jet_boundary.py
python -m py_compile verify_p7_mixed_color_pair_circuit_and_axis_jet_boundary.py audit_p7_mixed_color_pair_circuit_and_axis_jet_boundary.py
```

The primary verifier checks the generic outer-product determinant, a rank-two
point and full-rank `2 x 2` shadow, all nine circuit cofactors, the common
diagonal interpolation, and the pair/top Jacobian.  The independent no-import
audit uses exact rational determinants, direct outer products, a separate
rank routine, and deletion-label dictionaries for the three exceptional axis
patterns.  These bounded checks audit the formulas.  Equations (1), (9),
(10), (13), and the injective-label proof establish the characteristic-zero
claims.
