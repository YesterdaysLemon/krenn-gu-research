# Arbitrary permanent co-two equality-five active-support orbit synthesis

## Status

This note composes four already proved pair-level results into one exact
characteristic-zero boundary for every omitted pair of a weighted diagonal
restriction

```text
P_r -> Delta_3,                         r>=3.               (1)
```

For an omitted pair `{a,b}`, let

```text
U_a=span{u_(a,0),u_(a,1),u_(a,2)},
U_b=span{u_(b,0),u_(b,1),u_(b,2)},
B_ab=U_a U_b subset (Z_r)_2,                                  (2)
```

and let `A_S` be the complementary product sensor owned by the co-two
sensor theorem.  If

```text
dim B_ab=5,                                                   (3)
```

then the active coordinate support of `U_a+U_b` has size exactly four.
After moving those four coordinates to `x_0,...,x_3`, applying nonzero
coordinate scalings, and changing bases inside `U_a` and `U_b`, the
underlying pair is one of exactly three unbased `r=4` orbits:

```text
(3,1),                    (4,1),                    (4,2).   (4)
```

These labels are the normal-support/sign-split labels of the `r=4` orbit
classification; all three pairs use four active ambient coordinates.  Each
orbit admits an explicit pair-level `Delta_3` frame, replayed below.

Consequently, for every omitted pair in an actual restriction,

```text
|supp(U_a+U_b)|>=5
  => dim B_ab>=6
  => dim A_S<=binomial(r,2)-3.                               (5)
```

The conclusion in (4) is necessary, not sufficient, for a full restriction.
It classifies the underlying unbased pair, not the finer orbit of the given
colour bases together with their radical under the stabilizer of `Delta_3`.
In particular, it does not assert that any of the three displayed frames
extends through the other `r-2` modes.  Unrestricted `P_6 -> Delta_3`,
arbitrary-order permanent nonrestriction, and the global Krenn--Gu
conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. Frozen dependencies

This is a synthesis theorem: its load-bearing proofs remain in the four
owning packages below.  The exact dependency commits in the present branch
and the SHA-256 hashes of their theorem documents are

```text
4a3a0988f4fc837844bbcd3a57fa408a7850c521
  ARBITRARY_PERMANENT_COTWO_PRODUCT_SENSOR_CORANK_TWO_STRENGTHENING_THEOREM.md
  486cc700d12f99fc72997db918d816efcf5368ae6b45adf722a4aa38abf0d0b8

82928ccdc1faaa2519671e9d13680519f068038c
  ARBITRARY_PERMANENT_PAIR_DIMENSION_FIVE_R4_ORBIT_CLASSIFICATION_THEOREM.md
  4b7fccccf68b55e1ddeacb7328b7469a8a82f36aa2ab0303e9094519a95fc5bc

e9e9d47643c4d8dbcb6bf194de66f84fc37b746c
  ARBITRARY_PERMANENT_ACTIVE_SUPPORT_FIVE_EQUALITY_EXCLUSION_THEOREM.md
  de7fa0633e0d79796a5f76528f7b79bc99655f3f0f549133df4651b71f6e83d2

e486e693f20672ffdf6e6a82f1214f30fb243b9b
  ARBITRARY_PERMANENT_ACTIVE_SUPPORT_AT_LEAST_SIX_EQUALITY_EXCLUSION_THEOREM.md
  d55aa47cda33cc749522164ac477935798b9e6bee1def41edaada80be9e645f7
```

The primary verifier and independent audit also pin the corresponding
primary-verifier and no-import-audit hashes.  A changed dependency is not
silently accepted as the theorem used here.

The imported statements, with their original scope preserved, are:

1. In every exact characteristic-zero restriction (1), the local colour
   triples are independent, `dim B_ab>=5`, the complementary pairing has
   rank three, all six mixed-colour products lie in its left radical, the
   three same-colour products are independent modulo that radical, and

   ```text
   dim A_S+dim B_ab<=binomial(r,2)+3.                        (6)
   ```

2. For two three-planes in `Z_4` with product dimension five, there are
   five unbased monomial orbits.  Pair-level `Delta_3` admissibility holds
   exactly for `(3,1),(4,1),(4,2)` and fails for the coincident
   support-three orbit and `(2,1)`.

3. An active-support-five equality pair has the form
   `U=V=Kx_i direct-sum W`, with `dim W=2` and `dim(W^2)=3`, and is not
   pair-level `Delta_3` admissible.

4. The same structural conclusion and nonadmissibility hold for every
   active-support `n>=6` equality pair.

Items 3--4 are exclusion theorems for admissible equality frames, not
claims that equality-five pairs do not exist.  Indeed, their owning
packages exhibit exact nonadmissible equality pairs.

## 2. Pair-level admissibility forced by a restriction

Put

```text
M_ab={q in B_ab : <q,A_S>=0}.                              (7)
```

The complement pairing has rank three.  Under (3), therefore,

```text
dim M_ab=2.                                                (8)
```

The imported diagonal pairing identities say

```text
u_(a,c)u_(b,d) in M_ab,                         c!=d,       (9)
```

while the three residue classes

```text
u_(a,c)u_(b,c)+M_ab,                            c=0,1,2,   (10)
```

form a basis of `B_ab/M_ab`.  Thus the colour bases supplied by the full
restriction make `(U_a,U_b)` a pair-level `Delta_3`-admissible equality
frame.  Indeed, the nine displayed products span `B_ab`; the three diagonal
products contribute exactly three dimensions modulo `M_ab`, so the six
mixed products must span the whole two-space `M_ab`.  This is the only
implication from the other modes used in the support argument.

Notice the direction carefully: a full restriction supplies an admissible
pair.  An admissible pair does not by itself supply the other modes of a
full restriction.

## 3. The active support cannot have size below four

Let

```text
T=supp(U_a+U_b),                         m=|T|.             (11)
```

Both local triples are independent, so each of `U_a,U_b` has dimension
three.  Hence `m>=3`.

If `m=3`, each three-plane equals the full three-dimensional coordinate
space on `T`.  Its square-free quadratic product space has dimension only

```text
dim (Z_T)_2=binomial(3,2)=3,                               (12)
```

contradicting (3).  Therefore

```text
m>=4.                                                      (13)
```

This step uses the actual active support rather than the ambient value of
`r`; deleting inactive coordinates does not change any product in `B_ab`.

## 4. Supports five and above are incompatible with equality

Suppose first that `m=5`.  Delete the inactive ambient coordinates and
identify the active coordinate subalgebra with `Z_5`.  The resulting
three-planes use all five coordinates, retain product dimension five, and
retain the admissible colour frame from Section 2.  The active-support-five
exclusion says that no such frame is pair-level admissible, a contradiction.

If `m>=6`, the same deletion identifies the active subalgebra with `Z_m`.
The active-support-at-least-six exclusion applies with `n=m` and gives the
same contradiction.  Together with (13), this proves

```text
m=4.                                                       (14)
```

The reduction to `Z_m` is exact: coordinate deletion removes only
identically zero coefficients, so it changes neither the nine products,
their span, nor the mixed/diagonal quotient conditions.

## 5. The three surviving `r=4` orbits

Move the active coordinate set to `{0,1,2,3}`.  The `r=4` equality-five
classification now applies to the underlying pair `(U_a,U_b)`.  Its two
nonadmissible orbits are impossible by Section 2.  The remaining orbits are
exactly those in (4).

For transparency, use edge order

```text
(01,02,03,12,13,23).                                      (15)
```

The following exact frames replay one admissible representative of each
surviving unbased orbit.

### Type `(3,1)`

```text
u_0=x_1-x_2,       u_1=x_3,          u_2=-x_0+x_2,
v_0=-x_1+x_2,      v_1=x_0+x_1,      v_2=x_3.              (16)
```

The hyperplane normals are `(1,1,1,0)` and `(1,-1,-1,0)`.  The six mixed
products span the plane generated by

```text
(1,-1,0,-1,0,0),                  (0,0,0,0,1,-1).          (17)
```

### Type `(4,1)`

```text
u_0=-x_0+x_2,      u_1=x_0-x_3,       u_2=x_1-x_2,
v_0=x_0+x_1-x_2+x_3,
v_1=x_0+x_1,       v_2=-x_1+x_2.                            (18)
```

The normals are `(1,1,1,1)` and `(1,-1,-1,-1)`.  The mixed plane is
generated by

```text
(-1,1,0,1,0,0),                   (1,-1,0,0,-1,1).         (19)
```

### Type `(4,2)`

```text
u_0=x_0-x_3,       u_1=x_1-x_3,       u_2=x_2-x_3,
v_0=x_1+x_2,       v_1=x_0+x_2,       v_2=x_2-x_3.         (20)
```

The normals are `(1,1,1,1)` and `(1,1,-1,-1)`.  The mixed plane is
generated by

```text
(0,1,-1,0,0,-1),                  (0,0,0,1,-1,-1).         (21)
```

For each frame, the verifier checks exactly that the mixed products have
rank two and that adjoining the three diagonal products gives rank five.
The annihilator support graphs have degree multisets, respectively,

```text
(2,1,1,0),                    (3,1,1,1),
(2,2,2,2),                                                 (22)
```

which also separate the three unbased monomial orbits.

The existence of these representatives proves pair-level admissibility of
the three orbit types.  It does not show that every admissible choice of
colour bases is equivalent under a `Delta_3`-preserving transformation, and
it does not construct a full extension.

## 6. The improved sensor bound on active support at least five

Now drop hypothesis (3) and assume only that an omitted pair in an actual
restriction has `m>=5`.  The co-two theorem gives `dim B_ab>=5`.  Equality
would contradict Sections 2 and 4, so integrality gives

```text
dim B_ab>=6.                                               (23)
```

Writing `N=binomial(r,2)`, substitute (23) into (6):

```text
dim A_S<=N+3-dim B_ab<=N-3.                                (24)
```

This proves (5).  It is a conditional improvement attached to the active
support of the particular omitted pair; it does not say that every omitted
pair has support at least five.

## 7. Exact boundary

```text
dim B_ab=5 in a full restriction implies active support four: PROVED;
surviving unbased equality-five pair orbits:                 THREE;
their labels:                                                (3,1),(4,1),(4,2);
active support at least five implies dim B_ab>=6:             PROVED;
then dim A_S<=binomial(r,2)-3:                                PROVED;

classification of based frames under the Delta_3 stabilizer: NOT CLAIMED;
extension of any displayed pair through all other modes:      NOT CLAIMED;
existence of a full P_r -> Delta_3 restriction:                NOT IMPLIED;
unrestricted P_6 -> Delta_3:                                  UNKNOWN;
global Krenn--Gu conjecture:                                  UNRESOLVED.
```

## Replay

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_cotwo_equality_five_active_support_orbit_synthesis.py
python claims/arbitrary-order/audit_arbitrary_permanent_cotwo_equality_five_active_support_orbit_synthesis.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_cotwo_equality_five_active_support_orbit_synthesis.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_equality_five_active_support_orbit_synthesis.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_cotwo_equality_five_active_support_orbit_synthesis.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_equality_five_active_support_orbit_synthesis.py
```

The primary verifier uses exact symbolic linear algebra, checks every frozen
dependency hash, replays all three displayed rational frames, and checks the
dimension implications.  The independent audit imports neither the primary
verifier nor SymPy; it uses a standalone exact row reducer, independently
reconstructs the three product tables over the integers and two finite
fields, checks the dependency pins, and audits the complete support-case and
sensor-bound logic.  These scripts guard composition and transcription.
The characteristic-zero theorem is the written implication from the four
proved dependencies.
