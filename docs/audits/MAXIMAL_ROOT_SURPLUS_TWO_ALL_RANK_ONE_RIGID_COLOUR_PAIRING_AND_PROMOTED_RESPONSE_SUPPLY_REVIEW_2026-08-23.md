# Hostile review: all-rank-one rigid colour pairing and promoted-response supply

## Verdict

**ACCEPT as a scoped root-order-three source/deck theorem, conditional on the
repository replay and exact-head hosted CI below.**

`GLS57` decides the all-rank-one subbranch of the zero-anchor, all-six-rigid
`GLS56` source cell.  Rank-one torus rigidity makes each auxiliary label read
one unique coordinate.  The complete target forces exactly two labels of
each colour.  On the pure auxiliary word, one and only one pair companion
survives, so the entire companion--including both old probe slots--is a
nonzero pure diagonal target tensor and its complementary physical deck has a
nonzero pure coefficient.

The same complete coefficient comparison gives a mixed-word master identity.
On the complementary off-readout `2 x 2 x 2 x 2` face of each colour-pair
deck, fifteen mixed cells vanish and the sole constant-colour cell is
nonzero.  This is face purity, not purity of the whole physical deck.

At least one colour pair avoids the two residual labels and is therefore a
literal promoted `GLS8` pair target.  Its response polynomial has a nonzero
residual monomial, so it is generically nonzero and can be retained together
with the original two `GLS4` polynomial gates.  This does not prove
complete-nuisance survival or pointwise nonvanishing on every residual fibre.

The all-rigid branch, the maximum-root surplus-two strategic node, and the
global Krenn--Gu conjecture remain **UNRESOLVED**.

## Reviewed artifacts and ownership

- [`GLS57 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ALL_RANK_ONE_RIGID_COLOUR_PAIRING_AND_PROMOTED_RESPONSE_SUPPLY_THEOREM.md)
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_all_rank_one_rigid_colour_pairing_and_promoted_response_supply.py)
- [`independent no-project-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_all_rank_one_rigid_colour_pairing_and_promoted_response_supply.py)
- complete two-probe expansion and promoted target typing: `GLS8`
- rank-one torus-rigidity equivalence: `GLS55`
- rigid/nonrigid source split and rigid-pair cautions: `GLS56`
- raw residual-absent deck/output separation: `GLS35`
- receiver interfaces checked against `GLD3`, `GLD6`, and `GLD15/GLD16`

The new content is not present in those owners: exact `2+2+2` pairing, full
pure-companion factorization, the mixed-word master identity and off-readout
face, exhaustive residual-pair incidence typing, and the forced nonzero
promoted-response polynomial.

## Quantifier and pure-slice audit

Fix an actual characteristic-zero complete-GHZ witness in a `GLS4`-eligible
`r=3` promoted chart, with old probes `A`, six auxiliary labels
`Bhat=Q disjoint-union Uhat`, and zero probe block
`omega=W_(a_0,a_1)=0`.  Assume all six full joint probe-incidence maps are
torus-rigid of rank one.

`GLS55` gives, without choosing a minor,

```text
row(J_t)=K e_(t,kappa(t))^*.
```

Thus every pair companion `G^A_D` is supported at the unique auxiliary cell
`(kappa(s),kappa(t))` on its two labels.  Evaluating all six auxiliary labels
at colour `c` leaves only pairs inside `P_c=kappa^(-1)(c)`.  The target slice
is the nonzero probe tensor `E_(A,c)`, so `|P_c|>=2`.  Since the three sets
partition six labels, all have size two.

For the unique pair `P_c`, complete coefficient comparison gives

```text
h_c M_c=E_(A,c).
```

This proves simultaneously that `h_c` and `M_c` are nonzero.  Because the
auxiliary support of the full companion is already one cell, the conclusion
is the full tensor identity

```text
h_c G^A_(P_c)=d_c.
```

The proof is denominator-free.  Displaying `h_c^(-1)` is a consequence after
nonvanishing has been proved, not a localization assumption.

## Mixed-word and face audit

For an arbitrary auxiliary coordinate word `sigma`, a pair term survives
exactly when both of its labels use their readout coordinate.  Hence the
coefficient identity is

```text
sum_(D subset A(sigma), |D|=2) M_D h_D(sigma)
 = E_(A,c) for a constant word c, and 0 otherwise.
```

On the off-readout complement face for a fixed pair `D`, the active set is
exactly `D`, so there is only one summand.  For `D=P_c`, exactly one of the
sixteen complement words makes the global word constant: all four complement
labels also use `c`.  The other fifteen words are mixed and their deck
coefficients vanish because `M_(P_c)!=0`.  For a cross-colour pair, all
sixteen words are mixed, but the vanishing conclusion is correctly stated
only when its companion matrix is nonzero.

The theorem explicitly does not extend face purity to the whole deck.  Once
another label uses its own readout coordinate, several pair terms may survive
and cancel.

## Residual-label and response typing

The two residual labels either occupy one colour pair or two different colour
pairs.  These are exhaustive.

| Residual placement | Pairs inside `Uhat` | Other forced deck types |
|---|---:|---|
| `Q=P_d` | two | `D=Q` has residual-absent `H_Uhat` |
| residuals split between two `P_c` | one | two mixed `Q`--`Uhat` labels have one-residual three-port decks |

For `C=P_c subset Uhat`, `S_c=Uhat-C` has size two and the literal `GLS8`
typing is

```text
g_(S_c)=G_C^A,
P_(S_c)(H;z_Q)=H_(Q union S_c)(z_Q,-_(S_c))
              =H_(Bhat-C)(z_Q,-_(S_c)).
```

The coefficient of the pure-`c` output polynomial at the residual monomial
`z_(q_0,c)z_(q_1,c)` is exactly `h_c!=0`.  Distinct residual monomials are
independent, so the response is not the zero polynomial.  Multiplying it by
the two nonzero `GLS4` gate polynomials gives a nonzero polynomial, whose
nonvanishing locus meets the complex residual torus.

This is generic/existential nonvanishing.  Other residual monomials can
cancel at a prescribed fully supported point, and no exceptional response
fibre is excluded.

## Selector and receiver audit

The desired coefficient is a pure target row, but that does not imply

```text
[g_(S_c)]!=0 in L_(S_c)^*/N_(S_c)(z_Q).
```

The nuisance space is fibre-dependent.  The theorem correctly gives two
conditional routes only:

1. assume response, both `GLS4` gates, and quotient survival at one specified
   common residual point; or
2. assume function-field quotient survival, whose dense open can be
   intersected with the proved response/gate open.

It does not combine pointwise survival at one point with response
nonvanishing at another.

The downstream receiver corrections are also exact.

- The formerly suggested direct `GLD3` endpoint using old probes `A` is
  structurally impossible on this branch.  After any fixed probe contraction,
  `D_(st)` is supported only at `(kappa(s),kappa(t))`.  At a fixed port `u`, a
  diagonal coefficient can therefore be nonzero only in colour `kappa(u)`,
  whereas `GLD3` requires activity in all three colours at one port.
- One useful promoted-`Q` row is not that package.
- `omega=W_(a_0,a_1)=0` is not the promoted residual scalar `H_Q(z_Q)`, so it
  is not an `h=0` `GLD15/GLD16` entry.
- A six-vertex contradiction would require a legal contraction/splicing that
  identifies the contracted six-mode tensor with one weighted `P_6`
  restriction.  The original equation is already the physical eight-vertex
  matching identity; its contracted first-variation presentation does not by
  itself provide the six-mode reduction.

The local probe row realizing one rigid coordinate may vary with the label;
no common contraction or projective synchronization is silently inferred.

## Verifier independence and scope

The primary verifier uses exact rational tensors.  It checks all `3^6`
readout assignments, all fifteen residual-pair placements on every compatible
assignment, full companion entries, all 240 off-readout pair-face words, the
response monomial, an explicit exceptional cancellation, and a common torus
point for representative nonzero gate polynomials.  It additionally exhausts
all `90*15*4=5400` compatible profile/window/port cases and finds at most one
possible active diagonal colour at every port.

The independent audit imports neither the primary verifier nor project code.
It uses base-three/bit-mask label encodings, a bounded `F_7` shore replay with a
separate matrix implementation, a separate face census, and sparse
polynomial-support masks.  It is genuinely independent replay of the finite
algebra.  Its separate base-three/bit-mask activity census also exhausts the
same `5400` cases without importing the primary representation.  The written
proof, not the bounded `F_7` replay, carries the characteristic-zero
complete-witness theorem.

## Hostile boundaries

The review rejects each of the following stronger readings.

- all six rigid implies all six ranks one;
- rank-one rigidity without the complete target forces nonzero companions;
- the complementary physical deck is globally pure;
- a nonzero response polynomial is nonzero on every residual fibre;
- a pure desired coefficient survives complete nuisance;
- one useful target enters `GLD3`, `GLD6`, or `GLD16`;
- old-probe selector or synchronization improvements can restore `GLD3`
  three-colour activity on the rank-one branch;
- the label-dependent rigid rows synchronize automatically;
- the contracted six-label first variation is already a weighted `P_6`
  restriction;
- the six-label counting proof extends to arbitrary root order;
- `GLS57` closes the all-rigid branch, strategic node, or global conjecture.

The smallest remaining obligation on this branch is to use the complete
mixed/deck equations to force a legal splicing that identifies the contracted
six-mode tensor with a weighted `P_6` restriction accepted by the committed
six-vertex theorem, or to construct a different named receiver with all of
its gates.  The old-probe `GLD3` route is closed, not merely unsynchronized.
Higher joint ranks remain a separate all-rigid branch.

## Required replay

From repository root:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_all_rank_one_rigid_colour_pairing_and_promoted_response_supply.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_all_rank_one_rigid_colour_pairing_and_promoted_response_supply.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_torus_kernel_contraction_and_five_rigid_label_floor.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_torus_kernel_contraction_and_five_rigid_label_floor.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_nonrigid_probe_kernel_three_colour_pure_star_escape.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_nonrigid_probe_kernel_three_colour_pure_star_escape.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
```

Then run the authoritative candidate-tree validation and require exact-head
hosted CI before merge.

```text
GLS57 base HEAD: cca89501ae1a568ca395ba3ef0c38f23d9b39df4
```

The protected authority checkout, protected exploratory worktrees, and every
unrelated process were read-only or left untouched throughout this tranche.
