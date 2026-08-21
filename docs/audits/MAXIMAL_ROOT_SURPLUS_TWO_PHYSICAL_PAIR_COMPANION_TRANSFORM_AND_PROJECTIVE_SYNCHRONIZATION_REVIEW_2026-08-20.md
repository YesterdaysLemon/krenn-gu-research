# Hostile review: maximum-root physical pair-companion transport

Date: 2026-08-20

Base: `origin/main` at `5381f07a49de24e2825c4fc952426c2a0cb31a3a`

## Verdict

**PASS for the exact scoped arbitrary-root companion-exchange, projective
quotient-kernel, cross-target determinant, and complete-target identities.
FAIL as a closure claim for the maximum-root supply/attachment node.**

The proof correctly identifies, for every pair target, one common physical
partial-matching transform `Psi_C` whose inputs are the actual root-edge array
`R` and the residual-induced array `K^Q`.  The rank-one line/kernel orientation
is correct, both projective axes are included, and the target-coupled identity
uses no division.  The result does not prove that a foreign absorbed direction
belongs to another target's complete nuisance space.  It also leaves joint
rank zero, missing activity, the `r=4` four-port line, and the lack of a named
arbitrary-order downstream package open.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Postmerge interface correction

The initial review missed one proof-DAG error: it accepted a dependency note
identifying the original arbitrary-`r` pair targets with the top-minus-two
targets of `GLS8`.  That identification is false.  GLS15 uses `r` roots,
`r` ports, and `|S|=2`; GLS8 repartitions the graph into two probe roots,
`2r-2` promoted ports, and `|S|=2r-4`.  The matching identities and quotient
proofs below are unaffected, but they do not integrate GLS8.  The live DAG,
claim provenance, README, and scope ledger are corrected in the follow-up
erratum tranche.  This review explicitly fails the former dependency claim.

## Frozen reviewed artifacts

The following LF-normalized SHA256 hashes were computed after the focused
scripts and Ruff checks passed and before the corrected publication:

```text
34bd68315c060fa6e957d261fd860c355d62dbb453973bcd4580e36326db4810
  claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PHYSICAL_PAIR_COMPANION_TRANSFORM_AND_PROJECTIVE_SYNCHRONIZATION_OBSTRUCTION_THEOREM.md

d6c8cc3773647ee1b7079697936f7c41f5e459c252d16c95b5160b5ac8cf22bd
  claims/arbitrary-order/verify_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py

1032592656f5c5389fc199e366643d18ddf840d48f3bb1571419347e25c7107e
  claims/arbitrary-order/audit_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py
```

## Mathematical review

### 1. Matching multiplicities and complement orientation

For a pair target `S`, `C=U-S` has size `r-2`.

- A term of `G_C` has exactly one root--root edge and a bijection from the
  remaining roots to `C`.  This is exactly one term of `Psi_C(R)`.
- A term of `G_(Q union C)` sends every root outside.  The preimage of `Q` is
  one root pair, its two residual orientations give the two summands of
  `K_ij^Q`, and the other roots are bijected to `C`.  This is exactly one term
  of `Psi_C(K^Q)`.

There is no factor of two and no complementary-root-pair involution missing.
The proof keeps labelled tensor slots, so commutative monomial shorthand in
the verifier is evidence for multiplicity only, not a replacement for the
tensor proof.

### 2. Selector line versus absorbed direction

At joint rank one, write

```text
bar g_M=delta_S bar g_S,
bar g_Z=eta_S bar g_S.
```

The accessible operator row is therefore `(delta_S,eta_S)`, while the column
kernel vector is `(-eta_S,delta_S)`.  Since `g_M=Psi_C(K^Q)` and
`g_Z=Psi_C(R)`, the absorbed physical array is correctly

```text
delta_S R-eta_S K^Q.
```

This orientation was attacked explicitly because exchanging `R,K^Q` or using
the operator row itself as the column-kernel vector would reverse the theorem.
The displayed calculation and both verifiers agree.

### 3. Cross-target determinant

For another line `(delta_T,eta_T)`, linearity gives

```text
[Psi_(C_S)(delta_T R-eta_T K^Q)]
 =(delta_T eta_S-eta_T delta_S)bar g_S.
```

Because `bar g_S` is nonzero, this class vanishes exactly when the two
projective lines agree.  The connected comparison-graph criterion is then
only transitivity of equality; it does not infer any unproved transport map.

### 4. Complete-target identity

The complete joint quotient equation has left side supported only on the
active pure target words.  Since the quotient generator is nonzero, the
selected response is diagonal and coefficient comparison gives

```text
alpha_c[d_(S,c)]=D_S(c,c)bar g_S.
```

Multiplication by the cross determinant proves the target-coupled identity.
No `alpha_c`, selected response value, determinant, slope coordinate, or
incidence minor is inverted.  Nonzero consequences are asserted only after
the relevant factors are declared nonzero.

## Adversarial scope and case-cover audit

The following attempted overextensions were rejected:

1. **Raw transform injectivity is synchronization.**  False.  Synchronization
   is membership of a cross transform in the complete target-dependent
   nuisance quotient.  A generic inverse for raw `Psi_C` does not prove it.
2. **Own-target absorption transports automatically.**  Not proved.  The
   nuisance spaces for different targets remove different labelled columns.
   Equation (15) names the transport defect; it does not kill it.
3. **Rank one covers all operator spaces.**  False.  Rank two already supplies
   separate selectors; rank zero has no projective line and remains open.
4. **Response zero is harmless.**  False.  The module determinant identity
   survives, but the target-coupled nonzero class requires selected-response
   activity.
5. **Projective axes were divided away.**  False.  `delta=0` and `eta=0` are
   explicit branches of the homogeneous quotient-kernel identity and are
   replayed independently.
6. **Incidence rank-drop fibres are excluded.**  False.  The matching identities
   hold there without division; the needed foreign-nuisance membership is
   still open on those fibres.
7. **Six pair lines supply GLD16.**  False.  At `r=4`, the four-port desired
   companions are quadratic matching expressions and its operator line still
   has to exist and agree.  GLD16 activity is separate.
8. **Arbitrary-root pair rows are a downstream package.**  False.  The source
   identity is arbitrary-root, but no named committed theorem accepts only
   these rows at `r=3` or `r>=5` as the complete required interface.
9. **The pair rows are the promoted GLS8 rows.**  False.  The two partitions
   have different root counts, port counts, target sizes, companion grades,
   and nuisance modules.  GLS8 remains an independent source obligation.
10. **A finite replay proves the arbitrary-root theorem.**  False.  The proof is
   the all-`r` matching bijection.  Orders through seven and eight are bounded
   exact audits only.
11. **The result changes global status.**  False.  It neither produces a
    permanent restriction nor excludes every source point.

The theorem therefore changes the live frontier only by replacing an informal
"projective faithfulness/synchronization" request with one exact physical
quotient class and one exact target identity.  It does not close a branch of
the full pointwise source cover.

## Verification independence

The primary verifier expands labelled matching monomials in two ways:
partial root matching versus direct root-to-outside bijection.  It checks every
pair target through root order seven and uses SymPy only for the separate
homogeneous quotient and target identities.

The independent audit imports no project code or primary verifier.  It uses a
different canonical description: every root-to-`Q union C` bijection is decoded
to a residual root pair, an orientation bit, and a root-to-`C` map, then
round-tripped.  It checks all pair targets through root order eight.  Its
projective replay uses exact `Fraction` arithmetic and includes pure `M`, pure
`Z`, finite slopes, and connected three-line comparisons.

These are genuinely different representations.  Neither audit checks a
support atlas or claims exhaustive witness search.

## Reproduction record

The following focused commands passed at the frozen hashes:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py claims/arbitrary-order/audit_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py claims/arbitrary-order/audit_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py claims/arbitrary-order/audit_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py
```

The publication candidate must additionally pass the repository's
index-complete validation floor and exact-head hosted CI.

## Exact remainder

The next proof-producing obligation is one of:

1. prove the foreign transport membership
   `Psi_(C_S)(A_T) in N_(C_S)^J` from a support-free physical
   companion-exchange/module syzygy, including exceptional fibres; or
2. use the nonzero identity with `[d_(S,c)]` to isolate a complete mixed GHZ
   contradiction whenever two active rank-one lines differ.

That work must be combined with a pointwise treatment of `k=0`, selected
response zero, the `r=4` four-port line, and the promoted `r=3`/`r>=5`
downstream-package boundary before the strategic node can be called closed.
