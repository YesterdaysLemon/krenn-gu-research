# Self-review: diagonal same-coordinate one-visible-wall exclusion

Date: 2026-08-14

## Verdict

Accept the stated characteristic-zero exclusion of the exact normalized
support cells `x=y=e_0` and `x=y=e_1` at the two diagonal monomial coordinate
endpoints, subject to the repository validation below.  The theorem combines
S2CF's corrected cube and complete retained target with S2CG's general
zero-pair geometry in the physical full-sensor alternating three-space.

It does not normalize or exclude any other one-visible support pair, it does
not exclude the two-visible open cell, and it does not close either diagonal
endpoint.  Global Krenn--Gu remains **UNRESOLVED**.

## Load-bearing chain checked

1. S2CF normalizes the endpoint as `C=lambda E_22,w=e_0`, with
   `lambda!=0`, `x,y` not proportional to `e_2`, fully injective involved
   rows, the complete recovered `k=1,2` faces, and the unsliced `k=0`
   tangent-coset equation.
2. Kernel incidence and full-sensor rank give `Alt(Q)!=0` for the physical
   third-row three-space.  S2CG's zero-pair classification and its dependent
   square-zero branch are coordinate-free consequences for any such `Q`;
   the canonical-binomial residual excluded by S2CG is not assumed.
3. On either same-coordinate cell, the corrected cube supplies two cross
   zero pairs and one nonzero visible target map.  Involved-row injectivity
   makes the two row planes two-dimensional.
4. The dependent/independent split of the two zero pairs is exhaustive.  Two
   distinct independent split planes span three pure lines in distinct
   sources; equal planes give one common split plane.  One dependent pure
   line either lies in the independent split plane, supplies its omitted
   source, or contradicts `Alt(Q)!=0`.  Two dependent pairs give the same
   split plane because the visible map forces their pure lines into distinct
   sources.
5. For `x=y=e_1`, the split-three-source fork makes every `Q^3` permanent a
   multiple of `T_0`; the triple quotient by its factor lines kills
   `M(r_1,p_1,q_1)` but not the recovered target `T_1`.  In the equal-plane
   fork, `H=span(q_1,q_2)` and all eight retained cross-face zeros force
   `r_1,p_1,q_1` to miss the same source, again contradicting `P_111=T_1`.
6. For `x=y=e_0`, quotienting by the factor lines of the visible `T_1` kills
   `P_000` in both incidence forks.  Because every tangent tensor has zero
   `(2,2)` entry, the complete target recovers
   `S_0=lambda^-1 P_220`, `S_1=lambda^-1 P_221`, and
   `S_2=lambda^-1(P_222-T_2)`.
7. Those source tensors have quotient values `0,0,-lambda^-1 bar(T_2)`.
   The exact unsliced `(0,0,0)` equation therefore says
   `-bar(T_0)=-lambda^-1(H_2)_00 bar(T_2)`.  The two nonzero quotient target
   classes are linearly independent, giving the contradiction.

## Adversarial checks and scope controls

- Three agents independently reconstructed the zero-pair incidence split.
  Both the complementary `e_1` face argument and the aligned `e_0` unsliced
  argument received explicit adversarial PASS verdicts before promotion.
- The proof uses the corrected cube only in the forward direction.  It does
  not infer a retained face from the contracted cube.
- The aligned proof keeps the exact `+H_c` signs in S2CF and uses
  `C_00=0`; no extra residual term is inserted at `(0,0,0)`.
- The `k=0` source recovery uses `x_2=y_2=0`, which makes every
  `(H_c)_22` vanish.  This step is special to the aligned coordinate cell
  and is stated explicitly.
- The target quotient is an ordinary vector-space quotient.  No generic
  nonzero coordinate, localization, saturation, or projective limit enters.
- A general one-visible pair is not target-stabilizer-equivalent to either
  same-coordinate support cell.  All nonsame-coordinate support patterns
  stay open.

## Verifier independence

The primary SymPy replay checks both corrected cube tables, the exact
complete-face indices, every dependent/independent incidence fork at the
support interface, the split/equal-plane quotient identities, the three
source recoveries, and the unsliced target quotient.

The independent audit imports neither the primary verifier nor SymPy.  It
uses standard-library `Fraction` arithmetic, reversed source/permutation and
pivot traversal, its own tensor, quotient, rank, and incidence routines,
and separate exact fixtures for the recovered-face and unsliced forks.  Both
scripts leave the coordinate-free zero-pair theorem to the written proof.

## Validation

Validation at the candidate checkpoint completed as follows:

```text
primary SymPy replay:                         PASS
independent no-import Fraction audit:         PASS
Python byte compilation:                      PASS
Ruff:                                         PASS
candidate-tree hygiene:                       PASS
  2,000 Python files / 1,143 Markdown files / 221 ledger entries;
  all hashes, provenance, links, and root-layout checks valid
migration-tool unit tests:                    191 PASS
fourteen-vertex cycle-cover lattice tests:     14 PASS
link rewrite:                                  zero changes
```

## Remaining obligations

The exact remaining diagonal cells are the nonsame-coordinate one-visible
support patterns and the two-visible open set.  Their sixteen retained
`k=1,2` face equations and nonzero tangent-coset rank-one `k=0` flattening
remain load-bearing.  All nonmonomial residuals outside S2CG, lower-rank
target cells, pair gates, other components and poles, higher orders, and
all-rank drop also remain.  The dedicated global resolution gate is not
triggered.
