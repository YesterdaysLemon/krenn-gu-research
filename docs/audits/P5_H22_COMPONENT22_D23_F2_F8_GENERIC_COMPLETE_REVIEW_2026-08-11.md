# Review: component 22 finite-`D23` `H=f2=f8=0` generic closure

## Verdict

**PASS at the stated generic scope.**  The package gives a written
characteristic-zero rank argument over `Q(A,R,D)`, a focused verifier bound to
the repository model, and a no-repository-import audit that reconstructs the
model and determinants independently.  It closes the whole generic
`H=f2=f8=0` finite-`D23` intersection, including the named isolated
`2h3+s!=0` complement.  It does not close pointwise parameter divisors, the
remaining `f2=0` residual, component 22, P5, or the global conjecture.

The global Krenn--Gu status remains **UNRESOLVED**.

## Claim reconstruction

The reviewed claim has four load-bearing steps:

1. a genuine weighted binary extension must give a nonzero vector in the
   kernel of the fourteen-by-eight mixed coefficient matrix, so every maximal
   minor must vanish;
2. on `H=f2=f8=0`, one fixed maximal minor is a coefficient-field unit times
   one linear polynomial in `h0` and therefore forces a unique `h0`;
3. after that substitution, two other fixed maximal minors are units times
   `L9` and `L13`, both linear in `h3`;
4. `L9-s*L13` is a nonzero element of `Q(A,R,D)`, equivalently their
   `h3`-resultant is nonzero, so the rank-drop system is empty.

All coefficients lie in `K`, and the nonzero unit factors and incompatibility
remain nonzero after every field extension `E/K`.  Thus the same argument
excludes geometric generic points, not only `K`-rational points.  This does
not turn the nonzero factors in the determinant prefactors into pointwise
hypotheses or closures; their zero loci remain special-fibre obligations.

## Adversarial checks

| attack | result |
|---|---|
| Hidden division by `rho` or `rho+1` | The package solves `f8=0` and checks `rho+1=2A/(AD+A+DR)`; both are nonzero rational functions in the component field. |
| Rational sampling substituted for a proof | Rejected.  Samples were used only during discovery.  Both accepted replays verify full symbolic determinant identities over `Q(A,R,D)`. |
| Equality divisor silently omitted | Rejected.  No division by `2h3+s` occurs.  The result closes both `2h3+s=0` and its complement at the generic point. |
| A maximal minor proves too much | Rejected.  The mathematical bridge used is only the necessary kernel/rank condition for a binary extension.  Rank eight excludes this scoped lift; it is not promoted to a global statement. |
| `K`-rational emptiness confused with geometric emptiness | Rejected.  The forced-`h0` identity and nonzero `h3` incompatibility persist after every field extension of `K`. |
| Algebraic exceptional factors treated as constants | Rejected pointwise.  They are units only in `Q(A,R,D)`; the theorem explicitly leaves all specializations open. |
| Primary and audit accidentally share an implementation | Rejected.  The primary imports the repository's exact component model and uses `DomainMatrix`; the audit imports no repository code, rebuilds permanent coefficients, and uses explicit Gaussian elimination. |
| Existing slope-intersection owner overwritten | Rejected.  The earlier theorem is preserved as lineage and an independently useful two-minor certificate; the new theorem strictly contains its generic cell without changing special-fibre status. |
| Component or global status inflated | Rejected.  The remaining `f2=0` branches, component 22 special/projective/source fibres, P5, gluing, and the global conjecture remain open. |

## Evidence replay

The focused commands are:

```powershell
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-f2-f8-generic-complete/verify_p5_h22_unequal_complement_common_kernel_component_d23_f2_f8_generic_complete_obstruction.py
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-f2-f8-generic-complete/audit_p5_h22_unequal_complement_common_kernel_component_d23_f2_f8_generic_complete_obstruction.py
```

Acceptance requires both to print `"status": "PASS"`, the same nonzero exact
resultant, `pointwise_special_fibres_closed: false`,
`remaining_f2_residual_closed: false`, and
`global_conjecture_resolved: false`.

## Publication boundary

The accepted live consequence is exactly:

```text
generic component 22 finite-D23 H=f2=f8=0: EMPTY.
```

The next component-22 work is the remaining finite-`D23` `f2=0` residual and
the special/projective/source boundaries.  No successor research lane is
selected by this review.
