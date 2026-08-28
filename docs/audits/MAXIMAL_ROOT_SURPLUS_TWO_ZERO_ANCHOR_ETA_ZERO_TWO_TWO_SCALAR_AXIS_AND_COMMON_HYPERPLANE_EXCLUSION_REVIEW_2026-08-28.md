# Hostile review: eta-zero two-two scalar-axis and common-hyperplane exclusion

## Review target and verdict

Target reviewed:

`claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ETA_ZERO_TWO_TWO_SCALAR_AXIS_AND_COMMON_HYPERPLANE_EXCLUSION_THEOREM.md`

Supporting artifacts reviewed:

`claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py`

`claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py`

**Verdict: PASS for the exact `GLS66` scope after three independent hostile
reviews.**  No characteristic-zero countermodel or load-bearing algebraic
error was found.  The theorem correctly excludes the `GLS65` eta-zero
`2,2,3,3` residual and therefore closes the complete `GLS63`
exactly-two-deficient branch.

The reviewed version explicitly states where `eta=0` enters the last pair
equation, why silent-off products annihilate the complete rank-three pair
image, why the all-target slice must be nonzero rank one, and why the normal
chart `tau P+B` omits no projective `tau=infinity` case.

This is a scoped zero-anchor, root-order-three, all-six-rigid exclusion.
Three-plus-deficient profiles, the unique-nonrigid/alternate-receiver branch,
attachment, response, selector, synchronization, activity, nonzero anchor,
arbitrary root order, and the global conjecture remain open.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## Exact inherited scope

The proof starts only after all of the following exact reductions:

```text
two deficient maps have common kernel K e_c;
four other ports are injective and nonaxis;
three or four ports are c-oriented;
the raw four-port matching scalar H is nonzero;
eta=W_nm(e_c,e_c)=0;
the eta-zero source is one separated P_4 restriction;
its generic local ranks are exactly 2,2,3,3;
the two rank-two ports are silent.                     (1)
```

The proof does not infer any of these hypotheses for a three-plus-deficient
profile.  All scalar rows and edges are evaluations of the same physical
graph used by `GLS63`--`GLS65`.

## Scalar-axis synchronization

Relabel the silent ports `s,t` and the rank-three ports `r,v`.  Silence gives

```text
A_s=B_s=A_t=B_t=0.
```

The two `GLS64` cofactors omitting `r` or `v` give
`A_rw_st=B_rw_st=0`.  Rank three implies
`(A_r,B_r)!=(0,0)`, hence `w_st=0`.

The other four cofactor equations put both cross-edge columns in the kernel
of

```text
M=[A_r A_v; B_r B_v].
```

If `det M` were nonzero, all four cross edges would vanish and then `H=0`.
Thus `A_rB_v-B_rA_v=0`.  On the already-proved `eta=0` divisor, the remaining
pair equation is `delta_rv=A_rB_v+B_rA_v=0`.  Characteristic zero forces
both products to vanish.  Since neither rank-three pair is zero, both lie
on one coordinate axis.  After exchanging the deficient labels,

```text
A_r,A_v!=0,           B_r=B_v=0,
w_tv=-lambda w_tr,    w_sv=-lambda w_sr,
H=-2 lambda w_sr w_tr!=0.                             (2)
```

No raw edge is divided out.  The four cross edges are consequences of
`H!=0`, and `w_rv` may vanish.

## Rank-three hyperplane synchronization

Let `U_i=im L_i^*` in the four-dimensional source space with coordinates
`P,Q,A,B`.  At `r,v`, condition (2) says that `a_i` leaves the probe plane
while `b_i` lies in it.  Therefore each rank-three rowspace is a hyperplane

```text
U_i=nu_i^perp,          nu_i in span{P,Q,B}.           (3)
```

If the two normals were independent, put `S'=span{P,Q,B}` and write
`U_i=FA direct-sum V_i`.  The two distinct planes `V_r,V_v` span `S'`, so

```text
A S' subseteq U_r U_v.                                (4)
```

In the squarefree Frobenius algebra, the complement pairing identifies
`A S'` perfectly with `R_2(S')`.  Purity says every product containing a
silent off row annihilates the whole pair image `U_rU_v`.

- Opposite silent orientations give the two-off product `PQ`.
- Two `Q` off rows give a one-off product with nonzero active `PQ`
  coefficient `u_t[P]`.
- Two `P` off rows give the probe-exchanged nonzero coefficient `u_t[Q]`.

Each has a nonzero `R_2(S')` component detected by (4).  Hence the normals
are proportional and

```text
U_r=U_v.                                               (5)
```

The independent finite audit separately tested 50,544 normalized pairs of
distinct `F_3` normals and silent orientations; none satisfied the required
off-shell annihilation.

## Common normal and complete annihilator

At least one rank-three port is `c`-oriented.  After probe exchange, take it
to have pure `P` shore and a two-direction `Q` quotient.  Since `B_r=0`, its
fixed `b_r` row lies in the generic probe plane.  A fixed quotient vector
cannot follow a generic two-direction `Q` row, so `b_r` lies on the
`c`-line.  The common relation uses only `P,B`, and its `B` coefficient is
nonzero because the active `P` shore is nonzero.  Thus the complete
projective chart is

```text
nu=tau P+B,          U=span{Q,A,P-tau B},             (6)
```

including `tau=0`; there is no omitted infinite chart.

For `tau!=0`, let `R_0=P-tau B` and `S_0=P+tau B`.  Exact multiplication
gives

```text
UU=span{QA, PQ-tau QB, PA-tau AB, PB},
(UU)^perp=span{Q S_0,A S_0}.                          (7)
```

Every silent-off product must lie in the second space.  Opposite
orientations give `PQ`, which does not.  Two `P` off rows make the one-off
product zero under (7), contradicting its nonzero active `PQ` coefficient.
For two `Q` off rows, both silent target rows lie in `span{Q,S_0}`.  Modulo
the annihilator, their product is a nonzero multiple of

```text
S_0^2=2 tau PB.
```

The bilinear form on `U x U` obtained by pairing with `PB` has matrix

```text
[0 1 0; 1 0 0; 0 0 0]
```

in the basis `(Q,A,R_0)`, hence rank two.  Because the two rank-three
`L_i^*` maps identify their physical duals with `U`, the nonzero pure target
would instead give the outer product of two nonzero target-coordinate
functionals, hence rank one.  This is the contradiction.

For `tau=0`,

```text
U=span{P,Q,A},
UU=(UU)^perp=span{PQ,PA,QA}.                          (8)
```

One-off purity forces the `B` coordinate of each silent target row to
vanish.  Their product then belongs to `UU`, which is totally isotropic
under the complement pairing.  The all-target slice is zero.  Zero fixed
silent rows and all same/opposite orientation types remain covered.

## Corollary scope

`GLS64` forces every `GLS63` exactly-two-deficient residual onto `eta=0`.
`GLS65` gives an exhaustive local-rank profile on that divisor, and the
present theorem excludes it.  Therefore no complete zero-anchor
root-order-three all-six-rigid hypothetical witness has exactly two
deficient joint maps.

This corollary does not say that all deficient branches are empty.  With
three or more deficient labels, the kernel supports, surviving open-port
count, effective permanent order, and target support change.  That is the
next parent obligation.

## Replay evidence

The following commands were rerun in the isolated working tree:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py
```

The primary symbolic replay checked both scalar cofactors, the matching
identity, the four-dimensional common pair image, its two-dimensional
annihilator, the rank-two target slice, and the totally isotropic zero chart.
Its first draft incorrectly divided the monomial `PB` by two; the independent
representation exposed that checker normalization error, and the corrected
primary replay passes.  The factor two belongs to `S_0^2`, not to `PB`.

The independent standard-library audit found exactly 96 `F_3` scalar
hierarchy solutions with `H!=0`, tested 50,544 distinct-normal orientation
trials with zero compatible off-shells, and tested 12,500 common-hyperplane
orientation trials over `F_5`.  Of 104 off-shell-compatible trials, none had
a nonzero rank-one target slice.  Compilation and Ruff checks passed.  These
programs audit finite and displayed algebra; the same-source, rowspace, and
purity bridges remain the written proof.

Final review status: **PASS for `GLS66`; exactly-two-deficient branch empty;
three-plus-deficient branch and global Krenn--Gu conjecture UNRESOLVED.**
