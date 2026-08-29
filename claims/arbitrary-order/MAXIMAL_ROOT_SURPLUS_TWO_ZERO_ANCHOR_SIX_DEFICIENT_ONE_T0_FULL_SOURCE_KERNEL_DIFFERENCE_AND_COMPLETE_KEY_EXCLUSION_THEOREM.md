# Maximum-root surplus-two zero-anchor six-deficient one-`T_0` full-source kernel difference and complete key exclusion

## Status

This is theorem package **GLS77**.  It closes the Family-A `r=1` key

```text
S_0 R_2 R_1 R_0^2 T_0
```

left open by `GLS72` and sharpened by `GLS73`.

The proof uses literal coefficients of the complete eight-vertex source
identity.  Twenty-four zero-target coefficients force one common `2 x 2`
physical outer-product matrix to vanish.  Five differences of full
monochromatic coefficient rows then give an elementary characteristic-zero
contradiction.  The differences cancel the two off-kernel repair channels
which prevented the `GLS73` proper-face argument from closing the key.  No
transport from a kernel line to an off-kernel vector is assumed.

The key contains `1,080` labelled profiles.  Hence the live six-deficient
residual changes from

```text
98,295 / 80  ->  97,215 / 79.
```

Family A at `r=2,3`, every other five-/six-deficient branch, every earlier
residual branch, and the global Krenn--Gu conjecture remain **OPEN /
UNRESOLVED**.

## 0. Dependencies, field, and complete-row convention

Work over the characteristic-zero fraction field used by
`GLS61`--`GLS76`.  The proof uses:

- the Family-A crossed normalization of `GLS71`;
- the exhaustive activity localization of `GLS72`; and
- the `GLS72` conclusion that every survivor has the unique `T_0` port
  selector-silent and lies on `alpha=a=b=0`.

Put the central triangle at `{0,1,2}`, the two `R_0` ports at `3,4`, and the
silent `T_0` port at `5`.  The crossed normalization is

```text
p_0=P_1 e_(0,1),       q_0=Q_2 e_(0,2),
p_1=P_2 e_(1,2),       q_1=0,
p_2=0,                 q_2=Q_1 e_(2,1).              (1)
```

The nonzero scalars absorbed in (1) merely rescale the three nonzero GHZ
target coefficients and never make them zero.

For a complete coefficient word use the order

```text
(c_P,c_Q,c_0,c_1,c_2,c_3,c_4,c_5) in {0,1,2}^8       (2)
```

and the zero-based base-three index

```text
ind(c)=sum_(j=0)^7 c_j 3^(7-j).                       (3)
```

Thus every numerical row named below identifies one literal coefficient of
the full eight-vertex hafnian identity.  It is not an index in a reduced
deck or a finite-field encoding.

## 1. The surviving `T_0` normalization

Write the rank-two row plane and its kernel as

```text
J_5=F e_(5,0)^* direct-sum F h_5,
h_5=e_(5,1)^*+kappa e_(5,2)^*,
K_5=F(kappa e_(5,1)-e_(5,2)),       kappa!=0.         (4)
```

The two target coordinates occur nontrivially on the `T_0` kernel, so
`kappa` is a unit in the function field.  Since the `P_0,Q_0` rows at port
`5` are silent, write the four remaining source rows in the basis (4):

```text
[P_i]p_5=P_i0 e_(5,0)^*+P_ih h_5,
[Q_i]q_5=Q_i0 e_(5,0)^*+Q_ih h_5,       i=1,2.       (5)
```

Their span is `J_5`, hence has rank two.

For physical edges put

```text
I_ij^(ab)=[e_(i,a)e_(j,b)]W_ij.                       (6)
```

The `GLS72` survivor equations are

```text
I_12^(12)=0,
W_15(e_(1,1),-)|_(K_5)=0,
W_25(e_(2,2),-)|_(K_5)=0.                             (7)
```

In the basis (4), the last two equalities say

```text
I_15^(12)=kappa I_15^(11),
I_25^(22)=kappa I_25^(21).                            (8)
```

They impose no condition on the `e_(5,0)` coefficients of those edges.

On the two `R_0` kernels define

```text
r_i=I_13^(1i),       s_i=I_23^(2i),       i=1,2,
m_j=I_14^(1j),       p_j=I_24^(2j),       j=1,2,
C_ij=r_i p_j+s_i m_j.                                 (9)
```

Equivalently,

```text
C=r p^T+s m^T.                                        (10)
```

## 2. Twenty-four full coefficients force `C=0`

### Lemma 2.1 (complete-row product table)

For each `i,j in {1,2}`, literal expansion of the full source identity on
the following rows gives `C_ij` times the indicated source-row coordinate,
up to the displayed nonzero unit `1` or `kappa`:

| coordinate | `C_11` | `C_12` | `C_21` | `C_22` |
|---|---:|---:|---:|---:|
| `Q_10` | `3306` | `3309` | `3315` | `3318` |
| `Q_20` | `4035` | `4038` | `4044` | `4047` |
| `P_10` | `4278` | `4281` | `4287` | `4290` |
| `P_20` | `6465` | `6468` | `6474` | `6477` |
| `Q_1h` | `3308` | `3310` | `3317` | `3319` |
| `P_2h` | `6467` | `6470` | `6476` | `6479` |

Every target on these twenty-four rows is zero.  More explicitly, each row
is one of

```text
Q_10 C_ij=0,       Q_20 C_ij=0,
P_10 C_ij=0,       P_20 C_ij=0,
u_ij Q_1h C_ij=0, v_ij P_2h C_ij=0,                  (11)
```

where `u_ij,v_ij` belong to `{1,kappa}`.

### Proof

Expand the `105` perfect matchings of the eight vertices on each word (2).
The crossed normalization (1), the rank-one support of ports `3,4`, and (7)
kill every matching except the two terms

```text
I_13^(1i) I_24^(2j)       and
I_23^(2i) I_14^(1j),                              (12)
```

multiplied by the named row coefficient at port `5`.  When the local
coordinate at port `5` is `2`, (4) supplies the unit `kappa`.  This is
exactly (11). `square`

### Corollary 2.2 (rank-two source integrability)

```text
C_ij=0 for every i,j.                                  (13)
```

### Proof

If some `C_ij` were nonzero, its six equations in (11) would give

```text
P_10=P_20=Q_10=Q_20=Q_1h=P_2h=0.                     (14)
```

The four rows in (5) would then be

```text
P_1h h_5,       0,       0,       Q_2h h_5,          (15)
```

and would span at most one line.  This contradicts `rank J_5=2`.  Hence no
entry can be nonzero. `square`

The two exceptional coordinates `P_1h,Q_2h` are not set to zero.  The rank
argument works precisely because, after (14), both lie on the same
transverse line.

## 3. Five kernel differences retain the full source

Define the four physical kernel differences

```text
X=I_45^(12)-kappa I_45^(11),
T=I_45^(22)-kappa I_45^(21),
Y=I_35^(12)-kappa I_35^(11),
Z=I_35^(22)-kappa I_35^(21).                          (16)
```

For each pair below, subtract `kappa` times the first full coefficient from
the second:

```text
(3280,3281),       (3289,3290),
(6547,6548),       (6556,6557),       (6559,6560).     (17)
```

Every source-pair term incident to port `5` cancels because its row lies in
`J_5`.  The `W_15(e_(1,1),-)` and `W_25(e_(2,2),-)` terms cancel by (8).
All off-kernel source-row and deck repair terms therefore cancel before any
restriction is taken.  Direct expansion leaves

```text
r_1 X+m_1 Y=M_1,          M_1=-kappa mu_1!=0,
r_2 X+m_1 Z=0,
s_1 X+p_1 Y=0,
s_2 X+p_1 Z=0,
s_2 T+p_2 Z=M_2,          M_2=mu_2!=0.                (18)
```

The values `mu_1,mu_2` include the harmless nonzero normalizing scalars from
(1).  Only their nonvanishing is used.

Equation (18) is a full-source statement.  It is not obtained by first
restricting the `GLS73` relation to `K_5`; in particular, the synchronized
`H_(0124)` and `H_(0123)` repair channels are present in each raw row and
cancel in the paired differences.

## 4. The outer-product contradiction

### Lemma 4.1

Over a field of characteristic zero, equations (13) and (18) have no
solution with `M_1M_2!=0`.

### Proof

Equation (13) is

```text
r p^T=-s m^T.                                          (19)
```

Suppose first that both rank-one tensors in (19) are nonzero.  Then for a
nonzero scalar `gamma`,

```text
r=gamma s,             p=-gamma^(-1)m.                (20)
```

The first and third equations of (18) give

```text
gamma s_1 X+m_1Y=M_1,
gamma s_1 X-m_1Y=0.                                   (21)
```

Thus `M_1=2gamma s_1X=2m_1Y`.  Characteristic zero and `M_1!=0` imply

```text
s_1 X m_1 Y!=0.                                       (22)
```

The second and fourth equations of (18) similarly give

```text
gamma s_2X+m_1Z=0,
gamma s_2X-m_1Z=0.                                    (23)
```

Hence `s_2=0` and `Z=0`.  The last equation of (18) now has zero left side,
contradicting `M_2!=0`.

It remains to suppose that one rank-one tensor in (19) is zero.  Then both
are zero.  The alternatives `r=0 or p=0` and `s=0 or m=0` give four cases:

1. `r=s=0`: the first equation makes `m_1Y=M_1`, so `m_1,Y!=0`; the second
   gives `Z=0`, and the last contradicts `M_2!=0`.
2. `r=m=0`: the first equation reads `0=M_1`.
3. `p=s=0`: the last equation reads `0=M_2`.
4. `p=m=0`: the first equation makes `r_1X=M_1`, so `X!=0`; the second,
   third, and fourth give `r_2=s_1=s_2=0`, and the last again reads
   `0=M_2`.

These cases exhaust (19). `square`

### Theorem 4.2 (complete Family-A `r=1` exclusion)

No Family-A source exists in the `r=1` key.

### Proof

`GLS72` exhaustively excludes the all-active cell, every silent-`R_0` cell,
and the silent-`T_0` branches with `alpha!=0` or `alpha=0,ab!=0`.  Its only
survivor is exactly (7).
Corollary 2.2 and the five complete-row differences (18) apply to that
survivor, while Lemma 4.1 excludes it.  Therefore no cell remains. `square`

## 5. Residual and live boundary

The closed key has `1,080` labelled profiles, so

```text
98,295 / 80 - 1,080 / 1 = 97,215 / 79.                (24)
```

The remaining single-binary keys are

```text
Family A, r=2:       1,080 / 1 key,
Family A, r=3:         360 / 1 key,
total:               1,440 / 2 keys.                  (25)
```

This is a strict local closure.  It does not close the other `97,215`
six-deficient profiles, any five-deficient or earlier residual branch, or
the global conjecture.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_one_t0_full_source_kernel_difference_and_complete_key_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_one_t0_full_source_kernel_difference_and_complete_key_exclusion.py
```

The primary verifier reconstructs the `105` perfect matchings, expands all
thirty-four raw coefficient rows over a symbolic characteristic-zero ring,
checks the twenty-four product factorizations and five paired differences,
and checks the residual arithmetic.  The independent audit uses a separate
matching recursion and an exact custom sparse-polynomial representation
without importing the primary script; it also exhausts the reduced
consequence over two small fields.  The rank-two inference and the arbitrary
characteristic-zero outer-product case split remain written mathematics; the
scripts replay their exact algebraic inputs and test their consequences
independently.

Neither script proves any result outside the stated Family-A `r=1` key or
resolves the Krenn--Gu conjecture.
