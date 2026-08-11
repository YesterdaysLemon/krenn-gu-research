# Hostile review of the arbitrary permanent co-two sensor rank-drop theorem

## Verdict and provenance

**PASS, as an exact necessary boundary rather than a nonrestriction theorem.**
For every characteristic-zero weighted diagonal restriction

```text
P_r -> Delta_3,              r>=3,
```

and every omitted pair of modes, the complementary `r-2` local planes have
product span of dimension at most `binomial(r,2)-1`.  The stronger tradeoff

```text
dim A_S + dim B_ab <= binomial(r,2)+3,
dim B_ab >= 4
```

is also valid.  A separate moment-curve chart proves that full product sensors
exist in the ambient local-plane space, so the necessary locus is proper.

This result does not prove that the intersection of all co-two rank-drop
loci is empty.  An exact P6 two-block model lies in that intersection while
retaining local rank and nonzero pure coefficients, although it is not a
restriction to `Delta_3`.  Unrestricted `P_6 -> Delta_3`, arbitrary-order
permanent nonrestriction, and the global Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_COTWO_PRODUCT_SENSOR_RANK_DROP_THEOREM.md
  verify_arbitrary_permanent_cotwo_product_sensor_rank_drop.py
  audit_arbitrary_permanent_cotwo_product_sensor_rank_drop.py
```

The review reconstructed the linear-algebra proof independently before
comparing the two replay routes.

## 1. The square-free algebra represents the permanent

In

```text
Z_r=K[x_0,...,x_(r-1)]/(x_0^2,...,x_(r-1)^2),
```

the coefficient of `x_0...x_(r-1)` in a product of `r` linear forms is the
unsigned sum over bijections from forms to variables.  It is therefore the
permanent, with no determinant signs and no factorial.  The monomial bases
also give a perfect complement pairing between degrees two and `r-2`.

The theorem uses only this coefficient pairing.  It does not identify the
full square-free product with the target tensor, and it does not import
hafnian or balanced-shore sensor semantics into the permanent node.

## 2. Local independence is forced by the target

Each dual local map supplies three degree-one forms.  If they were dependent
at any mode, the corresponding one-mode flattening of the pulled-back tensor
would have rank below three.  A weighted ternary diagonal tensor with all
three weights nonzero has one-mode flattening rank three.  Thus each local
triple is independent; this is a consequence of the hypothetical
restriction, not an extra genericity assumption.

For omitted modes `a,b`, the pairing restricted to their pair-product space
`B_ab` and the complementary product sensor `A_S` is exactly the
`2|(r-2)` flattening.  Its rank is three for every `r>=3`, including the
endpoint `r=3` where the complementary side has one mode.

## 3. The annihilator lemma has the claimed pointwise scope

For `u=sum u_p x_p` and `v=sum v_p x_p`, the equation `uv=0` is

```text
u_p v_q + u_q v_p = 0       for all p!=q.
```

Support one leaves exactly the line spanned by the supported coordinate.
Support two leaves one linear relation on two coordinates.  If at least
three coordinates of `u` are nonzero, three pair equations force the three
ratios `v_p/u_p` to vanish in characteristic different from two; equations
against one of those coordinates then kill every remaining entry.

The written result is therefore valid pointwise over arbitrary algebraic
coefficients and does not rely on rational sampling.  Characteristic zero is
more than sufficient.  The primary symbolic full-rank minor contains the
expected factor `-2`; the independent modular audit deliberately uses odd
primes.

## 4. Why the pair-product space has dimension at least four

The three pure pair products

```text
u_(a,c) u_(b,c),       c=0,1,2,
```

pair diagonally and nontrivially with the three complementary constant-word
products.  Their images in `A_S^*` are independent, hence `dim B_ab>=3`.

If equality held, the rank-three restricted pairing would have zero left
radical.  Every mixed pair product with colours `c!=d` pairs to zero with
every generator of `A_S`, because the resulting target word is necessarily
nonconstant.  Zero left radical would make all those mixed products zero.
Fixing one nonzero form at mode `a` would then put two independent forms at
mode `b` in its degree-one annihilator, contradicting the preceding lemma.

This argument does not assume that all nine pair products are independent.
It proves only the sharp lower bound needed by the theorem.

## 5. The dimension tradeoff is exact linear algebra

Let `N=binomial(r,2)`.  For subspaces `B` and `A` inside the two factors of a
perfect `N`-dimensional pairing, the restricted rank is at least

```text
dim B + dim A - N.
```

Applying the actual target rank three and `dim B_ab>=4` gives

```text
dim A_S + dim B_ab <= N+3,
dim A_S <= N-1.
```

No semicontinuity, generic-rank assumption, or numerical tolerance enters.
For P6, `N=15`, so every one of the fifteen four-mode sensors has rank at
most fourteen.

## 6. Properness is proved without assuming a witness

The common plane spanned by

```text
sum x_p,       sum t_p x_p,       sum t_p^2 x_p
```

with distinct `t_p` has full degree-`r-2` square-free product span.  Dual to
that multiplication map are the forms

```text
F_pq=product_(k notin {p,q}) (X+t_k Y+t_k^2 Z).
```

At the intersection of the two lines indexed by `p,q`, every other `F_ij`
vanishes, while `F_pq` does not.  The Vandermonde determinant excludes a
third concurrent line.  The `binomial(r,2)` forms are therefore independent.

This is an ambient chart only.  It proves that each maximal sensor minor is
not the zero polynomial and hence that the rank-drop condition is a proper
determinantal boundary.  It does not claim that this chart satisfies any
mixed GHZ equation.

## 7. The P6 block model blocks two tempting overstatements

The exact coordinate model

```text
U_0=U_1=U_2=<x_0,x_1,x_2>,
U_3=U_4=U_5=<x_3,x_4,x_5>
```

with cyclic coordinate bases has:

- local plane dimension three at every mode;
- all three constant-word top coefficients equal to one;
- all fifteen four-mode sensors of dimension three or nine; and
- a first-three/last-three flattening of rank one.

The last item excludes `Delta_3`, whose same flattening has rank three.  The
model has 33 nonzero mixed words, so it is not a hidden counterexample.

For one omitted low/high pair, both the pair and complement product spaces
have dimension nine.  Their sum is `18=binomial(6,2)+3`.  This exactly
refutes the stronger exploratory claim that arbitrary independent local
planes must have dimension sum at least nineteen.  That failed strengthening
is not used or promoted.

## 8. Computational independence and replay meaning

The primary verifier uses SymPy plus an explicit square-free mask algebra to
check:

- perfect complement pairings through `r=8`;
- symbolic annihilator minors, including the characteristic-two factor;
- full moment-curve product sensors through `r=8`; and
- every P6 block sensor, pure word, mixed support, and the rank-one split.

The independent audit imports neither the primary module nor SymPy.  It uses:

- custom modular row reduction over two odd primes;
- pairwise line-intersection evaluation of the star configuration through
  `r=10`;
- every nonempty coordinate-support pattern for the annihilator map through
  rank nine; and
- a direct bit-support walk for the P6 block tensor.

These bounded checks audit signs, indexing, dimensions, and the sharpness
example.  The arbitrary-order theorem is proved by the written annihilator,
pairing-rank, and line-intersection arguments.

## 9. Accepted proof-topology update

```text
every co-two product sensor full under P_r -> Delta_3: IMPOSSIBLE;
every P6 four-mode product sensor rank <=14:           PROVED necessary;
ambient full product-sensor chart at every r>=3:       PROVED;
all co-two sensors rank-drop plus pure/local data:      INSUFFICIENT;
unrestricted P6 restriction:                           UNKNOWN;
arbitrary-r permanent nonrestriction:                  UNKNOWN;
balanced physical hafnian sensor consequence:          NOT INFERRED;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

The surviving permanent problem lies inside the simultaneous rank-drop
intersection and must use its mixed equations.  No reduction to P5 or P7,
case-cover theorem, graph extraction, or local-to-global gluing follows.

## Strongest fresh-referee objection

The easiest invalid promotion is: "a generic local-plane tuple has a full
co-two sensor, therefore no restriction exists."  The hypothetical
restriction is forced onto the proper rank-drop locus; generic ambient
behavior says only that this is a genuine constraint.  Because the P6 block
model shows the simultaneous locus is nonempty even after local rank and
pure nonvanishing, properness is not an exclusion.  The theorem is accepted
only with that boundary explicit.
