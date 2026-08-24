# Fixed-Q product-selector companion/full-coefficient interface correction review -- 2026-08-24

## Verdict

**FAIL for the live `GLD65` and `GLD66` exclusions; PASS for the exact
correction and counterexample at its stated scope.**

The product-selector row in `GLD15` annihilates evaluated root companions
`G_D`.  The `GLD65` proof instead set a full matching coefficient `F_D` to
zero after direct edges internal to `D` had been restored.  For
`D=Q union {u,v}`, the correct equation is

```text
G_D=0,
F_D=m B_uv,                                             (1)
```

not `F_D=0`.  The claimed cross-Gram identity `J=-mB`, the `GLD65`
three-colour exclusion, and the dependent `GLD66` two-colour and plane-
synchronization conclusions are therefore not live.

The fixture below directly falsifies former GLD65 Theorem 5.  GLD66 wrote the
false full-coefficient zero as an explicit assumption, so the fixture is not
a counterexample to its later algebra conditional on that assumption; rather,
it proves that the legal selector does not supply GLD66's load-bearing input.

No global witness or counterexample was found.  The Krenn--Gu conjecture
remains **UNRESOLVED**.

## 1. Audited interfaces

The review compared the following exact types rather than relying on the
shared letter `F`:

1. `GLS2` defines `G_D` by a root partial matching and a bijection of every
   unused root to `D`; `G_D` contains no outside--outside edge.
2. `GLD15` assigns the deck label `I` the coefficient `G_(B-I)` and defines a
   legal pure-`M` row by annihilation of every label except `I=U`.
3. `GLS17` makes a surviving first-root class into a product evaluation of
   that same legal row.
4. `GLD65` introduces `F_D` as the full perfect-matching coefficient on
   `R union D`, explicitly stratifies matchings with outside--outside edges,
   and then calls `F_D=0` a complete-nuisance consequence.

Items 1--3 imply zero for the root-only coefficient `G_D`; they do not imply
zero for item 4.  The distinction is mathematical, not notational.

## 2. Direct derivation

For a pure-`M` target-`U` row with coefficient `m`, the complete labelled
module gives

```text
G_Q=m,
G_empty=0,
G_D=0 for every other allowed D.                       (2)
```

On four outside vertices, exact matching stratification gives

```text
F_D=G_D+sum_(e subset D, |e|=2) E_e G_(D-e)
        +haf(E[D])G_empty,                              (3)
```

where `E_e` is the evaluated direct outside edge and `E_uv=B_uv` for two
ports.  For `D=Q union {u,v}`, only the term `B_uv G_Q` survives, proving (1).
This is the precise invalid edge in the former proof.

The generic `24+72+9` matching identity replayed by the old verifiers is
correct.  Those scripts did not verify that module nuisance sets the full
coefficient `F_D` to zero.  Independent checking of a correct combinatorial
identity therefore did not audit the load-bearing type substitution.

## 3. Exact physical graph-side counterexample to former GLD65 Theorem 5

The new owning correction supplies one ternary graph with:

- a maximum four-root torus zero set;
- one `GLS17`-factored complete `GLD15` row `(1,0)` for target `U`;
- all `431` scalar entries of the evaluated companion table equal to zero
  except `G_Q=1`;
- six diagonal direct port blocks; and
- `M_U=0000+1111+2222`.

For the selected pair `u_0u_1` in colour zero, its root companion is zero but
its direct-edge times anchor contribution and full coefficient are both one.
This simultaneously checks the hypotheses and falsifies the claimed
cross-Gram conclusion.

The fixture is not a full GHZ witness: its global all-one coefficient is zero
because every root-incident block has zero `(1,1)` entry, while the target
coefficient is one.  Being off the witness locus is irrelevant to the
conditional module theorem as stated; additionally, the false cross-Gram
lemma was asserted before any witness-only conclusion.  A future witness-only
theorem would require a new target equation that actually kills `F_D`.

## 4. Independent evidence

Run:

```powershell
python claims/arbitrary-order/verify_fixed_q_product_selector_companion_full_coefficient_separation.py
python -I claims/arbitrary-order/audit_fixed_q_product_selector_companion_full_coefficient_separation.py
python -m py_compile claims/arbitrary-order/verify_fixed_q_product_selector_companion_full_coefficient_separation.py claims/arbitrary-order/audit_fixed_q_product_selector_companion_full_coefficient_separation.py
uv run --with ruff ruff check claims/arbitrary-order/verify_fixed_q_product_selector_companion_full_coefficient_separation.py claims/arbitrary-order/audit_fixed_q_product_selector_companion_full_coefficient_separation.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_fixed_q_product_selector_companion_full_coefficient_separation.py claims/arbitrary-order/audit_fixed_q_product_selector_companion_full_coefficient_separation.py
```

The primary replay uses explicit ternary block matrices and recursive perfect-
matching enumeration.  The no-import audit instead uses sparse evaluated edge
tables and a bitmask hafnian recurrence.  Both check `431` complete companion
entries and the coefficient triple

```text
(G_(Q union {u_0,u_1}), B_(u_0,u_1)G_Q,
F_(Q union {u_0,u_1}))=(0,1,1).                       (4)
```

The primary replay also checks that the graph's global all-one coefficient is
zero.  The arbitrary-field statements (2)--(3), the maximum-root proof, and
the module-type distinction are the written proof.

A separately forked read-only hostile audit reconstructed `GLS2`, `GLD15`,
and former `GLD65` directly before inspecting the fixture.  It initially
rejected an earlier weaker model whose four-set companions were nonzero, then
replayed the corrected worktree and independently accepted all four
load-bearing points: the complete `431`-entry legal row, maximum-root status,
the diagonal three-colour response, and refutation of former GLD65 Theorem 5
at exactly its stated conditional scope.  The audit made no repository
changes.  This conceptual review is additional to, not a replacement for,
the no-import implementation above.

## 5. Frontier consequence

The following remain live:

- `GLS2`, `GLD15`, and the `GLS17` factored-selector implication;
- the target-coupled/Fitting statements `GLS18` and `GLS19`;
- the standalone support lemma saying a diagonal three-full compound has the
  six-edge camouflage support; and
- `GLD64`, whose decomposable-channel proof does not use the failed
  product-selector cross-Gram identity.

The following are withdrawn from live use:

- the `GLD65` cross-Gram representation and three-colour exclusion;
- the `GLD66` common cross-pairing step, two-colour exclusion, and
  synchronized-plane corollaries; and
- every frontier edge that used those exclusions to reduce the first-root
  profiles.

The corrected universal-bridge obligation returns to the `GLS17`/`GLS18`
source boundary: force and target-couple legal rows using actual companion
coefficients, without transferring their nuisance equations to full subgraph
matching tensors.
