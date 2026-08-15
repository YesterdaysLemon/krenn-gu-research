# Self-review: complete diagonal one-visible-wall exclusion

Date: 2026-08-14

## Verdict

Accept the stated characteristic-zero exclusion of the complete one-visible
wall at both surviving diagonal monomial coordinate endpoints, subject to
the repository validation below.  The proof exhausts all twenty ordered
support masks and couples S2CF's corrected cube to the exact complete faces
and unsliced root matrix, using S2CG's general zero-pair/radical geometry.

The theorem does not exclude the two-visible open cell and therefore does
not close either endpoint.  It does not reduce an arbitrary nonmonomial
residual to a monomial endpoint.  Global Krenn--Gu remains **UNRESOLVED**.

## Load-bearing chain checked

1. S2CF's visibility predicates depend only on the projective zero supports
   of `x,y`.  Among the six allowed nonempty supports other than `{2}`, their
   exclusive-or has exactly twenty ordered solutions.
2. The support table partitions disjointly as two same-coordinate masks,
   four radical masks, seven `T_0` cross-pair masks, six coordinate-shore
   `T_1` masks, and the final `{0,2}` by `{0,2}` mask.  S2CI owns the first
   two masks; every other mask appears once in the new proof.
3. On the four radical masks, a nonzero coordinate row has the entire other
   injective perpendicular plane in its radical.  The resulting dimension
   two contradicts S2CG's coordinate-free radical bound in the physical
   `Alt(Q)!=0` three-space.
4. The fourteen remaining masks have explicit bases of `x^perp,y^perp`
   with one visible corner and two cross-zero corners.  The bases retain all
   support boundaries and have nonzero determinants exactly on their named
   masks.
5. S2CG's zero-pair theorem gives an exhaustive split-three-source/common-
   split-plane dichotomy, including every dependent/independent combination.
   A dependent square-zero row is pure; no generic plane position is used.
6. On all seven `T_0` masks, `q_1` supplies a factor line of `T_0` in both
   incidence forks.  The triple quotient therefore kills
   `M(r_1,p_1,q_1)` while the complete face requires the fully transverse
   tensor `T_1`.
7. On the six `T_1` masks with one `e_0` shore, the exact linear combination
   `M(A',B')` cancels the tangent terms at `q_0` and uses retained zeros at
   `q_1,q_2`.  In both root orientations it recovers quotient source values
   `0,0,-lambda^-1 bar(T_2)`.
8. The unsliced `(0,0,0)` coefficient then makes the independent nonzero
   quotient images of `T_0,T_2` proportional.  Both orientations are written
   explicitly; no colour swap moves the normalized line `w=e_0`.
9. In the final `{0,2}` by `{0,2}` mask, the corrected cube instead gives
   `bar(S_0)=-x_2y_2/(lambda x_0y_0)bar(T_0)`.  Quotienting the entire
   unsliced root matrix and separating `bar(T_0),bar(T_2)` forces `H_2=0`
   and `E_00=r(C+H_0)`.
10. From `H_2=0`, either both lift entries vanish or rank-one equality gives
    `a_2=t x,b_2=t y`.  The legitimate shear `k_2 -> k_2-t(x,y,0)` leaves
    `q_0,q_1,q_2` fixed and gauges those two entries to zero while retaining
    the third entry `e_2`.  S2CF's row formula and injectivity force
    `R=P=span(q_0,q_1)`.
11. Reclassifying the cross pairs inside that common plane makes it split
    across two sources.  Its three rows `r_1,p_1,q_1` then have zero
    permanent, contradicting the visible `P_111=T_1`.

## Adversarial checks and scope controls

- Two independent agents reconstructed the full support atlas and returned
  theorem-ready PASS verdicts.  One separately audited the actual written
  theorem and identified five prose-level precision issues; all five were
  corrected before promotion.
- The proof never treats a timeout, numerical fit, modular calculation, or
  chart count as evidence.  No solver is used.
- Divisions occur only by `lambda` and by coordinates declared nonzero on
  the named support chart.  The support union, radical cases, and root-
  exchanged formulas retain every boundary.
- The triple quotient is used only after proving that the relevant physical
  row supplies one of the visible target's factor lines.  The outside rows
  need not lie in `Q`.
- `H_2=0` does not erase the graph lift `k_2`; only its first- and second-root
  entries are gauged to zero.  The theorem explicitly retains its third
  entry and the dual-row basis behavior.
- The final conclusion is only a local monomial-endpoint wall exclusion.
  The two-visible cell, all other nonmonomial residuals, and the wider global
  proof obligations remain stated as open.

## Verifier independence

The primary SymPy replay exhausts the support table, checks all perpendicular
bases and cube coefficients, reconstructs the radical-shore dimensions,
checks retained face indices and both source-recovery orientations, and
symbolically verifies the final matrix separation and graph-gauge/rank
interface.

The independent audit imports neither the primary verifier nor SymPy.  It
uses standard-library `Fraction` arithmetic, reversed support, source,
permutation, and pivot traversal, its own tensor, quotient, rank, and
incidence routines, and independent fixtures for the support atlas, source
identities, and final matrix argument.  Both scripts explicitly leave the
coordinate-free S2CG classification to the written proof.

## Validation

Validation at the candidate checkpoint completed as follows:

```text
primary SymPy replay:                         PASS
independent no-import Fraction audit:         PASS
Python byte compilation:                      PASS
Ruff:                                         PASS
candidate-tree hygiene:                       PASS
candidate-tree census:                        2,002 Python / 1,145 Markdown / 222 ledger entries
migration-tool unit tests:                    191 PASS
fourteen-vertex cycle-cover lattice tests:     14 PASS
link rewrite:                                  zero changes
```

## Remaining obligations

The sole remaining diagonal monomial coordinate-endpoint cell is the
two-visible open set.  Its sixteen retained `k=1,2` faces and nonzero
tangent-coset rank-one `k=0` flattening remain load-bearing.  Every
nonmonomial residual outside S2CG, lower-rank target cell, pair gate, other
component and pole stratum, higher order, and all-rank-drop branch also
remains open.  The dedicated global resolution gate is not triggered.
