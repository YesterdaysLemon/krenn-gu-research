# Self-review: one-deficient involved row with support-one third kernel

Date: 2026-08-13

Claim reviewed:
[one-deficient-involved-row third-row-support-one complete exclusion](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_ONE_DEFICIENT_INVOLVED_ROW_THIRD_ROW_SUPPORT_ONE_COMPLETE_EXCLUSION_THEOREM.md).

## Verdict

The mixed `(2,3,2)` support-one exclusion and its root-exchanged `(3,2,2)`
mate are supported.  Combined with S2BY and S2BZ, every rank-four/rank-eight
profile with at least one deficient involved row is now closed.  The proof
does not address a fully injective involved-row profile.

## Load-bearing checks

### The split orientation is exhaustive

The third-row-kernel atlas proves that the supported colour `s` is
represented by `x` or `y`.  The `T_s` correction sharpens these alternatives
to a split vector in the opposite involved summand.  The `T_d` correction is
vertical because `d!=s`.  If `y` represented `s`, these vectors and the one
remaining third lift would give the second projection dimension at most two,
contrary to its assumed rank three.  Thus no orientation was discarded by a
coordinate choice.

### The root-box quotient is genuinely direct

The singleton images have triangular coordinates outside the root box:
`ddd`, then `ddt`, then `sss`.  Their coefficients are respectively
`kappa`, `kappa`, and `e_s^*(w)`, all nonzero.  This proves `U intersect L=0`
for arbitrary residual `C_bar` and arbitrary `w` nonzero on `e_s`; the proof
does not silently assume a monomial residual block or coordinate shared
factor.

### The second-row rank is used exactly

The second rows `p_d,p_t` lie in `span(u,v)`.  Rank three of the whole row,
whose `p_s` alone contains `g_2`, makes `p_d,p_t` independent.  Their two
zero third-`t` coefficients therefore force both `P(u,u,v)` and
`P(u,v,v)` to vanish.  The `tdt` zero and nonzero `ttt` target then force
`p_d` onto the `u` line and make `P(v,v,v)` a nonzero pure tensor.

### Resonance does not assume an algebraic closure

The proof uses only the field elements `alpha,beta,gamma` already obtained
from the physical rows and the identities `e_1=e_2=0`.  A primitive cube
root appears only in verifier fixtures over the exact extension
`Q(omega)`; it is not adjoined in the theorem.  The common-kernel rank
argument uses characteristic zero directly and remains valid over the
original field.

### The `T_d` line cannot hide in the tangent space

After resonance, every term of `P(v,u,r)` and `P(u,u,r)` has two `t` factor
lines, hence lies in the Segre tangent at `T_t`.  Quotienting all three
source factors by their `t` lines kills that tangent and preserves `T_d`.
Thus membership in `span(T_d)` forces the two tensors themselves to vanish;
no coefficient of `C_bar` is assumed zero.

### The final dependence is physical

The simultaneous kernel of the two scalar rows is exactly
`span((1,1,1))`, so `g_1` is proportional to `g_3`.  These are images of
two distinct basis covectors under `H^*`.  Surjectivity of the physical map
`H` makes `H^*` injective, so the dependence is a genuine contradiction,
not a basis artifact.

## Verification independence

The SymPy replay constructs the mixed four-space, checks the direct
twelve-dimensional root box, performs the root-row elimination, and verifies
the resonance collapse as a rank-eight map.  The no-import audit reverses
tensor indexing, implements independent Gaussian elimination and a custom
two-coordinate `Q(omega)` field, and repeats the argument for all six colour
permutations.  Neither script imports the other.

## Status boundary

```text
mixed (2,3,2)/(3,2,2), support-one third kernel:    IMPOSSIBLE;
all profiles with one deficient involved row:        CLOSED;
fully injective involved-row rank-four/rank-eight:   OPEN;
other cells, components, poles, higher orders:       OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```
