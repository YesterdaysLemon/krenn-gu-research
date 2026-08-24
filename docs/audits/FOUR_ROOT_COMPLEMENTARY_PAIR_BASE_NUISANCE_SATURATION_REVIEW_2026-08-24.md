# Four-root complementary-pair base-nuisance saturation review -- 2026-08-24

## Verdict

**PASS at the stated complete-module source scope.**  For complementary port
pairs `S` and `T=U-S` at root order four, the target-`S` complete base
nuisance contains the order-two label `I=T`.  Its maximum-root term is

```text
H_T tensor Pi_T in L_S^0 tensor W_S.                  (1)
```

If `Pi_T!=0`, a target functional nonzero on `Pi_T` turns the coefficient
slices of (1) into every possible `H_T`, so `N_S^0=L_S^0` and `b_S=0`.
If `Pi_T=0`, its own class `b_T=[Pi_T]` is zero.  Therefore

```text
b_S!=0  =>  b_T=0,                                    (2)
```

at most three of the six pair base shadows survive, and every maximal
survivor set is a star or triangle.

This rejects the `GLS17` all-six pair-base source premise formerly feeding
the conditional `GLD16` detector.  It does not reject the full `GLD16`
common-line theorem, because non-leading or promoted legal rows remain
possible.  It supplies no direct-port restriction, no full-coefficient zero,
no GHZ witness or counterexample, and no global resolution.  The Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. Audited coefficient types and tensor factors

The review reconstructed the relevant objects from `GLD15` and `GLS16`.

For a pair target `S`, after maximum-root evaluation,

```text
L_S^0=tensor_(u in U-S)V_u^*,
W_S=tensor_(s in S)V_s^*,
b_S=[Pi_S] in L_S^0/N_S^0.                            (3)
```

The complete base nuisance retains every order-two label `I!=S`.  It does
not discard the complementary port pair.  If `T=U-S`, then the label `I=T`
has:

- deck input `H_T` on `T=U-S`, exactly the receiver factor `L_S^0`; and
- companion `G_(B-T)=G_(Q union S)`, which evaluates to `Pi_T` on
  `U-T=S`, exactly the target factor `W_S`.

Thus (1) has the stated orientation.  Swapping `Pi_S` and `Pi_T`, or slicing
the receiver factor rather than `W_S`, would invalidate the proof; neither
swap occurs in the owning theorem.

The label `I=T` is not either desired target-`S` label.  Those are `I=S` and
`I=Q union S`.  It is therefore genuinely part of the joint nuisance before
the maximum-root shadow is taken.

## 2. Complete-domain saturation

The proof uses the universal labelled deck domain

```text
E=direct-sum_(empty!=I subset B, |I| even)
    tensor_(i in I)V_i^*.                              (4)
```

On the `I=T` direct summand, `H_T` ranges over the whole tensor space
`L_S^0`.  Choose `eta in W_S^*` with `eta(Pi_T)=1`.  Then

```text
(id tensor eta)(H_T tensor Pi_T)=H_T                  (5)
```

for every deck input.  Equation (5), not one selected physical value of
`H_T`, is what proves that the nuisance equals the whole receiver.  The
review specifically rejected the weaker and invalid interpretation in which
only the graph's realized `H_T` were available.

The final implication in (2) is also typed correctly.  In the target-`T`
base quotient, the desired raw tensor is the same `Pi_T`; hence
`Pi_T=0` implies `b_T=[0]=0` without any converse or genericity assumption.

No division by a graph coefficient, response, permanent, rank minor, or
selector coordinate occurs.  Characteristic zero is inherited from the live
chart, although the displayed finite-dimensional slicing argument itself
works over any field.

## 3. Exhaustive four-port consequence

The six port pairs split into

```text
{01,23},             {02,13},             {03,12}.    (6)
```

Equation (2) permits at most one survivor in each bracket.  Exhausting the
`64` labelled survivor masks gives `27` admissible masks.  Exactly `8` have
three edges: the four vertex stars and the four complementary triangles.

This is a base-class atlas only.  The review found no justification for
transferring it to direct-block support, response support, operator-space
rank, or a physical graph support skeleton, and the owning theorem makes none
of those transfers.

## 4. Independent evidence

Run:

```powershell
python claims/arbitrary-order/verify_four_root_complementary_pair_base_nuisance_saturation.py
python -I claims/arbitrary-order/audit_four_root_complementary_pair_base_nuisance_saturation.py
python -m py_compile claims/arbitrary-order/verify_four_root_complementary_pair_base_nuisance_saturation.py claims/arbitrary-order/audit_four_root_complementary_pair_base_nuisance_saturation.py
```

The primary replay uses exact row reduction on the full family of coefficient-
slice matrices for local dimensions one through four.  It verifies all six
ordered complementary slot orientations, every coordinate and dense
nonzero-companion profile, the `27` admissible survivor masks, and all
consistent raw/quotient Boolean profiles.

The no-import audit uses a different constructive route.  It selects the
first nonzero companion coordinate, constructs its normalized dual target
slice, and recovers every receiver basis vector directly for dimensions one
through five.  It traverses the port labels in reverse order and independently
classifies the eight maximal families as four stars and four triangles.

The scripts replay the finite tensor-factor and `K_4` consequences.  The
arbitrary-field saturation statement is the written linear proof.

## 5. Read-only hostile research audit

A separately delegated Luna-max council first saturated on merged
`origin/main`, `GLD67`, `GLD15`, `GLS15`--`GLS19`, `GLD4`, and the same-graph
target-coupling boundaries.  It independently tested the three proposed
universal bridges:

1. the full GHZ contraction of one pure-`M` row;
2. a separately legal `M/Z` response axis; and
3. a coefficient-pure cross-target transport map.

It found no valid unconditional `G_D -> F_D/B_uv` transfer.  The first route
collapses only to the selected residual-absent response, the second still
requires rank/common-line/activity gates, and the third still lacks the
complete-nuisance transport membership or coefficient-pure separator.

The council then derived (1)--(2) independently, checked the exact target and
complement orientations against the complete module, ran both new scripts,
and confirmed the `27/8/4/4` survivor counts.  It made no repository edits.
Its final draft audit also replayed the owning `GLS16`, `GLS17`, and `GLD16`
checks and required one documentation clarification: the solid conditional
arrows into `GLD16` must say explicitly that their all-six root-order-four
base-shadow source is impossible.  The frontier labels now do so.
This conceptual audit is additional to, not a replacement for, the no-import
implementation.

## 6. Frontier consequence

The following proposed source lane is empty:

```text
all six GLS16 pair base shadows
 + one GLS17 four-port first-root shadow
 -> seven-row pure-M GLD16 package.                    (7)
```

The conditional implication from the seven rows to the `GLD16` detector
remains mathematically valid, but (7) cannot supply those rows.  At every fixed-
`Q`, root-order-four point, at least one base class in each complementary pair
is swallowed.

The smallest positive successor is correspondingly sharper: use the at-least-
three swallowed base circuits, in the complements of a star/triangle survivor
family, to obtain a coefficient-pure complete mixed-target contradiction; or
supply the needed pair rows through a genuinely non-leading or promoted
interface.  Other roots, activity, anchors, permanent extraction, and global
resolution remain separate obligations.
