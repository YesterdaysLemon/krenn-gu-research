# Arbitrary permanent fixed-pair support-two low double-contraction incidence theorem

## Status

This note proves an exact characteristic-zero incidence restriction inside
the simultaneous-low residual for the fixed equality-five pair.  Suppose two
**distinct** remaining local modes contain support-two exceptional low
vectors.  If the lows belong to different projection families, their
exceptional lines must miss different colours.  If they belong to the same
family, they must be the common line `N` and one non-`N` line; in particular,
each family has at most two support-two low modes.

In every surviving case the `x_4,x_5` pairing matrix between the other two
modes is a nonzero rank-one matrix supported on the unique common colour.
Consequently at least one of those modes has `A`-projection rank one, and its
`A`-projection is supported only at that colour.

The distinct-mode hypothesis is essential.  This note does not exclude a
`Phi_1`-low and a `Phi_2`-low in the same local mode, does not classify
singleton-supported exceptional lows, and does not exclude all surviving
support-two incidences.  Unrestricted permanent nonrestriction remains
unknown, and the global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Fixed pair and exceptional lines

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

At the fixed equality-five pair, the complementary quartics of the two mixed
and three diagonal product classes are

```text
star(m_1)= x_4x_5 x_1 (x_3-x_2-x_0),
star(m_2)= x_4x_5 x_0 (x_3-x_2-x_1),
star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.                             (1)
```

Let the ordered independent triples

```text
(y_(t,0),y_(t,1),y_(t,2)),                 t=2,3,4,5,
```

span the local planes `L_t`, and assume the exact target equations

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (2)
```

The exceptional-kernel predecessor reduces every low line to

```text
Phi_1: N=x_2+x_3,  A_0=x_0+x_3,  C_0=x_0-x_2,
Phi_2: N=x_2+x_3,  A_1=x_1+x_3,  C_1=x_1-x_2.          (3)
```

For a support-two low vector, the missing colour and hence its exact support
are

```text
line      missing colour       support

N                2              {0,1}
A_0              0              {1,2}
C_0              1              {0,2}
A_1              1              {0,2}
C_1              0              {1,2}.                 (4)
```

Here support is taken in the local colour expansion of the vector.  The
predecessor proves the displayed zero; the support-two hypothesis says that
the other two coefficients are nonzero.

Split the ambient six-space as

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5},         (5)
```

and put

```text
J((s_4,s_5),(t_4,t_5))=s_4t_5+s_5t_4.                 (6)
```

## 2. The double-contraction equation

Parametrize the two ambient kernels by

```text
p_1(a,b)=(a,0,b,a+b,0,0),
p_2(c,d)=(0,c,d,c+d,0,0).                              (7)
```

Direct double contraction of (1), with the common `x_4x_5` suppressed,
gives

```text
pair                     m_1       m_2       d_0

p_1(a,b),p_2(c,d)          0         0       2b(c+d)
p_1(a,b),p_1(A,B)          0       2aA       2bB
p_2(c,d),p_2(C,D)        2cC        0       2(c+d)(C+D)

pair                     d_1                    d_2

p_1(a,b),p_2(c,d)        2d(a+b)               -2ac
p_1(a,b),p_1(A,B)        2(a+b)(A+B)              0
p_2(c,d),p_2(C,D)        2dD                       0.    (8)
```

Now put the two low vectors in distinct modes `t,u`, write their local
coefficient vectors as `alpha,beta`, and call the other modes `s,v`.  Define

```text
M_ij=J(a(y_(s,i)),a(y_(v,j))),              0<=i,j<=2, (9)
```

where `a` denotes projection to `A`.  If `sigma_z` is the entry of (8) for
channel `z`, evaluation of the twice-contracted quartic on the last two
local modes and comparison with (2) gives the exact matrix equations

```text
sigma_(m_1) M=sigma_(m_2) M=0,
sigma_(d_c) M=lambda_c alpha_c beta_c E_cc,
                                                   c=0,1,2. (10)
```

The same matrix `M` occurs in every channel.  This elementary observation
is the entire obstruction.

## 3. Cross-family classification

### Theorem 1 (different families must miss different colours)

Let a support-two `Phi_1`-low and a support-two `Phi_2`-low occur in
distinct modes.  Their exceptional lines cannot have the same missing
colour.  The six surviving ordered pairs, their unique common support
colour `e`, and the only nonzero diagonal scalar in (8) are

```text
Phi_1 line   Phi_2 line     e       nonzero channel

N            A_1            0       d_0
N            C_1            1       d_1
A_0          N              1       d_1
A_0          A_1            2       d_2
C_0          N              0       d_0
C_0          C_1            2       d_2.               (11)
```

In every case

```text
M=mu E_ee                         for some mu!=0.       (12)
```

### Proof

If the two lines miss the same colour, their support is the same two-colour
set.  The three possibilities are

```text
(N,N),             (A_0,C_1),             (C_0,A_1).
```

Substitution in (8) gives two nonzero diagonal scalars, one for each support
colour.  Since the corresponding `alpha_c beta_c` and `lambda_c` are
nonzero, (10) would make the one matrix `M` a nonzero multiple of two
different matrix units.  This is impossible.

If the missed colours differ, the two supports intersect in exactly one
colour `e`.  Substitution in (8) gives exactly one nonzero diagonal scalar,
in channel `d_e`; this yields precisely table (11).  Equation (10), together
with `lambda_e alpha_e beta_e!=0`, then proves (12).

## 4. Same-family classification

### Theorem 2 (at most two support-two low modes per family)

Two support-two lows from one projection family in distinct modes can occur
only as `N` plus one non-`N` line.  More explicitly, the surviving pairs are

```text
family       lines          e       nonzero diagonal channel

Phi_1        N,A_0           1       d_1
Phi_1        N,C_0           0       d_0
Phi_2        N,A_1           0       d_0
Phi_2        N,C_1           1       d_1.               (13)
```

Again (12) holds.  Consequently, among all four remaining local modes, each
projection family has at most two support-two low modes; if it has two,
their line types are exactly one of the pairs in (13).

### Proof

Any two non-`N` lines in the same family both contain colour `2` in their
support.  But the same-family `d_2` scalar in (8) is identically zero, so
the `d_2` equation in (10) reads

```text
0=lambda_2 alpha_2 beta_2 E_22,
```

whose right side is nonzero.  Thus two non-`N` lows are impossible.

For two `N` lows, both `d_0` and `d_1` scalars are nonzero and both colour
coefficients are nonzero.  Equation (10) would again make `M` a nonzero
multiple of two distinct matrix units.  Thus two `N` lows are impossible.

The only remaining pair type is `N` plus one non-`N` line.  Direct
substitution in (8) gives (13), and (10) proves (12).  Finally, among three
support-two low modes some pair would be either two `N` modes or two
non-`N` modes.  Hence there can be at most two.

## 5. Forced `A`-rank-one shore

### Lemma 3 (rank-one pairing matrix)

Let `P,Q:K^3 -> A` be the two `A`-projection maps whose matrices have the
columns `a(y_(s,i))` and `a(y_(v,j))`.  If

```text
P^T J Q=mu E_ee,                         mu!=0,         (14)
```

then

```text
(rank P,rank Q) is one of (1,1),(1,2),(2,1).           (15)
```

Every rank-one map among `P,Q` is supported only at colour `e`: its two
off-`e` columns vanish.  If the other map has rank two, its off-`e` columns
lie in the single `J`-orthogonal line to the rank-one shore's `e`-column.

### Proof

The nonzero matrix in (14) makes both maps nonzero.  If both had rank two,
then `Q` would be surjective, `J` would be an isomorphism, and `P^T` would
be injective.  Their composite would have rank two, contradicting (14).
This proves (15).

Suppose, for example, that `P` has rank one.  Its `e`-column is nonzero,
because row `e` of (14) is nonzero.  Every other column of `P` is a scalar
multiple of that column.  Column `e` of `Q` pairs nontrivially with it, while
the off-`e` rows of (14) vanish, so those scalars are zero.  Thus the
off-`e` columns of `P` vanish.  The statement for `Q` is symmetric.  If
`P` has rank two and `Q` rank one, the zero off-`e` rows say that the
off-`e` columns of `P` lie in the one-dimensional orthogonal complement of
the nonzero `e`-column of `Q`; the other case is symmetric.

Applying the lemma to (12) proves the announced `A`-rank boundary for every
surviving pair in (11) and (13).

## 6. Same-mode cross-family boundary

The cross-family part uses `t!=u` essentially: the two contractions occupy
two different slots of the four-linear target tensor.  If both family lows
lie in the same local plane, plugging both vectors into different slots is
not an evaluation of the restricted tensor, so equation (10) is unavailable.

At the ambient level

```text
ker(Phi_1) intersect ker(Phi_2)=K N.                   (16)
```

Thus proportional same-mode family lows must both use `N`; nonproportional
same-mode lows would have to use two different exceptional lines.  Neither
case is excluded here.  In particular, the double-contraction table (8) must
not be silently applied to two vectors drawn from one input slot.

## 7. Exact scope and replay

```text
support-two exceptional lows in distinct modes:          ASSUMED;
cross-family same-missed-colour pairs:                    EXCLUDED;
six cross-family different-missed pairs:                 LOCALIZED;
same-family pair types:                                  CLASSIFIED;
support-two low modes per family:                        AT MOST TWO;
surviving other-mode A-ranks:                            (1,1),(1,2),(2,1);
rank-one A-shore supported only on common colour:         PROVED;
same-mode cross-family lows:                             OPEN HERE;
existence/exclusion of surviving incidences:             OPEN;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.  (17)
```

Replay with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_support_two_low_double_contraction_incidence.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_support_two_low_double_contraction_incidence.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_support_two_low_double_contraction_incidence.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_support_two_low_double_contraction_incidence.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_support_two_low_double_contraction_incidence.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_support_two_low_double_contraction_incidence.py
```

The primary verifier derives all three tables in (8) from the factorized
quartics by exact symbolic polarization, checks every exceptional-line pair,
and exhausts the finite line-type incidence combinatorics.  The independent
audit imports neither the primary verifier nor SymPy: it reconstructs the
quartics as square-free monomial dictionaries, contracts them over the
rationals, independently checks the line-pair classifications, and exhausts
the rank-one pairing consequence over two odd finite fields.  These scripts
replay identities and finite case splits; the written characteristic-zero
argument proves the theorem.
