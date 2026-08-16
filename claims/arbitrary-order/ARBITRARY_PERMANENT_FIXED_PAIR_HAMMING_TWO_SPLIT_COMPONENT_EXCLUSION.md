# Arbitrary permanent fixed-pair Hamming-two split-component exclusion

## Status

This note proves two exact characteristic-zero exclusions inside the
low-projection residual of
`ARBITRARY_PERMANENT_FIXED_PAIR_DIMENSION_FIVE_FULL_PROJECTION_BOUNDARY.md`.
Both use the same fixed five-dimensional two-mode product space.

1. In the **common-plane split component**, modes `2,3,4` have one common
   plane `H=span{x_4,x_5,h}`, their bases may vary arbitrarily by
   `GL_3`, and mode `5` dualizes the three diagonal pair products.  The
   exact Hamming-two shell alone, together with the nonzero pure
   coefficients, excludes this entire component.
2. In a natural **three-parameter affine deformation**, the three planes
   are

   ```text
   H_t=span{x_4,x_5,h(s_t)},
   h(s)=x_1+s x_2+(1+s)x_3,        t=2,3,4,              (1)
   ```

   while mode `5` is the three-plane

   ```text
   Z=ker(-x_0+x_1-x_2+x_3) subset span{x_0,x_1,x_2,x_3}. (2)
   ```

   Arbitrary ordered bases are allowed in all four planes.  The accumulated
   Hamming-one and Hamming-two equations, together with the nonzero
   colour-two pure coefficient, exclude this family.

The second family contains the previous exact Hamming-one sharpness fixture
at `s_2=s_3=s_4=-2`.  Thus the first nonzero Hamming-two shell in that
fixture is an actual detector: it is not removable by arbitrary basis
changes in the common plane while retaining the pure equations, nor by the
affine plane deformations (1) while retaining the nonzero colour-two pure
coefficient and all Hamming-one zeros.

These results do **not** classify all simultaneous zero tensors of the two
mixed-radical quartics.  In particular, cancellation-based low-projection
components outside the two families remain open.  This note does not prove
unrestricted `P_6 -> Delta_3`; arbitrary-order permanent nonrestriction
remains unknown, and the global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Fixed pair and five complementary quartics

Let `K` be a field of characteristic zero and

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).                       (3)
```

At modes `0,1`, use

```text
u_0=x_0-x_3,      u_1=x_1-x_3,      u_2=x_2-x_3,
v_0=x_1+x_2,      v_1=x_0+x_2,      v_2=x_2-x_3.            (4)
```

In edge order `(01,02,03,12,13,23)`, the mixed product space and three
diagonal products have the basis

```text
m_1=(0,1,-1,0,0,-1),          m_2=(0,0,0,1,-1,-1),
d_0=(1,1,0,0,-1,-1),          d_1=(1,0,-1,1,0,-1),
d_2=(0,0,0,0,0,-2).                                      (5)
```

Put

```text
ell_1=x_3-x_2-x_0,                 ell_2=x_3-x_2-x_1.     (6)
```

Complementing the six-variable edges gives the five factorized quartics

```text
star(m_1)= x_4x_5 x_1 ell_1,
star(m_2)= x_4x_5 x_0 ell_2,

star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.                              (7)
```

For a complementary four-word `w=(c_2,c_3,c_4,c_5)`, write

```text
T_q(w)=[x_0x_1x_2x_3x_4x_5]
       q y_(2,c_2)y_(3,c_3)y_(4,c_4)y_(5,c_5).          (8)
```

An actual extension to `Delta_3` would have `T_(m_1)=T_(m_2)=0`
identically and

```text
T_(d_c)(c,c,c,c)=lambda_c != 0.                         (9)
```

The two theorems below need only the explicitly named portions of the mixed
target equations.

## 2. Hamming-shell conventions

The diagonal pair product `d_c` fixes the first two colours to `(c,c)`.
Thus a complementary word `w` contributes to the Hamming-`j` shell around
the full constant word `c^6` precisely when

```text
distance(w,c^4)=j.                                      (10)
```

The **exact Hamming-two equations** used in Theorem 1 are

```text
T_(d_c)(w)=0 whenever distance(w,c^4)=2.                 (11)
```

The **accumulated radius-two equations** used in Theorem 2 are (11) plus
the corresponding equations at distance one.  Neither phrase includes the
unproved claim that the equations outside the named family have been
classified.

## 3. Common-plane split factorization

Fix a nonzero `h in span{x_0,x_1,x_2,x_3}` and put

```text
H=span{x_4,x_5,h}.                                      (12)
```

Suppose modes `2,3,4` all have plane `H`, with arbitrary ordered bases.
Let `z_0,z_1,z_2` be an ordered basis of a first-four-coordinate plane at
mode `5`.  Assume that this basis dualizes the fixed pair in the following
exact sense:

```text
[x_0...x_5] m_j x_4x_5 h z_e=0,             j=1,2,
[x_0...x_5] d_c x_4x_5 h z_e=mu_c delta_(c,e),
                                                mu_c != 0.    (13)
```

For the three modes in `H`, record coordinates in the ordered basis
`(x_4,x_5,h)`.  If their colour-coordinate matrices are `A_2,A_3,A_4`,
then each `A_t` is invertible.  Define

```text
R(i,j,k)=P_3(A_2 e_i,A_3 e_j,A_4 e_k).                  (14)
```

Every full monomial contribution must select `x_4,x_5,h` once from modes
`2,3,4`.  Therefore (13) gives the exact tensor factorization

```text
T_(d_c)(i,j,k,e)=mu_c delta_(c,e) R(i,j,k),
T_(m_j)=0.                                               (15)
```

The tensor `R` is a `GL_3^3` translate of the three-mode permanent tensor
`P_3`.

### Theorem 1 (the exact Hamming-two shell excludes the common plane)

Under (12)--(15), the three nonzero pure equations (9) and the exact
Hamming-two equations (11) are inconsistent.

### Proof

Let `w=(i,j,k)` be any nonconstant ternary triple.  Its colour-multiplicity
type is either `2+1` or `1+1+1`, so some colour `e` occurs exactly once in
`w`.  The full word

```text
(e,e,i,j,k,e)                                           (16)
```

differs from `e^6` in exactly the other two middle positions.  It is an
exact Hamming-two word.  Equations (11) and (15), with `mu_e!=0`, force

```text
R(i,j,k)=0.                                              (17)
```

Thus every nonconstant coefficient of `R` vanishes.  The three pure
equations make all three diagonal coefficients nonzero, so `R` is a
concise diagonal tensor.

This is impossible for a `GL_3^3` translate of `P_3`.  In the standard
first-mode slicing, the slice space of `P_3` consists of

```text
          [ 0   a_2 a_1]
A(a)=     [a_2   0  a_0].                               (18)
          [a_1  a_0  0 ]
```

The three principal `2`-by-`2` minors are

```text
-a_2^2,       -a_1^2,       -a_0^2.                     (19)
```

Hence the slice space contains no nonzero matrix of rank at most one over
any field.  In contrast, each nonzero coordinate slice of a diagonal
tensor has rank one.  Changes of bases mix the slices invertibly and
multiply every slice on the left and right by invertible matrices, so they
preserve whether the slice space contains a nonzero rank-one matrix.  This
contradiction proves the theorem.

Notice that Hamming-one vanishing was not used.

## 4. A radical-preserving affine deformation

For `s in K`, define

```text
h(s)=(0,1,s,1+s,0,0)=x_1+s x_2+(1+s)x_3.               (20)
```

For arbitrary `s_2,s_3,s_4 in K`, use the planes

```text
H_t=span{x_4,x_5,h(s_t)},                 t=2,3,4,      (21)
```

and use `Z` from (2) at mode `5`.  Every plane in (21), and `Z`, has
dimension three.  Bases inside these planes remain completely arbitrary.

Let `z=(z_0,z_1,z_2,z_3,0,0) in Z`.  Direct evaluation of the factor pairs
in (7) gives

```text
<m_1,x_4x_5h(s)z> = -z_0+z_1-z_2+z_3 = 0,
<m_2,x_4x_5h(s)z> = 0,

<d_0,x_4x_5h(s)z> =  2(1+s)z_2,
<d_1,x_4x_5h(s)z> =  2s z_3,
<d_2,x_4x_5h(s)z> = -2z_0.                              (22)
```

Here `<q,f>` means `[x_0...x_5]qf`.  The first two identities show that
both mixed-radical tensors vanish identically for all four local bases:
every nonzero full-monomial term chooses `x_4,x_5`, one `h(s_t)`, and one
`z in Z`.

For each mode `t=2,3,4`, use `(x_4,x_5,h(s_t))` as a reference basis.
Let

```text
R(i,j,k)=P_3(A_2e_i,A_3e_j,A_4e_k),                    (23)
```

where the invertible `A_t` record the arbitrary colour bases.  The last
identity in (22) is independent of both `s` and the mode supplying `h(s)`.
Consequently the complete `d_2` component factors as

```text
T_(d_2)(i,j,k,e)=-2 x_0(z_e) R(i,j,k).                  (24)
```

Again, `R` is a `GL_3^3` translate of `P_3`.

### Theorem 2 (radius two excludes the affine deformation)

Under (20)--(24), a nonzero colour-two pure coefficient and the accumulated
Hamming-one and Hamming-two equations are inconsistent.

### Proof

The pure word gives

```text
-2x_0(z_2)R(2,2,2) != 0.                               (25)
```

Fix the first middle colour to `2` and the mode-five colour to `2`.  For
every `(j,k)!=(2,2)`, the word

```text
(2,2,2,j,k,2)                                          (26)
```

has Hamming distance one or two from `2^6`.  Equations (24)--(26) therefore
give

```text
R(2,j,k)=0                  whenever (j,k)!=(2,2).      (27)
```

The colour-`2` slice of `R` is consequently a nonzero matrix with only its
`(2,2)` entry present.  It has rank one.  This contradicts the rank-one-free
slice-space invariant (18)--(19) for a `GL_3^3` translate of `P_3`.

Both distance-one and distance-two equations occur in (27), so unlike
Theorem 1 this proof genuinely uses the accumulated radius-two condition.

## 5. The previous sharp fixture lies in both families

Set

```text
s_2=s_3=s_4=-2,
h=h(-2)=x_1-2x_2-x_3.                                  (28)
```

At modes `2,3,4`, use the colour bases

```text
(x_4,x_5,h),       (x_5,h,x_4),       (h,x_4,x_5).     (29)
```

At mode `5`, use

```text
b_0=2x_1+2x_2,
b_1=2x_1-2x_3,
b_2=x_0+x_1.                                           (30)
```

The three vectors in (30) are independent and satisfy the equation of
`Z`.  Substitution into (22) at `s=-2` gives

```text
(<d_c,x_4x_5hb_e>)_(c,e)=diag(-4,8,-2),                (31)
```

while both mixed rows vanish.  Thus (28)--(30) are exactly the earlier
Hamming-one sharpness model.  In the common-plane description, (31) is the
dualization (13); in the affine description, it is the equal-parameter
point of (20)--(24).

The fixture has projection-rank profiles `(3,3,3,1)` and `(2,2,2,2)` and
all ambient local planes have rank three.  It satisfies every Hamming-one
equation but has nine nonzero Hamming-two coefficients.  Theorem 1 shows
that those coefficients cannot all be removed in the common-plane family
while retaining the pure equations.  Theorem 2 gives the analogous statement
for the affine family while retaining the nonzero colour-two pure coefficient
and the Hamming-one equations.

## 6. Exact scope and replay

The proved and open boundaries are

```text
common-H split component under pure + exact H2:        EXCLUDED;
affine h(s_t),Z component under pure + H1 + H2:        EXCLUDED;
arbitrary bases and arbitrary parameters in families: INCLUDED;
all cancellation-based low-projection components:      NOT CLASSIFIED;
general fixed-pair radius-two residual:                 OPEN;
unrestricted P_6 -> Delta_3:                           UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.       (32)
```

Replay the exact checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_hamming_two_split_component_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_hamming_two_split_component_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_hamming_two_split_component_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_hamming_two_split_component_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_hamming_two_split_component_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_hamming_two_split_component_exclusion.py
```

The primary verifier checks all five factorized quartics, symbolically
derives (22), expands both split tensors on coordinate bases, checks the
Hamming-shell combinatorics and slice minors, and reconstructs the sharp
fixture.  The independent no-import audit uses separate sparse arithmetic,
an exhaustive `F_5` audit of the affine identities and the rank-one-free
slice space, and a direct fixture replay.  These finite checks replay exact
identities and conventions.  The written arguments prove the quantified
characteristic-zero statements.
