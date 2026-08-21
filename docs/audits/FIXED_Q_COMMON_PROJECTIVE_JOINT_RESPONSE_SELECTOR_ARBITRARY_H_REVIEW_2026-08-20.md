# Fixed-Q arbitrary-h common projective selector hostile review -- 2026-08-20

## Verdict

**Accepted for the exact conditional scope stated below, subject to the frozen
hashes recorded before publication.**  The strengthened `GLD16` result is an
exact characteristic-zero common-projective operator-supply criterion and an
arbitrary-residual-scalar shifted `GLD3` detector.  It removes the old `h=0`
restriction from this conditional detector.  It does not force a common line,
force three-colour selected-response activity, cover zero or unequal-slope
operator spaces, integrate a formal response fixture into the witness locus,
or imply a permanent restriction.  The maximum-root surplus-two
supply-and-target node remains **OPEN**, and the global Krenn--Gu conjecture
remains **UNRESOLVED**.

The earlier
[2026-08-17 review](FIXED_Q_COMMON_PROJECTIVE_JOINT_RESPONSE_SELECTOR_REVIEW_2026-08-17.md)
remains the frozen review of the `h=0` version.  This review audits the
strengthening rather than rewriting that historical evidence.

## Owning normalization and quantifiers

For one graph, one residual pair `Q`, one fully specified contraction, and one
globally fixed `M/Z` coefficient plane, `GLD15` gives the labelled physical
layers

```text
M_e=B_e,                    Z_e=h B_e+K_e,
M_U=C(B),                   Z_U=h C(B)+X(B,K).
```

The scalar `h` and channel `K` are common physical data for all six pair
targets and the four-port target.  They are not chosen or normalized target by
target.  A nonzero common vector `(delta,eta)` in the intersection of the
seven exact operator spaces gives seven target-specific constant functionals,
but the graph, `Q`, contraction, bases, coefficient axes, and vector are the
same throughout.

Put

```text
a=delta+h eta,
D_e=delta M_e+eta Z_e=a B_e+eta K_e,
T'=delta M_U+eta Z_U=a C(B)+eta X(B,K).
```

This is a selected physical response package in the precise `GLD15` operator
sense.  It is not a new labelled deck summand and does not assert that varying
the projective vector produces a same-graph fibre.

## Denominator-free identity

For each complementary edge pair `{e,f}`, direct expansion gives

```text
(aB_e+eta K_e)(aB_f+eta K_f)
 =a^2 B_eB_f+a eta(B_eK_f+K_eB_f)+eta^2 K_eK_f.
```

Summing the three complementary matchings and subtracting
`C(eta K)=eta^2 C(K)` proves

```text
a T'=C(D)-C(eta K).
```

This is polynomial in `delta,eta,h`.  No division by `a`, `h`, `delta`,
`eta`, a response coordinate, an activity product, or a module minor occurs.
The corrected array `eta K` retains the two-shore physical factorization, so
every one-port flattening of `C(eta K)` has rank at most two.

The two effective-scalar cases are exhaustive and do not require a principal
open:

1. On `a=0`, equivalently `[delta:eta]=[-h:1]`, the selected pair array is
   `D=eta K`.  Three-colour activity makes the selected `3 x 3` submatrix of
   `C(D)` invertible, contradicting its rank-at-most-two bound.
2. On `a!=0`, if all nine displayed mixed entries of `T'` vanished, the same
   selected submatrix of `C(D)-aT'` would be invertible and rank at most two.
   Hence one selected mixed coefficient is nonzero.  Legal target attachment
   makes every such mixed selected coefficient zero on a GHZ witness.

At `h=0`, the divisor `a=0` is the pure-`Z` axis.  At `h!=0`, pure `Z` has
`a=h eta` and enters the nine-word case; the projective divisor rotates to
`[-h:1]`.  The proof handles both without silently preserving the old axis
description.

## Hostile gate and case-cover audit

The theorem's conditional branch cover is exact:

```text
common operator intersection nonzero
 + three-colour pair-depth activity
 -> {a=0 rank contradiction | a!=0 mixed selected coefficient}.
```

It is not a source-witness case cover.  A zero operator space, incompatible
rank-one slopes, missing selected-response activity, response-invisible
operator lines, and every exceptional nuisance-rank fibre remain outside the
hypotheses.  The theorem therefore cannot be cited as maximum-root node
closure or as an exclusion of the complete `k=0,1,2` ledger.

The existing unequal-slope three-active fixture and common-line two-active
fixture remain valid hostile controls.  They occur at `h=0`, which is a
literal fibre of the arbitrary-`h` theorem, so they continue to prove that
synchronization and activity cannot be dropped from a universal statement.
They are response-algebra fixtures, not legal module-selector realizations or
hypothetical witnesses.

No augmented `GLD2` weight, alignment, or target-pure-anchor gate is used by
this chosen `GLD15`/`GLD16` entry.  Full-nuisance legality, common-line
synchronization, and selected-response activity are load-bearing and remain
explicit.

## Independent checks and frozen hashes

The focused primary uses exact SymPy polynomial and determinant arithmetic.
The no-import audit imports neither SymPy nor the primary verifier; it uses a
separate sparse polynomial dictionary and direct complementary-matching
enumeration.  It independently checks the arbitrary-`h` identity and the
effective-scalar divisor before replaying the existing controls.

Frozen against base HEAD `4e98a75c6e596f36e0c1b7e05f5d1b0e3c00095e`:

```text
theorem  f3cd365706d08a8976d60d6f0d2f4b34da829cd83a869e24e8a48a8601985ba0
primary  16e08d0d3d0793eed24785ad0c9f53bc43bf60c56300b85b190519fe90e7f907
audit    5d05a832a6309fae28076dd6d8ac1dc870acbff705595f2dee4727b0955d3061
```

Required focused commands:

```powershell
python claims/arbitrary-order/verify_fixed_q_common_projective_joint_response_selector.py
python -I claims/arbitrary-order/audit_fixed_q_common_projective_joint_response_selector.py
python -m py_compile claims/arbitrary-order/verify_fixed_q_common_projective_joint_response_selector.py claims/arbitrary-order/audit_fixed_q_common_projective_joint_response_selector.py
```

The scripts audit bounded polynomial identities and controls.  The written
`GLD15` operator-space equivalence and the arbitrary-field determinant
argument remain load-bearing.

## Exact remainder

Still **UNKNOWN**: forcing a nonzero common coefficient line on any required
maximum-root witness window; forcing three-colour pair-depth activity for its
selected pair package; excluding zero spaces, unequal rank-one slopes,
response-invisible rows, and all nuisance-rank-drop fibres; integrating the
root-order-three and root-order-at-least-five source interfaces into a named
downstream detector; and every permanent consequence.
