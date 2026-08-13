# Self-review: transverse rank-six aligned-rank-two exclusion

Date: 2026-08-13

## Reviewed claim

The new theorem excludes only the non-coordinate-relation alternative of the
balanced `m=3`, common-three-space, joint-rank-six transverse branch.  It
assumes the exact S2AD normal form and one aligned involved row of rank two.
It does not exclude the coordinate-relation-plane alternative, joint rank at
most five, another physical component, or any higher order.  Global
Krenn--Gu remains `UNRESOLVED`.

## Hostile reconstruction

I rebuilt the argument from the coefficientwise common-shore equations rather
than treating the earlier localization prose as a black box.

1. The aligned row gives `p_0=0`, while S2AD gives the diagonal contraction
   `B_(0,-)=kappa e_0`.
2. If the other row also had rank two, the zero root-2 slice of `G_N` could
   not absorb the `T_0 E_000` target coefficient.  Thus the other row has
   rank three and `K_12` is the graph of a rank-two map `T`.
3. The relation-plane contraction and the beta-zero torus atlas force
   `B=kappa e_0 tensor e_0`; the tempting noncoordinate alternative would
   make `C` a coordinate monomial and reintroduce a derivative intersection.
4. Coefficientwise target consistency then gives the full identity

   ```text
   G_N=T_1E_111+T_2E_222-kappa^(-1)T_0 C tensor T(e_0).
   ```

5. Since the second permanent row is `T` applied to the first, coefficient
   matrices have the form `S T^T` with `S` symmetric.  This forces the two
   surviving coordinate columns of `T` to be diagonal and
   `C=lambda e_0 tensor e_0+k tensor w`, where `k=ker T`.
6. A repeated-row contraction is a Segre-tangent tensor of mode ranks at most
   two.  If `lambda` were nonzero, its exact target would be a three-term
   diagonal of mode rank three.  Hence `lambda=0`.
7. On `k^perp`, the remaining correction vanishes and the full permanent is a
   symmetric binary square pencil: its cross term is zero and its two squares
   are distinct coordinate product tensors.  The zero/one/two/three
   pair-tensor atlas rules this out on a three-plane.

## Correction made during review

An initial derivation incorrectly strengthened the zero root-2 slice to
`E_000 in U`.  That is false: the `T_0` coefficient of `G_N` can have entries
in the other second-root rows.  The proof now retains the unique graph
preimage of that whole coefficient.  The corrected statement is equation
(18) of the theorem; both implementations reconstruct all 27 root
coefficients and check the nonzero off-slice control.

This correction is load-bearing.  No conclusion in the theorem uses the
discarded stronger claim.

## Adversarial checks

- **Both involved rows rank two.**  Checked separately before introducing the
  graph map; target absorption fails in the missing coordinate.
- **Noncoordinate first root block.**  The torus argument was rerun with the
  quantifiers in the correct order.  One fixed fully supported annihilator of
  `b` forces every torus value of `C` onto a nonzero coordinate line;
  irreducibility and nonvanishing make `C` a coordinate monomial.
- **Exceptional columns of `T`.**  Density of `L^circ` is used exactly to say
  that all three columns of `T` are nonzero.  No division by `t_1` or `t_2`
  occurs; either may vanish.  Only `tau_1,tau_2` are divided by, after their
  nonvanishing is proved.
- **Exceptional factor `lambda=0`.**  It is not discarded after the tangent
  argument.  It becomes the separate symmetric binary-square problem in
  Sections 6--7.
- **Mixed-product rank drops.**  Lemma 1 treats zero, one, two, and three
  nonzero pair tensors.  In the two-tensor case, both the no-shared-factor
  three-dimensional kernel and the shared-factor four-dimensional kernel are
  checked.  Boundary solutions make a square zero rather than escaping the
  case split.
- **Generic-point leakage.**  The only chosen covectors avoid finitely many
  hyperplanes over an infinite characteristic-zero field.  The final kernel
  lemma is pointwise and includes every rank-drop chart.
- **Target-line use.**  The last contradiction needs the two target tensors
  to have distinct factor lines in all three nonroot sources.  They are
  exactly `T_1=X_1Y_1Z_1` and `T_2=X_2Y_2Z_2`; no generic target is inferred.

## Verification independence

The primary verifier uses SymPy matrices and column-oriented tensor maps.  It
checks the graph and relation spaces, derivative rank six, every coefficient
of the corrected target identity, the symmetric pullback, tangent flattening
ranks, and representative controls for all four kernel cases.

The audit imports neither SymPy nor repository code.  It uses a separate
row-oriented `Fraction` implementation, its own elimination, and separately
reconstructs the block derivative, tensor flattenings, pair blocks, kernel
restrictions, and graph transpose calculations.  The scripts replay the
displayed algebra; the irreducibility and arbitrary-three-plane dimension
arguments remain the written proof.

## Remaining boundary

The theorem leaves exactly the coordinate-relation-plane alternative at
joint rank six.  A successor must impose the full permanent equation after
one coordinate of one projection of `L` vanishes identically.  It must not
reuse the graph-isomorphism step unless the relevant opposite row is first
proved to have rank three.
