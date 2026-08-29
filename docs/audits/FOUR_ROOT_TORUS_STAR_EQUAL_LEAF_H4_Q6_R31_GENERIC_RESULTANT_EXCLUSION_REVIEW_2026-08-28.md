# GLD96 hostile review: generic R31 resultant localization

> **Historical scope note (2026-08-29).**  This review records the narrower
> first publication.  Its treatment of `R31` as a localization gate is
> superseded by the exact
> [R31 gate-removal review](FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_R31_GATE_REMOVAL_REVIEW_2026-08-29.md),
> which leaves the original determinant/resultant evidence intact and expands
> the proved open only to `D(E31*H2*g0*Delta)`.

## Disposition

**Accepted as a scoped exact localization, with the exceptional factors
retained.**  The package proves that four selected R31 bordered seven-minors
force the GLD88 offsets `B=C=0` on
`D(R31*E31*H2*g0*Delta) intersect V(Q6)`.  GLD95 then supplies the separate
F88 finite-residual exclusion on `D(Delta)`.  This is not a closure of the
R31=0/double-pivot branch, the E31/g0/H2 exceptional strata, arbitrary H4
points outside the F88 offset domain, or the global conjecture.  The global
status remains **UNRESOLVED**.

## Evidence inspected

The primary verifier
`claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_r31_generic_resultant_exclusion.py`
reconstructs the fixed GLD71 `37 x 9` syndrome over `Q` and checks:

1. the raw R31 pivot and all four selected seven-minors, including their
   reduced denominators, term counts, degrees, and pinned `srepr` hashes;
2. all `111` GLD88 common block-kernel identities, which provide the exact
   `B`-divisibility at the F88 offset origin;
3. the exact specialization `(p,a)=(2,3)` on
   `Q6=5q^4-4q^3+12q^2-16q+8`, with all four residual supports;
4. the two B-cross-resultants, their primitive q-coefficient tuple and hash,
   and the nonzero resultant norm against Q6; and
5. the first C-coefficient at `B=0` and its separate nonzero Q6 norm.

The independent audit
`claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_r31_generic_resultant_exclusion.py`
does not import the primary or GLD88.  It transcribes the written F88
functions locally, accumulates the syndrome entries directly from the pinned
GLD71 sparse supports, and computes the bordered determinants by a Bareiss
elimination in `Q(q)[B,C]`.  It repeats the Q6 reduction, resultant, and both
norm checks.  The primary instead uses the GLD71 matrix builder and an
adjugate/Schur identity, so the determinant representation and arithmetic
route differ materially.

Both scripts share the fixed sparse relation supports and the stated F88/Q6
formulae as mathematical inputs.  Neither re-proves the GLD75/GLD86
incidence bridge or GLD95's all-factor F88 theorem.

## Adversarial checks

### Generic versus pointwise scope

The specialization `(p,a)=(2,3)` is used only to prove that the generic
cleared resultant factors `E31` and `g0` are not identically zero.  It does
not prove that they are nonzero at every parameter point.  The theorem
therefore explicitly localizes at `E31` and `g0`; their zero loci remain open.

### No hidden cancellation

The raw R31 numerator is retained with its factor
`2*(p-q)*(p+q-1)`.  The raw target denominators are powers of `d0`; after
the F88 substitution, all denominators cleared in the offset calculation
depend only on parameters, never on `B` or `C`.  Thus the affine-in-C form
and the B-divisibility are not obtained by cancelling an offset factor.

### Resultant logic

If `B != 0` and all four residuals vanish, cross-multiplication gives
`H_01=H_02=0`.  The cleared q-resultant `E31` is exactly the obstruction to a
common Q6 root, so `D(E31)` forces `B=0`.  At `B=0`, the first equation is
`C*g_0(0)=0`; the separately cleared Q6 norm `g0` makes this coefficient a
unit in the localized finite algebra.  No conclusion is drawn on `H2=0`,
where the q-leading-coefficient reduction is invalid.

### Upstream consequence

After `B=C=0`, the point is on the written F88 family.  GLD95, whose own
scope is explicitly `F88 intersect V(Q6) intersect D(Delta)`, closes its
finite common-minor residual, including the old `P6=0` content fibres.  GLD96
does not silently apply GLD95 to arbitrary H4 points outside F88.

### Double-pivot boundary

The R31=0/double-pivot census and any H-resultant exploration are not used in
the proof.  They remain scoped evidence only; no finite census is promoted
to an exhaustive theorem.

## Accepted residuals and non-claims

| item | review verdict |
| --- | --- |
| `V(Q6,T0,T1,T2,T3) intersect D(R31*E31*H2*g0*Delta)` | contained in F88 by the exact offset/resultant argument |
| the resulting F88 incidence on `D(Omega)` | excluded by the upstream GLD95 theorem |
| `R31=0` / double pivot | open |
| `E31=0` | open; cross-resultant exceptional locus |
| `g0=0` | open; selected C-coefficient loses its unit |
| `H2=0` | open for this theorem; no invalid q-division is used |
| `Delta=0` | outside this localization; only the separately scoped GLD87/89/93/94 pieces apply |
| arbitrary H4 Q6 outside F88 | not covered |
| GLD83 pulled-back Fitting ideal and other charts/components/source branches | open |
| global Krenn--Gu conjecture | **UNRESOLVED** |
