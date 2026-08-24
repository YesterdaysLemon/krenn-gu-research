# Fixed-Q globally decomposable channel variable-slope exclusion hostile review -- 2026-08-23

## Verdict

**Accepted within the exact scope below.**  No P0 or P1 defect remains in the
response theorem, fixed word cover, or conditional `GLD15` attachment.  The
package removes the common-pair-slope hypothesis from `GLD18`'s globally
decomposable-channel exclusion.  It does not force the branch on an arbitrary
hypothetical witness.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Reviewed artifacts:

- [theorem](../../claims/arbitrary-order/FIXED_Q_GLOBALLY_DECOMPOSABLE_CHANNEL_VARIABLE_SLOPE_THREE_FULL_PAIR_EXCLUSION_THEOREM.md),
- [primary exact replay](../../claims/arbitrary-order/verify_fixed_q_globally_decomposable_channel_variable_slope_three_full_pair_exclusion.py),
- [independent no-import audit](../../claims/arbitrary-order/audit_fixed_q_globally_decomposable_channel_variable_slope_three_full_pair_exclusion.py).

## Exact claim retained

On one physical `q=2`, `h=0` four-port response, assume all seven chosen rows
are on the finite `M`-active chart:

```text
D_e=B_e+p_eK_e,             T=C(B)+tX(B,K).
```

The six `p_e` and `t` are arbitrary and need not agree or satisfy a
cancellation polynomial.  Assume further that

```text
K_uv=a_u tensor a_v
```

through one common port vector at every vertex, all six `D_e` are diagonal,
and one named complementary pair is three-full.  Then one of thirty-six
`2+1+1` words, six named `2+2` words, or the fixed `3+1` word `(0,0,0,1)`
has nonzero four-port coefficient.

For a hypothetical witness, the conclusion becomes a contradiction only
after seven already legal constant operator rows from the complete `GLD15`
nuisance quotients are supplied.  The response theorem does not construct
those rows from observed diagonality.

## Hostile derivation audit

For each complementary partition, direct substitution of
`B_e=D_e-p_eK_e` gives the `GLD18` edge-dependent expansion.  Global vertex
factorization makes every `K_eK_f` matching on a fixed word equal the same
four-port monomial.  Writing the sum of its three coefficients as `G`, the
review checked the following chain without slope division:

1. A named `cc|dd` row rules out distinct diagonal channel zeros on opposite
   members of the three-full pair.
2. If one named channel diagonal entry is zero, a `2+1+1` row forces the
   opposite slope to equal `t`; a named `2+2` row then reduces to a nonzero
   product of the two three-full entries.  The symmetric case is identical.
   Thus all four port vectors have full ternary support.
3. Every `2+1+1` row now gives

   ```text
   (t-p_(bar g))D_g(c,c)+G K_g(c,c)=0.
   ```

4. The fixed `3+1` row is the sum of three such relations minus `2G` times a
   nonzero port monomial.  Characteristic zero forces `G=0`.
5. The two named three-full blocks then force both complementary slopes to
   equal `t`; a final named `2+2` row is a nonzero product.

Every finite slope coincidence, including `p_e=t`, remains inside the proof.
The proof does not divide by `G`, a response value, a selector coefficient,
or a channel minor.  The use of `-2G` is the exact reason the statement is not
claimed in characteristic two.

## Independent evidence

The primary replay uses SymPy and the inherited edge-dependent expansion.  It
checks all `3^4=81` matching monomials, constructs the forty-three-word
ledger, proves the `2+1+1`, `2+2`, and `3+1` formulas symbolically, and retains
the zero-support and slope-divisor substitutions.

The independent audit imports only the Python standard library.  It uses its
own sparse-polynomial arithmetic, constructs the response directly from
`C(D-pK)+tX(D-pK,K)`, and never imports the primary or `GLD18` verifier.  Its
separate support audit exhausts all `8^4=4096` choices of coordinate support
at the four port vectors.  The cover consists of `3942` distinct-opposite-zero
patterns, `90` first-named-edge boundary patterns, `63` opposite-edge boundary
patterns, and the single full-support pattern.  Seven rational fixtures give
an additional direct-response check across slope coincidences and signs.

## Rejected strengthenings and no-go routes

- **Cross-target annihilation is not foreign nuisance membership.**  The
  `GLS16` functional and the target whose nuisance is being tested have
  different open-port tensor types.  This tranche does not claim that
  `GLS15` transport defects vanish or that projective slopes synchronize.
- **Edgewise rank one is insufficient.**  The proof needs one vector `a_u`
  shared by every incident channel block so that all complementary matchings
  give the same monomial.  Six unrelated rank-one blocks are outside scope.
- **Three-colour activity is not three-fullness.**  The exact `GLD18` support-
  drop control has three-colour activity but no three-full edge.  The local
  hypothesis cannot be weakened that way.
- **Pure-`Z` axes are not finite slopes.**  The affine normalization requires
  a nonzero `M` coefficient at every pair target and the four-port target.
  Homogeneous closure polynomials do not silently extend the detector to an
  axis where the substitution `B=D-pK` is unavailable.
- **Response shape is not operator supply.**  A diagonal physical combination
  does not imply that the complete nuisance quotient contains its coefficient
  row.  The corollary assumes all seven legal `GLD15` identities.
- **Four ports are not arbitrary-root coverage.**  The result is a fixed
  four-port receiver branch and supplies no reduction from `r=3` or `r>=5`
  source witnesses.

The theorem is therefore a strict branch closure, not closure of the
maximum-root supply-and-target-attachment node and not a global proof.

## Dependency and validation record

Load-bearing dependencies are the exact `GLD15` legal-row semantics and the
`GLD18` physical response normalization.  The new primary independently
replays the algebraic expansion; the no-import audit constructs it from the
original `B,K` response.  Focused dependency replays and the repository
candidate-tree validation are required at the frozen candidate head.

Base `origin/main` before this tranche:

```text
6de39bd123195b5b091c9bb6174d9576bf495286
```

Frozen artifact SHA-256 hashes after final focused validation:

```text
theorem  5ec41b2080969f57a0df0070e42ded91ded5678f3d6cb699d6c2fcfce4431975
primary  15950bb77a95696b89316c5d9af6ac0b874eed1eff9bd02da5794447144db4d2
audit    71b73c74921b4b2cd3b02c57e3c1ed9dfedb42496b41879f68c9cb61fce59ff1
```

Exact candidate-head CI is a publication gate and is recorded on the hosted
PR before merge; these hashes do not substitute for that gate.

## Exact remainder

Still **UNKNOWN**: forcing even one nonzero legal operator row on every
witness; resolving zero spaces, response-invisible lines, and pure-`Z` axes;
forcing global decomposability or a three-full complementary pair; treating
general physical rank-two/nondecomposable channels; integrating the fixed
four-port receiver with arbitrary-root source coverage and every nuisance,
anchor, and activity gate; and every weighted-permanent consequence.
