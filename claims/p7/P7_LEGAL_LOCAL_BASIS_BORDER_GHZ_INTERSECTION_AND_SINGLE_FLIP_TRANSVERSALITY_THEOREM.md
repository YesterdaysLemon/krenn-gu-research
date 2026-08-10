# Legal local bases force a border-GHZ intersection and give a 30-direction transversality test

## Status

**Exact characteristic-zero border-incidence theorem and legal-pullback
tangent criterion.**  Let `Gamma:U->T` be a legal full five-root companion
map with

```text
dim U=219,              T=(K^3)^(tensor 5),
dim T=243,              W=im Gamma.                   (1)
```

Independent invertible changes of basis at the five roots act on every
root-side companion form and on the root vectors contragrediently.  This
preserves:

- rank 219 of `Gamma`;
- pairwise-zero root contractions;
- every blocker/nonblocker contraction;
- symmetry of the unordered graph blocks.

Thus a tensor of `W` that is locally equivalent to a nonzero diagonal GHZ
tensor would produce a legal full-rank target-incidence chart, provided the
transformed roots remain coordinatewise nonzero.

There is an unconditional closure result.  In `P(T)=P^242`, the third secant
variety of the Segre variety `(P^2)^5` has dimension 32.  Since `P(W)` has
dimension 218, projective dimension forces

```text
dim(P(W) intersect sigma_3((P^2)^5)) >= 218+32-242=8. (2)
```

Every legal rank-219 sensor therefore contains at least an eight-dimensional
projective family of tensors of border rank at most three.  This is much
stronger than a raw channel count, but it is not yet an actual GHZ
intersection: the family could lie entirely in the boundary of the open
locally diagonalizable rank-three orbit, or its local factor bases could
send a fully supported root to a coordinate hyperplane.

At an actual simple target-incidence point, there is a small exact tangent
test.  If

```text
tau=sum_(c in S) lambda_c e_c^(tensor 5),
lambda_c!=0,                 r=|S|,                    (3)
```

then infinitesimal local basis changes contribute exactly the `10r`
single-flip coordinate words obtained by changing one of the five copies of
an active colour `c` to either other colour.  The ambient target-incidence
normal space has dimension 22.  Consequently:

- one-term and two-term diagonal targets can contribute at most 10 and 20
  local-basis normal directions, so local bases alone cannot make their
  pullback transverse;
- a full three-term target contributes 30 directions and is transverse
  exactly when their image in `T/(W+Delta)` has rank 22;
- equivalently, the 30-dimensional single-flip space meets `W+Delta` in its
  minimum possible dimension eight.

This reduces legal local-basis transversality to one rank computation on 30
named coordinate words.  No augmented minor is expanded.

No exact legal full-rank point with `W intersect Delta` a line is constructed
here.  The result instead proves a sharp alternative: either the committed
legal sensor image already contains a torus-concise rank-at-most-three tensor
and a legal target-incidence chart follows by basis change, or its mandatory
eight-dimensional border-rank-three intersection is trapped in an explicit
exceptional boundary.  Deciding which alternative holds, and realizing the
resulting cofactor line by one physical nonroot graph, remain **UNKNOWN**.
The `P_7` restriction problem and the global Krenn--Gu conjecture remain
**UNRESOLVED**.

No random coefficients, configuration search, support enumeration, or
augmented-minor expansion is used.

## 1. Legal root-local covariance

Let `V_i=K^3` be the local vector space at root `i`.  Write root--nonroot
forms and root--root blocks as

```text
h_(i,u) in V_i^*,
L_ij in V_i^* tensor V_j^*.                           (4)
```

Let the chosen root vector be `x_i in V_i`.  For
`g=(g_1,...,g_5) in product_i GL(V_i^*)`, define

```text
h'_(i,u)=g_i h_(i,u),
L'_ij=(g_i tensor g_j)L_ij,
x'_i=(g_i^(-1))^* x_i.                                (5)
```

Then

```text
h'_(i,u)(x'_i)=h_(i,u)(x_i),
L'_ij(x'_i,x'_j)=L_ij(x_i,x_j).                       (6)
```

Every depth-five, depth-three, and depth-one aggregate companion form has
one covector factor in every root slot.  Hence

```text
Gamma'=(tensor_i g_i) Gamma.                           (7)
```

### Theorem 1 (legal local-basis covariance)

The transformation (5) preserves full sensor rank, pairwise-zero roots,
the active blocker set, residual nonblockers, and legal symmetric graph
blocks.  If

```text
tau in W
```

has a decomposition

```text
tau=sum_(c=0)^2 lambda_c
        a_(1,c) tensor ... tensor a_(5,c),             (8)
```

where for each root `i` the active `a_(i,c)` are linearly independent and

```text
a_(i,c)(x_i)!=0                                       (9)
```

for every active pair `(i,c)`, then a legal local change of basis sends
`tau` to a nonzero diagonal target while keeping every transformed root
fully supported in the active target coordinates.

### Proof

Equations (6) follow immediately from duality, so all named graph
contractions are preserved.  The reverse orientation of a transformed
unordered edge still carries the transpose, preserving symmetry.  Equation
(7) follows term by term from the matching formulas; its left factor is
invertible, so rank is unchanged.

Extend the active covectors in (8) to a basis at each root and choose `g_i`
sending that basis to coordinate covectors.  The tensor becomes diagonal.
Equation (9) says precisely that the coordinates of `(g_i^(-1))^*x_i` on
the active axes are nonzero.  For a full three-term target these are all
three coordinates, so the new roots are fully supported.  With one or two
active terms, choose the unused members of each extended covector basis
outside the additional hyperplanes of covectors vanishing at `x_i`; the new
roots can then be kept fully supported as well.

Call tensors satisfying the basis and nonvanishing conditions in (8)--(9)
**torus-concise GHZ tensors**.  They form a Zariski-open subset of the usual
locally diagonalizable rank-three orbit relative to the fixed roots.

## 2. Every full sensor meets the border-GHZ variety

Let

```text
X=Segre((P^2)^5) subset P(T)                           (10)
```

be the projective pure-tensor variety, `dim X=10`, and let `sigma_3(X)` be
the Zariski closure of projective planes spanned by triples of points of
`X`.

### Lemma 2 (the third secant has dimension 32)

Over an algebraically closed characteristic-zero field,

```text
dim sigma_3(X)=32.                                    (11)
```

### Proof

Three projective pure tensors contribute `3*10` parameters and their
projective linear combination contributes two, so the dimension is at most
32.  At

```text
tau_0=e_0^(tensor 5)+e_1^(tensor 5)+e_2^(tensor 5),   (12)
```

differentiate the three summands and their coefficients.  The affine
tangent image contains:

- the three pure words `c c c c c`;
- for each of three colours, five root positions, and two replacement
  colours, the 30 words obtained by changing exactly one slot.

These 33 coordinate tensors are distinct and independent.  The projective
image therefore has local dimension at least 32, proving equality.

The same 33 directions are the affine tangent image of the root-local
`GL(3)^5` orbit of (12).  Hence that projective orbit has the full dimension
32 of the irreducible secant variety and is a dense Zariski-open orbit.  Its
points are exactly the rank-three decompositions whose three factors form a
basis at every root, with all three coefficients nonzero.  Requiring the 15
factor evaluations in (9) to be nonzero removes further proper hyperplane
sections, so the torus-concise locus is again a dense open subset.

The surrounding secant/tangent and tensor-identifiability dictionary is
surveyed by Bernardi et al., [*Hitchhiker guide to: Secant varieties and
tensor decomposition*](https://arxiv.org/abs/1812.10267).  The dimension and
orbit statements above are proved directly for this five-qutrit tensor; the
survey is used only to identify the neighboring geometric toolkit.  Its
flattening and tangential methods suggest exact tests for whether the forced
intersection is trapped in the exceptional secant boundary.

### Theorem 3 (mandatory border-GHZ intersection)

For every 219-dimensional linear subspace `W subset T`, every irreducible
component of the nonempty projective intersection satisfies

```text
dim(P(W) intersect sigma_3(X))>=8.                    (13)
```

### Proof

The projective dimension theorem in `P^242` gives

```text
dim(P(W) intersect sigma_3(X))
 >=dim P(W)+dim sigma_3(X)-242
 =218+32-242=8.                                       (14)
```

The same inequality guarantees nonemptiness.

The torus-concise GHZ tensors of Theorem 1 form an open subset of
`sigma_3(X)`.  Thus (13) gives the exact alternative

```text
P(W) meets the torus-concise open set,
or
an at-least-eight-dimensional intersection is contained in its boundary.
                                                               (15)
```

The first branch produces a legal full-rank target incidence by (5)--(9).
The second branch is a genuine border obstruction, not proof that actual
incidence is empty.

## 3. Single-flip tangent space of the diagonal orbit

For a support `S subset {0,1,2}`, define

```text
F_S=span{
 e_c tensor ... tensor e_a tensor ... tensor e_c:
 c in S, a!=c, one changed root slot
}.                                                     (16)
```

The displayed coordinate words are distinct, so

```text
dim F_S=5*2*|S|=10|S|.                                (17)
```

### Lemma 4 (local-orbit differential)

At the diagonal tensor (3), the tangent space produced by
`product_i GL(V_i^*)` is

```text
span{e_c^(tensor 5):c in S} + F_S.                    (18)
```

### Proof

For `X_i in End(V_i^*)`, differentiation gives

```text
sum_(c in S) lambda_c sum_(i=1)^5
 e_c tensor ... tensor X_i e_c tensor ... tensor e_c. (19)
```

The diagonal entries of `X_i` give the active pure words.  Its two
off-diagonal entries in column `c` give the two single flips at root `i`.
All occur independently because `lambda_c!=0`, proving (18).

## 4. Exact legal-pullback tangent criterion

Suppose now that `Gamma` is a legal full-rank sensor and

```text
W intersect Delta=K tau,                              (20)
```

where `tau` is (3).  Put

```text
N_Gamma=T/(W+Delta).                                  (21)
```

The Schubert incidence theorem gives `dim N_Gamma=22`.

### Theorem 5 (single-flip transversality)

The normal image of legal root-local basis changes is the image of

```text
F_S -> N_Gamma.                                       (22)
```

Its rank is

```text
nu_S=dim(F_S+W+Delta)-dim(W+Delta).                    (23)
```

Therefore:

1. if `|S|=1`, then `nu_S<=10<22`;
2. if `|S|=2`, then `nu_S<=20<22`;
3. if `|S|=3`, then local-basis changes are transverse to target incidence
   exactly when

   ```text
   nu_S=22
   <=> F_S+W+Delta=T
   <=> dim(F_S intersect (W+Delta))=8.                (24)
   ```

Whenever (24) holds, the full legal companion pullback is transverse as
well, because local basis changes are a subfamily of legal companion
deformations.

### Proof

The active pure-word part of (18) lies in `Delta` and disappears in the
normal quotient.  The remaining differential is exactly (22), giving
(23).  The first two bounds follow from (17).  In the full-support case,
`dim F_S=30` and `dim(W+Delta)=221`, so every intersection has dimension at
least

```text
30+221-243=8.                                         (25)
```

The normal rank is 22 exactly when this lower bound is attained, which is
equivalent to spanning `T`.

The criterion uses only the 30 named Hamming-distance-one words.  It is not
a claim that every actual incidence point satisfies (24).  Failure of (24)
also does not prove the full legal pullback nontransverse: variations of the
companion blocks not induced by local basis changes may supply the missing
normal directions.

## 5. Consequences for the committed P7 sensor

Let `W_0` be the image of the committed legal rank-219 sensor.  The earlier
target-incidence certificate proves

```text
W_0 intersect Delta={0}.                              (26)
```

Theorem 3 nevertheless gives an at-least-eight-dimensional variety

```text
P(W_0) intersect sigma_3(X).                          (27)
```

Hence the next legal question is no longer whether `W_0` contains any
low-border-rank tensor; it necessarily contains many.  The exact question
is whether (27) contains a torus-concise point.

- If yes, choose its five local factor bases in Theorem 1.  The transformed
  graph remains legal and rank 219, and its image meets `Delta`.
- If no, every component supplied by (13) lies in the union of the
  non-concise, colliding-summand, lower-rank, or root-coordinate-boundary
  strata of the secant closure.

This is a structural algebraic-geometric alternative.  It does not require
listing secant decompositions.  A future proof can attack the exceptional
boundary by flattenings, subspace varieties, tangential equations, or the
root-torus resultants already present in the repository.

Even in the positive branch, the unique formal cofactor line supplied by
sensor injectivity need not be the principal-hafnian deck of one nonroot
graph.  Pinned-star, determinant-cleared integrability, and nested-hafnian
tests remain mandatory before any physical conclusion.

## 6. Scope wall

```text
legal local GL(3)^5 covariance of Gamma:               PROVED;
full sensor rank under local basis changes:            PRESERVED;
blocker/nonblocker and pairwise-zero contractions:      PRESERVED;
dimension of third five-qutrit secant:                 32;
mandatory projective border-rank-three intersection:   DIMENSION AT LEAST 8;
border intersection contains torus-concise tensor:     UNKNOWN;
actual legal full-rank target-incidence chart:         UNKNOWN;
single-flip local tangent space for r target terms:    DIMENSION 10r;
one/two-term local-basis transversality:               IMPOSSIBLE;
three-term local-basis transversality criterion:       EXACT RANK-22 TEST;
full companion pullback transverse at a real point:    UNKNOWN;
formal cofactor line physically realizable:            UNKNOWN;
P7 nonrestriction:                                     UNKNOWN;
global Krenn--Gu:                                      UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_legal_local_basis_border_ghz_intersection_and_single_flip_transversality.py
python claims/p7/audit_p7_legal_local_basis_border_ghz_intersection_and_single_flip_transversality.py
python -m py_compile claims/p7/verify_p7_legal_local_basis_border_ghz_intersection_and_single_flip_transversality.py claims/p7/audit_p7_legal_local_basis_border_ghz_intersection_and_single_flip_transversality.py
uv run --with ruff ruff check claims/p7/verify_p7_legal_local_basis_border_ghz_intersection_and_single_flip_transversality.py claims/p7/audit_p7_legal_local_basis_border_ghz_intersection_and_single_flip_transversality.py
```

The primary replay builds the 33 tangent coordinate words, verifies the
secant and intersection dimensions, and checks the rank-22 criterion on a
fixed rational simple-incidence model.  The independent no-import audit uses
base-three word indices and separate rational elimination.  These are small
audits of the symbolic proofs, not searches for legal configurations or
secant decompositions.
