# The legal-companion simple-incidence pullback ideal

## Status

**Exact characteristic-zero determinant-cleared pullback theorem and ambient
non-forcing boundary.**  This note pulls the P7 residual-pair pentad, the
`h=0` gate, and the pinned-star alignment equations all the way back to the
entries of the legal 219-label companion map.  It introduces no free
219-vector and performs no graph, parameter, support, colouring, or
quadruplet search.

Let `Gamma(z)` be the full named P7 companion map in the polynomial
coordinates `z` of the legal symmetric loopless companion blocks.  After
quotienting the three-dimensional diagonal target space, put

```text
B(z)=pi_Delta Gamma(z),                  240 x 219.     (1)
```

On a full-sensor simple-incidence chart, a signed vector of `218 x 218`
maximal minors of a `218 x 219` row submatrix of `B` is the unique target
cofactor line.  Substituting this minor vector into the established pair
tests gives polynomial covariants in the legal parameters.  Their vanishing
is independent of the chosen row chart:

```text
pentad pullback:              relative line weight 5;
h=0 numerator pullback:       relative line weight 8;
pair-star alignment pullback: relative line weight 17.  (2)
```

There is a stronger ideal statement.  Give the pair amplitude `tau` relative
weight 15.  Then the 21 equations

```text
tau q_ij=khat_ij(q)                                  (3)
```

all have weight 16 and glue across simple-incidence charts.  In the Laurent
ring where `tau` and the pinned determinants are invertible, (3) together
with the weight-eight `h=0` gate is necessary and sufficient for the entire
residual-pair four-deck sector.  Every degree-five pentad and every degree-17
alignment minor is an algebraic consequence of this weighted pullback ideal.

The ambient determinantal incidence equations do **not** force any of these
physical conditions, even after restricting to `h=0` and the pinned-open
chart.  An exact fixed deck supplies a simultaneous counterexample.  This
does not decide containment after pullback to the **legal** companion
parameterization: no legal full-sensor target-incidence point is currently
known.  P7 and global Krenn--Gu remain **UNRESOLVED**.

## 1. The legal parameter ring and the incidence ideal

Work over a characteristic-zero field `K`.  Let

```text
R=K[z]                                                  (4)
```

be the coordinate ring of a chosen legal P7 cell, with symmetric and
loopless constraints already built into the independent coordinates `z`.
The 219 columns of `Gamma(z)` retain their named complementary-cofactor
labels.  Let

```text
Delta=span{e_0^(tensor 5),e_1^(tensor 5),e_2^(tensor 5)}
       subset T,                         dim T=243.     (5)
```

Variable diagonal target incidence is equivalent, on the full-sensor locus,
to a nonzero kernel of (1).  Its determinantal ideal is

```text
I_inc=I_219(B),                                         (6)
```

the ideal of maximal minors of `B`.  Formula (6) is a symbolic determinantal
ideal; it is not an instruction to list or evaluate its generators.

Choose 218 row labels `S` and form the `218 x 219` matrix `B_S`.  Define its
signed maximal-minor vector

```text
q_j^S=(-1)^j det(B_S with column j deleted),
                         0<=j<=218.                    (7)
```

Choose one coordinate `q_r^S` and one full-sensor minor `g` of `Gamma`.
Consider the localized simple-incidence chart

```text
X_(S,r,g)=V(I_inc) intersect D(q_r^S g).               (8)
```

### Theorem 1 (maximal-minor target-line covariant)

On (8), `Gamma` has rank 219, `B` has rank 218, and

```text
ker B=K q^S.                                           (9)
```

In particular, `Gamma q^S` is a nonzero diagonal target and `[q^S]` is the
unique named shallow-cofactor line.  No linear solve or elimination in 219
cofactor variables is required.

### Proof

Laplace expansion gives `B_S q^S=0`.  For a row `b` of `B` outside `S`, the
scalar `b q^S` is, up to its fixed sign, the `219 x 219` minor obtained by
adjoining `b` to `B_S`.  It therefore vanishes modulo `I_inc`.  Since
`q_r^S!=0`, the row rank of `B_S` is 218, proving (9).  Full sensor rank makes
`Gamma` injective, so `Gamma q^S` is nonzero; (1) and (9) put it in `Delta`.

The vector (7) is the coordinate form of the Hodge dual of the exterior row
product `wedge^218 B_S`.  This is the promised representation-theoretic
translation of the Schubert target-line condition.

### Chart covariance

If `(S,r,g)` and `(S',r',g')` overlap, both minor vectors span (9), so

```text
q^(S')=s q^S                                             (10)
```

for an invertible regular scalar `s` on the overlap.  Hence a homogeneous
degree-`d` equation in the line vector changes by the unit `s^d`.  Its zero
locus is chart independent.

## 2. Pullback of the three `h=0` pair tests

Relabel the residual pair as `Q={0,1}` and the seven blockers as
`A={2,...,8}`.  In the minor vector (7), use remaining-set notation and put

```text
y_ij(q)=q_{ {0,1,i,j} },              2<=i<j<=8.       (11)
```

For each five-subset `F` of blockers, define the pulled pentad

```text
Phi_F^S(z)=P_F(y(q^S(z))).                              (12)
```

Build the established pinned matrices directly from `q^S` and put

```text
d_p(q)=det Nhat_p(q),
u_p(q)=adj(Nhat_p(q)) bhat_p(q),        p=0,1,          (13)

eta^S(z)=(u_0(q^S))_1,                                  (14)

khat_ij(q)=(u_0(q))_i (u_1(q))_j
            +(u_0(q))_j (u_1(q))_i,                    (15)

Alpha_ef^S(z)=y_e(q^S) khat_f(q^S)
              -y_f(q^S) khat_e(q^S).                  (16)
```

These are honest polynomials in `z`: (7), (11), and (13)--(16) use only
determinants, adjugates, additions, and multiplications.  Their degrees in
the projective line coordinate are respectively

```text
deg_q Phi=5,   deg_q eta=8,   deg_q khat=16,
deg_q Alpha=17.                                         (17)
```

The companion-parameter multidegrees of the maximal minors can depend on the
named deletion columns; no unsupported uniform degree in `z` is claimed.

### Theorem 2 (determinant-cleared legal pullbacks)

On the localized chart

```text
X_pin=X_(S,r,g) intersect D(d_0(q^S)d_1(q^S)),          (18)
```

every physical P7 target point on the branch `a_01=0` satisfies

```text
Phi_F^S=0       for every five-blocker F,
eta^S=0,
Alpha_ef^S=0   for every pair of blocker edges e,f.    (19)
```

The vanishing conditions in (19) are independent of `S,r,g` on chart
overlaps.

### Proof

Theorem 1 identifies `q^S` with the unique target-incidence line vector.
The degree-five residual-pair theorem, pinned `h=0` numerator theorem, and
pair-star alignment theorem then give (19).  Under (10), the three displayed
families scale by `s^5,s^8,s^17`; these are units on an overlap.

## 3. The weighted Schubert--hafnian pullback ideal

The alignment minors are the eliminated form of a more precise ideal.  Work
in the localized Laurent extension

```text
S_pin=(R/I_inc)_[q_r^S g d_0(q^S)d_1(q^S)]
      [tau,tau^(-1)].                                  (20)
```

Give `q` relative weight one and `tau` relative weight 15.  Define

```text
J_pair^S = < eta(q^S),
             tau y_ij(q^S)-khat_ij(q^S) : 2<=i<j<=8 >
             subset S_pin.                             (21)
```

The value 15 is forced, not chosen: under `q -> s q`, the pinned
determinants and Cramer vectors have weight eight, so `khat` has weight 16.
Equation (3) then glues precisely under

```text
tau -> s^15 tau.                                       (22)
```

### Theorem 3 (exact pair-sector ideal)

A point of `X_pin` admits a nonzero target amplitude whose complete 21-entry
residual-pair four-deck is physical on `a_01=0` if and only if it lifts to a
zero of (21).  The ideals `J_pair^S` glue under (10) and (22), so this
criterion is independent of the maximal-minor chart.

Moreover, inside `S_pin`,

```text
Phi_F^S belongs to J_pair^S,
Alpha_ef^S belongs to J_pair^S.                        (23)
```

Thus the pentads are the lowest-weight circuit shadows, and the degree-17
minors are the ordinary projective elimination shadows, of one exact
weighted incidence-integrability ideal.

### Proof

On the pinned chart the reconstructed pair response is
`khat_ij/(d_0d_1)`.  If `t` is the nonzero target-line amplitude, set
`tau=t d_0d_1`; this gives (21).  Conversely, an invertible `tau` gives
`t=tau/(d_0d_1)` and all 21 pair equations.  The first generator is exactly
the `h=0` condition.

The hyperbolic-Gram identity gives `P_F(khat)=0`.  Modulo the pair generators,

```text
0=P_F(khat)=P_F(tau y)=tau^5 P_F(y).                   (24)
```

Since `tau` is invertible, (24) proves the first containment in (23).  For
the second,

```text
y_e(tau y_f-khat_f)-y_f(tau y_e-khat_e)
 =-Alpha_ef.                                           (25)
```

Chart covariance follows from the weights already computed.

The Laurent formulation handles all zero-coordinate cases correctly.  In
particular, ordinary rank-one minors alone would incorrectly retain a point
with `y!=0` and `khat=0`, which would require the forbidden amplitude
`tau=0`.

## 4. Exact ambient non-forcing theorem

The ideal (21) is physical information.  It is not a formal consequence of
the Schubert incidence ideal (6).

### Theorem 4 (incidence, even with the gate, does not force the pair ideal)

On the ambient space of named injective maps `Gamma:U->T`:

1. full-sensor simple incidence does not force `eta=0`;
2. full-sensor simple incidence together with `eta=0` and `d_0d_1!=0` does
   not force a pentad or an alignment minor to vanish.

These failures hold over the integers before the ambient map is chosen.

### Proof

For the first assertion, take the principal `h_4,h_6,h_8` deck of the
nine-vertex all-one graph.  In the pinned rows

```text
(0,1,2,3,4,10,20,35),                                 (26)
```

the exact determinants are

```text
d_0=d_1=32805,
(u_0)_1=32805.                                         (27)
```

Thus the pinned chart is open and `eta!=0`.

For the stronger second assertion, set only `a_01=0` and leave every other
nonroot edge equal to one.  The same selected pinned systems give

```text
d_0=d_1=32805,
(u_0)_1=0,
(u_0)_i=(u_1)_i=32805,             2<=i<=8.            (28)
```

The 21 four-set coordinates containing both `0` and `1` do not enter either
selected pin matrix or right-hand side: the pin-0 matrix uses four-sets
avoiding `0` and six-sets containing `0`, and similarly for pin 1.  Replace
the ten pair coordinates on blockers `2,3,4,5,6` by `1,2,...,10` in
lexicographic edge order.  Equations (28) remain unchanged, but

```text
P_23456=-6,                                             (29)

khat_e=2(32805)^2       for every blocker edge e,
Alpha_(23),(24)=-2(32805)^2=-2152336050.               (30)
```

It remains to realize either fixed named vector as an ambient simple target
line.  For any nonzero `w in U`, choose a decomposition `U=K w direct-sum H`,
an injection `H->T/Delta`, and a nonzero `d in Delta`.  Map `w` to `d` and
`H` injectively into a complement of `Delta`.  The resulting `Gamma` is
injective and

```text
ker(pi_Delta Gamma)=K w.                               (31)
```

Apply (31) to the decks above.  This proves both non-forcing statements.

The construction in (31) is intentionally ambient.  It is not claimed that
the resulting map is a legal symmetric graph-companion map.

## 5. The exact remaining legal question

The legal P7 problem is now a containment/disjointness question in the
parameter ring (4), not an unstructured search in shallow-deck space.
On every maximal-minor chart one may ask whether

```text
J_pair^S=(1) in S_pin.                                 (32)
```

If (32) holds on a cover of the legal full-sensor simple-incidence locus,
then that entire `h=0` residual-pair branch is excluded.  If (21) has a legal
zero, the residual-pair four-deck sector survives, but the other 105
four-deck coordinates and the six- and eight-deck partner equations must
still be imposed.  A prescribed diagonal GHZ amplitude may add further
equations inside `Delta`; (6) treats variable diagonal incidence.

Theorem 4 prevents replacing this legal-ring question by a universal theorem
about determinantal incidence.  Any successful proof must use identities of
the symmetric companion parameterization, the GHZ fibre, or deeper hafnian
integrability.

## Scope wall

```text
legal companion quotient sensor B(z):                 POLYNOMIAL;
target-incidence ideal I_219(B):                       EXACT SYMBOLIC;
simple-incidence line from 218-minor covariant:        PROVED;
pullback pentad, gate, alignment weights 5,8,17:       PROVED;
weighted amplitude tau has relative weight 15:        PROVED;
Laurent pair ideal is exact for all 21 Q-pair entries: PROVED ON OPEN;
pentads and alignment minors follow from pair ideal:   PROVED;
ambient incidence forces eta:                         FALSE;
ambient incidence plus eta forces pentad/alignment:   FALSE;
same non-forcing inside legal companion image:         UNKNOWN;
legal localized ideal J_pair is the unit ideal:        UNKNOWN;
legal full-sensor simple target-incidence point:       UNKNOWN;
prescribed GHZ amplitude compatibility:                UNKNOWN;
other 105 four-deck entries and upper decks:           STILL REQUIRED;
P7 obstruction or construction:                       UNKNOWN;
global Krenn--Gu:                                      UNRESOLVED.
```

## Exact replay

```powershell
uv run --with sympy python claims/p7/verify_legal_companion_simple_incidence_weighted_pullback_ideal.py
python claims/p7/audit_legal_companion_simple_incidence_weighted_pullback_ideal.py
python -m py_compile verify_legal_companion_simple_incidence_weighted_pullback_ideal.py audit_legal_companion_simple_incidence_weighted_pullback_ideal.py
uv run --with ruff ruff check verify_legal_companion_simple_incidence_weighted_pullback_ideal.py audit_legal_companion_simple_incidence_weighted_pullback_ideal.py
```

The primary replay verifies the maximal-minor kernel identity, chart
covariance, weights, ideal consequences, and the fixed exact decks (27)--(30)
with symbolic determinants.  The independent standard-library audit uses a
separately written Bareiss determinant and rational linear solver.  The
replays audit the displayed identities; they do not search any graph or
parameter family and do not expand the determinantal ideal (6).
