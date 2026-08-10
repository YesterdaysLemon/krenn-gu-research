# P6 clean two-by-three selector: Segre pullback and torus permission

## Status

**Exact arbitrary-chart characteristic-zero compatibility theorem and a
coordinate-torus permission result.**  After one nonzero four-root
root--root shore has been legally selected, the clean `2 x 3` permanental
fan of the principal-deletion theorem is a linear map

```text
O: K^6 -> K^2 tensor K^3.                              (1)
```

On an invertible fan chart, a clean diagonal GHZ output first forces every
one of the six principal-deck tensors itself into the diagonal blocker
space.  It does not force the shore to vanish and does not force `det O=0`.
Instead, for each target colour it forces the six face coefficients to lie
in the inverse image under `O` of the rank-one `2 x 3` determinantal cone.
Equivalently, three explicit quadrics -- the pulled-back `2 x 2` minors --
vanish.  Projectively this is a linear copy of

```text
Seg(P^1 x P^2) subset P^5,                             (2)
```

of codimension two and degree three.

This condition is a genuine obstruction on a proposed physical deletion
deck, but it is not a no-go by itself.  For **every** invertible fan `O`, the
pulled-back Segre cone meets the six-coordinate torus.  Three such torus
points may simultaneously be chosen so that their left factors span two
dimensions and their right factors span three dimensions, exactly the local
rank pattern required by a concise three-colour target slice.

A symbolic all-incidence-nonzero fan family makes the permission concrete.
For four distinct parameters `t_0,...,t_3`, put

```text
a(t)=(1,t),                  b(t)=(1,t^2,t^3),         (3)
```

and use the six permanental columns

```text
kappa_ij=a(t_i) tensor b(t_j)+a(t_j) tensor b(t_i).
```

Their determinant is

```text
-2 product_(i<j)(t_i-t_j)^2 (t_0+t_1+t_2+t_3).        (4)
```

Thus distinct nonzero parameters with nonzero sum give an invertible fan
without placing any root--residual incidence coordinate on a boundary.
At `(t_0,t_1,t_2,t_3)=(1,2,3,4)`, an explicit three-colour face table has
all eighteen entries nonzero and maps to three rank-one GHZ slices.  The
same certificate includes a nonzero root--root bilinear form which vanishes
at the original common root vectors but is nonzero at the selected
polarization.  Therefore neither GHZ diagonality nor coordinate-boundary
considerations can close the P6 selector.

What remains is more precise: the physical principal-hafnian response
variety, nuisance-column separation, the depth-four companion sector, and
the three fixed target-factor lines must meet this pulled-back Segre locus
on one synchronized graph.  That intersection is **UNKNOWN**.  No physical
`P_6 -> Delta_3` restriction, Krenn--Gu counterexample, or global proof is
claimed.  Global Krenn--Gu remains **UNRESOLVED**.

No graph, support, colour word, matching family, parameter grid, finite
field, or numerical point is searched.  Formula (4), the target equations,
and the displayed permission point are exact symbolic identities.

## 1. The selected clean depth-two sector

Work over a characteristic-zero field `K`.  Split four probe roots into a
shore pair and two residual-active roots.  Let

```text
E=K^2,                         F=K^3,                 (5)
W={0,1,2,3}.
```

At the two active roots let the root-to-window incidence covectors be

```text
a_u in E^*,                    b_u in F^*,            (6)
```

and order the six window pairs as

```text
01,02,03,12,13,23.                                      (7)
```

The mixed permanental fan is

```text
K(A,B)e_uv=a_u tensor b_v+a_v tensor b_u.             (8)
```

Depending on whether the response coordinates are labelled by the deleted
pair or its surviving complementary pair, the physical observation matrix
is either `K(A,B)` or `K(A,B)J`, where `J` is the six-by-six complement
permutation.  Write either convention as `O`; since `J` is invertible, all
statements below are convention-independent.

Let `T` be the blocker tensor space, let `D subset T` be its three-dimensional
GHZ diagonal space with basis `delta_0,delta_1,delta_2`, and initially let
the six selected principal-deck tensors `Z_e` be arbitrary members of `T`.

Let `L` be the chosen root--root bilinear shore and let `psi` be the legal
shore coefficient functional.  Put

```text
alpha=psi(L).                                           (9)
```

The word **clean** means that every competing root--root grade and every
depth-zero/depth-four or blocker nuisance column is zero or has already been
independently subtracted with the same normalization.  The isolated
depth-two observation is then

```text
alpha sum_e (O e)_active tensor Z_e.                  (10)
```

Call the grade **target-clean** when the same synchronized coefficient
bookkeeping identifies (10) itself with a GHZ target slice.  This is stronger
than merely subtracting an arbitrary known nuisance tensor from the total
target: such a subtraction need not remain diagonal.  Every diagonal
conclusion below assumes target-cleanliness.  Column separation alone does
not supply it.

### Proposition 1 (fan inversion forces deck diagonality)

Assume `alpha!=0` and `O in GL_6(K)`.  If the target-clean observation (10)
lies in

```text
E^* tensor F^* tensor D,
```

then every `Z_e` lies in `D`.

### Proof

Apply the quotient map `pi:T -> T/D` to the last tensor factor in (10).  The
result is

```text
alpha (O tensor id) (pi(Z_e))_e=0.
```

Both `alpha` and `O` are invertible, so every `pi(Z_e)` is zero.  Hence every
deck tensor is diagonal.  Write

```text
Z_e=sum_(c=0)^2 z_e^(c) delta_c,
z^(c)=(z_e^(c))_(e in binom(W,2)).                    (11)
```

For a GHZ target, let `r_c in E^*` and `s_c in F^*` be the restrictions of
the target coordinate covector of colour `c` to the two chosen active-root
polarization spaces.  Let `mu_c` be the nonzero product of the global target
coefficient and the selected shore coefficient on colour `c`.  Comparison
of the `delta_c` coefficients in (10), using (11), gives the exact clean
selector equation

```text
alpha O z^(c)=mu_c vec(r_c s_c^T),       c=0,1,2.     (12)
```

This equation is the diagonal target constraint at the legal selector
grade.  It contains no formal edge derivative.

## 2. The pulled-back Segre obstruction

For `y=(y_00,y_01,y_02,y_10,y_11,y_12)^T`, set

```text
q_01(y)=y_00 y_11-y_01 y_10,
q_02(y)=y_00 y_12-y_02 y_10,
q_12(y)=y_01 y_12-y_02 y_11.                          (13)
```

These are the three two-by-two minors of the associated `2 x 3` matrix.

### Theorem 1 (arbitrary-chart GHZ/Segre criterion)

Assume `alpha!=0` and `O in GL_6(K)`.

1. Every clean diagonal target slice satisfies

   ```text
   q_01(O z^(c))=q_02(O z^(c))=q_12(O z^(c))=0        (14)
   ```

   for each colour `c`.

2. Conversely, a nonzero face vector `z` satisfies (14) exactly when
   `O z=r tensor s` for nonzero `r in K^2`, `s in K^3`.  Thus, after
   allowing the active-root bases and a nonzero target scaling to vary, it
   is exactly one compatible GHZ colour slice.

3. Projectively the solutions are `O^(-1) Seg(P^1 x P^2)`.  They have
   dimension three, codimension two, and degree three in `P^5`; their ideal
   is generated by the three quadrics (14).

### Proof

Equation (12) has rank one after reshaping, so all minors (13) vanish.  A
nonzero `2 x 3` matrix has all two-by-two minors zero exactly when it has rank
one, hence factors as `r s^T`.  Invertibility of `O` transports this rank-one
cone without changing its projective dimension, codimension, degree, or
ideal.  The rank-one matrix locus is the Segre embedding (2), whose defining
ideal in this format is precisely the three minors (13).

For fixed physical root bases, (12) is sharper than (14): `O z^(c)` must lie
on the particular line spanned by `r_c tensor s_c`.  Theorem 1 records the
basis-free obstruction before that final line incidence is imposed.

### Theorem 2 (no fan-chart coordinate boundary)

For every `O in GL_6(K)`, the affine cone

```text
O^(-1){r tensor s:r in K^2, s in K^3}                (15)
```

meets `(K^*)^6`.  Moreover, three points can be chosen in that intersection
with factorizations `r_c tensor s_c` such that

```text
rank[r_0 r_1 r_2]=2,             det[s_0 s_1 s_2]!=0. (16)
```

Consequently an invertible clean fan plus GHZ rank-one output never forces
any of the six deck-face coordinates to vanish.

### Proof

For each output coordinate `i`, the function

```text
f_i(r,s)=e_i^T O^(-1) vec(r s^T)                     (17)
```

is a nonzero bilinear polynomial: the `i`th row of `O^(-1)` is nonzero.
Because the polynomial ring over `K` is an integral domain, the product of
the six `f_i` is nonzero.  Its nonvanishing locus is therefore a nonempty
Zariski-open subset of `K^2 x K^3`, and every point in it maps to the
six-coordinate torus.

For triples of factor pairs, this torus condition, the left rank-two
condition, and the right determinant condition are all nonempty Zariski-open
conditions in the irreducible affine parameter space.  Their intersection
is nonempty over an infinite characteristic-zero field.  This proves (16).

The theorem is stronger than one favourable example: coordinate-boundary
forcing fails on **every** invertible `2 x 3` fan chart.

## 3. A symbolic all-nonzero permanental fan

For indeterminates `t_0,...,t_3`, use (3) and let `K(t)` have columns (8).
Use the row order

```text
a_0 b_0, a_0 b_1, a_0 b_2, a_1 b_0, a_1 b_1, a_1 b_2. (18)
```

### Theorem 3 (Vandermonde-square fan determinant)

The exact determinant is (4).

### Proof

Each row of `K(t)` is homogeneous of degree respectively

```text
0,2,3,1,3,4,                                            (19)
```

so the determinant is homogeneous of degree thirteen.  Permuting two
parameters permutes the six pair columns by two transpositions, hence leaves
the determinant unchanged; it is symmetric in the four parameters.

If `t_i=t_j`, then for each of the other two vertices `k`, the columns `ik`
and `jk` coincide.  Subtracting those two column pairs before specializing
shows divisibility by `(t_i-t_j)^2`.  Therefore the determinant is divisible
by the degree-twelve symmetric polynomial

```text
Delta(t)^2=product_(i<j)(t_i-t_j)^2.                  (20)
```

The quotient is a symmetric homogeneous polynomial of degree one, hence a
constant multiple of `t_0+t_1+t_2+t_3`.  At `(1,2,3,4)`, direct integer
elimination gives determinant `-2880`, while `Delta^2 sum t_i=1440`.
The constant is `-2`, proving (4).

This gives an open family of full-rank fans.  If every `t_i` is nonzero,
then every coordinate displayed in (3) is nonzero as well.

## 4. An exact three-colour torus permission certificate

At `(t_0,t_1,t_2,t_3)=(1,2,3,4)`, the fan in pair order (7) is

```text
K=
[ 2   2   2   2   2   2]
[ 5  10  17  13  20  25]
[ 9  28  65  35  72  91]
[ 3   4   5   5   6   7]
[ 6  12  20  30  48  84]
[10  30  68  78 160 300],             det K=-2880.   (21)
```

Choose factor columns

```text
r_0=(1,1),       r_1=(1,1),       r_2=(1,2),
s_0=(1,1,1),     s_1=(1,2,3),     s_2=(1,4,9).       (22)
```

The left factor matrix has rank two and the determinant of the right factor
matrix is two.  In the row order (7), take the three face columns

```text
             colour 0   colour 1   colour 2
01              14          10           2
02             -24         -33          38
03              20          36         -45
12              15          30         -30
13             -29         -58          73
23               9          18         -23.           (23)
```

Every entry is nonzero, and direct multiplication gives

```text
K z^(0)=10 vec(r_0 s_0^T),
K z^(1)= 6 vec(r_1 s_1^T),
K z^(2)=30 vec(r_2 s_2^T).                            (24)
```

The shore can simultaneously be legal and nonzero.  At each of the first
two roots take the common root vector `x=(1,1,1)` and use the root--root
bilinear matrix

```text
L=[-1  1  0]
  [ 0  0  0]
  [ 0  0  0].                                        (25)
```

The reverse orientation uses `L^T`, so this is a legal symmetric graph edge
block between two distinct local spaces.

Then

```text
L(x,x)=0,
L((1,1,1),(1,2,3))=1.                                (26)
```

Thus the original root pair remains zero-coupled while a fully supported
polarization selects `alpha=1`.  Use target diagonal coefficients
`(10,3,10)`.  Contracting the first two target modes by `(1,1,1)` and
`(1,2,3)` produces the weights `(10,6,30)` in (24).

At the two active roots use polarization bases with row matrices

```text
R=[1 1 1]                 S=[1 1 1]
  [1 1 2],                  [1 2 4]
                             [1 3 9].                 (27)
```

Their target coordinate restrictions are exactly the factor columns (22).
The first matrix has rank two and `det S=2`.  Defining the four
root--residual covectors by their values `(1,t_i)` and `(1,t_i^2,t_i^3)` in
these bases realizes (21) with every incidence coordinate nonzero.

Equations (21)--(27) are therefore a legal local root-space and target-slice
certificate: a zero-coupled but nonzero root--root block, an invertible
`2 x 3` fan chart, a three-nonzero-colour GHZ slice with active ranks two and
three, and a full-coordinate-torus deck table coexist exactly.

The table (23) is an abstract diagonal principal-response ledger.  This note
does **not** assert that one physical nonroot graph realizes all eighteen
entries while also supplying the required depth-four labels and nuisance
subtractions.  That physical integrability intersection is the remaining
problem.

## 5. Translation to existing mathematics

The columns (8) are the mixed order-two permanental compound, or symmetric
square-free/zeon compound, of the two labelled incidence maps.  This is the
commuting counterpart of an exterior compound; permanent/zeon compounds are
developed by Feinsilver and McSorley in
[*Zeons, Permanents, the Johnson Scheme, and Generalized Derangements*](https://arxiv.org/abs/1710.00788).

The GHZ equation changes the relevant geometry from the whole six-dimensional
face space to the decomposable-tensor locus.  The fact that the Segre ideal
is generated by two-by-two minors is standard; see for example
[*Ideals of varieties parameterized by certain symmetric tensors*](https://arxiv.org/abs/0705.1942).
The problem-specific content here is the exact selector equation (12), its
pullback through the permanental fan, the universal torus-permission theorem,
and the determinant (4).

## 6. Exact remaining intersection

The clean P6 branch is reduced to the simultaneous incidence

```text
physical principal-deck variety
  intersect O^(-1)(three fixed rank-one target lines)
  intersect depth-four companion compatibility
  intersect synchronized nuisance-separation locus.                 (28)
```

Theorem 1 supplies three quadratic equations per colour before the fixed
target lines are imposed.  Theorem 2 proves that these quadrics alone cannot
give a coordinate-boundary obstruction.  Theorem 3 proves that the fan
determinant can remain open with every displayed incidence nonzero.  Any
future P6 no-go must therefore use physical hafnian integrability or
cross-depth synchronization, not merely diagonal tensor rank or port
nonvanishing.

## Scope wall

```text
clean selected P6 equation alpha O z=mu(r tensor s):   PROVED;
target-clean invertible fan forces each deck diagonal: PROVED;
GHZ implies three pulled-back 2x2-minor quadrics:      PROVED;
projective clean-face locus on an invertible chart:    Seg(P1 x P2);
codimension / degree:                                  TWO / THREE;
every invertible fan's Segre pullback meets (K*)^6:    PROVED;
three torus points with active ranks 2 and 3:           PROVED;
all-nonzero Vandermonde fan determinant:                PROVED;
nonzero shore with zero original root evaluation:      CONSTRUCTED;
exact three-colour full-torus target slice:             CONSTRUCTED;
GHZ diagonality forces root--root shore zero:           FALSE AT TARGET SLICE;
GHZ diagonality forces fan singularity:                 FALSE;
coordinate boundary forced on an invertible fan:       FALSE;
table (23) realized by one physical hafnian graph:      UNKNOWN;
depth-two and depth-four sectors synchronized:          UNKNOWN;
nuisance columns legally separated in a full witness:  UNKNOWN;
unrestricted P6 obstruction or construction:            UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.      (29)
```

## Replay

```powershell
uv run --with sympy python claims/p6/verify_p6_clean_two_by_three_selector_segre_pullback_and_torus_permission.py
python claims/p6/audit_p6_clean_two_by_three_selector_segre_pullback_and_torus_permission.py
python -m py_compile claims/p6/verify_p6_clean_two_by_three_selector_segre_pullback_and_torus_permission.py claims/p6/audit_p6_clean_two_by_three_selector_segre_pullback_and_torus_permission.py
uv run --with ruff ruff check claims/p6/verify_p6_clean_two_by_three_selector_segre_pullback_and_torus_permission.py claims/p6/audit_p6_clean_two_by_three_selector_segre_pullback_and_torus_permission.py
```

The primary replay proves the symbolic determinant factorization, constructs
the fixed fan, checks all three rank-one target equations and pulled-back
quadrics, and verifies the root-space shore certificate.  The independent
no-import audit uses a separate sparse multivariate polynomial determinant,
integer matrix arithmetic, and direct bilinear evaluation.  Neither replay
searches any graph, support, word, parameter family, or finite field.

## Dependencies

- [`RESPONSE_JETS_AS_PRINCIPAL_DELETION_DECKS_AND_ROOT_PARITY_LEGALITY_THEOREM.md`](../arbitrary-order/RESPONSE_JETS_AS_PRINCIPAL_DELETION_DECKS_AND_ROOT_PARITY_LEGALITY_THEOREM.md)
- [`P6_FOUR_ROOT_FULL_H4_SENSOR_AND_TARGET_INCIDENCE_BOUNDARY.md`](P6_FOUR_ROOT_FULL_H4_SENSOR_AND_TARGET_INCIDENCE_BOUNDARY.md)
- [`NONPROJECTIVE_ROOT_PAIR_FAN_SELECTOR_TOMOGRAPHY_THEOREM.md`](../arbitrary-order/NONPROJECTIVE_ROOT_PAIR_FAN_SELECTOR_TOMOGRAPHY_THEOREM.md)
