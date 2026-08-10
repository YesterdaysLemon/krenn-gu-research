# Cross-depth hafnian derivatives and the projective marked-star boundary

## Status

**Exact characteristic-zero recurrence, exact marked-sector criterion, and
exact projective no-go.**  There is a universal principal-hafnian operation
that crosses from a root-pair cofactor with no blocker deletions to a pair
cofactor with five blocker deletions: differentiate with respect to the
three complementary blocker--blocker edges after applying the clean-shore
matching operator.  All six pair faces then occur with the same nonzero
shore factor.

That operation is an **edge derivative**.  It is not supplied by a scalar
change of a local physical vector.  In an actual five-root matching sector,
the corresponding pair face is instead multiplied by a `2 x 2` permanent of
the two remaining root-to-window rows.  Four standard unit marked stars from
one root pair require all six of these permanents to have one common nonzero
value.

In the projectively constant root branch the differentiated root--blocker
maps vanish.  The entire `2 x 4` matrix is therefore zero, so every physical
cross-depth marked sector vanishes.  Consequently the natural edge-derivative
recurrence has zero physical implementation inside the 31 nonempty
projective root jets.  A nonprojective root direction, an edge-specific
marked circuit, or an additional synchronized companion depth is genuinely
necessary for this route.

This does not exclude a general `P_7` witness: the full equations may force a
nonprojective marked sector or a different selector.  It also does not make
an edge derivative into a legal graph operation.  The jet-orthogonal splice
and the physical free-`h` response remain exact controls.  The `P_7`
restriction problem and the Krenn--Gu conjecture remain **UNRESOLVED**.

No graph, support, matching-family, colour-word, or tuple enumeration is
used.

## 1. The universal edge-derivative recurrence

Let `K` be a characteristic-zero field and let `A=(a_uv)` be a loopless
symmetric matrix indexed by a finite set `V`.  For every even `S subset V`
write

```text
h_S=haf A[S],                 h_empty=1.              (1)
```

For distinct `u,v in S`, differentiation of the matching polynomial gives

```text
partial_(a_uv) h_S=h_(S minus {u,v}).                 (2)
```

Every matching contains `uv` at most once, and deleting that edge is a
weight-preserving bijection onto the matchings of `S minus {u,v}`.  Thus (2)
is an identity of polynomials, not a generic or nonvanishing assertion.

There is a useful simultaneous form.  Let `J,D subset S` be disjoint sets of
the same size and define the shore operator

```text
L_(J,D)
 =sum_(sigma:J -> D bijective)
    product_(j in J)
      a_(j,sigma(j)) partial_(a_(j,sigma(j))).        (3)
```

### Theorem 1 (principal-hafnian shore recurrence)

For every even `S` containing `J union D`,

```text
L_(J,D) h_S
 =per A[J,D] h_(S minus (J union D)).                 (4)
```

Proof.  A product of edge derivatives in one summand of (3) retains exactly
the matchings containing that shore bijection.  Removing its edges leaves an
arbitrary perfect matching of the complement.  Distinct shore bijections
cannot occur in the same perfect matching.  Restoring their edge weights and
summing gives the permanent in (4).

Equivalently, multiply only the `J--D` edges by a marker `t`.  Formula (4) is
the coefficient of `t^|J|`.  More generally, for deletion sets `E subset F`
with even `Delta=F minus E`, multiplying the edges induced by `Delta` by `t`
gives the interval formula

```text
[t^(|Delta|/2)] haf A(t)[V minus E]
 =haf A[Delta] haf A[V minus F].                      (5)
```

This is the strongest top-degree transfer across an arbitrary principal-
deletion interval: maximal marker degree forces a perfect matching of all of
`Delta`, after which the complement matches independently.

## 2. Exact P7 depth-zero to depth-five transfer

Use

```text
R=J disjoint_union I,       |J|=3, |I|=2,
B=D disjoint_union W,       |D|=3, |W|=4,
Q={q_0,q_1}.                                           (6)
```

Suppose the clean-shore theorem supplies

```text
f=per A[J,D] !=0.                                     (7)
```

For a pair `e subset W`, put `p=W minus e`, also a pair.  In the active
cofactor notation,

```text
C_I       =haf A[V minus I],
C_(IuQ)   =haf A[V minus (I union Q)],
z_e       =haf A[Q union e],
m_e       =haf A[e].                                  (8)
```

Apply (2) after (4).  Since deleting `p` from `Q union W` leaves `Q union e`,
while deleting it from `W` leaves `e`, one obtains

```text
partial_(a_p) L_(J,D) C_I     =f z_e,
partial_(a_p) L_(J,D) C_(IuQ) =f m_e.                 (9)
```

### Theorem 2 (common-normalization cross-depth recurrence)

All six depth-five pair faces `(z_e,m_e)`, `e in binom(W,2)`, are the six
complementary edge derivatives (9) of the two depth-zero root-pair cofactors,
with one common nonzero multiplier `f`.

In particular they obey the division-free rank-one syzygies

```text
m_e partial_(a_p)L C_I
 -z_e partial_(a_p)L C_(IuQ)=0,                       (10)
```

and every two choices of shore have the corresponding `2 x 2` proportionality
minor.  These are genuine principal-hafnian identities on a common physical
matrix.

For `a in W`, let

```text
T_(W,a)=sum_(p subset W minus {a}, |p|=2) partial_(a_p). (11)
```

The complement `e=W minus p` contains `a`, so (9) gives the standard
marked-star rows

```text
T_(W,a)L C_I     =f sum_(e contains a) z_e,
T_(W,a)L C_(IuQ) =f sum_(e contains a) m_e.           (12)
```

Thus compatible normalization is not an algebraic mystery: the hafnian
derivative calculus supplies exactly the unit incidence matrix used by the
tetrahedral tomography theorem.  The remaining question is whether (11) is
a legal observation of the unchanged graph.

## 3. What an actual two-root marked sector supplies

Fix tangent directions at the two roots in `I` and the already selected
directions at the four ports in `W`.  Their scalar incidence matrix is

```text
K_IW=[a_1 a_2 a_3 a_4]
     [b_1 b_2 b_3 b_4].                               (13)
```

If the roots in `I` match a pair `p={u,v} subset W`, the exact sector weight
is

```text
kappa_p=per K_IW[:,{u,v}]=a_u b_v+a_v b_u.            (14)
```

After the independent `J--D` shore matching, the remaining vertices are
`Q union e`, where `e=W minus p`.  Hence this physical five-root sector is

```text
f kappa_p z_e.                                        (15)
```

There are no omitted signs or matching multiplicities: the shore bijection,
the root-pair bijection, and the residual cofactor use disjoint vertices.

### Theorem 3 (one-root-pair marked-star normalization criterion)

For a fixed `a in W`, the actual root pair gives a nonzero scalar multiple of
the standard `z`-star at `a` exactly when

```text
kappa_p=gamma_a !=0
for all p subset W minus {a}, |p|=2.                  (16)
```

The same root pair gives all four standard stars, allowing an independent
nonzero row normalization for each star, if and only if

```text
kappa_12=kappa_13=kappa_14=kappa_23=kappa_24=kappa_34
          =gamma !=0.                                 (17)
```

Proof.  Equation (15) is the coefficient of `z_(W minus p)`.  The three
complement pairs `W minus p` are precisely the three edges incident to `a`,
so (16) is necessary and sufficient.  Any two of the four complementary
triangles share an edge.  Their row scalars must therefore agree, and the
four conditions together are exactly (17).

Condition (17) is attainable: taking both rows of (13) equal to
`(1,1,1,1)` gives `kappa_p=2` for all `p`.  It is not automatic.  For example,

```text
K_IW=[1 0 1 0]
     [0 1 1 2]                                        (18)
```

has permanental pair vector

```text
(kappa_12,kappa_13,kappa_14,kappa_23,kappa_24,kappa_34)
 =(1,1,2,1,0,2),                                     (19)
```

so not even a nonzero four-star normalization exists.  Since physical edge
blocks on distinct root--port pairs are independent bilinear blocks, (18)
can coexist with the same nonzero shore (7).  Pure-shore nonvanishing alone
does not force (17).

## 4. The projective branch kills the differential

The projectively constant root--blocker hypothesis is

```text
B_(r,u)(y,-)=0
for every root r, blocker u, and tangent y in S_r.     (20)
```

For a differentiated root pair `I`, (20) says exactly that the matrix (13)
is zero on every chosen window.  Therefore

```text
kappa_p=0                         for all p subset W. (21)
```

### Theorem 4 (projective cross-depth no-go)

Inside the projectively constant branch, every physical five-root marked
sector (15) from a nonempty root-pair jet to a five-blocker-deletion pair
face is zero.  Hence neither (9) nor the marked stars (12) are legal
consequences of the 31 nonempty projective root jets.

This explains the zero elimination theorem structurally.  Formal edge
differentiation crosses the cofactor-depth grading, but the physical root
directions that would have to implement it have zero root--blocker incidence.
The differential on the projective page is identically zero.

The conclusion is restricted to this branch.  It does not rule out a
nonprojective root pair, an extra companion channel, a mixed blocker probe,
or an edge-specific marked gadget.

## 5. Why an edge derivative is not a local scalar probe

If a local physical vector at vertex `u` is multiplied by `t`, every incident
edge evaluation is multiplied by `t`.  Every perfect matching uses exactly
one edge at `u`, so

```text
haf A[S](...,t x_u,...)=t haf A[S](...,x_u,...).      (22)
```

More generally, vertex gauges `x_u -> t^(c_u)x_u` multiply every matching by
the same factor `t^(sum_(u in S)c_u)`.  They cannot distinguish the three
complement edges in (11) from residual, root, or other blocker edges.

By contrast, `partial_(a_p)` changes one physical edge block while holding
all other blocks fixed.  Therefore (9)--(12) are legal only if an actual
multilinear selector reproduces that edge derivative on the relevant
cofactor family.  The root-pair mechanism gives the weighted replacement
(14)--(15), and Theorem 3 is its exact normalization test.

## 6. Residual-depth and countermodel checks

The actual sector (15) leaves the two residual vertices `Q`, so it exposes
`z_e`, not `m_e`.  Deleting `Q` as well needs a synchronized companion depth.
The formal second identity in (9) starts from `C_(I union Q)`; the current
`q=2` root budget does not manufacture that depth-five observation.  Thus the
recurrence does not bypass the proved absence of the direct pair layer.

The two sharp controls survive exactly.

1. In the jet-orthogonal splice, differentiated root--blocker edges vanish,
   so (21) holds.  Its depth-five pair labels are formal independent
   coordinates, and Theorem 4 correctly supplies no relation on them.
2. In the physical free-`h` response

   ```text
   M=1+x_1x_2,             Z=lambda,                 (23)
   ```

   every nonempty `z_e` is zero.  Hence every physical marked sector (15)
   and every residual-present star in (12) is zero for all `lambda`.  The
   missing scalar remains free.  The formal direct derivative in (9) is not
   a legal synchronized observation, exactly as the root-budget theorem
   requires.

Neither control is contradicted or silently strengthened.

## Strongest exact consequence

The cross-depth problem now separates into two statements:

```text
principal-hafnian edge derivative:
  depth 0 -> depth 5 with common shore normalization, PROVED;

physical projective root jet:
  its implementing incidence weights are all zero,   PROVED. (24)
```

A successful P7 argument must therefore prove at least one of:

1. a nonprojective root pair with a nonzero weighted-star observation matrix
   of sufficient rank (unit condition (17) is sufficient, not necessary);
2. a legal edge-specific circuit implementing the derivatives (11);
3. a synchronized companion depth that exposes the direct pair family; or
4. a different cross-depth principal-hafnian identity not generated by the
   projective root--blocker incidences.

## Scope wall

```text
single-edge hafnian derivative recurrence:             PROVED;
arbitrary deletion-interval top coefficient:           PROVED;
clean-shore depth-zero/depth-five normalization:        PROVED AS EDGE DERIVATIVE;
division-free pair syzygy (10):                         PROVED;
actual two-root marked-sector weight (15):              PROVED;
common four-star criterion (17):                        PROVED;
criterion forced by a nonzero pure shore:               FALSE;
projective root-to-window marked sectors:               ALL ZERO;
edge derivative supplied by local scalar rescaling:     FALSE;
edge derivative supplied by a new legal marked circuit: UNKNOWN;
nonprojective weighted fan rank sufficient for recovery: UNKNOWN;
synchronized direct m-pair depth at q=2:                UNKNOWN;
jet-orthogonal splice excluded:                         FALSE;
free-h response excluded:                               FALSE;
P7 nonrestriction:                                      UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

## Replay

Run from the repository root:

```powershell
uv run --with sympy python claims/p7/verify_p7_cross_depth_hafnian_derivative_and_projective_marked_star_boundary.py
python claims/p7/audit_p7_cross_depth_hafnian_derivative_and_projective_marked_star_boundary.py
python -m py_compile claims/p7/verify_p7_cross_depth_hafnian_derivative_and_projective_marked_star_boundary.py claims/p7/audit_p7_cross_depth_hafnian_derivative_and_projective_marked_star_boundary.py
uv run --with ruff ruff check claims/p7/verify_p7_cross_depth_hafnian_derivative_and_projective_marked_star_boundary.py claims/p7/audit_p7_cross_depth_hafnian_derivative_and_projective_marked_star_boundary.py
```

The primary verifier checks a generic symbolic shore recurrence, the exact
P7 complement/star incidence, both normalization controls, the projective
zero specialization, the rank-one syzygy, and the free-`h` boundary.  The
independent no-import audit reconstructs the polynomial recurrence with
monomial dictionaries and checks the P7 incidence and normalization
conditions using separate integer arithmetic.  Neither script imports the
other or enumerates graph families, blocker supports, colour words, or large
tuple sets.
