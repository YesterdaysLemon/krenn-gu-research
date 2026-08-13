# Self-review of the residual second-root-coloop projective-pencil localization

## Review verdict

The claimed localization is supported.  Under either residual coloop
`N subset {beta_j=0}`, `j!=t`, the determinant-zero projective pencil puts
the first- and third-row planes and a nonzero line of the middle-row plane in
one at-most-three-space.  The new permanent lemma excludes a binary diagonal
frame with an arbitrary middle-plane intersection line.  Exact factorization
then forces one projective coordinate gate to vanish identically, and the
auxiliary third-root-kernel face supplies the stated endpoint support table.

This does not exclude a residual coloop or any one of its four ordered
coordinate endpoints.  Five other `(1,2,2)` coloop orientations, lower joint
rank, other physical components and pole strata, higher orders, and the
global conjecture remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## Inherited-scope audit

### Does the proof use `pi,theta` injectivity outside its scope?

No.  S2BC proves injectivity before selecting its `alpha_s`-specific coloop.
That argument uses only the S2AZ quotient formulas, the independence of
`y,e_t` and `z,w`, and complete target contraction.  It applies unchanged
under `N subset {beta_j=0}`.

### Is the selected middle row merely allowed to escape, or forced to?

It is forced.  The seven canonical rows span the three-space `V`.  Under the
residual coloop, both pure first-root rows, `g_k`, and all three `h_a` lie in
the two-plane `R`.  If `g_j` also lay in `R`, all seven would span at most
`R`, contrary to `dim V=3`.  Thus `g_j notin R`.  Since
`V intersect (R direct-sum span(A))=R` and `p_j=y_jA+g_j`, one has
`p_j notin S`.  No quotient representative is silently identified with a
row in `E` here.

## Projective-face audit

### Is the determinant face complete?

Yes.  For

```text
P_delta={beta:k beta(y)-h mu beta_t=0},
Q_delta={gamma:k gamma(z)-h gamma(w)=0},
```

the evaluation pairs `(beta(y),mu beta_t)` and
`(gamma(z),gamma(w))` lie on the same projective line.  With
`alpha_s=0`, their determinant is zero and all three components of the
gauge-fixed derivative transpose vanish.  The full target equation therefore
holds on all of `e_s^perp x P_delta x Q_delta`, not on selected samples.

### Why do the three row objects share an at-most-three-space under a
`beta_j` coloop?

Let `v` span `z^perp intersect w^perp`.  The pure covector `(0,0,v)` lies in
`L intersect {beta_j=0}`, so `q(v) in R`.  For fixed `delta`, the line
`P_delta intersect {beta_j=0}` is nonzero.  Choose `0!=beta_*` on it.

If its evaluation pair vanishes, `(0,beta_*,0)` lies in the selected
hyperplane and `p(beta_*) in R`.  Otherwise the surjective third-root
evaluation map supplies `gamma_* in Q_delta` with the opposite pair.  Then
`(0,beta_*,gamma_*)` lies in the selected hyperplane, so
`p(beta_*)+q(gamma_*) in R`.  Because `q(Q_delta)` is spanned by
`q(v),q(gamma_*)`, both cases put

```text
R, q(Q_delta), p(beta_*)
```

in `R+span(p(beta_*))`, of dimension at most three.  Injectivity makes
`p(beta_*)` nonzero and both full row planes two-dimensional.  Thus the
middle plane has a genuine nonzero intersection with the common space.

### Are the coordinate gates correct in all three positions of `s`?

Yes.  A covector plane with normal `n` projects isomorphically to the two
coordinates different from `s` exactly when `n_s!=0`.  The normals above
give

```text
L_P=k y_s-h mu delta_(s,t),
L_Q=k z_s-h w_s.
```

If both are nonzero, coordinate lifts give the exact binary diagonal table
on the common row space, which the new lemma excludes.  Hence their product
vanishes at every projective direction.  Over an infinite field it is the
zero homogeneous polynomial, and the polynomial ring is a domain, so one
linear factor is identically zero.  If `s=t`, `L_P=-h mu` is not zero and
`z_t=w_t=0`.  If `s!=t`, the gauge gives `L_P=k y_s`, producing exactly
`y_s=0` or `z_s=w_s=0`.  No generic direction is promoted to a pointwise
claim.

## Generalized binary-frame audit

### Does S2BD's first/third-plane incidence reduction depend on a named
middle row lying in the common space?

No.  Equality of the first and third planes is excluded by permanent
symmetry evaluated separately at `p_0,p_1`; their ambient positions are not
used.  When those planes are distinct, their intersection line exists inside
the common three-space.  Its two square values on `p_0,p_1` give the same
tangent-line and mixed-factor alternatives as S2BD.  Therefore it must be a
coordinate endpoint in both ordered planes.  Again, the location of
`p_0,p_1` is irrelevant to this reduction.

### Is the generic middle-intersection normal form exhaustive?

Yes.  If `P subset S`, the old three-plane obstruction applies.  If
`P intersect S` is either target-indexed row, S2BD applies after an optional
label swap.  Otherwise the intersection is `span(a p_0+b p_1)` with
`ab!=0`.  Independent row rescaling makes it `span(p_0+p_1)`.

After the four first/third endpoint choices, choose

```text
r_a=q_b=e_0, r_(1-a)=e_1, q_(1-b)=e_2, p_0=e_3.
```

The nonzero row `p_0+p_1` lies in the span of `e_0,e_1,e_2`.  Diagonal basis
scaling normalizes its nonzero coefficients to one, yielding exactly seven
nonempty support masks and

```text
p_1=epsilon_0e_0+epsilon_1e_1+epsilon_2e_2-e_3.
```

Thus four ordered endpoints times seven masks give all 28 generic-line
orbits.  There is no discarded continuous parameter.

## Certificate and independence audit

For every normal form, the 64 equations are the selected source-coordinate
coefficients of all eight binary row cells.  Only
`(source;row)=(000;000)` and `(111;111)` are one; the other 62 are zero.
Any full tensor-table realization must solve this subsystem, so a unit-ideal
identity is sufficient even though unused third source-coordinate lines are
unconstrained.

The compact durable artifact contains 28 rational identities and 20,582
sparse multiplier terms.  Its SHA-256 is
`0a92e61cef0b3db7940c68ea6e24bab4befb5dc1bd137ada581d0dbde4b9e0ca`.

The primary verifier reconstructs every row form, permanent, and generator
with SymPy before checking the identities.  The independent audit imports no
repository module or third-party package.  It reverses all 24 variables,
uses a separate direct six-permutation expansion, rebuilds the generators,
and accumulates every coefficient with `fractions.Fraction`.  The two paths
share the certificate semantics and mathematical normal forms, but not a
polynomial library, variable order, stored generator list, or multiplication
implementation.

Singular is used only for deterministic multiplier regeneration.  Neither
replay trusts a Gröbner-basis status report; both check `1=sum h_i f_i`
coefficientwise.

## Auxiliary-incidence and endpoint audit

The pure row `q(v)` is nonzero by `theta` injectivity and lies in `R`.  On
the complete face `alpha_s=0,gamma=v`, both coordinates of `v` outside `s`
cannot be nonzero: the S2BA coefficient fork would create either one square
map containing two fully transverse targets or two rank-one maps whose
fully transverse images must share a source factor.  Hence
`span(z,w)` contains a coordinate `e_i`, `i!=s`.

At `w=e_l`, with `m` the other colour complementary to `t`:

- If `s=l`, the projective fork cannot use `z_s=w_s=0`, so `y_s=0`.
  Together with `y_t=0` and independence from `e_t`, this gives
  `y parallel e_m`.  The auxiliary incidence is exactly `z_m z_t=0`.
- If `s=m`, the projective fork is `y_m=0` or `z_m=0`, hence
  `y_m z_m=0`.
- If `s=t`, it gives `z_t=0` (with `w_t=0` already known).

These are necessary conditions only.  The review does not infer an endpoint
construction or an endpoint exclusion from them.

## Remaining obligations

The result is exactly

```text
N subset {beta_j=0}, j!=t,
  w=e_l, l in {j,k}, subject to the endpoint table: OPEN.
```

The four ordered coloop/endpoint cases remain.  The three third-root and two
complementary first-root coloop orientations, joint rank at most four, other
physical components and low-span pole strata, higher orders, and global
resolution also remain open.  Global status stays **UNRESOLVED**.
