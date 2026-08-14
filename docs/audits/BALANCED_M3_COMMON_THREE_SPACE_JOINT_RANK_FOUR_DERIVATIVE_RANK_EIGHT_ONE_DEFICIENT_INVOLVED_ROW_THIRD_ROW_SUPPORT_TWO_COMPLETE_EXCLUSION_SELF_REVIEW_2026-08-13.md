# Self-review: one-deficient involved row with support-two third kernel

Date: 2026-08-13

Claim reviewed:
[one-deficient-involved-row third-row-support-two complete exclusion](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_ONE_DEFICIENT_INVOLVED_ROW_THIRD_ROW_SUPPORT_TWO_COMPLETE_EXCLUSION_THEOREM.md).

## Verdict

The mixed `(2,3,2)` support-two exclusion and its `(3,2,2)` mate are
supported.  The proof also recovers the already closed same-colour
support-two case, but does not replace S2BW's independent projection-rank
proof or claim a support-one conclusion.

## Load-bearing checks

### The correction image really is one-dimensional

Third-row rank two makes `ker(pr_3|K)` a two-plane.  Its intersection with
`ker D` is the known one-dimensional derivative syzygy, because the entire
derivative kernel is that line.  Thus its derivative image has dimension
one.  First-missing-row contraction puts every non-`T_d` correction
preimage in this two-plane, so one source tensor multiplying one fixed root
tensor captures all such coefficients.

### The `T_d` ambiguity is harmless

A lift over `e_d` is not unique and may differ from the actual `T_d`
preimage by an element of `ker(pr_3|K)`.  Its derivative difference lies on
the same one-dimensional correction line and is absorbed into the arbitrary
source tensor `S`.  No unrecorded splitting is assumed.

### The third-kernel support excludes the missing colour

The `T_d` preimage has nonzero third component proportional to `e_d`, so
`e_d` belongs to `pr_3 K`.  Every covector in the third-row kernel therefore
annihilates `e_d`.  Support two is exactly the two complementary colours;
both coefficients and the evaluation on `w` are nonzero.

### Source and root coefficients are not conflated

After third contraction, the identity lives in the tensor product of the
source target space with `A_1 tensor A_2`.  Comparing the independent source
coefficients `T_s` and `T_t` separately makes the same nonzero root tensor
`R` proportional to `e_s tensor e_s` and `e_t tensor e_t`.  The `T_d`
tangent term cannot enter either comparison.

### The mixed row is unused for a legitimate reason

The proof requires only one deficient involved row and the rank-two third
projection.  No kernel or zero row is assigned to the injective involved
row.  Root exchange therefore gives the mate profile exactly.

## Verification independence

The SymPy replay builds an exact rank-eight derivative and a rank-(2,3,2)
four-space fixture, checks all projection ranks, the correction affine
system, and the incompatible target lines.  The no-import audit reverses
tensor indexing, implements separate `Fraction` elimination, reconstructs
the derivative and `K` images, and checks every colour permutation.  The
arbitrary source-coefficient comparison remains written mathematics.

## Status boundary

```text
mixed (2,3,2)/(3,2,2), support-two third kernel:    IMPOSSIBLE;
one deficient involved row, support-two third kernel: CLOSED;
mixed support-one / fully injective involved rows:   OPEN;
other cells, components, poles, higher orders:       OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```
