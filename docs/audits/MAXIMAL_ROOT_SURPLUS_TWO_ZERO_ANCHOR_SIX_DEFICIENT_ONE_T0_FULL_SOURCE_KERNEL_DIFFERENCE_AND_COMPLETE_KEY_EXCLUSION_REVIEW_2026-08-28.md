# Hostile review: one-`T_0` Family-A full-source kernel difference and complete key exclusion

## Verdict

**PASS for the complete Family-A `r=1` key.**  `GLS77` closes the sole
`GLS72` survivor by using literal coefficients of the complete eight-vertex
source identity.  It does not transport a relation from the silent-port
kernel to an off-kernel vector.  The proof removes `1,080 / 1` and changes the
live six-deficient residual from `98,295 / 80` to `97,215 / 79`.

This verdict is scoped.  Family A `r=2,3`, every other five-/six-deficient
branch, the earlier residual branches, and the global Krenn--Gu conjecture
remain **OPEN / UNRESOLVED**.

## Artifacts reviewed

- [`GLS77` theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_ONE_T0_FULL_SOURCE_KERNEL_DIFFERENCE_AND_COMPLETE_KEY_EXCLUSION_THEOREM.md)
- [primary verifier](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_one_t0_full_source_kernel_difference_and_complete_key_exclusion.py)
- [independent audit](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_one_t0_full_source_kernel_difference_and_complete_key_exclusion.py)
- [`GLS72` localization and sharpness parent](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_ONE_T0_SINGLE_BINARY_ACTIVITY_LOCALIZATION_AND_TRANSVERSE_FULL_DECK_SHARPNESS_THEOREM.md)
- [`GLS73` fixed-core nonextension boundary](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_ONE_T0_OFF_PORT_CORE_FULL_SOURCE_NONEXTENSION_AND_COUPLED_CORRECTION_BOUNDARY_THEOREM.md)

## 1. Complete-row provenance

The audit independently reconstructed all `105` perfect matchings with word
order

```text
(c_P,c_Q,c_0,c_1,c_2,c_3,c_4,c_5)
```

and zero-based base-three row indices.  In the crossed Family-A normalization,
the twenty-four stated zero-target rows expand as follows:

```text
Q_10 C_ij:  3306, 3309, 3315, 3318
Q_20 C_ij:  4035, 4038, 4044, 4047
P_10 C_ij:  4278, 4281, 4287, 4290
P_20 C_ij:  6465, 6468, 6474, 6477
Q_1h C_ij:  3308, 3310, 3317, 3319
P_2h C_ij:  6467, 6470, 6476, 6479
```

The `Q_1h` units are `kappa,1,kappa,1`; all four `P_2h` units are
`kappa`.  The only surviving physical terms are

```text
I_13^(1i) I_24^(2j) + I_23^(2i) I_14^(1j).
```

The otherwise possible `I_12^(12) I_34^(ij)` term is zero on the exact
`GLS72` survivor.  Therefore the common matrix is genuinely

```text
C=r p^T+s m^T,
```

with no omitted complete-source repair term.

## 2. Rank-two inference

If one entry `C_ij` were nonzero, its six product equations would force

```text
P_10=P_20=Q_10=Q_20=Q_1h=P_2h=0.
```

The `P_0,Q_0` rows are already silent at port `5`.  The only rows remaining
in its source row plane would therefore be `P_1h h_5` and `Q_2h h_5`, which
span at most one line.  This contradicts the rank-two `T_0` type.  Hence
every entry of `C` is zero.

This argument deliberately retains the two exceptional coordinates
`P_1h,Q_2h`.  An earlier exploratory route incorrectly set both to zero and
then reported a finite-field obstruction.  That route hard-wired a stronger
endpoint condition than the `T_0` hypothesis supplies and was discarded.
Neither the theorem nor either retained checker uses it.

## 3. Full-source kernel differences

The five paired rows

```text
(3280,3281), (3289,3290), (6547,6548),
(6556,6557), (6559,6560)
```

were expanded before taking any kernel restriction.  Subtracting `kappa`
times the first row in each pair from the second gives exactly

```text
r_1 X+m_1 Y=-kappa mu_1,
r_2 X+m_1 Z=0,
s_1 X+p_1 Y=0,
s_2 X+p_1 Z=0,
s_2 T+p_2 Z=mu_2.
```

The relevant `W_15` and `W_25` slices cancel by the two accepted `GLS72`
kernel relations.  Probe-source terms incident to port `5`, including their
off-kernel row coordinates, cancel in the same raw difference.  The
synchronized `H_(0124)` and `H_(0123)` channels are therefore present in
each individual coefficient but absent from the difference for a proved
algebraic reason.  This is the required source-integrability step; no
coefficient on `K_5` is silently promoted to `e_(5,0)`.

## 4. Characteristic-zero contradiction

From `C=0`,

```text
r p^T=-s m^T.
```

If both outer products are nonzero, their rank-one factors are proportional:
`r=gamma s` and `p=-gamma^(-1)m`.  Adding and subtracting the first/third
target equations makes `s_1,X,m_1,Y` nonzero.  The second/fourth equations
then give `s_2=Z=0`, so the last nonzero target equation vanishes.  The use of
`2!=0` is explicit and is why the theorem is stated in characteristic zero.

If either outer product is zero, both are zero.  The four exhaustive choices

```text
r=s=0,  r=m=0,  p=s=0,  p=m=0
```

contradict respectively the second target after `Z=0`, the first target, the
second target, or the second target after `r_2=s_1=s_2=0`.  No division by a
possibly zero physical coefficient occurs in this branch.

## 5. Computational and scope audit

The primary verifier symbolically expands all thirty-four literal rows over
an exact characteristic-zero ring, checks all twenty-four product
factorizations and five paired differences, and independently checks the
reduced obstruction by Groebner ideal arithmetic over `QQ`.

The no-import audit uses a separate bit-mask matching recursion and a custom
sparse integer-polynomial representation rather than SymPy.  It reconstructs
the same thirty-four rows and exhaustively finds no reduced solution over
`F_2` or `F_3`.  Those finite-field checks audit the algebraic inputs; the
written rank-one case split supplies the arbitrary characteristic-zero
proof.

Both scripts reproduce the count change

```text
98,295 / 80 - 1,080 / 1 = 97,215 / 79.
```

The audit found no exact counterexample and no surviving cell inside the
stated Family-A `r=1` key.  It does not claim that the same row-plane argument
extends to Family A `r=2,3`, nor that the remaining `97,215` profiles form an
exhaustive global proof route.  Global Krenn--Gu remains **UNRESOLVED**.
