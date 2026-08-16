# Self-review: S2BW support-two third-row exclusion

Date: 2026-08-13

## Claim reviewed

S2BW excludes the S2BR same-missing-colour `(2,2,2)` cell in which the
one-dimensional third-row kernel has both complementary target colours in
its support.  Together with S2BU--S2BV, it closes the full same-colour
`(2,2,2)` profile for a rank-two third row.

## Adversarial checks

1. **Support-two normalization.**  S2BR proves that both shared tangent
   factors are the two complementary coordinate lines, in one order, and
   that the third-kernel covector is nonzero on `w`.  The proof exchanges the
   first two roots only to write those factors as `e_s,e_t`; it does not add a
   coordinate assumption on `w` or `C_bar`.

2. **Coefficient versus whole-column vanishing.**  The missing first and
   third rows kill the corresponding contractions of each physical source
   coefficient of `G_N`.  The proof does not incorrectly claim that a full
   correction coefficient vanishes.

3. **Third components.**  First-`d` contraction uses the isolated nonzero
   row `(e_d^* tensor id)C=kappa e_d`.  It fixes the whole third component of
   the `T_d` preimage and forces the whole third components of the `T_s,T_t`
   preimages to zero.

4. **Use of both kernel colours.**  The third-kernel contractions of the
   `T_s,T_t` coefficients are nonzero because both `eta_s,eta_t` are nonzero.
   If one vanished, the forced-vector argument would not apply; that is the
   separate support-one branch already handled by S2BT--S2BV.

5. **Tangent-map kernel.**  The kernel of
   `(a,b) -> a tensor e_t-e_s tensor b` is exactly the shared syzygy line.
   Quotienting by `e_s` and `e_t` establishes this without a hidden rank or
   genericity assumption.

6. **Forced representatives.**  Modulo the shared syzygy, the three target
   corrections force the exact lines `(0,0,e_d)`, `(0,e_s,0)`, and
   `(e_t,0,0)`.  All denominators are among the explicitly nonzero scalars
   `kappa,eta_s,eta_t,eta(w)`.

7. **Independence.**  The three forced lines plus `(e_s,e_t,0)` are visibly
   independent in `A_1 direct-sum A_2 direct-sum A_3`.  Since `dim K=4`, no
   fifth vector can restore a second third-projection direction.

8. **Contradiction target.**  The four forced vectors span a space whose
   third projection is exactly `span(e_d)`, so the transposed third root row
   has rank one.  This contradicts the cell hypothesis rank two; it is not a
   contradiction with an assumed coordinate basis artifact.

9. **Scope.**  No pair gate or source classification is needed.  The theorem
   closes support two only; the support-one graph cell is supplied by the
   separate S2BU--S2BV chain.  Third-row rank three, other involved-row
   profiles, lower-rank target cells, other components, higher orders, and
   all-rank drop remain open.  Global status remains `UNRESOLVED`.

## Independent evidence

The SymPy replay builds the derivative and the combined first-/third-root
contraction matrix, checks rank eight and its common syzygy kernel, verifies
all three affine representatives, and computes the forced projection ranks.
The no-import audit uses reverse tensor indexing and standard-library
`Fraction` row reduction to reconstruct the same affine systems
independently.  Neither implementation imports the other.

## Review result

**PASS for the complete support-two exclusion and the stated rank-two-third-
row profile closure.**  No broader resolution claim is supported or made.
