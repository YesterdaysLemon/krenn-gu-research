# Balanced common-quadric mixed-permanent divisibility and conformal-shore exclusion

## Status

**Exact arbitrary-order characteristic-zero mixed/pure obstruction for one
balanced shore.**  Fix a balanced partition `Omega=R disjoint-union N` of a
ternary graph, with `|R|=|N|=m>=2`, and identify the root spaces with one
three-dimensional space.  Suppose the diagonal evaluation of every
root--root block is a scalar multiple of one nondegenerate quadratic `Q`.
Then, for every nonconstant coordinate word on `N`, the permanent of the
corresponding root-to-nonroot linear-form matrix must be divisible by `Q` in
any hypothetical GHZ witness.  For a constant colour word, the same permanent
must instead equal the nonzero pure-root product modulo `Q`.

This gives an immediate exact exclusion.  If, for one nonconstant word, the
cross matrix has column-separable form

```text
H_(i,u)(x)=lambda_(i,u) L_u(x),                      (1)
```

with every `L_u` nonzero and `perm(lambda)!=0`, then its permanent is the
nonzero product

```text
perm(lambda) product_(u in N) L_u(x),                (2)
```

which cannot be divisible by the irreducible quadratic `Q`.  Hence no graph
with that balanced shore can realize ternary GHZ, regardless of the blocks
internal to `N`.

In particular, this excludes **every** common-conformal shore whose
root--root and root--nonroot blocks are scalar multiples of one nondegenerate
symmetric form.  If the cross-scalar permanent is nonzero, a nonconstant word
contradicts mixed vanishing; if it is zero, a constant word contradicts the
pure GHZ coefficient.  The conclusion strictly extends the common-quadratic
orbit exclusion: internal nonroot blocks are arbitrary, root and cross edge
scalars may vary, and a single balanced cut suffices.

The theorem does not prove that every hypothetical witness has a common root
quadric or force general cross permanents to be column-separable.  Those are
the exact surviving boundaries.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Balanced-shore notation

Work over `C`; equivalently, work over a characteristic-zero field and extend
scalars to an algebraic closure.  Let

```text
Omega=R disjoint-union N,       |R|=|N|=m.           (3)
```

Choose isomorphisms `A_i:L_i -> V` for `i in R`, where `dim V=3`.  For each
root--root edge define its diagonal quadratic

```text
b_ij(x)=W_ij(A_i^(-1)x,A_j^(-1)x).                  (4)
```

Assume there is one nondegenerate quadratic form

```text
Q in Sym^2(V^*)
```

such that

```text
b_ij=rho_ij Q                                       (5)
```

for all distinct roots `i,j`.  The scalars `rho_ij` may vanish.  Condition
(5) concerns only simultaneous diagonal evaluation after the fixed root
identifications.  It does not assert that the full bilinear root--root blocks
are equal, symmetric, or nondegenerate.

Fix the original target coordinate bases on every local space; write their
nonroot vectors as `e_(u,0),e_(u,1),e_(u,2)`.  For a coordinate word

```text
alpha:N -> {0,1,2},                                 (6)
```

define the `m x m` matrix of root-linear forms

```text
H_alpha(x)[i,u]
 = W_iu(A_i^(-1)x,e_(u,alpha(u))).                  (7)
```

No assumption on (7), or on any block internal to `N`, is made for the
divisibility theorem.

## 2. The mixed all-cross permanent is the residue modulo Q

Contract every nonroot `u` against `e_(u,alpha(u))` and put the same
transformed vector `x` into every root, meaning that the original root vector
is `A_i^(-1)x` at vertex `i`.  Apply the balanced complete-deck identity.

The all-cross companion has label `D=N`.  It contains no root--root edge,
and summing its root-to-nonroot bijections gives exactly

```text
G_N(x,...,x;e_alpha)=perm H_alpha(x).                (8)
```

Its internal deck multiplier is `C_empty=1`.

Every other parity-legal companion has `D` a proper subset of `N`.  Since
`m-|D|` is then a positive even integer, each of its matching terms contains
at least one root--root edge.  On the repeated root vector that edge supplies
one factor `b_ij(x)=rho_ij Q(x)`.  Therefore

```text
G_D(x,...,x;e_(alpha|D)) belongs to (Q)              (9)
```

for every `D!=N`.  Multiplication by the arbitrary internal deck value
`C_(N-D)` preserves divisibility.  Consequently the complete graph
contraction satisfies the polynomial congruence

```text
T_W(A_R^(-1)x,e_alpha) = perm H_alpha(x)   mod (Q).  (10)
```

This is an identity in `C[x_0,x_1,x_2]`.  It uses neither sensor rank nor a
generic contraction point.  The empty-deck coefficient and the complement
label `N-D` are load-bearing: they are why the all-cross permanent occurs
with coefficient one and every other sector contains a root--root edge.

### Theorem 1 (mixed-permanent divisibility)

If `T_W` is the ternary GHZ tensor and `alpha` is nonconstant, then

```text
Q divides perm H_alpha.                              (11)
```

### Proof

Contracting ternary GHZ against a nonconstant coordinate word on `N` gives
the zero tensor on `R`: for each target colour `c`, at least one chosen
nonroot coordinate differs from `c`.  Hence the left side of (10) is the
zero polynomial.  Congruence (10) gives (11).

The conclusion holds for **every** nonconstant `alpha`, not merely for a
sampled word or a dense open set.

### Lemma 2 (pure-permanent residue)

Let `alpha(u)=c` be constant.  Define the nonzero root linear forms

```text
R_(i,c)(x)=e_(i,c)^*(A_i^(-1)x).                    (11a)
```

If `T_W` is ternary GHZ, then

```text
perm H_c(x)
 = product_(i in R) R_(i,c)(x)             mod (Q). (11b)
```

### Proof

Contracting every nonroot against `e_(u,c)` leaves the pure root tensor
`tensor_(i in R)e_(i,c)^*`.  Its repeated transformed-root polynomial is the
product on the right of (11b).  Apply congruence (10).  Each `R_(i,c)` is
nonzero because `A_i` is an isomorphism.

## 3. Column separation contradicts the mixed equations

Assume for one nonconstant word `alpha` that there are scalars `lambda_(i,u)`
and nonzero linear forms `L_u in V^*` with

```text
H_alpha(x)[i,u]=lambda_(i,u)L_u(x).                  (12)
```

Factoring `L_u` from column `u` of the permanent gives

```text
perm H_alpha
 = perm(lambda) product_(u in N) L_u.                (13)
```

### Theorem 3 (one-word column-separable shore exclusion)

Under (3)--(7) and (12), if

```text
perm(lambda)!=0,                                    (14)
```

then `T_W` is not ternary GHZ.

### Proof

A nondegenerate ternary quadratic is irreducible over `C`: a product of two
linear forms has quadratic-matrix rank at most two, whereas `Q` has rank
three.  The polynomial ring is a unique factorization domain, so the
irreducible `Q` is prime.  It cannot divide any nonzero linear form `L_u`, and
therefore cannot divide their product.  Conditions (13)--(14) contradict the
necessary divisibility (11).

Equivalently, on the smooth projective conic `Q=0`, finitely many nonzero
linear forms cannot cover the conic by their zero sets.  At an isotropic
point avoiding all those lines, every non-all-cross companion vanishes while
(13) does not.  This is the same contradiction without polynomial division.

## 4. Common-conformal balanced shores

The column-separable hypothesis has a direct physical specialization.  Let
`q` be one nondegenerate symmetric bilinear form on `V`, let
`A_u:L_u -> V` also be isomorphisms for `u in N`, and suppose the blocks on
one balanced shore obey

```text
W_ij(v_i,v_j)
 = rho_ij q(A_i v_i,A_j v_j)             for i,j in R,

W_iu(v_i,v_u)
 = lambda_(i,u) q(A_i v_i,A_u v_u)       for i in R, u in N.       (15)
```

There is no condition on `W_uv` for `u,v in N`.  Set `Q(x)=q(x,x)`.  For a
coordinate word `alpha`, define

```text
L_u(x)=q(x,A_u e_(u,alpha(u))).                       (16)
```

Nondegeneracy of `q` and invertibility of `A_u` make every `L_u` nonzero.
Equations (15)--(16) give (5) and (12).

### Corollary 4 (complete common-conformal shore obstruction)

For every cross-scalar matrix `lambda` in (15), the graph cannot realize
ternary GHZ for `m>=2`, whatever the internal nonroot blocks are.

### Proof

Put `p=perm(lambda)`.

- If `p!=0`, choose any nonconstant coordinate word, which exists because
  `m>=2`.  Equations (13)--(16) satisfy Theorem 3 and contradict the mixed
  target zero.
- If `p=0`, choose any constant colour `c`.  Column factorization makes
  `perm H_c=0`.  Lemma 2 would then make the nonzero product
  `product_i R_(i,c)` divisible by the irreducible quadratic `Q`, impossible
  in the polynomial UFD.

The two target sectors therefore close complementary values of the same
scalar permanent.  Entrywise nonvanishing and a separate argument forcing
`p!=0` are unnecessary.

In the vertex-gauge common-quadratic orbit, `rho_ij=lambda_(i,u)=1`, so

```text
perm(lambda)=m! !=0                                  (17)
```

in characteristic zero.  Thus Corollary 4 contains that orbit as a strict
special case while dropping all synchronization assumptions inside `N`.
The earlier flattening-rank proof remains an independent global obstruction
for the fully synchronized graph.

If `q` in (15) is degenerate, every edge incident to a root has its root
covectors in a space of dimension `rank(q)<3`; the one-vertex flattening at
that root then has rank below the GHZ rank three.  Hence degenerate
common-conformal shores are also excluded, by local rank rather than Theorem
3.  The irreducible-quadric argument is deliberately stated only for the
nondegenerate case.

## 5. Sharp boundary left by the proof

For Theorem 3, which assumes column separation for only one nonconstant word,
`perm(lambda)=0` makes that particular detector vanish and remains a genuine
boundary.  Corollary 4 closes it only because one physical common-conformal
shore supplies the **same** scalar matrix `lambda` for the constant words;
their pure residues then give the complementary contradiction.  No claim is
made that arbitrary wordwise column factorizations share one scalar matrix.

Without column separation Theorem 1 leaves the exact
divisibility branch

```text
Q divides perm H_alpha
for every nonconstant coordinate word alpha.         (19)
```

These are necessary conditions, not constructions of witnesses.  Internal
nonroot blocks cannot repair a failure of (19), because they occur only in
the sectors already killed modulo `Q`.

The proof-topology update is therefore:

```text
common root quadric => mixed cross-permanent divisibility: PROVED;
constant word => pure-root product residue modulo Q:       PROVED;
one column-separable mixed word, nonzero permanent:        EXCLUDED;
common-conformal shore, every cross permanent value:       EXCLUDED;
arbitrary internal nonroot completion can repair it:       FALSE;
one-word zero-permanent column separation:                  OPEN;
nonseparable cross permanents satisfying all residues:      OPEN;
universal extraction of a common root quadric:              NOT CLAIMED;
global Krenn--Gu conjecture:                                 UNRESOLVED.     (20)
```

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_common_quadric_mixed_permanent_divisibility_and_conformal_shore_exclusion.py
python claims/arbitrary-order/audit_balanced_common_quadric_mixed_permanent_divisibility_and_conformal_shore_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_common_quadric_mixed_permanent_divisibility_and_conformal_shore_exclusion.py claims/arbitrary-order/audit_balanced_common_quadric_mixed_permanent_divisibility_and_conformal_shore_exclusion.py
uv run --with ruff ruff check claims/arbitrary-order/verify_balanced_common_quadric_mixed_permanent_divisibility_and_conformal_shore_exclusion.py claims/arbitrary-order/audit_balanced_common_quadric_mixed_permanent_divisibility_and_conformal_shore_exclusion.py
```

The primary verifier constructs the full repeated-root contraction with
arbitrary fixed internal nonroot weights, checks (10) by exact polynomial
division through eight vertices, verifies permanent column factorization,
checks the complementary zero-permanent pure residue, and exhibits nonzero
remainders modulo `Q`.  The independent no-import audit
uses a separate sparse-polynomial ring, direct matching recursion, exact
quotient reduction, and different scalar/form instances.  These bounded
calculations audit the matching sectors, signs, complements, and constants.
The arbitrary-order proof is the balanced matching partition, the common
`Q` factor in every non-all-cross sector, the mixed/pure target dichotomy,
permanent factorization, and irreducibility in the polynomial UFD.
