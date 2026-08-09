# Target incidence has a determinant-cleared P7 hafnian integrability test

## Status

**Exact characteristic-zero conditional reconstruction theorem and low-degree
obstruction hierarchy.**  Let `Gamma` be the named `243 x 219` full mixed-root
companion map for five roots and nine nonroots, with columns indexed by
deletion sets of sizes five, three, and one.  Suppose `Gamma` has rank 219 and
a diagonal target `J_lambda` lies in its image:

```text
Gamma C=J_lambda.                                      (1)
```

Then `C` is unique.  Complementing deletion labels turns it into supplied
principal-hafnian candidates

```text
h_I=C_(N minus I),       |I| in {4,6,8}.               (2)
```

This note gives a division-free test for whether those 219 numbers are the
three principal-hafnian decks of one symmetric nine-vertex graph.  On a
fixed pinned-open chart, eight Cramer star inversions produce all 36 edge
candidates.  Principal-hafnian realizability is then equivalent to:

1. the 126 four-set matching equations;
2. one pinned partner/Hadamard row equation for each of the 84 six-sets;
3. one pinned partner/Hadamard row equation for each of the nine eight-sets.

All denominators are cleared explicitly.  The first useful necessary tests
are degree-nine polynomials in the unique cofactor numerators, not a generic
elimination in 219 variables.  Once the three displayed families vanish,
every other partner expansion, Hadamard row stress, and Euler stress follows
from one reconstructed graph.

This is a **relative companion-data theorem**.  `Gamma`, its named column
normalizations, and a nonzero sensor minor must be known.  The theorem does
not reconstruct unknown companion blocks from `J_lambda`, does not show that
the GHZ target-incidence locus meets the pinned-open locus, and does not show
that GHZ forces any of the integrability equations.  The explicit full sensor
currently in the repository is disjoint from the nonzero diagonal target
space.  `P_7` and global Krenn--Gu remain **UNRESOLVED**.

## 1. The unique relative cofactor vector

Let `N={0,...,8}`.  Choose 219 tensor-coordinate rows `R` for which

```text
B=Gamma[R,:],             beta=det B != 0.             (3)
```

Define the Cramer numerator vector

```text
v=adj(B) J_lambda[R].                                  (4)
```

For every tensor row `t` outside `R`, put

```text
T_t=beta (J_lambda)_t-Gamma[t,:] v.                    (5)
```

### Lemma 1 (determinant-cleared target incidence)

On `beta!=0`, equation (1) holds if and only if every residual (5) vanishes.
When it holds,

```text
C=v/beta.                                              (6)
```

### Proof

The selected rows give `B C=J_lambda[R]`.  Cramer's identity
`B adj(B)=beta I` makes their unique solution `v/beta`.  The omitted row of
`Gamma(v/beta)=J_lambda` is exactly (5) divided by `beta`.

Write `v_I=v_(N minus I)` for the numerator carrying a remaining set `I` of
size four, six, or eight.  These are not absolute hafnian values: the actual
candidate is `h_I=v_I/beta`.

## 2. Eight oriented pinned inversions recover all edges

Fix the vertex order `0<...<8`.  For each pin `p=0,...,7`, order the eight
other vertices increasingly and order their five-subsets lexicographically.
Use the fixed row indices

```text
P=(0,1,2,3,4,10,20,35).                               (7)
```

For a row five-set `T` and a column vertex `s!=p`, define

```text
Nhat_p[T,s] = v_(T minus {s})  if s in T,
               0                otherwise,             (8)

bhat_p[T] = v_({p} union T).                           (9)
```

In (8), the remaining set has size four; in (9), it has size six.  Restrict
to the eight rows in (7), and put

```text
d_p=det Nhat_p,
u_p=adj(Nhat_p) bhat_p.                               (10)
```

The pinned-open condition is

```text
D_pin=product_(p=0)^7 d_p != 0.                       (11)
```

At the all-one nonroot graph, every `d_p` is a nonzero scalar multiple of
the fixed `W_(1,5)(8)` minor of determinant five, so (11) defines a nonempty
open chart.

The actual pinned matrix built from `C=v/beta` is `Nhat_p/beta`.  Its
determinant and Cramer numerator are respectively `d_p/beta^8` and
`u_p/beta^8`.  The common factor cancels.  Orient every edge by its smaller
endpoint and define

```text
a_pq=(u_p)_q/d_p,             p<q.                    (12)
```

Pins `0,...,7` cover all 36 edges, so no ninth inversion is needed.  Formula
(12) is invariant under common rescaling of the 219-vector `v`.

## 3. The first determinant-cleared obstructions

For any six-set `S` and any pin `p in S`, the partner expansion of a physical
deck is

```text
h_S=sum_(s in S minus {p}) a_ps h_(S minus {p,s}).     (13)
```

Using the star reconstructed at `p`, clear its one determinant:

```text
H6_(p,S)
 =d_p v_S-sum_(s in S minus {p}) (u_p)_s v_(S minus {p,s}). (14)
```

Likewise, for every eight-set `Q` containing `p`,

```text
H8_(p,Q)
 =d_p v_Q-sum_(s in Q minus {p}) (u_p)_s v_(Q minus {p,s}). (15)
```

Each term in (14) and (15) has ordinary degree nine in the numerator deck:
`d_p` has degree eight, and each coordinate of `u_p` has degree eight.
Neither polynomial involves `beta`.  Rows used in (7) make the corresponding
instances of (14) Cramer identities; every other row is a genuine
compatibility test.

### Proposition 2 (first low-degree obstruction)

If any nonselected polynomial (14), or any polynomial (15), is nonzero, the
unique relative cofactor vector in (6) is not a principal-hafnian tower of a
single graph on the pinned-open chart.

This is the smallest natural determinant-cleared test in the reconstruction
hierarchy: it uses one pin determinant and one partner row.  No claim of
absolute minimal polynomial degree in the full incidence ideal is made.

A physical tower also makes independently reconstructed opposite stars
agree.  If the ninth pin is retained, the corresponding symmetry stress is

```text
O_pq=d_q (u_p)_q-d_p (u_q)_p.                         (16)
```

This degree-16 test is useful diagnostically, but is not needed by the
oriented reconstruction theorem below.

Equivalently, one may reconstruct all nine stars first.  Then every
nonselected instance of (14) and every overlap (16) is a necessary
projective line test.  The minimal oriented criterion later omits these
redundant equations: once its four-deck realization and one partner row per
upper coordinate hold, all reverse-star and unused-row equations follow.

## 4. Hadamard and Euler stresses

For an even set `S`, let its cofactor matrix have off-diagonal entries

```text
K^S_ij=h_(S minus {i,j}).                              (17)
```

The partner identities are the Hadamard row stress

```text
(A[S] Hadamard K^S) 1=h_S 1.                          (18)
```

Summing its rows twice-counts every edge and gives Euler's hafnian identity

```text
sum_(e subset S) a_e h_(S minus e)=k h_S,
|S|=2k.                                               (19)
```

Equations (14)--(15) are single determinant-cleared rows of (18).  The
Euler forms provide symmetric necessary checks.  For an even set `S`, put

```text
D_S=product_(p in S minus {max S}) d_p.                (20)
```

Every oriented edge denominator in `S` divides `D_S`.  Therefore the
numerator Euler stresses are

```text
E6_S=3 D_S v_S
     -sum_(p<q in S) (u_p)_q (D_S/d_p) v_(S minus {p,q}),  (21)

E8_S=4 D_S v_S
     -sum_(p<q in S) (u_p)_q (D_S/d_p) v_(S minus {p,q}).  (22)
```

In (21) the lower values are four-set numerators; in (22) they are six-set
numerators.  Common powers of `beta` cancel exactly.  A nonzero Euler stress
is another immediate obstruction.  The partner-row tests are algebraically
smaller because they use only one `d_p`.

## 5. Determinant-cleared four-hafnian realization

The pinned systems alone are homogeneous in the supplied decks and do not
fix their absolute cofactor scale.  Four-hafnian realization supplies that
missing condition.

For a four-set `I={i<j<k<l}`, put

```text
D_I=d_i d_j d_k.                                      (23)
```

Using the oriented edges (12), the identity

```text
h_I=a_ij a_kl+a_ik a_jl+a_il a_jk                    (24)
```

is equivalent to the polynomial

```text
F_I=D_I v_I
    -beta [d_j (u_i)_j (u_k)_l
           +d_k (u_i)_k (u_j)_l
           +d_k (u_i)_l (u_j)_k]=0.                  (25)
```

The factor `beta` is essential.  The edges (12) are invariant when all
cofactor numerators are rescaled, whereas the physical four-hafnians are
not.  Thus (25) fixes the target amplitude relative to the named companion
normalization.  Omitting `beta` would confuse the relative cofactor vector
`v` with the absolute vector `C=v/beta`.

## 6. Conditional graph-side reconstruction theorem

### Theorem 3 (target-incidence plus pinned-open integrability)

Assume characteristic zero, `beta!=0`, all target-incidence residuals (5)
vanish, and `D_pin!=0`.  Define the symmetric edge graph `A` by (12).  Then
the unique vector `C=v/beta` in (1) is exactly the complete principal
`h_4,h_6,h_8` tower of `A` if and only if all of the following hold:

```text
F_I=0   for every four-set I;                          (26)
H6_(min S,S)=0 for every six-set S;                    (27)
H8_(min Q,Q)=0 for every eight-set Q.                  (28)
```

Thus the target-incidence problem on this chart reduces to explicit
determinants, adjugate-vector products, and matching sums.  It requires no
elimination over free cofactor variables.

### Proof

If `C` is a principal-hafnian tower, every selected pinned system is a
partner expansion of its graph.  Cramer's rule recovers the actual oriented
edges, so (25), (14), and (15) all vanish.

Conversely, (26) and (25) say that every supplied four-set value is the
four-hafnian of the reconstructed graph.  Fix a six-set `S` and expand the
hafnian of `A[S]` by its least vertex.  Equation (27), after division by the
nonzero `d_(min S)` and restoration of `C=v/beta`, says that the supplied
`h_S` equals that expansion.  Hence the whole six-deck is correct.  The same
argument with (28), now using the established six-deck, proves every supplied
eight-set value.  This proves sufficiency.

Once (26)--(28) hold, all opposite-pin reconstructions equal the same graph,
every stress (16), every row of (18), and every Euler stress (21)--(22)
vanishes automatically.  Only one partner row per upper-deck coordinate was
needed for the equivalence.

## 7. The sensor-dependent cofactor-line reduction

The generic target-incidence theorem in
`FIVE_ROOT_DIAGONAL_TARGET_INCIDENCE_SCHUBERT_DUALITY_AND_COFACTOR_LINE_THEOREM.md`
has an especially economical form.  Let `pi_Delta` be projection of the
243-dimensional tensor space modulo the three-dimensional diagonal target
space, and suppose

```text
K_Gamma=ker(pi_Delta Gamma)                            (29)
```

is one-dimensional.  Choose a nonzero named generator `w`.  Every nonzero
diagonal completion carried by this sensor then has

```text
C=t w,             J=t Gamma w,        t != 0.         (30)
```

The line `K_Gamma`, and hence every test below, depends on `Gamma`.  There is
no ambient Gamma-independent cofactor relation being asserted.

Build `d_p(w)` and `u_p(w)` by (8)--(10).  Common scaling obeys

```text
d_p(tw)=t^8 d_p(w),
u_p(tw)=t^8 u_p(w),
a_pq(tw)=a_pq(w),                                      (31)

H6_(p,S)(tw)=t^9 H6_(p,S)(w),
H8_(p,Q)(tw)=t^9 H8_(p,Q)(w).                         (32)
```

Thus a nonzero degree-nine stress at `w` excludes the **entire** nonzero
target-incidence line.  If all those projective stresses vanish, only the
absolute hafnian amplitude remains.

For `I={i<j<k<l}`, define

```text
M_I(w)=d_j(w) (u_i(w))_j (u_k(w))_l
      +d_k(w) (u_i(w))_k (u_j(w))_l
      +d_k(w) (u_i(w))_l (u_j(w))_k.                  (33)
```

Substitution of `C=tw` into the absolute four-hafnian equation and removal
of the common nonzero factor `t^24` leaves the affine-linear amplitude test

```text
t D_I(w) w_I-M_I(w)=0.                                (34)
```

Because the pinned-open condition forces some four-set coordinate of `w` to
be nonzero, at least one equation (34) has a nonzero coefficient of `t`.
It determines at most one target amplitude.  Every other four-set must give
the same amplitude; if `w_I=0`, its required condition is `M_I(w)=0`.

### Corollary 4 (one-line conditional reconstruction)

Assume `dim K_Gamma=1` and the pinned determinants of a generator `w` are
nonzero.  A nonzero point `C=tw` of the target-incidence line is a principal
`h_4,h_6,h_8` tower if and only if:

1. `H6_(min S,S)(w)=0` for every six-set `S`;
2. `H8_(min Q,Q)(w)=0` for every eight-set `Q`; and
3. the single amplitude `t` satisfies every linear equation (34).

The reconstructed graph depends only on the projective line `[w]`; the
four-deck fixes its unique possible affine normalization.  For a prescribed
diagonal target, its already-determined value of `t` must equal that
normalization.  In particular, a radial target-incidence line meets the
physical shallow-deck image in **at most one nonzero point** on the
pinned-open chart.  This is a sensor-dependent line test, not a search or
elimination over 219 independent cofactors.

## 8. Relative-data and GHZ boundary

The theorem is invariant under the choice of nonzero sensor row minor on
overlaps: changing `R` rescales the Cramer representation of the same unique
vector `C`, and the reconstructed graph and zero/nonzero conclusions agree.
It is **not** invariant under forgetting the named companion basis.  A
general `GL(219)` change mixes deletion sizes and labels, destroying the
principal-hafnian meaning of (2).  Even diagonal column rescalings must be
tracked as part of the companion normalization.

An overall target rescaling `J_lambda -> t J_lambda` rescales `v` but leaves
the rational edges (12) unchanged.  The homogeneous partner and Euler
stresses scale uniformly, while (25) imposes the absolute amplitude needed
for an honest hafnian deck.  This separates the projective sensor problem
from the affine graph-realizability problem.

The exact remaining intersection is

```text
target incidence (5), equivalently a sensor-dependent line when (29) holds,
  intersect pinned open (11)
  intersect zero set of (26)--(28).                    (35)
```

No point of (29) satisfying the GHZ witness requirements is currently
known, and no theorem proves that (29) is empty.  The result turns that
question into a structured symbolic incidence problem but does not settle
it.

## 9. Scope wall

```text
full-rank named Gamma gives unique relative C:          EXACT;
target incidence outside one sensor minor:             EQUATIONS (5);
eight pinned inversions recover 36 oriented edges:     RATIONAL ON OPEN;
first determinant-cleared partner obstruction:         DEGREE 9 IN v;
Hadamard/Euler necessary stresses:                     EXACT;
h8 consistency after h4/h6 reconstruction:            NINE ROW TESTS;
conditions (26)--(28) characterize graph-side tower:   PROVED ON OPEN;
one-dimensional target incidence reduces to line test: PROVED;
degree-nine stress excludes a whole nonzero line:       PROVED;
four-deck fixes at most one line amplitude:             PROVED;
radial line meets physical shallow-deck image <=1 time: PROVED ON OPEN;
ambient Gamma-independent cofactor relation:            NOT CLAIMED;
generic 219-variable elimination used:                 NO;
companion blocks reconstructed from target alone:      NO;
named column normalization dispensable:                FALSE;
explicit full sensor meets nonzero diagonal target:    FALSE;
GHZ fibre meets target-incidence plus pinned open:      UNKNOWN;
GHZ forces determinant-cleared integrability:          UNKNOWN;
P7 obstruction or construction:                       UNKNOWN;
global Krenn--Gu:                                      UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_target_incidence_determinant_cleared_hafnian_integrability.py
python claims/p7/audit_p7_target_incidence_determinant_cleared_hafnian_integrability.py
python -m py_compile verify_p7_target_incidence_determinant_cleared_hafnian_integrability.py audit_p7_target_incidence_determinant_cleared_hafnian_integrability.py
uv run --with ruff ruff check verify_p7_target_incidence_determinant_cleared_hafnian_integrability.py audit_p7_target_incidence_determinant_cleared_hafnian_integrability.py
```

The primary verifier checks Cramer target incidence, the `v=beta C` scaling,
all determinant-cleared four-, six-, eight-, Hadamard-, and Euler identities
on a fixed nonconstant nine-vertex graph, and exact detection after perturbing
one unselected six- or eight-deck coordinate.  The independent standard-
library audit repeats the construction with Bareiss determinants and its own
recursive hafnian implementation.  Both are fixed symbolic replays, not
searches over graphs, supports, targets, or parameter families.
