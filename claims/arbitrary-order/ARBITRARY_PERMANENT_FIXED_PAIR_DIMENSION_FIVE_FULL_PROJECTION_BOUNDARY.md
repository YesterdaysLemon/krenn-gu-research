# Arbitrary permanent fixed pair-dimension-five full-projection boundary

## Status

This note proves an exact characteristic-zero obstruction for one fixed
two-mode pair on the `P_6 -> Delta_3` permanent-restriction boundary.  The
pair product space has dimension exactly five, so it realizes the lower
bound from
`ARBITRARY_PERMANENT_COTWO_PRODUCT_SENSOR_CORANK_TWO_STRENGTHENING_THEOREM.md`
at the level of the two-mode algebra.

The theorem is deliberately local and pointwise.  If modes `0,1` of a
putative restriction are exactly the pair displayed below, then the four
complementary local planes cannot all have rank three under both of two
explicit four-factor projections.  Equivalently, every extension of this
fixed pair to `Delta_3` must satisfy

```text
min { rank Phi_k|L_t : k in {1,2}, t in {2,3,4,5} } <= 2.       (1)
```

The note does **not** classify all five-dimensional pair product spaces,
does not prove that an arbitrary such pair can be normalized to this one,
and does not exclude the residual rank-at-most-two locus.  Hence it does
not prove unrestricted `P_6 -> Delta_3` nonrestriction.  Arbitrary-order
permanent nonrestriction remains unknown, and the global Krenn--Gu
conjecture remains **UNRESOLVED**.

The final section gives an exact six-mode model with the same fixed pair,
rank-three ambient local maps, all pair-mixed coefficients zero, nonzero
pure coefficients, and all 36 Hamming-one mixed coefficients zero.  Fifteen
Hamming-two or Hamming-three coefficients survive.  The model explicitly
omits the full projected-rank hypotheses: its two projection-rank profiles
are `(3,3,3,1)` and `(2,2,2,2)`.  It shows only that pair-mixed zeros, pure
nonvanishing, Hamming-one zeros, and ambient local rank three do not exclude
the low-projection residual.  It is not a restriction to `Delta_3`.

## 1. Fixed pair and its five-dimensional product space

Let `K` be any field of characteristic zero and put

```text
Z_6 = K[x_0,...,x_5]/(x_0^2,...,x_5^2).                       (2)
```

At modes `0` and `1`, fix the independent triples

```text
u_0 = x_0-x_3,       u_1 = x_1-x_3,       u_2 = x_2-x_3,
v_0 = x_1+x_2,       v_1 = x_0+x_2,       v_2 = x_2-x_3.       (3)
```

Use the degree-two edge order

```text
(01,02,03,12,13,23).                                         (4)
```

Writing `p_ij=u_i v_j`, the nine products are

```text
d_0=p_00 = (1,1, 0,0,-1,-1),
d_1=p_11 = (1,0,-1,1, 0,-1),
d_2=p_22 = (0,0, 0,0, 0,-2),

m_1=p_01=p_02=p_21 = (0,1,-1,0, 0,-1),
m_2=p_10=p_12=p_20 = (0,0, 0,1,-1,-1).                       (5)
```

Thus, for

```text
B = span{p_ij : 0<=i,j<=2},       M = span{m_1,m_2},          (6)
```

one has the direct sum

```text
B = M direct-sum span{d_0,d_1,d_2},
dim B=5,                         dim M=2.                      (7)
```

In the edge coordinates (4), the unique ordinary coefficient relation on
`B` is

```text
q_02+q_03+q_12+q_13=0.                                    (8)
```

The relation vector `(0,1,1,1,1,0)` is fixed by edge complementation in
four variables, so it also represents the complement-pairing annihilator
of `B` inside the six-dimensional stripped four-variable quadratic space.

If this pair occurs in a restriction to `Delta_3`, every mixed pair word
has target coefficient zero against every complementary word.  Therefore
`M` lies in the left radical of the `B`-by-complementary-sensor pairing.
That pairing has target rank three, and (7) then makes `M` the entire
two-dimensional left radical.  This last radical statement is conditional
on an actual `Delta_3` extension; equations (3)--(8) themselves are
unconditional identities in `Z_6`.

## 2. The two mixed-radical quartics

For a quadratic `q` supported on `x_0,...,x_3`, let its complementary
quartic be

```text
star(q) = sum_(0<=i<j<=3) q_ij product_(s notin {i,j}) x_s.    (9)
```

Direct complementation of (5) gives

```text
F_1 = star(m_1) = x_1 x_4 x_5 (x_3-x_2-x_0),
F_2 = star(m_2) = x_0 x_4 x_5 (x_3-x_2-x_1).                 (10)
```

Put

```text
ell_1=x_3-x_2-x_0,                 ell_2=x_3-x_2-x_1,
Phi_1=(x_1,x_4,x_5,ell_1),         Phi_2=(x_0,x_4,x_5,ell_2), (11)
```

where `Phi_k:K^6 -> K^4` is the linear map whose coordinates are the four
listed covectors.

Let `L_2,...,L_5` be the rank-three local image planes of four proposed
complementary modes.  For `y_t in L_t`, direct expansion of (10) gives

```text
[x_0...x_5] m_k y_2 y_3 y_4 y_5
  = per( phi_(k,s)(y_t) )_(0<=s<=3, 2<=t<=5).                 (12)
```

Thus the mixed `Delta_3` equations for either nonzero radical vector say
that the pullback of the four-variable permanent under the four maps
`Phi_k|L_t` is the zero four-linear tensor.

## 3. A hyperplane-product lemma

Let `E=K^4` with its fixed coordinate basis, and let

```text
Z(E)=K[z_0,z_1,z_2,z_3]/(z_0^2,z_1^2,z_2^2,z_3^2).
```

For a nonzero covector `alpha`, write `H_alpha=ker(alpha)`, and let
`H_alpha H_beta` denote the span in `Z(E)_2` of all products `uv` with
`u in H_alpha` and `v in H_beta`.

### Lemma 1 (hyperplane products)

Over every field of characteristic different from two,

```text
dim(H_alpha H_beta) >= 3.                                      (13)
```

Equality holds if and only if `alpha,beta` are proportional to the same
coordinate covector.  In that case `H_alpha=H_beta` is the corresponding
coordinate three-space.

### Proof

Identify the dual of `Z(E)_2` with the six-dimensional space of symmetric
zero-diagonal `4`-by-`4` matrices.  A matrix `C` annihilates
`H_alpha H_beta` precisely when its symmetric bilinear form vanishes on
`H_alpha x H_beta`.

First suppose `alpha,beta` are independent and put
`H_0=H_alpha intersect H_beta`.  If `x in H_0`, symmetry and the two
vanishing conditions give

```text
Cx in K alpha intersect K beta = 0.                            (14)
```

Hence `C` kills `H_0` and descends to a symmetric form on the
two-dimensional quotient `E/H_0`.  That space of symmetric forms has
dimension three, so the annihilator of `H_alpha H_beta` has dimension at
most three.  Equality cannot occur: if all three quotient symmetric forms
pulled back with zero diagonal, then every coordinate class `e_i mod H_0`
would have zero square under every symmetric form.  A nonzero vector in a
two-dimensional space has nonzero square under the rank-one symmetric form
`lambda^2` for a suitable `lambda`, so all four `e_i` would lie in the
two-dimensional `H_0`, an impossibility.  The annihilator therefore has
dimension at most two, and

```text
dim(H_alpha H_beta) >= 4                                      (15)
```

in the independent case.

Now suppose `beta` is proportional to `alpha`.  Every symmetric form
vanishing on `H_alpha x H_alpha` is uniquely

```text
C=alpha tensor z + z tensor alpha,              z in E^*.     (16)
```

The zero-diagonal conditions are `2 alpha_i z_i=0`.  If `s` is the number
of nonzero coordinate entries of `alpha`, the annihilator has dimension
`4-s`, and hence

```text
dim(H_alpha H_alpha)=6-(4-s)=2+s.                              (17)
```

This is at least three, with equality exactly when `s=1`, namely when
`alpha` is a coordinate covector.  The two cases prove the lemma.

### Corollary 2 (zero four-mode permanent)

Let `H_0,H_1,H_2,H_3` be hyperplanes in `K^4`.  If

```text
[z_0z_1z_2z_3] h_0h_1h_2h_3=0
for every h_i in H_i,                                         (18)
```

then all four hyperplanes are one and the same coordinate hyperplane.

Indeed, group the factors as `(H_0H_1)(H_2H_3)`.  The two quadratic
product spaces are orthogonal under the perfect edge-complement pairing.
Lemma 1 gives dimension at least three for each, so both have dimension
three.  Equality in the lemma makes `H_0=H_1=W_i` and
`H_2=H_3=W_j` for coordinate hyperplanes.  The product space `W_i^2` is
its own orthogonal under edge complementation.  Hence `W_j^2=W_i^2`, and
therefore `j=i`.

## 4. The full-projection obstruction

### Theorem 3

Let `K` have characteristic zero.  Suppose four independent local triples
span planes `L_2,...,L_5 subset K^6`, and suppose that together with the
fixed modes (3) they pull `P_6` back to a diagonal tensor with three nonzero
constant coefficients and every nonconstant coefficient zero.  Then (1)
holds.

### Proof

Assume instead that all eight ranks in (1) equal three.  For fixed `k`, the
four images `Phi_k(L_t)` are hyperplanes in `K^4`.  Equation (12), the mixed
target zeros, and Corollary 2 give one common missing coordinate factor at
all four modes.  Thus there are

```text
phi in {x_1,x_4,x_5,ell_1},       psi in {x_0,x_4,x_5,ell_2}  (19)
```

such that

```text
L_t subset K_(phi,psi):=ker(phi) intersect ker(psi)
for every t=2,3,4,5.                                      (20)
```

Let

```text
C_(phi,psi)=span{y_2y_3y_4y_5 : y_t in K_(phi,psi)}
             subset (Z_6)_4,                                  (21)
```

and let

```text
rho_(phi,psi):C_(phi,psi) -> B^*,
rho(f)(q)=[x_0...x_5]qf.                                     (22)
```

Section 5 proves in all 16 cases that

```text
rank rho_(phi,psi) <= 2.                                     (23)
```

On the other hand, if `a_c` is the product of the four complementary local
forms of constant colour `c`, the target equations say

```text
rho(a_c)(d_e)=lambda_c delta_(c,e),       lambda_c != 0.       (24)
```

The three functionals `rho(a_0),rho(a_1),rho(a_2)` are therefore
independent, so the actual complementary sensor has pairing rank at least
three.  It is contained in `C_(phi,psi)`, contradicting (23).  This proves
the theorem.

## 5. Exact 16-cell rank table

Order the basis of `B` as

```text
(m_1,m_2,d_0,d_1,d_2).                                      (25)
```

The exact ranks of (22) are

```text
                     psi
              x_0   x_4   x_5   ell_2
phi  x_1       1     0     0      2
     x_4       0     0     0      0
     x_5       0     0     0      0
     ell_1     2     0     0      2.                         (26)
```

If either missing factor is `x_4` or `x_5`, every element of
`C_(phi,psi)` lacks that variable.  Since every `q in B` uses only
`x_0,...,x_3`, the full square-free monomial can never occur.  This proves
the twelve zero cells.

For the remaining four cells, write

```text
K_(phi,psi)=K_0 direct-sum span{x_4,x_5},
K_0 subset span{x_0,x_1,x_2,x_3}.                            (27)
```

The part of (21) detected by `rho`, after extracting its `x_4x_5`
coefficient, is exactly the quadratic product space `K_0K_0`.  In the edge
order (4), bases for those product spaces and their pairing matrices against
(25) are

```text
(phi,psi)=(x_1,x_0):
  K_0K_0 basis:  x_2x_3
  matrix:         [0 0  1  1  0]                              rank 1

(phi,psi)=(x_1,ell_2):
  K_0K_0 basis:  x_0x_2+x_0x_3,  x_2x_3
  matrix:         [0 0 -1  1  0]
                  [0 0  1  1  0]                              rank 2

(phi,psi)=(ell_1,x_0):
  K_0K_0 basis:  x_1x_2+x_1x_3,  x_2x_3
  matrix:         [0 0  1 -1  0]
                  [0 0  1  1  0]                              rank 2

(phi,psi)=(ell_1,ell_2):
  K_0K_0 basis:  x_0x_1+x_0x_3+x_1x_3,
                  x_0x_2+x_0x_3+x_1x_2+x_1x_3+x_2x_3,
                  x_2x_3
  matrix:         [0 0  0  0 -2]
                  [0 0  1  1  0]
                  [0 0  1  1  0]                              rank 2. (28)
```

For example, in the last cell

```text
K_0=span{x_0+x_1+x_3, x_2+x_3};                              (29)
```

the three displayed quadratics are one half of the first square, the
mixed product, and one half of the second square.  Characteristic zero
justifies these divisions and the displayed ranks.  Equations (26)--(29)
prove (23) without a genericity assumption.

## 6. Exact Hamming-one sharpness model

Keep the fixed pair (3), and set

```text
a=x_4,              b=x_5,              h=x_1-2x_2-x_3,
b_0=2x_1+2x_2,      b_1=2x_1-2x_3,      b_2=x_0+x_1.          (30)
```

Give modes `2,3,4,5` the ordered colour frames

```text
L_2: (a,b,h),
L_3: (b,h,a),
L_4: (h,a,b),
L_5: (b_0,b_1,b_2).                                         (31)
```

Every frame has rank three.  With rows ordered as in (11) and columns by
colours `0,1,2`, the exact projected matrices are

```text
             Phi_1 matrix                         Phi_2 matrix

L_2:  [0 0 1] [1 0 0] [0 1 0] [0 0 1]      [0 0 0] [1 0 0] [0 1 0] [0 0 0]
       rank 3                                  rank 2

L_3:  [0 1 0] [0 0 1] [1 0 0] [0 1 0]      [0 0 0] [0 0 1] [1 0 0] [0 0 0]
       rank 3                                  rank 2

L_4:  [1 0 0] [0 1 0] [0 0 1] [1 0 0]      [0 0 0] [0 1 0] [0 0 1] [0 0 0]
       rank 3                                  rank 2

L_5:  [2 2 1] [0 0 0] [0 0 0] [-2 -2 -1]   [0 0 1] [0 0 0] [0 0 0] [-4 -4 -1]
       rank 1                                  rank 2.                         (32)
```

Each bracket in (32) is one row, so each displayed projection is a
`4`-by-`3` matrix.  The model lies on the low-projection residual required
by Theorem 3 and does not lie in the all-eight-ranks-three case excluded in
that theorem's proof.

For a colour word `c=(c_0,...,c_5)`, let `T_c` be the coefficient of
`x_0...x_5` in the product of its six selected forms.  Put

```text
P={000,012,111,120,201,222},
(lambda_0,lambda_1,lambda_2)=(-4,8,-2).                       (33)
```

The six-support tensor on modes `2,3,4` is a colour-permuted copy of
`P_3`: applying `(i,j,k) -> (i,j-1,k+1) mod 3` to the usual permanent
support `{012,021,102,120,201,210}` gives exactly `P`.  Consequently the
complete six-mode tensor in this model factors as a weighted three-mode
diagonal tensor on modes `{0,1,5}` times that colour-permuted `P_3` on
modes `{2,3,4}`.

Then exact multiplication gives the complete coefficient rule

```text
T_c = lambda_e  if c_0=c_1=c_5=e and (c_2,c_3,c_4) in P,
T_c = 0         otherwise.                                   (34)
```

Indeed, a contribution to the full monomial requires modes `2,3,4` to
select `a,b,h` in some order; these are exactly the six triples in `P`.
The three products `h b_e` pair with `(d_0,d_1,d_2)` as the diagonal matrix
`diag(-4,8,-2)` and annihilate `M`, which proves (34).

Coefficient by coefficient, the 18 nonzero words are

```text
-4: 000000  000120  001110  001200  002010  002220
 8: 110001  110121  111111  111201  112011  112221
-2: 220002  220122  221112  221202  222012  222222.            (35)
```

All other `729-18=711` coefficients vanish.  The canonical serialization
of all 729 lines as `word:value\n` in lexicographic word order has SHA-256

```text
1360041c9a60d4451f58f18b978dfb30c86b707bb4fc7c860d7573d4686a7da8. (36)
```

Define the Hamming shell of a word by its minimum distance to the
monochromatic code `{000000,111111,222222}`.  The three constant words have
distance zero.  Among the fifteen surviving mixed words, nine have distance
two and six have distance three.  Every one of the `3*6*2=36` distinct
Hamming-one neighbours of a constant word is zero.  Thus the Hamming-one
shell is identically zero and the first nonzero mixed shell is Hamming
distance two.  Moreover, all `6*3^4=486` words with `c_0!=c_1` vanish, so
the pair-mixed equations hold.  Consequently pair-mixed zeros, pure
nonvanishing, Hamming-one zeros, and ambient local rank three do not exclude
this fixed pair on the low-projection residual.  Equation (35) also shows
exactly why the model is not `Delta_3`.

## 7. Scope and replay

The exact conclusion is only (1) for the fixed coordinate pair (3).  The
remaining obligations are explicit:

```text
classification of all dim(B_ab)=5 pair orbits:          NOT PROVIDED;
reduction of an arbitrary equality-five pair to (3):    NOT PROVIDED;
exclusion of the rank-at-most-two projection residual:  OPEN;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.       (37)
```

Replay the exact checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_dimension_five_full_projection_boundary.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_dimension_five_full_projection_boundary.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_dimension_five_full_projection_boundary.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_dimension_five_full_projection_boundary.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_dimension_five_full_projection_boundary.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_dimension_five_full_projection_boundary.py
```

The primary verifier uses exact symbolic linear algebra, independently
generates all 16 missing-factor product spaces, and computes all 729 tensor
coefficients by square-free subset multiplication.  The no-import audit
uses a custom exact row reducer, the displayed residual quadratic bases,
direct `6!` permanent enumeration, and an exhaustive projective
hyperplane-product audit over `F_5`.  These finite programs replay the
coordinate identities and stress-test conventions.  The written arguments,
not the finite audits alone, prove the characteristic-zero statements.
