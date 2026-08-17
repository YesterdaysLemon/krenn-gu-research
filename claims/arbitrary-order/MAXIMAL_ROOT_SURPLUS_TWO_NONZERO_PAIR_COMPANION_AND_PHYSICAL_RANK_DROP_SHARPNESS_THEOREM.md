# Maximal-root surplus-two nonzero pair companion and physical rank-drop sharpness

## Status

**Exact characteristic-zero Universal Supply advance and sharp witness-locus
boundary.**  In every maximum-root surplus-two cell of a hypothetical complex
ternary Krenn--Gu witness, blocker saturation forces at least one nonzero raw
two-root/two-residual permanental companion

```text
p_(A,Q)=per H_(A,Q).                                  (1)
```

Thus a raw pair-companion factor is not universally zero.  This is strictly
weaker than a target-coupled selector: it neither supplies a complementary
root-edge factor, identifies the outside pair blocks, nor supplies
synchronized consecutive response depths.

The exact linear obstruction is the quotient pair sensor.  The order-two
companion columns must be independent modulo every order-four-and-higher
nuisance column.  This criterion is equivalent to linear pair-coordinate
identifiability over the outside function field.  It is only a sufficient
criterion for reconstructing the physical graph deck; failure need not
integrate to a second physical deck.

That distinction is sharp.  An exact `r=3`, surplus-two graph-side family is
maximum-root, saturates the blocker-corank bound, is locally concise, has all
three pure GHZ coefficients independently normalized to one, and has the
entire Hamming-one target shell equal to zero.  Nevertheless every residual
pair fails the fixed-pair sensor criterion.  In the displayed zero-root-edge
specialization, three outside pair blocks form a genuine physical same-state
torus fibre.  The family is not a witness: the mixed word `02120111` has an
explicit nonzero coefficient.  Hence the full mixed target equations, rather
than maximality, blocker quotas, local concision, or pure normalization, must
remove this rank-drop branch.

This theorem does not supply the paired GLQ2 charts on the rank-drop locus,
extract a weighted permanent restriction, or prove that every witness is
observable.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

The witness application uses the field and incidence conclusions of the
[`maximum torus-root saturation theorem`](MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md),
which is currently proved over `C`.  The companion-sensor notation and
quotient criterion come from the
[`surplus-two complete-deck sensor theorem`](MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md).
The linear arguments below hold over any characteristic-zero field once the
displayed saturation and corank hypotheses are assumed.

## 1. The quotient pair sensor

Work over a characteristic-zero field `K`.  Let `R` be a maximum-cardinality
torus-root set of order `r>=3`, where the maximum ranges over both vertex sets
and fully supported torus vectors, and let the outside set `B` have order
`r+2`.  Use the
uncontracted surplus-two companion sensor

```text
Gamma_2:E_+ -> F                                      (2)
```

from the surplus-two complete-deck theorem.  Its coordinates are the
nonempty even outside principal hafnians `H_I`, `I subset B`.  Split its
domain as

```text
E_+=E_2 direct-sum E_>=4,                              (3)
E_2=direct-sum_(P in binom(B,2)) K(X)e_P,             (4)
```

over the outside function field `K(X)`.  Write `Gamma_2^(2)` and
`Gamma_2^(>=4)` for the two restrictions.

### Theorem 1 (exact quotient criterion)

The following are equivalent.

1. Every pair coordinate of an arbitrary rational deck array is determined
   by its sensor state.
2. `pi_2(ker Gamma_2)=0`.
3. The induced map

   ```text
   bar Gamma_2^(2):E_2 -> F/im Gamma_2^(>=4)           (5)
   ```

   is injective.
4. The `binom(r+2,2)` order-two companion columns are linearly independent
   modulo the span of all higher-order companion columns.

When these conditions hold, the physical pair blocks of the input graph are
uniquely recovered and generate its full same-graph hafnian deck by the
matching recurrence.  When they fail, the sensor alone does not certify
physical nonuniqueness.

### Proof

If two rational coordinate arrays have the same sensor state, their
difference lies in `ker Gamma_2`; their pair coordinates agree exactly when
the projection of every such difference to `E_2` is zero.  This proves the
equivalence of 1 and 2.  A pair vector `v` maps to zero in the quotient in
(5) exactly when `Gamma_2^(2)(v)` is cancelled by a higher-order nuisance
vector.  Equivalently `(v,n)` lies in `ker Gamma_2` for some `n in E_>=4`.
This proves 2--4.

For a physical input graph, `H_{uv}=B_{uv}`.  Hence recovery of every pair
coordinate recovers every physical edge block.  The complete principal deck
then follows from the perfect-matching recurrence.  The converse physical
claim would require a kernel vector to satisfy the nonlinear matching
relations, which an arbitrary rational vector need not do.  QED.

## 2. Every surplus-two cell has a nonzero raw pair companion

For every outside mode `u`, evaluate the root endpoint of its incident blocks
at the fixed root vectors and form

```text
L_u:V_u -> K^r,
z |-> (B_(i,u)(x_i,z))_(i in R).                       (6)
```

In the complex witness application, maximum-root blocker saturation gives
`rank L_u>=1`.  At surplus two its proved incidence bound is

```text
sum_(u in B) (3-rank L_u)<=6.                          (7)
```

Over a general characteristic-zero `K`, these two incidence conclusions are
the explicit hypotheses for Theorem 3.

For distinct `q0,q1 in B`, vectors `z0,z1`, and a root pair `A={i,j}`, put

```text
p_(A,Q)(z0,z1)
 =B_(i,q0)(x_i,z0)B_(j,q1)(x_j,z1)
  +B_(j,q0)(x_j,z0)B_(i,q1)(x_i,z1).                  (8)
```

This is exactly `per H_(A,Q)`.

### Lemma 2 (off-diagonal symmetric-product kernel)

For nonzero `b in K^r`, let

```text
S_b={a in K^r:a_i b_j+a_j b_i=0 for all i<j}.         (9)
```

Then `dim S_b<=1`.

### Proof

If `b` has one nonzero coordinate, every other coordinate of `a` is zero.
If it has two, the same conclusion holds off that support and there is one
linear relation on the two remaining coordinates.  If it has at least three,
write `rho_i=a_i/b_i` on three nonzero coordinates.  Pairwise equations give
`rho_i=-rho_j=-rho_k`, while the `j,k` equation gives
`rho_j=-rho_k`; characteristic zero forces all three to vanish.  Equations
against a nonzero coordinate then kill every remaining coordinate.  QED.

### Theorem 3 (universal complex-witness nonzero raw companion)

There exist distinct outside modes `q0,q1`, fully supported vectors
`z0,z1`, and a root pair `A` such that

```text
p_(A,Q)(z0,z1)!=0.                                    (10)
```

### Proof

There are `r+2>=5` outside modes.  If every `L_u` had rank at most one, the
left side of (7) would be at least `2(r+2)>6`.  Choose `q0` with
`rank L_q0>=2`, and choose any different `q1`; saturation gives
`rank L_q1>=1`.  Fix nonzero `b in im L_q1`.  If (10) failed for every root
pair and every `a in im L_q0`, then `im L_q0 subset S_b`, contradicting
Lemma 2.  Thus (8) is a nonzero polynomial in `(z0,z1)`.  Since `K` is
infinite, the fully supported torus is Zariski dense, so it contains a point
where this polynomial is nonzero.  QED.

### Scope wall

Theorem 3 produces one nonzero column weight.  It does not say that the
desired `p=0` and `p=1` deck functionals lie in the same constant target-pure
row space, nor that the quotient map (5) is injective.  Those are separate
breadth/depth conditions.

## 3. Physical fibres require the matching secant equations

Let `e_P` be the outside pair blocks and perturb them by `delta_P`.  For an
even outside set `I`, expansion over the nonempty set of perturbed edges in a
matching gives

```text
H_I(e+delta)-H_I(e)
 =sum_(empty!=S matching in I)
    delta_S H_(I-V(S))(e),                            (11)
delta_S=product_(P in S) delta_P.                     (12)
```

### Proposition 4 (physical same-state criterion)

The perturbed graph has the same uncontracted target state exactly when the
secant deck in (11) lies in `ker Gamma_2`.  Infinitesimally, the tangent deck

```text
dot H_I=sum_(P subset I, |P|=2)
          delta_P H_(I-P)                             (13)
```

must lie in that kernel.  Therefore a nonzero projection of an unrestricted
kernel to `E_2` is not, by itself, a physical fibre.

### Proof

Equation (11) is the multilinear expansion of each perfect-matching product.
Applying the linear companion sensor gives the change in the target state.
This change is zero exactly under the stated kernel condition.  Taking the
linear term in the perturbation proves (13).  QED.

## 4. A pure-normalized physical rank-drop family

Let `r=3`, `B={u0,u1,u2,u3,u4}`, and give every vertex the basis
`e0,e1,e2`.  Put `x_ri=(1,1,1)` and set every root--root block to zero.
Every displayed nonzero edge below is the coordinate-diagonal monomial
`e_c^* tensor e_c^*` with weight one.

The root--outside colour table is

```text
       u0 u1 u2 u3 u4
r0      1  0  2  -  -
r1      2  1  0  -  -
r2      -  -  1  0  2.                               (14)
```

Every outside--outside pair is nonzero.  Give `u0u4` colour zero,
`u3u4` colour one, `u1u3` colour two, and every other outside pair colour
zero.  Keep every displayed edge weight equal to one except

```text
B_01=t_01 e0e0, B_02=t_02 e0e0, B_12=t_12 e0e0,
(t_01,t_02,t_12) in (K^*)^3.                          (15)
```

### Theorem 5 (exact sharpness family)

The support family (14) has all of the following properties.

1. `R={r0,r1,r2}` is a maximum torus-root set.
2. The outside row ranks are `(2,2,3,1,1)`, so their coranks sum to six.
   The blocker sets are

   ```text
   B0={u1,u2,u3}, B1={u0,u1,u2}, B2={u0,u2,u4}.       (16)
   ```

3. Every vertex is incident with all three coordinate colours, every root row
   uses all three colours, and the full state is locally concise.
4. The surplus-two sensor has rank seven.  Its only nonzero columns are the
   seven order-two labels whose complementary root-injection triples are

   ```text
   012,013,014,023,024,123,124.                        (17)
   ```

   Their fourteen root-word supports are pairwise disjoint.  The pair labels
   `01,02,12` and all five order-four labels are zero columns.
5. Every residual pair `Q subset B` fails fixed-`Q` linear observability.
6. The three blocks `H_01,H_02,H_12` are physically invisible to the full
   state.  Varying their nonzero weights gives a three-dimensional algebraic
   torus of distinct physical graphs with the same state.
7. The pure full-graph coefficients are the three unique unit matchings

   ```text
   lambda0=(r0u1)(r1u2)(r2u3)(u0u4),
   lambda1=(r0u0)(r1u1)(r2u2)(u3u4),
   lambda2=(r0u2)(r1u0)(r2u4)(u1u3),                  (18)
   ```

   so all three coefficients equal one for every parameter in (15).
8. Every Hamming-one neighbour of a pure word has coefficient zero.
9. The mixed word, in vertex order
   `(r0,r1,r2,u0,u1,u2,u3,u4)`,

   ```text
   chi=02120111                                        (19)
   ```

   has the unique nonzero matching

   ```text
   r0-u1, r1-u0, r2-u2, u3-u4,                        (20)
   ```

   and coefficient one.

### Proof

Outside--outside coordinate monomials prohibit two outside vertices in a
torus-root set.  If one outside vertex is chosen, at least one nonzero
root--outside coordinate monomial excludes an old root, so the set has size
at most three.  The displayed `R` has size three because its root--root
evaluations are zero.  This proves 1.

The table gives the ranks and blocker sets in 2 directly.  The three special
outside edges complete the missing colours at every outside vertex.  For any
one-mode flattening, restrict to the three columns in which all other modes
have one common colour.  The diagonal entries are the three unit pure
coefficients in (18), while the off-diagonal entries are Hamming-one
coefficients and vanish.  This `3 by 3` identity submatrix proves local
concision in 3.

Because root--root blocks vanish, only the `p=0` injection columns survive.
Directly enumerating injections from the three roots gives (17); the
complementary triples `034,134,234` have no injection.  Their nonzero word
supports are pairwise disjoint, proving rank seven.  The vanishing pair
labels are the complements of those three missing triples.  For any residual
pair `Q`, either `Q` is one of these labels, the edge between the other two
vertices of `{u0,u1,u2}` avoids `Q`, or all three labels avoid `Q`.  In every
case the fixed-`Q` desired coordinates contain a kernel axis.  This proves
4--5.

Any full matching using one of `u0u1,u0u2,u1u2` would have to match the three
roots bijectively to its complementary outside triple, which is one of
`234,134,034`; no such injection exists.  Root--root blocks vanish, so there
is no other matching sector.  Hence those edge weights never occur in the
full state, proving 6 and the physical secant condition (11).

Coordinate-diagonal edges force every colour multiplicity in a nonzero word
to be even.  This proves 8.  Direct matching inspection gives the three
unique pure matchings (18), and gives (20) as the unique matching at (19).
This proves 7--9.  QED.

## 5. Exact GL consequence

The breadth/depth map is now:

```text
maximal-root surplus two
  -> some raw p_(A,Q)!=0                              PROVED;
  -> quotient pair observability                      NOT FORCED;
  -> physical rank-drop can survive pure normalization
     and the Hamming-one target shell                 PROVED;
  -> the displayed family is killed by one higher
     mixed GHZ coefficient                            PROVED;
  -> every hypothetical witness is observable or has
     a uniformly displayed mixed detector             OPEN.       (21)
```

Thus the next legal supply-or-detect theorem must use actual mixed witness
equations to exclude the matching-secant rank-drop locus, or must reconstruct
only the quotient physical graph after proving that the invisible fibre does
not change the desired corrected channel.  No permanent/co-two theorem may
be imported here, because those theorems assume the permanent restriction
that Universal Supply is intended to extract.

## 6. Exact verification boundary

The focused verifier enumerates the injection sensor and all perfect
matchings of the eight-vertex sharpness family with exact integer arithmetic.
It checks maximum-root incidence data, rank seven, the three invisible pair
axes, all residual-pair failures, pure coefficients, the Hamming-one shell,
and the mixed detector (19).

The no-import audit uses a separate bit-mask matching recurrence and an
independently written rational row-reduction routine.  It also checks the
finite support cases in Lemma 2.  These programs audit the displayed bounded
family and algebra.  They do not prove the arbitrary-order incidence bound,
the written characteristic-zero argument, or a statement about every witness.
