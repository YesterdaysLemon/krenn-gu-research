# Nonprojective root-pair fan selector tomography

## Status

**Exact characteristic-zero selector theorem with a sharp two-sensor
criterion.**  A nonprojective two-root jet on a four-port window does not
merely give one weighted marked star.  Retaining both tangent variables gives
four linear observation channels at once.  The six complementary pair faces
enter through the mixed second zeon compound

```text
K(A,B)_(uv)=a_u tensor b_v+a_v tensor b_u.             (1)
```

Here `a_u` and `b_u` are the two roots' tangent incidence covectors at port
`u`.  The resulting `4 x 6` fan matrix has rank at most four.  On a nonempty
Zariski-open chart it has rank exactly four and therefore leaves an exact
two-dimensional invisible pair-face space.  This proves that one fully
polarized root pair is still insufficient for tetrahedral pair tomography.

Two root-pair fans on the same physical four-window recover all six faces if
and only if their two invisible planes are transverse, equivalently their
stacked fan matrix has rank six.  This criterion is sharp: two explicit
integer fans have ranks `4,4` and stacked rank six.  It replaces the earlier
unit-weight four-star condition by the exact observation-matroid condition
for arbitrary nonprojective root incidence.

The theorem is an observation theorem, not a forced `P_7` extraction.  To
apply it, the two mixed-root sectors must be legally isolated on one common
shore, and nuisance root--root/residual companion columns and the relevant
top faces must be selected or subtracted.  Current theory does not force two
such co-occurring transverse fans.  The projectively constant branch has
`A=B=0` and remains invisible.  No `P_7` nonrestriction or global Krenn--Gu
proof is claimed; both remain **UNKNOWN/UNRESOLVED**.

No graph, support, colour-word, matching-family, or parameter enumeration is
used.

## 1. The polarized permanental fan

Let `E,F` be two-dimensional tangent spaces over a characteristic-zero
field, and let

```text
W={1,2,3,4}.
```

At the two differentiated roots, write the root-to-port tangent covectors as

```text
a_u in E^*,             b_u in F^*,          u in W.  (2)
```

If the roots use the port pair `{u,v}`, the two assignments give the exact
bilinear coefficient

```text
kappa_uv=a_u tensor b_v+a_v tensor b_u
         in E^* tensor F^*.                            (3)
```

Choose bases of `E^*,F^*`, let `A,B` be the `2 x 4` matrices whose columns
are `a_u,b_u`, and order the port pairs as

```text
12,13,14,23,24,34.                                    (4)
```

The **fan matrix** `K(A,B)` is the `4 x 6` matrix with columns (3), after
flattening `E^* tensor F^*` in the chosen product basis.

For a face vector `c=(c_uv)`, let `X(c)` be the hollow symmetric `4 x 4`
matrix with off-diagonal entries `c_uv`.

### Theorem 1 (hollow sandwich identity)

```text
K(A,B)c = vec(A X(c) B^T).                             (5)
```

Consequently

```text
ker K(A,B)={c:A X(c)B^T=0},
rank K(A,B)<=4.                                        (6)
```

Proof.  Expanding the matrix product gives

```text
A X(c)B^T
 =sum_(u<v)c_uv(a_u b_v^T+a_v b_u^T),                 (7)
```

which is precisely the unflattened sum of the columns (3).  The kernel and
rank statements follow.

Equation (5) is the bosonic, unsigned analogue of a polarized compound map.
The columns are permanents of the two labelled root rows on each port pair;
they are not exterior minors and obey no alternating signs.

## 2. Exact observability and invisible deformations

Suppose a legally isolated root-pair sector has complementary face vector
`z=(z_e)_(e in binom(W,2))`.  If roots use `p`, the surviving response is on
the complementary edge `e=W\p`.  Let `J` be the `6 x 6` permutation matrix
implementing this complement involution.  The full polarized sector observes

```text
K(A,B) J z.                                            (8)
```

### Theorem 2 (fan selector criterion)

A linear face combination `lambda^T z` is recoverable from (8) for every
face vector if and only if

```text
lambda in rowspace(K(A,B)J).                           (9)
```

Every deformation

```text
z -> z+J n,              n in ker K(A,B),             (10)
```

is invisible.  Thus one root pair can recover all six faces only if
`rank K(A,B)=6`, which is impossible by (6).

Proof.  The obtainable linear functionals are exactly the row space of the
observation matrix in (8).  Equation (10) changes the output by `K n=0`.

This is stronger than fixing one tangent direction at each root.  A fixed
direction gives one scalar row of (8); complete polarization gives all four
rows, but the two-dimensional fan defect remains generically.

## 3. The generic defect is exactly two

Take

```text
A_1=[1 0 1 0]       B_1=[1 0 0 1]
    [0 1 0 1],          [0 1 1 0].                   (11)
```

In the pair order (4),

```text
K_1=
[0 1 1 0 0 1]
[1 1 0 1 0 0]
[1 0 1 0 1 0]
[0 0 0 1 1 1].                                        (12)
```

It has rank four and kernel

```text
n_1=(0,1,-1,-1,1,0),
n_2=(1,0,-1,-1,0,1).                                  (13)
```

### Corollary 3 (generic rank-four fan)

The rank-four locus of `K(A,B)` is a nonempty Zariski-open subset of the
space of two `2 x 4` incidence matrices.  On that locus the invisible face
space has dimension exactly two.

Proof.  One `4 x 4` minor of (12) is nonzero.  The same minor is a polynomial
in the entries of `A,B`, so its nonvanishing defines a nonempty open chart.
The rank upper bound is four, and rank-nullity gives the defect.

The vectors (13) are honest response ambiguities: adding either one to the
port-use coefficient vector, or its complement permutation to the surviving
pair-face vector, leaves the entire polarized root-pair sector unchanged.

## 4. Two-fan tomography

Let two legally isolated root-pair sectors on the same window have fan
matrices `K_1,K_2`.  Their combined observation is

```text
[K_1 J]
[K_2 J] z.                                             (14)
```

### Theorem 4 (transverse-fan criterion)

The two sectors recover all six pair faces if and only if

```text
rank [K_1;K_2]=6,                                     (15)
```

equivalently

```text
ker K_1 intersect ker K_2={0}.                        (16)
```

When both fans have rank four, condition (16) says exactly that their two
defect planes in the six-dimensional face space are transverse.

Proof.  The complement matrix `J` is invertible, so it does not change rank.
Full recovery is full column rank of (14).  The kernel of a stacked matrix is
the intersection of the two kernels, proving the equivalence.

This bound is sharp.  Keep `A_1,B_1` from (11) and take

```text
A_2=[1 0 1 1]       B_2=[1 0 1 2]
    [0 1 1 2],          [0 1 2 1].                   (17)
```

Then

```text
K_2=
[0 2 3 0 0 3]
[1 2 1 1 1 3]
[1 1 2 1 2 4]
[0 0 0 3 3 5].                                        (18)
```

Both `K_1,K_2` have rank four, while their stack has rank six.  The minor
using all four rows of `K_1` and the first two rows of `K_2` has determinant
four.  Hence transverse two-fan tomography occurs on a nonempty Zariski-open
set of fan pairs.

## 5. Exact `P_7` interface

Use a clean four-window with roots split as

```text
R=J disjoint_union I,       |J|=3, |I|=2,
B=D disjoint_union W,       |D|=3, |W|=4,             (19)
```

and nonzero shore factor `f=per H[J,D]`.  Retain both tangent variables at
the roots in `I`.  In the sector where those roots use `p subset W`, the
coefficient on the complementary residual-present pair face is exactly

```text
f (a_u tensor b_v+a_v tensor b_u) z_(W\p).            (20)
```

Summing over the six port pairs gives (8), multiplied by the same nonzero
`f`.  Thus Theorems 1--4 are the exact linear observation theory of the
nonprojective marked sector; they do not replace an edge derivative by
fiat.

There are three additional legality requirements.

1. Root--root and root--residual companion sectors contribute nuisance
   columns.  They must be independently selected, subtracted through a
   synchronized top depth, or included in a larger observation matrix.
2. Two-fan recovery needs two root pairs on the same physical window with
   nonzero compatible shores.  Separate windows do not automatically share
   their six face coordinates.
3. Recovering both the residual-present pair vector `z_2` and the direct
   pair vector `m_2` needs synchronized companion depths.  Once both are
   recovered, the four-port coefficient of the exact discriminant

   ```text
   MZ-Y_0Y_1=hM^2                                      (21)
   ```

   is a legal test of the common graph response.

Inside the projectively constant branch every tangent root--blocker covector
in (2) is zero, so `K(A,B)=0`; the theorem correctly supplies no cross-depth
observation there.  Outside that branch, a generic pair gives four channels
and two transverse pairs suffice algebraically.  The missing theorem is now
co-occurrence and nuisance separation, not fan normalization.

## Literature interface

The fan columns are the order-two mixed permanental compound of two labelled
row maps.  They belong to the commuting zero-square, or zeon, calculus in
which induced compound entries are permanents; see Feinsilver and McSorley,
[*Zeons, Permanents, the Johnson Scheme, and Generalized Derangements*](https://doi.org/10.1155/2011/539030).
The observation criterion is ordinary linear-systems duality applied to that
compound.  The hollow sandwich identity (5), the complement-face
interpretation (8), and the transverse two-fan criterion are the
problem-specific content.

## Scope wall

```text
polarized two-root fan matrix K(A,B):                 PROVED;
hollow sandwich identity A X B^T:                    PROVED;
one-fan observation rank:                            AT MOST FOUR;
generic one-fan defect:                              EXACTLY TWO;
two-fan full tomography criterion:                   PROVED;
transverse rank-six fan pair:                        CONSTRUCTED;
projective root branch fan:                          ZERO;
forced nonprojective fan in every witness:           UNKNOWN;
two compatible clean shores on one window:           UNKNOWN;
nuisance companion-column separation:                UNKNOWN;
synchronized recovery of both m_2 and z_2:           UNKNOWN;
unrestricted P5/P6/P7 nonrestriction:                UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_nonprojective_root_pair_fan_selector_tomography.py
python claims/arbitrary-order/audit_nonprojective_root_pair_fan_selector_tomography.py
python -m py_compile claims/arbitrary-order/verify_nonprojective_root_pair_fan_selector_tomography.py claims/arbitrary-order/audit_nonprojective_root_pair_fan_selector_tomography.py
uv run --with ruff ruff check claims/arbitrary-order/verify_nonprojective_root_pair_fan_selector_tomography.py claims/arbitrary-order/audit_nonprojective_root_pair_fan_selector_tomography.py
```

The primary verifier checks the generic hollow-sandwich identity, the exact
rank-four fan and its kernel, the transverse stacked minor, complement
permutation, and invisible deformation.  The independent no-import audit
uses separate integer matrix arithmetic and exact rational row reduction.
Neither replay searches graphs, supports, words, matchings, or parameter
families.
