# Self-review: diagonal coordinate-endpoint zero-visible-wall exclusion

Date: 2026-08-14

## Verdict

Accept the stated characteristic-zero exclusion of the complete zero-visible
wall at the two diagonal monomial coordinate endpoints, subject to the
repository validation below.  The theorem combines S2CF's exact corrected
cube and visibility census with the general full-sensor radical-line theorem
proved inside S2CG.

It does not exclude a one-visible wall or the two-visible open cell, and it
does not close either diagonal endpoint.  Global Krenn--Gu remains
**UNRESOLVED**.

## Load-bearing chain checked

1. S2CF normalizes a diagonal endpoint as
   `C=lambda e_2 tensor e_2,w=e_0`, with nonzero `lambda`, shared-factor
   kernel `N=span((x,y,0)) subset K`, fully injective root rows, and
   `x,y` not proportional to `e_2`.
2. For `alpha in x^perp,beta in y^perp`, S2CF derives from the complete
   target the corrected cube
   `per(r_alpha,p_beta,q_k)=alpha_k beta_k T_k+lambda alpha_2 beta_2 S_k`.
   S2CH uses this proved consequence in the forward direction only; it does
   not replace the sixteen retained face equations by the cube.
3. The two visibility failures are exact Boolean support conditions.  With
   `x,y` nonzero and neither proportional to `e_2`, their intersection has
   exactly the ordered solutions `(e_0,e_1)` and `(e_1,e_0)`.  No generic
   coordinate is divided out.
4. At `(x,y)=(e_0,e_1)`, take `alpha=e_1`.  Every
   `beta in y^perp` has `beta_1=0`, while `alpha_2=0`.  Both the target term
   and corrected source term vanish for all three `q_k`.  The exchanged case
   uses `alpha=e_0` identically.
5. The root covectors defining these rows annihilate `N`.  Since
   `K=D^(-1)(U)`, `dim K=4`, and `dim ker D=1`, the quotient-dual image
   `V=H^T(N^perp)` has dimension three.  Third-row injectivity gives
   `Q=image theta=V`, so every row in the radical calculation genuinely lies
   in the same three-space.
6. The quotient maps `H_bar:W->K/N` and `D_bar:K/N->U` identify the
   full-sensor singleton determinant with a nonzero basis factor times
   `Alt(Q)`.  Hence `Alt(Q)!=0`; this is inherited physical structure, not a
   generic assumption about a three-plane.
7. S2CG Corollary 2 is coordinate-free: in any three-space with nonzero
   alternating tensor, the radical of a nonzero row has dimension at most
   one.  It does not depend on S2CG's canonical-binomial residual hypothesis.
8. Injectivity of `rho` makes the selected row nonzero, while injectivity of
   `pi` preserves the two dimensions of `y^perp`.  The corrected cube would
   therefore put a two-plane inside a radical of dimension at most one, the
   required contradiction.

## Adversarial checks and scope controls

- The support-mask census includes all six nonempty projective supports
  allowed by `x,y not proportional e_2`, hence all 36 ordered pairs.  It is
  not a finite sample of coefficient values: the visibility predicates
  depend only on those zero/nonzero supports.
- The argument uses all three `q_k` directions.  Checking only the
  `w`-perpendicular face would not establish a radical in `Q`.
- The radical-line theorem, not a numerical rank observation, supplies the
  contradiction.  The scripts replay its hypotheses and leave its analytic
  proof owned by S2CG.
- On the one-visible same-coordinate walls, the analogous radical shore is
  only one-dimensional.  S2CF has an exact quotient control there.  S2CH
  neither promotes that control to a physical point nor claims the wall
  impossible.
- No Nullstellensatz search, localization, modular lift, finite-field
  extrapolation, or numerical optimization enters the proof.

## Verifier independence

The primary SymPy replay exhausts the support masks, checks all twelve
target/correction coefficients in the two crossed orientations, reconstructs
an exact rank-eight derivative and rank-four incidence fixture with all root
projections injective, verifies `Q=H^T(N^perp)` dimension three, and checks
the separated alternating determinant and basis-change law.

The independent audit imports neither the primary verifier nor SymPy.  It
uses standard-library `Fraction` arithmetic, reversed support, root, source,
permutation, and pivot traversals, its own rank/span implementation, an
independent full-rank graph fixture in each orientation, and a separate loop
over all twelve cube coefficients.  Both scripts explicitly leave the
coordinate-free radical-line impossibility to S2CG's written proof.

## Validation

Validation at the candidate checkpoint completed as follows:

```text
primary SymPy replay:                         PASS
independent no-import Fraction audit:         PASS
Python byte compilation:                      PASS
Ruff:                                         PASS
candidate-tree hygiene:                       PASS
  1,998 Python files / 1,141 Markdown files / 220 ledger entries;
  all hashes, provenance, links, and root-layout checks valid
migration-tool unit tests:                    191 PASS
fourteen-vertex cycle-cover lattice tests:     14 PASS
link rewrite:                                  zero changes
```

## Remaining obligations

At each diagonal endpoint, the exact remaining cells are the one-visible
walls and the two-visible open set.  Their sixteen retained `k=1,2` face
equations and nonzero tangent-coset rank-one `k=0` flattening remain
load-bearing.  All nonmonomial residuals outside S2CG, joint-rank-three and
derivative-rank-seven target cells, pair gates, other components and poles,
higher orders, and all-rank-drop also remain.  The dedicated global
resolution gate is not triggered.
