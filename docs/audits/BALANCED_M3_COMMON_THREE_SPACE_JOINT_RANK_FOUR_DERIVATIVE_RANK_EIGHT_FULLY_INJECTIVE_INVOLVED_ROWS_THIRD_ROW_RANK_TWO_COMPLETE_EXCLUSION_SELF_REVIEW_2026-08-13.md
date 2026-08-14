# Self-review: fully injective involved rows with third-row rank two

Date: 2026-08-13

Claim reviewed:
[fully-injective-involved-rows third-row-rank-two complete exclusion](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_INVOLVED_ROWS_THIRD_ROW_RANK_TWO_COMPLETE_EXCLUSION_THEOREM.md).

## Verdict

The complete `(3,3,2)` exclusion is supported for both support-one and
support-two third kernels.  Together with S2BX--S2CA, this leaves only
`(3,3,3)` in the joint-rank-four, derivative-rank-eight row census.  No
claim is made for joint rank three or derivative rank seven.

## Load-bearing checks

### The vertical/nonvertical split is exhaustive

The vertical subspace is exactly `K intersect A_3` and has dimension at
most one under either injective involved projection.  A supported target
coefficient always gives a split tangent class modulo the known derivative
syzygy.  With a vertical line, support one leaves only one further first- or
second-projection direction, while support two uses both remaining classes
on the two coordinate splits.  The stated rank-two contradictions therefore
do not assume a special lift gauge.

### The root box is direct only after verticals are removed

For a singleton image lying in `A_1 tensor A_2 tensor Q_3`, contraction by
the third kernel kills its tangent part.  Subtracting the syzygy leaves a
vertical vector of `K`.  The nonvertical branch makes that vector zero and
proves `U intersect L=0`.  The proof does not use directness on the vertical
branch and does not silently discard a possible `C tensor c` intersection.

### The rank-four obstruction is applied to exact representatives

Directness makes the complete empty target equal to the sum of exactly three
source diagonals times the unique root representatives `F_i`; every other
source coefficient is zero.  Simultaneous nonvanishing of three nonzero
trilinear forms is valid over the infinite characteristic-zero field.  The
resulting concise ternary diagonal makes all three local maps invertible, so
the previously proved `rank(P_3)=4` obstruction applies without a genericity
upgrade.

### A zero representative has only two genuine alternatives

If its correction has nonzero third component, equality across the
`(A_1 tensor A_2)|A_3` split makes `C` the represented coordinate square;
that square lies in the derivative tangent plane and violates rank eight.
If the third component is zero, the same equality makes `w` the supported
coordinate.  No third case is hidden by a zero right-hand factor, since
`C` and the third component are then both nonzero.

### The support-one plane equality is basis-free

The annihilator of the complementary involved-row plane consists of vectors
whose involved component lies on the supported coordinate.  Both generators
of `ker(pr_3|K)` have exactly that property, and both annihilators have
dimension two.  Thus the involved binary plane equals the third-row plane;
this is not inferred from one convenient fixture.  The exact remaining
target is the two-colour diagonal table required by S2BF.

### The support-two symmetry reduction keeps the residual block

After identifying the equal first/third planes by the induced isomorphism
`A`, the proof retains every component of `C` visible on that plane.
Outer-factor symmetry fixes only its `e_d` coefficient and produces the
full normal form with a mixed coefficient `q_d` and arbitrary middle vector
`n`.  The mixed-factor lemma forces `q_d=0`; the independent/proportional
fork for `e_d,n` is exhaustive and lands respectively in the audited S2BF
binary obstruction and S2AL two-square obstruction.

## Verification independence

The SymPy replay constructs both vertical rank failures, a nonvertical
rank-eight fixture with an eighteen-dimensional direct root box, the
support-one equal plane, and the complete outer-symmetry reduction.  The
no-import audit reverses tensor indexing, uses separate `Fraction` Gaussian
elimination, loops over all six colour orders, and independently checks the
same terminal fork.  The already audited S2R rank, S2AL tangent/two-square,
and S2BF binary lemmas remain explicit dependencies rather than duplicated
certificates.

## Status boundary

```text
fully injective involved rows, third-row rank two:  IMPOSSIBLE;
remaining rank-four/rank-eight profile (3,3,3):     OPEN;
other lower-rank cells, components, and poles:      OPEN;
higher orders and all-rank-drop:                    OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```
