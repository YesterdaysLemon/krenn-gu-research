# Fixed-Q target quotient and global square-free Wick hostile review — 2026-08-17

## Verdict

**Accepted at the frozen hashes recorded below.**  No P0 or P1 defect remains.
The review initially found that the distinct-five-support six-port wall
asserted pointwise corank one from a determinant factorization without the
required pointwise argument, and that all four scripts needed formatting.
The theorem now includes the smooth-wall/adjugate proof and the exact
square-free kernel identity, and all scripts pass formatting.  These repairs
were reread and independently rerun.

The results are theorem-sized but scoped.  `GLD7` is a target-quotient
trichotomy and conditional attachment theorem.  `GLD8` is an exhaustive
**scalar** square-free support-union classification and bounded common-row
theorem downstream of legal row attachment.  Neither proves universal
attachment, a tensor-word cover on every witness, coefficient purity,
third-colour activity, or a permanent restriction.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## Frozen artifacts

```text
GLD7 theorem  A8873E2EC041761F043482AF5A83E86508F2AB27EFC23E166DC2294FC471EB8F
GLD8 theorem  6BC443DFB929E3A193C74993E7424056BB967D36D598A33A519B2BA504141D58
GLD7 primary  B67E0D1DED317B2613EF0C902457EC95A7DB23D922EC9C7E988E31ED8A312B90
GLD7 audit    302B11D7B60833AA258083B0C36218D6EC0BD93157277E13CAE262E8FA78CF29
GLD8 primary  C4F122123C1A42260A0C770B591A1AE283A29B84DA856D1612ABED81CCB91906
GLD8 audit    C192DD46B628F93E1D349FC8D7620507DA9107845475E88571C21057960D457B
README        E499D3EF04E070A490FFA3CC4558B2D4AF8C468C76FBFCDBBAB8AD65C64345CB
frontier      FE7A64261883C504629C827DD9D93D36B81316C71725511F37C65363AA594AAC
```

## GLD7: fixed-Q target quotient

The operator identity is exact.  From
`Gamma_Q=g_S tensor P_S+Theta_S` and the nuisance space containing every
coefficient slice of `Theta_S`, quotienting gives
`(pi_S tensor id)Gamma_Q=[g_S] tensor P_S` on the complete labelled deck
module, not merely at an observed diagonal value.  Applying the full
hypothetical-witness equation yields one decomposable tensor.  Because the
active pure port words are independent and every active contraction
coefficient is nonzero, the pure quotient span has rank at most one.

The active-colour and response quantifiers are correct.  One surviving active
pure class makes both `[g_S]` and `P_S(H)` nonzero, hence supplies the legal
constant-open-port selector.  Conversely, selector survival implies pure
survival only under `P_S(H)!=0`.  When the response is zero, all active pure
classes vanish but `[g_S]` remains undecided; the theorem preserves this
exception.

The simultaneous four-root statement keeps one graph, one residual pair, one
contraction, and target-specific functionals.  The six-root extension covers
exactly the fifteen pair, fifteen four-port, and one six-port sets, with the
full effective nuisance deck and correct dimensions.  It proves a conditional
trichotomy for each row; it does not force any of the thirty-one ranks to be
one.

Rank-one survival is not coefficient purity.  The dense-annihilator control
correctly shows why a selector can be exact while mixing pure coordinates.
No affine kernel is promoted to a physical graph fibre, and no permanent
implication is claimed.

## GLD8: exhaustive scalar support-union classification

The physical Wick map is literally multiplication by `ell_a ell_b` in the
square-free algebra.  Lemma 1's induction proves the one-step injection
threshold, and its degree-two block decomposition gives the complete
small-support nullity table.

The outside-union reduction is exhaustive: for supports at least five,
positive outside-degree blocks are injective and only
`A(V)_2 -> A(V)_4` can carry a kernel.  The union-at-least-seven proof covers
every remaining support pattern.  The `Y`-degree equations are complete
through degree three; `|Y|>=3` forces `m_0=0`, `|Y|=2` reduces to
`ell_C^3`, and the exceptional `|S|=6, |Y|=1` cases are closed separately
for `|C|=4` and `5`.  The reciprocal-triple-sum argument for `C=4` and the
quadratic-root/multiplicity argument for `C=5` are valid in characteristic
zero.

The resulting criterion is genuinely if and only if and pointwise: a support
of size at most four leaves a persistent first-factor kernel; union five has
exact nullity five; union six is decided by the published physical
determinant; union at least seven is coefficient-independent.

The repaired distinct-five-support wall is exact.  On the nonzero coefficient
torus, `grad e_2` cannot vanish along `e_2=0`.  Corank at least two would
annihilate the adjugate and hence all determinant derivatives, contradicting
the displayed determinant factorization.  Direct multiplication gives the
stated kernel vector and its nonzero `x_d x_y` coefficient.  The fixed nested
six/five rank-fourteen control remains a pointwise example, not a witness.

The one-sided kernel bases, intrinsic full-edge corollary, and twenty-one-row
selector all have the claimed quantifiers.  Full scalar edge support forces
both factor supports to have size at least `n-1` and their union to be all
ports.  For the twenty-one-row result, every named pair can be placed in a
seven-set containing five vertices of the smaller support; injectivity of the
restricted `35 x 21` map supplies a constant row minor after the graph
coefficient word is fixed.  The seven-port example kills exactly all five
principal six-windows containing the named zero pair, not every six-window on
the union.

The response interface is correctly downstream.  It reconstructs scalar
coefficients only after every used `z_4` tensor is legally attached.  Full
tensor recovery requires a coefficient-word cover satisfying the criterion
word by word.  One scalar word, a rational inverse, or one nonzero minor is
insufficient.  The breadth is all four-subwindows of one named port union; it
is not an arbitrary all-subwindow atlas.  `D/T` or scalar-row recovery is not
full `M,Z` agreement.

## Independent checks and controls

The four focused commands pass independently.  The `GLD7` primary and
no-import audit replay ranks zero through three, nonzero-column scaling, the
response-zero exception, the dense-annihilator purity control, and both
four-/six-root dimension ledgers.  The `GLD8` primary and no-import audit
independently construct the square-free/Wick matrices, verify the one-step
kernel table, union-five nullity, seven-port rank twenty-one with all five
relevant six-window determinants zero, the distinct-five determinant/kernel
control, and the nested full-edge rank-fourteen wall.  Ruff check and
format-check pass.

## Exact remainder

Still **UNKNOWN**: pure survival/rank one on every hypothetical witness;
exclusion of the swallowed-pure branch; legal same-`Q` attachment of every
required `z_2,z_4,z_6` row; a coefficient-word cover of all tensor entries;
the general tensor-valued witness singular locus; nonzero pure response and
third-colour activity for the depth-six detector; coefficient-pure mixed
syzygies; and weighted permanent extraction.  The frontier updates accurately
preserve these open edges.
