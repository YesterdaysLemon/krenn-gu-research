# Maximum-root surplus-two promoted all-target transverse-quotient hostile review -- 2026-08-20

## Verdict

**PASS for the exact quotient equivalence and failure reduction.  Strategic
node closure remains OPEN.**

The theorem correctly replaces the collapsed GLS20 maximum-root image with a
quotient by the uncontracted all-port nuisance line.  On the already-required
`p!=0` gate, the operator

```text
P=pI-q tensor epsilon_A
```

has kernel `Kq` and image `ker epsilon_A`.  Since `q tensor V_C^*` is contained
in the complete nuisance, this gives an exact equivalence between the full
`GLS8` selector quotient and its projected transverse quotient.  It loses no
upstairs selector and introduces no new divisor.

The theorem does not prove transverse survival, response nonvanishing,
simultaneous attachment, activity, or a downstream detector.  The global
conjecture remains **UNRESOLVED**.

## Scope audited

The review checked

- [`GLS22` owning theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md);
- [`GLS8` promoted module](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md);
- [`GLS21` all-port collapse](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_BASE_SHADOW_ALL_PORT_NUISANCE_COLLAPSE_THEOREM.md);
- the focused primary verifier; and
- the independent standard-library no-import audit.

No external literature claim is used.

## Load-bearing algebra

Write `E=E_A^*`, `q=G_Q^A(z_Q)`, `epsilon=epsilon_A`, and
`p=epsilon(q)`.  Direct calculation gives

```text
P(q)=0,
epsilon P=0,
P^2=pP.
```

On `D(p)`, `Pv=0` implies `v=p^(-1)epsilon(v)q`, while every
`v in ker epsilon` obeys `Pv=pv`.  Hence

```text
ker P=Kq,             im P=ker epsilon.
```

For a target left space `L_C=E tensor V_C`, tensoring makes the kernel
`q tensor V_C`, exactly the retained all-port nuisance submodule.  If
`P(g_C)=P(n)` for `n` in the complete nuisance, then `g_C-n` lies in that
kernel and therefore in the nuisance.  This proves full survival if and only
if transverse survival.

The selector formulas are also exact.  A transverse functional `mu` with
`mu(PN)=0` and `mu(Pg)=p` gives `lambda=p^(-1)mu P`.  Conversely a legal
`lambda` kills the all-port kernel, so `mu(Pv)=p lambda(v)` is well-defined.

Applying `P` to the complete target gives the stated pure columns

```text
(p r_c-kappa_c q) tensor v_(C,c),
```

and the decomposable target identity.  The all-rank Fitting argument is then
the same geometric rank-rise argument on `72` rows (or `8` for the top target).

## Hostile assertions

1. **The theorem deletes the all-port nuisance.**  False.  It quotients by its
   exact uncontracted coefficient submodule, already contained in the complete
   nuisance.

2. **The projector is the collapsed maximum-root contraction.**  False.
   `P` retains the eight probe-root directions transverse to `q`; the collapsed
   GLS20 map retained only the one maximum-root scalar direction.

3. **`P` is an idempotent over the Laurent ring.**  False and not claimed.
   The denominator-free identity is `P^2=pP`.  It becomes a projection only
   after localization at the declared unit `p`.

4. **A new generic denominator is introduced.**  False.  `p!=0` is already
   part of the GLS4/GLS6 common source gate and the GLS8 useful locus.

5. **The quotient equivalence proves only one implication.**  False.  The
   kernel is contained in the nuisance, so projected absorption lifts back to
   full absorption exactly.

6. **A transverse selector may fail to be legal upstairs.**  False.  Formula
   `lambda=p^(-1)mu P` annihilates the entire complete nuisance, not merely the
   all-port block.

7. **Every legal upstairs selector is missed by the transverse quotient.**
   False.  Every legal selector kills the all-port kernel and factors uniquely
   through `P` after the stated normalization.

8. **The top all-port target is omitted.**  False.  It is the `C=empty` case;
   its left dimension drops from nine to eight.  The top-minus-two targets drop
   from `81` to `72`.

9. **The target pure columns are simply `p r_c`.**  False.  The correction
   `-kappa_c q` is load-bearing and makes every column transverse to
   `epsilon_A`.

10. **Pure transverse rank one is assumed.**  False.  It follows only on the
    complete GHZ target from the decomposable right side.

11. **Transverse survival alone gives a useful row.**  False.  The physical
    response may vanish; the theorem keeps this failure branch explicit.

12. **The Fitting criterion covers only the generic transverse rank.**  False.
    It ranges over every minor size through `72` or `8`, with the `hp` gate
    retained and no division by a rank minor.

13. **The source aggregate `T_Q!=0` proves quotient survival.**  False.  It
    proves only some raw `t_C` is nonzero.  Complete projected nuisance may
    still absorb it.

14. **Aggregate synchronization implies every term is synchronized.**  False.
    `pF_Q=q tensor Pi_Q` may arise by cancellation.  Termwise identities are
    asserted only under the stronger hypothesis that every `t_C` vanishes.

15. **At `r=3` the seven rows are attached simultaneously.**  False.  All
    seven individual target quotients are reduced exactly, but common selector
    synchronization and three-colour activity remain unproved.

16. **At `r=4` these targets are the original GLD16 package.**  False.  They
    are fifteen promoted four-port targets plus a promoted six-port target in
    the two-probe chart.

17. **The theorem establishes projective synchronization across every target.**
    False.  It defines the exact source aggregate fork; neither branch is
    excluded or promoted to a common legal package.

18. **The theorem closes the strategic node or affects global status.**  False.
    Survival, response, activity, downstream shape, and original-chart
    coexistence remain open.  Global status is **UNRESOLVED**.

## Verification independence

The primary verifier uses exact SymPy matrices, Kronecker projectors,
constructive selector recovery, exhaustive small Fitting tables, and a tensor
source aggregate.  The independent audit imports neither SymPy nor repository
code; it implements the transverse map coordinatewise, uses hand-written
`Fraction` elimination, exhausts small quotient states, and assembles the
source identity independently.

The audit initially placed its test `q` on `p=0`; it failed as it should.  The
fixture was moved to `p=1`, after which both paths pass.  This confirms rather
than hides the localization boundary.

## Open boundary

The promoted problem is now an exact `72/8`-row all-target failure problem on
the physical source gate.  The next proof must contradict simultaneous
transverse absorption/response zero using complete mixed GHZ coefficients, or
produce a shared useful family satisfying every named detector gate.  Raw
nonvanishing of `T_Q` would still be only the first of those gates.

Strategic node: **OPEN**.  Global conjecture: **UNRESOLVED**.
