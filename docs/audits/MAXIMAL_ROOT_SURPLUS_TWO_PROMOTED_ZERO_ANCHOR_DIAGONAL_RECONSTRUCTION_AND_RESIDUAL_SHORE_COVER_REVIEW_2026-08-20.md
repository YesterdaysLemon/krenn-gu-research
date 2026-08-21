# Hostile review: promoted zero-anchor diagonal reconstruction and residual-shore cover

## Review decision

**Accept as the exact scoped theorem `GLS26`.**  The theorem validly sharpens
the zero-anchor branch of `GLS23`: the complete top-target equation forces a
two- or three-dimensional projected diagonal space into the remaining exact
physical nuisance, while every one-residual label is confined to a canonical
projected tangent of dimension at most seven.  Quotienting by that tangent
gives the exhaustive essential-pair versus coordinate-shore-cover split.

This review does **not** accept any of the following stronger statements:

- that the essential pair slice survives the complete nuisance of the pair's
  own target;
- that its physical response is nonzero;
- that the coordinate-shore cover is impossible on a witness;
- that the six pair targets synchronize or satisfy three-colour activity;
- that an `r>=4` downstream detector accepts this raw high-depth row; or
- that the maximum-root supply-and-attachment node or the global conjecture
  is closed.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Source and typing audit

The theorem uses one actual `GLS4` source pair `Q`, one actual probe pair
`A`, and the promoted partition of `GLS8`.  The retained gate is exactly

```text
p=epsilon_A(G_Q^A(z_Q))!=0.
```

No generic incidence minor or response coordinate is added.  In particular,
`p!=0` implies `q!=0`, so the use of `ker P_Q=Kq` is legal on every declared
point.

For two open roots, the evaluated `D=Q` companion is exactly

```text
q=xi_0^0 tensor xi_1^1+xi_0^1 tensor xi_1^0.
```

This is a matching bijection, not an assumed rank-two normal form.  Each
shore span has dimension one or two: if either were zero, `q` and hence `p`
would vanish.  Rank-one shores and proportional residual incidences are
therefore retained.

## 2. Residual-tangent audit

For `D={q_s,u}`, the only two matchings send the two roots to `q_s,u` in the
two possible orders.  After evaluating `q_s`, every port slice has the form

```text
xi_0^s tensor ell_1+ell_0 tensor xi_1^s.
```

It lies in

```text
T_Q=X_0 tensor V_1^*+V_0^* tensor X_1.
```

No label contained in `Uhat` is included in this assertion.  Thus the proof
does not silently classify genuine pair labels as residual-singleton labels.

The dimension calculation is exact:

```text
dim T_Q=3d_0+3d_1-d_0d_1,
T_Q intersect ker P_Q contains exactly Kq,
dim P_Q(T_Q)=3d_0+3d_1-d_0d_1-1.
```

At `(d_0,d_1)=(2,2)` this is seven, not eight.  At `(1,1)`, `(1,2)`, and
`(2,1)` it is respectively four, six, and six.  The proof uses only
`ker P_Q=Kq` and `q in T_Q`; it does not assume `P_Q` is an ordinary
idempotent rather than the scaled identity `P_Q^2=pP_Q`.

## 3. Projected diagonal audit

Let `D_A` be the three-dimensional coordinate-diagonal root space.  The
restriction of `P_Q` to `D_A` has kernel

```text
D_A intersect Kq.
```

It is zero when `q` is nondiagonal and one-dimensional when `q` is diagonal.
Consequently the projected diagonal rank is exactly three or two.  The
argument includes diagonal `q` of matrix rank one or two and makes no claim
that `q` is generically nondiagonal.

## 4. Complete-nuisance and target-equation audit

For the top target, the `GLS23` formula sums over every pair
`D subset Bhat`.  The cases are exhaustive:

1. `D=Q`, whose transverse contribution is zero;
2. `|D intersect Q|=1`, the one-residual family; and
3. `D subset Uhat`, the genuine promoted pair family.

There is no fourth case for a two-element label.  Hence

```text
N_empty^tr=N_empty^(1)+N_empty^(2)
```

is the complete nuisance, not a selected ledger.

On `omega=0`, the desired side of the `GLS22` top-target quotient vanishes.
The residual colour coefficients `alpha_c` are nonzero on the fixed fully
supported contraction, and the three pure tensors on `Uhat` are independent.
Coefficient comparison therefore puts each `P_Q(r_c)` in the exact nuisance.
This implication is pointwise and does not divide by a response or nuisance
minor.

The review checked a possible quantifier inflation here.  The proof uses the
complete hypothetical-witness tensor identity as the source of the quotient
equation.  Its conclusion concerns the three pure right-factor coefficients;
it does not claim that checking those three coefficients alone would certify
a witness.

## 5. Shore-cover equivalence audit

Because `q in T_Q`, quotienting by `P_Q(T_Q)` gives the same diagonal defect
as quotienting `D_A` by `T_Q`.  The annihilator is exactly

```text
T_Q^perp=X_0^perp tensor X_1^perp.
```

The coordinate diagonal `r_c` pairs with `v_0 tensor v_1` as
`v_0(c)v_1(c)`.  Therefore all diagonal rows lie in `T_Q` if and only if, for
each colour, one coordinate evaluation vanishes on an entire annihilator.
Finite-dimensional double annihilation gives exactly

```text
e_(a_0,c)^* in X_0 or e_(a_1,c)^* in X_1.
```

This equivalence includes the cases where both shores contain the same
coordinate line, where one shore has rank one, and where one or both shore
planes are noncoordinate away from the required covered axes.

For rank-two shores, normals are unique projectively and the condition becomes
`n_0(c)n_1(c)=0` for all three colours.  This is homogeneous and does not
choose a nonzero coordinate chart.

The low-rank corollary is also exact.  Two one-dimensional shores can contain
at most two independent coordinate lines, so `(1,1)` is always in the
essential-pair branch.  If the shore ranks are `(1,2)` and cover all three
lines, capacity is tight: the first shore is a coordinate line and the second
is the complementary coordinate plane.  The transpose case is identical.

## 6. Essential-pair semantics

When the diagonal defect is positive, exact reconstruction says that the
images of the genuine pair slices span it.  Hence at least one pair slice is
nonzero modulo `P_Q(T_Q)`.  Since a zero tensor has only zero slices, its
desired coefficient `t_D` is nonzero.

The hostile boundary is important:

```text
Slice_D(t_D) notsubset P_Q(T_Q)
```

does **not** imply

```text
t_D notin N_D^tr.
```

The first quotient removes a source-independent residual tangent inside the
top-target root space.  The second is the complete nuisance quotient of the
different pair target.  The theorem and frontier documentation preserve this
type distinction.

## 7. Exact exceptional fibres

No principal-open shore chart is declared.  The integer defect

```text
e_Q=dim((D_A+T_Q)/T_Q)
```

handles all shore ranks and every coordinate-minor drop.  The zero defect is
not dismissed as nongeneric; it is retained as the coordinate-shore-cover
branch.  The theorem also retains:

- diagonal and nondiagonal `q`;
- rank-one and rank-two residual shore spans;
- every overlap of the coordinate assignments;
- every response-zero fibre; and
- every rank drop in the pair target's own nuisance, which is not analyzed.

## 8. Verification independence

The primary verifier uses SymPy matrices and directly checks:

- tangent and transverse-tangent ranks;
- `P_Q(q)=0`, `epsilon_A P_Q=0`, and `P_Q^2=pP_Q`;
- the two/three projected diagonal ranks;
- equality of pre- and post-projection defects;
- the matching formula for all six one-residual/port-coordinate slices in
  each fixture; and
- both the essential-pair and shore-cover branches.

The independent audit imports no repository helper or primary verifier.  It
uses standard-library `Fraction`, a separate Gaussian elimination and
nullspace implementation, different rational fixtures, and the dual
Hadamard-zero criterion.  Both scripts are finite mechanism audits.  The
arbitrary-root result is supplied by the written label partition and matching
proof, whose root-space calculation is independent of `r`.

## 9. Dependency replay and publication gate

Before publication, replay:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_all_port_transverse_quotient_and_projective_synchronization_failure.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_all_port_transverse_quotient_and_projective_synchronization_failure.py
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_transverse_complete_nuisance_decomposition_and_top_anchor_dichotomy.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_transverse_complete_nuisance_decomposition_and_top_anchor_dichotomy.py
```

The full candidate-tree gate remains the repository contract.  Hosted CI must
run at the exact pushed head before merge.  A green merge establishes only
`GLS26` with the scope above.

## Final scope ledger

```text
zero-anchor diagonal reconstruction:                  ACCEPTED;
residual-singleton tangent bound:                     ACCEPTED;
essential-pair / coordinate-shore-cover split:       ACCEPTED;
pointwise exceptional-fibre coverage for this split: ACCEPTED;

essential pair legal survival or response:           OPEN;
coordinate-shore-cover exclusion:                    OPEN;
common package, synchronization, and activity:       OPEN;
maximum-root supply/attachment node:                 OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```
