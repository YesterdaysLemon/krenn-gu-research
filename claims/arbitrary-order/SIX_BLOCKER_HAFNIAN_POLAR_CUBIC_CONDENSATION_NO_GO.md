# No cubic polar-condensation identity for the six-vertex hafnian

## Status

**Exact characteristic-zero invariant-theory no-go.**  Let `h` be the
generic scalar hafnian on six labelled vertices and let

```text
C_ij=partial h/partial x_ij=haf X[V minus {i,j}]       (1)
```

be its fifteen principal four-vertex cofactors.  There is no cubic
polynomial `P` such that

```text
h^2=P((C_ij)_(i<j)).                                  (2)
```

Thus the first possible determinant-style or multiplicative-Legendre
condensation formula does not exist for the generic six-vertex hafnian.
Together with principal-cofactor dominance, this says that a scalar
cross-depth relation involving `h` and all `C_ij` must have weighted degree
at least eight when `weight(C)=2` and `weight(h)=3`.

The proof uses the eight symbolic `S_6` orbit types of loopless three-edge
multigraphs and nine coefficient functionals.  It does not enumerate graph
supports, blocker words, alignments, parameter points, or candidate
restrictions.

This is a proof-route no-go, not a Krenn--Gu obstruction by itself.  On
special fibres such as `C=0`, higher equations can still force `h=0`.  The
physical marked-star problem also involves tensor-valued common cofactors,
not only the scalar polar map.  The `P_7` restriction and the global
Krenn--Gu conjecture remain **UNRESOLVED**.

## 1. The polar data

Work over a characteristic-zero field `K`.  On the edge variables of `K_6`,

```text
h=sum_(M a perfect matching of V) product_(e in M)x_e. (3)
```

There are fifteen matching monomials.  Differentiation gives (1): every
`C_ij` is the sum of the three perfect-matching monomials on the complementary
four vertices.

The source variables have weight one, so

```text
weight(C_ij)=2,                    weight(h)=3.         (4)
```

The lowest homogeneous equation that could mix `h` with the cofactors has
weight six and therefore has the form (2).

If an arbitrary cubic `P` satisfied (2), average it over `S_6`.  The left
side is invariant, so the averaged cubic still satisfies (2).  Division by
`|S_6|=720` is legal in characteristic zero.  It is consequently enough to
exclude invariant cubics.

## 2. The eight invariant cubic orbit sums

A cofactor monomial `C_e C_f C_g` is indexed by a loopless multigraph with
three edges, repetitions allowed.  Up to vertex relabelling there are exactly
eight types:

```text
T3:       one triple edge;
DA:       one double edge and an adjacent single edge;
DD:       one double edge and a disjoint single edge;
K3:       a triangle;
K13:      a three-edge star;
P4:       a three-edge path;
P3K2:     a two-edge path plus a disjoint edge;
3K2:      a three-edge matching.                       (5)
```

Let `O_tau(C)` be the sum of the distinct cofactor monomials of type `tau`.
Every invariant cubic is uniquely a linear combination

```text
P=sum_tau a_tau O_tau.                                (6)
```

Uniqueness follows because the cofactor monomials themselves have disjoint
orbit types.

## 3. Eight separating coefficients

Use lexicographic edge names.  The following source monomials give a diagonal
coefficient table.  In each row, the displayed orbit sum is the only one
with a nonzero coefficient.

| orbit | source monomial | coefficient in `O_tau(C)` | coefficient in `h^2` |
|:--|:--|--:|--:|
| `T3` | `x01^3 x23^3` | `1` | `0` |
| `DA` | `x01^3 x23^2 x24` | `1` | `0` |
| `DD` | `x01^3 x23^2 x45` | `1` | `0` |
| `K3` | `x01^3 x23 x24 x25` | `1` | `0` |
| `K13` | `x01^3 x23 x24 x34` | `1` | `0` |
| `P4` | `x01^3 x23 x24 x35` | `1` | `0` |
| `P3K2` | `x01^2 x02 x23 x34 x45` | `2` | `0` |
| `3K2` | `x01^2 x23^2 x45^2` | `1` | `1` |

The table is read directly from (1).  For example, a factor `C_45` has the
three terms

```text
x01 x23,                 x02 x13,                 x03 x12. (7)
```

The exponent pattern of each displayed source monomial determines the three
complementary four-vertex matchings and hence the unique multigraph type in
(5).  The factor two in the `P3K2` row is the only repeated factorization.

Comparison with (6) and `h^2` forces

```text
a_T3=a_DA=a_DD=a_K3=a_K13=a_P4=a_P3K2=0,
a_3K2=1.                                               (8)
```

## 4. The two-triangle contradiction

Now take

```text
Omega=x01 x02 x12 x34 x35 x45.                        (9)
```

This is the product of the edge sets of the two disjoint triangles `012` and
`345`.  Its coefficient in `h^2` is zero.  Indeed, the union of two perfect
matchings is a disjoint union of doubled edges and even alternating cycles;
it cannot be two odd cycles.

In contrast,

```text
[Omega] O_3K2(C)=6.                                   (10)
```

There are six ways to choose the three complementary cofactor matchings that
produce the two oriented triangle cycles.  Equations (8)--(10) contradict
(2), since `6!=0` in characteristic zero.

### Theorem 1 (cubic polar-condensation no-go)

No cubic polynomial in the complete principal four-cofactor array of the
generic six-vertex hafnian equals the square of the full hafnian.

## 5. Exact cross-depth consequence

The principal-cofactor map `x -> C` is dominant in characteristic zero by
`HAFNIAN_PRINCIPAL_COFACTOR_GRADIENT_DOMINANCE.md`.  Hence there is no
cofactor-only equation, and a weight-seven equation would have the form
`h Q_2(C)=0`; dominance and the fact that `h` is nonzero force `Q_2=0`.
Theorem 1 removes weight six.  Therefore the first possible nonzero relation
between `h` and `C` has weighted degree at least eight, for example a
combination of `P_4(C)` and `h^2 L(C)`.

This explains why determinant/Pfaffian condensation does not transfer to the
bosonic six-blocker chart.  Shuffle-algebra hafnian identities organize Wick
expansion, but they do not supply a sign-free Pluecker equation of the form
(2); see Luque--Thibon,
[*Pfaffian and hafnian identities in shuffle algebras*](https://arxiv.org/abs/math/0204026).
The multiplicative-Legendre framework motivates (2), but Theorem 1 directly
rules out its polynomial cubic form for this hafnian; compare Chaput--Sabatino,
[*On homaloidal polynomial functions of degree 3 and prehomogeneous vector
spaces*](https://arxiv.org/abs/1011.5975).

For the current `P_7` programme this gives a strict routing rule:

```text
all fifteen scalar four-cofactors
    !=> full six-point hafnian by a cubic condensation law;

successful cross-depth bridge
    => higher weighted relation, special-fibre theorem,
       or tensor-valued physical incidence.                         (11)
```

The target-null fan sits on a special zero fibre and must be treated with
its separate matching-number theorem; Theorem 1 neither proves nor refutes a
physical `P_7` lift.

## Scope wall

```text
generic six-vertex identity h^2=cubic(C):       IMPOSSIBLE;
lowest bosonic polar-condensation weight:       AT LEAST EIGHT;
plain determinant/Pfaffian condensation route: CLOSED;
higher polar relation:                          EXISTS ABSTRACTLY, UNKNOWN FORM;
special zero-cofactor fibre:                    SEPARATE;
tensor-valued marked-star bridge:               UNKNOWN;
P7 and global Krenn--Gu:                        UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_six_blocker_hafnian_polar_cubic_condensation_no_go.py
python audit_six_blocker_hafnian_polar_cubic_condensation_no_go.py
python -m py_compile verify_six_blocker_hafnian_polar_cubic_condensation_no_go.py audit_six_blocker_hafnian_polar_cubic_condensation_no_go.py
uv run --with ruff ruff check verify_six_blocker_hafnian_polar_cubic_condensation_no_go.py audit_six_blocker_hafnian_polar_cubic_condensation_no_go.py
```

The primary replay constructs the generic hafnian and the eight exact
`S_6` orbit sums, then checks only the nine displayed coefficient
functionals.  The independent no-import audit uses rational sparse
polynomials and a separate orbit construction.  These are fixed symmetry
replays of the proof, not searches over graph supports or candidate words.
