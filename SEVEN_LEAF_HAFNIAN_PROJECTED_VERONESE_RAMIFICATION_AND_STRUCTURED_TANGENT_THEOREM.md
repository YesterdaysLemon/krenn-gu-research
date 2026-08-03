# The physical seven-leaf branch is structured ramification of a projected Veronese

## Status

**Exact characteristic-zero projective-geometric translation and strategy
no-go.**  Let

```text
A(L)=K[z_1,...,z_7]/(z_1^2,...,z_7^2),
V=A_2(L),                         dim V=21,
W=A_4(L),                         dim W=35.           (1)
```

The principal four-hafnian map is the Boolean square map

```text
H_4:V->W,                  F |-> F^2/2.               (2)
```

This note proves that (2) is a linear projection of the quadratic Veronese
embedding and that its differential is exactly Boolean multiplication:

```text
d(H_4)_F(K)=FK,
ker d(H_4)_F=Ann_2(F).                               (3)
```

Consequently every full-edge radial P7 extension from the preceding
leaf-annihilator theorem lies in the Jacobian rank-drop locus of `H_4`.
Its nonzero annihilator

```text
K=2ell A+tF,                 FK=0                    (4)
```

is the structured tangent direction killed by the projection.  On the
rank-20 leaf branch this direction is unique projectively; on the
rank-at-most-19 branch there are at least two affine annihilator directions.

This closes one plausible route: generic four-hafnian tomography, which
works on the full-Jacobian open set, cannot locally invert the physical
primitive radial branch because that branch is forced onto the ramification
locus.  The conclusion is symbolic and global on the branch, not evidence
from a sampled graph.

The theorem does **not** prove that the structured ramification incidence is
empty on the edge torus.  The rank-20 and rank-at-most-19 physical branches,
P7, and global Krenn--Gu remain **UNKNOWN/UNRESOLVED**.

## 1. Boolean multiplication is the projection center

Let

```text
m:Sym^2(V)->W                                      (5)
```

be multiplication in the Boolean algebra.  In the unordered edge-pair
basis, a column survives exactly when its two edges are disjoint; it then
maps to the four-set which is their union.  Every four-set has three such
perfect-matching columns, and columns belonging to different four-sets have
disjoint row support.  Therefore

```text
rank m=35,
dim ker m=binom(21+1,2)-35=231-35=196.              (6)
```

Let

```text
nu_2:P(V)->P(Sym^2 V)=P^230                         (7)
```

be the quadratic Veronese embedding and put

```text
Lambda=P(ker m)=P^195.                               (8)
```

Away from the base locus `F^2=0`, the projectivization of (2) is exactly

```text
P(H_4)=pi_Lambda composed with nu_2,                 (9)
```

where `pi_Lambda` is linear projection from the center (8).  Thus the
seven-leaf hafnian deck is not an arbitrary quadratic map: it is a fixed
high-center projection of a Veronese variety.

## 2. The tangent-center theorem

For `F,K in V`, the tangent to the Veronese curve
`nu_2(F+epsilon K)` is represented by the symmetric tensor `F symmetric K`.
Multiplication gives

```text
m(F symmetric K)=FK.                                (10)
```

On coefficients, for a four-set `U`, both sides equal

```text
sum_({e,g} perfect matching of U)
    (f_e k_g+f_g k_e).                              (11)
```

Equation (3) follows immediately.

### Theorem 1 (ramification equals a tangent-center intersection)

Let `F!=0` and `F^2!=0`.  Then the following are equivalent:

1. the projective four-hafnian map is ramified at `[F]`;
2. `Ann_2(F)!=0`;
3. the embedded tangent space to `nu_2(P(V))` at `[F symmetric F]`
   meets the projection center `Lambda`.

More precisely,

```text
Lambda intersect T_(nu_2([F]))nu_2(P(V))
  =P({F symmetric K:K in Ann_2(F)}),                 (12)
```

so the intersection has projective dimension
`dim Ann_2(F)-1`.

### Proof

The Veronese tangent space is

```text
P({F symmetric K:K in V}).                          (13)
```

For nonzero `F`, the map `K -> F symmetric K` is injective.  Indeed, choose
a nonzero coordinate `f_e`.  The `(e,e)` symmetric coordinate first forces
`k_e=0`, and then every `(e,g)` coordinate forces `k_g=0`.  Equations
(8), (10), and (13) now prove (12).

For completeness, the projective differential sends

```text
K mod KF  |->  FK mod K F^2.                        (14)
```

If (14) vanishes, write `FK=lambda F^2`.  Then
`F(K-lambda F)=0`; a nonzero projective tangent has
`K-lambda F!=0`.  Conversely every nonzero annihilator supplies such a
kernel direction.  This proves all three equivalences.

The affine statement (3) remains valid even on the square-zero base locus,
where the projective map (9) itself is undefined.

## 3. Primitive ramification incidence

The primitive four-form target is

```text
N_4=ker(ell:A_4(L)->A_5(L)),             dim N_4=14. (15)
```

The dimension follows from Boolean strong Lefschetz: the displayed map has
rank 21.  Hence the nonzero primitive-square locus is the inverse image

```text
P(H_4)^(-1)(P(N_4))                                   (16)
```

inside the projected Veronese.

The preceding physical leaf-annihilator theorem adds a tangent condition.
A full-edge primitive leaf square extends radially to P7 exactly when there
are full-support `A`, nonzero `t`, and nonzero `K` satisfying

```text
ell F^2=0,
K=2ell A+tF,
FK=0.                                                (17)
```

Equivalently, if `C=ell A_1` and `pi:V->V/C`,

```text
[F symmetric K] in Lambda intersect T_(nu_2([F])),
pi(K)=t pi(F),
K-tF in C,                                           (18)
```

with the seven recovered star coefficients nonzero.  Call (17)--(18) the
**primitive structured-ramification incidence**.  This is a new organizing
object, but its equivalence to radial extension is a theorem, not a proposed
analogy.

If `rho=rank d(H_4)_F=rank mu_2(F)`, then

```text
rho=20  => Lambda meets the Veronese tangent in one projective point;
rho<=19 => the tangent-center intersection has dimension at least one. (19)
```

The additional quotient-singular equation remains the structured cubic
syzygy

```text
2t Phi_N(G)=F(2AG-t(partial G)F).                    (20)
```

Thus (18) is the quadratic tangent-center layer and (20) is its cubic
syzygy refinement.

## 4. Why generic four-deck tomography cannot close this branch

At the all-one graph, (3) is the `2`-set versus `4`-set inclusion matrix and
has rank 21.  The earlier arbitrary-order tomography theorem therefore
gives a nonempty full-Jacobian open set on which finitely many principal
four-hafnians are local coordinates.

Every physical radial extension has the nonzero kernel vector (4), so

```text
rank d(H_4)_F<=20.                                   (21)
```

It is disjoint from that open set.  Therefore a proof strategy which first
places the physical primitive branch on the generic local-inversion chart
cannot succeed.  A viable next tool must instead analyze the structured
tangent-center intersection (18), its rank stratification, or the cubic
syzygy (20).

This does not contradict generic finiteness of `H_4`: a generically finite
map may ramify on a proper locus, and the physical equations force exactly
that exceptional locus.

## 5. Literature translation

Tangential varieties and their representation-theoretic equations are a
standard part of Segre--Veronese geometry; see Oeding and Raicu,
[*Tangential varieties of Segre--Veronese
varieties*](https://arxiv.org/abs/1111.6202).  That work supplies the ambient
tangential-variety language, not equations (12), (17), or (18).

The new transfer is the identification of Boolean four-hafnian
multiplication with the projection (9), followed by the observation that
the physical P7 annihilator is exactly a projection-center tangent.  The
Boolean strong-Lefschetz background for (15) is supplied by
[Cook](https://arxiv.org/abs/1111.4979) and the Boolean `sl_2` model by
[Feinsilver](https://arxiv.org/abs/1102.0368).

## 6. Exact wall

```text
Boolean multiplication Sym^2(A_2)->A_4:             SURJECTIVE;
projection-center vector/projective dimensions:      196 / 195;
four-hafnian map:                                    PROJECTED VERONESE;
four-hafnian differential at F:                      mu_2(F);
affine differential kernel:                          Ann_2(F);
projective ramification iff Ann_2(F) nonzero:         PROVED;
tangent-center intersection:                         P(F symmetric Ann_2(F));
primitive four-form target dimension:                14;
physical radial extension lies in ramification:      PROVED;
physical branch meets generic tomography open:        IMPOSSIBLE;
rank-20 tangent-center point:                         UNIQUE PROJECTIVELY;
rank-at-most-19 tangent-center family:                POSITIVE-DIMENSIONAL;
structured ramification incidence meets edge torus:  UNKNOWN;
rank-20 cubic-syzygy refinement has a torus point:    UNKNOWN;
rank-at-most-19 physical extension has a torus point: UNKNOWN;
P7 and global Krenn--Gu:                              UNRESOLVED. (22)
```

No graph/support enumeration, numerical approximation, finite-field
inference, parameter sweep, Groebner elimination, or timeout is used.

## Replay

```powershell
uv run --with sympy python verify_seven_leaf_hafnian_projected_veronese_ramification.py
python audit_seven_leaf_hafnian_projected_veronese_ramification.py
python -m py_compile verify_seven_leaf_hafnian_projected_veronese_ramification.py audit_seven_leaf_hafnian_projected_veronese_ramification.py
uv run --with ruff ruff check verify_seven_leaf_hafnian_projected_veronese_ramification.py audit_seven_leaf_hafnian_projected_veronese_ramification.py
```

The primary verifier builds the exact `35 x 231` Boolean multiplication
projection, proves its rank and kernel dimension, checks the complete
symbolic tangent/Jacobian identity, and verifies both the all-one unramified
control and the 14-dimensional primitive target.  The independent
standard-library audit reconstructs the multiplication, derivative, and
Lefschetz maps using separate combinatorics and exact rational row
reduction, without importing the primary script or project code.
