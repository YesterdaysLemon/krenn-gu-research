# Arbitrary permanent triangle-pair kernel-support boundary theorem

## Status

This note proves an exact characteristic-zero localization inside the
simultaneous projection-drop residual for the displayed Delta-admissible
`(3,1)` triangle pair.  Every local restriction of either mixed-factor
projection has rank at least two.  More precisely, a rank-two kernel for
the first family lies on one of three explicit lines, while a rank-two
kernel for the second family lies on one of two explicit lines:

```text
Phi_1: K(x_1+x_2), K(x_0+x_2), K(x_0-x_1),
Phi_2: Kx_3, K(x_1+x_2).                                  (1)
```

The second localization uses a linear dependence among the three diagonal
residual covectors; its three target tensors have disjoint colour support,
so a generic kernel vector would have all local coordinates zero.  The
first localization uses the exact `R direct-sum A` contraction tensor and
the same field-linear active-colour and one-diagonal obstructions as the
fixed-pair kernel boundary.

Together with
`ARBITRARY_PERMANENT_TRIANGLE_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md`,
this proves that every putative exact extension has a rank-exactly-two mode
in each family.  It does not exclude the remaining five-line incidence
problem or prove unrestricted permanent nonrestriction.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Exact target and the two kernels

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

For the triangle pair, put

```text
ell_1=x_2-x_1-x_0,                 ell_2=x_2-x_1,
Phi_1=(x_3,x_4,x_5,ell_1),         Phi_2=(x_0,x_4,x_5,ell_2). (2)
```

The two mixed and three diagonal complementary quartics are

```text
F_1=x_4x_5 x_3 ell_1,              F_2=x_4x_5 x_0 ell_2,
D_0=2x_4x_5 x_0x_3,
D_1= x_4x_5 x_2(x_0+x_1),
D_2= x_4x_5 x_1(x_0-x_2).                              (3)
```

Let ordered independent triples `(y_(t,0),y_(t,1),y_(t,2))` span local
planes `L_t`, for `t=2,3,4,5`.  A putative exact extension satisfies

```text
T_(F_1)=T_(F_2)=0,
T_(D_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (4)
```

Direct row reduction gives

```text
ker(Phi_1)={p_1(a,b)=(a,b,a+b,0,0,0):a,b in K},
ker(Phi_2)={p_2(a,b)=(0,a,a,b,0,0):a,b in K}.            (5)
```

If `p in L_t`, write its local expansion as

```text
p=alpha_0 y_(t,0)+alpha_1 y_(t,1)+alpha_2 y_(t,2).       (6)
```

## 2. Exact single-contraction table

After removing the common factor `x_4x_5`, direct contraction gives

```text
                         F_1             F_2

p_1(a,b)                  0       a(x_0-x_1+x_2)
p_2(a,b)          b(-x_0-x_1+x_2)        0

                         D_0                 D_1

p_1(a,b)              2a x_3       (a+b)(x_0+x_1+x_2)
p_2(a,b)              2b x_0          a(x_0+x_1+x_2)

                         D_2

p_1(a,b)          b(x_0-x_1-x_2)
p_2(a,b)          a(x_0-x_1-x_2).                         (7)
```

For `p_1`, the four residual covectors in the order
`(F_2,D_0,D_1,D_2)` have determinant

```text
-8a^2 b(a+b).                                             (8)
```

For `p_2` with `ab!=0`, the diagonal residuals obey the exact relation

```text
-(a/b) i_(p_2)D_0+i_(p_2)D_1+i_(p_2)D_2=0.              (9)
```

Both identities are in the four-space with coordinates `x_0,...,x_3`;
no quotient or algebraic closure is used.

## 3. Generic `Phi_1` directions are impossible

Assume `ab(a+b)!=0` for `p=p_1(a,b) in L_t`.  Decompose the ambient space
as

```text
R direct-sum A,
R=K^{\{0,1,2,3\}},                    A=K^{\{4,5\}},
J((s_4,s_5),(t_4,t_5))=s_4t_5+s_5t_4.                  (10)
```

For three remaining vectors define the symmetric `R`-valued tensor

```text
C(y,z,w)=r(y)J(a(z),a(w))+r(z)J(a(y),a(w))
                         +r(w)J(a(y),a(z)).             (11)
```

By (8), the mixed channel and the three diagonal channels form a basis of
`R^*`.  Hence (4), after contraction with (6), determines (11) on the
three remaining local colour bases:

```text
C(y_(s,i),y_(u,j),y_(v,l))=0                 unless i=j=l,
C(y_(s,c),y_(u,c),y_(v,c))!=0       iff alpha_c!=0.       (12)
```

We recall the two elementary field-linear consequences used in the fixed
pair boundary, and include their load-bearing steps here.

First, for distinct remaining modes and distinct colours, the map

```text
w |-> C(y_(s,i),y_(u,j),w) : R direct-sum A -> R          (13)
```

kills a three-plane.  On the four-dimensional `R` summand it is the scalar
identity multiplied by `J(a(y_(s,i)),a(y_(u,j)))`.  That scalar must
therefore vanish.  The resulting cross-colour orthogonality arrays in the
two-space `A` have at most two active colours.  If two colours are active,
all `A`-columns at the third colour vanish in the three remaining modes.
The removed kernel vector has zero `A`-part, so the coefficient of the
third pure tensor cannot supply both factors `x_4,x_5`, contradicting
`lambda_c!=0`.  Thus (12) has exactly one nonzero diagonal.

Second, one nonzero diagonal is impossible.  Indeed, some same-colour pair
of `A`-columns pairs nontrivially under `J`.  For either other colour in the
third mode, (13) and (12) force its `R`-part to vanish and its `A`-part to
lie on the one-dimensional orthogonal-complement line of a fixed nonzero
`A`-vector.  The two other-colour local vectors are then dependent,
contrary to independence of that local triple.

This contradiction excludes every `p_1(a,b)` with `ab(a+b)!=0`.

## 4. The three exceptional `Phi_1` lines

On the exceptional directions, a diagonal channel in (7) vanishes
identically.  Contracting the corresponding nonzero pure target in (4)
gives

```text
a=0       => alpha_0=0,
b=0       => alpha_2=0,
a+b=0     => alpha_1=0.                                  (14)
```

Consequently every nonzero local `Phi_1` kernel vector lies on exactly one
of

```text
K(x_1+x_2),               K(x_0+x_2),               K(x_0-x_1), (15)
```

with local support contained in `{1,2}`, `{0,1}`, `{0,2}`, respectively.

## 5. The two exceptional `Phi_2` lines

Suppose first that `ab!=0` for `p=p_2(a,b) in L_t`.  Contract relation
(9) with the exact target (4).  It becomes

```text
-(a/b)lambda_0 alpha_0 e_0^* tensor 3
 +lambda_1 alpha_1 e_1^* tensor 3
 +lambda_2 alpha_2 e_2^* tensor 3=0.                     (16)
```

The three displayed coordinate tensors are linearly independent.  Since
`a/b` and every `lambda_c` are nonzero, (16) forces
`alpha_0=alpha_1=alpha_2=0`, contradicting `p!=0`.  Thus a local `Phi_2`
kernel vector has `a=0` or `b=0`.

The exceptional zero channels in (7) sharpen their local supports:

```text
a=0: D_1=D_2=0  => alpha_1=alpha_2=0,
b=0: D_0=0      => alpha_0=0.                             (17)
```

Therefore the only possible lines are

```text
Kx_3,                  with local support exactly {0},
K(x_1+x_2),            with local support in {1,2}.       (18)
```

The first support is exactly `{0}` because the kernel vector is nonzero.

## 6. Rank and finite residual boundary

For fixed `k,t`, the vector space `L_t intersect ker(Phi_k)` is contained
in a finite union of the lines in (15) or (18).  Over the infinite field
`K`, a vector space cannot be a finite union of proper linear subspaces.
Thus

```text
dim(L_t intersect ker(Phi_k))<=1,
rank(Phi_k|L_t)>=2.                                      (19)
```

The two-sided projection-drop predecessor supplies a mode of rank at most
two in each family.  Combining with (19) gives

```text
min_t rank(Phi_1|L_t)=min_t rank(Phi_2|L_t)=2.           (20)
```

The exact proved/open boundary is

```text
triangle pair, every local Phi_k rank at least two:       PROVED;
Phi_1 low kernels localized to three lines:               PROVED;
Phi_2 low kernels localized to two lines:                 PROVED;
one rank-two mode in each projection family:              PROVED NECESSARY;
finite exceptional-line incidence exclusion:              OPEN;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.    (21)
```

## Replay

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_kernel_support_boundary.py
python claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_kernel_support_boundary.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_kernel_support_boundary.py claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_kernel_support_boundary.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_kernel_support_boundary.py claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_kernel_support_boundary.py
```

The primary verifier reconstructs both kernels, checks all ten polarized
single contractions, proves the determinant and residual relation
symbolically, and checks the rank gates used in the two structural lemmas.
The independent no-import audit rebuilds the quartics as square-free
monomial dictionaries, contracts them directly, and exhausts every
projective kernel direction over two odd finite fields.  These computations
audit identities and case boundaries; the written arguments prove the
characteristic-zero theorem.
