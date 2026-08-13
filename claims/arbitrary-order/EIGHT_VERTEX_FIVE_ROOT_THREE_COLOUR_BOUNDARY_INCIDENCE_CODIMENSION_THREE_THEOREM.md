# Eight-vertex five-root three-colour boundary-incidence codimension-three theorem

## Status

**Exact ternary characteristic-zero necessary condition at eight vertices.**
Let an eight-vertex matching tensor be a concise weighted three-colour
diagonal.  For every five-vertex set, the common zero scheme of its ten
internal bilinear edge forms is nonempty.  The full target identity forces
three stronger equations on that scheme: in each target colour, at least one
of the five root coordinates vanishes.

If all ten induced blocks are nonzero, their point in `(P^8)^10` therefore
lies in a fixed union of `120` closed incidence images, each of codimension at
least three.  In the affine ten-block space, whole-zero blocks form separate
codimension-nine branches and the resulting finite closed envelope still has
codimension at least three.

The matching ideal membership is the `n=8`, first-majority specialization of
the existing majority-subset internal-edge ideal hierarchy.  The new
proof-DAG edge combines that membership with unconditional five-root
intersection and a three-colour boundary-incidence calculation.  It is
stronger on the witness subclass than the earlier codimension-two envelope
for arbitrary five-root systems with no torus zero.

This theorem does **not** exclude the codimension-three envelope, prove that
the conditions from the `56` five-sets are independent, use the all-balanced
rank-drop minors, or resolve the Krenn--Gu conjecture.  The global conjecture
remains **UNRESOLVED**.

## 1. Five roots and the three anchored slice ideals

Work over `C`; equivalently, extend any characteristic-zero base field to an
algebraic closure.  Let

```text
Omega=S disjoint-union U,       |S|=5, |U|=3,          (1)
```

and let every local space `L_v` have dimension three.  Fix the target
coordinate covectors

```text
e_(v,0)^*, e_(v,1)^*, e_(v,2)^*.                      (2)
```

Write `e_(v,c)` for the corresponding dual coordinate vectors.

Suppose the physical matching tensor satisfies the concise weighted target
identity

```text
T_W=sum_(c=0)^2 lambda_c tensor_(v in Omega)e_(v,c)^*,
lambda_0 lambda_1 lambda_2 != 0.                       (3)
```

The normalized Krenn--Gu target has all `lambda_c=1`; allowing nonzero
weights records the exact invariant scope.

On

```text
X_S=product_(i in S) P(L_i)                            (4)
```

write

```text
b_ij(x)=W_ij(x_i,x_j),       i<j in S,
J_S=(b_ij:i<j in S),
X_c(x)=product_(i in S)e_(i,c)^*(x_i).                 (5)
```

Here `J_S` is a multihomogeneous ideal in the Cox coordinate ring of (4), and

```text
Z_S=V(J_S) subset X_S                                  (6)
```

is the five-root zero scheme.

### Theorem 1 (three-colour majority-ideal containment)

For every five-set `S` in (1),

```text
(X_0,X_1,X_2) subset J_S.                              (7)
```

Consequently `Z_S` is scheme-theoretically contained in
`V(X_0,X_1,X_2)`.  At every geometric point of `Z_S`, at least one root
coordinate vanishes in each of the three target colours.

### Proof

Fix a colour `c`.  Put `e_(u,c)` into every complement slot `u in U` and
leave the five `S` slots open.  For one perfect matching let

```text
a=# internal-S edges,
b=# crossing edges,
d=# internal-U edges.                                 (8)
```

Counting endpoints gives

```text
2a+b=5,       2d+b=3,
a=d+1>=1.                                               (9)
```

Thus every matching monomial in

```text
F_c(x)=T_W(x_S,(e_(u,c))_(u in U))                     (10)
```

contains at least one generator `b_ij`; hence `F_c belongs to J_S`.
Equation (3) gives simultaneously

```text
F_c=lambda_c X_c.                                      (11)
```

Since `lambda_c` is nonzero, `X_c belongs to J_S`.  Doing this for all three
colours proves (7).

This is exactly the `m=4,r=1` case of the committed
[`majority-subset internal-edge ideal theorem`](MAJORITY_SUBSET_INTERNAL_EDGE_IDEAL_HIERARCHY.md).
The proof uses the three complete anchored slice identities (10)--(11), not
only the three pure coordinate coefficients.  Coordinatewise, those slices
contain `3*3^5=729` target equations, of which `726` are mixed zero
equations.  The mixed equations are load-bearing.  QED.

## 2. The 120 three-colour boundary products

The
[`five-root zero-coupling intersection lemma`](FIVE_ROOT_ZERO_COUPLING_INTERSECTION_LEMMA.md)
applies to the ten forms in (5), including zero forms.  It proves

```text
Z_S != empty.                                          (12)
```

When the ten divisors meet properly, their intersection number is `24`; only
nonemptiness is needed below.

For every map

```text
f:{0,1,2}->S                                           (13)
```

put

```text
Y_f={x in X_S:
     e_(f(c),c)^*(x_(f(c)))=0 for c=0,1,2}.            (14)
```

The five constant maps give the empty projective locus, because all three
homogeneous coordinates of one root would vanish.  Every nonconstant map
gives a nonempty smooth irreducible coordinate product of codimension three:

- if `f` has image size three, three `P^2` factors become `P^1`;
- if `f` has image size two, one factor becomes a coordinate point and one
  becomes `P^1`.

Thus every nonempty `Y_f` has dimension seven.  There are

```text
5^3-5=120                                               (15)
```

such maps: `60` have fibre-size profile `(2,1)` and `60` have profile
`(1,1,1)`.

Theorem 1 gives the set-theoretic cover

```text
|Z_S| subset union_(f nonconstant) Y_f.                (16)
```

The loci in (16) may overlap, and a different `f` may be needed at every
root and for every five-set.

## 3. The projective codimension-three envelope

Assume first that all ten induced blocks on `S` are nonzero, so they define a
point of

```text
P_S=product_(i<j in S) P((L_i tensor L_j)^*)
   isomorphic to (P^8)^10,
dim P_S=80.                                             (17)
```

For every nonconstant `f`, define the incidence variety and its coefficient
image

```text
I_f={(x,B) in Y_f x P_S:
     B_ij(x_i,x_j)=0 for every i<j in S},
D_f=pr_(P_S)(I_f).                                     (18)
```

### Theorem 2 (five-root three-colour incidence obstruction)

Each `D_f` is a closed irreducible subvariety of `P_S` with

```text
dim D_f<=77,
codim_(P_S) D_f>=3.                                    (19)
```

Every ten-block system induced by an eight-vertex tensor (3), with all ten
blocks nonzero as assumed above, lies in the fixed closed envelope

```text
C_S=union_(f nonconstant) D_f,                         (20)
```

which has codimension at least three in `P_S`.

### Proof

For fixed `x in Y_f`, the rank-one tensor `x_i tensor x_j` is nonzero for
every edge.  Evaluation at it is therefore one nonzero linear functional on
the corresponding `P^8` block.  The fibre of `I_f -> Y_f` is exactly

```text
(P^7)^10.                                              (21)
```

It follows that `I_f` is an irreducible product of ten projective hyperplane
bundles over the irreducible sevenfold `Y_f`, and

```text
dim I_f=7+10*7=77.                                     (22)
```

The projection in (18) is projective, hence proper, so `D_f` is closed.  Its
dimension is at most that of `I_f`, proving (19).

By (12), choose `x in Z_S`.  Theorem 1 places `x` in some nonempty `Y_f`.
Then `(x,B) in I_f`, so `B in D_f subset C_S`.  A finite union of closed
sets of codimension at least three has the same lower codimension bound,
proving (20).  QED.

No generic finiteness is asserted for `I_f -> D_f`; `D_f` may have
codimension greater than three.  The envelope is only necessary.  A general
member of `D_f` need not be a witness, need not have all five-root solutions
on the three-colour boundary, and may have torus roots as well.

## 4. Affine blocks and the full graph space

Let

```text
A_S=product_(i<j in S) (L_i tensor L_j)^*
   isomorphic to (C^9)^10,
dim A_S=90.                                             (23)
```

On the open `A_S^o` where every block is nonzero, independent block
projectivization

```text
q:A_S^o -> P_S                                         (24)
```

has `(C^*)^10` fibres.  Therefore

```text
dim q^(-1)(D_f)<=77+10=87.                             (25)
```

Its closure in `A_S` has the same dimension bound.  The locus on which one
whole `3 x 3` block is zero is a linear subspace of codimension nine.  Hence

```text
C_S^aff
 = union_f closure_(A_S)(q^(-1)(D_f))
   union union_(i<j in S){W_ij=0}                      (26)
```

is a fixed closed subset of codimension at least three in `A_S`, and every
induced ten-block system from (3) lies in it.

The map from the full affine `28`-block space to `A_S` is a surjective linear
projection.  Pullback therefore preserves this codimension bound for each
fixed `S`.  A hypothetical eight-vertex witness lies in all `binomial(8,5)=56`
such pullbacks, but no transversality or independence among those `56`
conditions is proved.  Their codimensions must not be added.

## 5. Relation to adjacent balanced cuts

Two balanced four-shores differing by one vertex have a five-vertex union.
Theorem 2 is therefore a gauge-invariant consequence available whenever one
tries to compare adjacent cuts.  It replaces an invalid demand that their
two prescribed same-vector root ideals have compatible basepoints.

Stronger still, no balanced maximal-minor equation was used: Theorems 1--2
hold for every eight-vertex witness, not only for the all-balanced rank-drop
branch.  The new S3 obligation is to intersect (26), for overlapping
five-sets, with the balanced maximal-minor equations and the remaining mixed
target equations.  The exact coordinate-boundary and nontransverse
five-root classifications are the natural next strata.

The companion
[`adjacent-cut monomial mixed-shell sharpness theorem`](EIGHT_VERTEX_ADJACENT_CUT_MONOMIAL_HAMMING_ONE_BLINDNESS_AND_HAMMING_TWO_DETECTOR_SHARPNESS_THEOREM.md)
shows why first mixed derivatives do not recover prescribed same-vector
basepoints: an exact all-rank-drop control has empty fixed-gauge base loci on
two adjacent shores and satisfies every Hamming-one mixed equation.  Pair-
local Hamming-two equations detect that synchronized monomial control class,
but do not add another universal equation to (7) without a new elimination
argument.

## 6. Proof-topology consequence

The exact status is

```text
five-root zero scheme on every five-set:               NONEMPTY;
three colour products lie in its internal-edge ideal: PROVED;
all-ten-nonzero induced K5 envelope in (P^8)^10:      CODIMENSION >= 3;
affine envelope including zero blocks:                 CODIMENSION >= 3;
all-balanced rank-drop equations used:                 NO;
independence across the 56 five-sets:                   NOT CLAIMED;
eight-vertex witness exclusion:                        OPEN;
all-balanced witness exclusion:                        OPEN;
global Krenn--Gu conjecture:                           UNRESOLVED.          (27)
```

The closest earlier coefficient-space result put the ambient no-torus locus
inside a codimension-at-least-two envelope.  Theorem 2 is not a replacement
for that theorem: it uses the witness slice identities and confines a
smaller class by the simultaneous three-colour condition.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_eight_vertex_five_root_three_colour_boundary_envelope_and_adjacent_cut_sharpness.py
python -I claims/arbitrary-order/audit_eight_vertex_five_root_three_colour_boundary_envelope_and_adjacent_cut_sharpness.py
python -m py_compile claims/arbitrary-order/verify_eight_vertex_five_root_three_colour_boundary_envelope_and_adjacent_cut_sharpness.py claims/arbitrary-order/audit_eight_vertex_five_root_three_colour_boundary_envelope_and_adjacent_cut_sharpness.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_eight_vertex_five_root_three_colour_boundary_envelope_and_adjacent_cut_sharpness.py claims/arbitrary-order/audit_eight_vertex_five_root_three_colour_boundary_envelope_and_adjacent_cut_sharpness.py
python claims/arbitrary-order/verify_majority_subset_internal_edge_ideal.py
python claims/arbitrary-order/audit_majority_subset_internal_edge_ideal.py
python claims/arbitrary-order/verify_five_root_zero_coupling_intersection.py
```

The SymPy primary enumerates all `105` eight-vertex matchings, checks their
`60+45` majority sectors, recomputes the five-root intersection degree `24`,
enumerates the `120` nonempty boundary products, and audits the projective and
affine dimensions.  The standard-library audit imports neither SymPy nor the
primary; it uses a reverse-pivot matching recursion, endpoint-assignment
dynamic programming, and separate incidence arithmetic.  Both scripts also
replay the separately scoped adjacent-cut sharpness theorem.

The arbitrary-field ideal membership, projective incidence argument, and
proper-image dimension bound are the written proof.  The bounded scripts
audit the discrete counts, exact fixture, and conventions; they are not a
finite enumeration of the witness locus.

## Dependencies and lineage

- [`MAJORITY_SUBSET_INTERNAL_EDGE_IDEAL_HIERARCHY.md`](MAJORITY_SUBSET_INTERNAL_EDGE_IDEAL_HIERARCHY.md)
- [`FIVE_ROOT_ZERO_COUPLING_INTERSECTION_LEMMA.md`](FIVE_ROOT_ZERO_COUPLING_INTERSECTION_LEMMA.md)
- [`FIVE_ROOT_NO_TORUS_CODIMENSION_TWO_THEOREM.md`](FIVE_ROOT_NO_TORUS_CODIMENSION_TWO_THEOREM.md)
- [`FIVE_ROOT_BOUNDARY_TRANSVERSAL_BLOCKER_CLASSIFICATION.md`](FIVE_ROOT_BOUNDARY_TRANSVERSAL_BLOCKER_CLASSIFICATION.md)
