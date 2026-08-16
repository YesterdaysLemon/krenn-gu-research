# Self-review: nonmonomial complete-target zero-pair localization

Date: 2026-08-14

## Verdict

Accept the stated characteristic-zero complete-target normal form and
zero-pair localization for the actual nonmonomial residual block in the
fully-injective joint-rank-four/derivative-rank-eight cell, subject to the
repository validation below.

Every correcting mixed zero pair is impossible.  Every surviving mixed zero
pair is structural and belongs to an explicit union of at most four
projective points.  This is a strict reduction, not an exclusion of the
nonmonomial cell: the finite structural-zero cells and the zero-pair-free
cell remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## Load-bearing chain checked

1. S2BQ's exact rank-eight incidence table puts the shared syzygy
   `N=span((x,y,0))` inside `K`.  Actual nonmonomial `C` makes the other
   shared factor coordinate.  If `w=omega e_t`, replacing `x,y` by
   `omega x,omega y` normalizes `w=e_t` without changing `D`, `N`, or `C`.
2. Third-row injectivity makes `K` a graph over the third root space modulo
   `N`.  Its three derivative images give unique source tensors `S_k`.  The
   complete coefficient identity has two slices `F^(k)=C S_k` for `k!=t`
   and one slice containing all tangent columns.  Removing the other tangent
   columns leaves `(C+H_t)S_t`; this root factor is nonzero by rank eight.
3. Kernel incidence identifies `Q=image theta` with `H^T(N^perp)`.  The
   quotient singleton map and full-sensor determinant give `Alt(Q)!=0`.
   The injective planes `R=rho(x^perp),P=pi(y^perp)` lie in `Q`.
4. Contracting the complete slices by `alpha in x^perp,beta in y^perp`
   kills every tangent column, and only for that stated reason.  The exact
   cube is `M(r_alpha,p_beta)(q_k)=alpha_k beta_k T_k+C(alpha,beta)S_k`.
5. When `C(alpha,beta)=0`, a mixed zero has coordinatewise-disjoint
   covector supports.  One covector must be coordinate.  Splitting by which
   covector is coordinate gives the two unions in the theorem, and every
   point of those unions is genuinely a structural zero.
6. A positive-dimensional partner shore would inject a two-plane into the
   radical of a nonzero row.  S2CG bounds that radical by one dimension in
   every three-space with nonzero alternating tensor.  Each zero coordinate
   of `x` or `y` therefore contributes at most one point, giving the exact
   upper bound `(3-|supp x|)+(3-|supp y|)<=4`.
7. When `c=C(alpha,beta)!=0`, the zero pair recovers
   `S_k=-alpha_k beta_k c^(-1)T_k`.  If all three resulting root tensors in
   the empty permanent were nonzero, a common root evaluation would map the
   rank-four tensor `P_3` invertibly to a concise rank-three diagonal.  Thus
   one root tensor vanishes.  A colour different from `t` would make the
   actual `C` monomial, so the vanishing colour is `t` and
   `C+H_t` is proportional to `E_tt`.
8. The resulting corrected cube has diagonal bilinear forms `B_k` and
   `B_t=0`.  Quotienting out the third target's factor lines and applying
   S2CK forbids two forms from being simultaneously nonzero.  The infinite-
   field polynomial-domain argument leaves exactly one nonzero form; S2CG's
   radical bound makes it a perfect pairing.
9. Permanent symmetry with two rows in `R`, then two in `P`, forces both
   planes into the kernel of the surviving target coordinate.  They equal
   that common plane.  A nonisotropic row and its orthogonal mate form an
   independent zero pair, so S2CG makes the common plane a split two-source
   plane and aligns it with the surviving target factors.
10. For the third colour `k` outside the surviving colour and `t`, one has
    `k!=t` and `q_k` in the split plane.  Quotienting by the surviving target
    factors kills the whole physical `k` slice while preserving `T_k`.  The
    retained complete face gives `E_kk=mu_k C`; if `mu_k=0` it is impossible,
    and otherwise the actual `C` is monomial.  This excludes every correcting
    zero, including coordinate `x` or `y` walls.

## Adversarial checks and scope controls

- Three independent research lanes reconstructed the complete slices,
  structural-zero census, correcting rank fork, one-target plane collapse,
  and retained-slice quotient.  All returned mathematical PASS verdicts.
- An early shortcut incorrectly tried to infer nonzero correction
  coefficients on coordinate `x` or `y` walls.  It was retracted.  The final
  proof uses the perfect-pairing plane collapse and the full-slice quotient;
  if the remaining scalar is zero, the target equation itself is already a
  contradiction.
- The theorem consistently distinguishes the actual residual block `C` from
  its restriction modulo `A_1 tensor y+x tensor A_2`.  Only the final complete
  slice promotes a quotient localization to an actual-monomial conclusion.
- The structural atlas counts underlying projective zero pairs, not scheme
  length or multiplicity.  It is conditional on a zero pair; the theorem does
  not claim one exists.
- No degeneration, generic-point promotion, numerical solve, modular result,
  saturation, or hidden localization enters the proof.  Characteristic zero
  supplies an infinite field and the inherited permanent/tensor lemmas.
- The primary and independent scripts replay algebraic interfaces.  The
  written proof owns the S2R tensor-rank application, S2CG radical and
  zero-pair classification, S2CK mixed-map application, and source-factor
  quotient geometry.

## Evidence matrix

| Evidence axis | Result |
|---|---|
| Mathematical status | proved exact reduction and correcting-zero exclusion |
| Scope | fully-injective `(3,3,3)` joint-rank-four/derivative-rank-eight actual nonmonomial residual |
| Structural coverage | exact union, at most four projective zero pairs |
| Primary replay | deterministic symbolic exact arithmetic |
| Independent audit | no-import standard-library exact rational arithmetic |
| Formalization | not formalized in Lean |
| Global status | **UNRESOLVED** |

## Validation

The focused primary and independent replays, Ruff, candidate-tree hygiene,
the migration and lattice unit suites, and the zero-change link rewrite must
all pass on the staged candidate tree before checkpointing.  A timeout or
missing script is not accepted as evidence.

## Remaining obligation

Inside this local rank cell, the next exact split is

```text
actual nonmonomial residual:
  structural mixed zero present:   at most four explicit points, OPEN;
  no mixed zero present:            OPEN.
```

These local successors do not discharge lower-rank derivatives, pair
regularity elsewhere, other components or poles, higher balanced orders, or
the global extraction/unavoidability bridge.
