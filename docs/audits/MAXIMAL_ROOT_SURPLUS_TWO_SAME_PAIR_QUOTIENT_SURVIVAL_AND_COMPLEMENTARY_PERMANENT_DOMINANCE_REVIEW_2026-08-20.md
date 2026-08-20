# Maximal-root surplus-two same-pair survival and permanent dominance hostile review -- 2026-08-20

## Verdict

**Accepted as an exact, scoped first tranche at the frozen file hashes below.**
No counterexample or invalid load-bearing inference was found.  The theorem
proves one source-to-individual-supply edge for every actual maximum-root
surplus-two hypothetical complex witness.  It does **not** close the strategic
supply-and-target-attachment node, prove collective pair-observability or full
fixed-`Q` coordinate-family observability, or supply a legal GLD target
selector.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Source, field, and quotient scope

The conditional algebraic theorem is characteristic zero.  Its actual-witness
corollary remains over `C`, matching M1.  M1's five-outside-mode bound rules out
`r=2` at surplus two, so the corollary's `r>=3` scope is correct.

The reviewed quotient is explicitly the generic-point GLS2 quotient over the
outside function field `K(X)`.  Contracting every root slot with the fixed
maximum-root vectors gives a `K(X)`-linear functional on the generic target
fibre.  Every order-four-and-higher companion has positive root--root grade, so
each of its matching terms contains a root edge killed by the maximum-root
zero.  The order-two column `G_(B-Q)` instead maps to the generic evaluation of
the complementary permanent tensor `Pi_Q`.  Therefore `Pi_Q!=0` proves that
this one column survives modulo the entire higher-column image.  No minor,
coordinate, denominator, or exceptional factor is divided out.

This conclusion is individual quotient survival.  It does not say that the
order-two columns are collectively independent or that all coordinates of a
fixed-`Q` GLS2 block are identifiable.

## Same-pair proof audit

Assume for contradiction that every active pair has every raw
`p_(A,Q)` equal to zero.  For an active `Q={u,v}`, each nonzero incidence image
then lies in the off-diagonal symmetric-product kernel of a nonzero vector.
That kernel has dimension at most one in characteristic zero, so both endpoint
incidence maps have rank one.  The corank-six quota leaves only two cases.

If exactly two outside modes have rank one, only their pair can be active.
The left side of the contracted target has flattening rank one across that
pair and its complement, while the three nonzero pure target tensors have
rank three.  This is impossible.

If exactly three modes `a,b,c` have rank one, expansion at the remaining low
column gives

```text
Pi_(bc)=ell_a tensor K_a,
Pi_(ac)=ell_b tensor K_b,
Pi_(ab)=ell_c tensor K_c.
```

Quotienting the three low-mode dual spaces by their `ell` lines kills every
left summand.  Independence of the three pure tensors on the high shore forces
the three coordinate colours to occupy the three low lines bijectively.  The
reviewed proof explicitly permits rescaling the rank-one factorizations before
normalizing those lines to coordinate covectors.  The low pure words then
force `K_a,K_b,K_c` to be nonzero and pairwise independent.

All three high tensors arise from one linear cofactor map
`Psi(v)=sum_i v_i D_i`.  Raw failure for `{a,b}` and `{a,c}` puts both
`alpha_b` and `alpha_c` in the at-most-one-dimensional space
`S_(alpha_a)`.  Their proportionality makes `K_b` and `K_c` proportional
under the same `Psi`, contradicting the pure-word conclusion.  Hence some
active same pair has nonzero raw incidence.  Density of the fully supported
torus over the infinite characteristic-zero field supplies the stated
residual evaluation; it does not assert nonzero GLD response at that point.

## Complementary-permanent dominance audit

At `A_0=[I_r|1|1]`, the complementary permanent coordinates are `1` after
deleting the final two columns, `1` after deleting one identity and one final
column, and `2` after deleting two identity columns.  For `i<j`, the direction

```text
D_ij=partial_(x_ij)-partial_(a_i)-partial_(b_i)
```

kills every output except the coordinate deleting identity columns `i,j`,
where its derivative is `-2`.  These directions give a diagonal `-2I` block;
the `a_i`, `b_i`, and `x_11` directions give two identity blocks and one final
unit after elimination.  The selected Jacobian minor is therefore
`plus-or-minus 2^(binom(r,2))`.  This proves dominance when `2!=0` and hence no
ambient universal polynomial relation among the scalar complementary
permanents.

The conclusion does not rule out identities on the physical target locus or
identities using tensor polarizations, higher companions, or same-graph
matching recurrences.

## Independent evidence

The focused primary verifier uses exact SymPy permanents and Jacobians.  It
replays matching grades and root contraction for `r=3,4`, the rank-one
triangle for `r=3,4`, and full complementary-permanent Jacobian ranks and the
displayed minor for `r=2,...,6`.

The no-import audit is standard-library only.  It imports neither the primary
verifier nor project code nor SymPy.  It uses sparse tensor-word dictionaries,
direct permutation expansion, and separately implemented rational row
reduction for the triangle and cofactor identities at `r=2,...,5` and the
Jacobian at `r=2,...,5`.  It reports `AUDIT_PASS`.  The hostile reviewer also
reconstructed the Jacobian independently and obtained full ranks
`6,10,15,21` at `r=2,3,4,5`.

These bounded programs replay identities and conventions.  The written
arbitrary-`r` matching-grade, quotient, symmetric-kernel, triangle, and
Jacobian arguments are the proofs.

Frozen at base HEAD `a16315f145324b503c3ec0ccd017ee7562f9626d`:

```text
theorem  f887dd58c724160fa7b52df24385f7f89311ac410373c636069e7b420b027466
primary  d73c8ed6882eea8ae3e46aad1fce4781fbc7bf2140353b8e805c347af716d474
audit    4232fd5e0e5648fedaa8d57c31c64bd492dbf6d7c2a9fbd6042028ba6d6e06a0
```

## Exact remainder

For every actual source point, use at least one now-guaranteed supplied pair
`Q` to construct the complete legal same-`Q` response/target-selector package,
or exclude every simultaneous attachment failure on the same graph.  This
still requires full nuisance legality; response-zero and exceptional-rank
fibres; every relevant selector rank, slope, and visibility alternative; the
GLD2 augmented-weight, alignment, synchronization, and anchor gates where
that detector is used; and pointwise coverage for every `r>=3`.  Collective
or full fixed-`Q` observability also remains necessary whenever the chosen
downstream entry uses it.
