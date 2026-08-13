# Self-review: Hilbert--Burch `(1,1,2)` third-colour coloop exclusion

Date: 2026-08-13

Claim under review:

[`BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_THIRD_COLOUR_COLOOP_EXCLUSION_THEOREM.md`](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_THIRD_COLOUR_COLOOP_EXCLUSION_THEOREM.md)

Global status after this claim: **UNRESOLVED**.

## Scope and adversarial questions

### 1. What exact S2AS residual is treated?

Only the distinct-colour central coordinate-pair chart
`x=lambda e_s`, `y=mu e_t`, with `s,t,u` pairwise distinct and with the
S2AS outer-line exclusions `w` not proportional to `e_s` and `z` not
proportional to `e_t`.  Of the four ordinary coloops left by S2AS, this
claim excludes `alpha_u=0` and its first/second-root symmetric mate
`beta_u=0`.

It does not treat `alpha_t=0`, `beta_s=0`, the two repeated outer lines,
the same-colour central chart, or an outer coordinate-pair chart.

### 2. Does hyperplane containment really give the stated row geometry?

Yes.  The seven rows

```text
r_t,r_u,p_s,p_u,h_0,h_1,h_2
```

are the images of a basis of the seven-dimensional derivative-kernel
annihilator.  Their relation kernel is the four-plane `N`.  If
`N subset {alpha_u=0}`, deleting `r_u` leaves a six-dimensional domain
whose kernel is still `N`; its image therefore has dimension two.  It
contains `p_s,p_u`, already an independent pair, so it is exactly
`S=P`.  It also contains `r_t` and every `h_k`.  The omitted `r_u` is
outside `S` because all seven rows span a three-space.

### 3. Is `per(r_t,S,Q)=0` an inferred or an untouched identity?

It is the exact untouched table from S2AS.  For distinct `s,t,u`, the only
nonzero target in

```text
span(r_t,r_u) x span(p_s,p_u) x image theta
```

is the `(u,u,u)` entry.  Thus the complete `r_t` row is zero.  Replacing
`P` by its proved equality `S=P` gives the displayed zero table without
using a touched coefficient.

### 4. Why is the third-row image three-dimensional rather than merely at least two?

Let `L=(ker D_B)^perp` and `V=H^T(L)`.  Since `ker H^T=N subset L`, the
map induced by `H^T` from the two-dimensional quotient of the full root
dual by `L` to `W/V` is injective.  Both spaces have dimension two, so the
classes of `A=lambda^(-1)r_s` and `B=mu^(-1)p_t` are independent modulo
`V`.  Modulo `V`,

```text
q(gamma)=gamma(z)A+gamma(w)B.
```

Independence of `z,w` therefore gives quotient rank two.

For `0!=n in z^perp intersect w^perp`, `q(n)=h(n)` lies in `S`.  If it
vanished, `n` would annihilate `pr_3 K`.  Third-root contraction would
then kill the all-cross term and all of `D_B(K)`: the derivative's first
two summands have third factors `z,w`, while its last summand has third
factor in `pr_3 K`.  The target contraction `sum n_c T_c` is nonzero.
Thus `q(n)!=0`, adding one direction to the quotient rank two and proving
`dim Q=3`.

### 5. Does the exterior face really become a square?

Yes.  On `gamma in z^perp`, S2AS gives

```text
per(r_t,B,q(gamma))=c gamma_t T_t,  c!=0.
```

The restrictions of `gamma_t` and `gamma(w)` to `z^perp` are nonzero by
the explicit outer-line hypothesis and independence of `z,w`.  Over the
infinite characteristic-zero field one may avoid their two kernel lines.
For such a `gamma`,

```text
q(gamma)=gamma(w)B+h(gamma),  h(gamma) in S.
```

Trilinearity and `per(r_t,S,Q)=0` give

```text
per(q(gamma),q(gamma),r_t)
 =gamma(w)per(B,q(gamma),r_t)!=0.
```

No division by a possibly zero coordinate is used.

### 6. Is the three-source square kernel exactly two-dimensional?

Yes.  For `r_t=x+y+zeta` with all components nonzero,

```text
per(r_t,r_t,q)
 =2(q_X tensor y tensor zeta
    +x tensor q_Y tensor zeta
    +x tensor y tensor q_Z).
```

Vanishing first forces each off-line component of `q` to vanish and then
forces the sum of the three line scalars to be zero.  The kernel is the
two-dimensional scaling plane.  It cannot contain the proved
three-dimensional `Q`.

### 7. Is the two-source tangent kernel only one-dimensional?

Yes.  For `r_t=x+y`, square-zero puts `Q` in `X direct-sum Y`.  The mixed
map is

```text
per(r_t,p,q)=p_Z tensor (x tensor q_Y+q_X tensor y).
```

The parenthesized map has kernel `span(x,-y)`.  Since `dim Q=3`, it cannot
vanish on all of `Q`; hence every `p in S` has `p_Z=0`.  Then `S,Q` both
miss the third source and every square with `r_t` vanishes, contradicting
the nonzero `T_t` square.

### 8. Does the pure-source equation impose the claimed conjugate lines?

Yes.  After taking `r_t=x in X`, write the square vector as
`q=(q_X,y,zeta)`, with `y,zeta` nonzero.  For every `p in S`, the zero
table is

```text
p_Y tensor zeta+y tensor p_Z=0.
```

The two rank-one summands can cancel only when
`p_Y=a(p)y` and `p_Z=-a(p)zeta`.  Uniqueness makes `a` a linear
functional on `S`.

### 9. What happens if `a=0`?

Then `S subset X`.  The nonzero `T_s` exterior face, the `T_t` square, and
the untouched `T_u` core have middle rows `p_s`, `r_t`, and `p_u`,
respectively.  Because those rows are pure in `X`, they supply the three
target `X` factor lines.  These are the independent coordinate lines
`X_s,X_t,X_u`, but all three rows lie in the two-plane `S`.  This is a
dimension contradiction.

### 10. What happens if `a` is nonzero?

Choose `p_0` with `a(p_0)!=0`.  The zero table makes every `q' in Q`
satisfy

```text
q'_Y=b(q')y,  q'_Z=b(q')zeta.
```

A direct six-term expansion, including cancellation of the `C_X` terms,
gives

```text
per(C,p,q') in
 X tensor Y tensor span(zeta)
 +X tensor span(y) tensor Z.
```

Projection to `X tensor (Y/span(y)) tensor (Z/span(zeta))` shows that a
nonzero decomposable tensor in this sum shares the `Y` line `span(y)` or
the `Z` line `span(zeta)` with `T_t`.  The required `T_s` exterior and
`T_u` core values are both of this form and are fully transverse to
`T_t`, a contradiction.

### 11. Is the second coloop orientation genuinely symmetric?

Yes.  Exchange the first two root variables and the corresponding first
two source factors, and exchange `s,t` and `z,w`.  The Hilbert--Burch
normal form, outer-line hypotheses, untouched table, and exterior faces
are preserved.  `alpha_u=0` becomes `beta_u=0`.

### 12. What do the replays establish, and what do they not establish?

The primary SymPy replay checks the coloop ranks, quotient and full
third-row ranks, normal contraction, square upgrade, exact square/tangent
kernels, conjugate-row expansion, and quotient factor sharing.  The
independent audit imports no repository or third-party code; it uses
`Fraction`, separate row reduction, a third-index-major tensor convention,
and its own derivative and permanent implementations.

The Markdown argument is the proof.  The scripts replay its load-bearing
linear and multilinear identities; they are not a finite search standing
in for the characteristic-zero argument.

### 13. What remains open?

The distinct-colour central chart still has the symmetric central-colour
coloop orbit `alpha_t=0` or `beta_s=0` and the repeated outer-factor lines.
The same-colour central chart, outer coordinate-pair charts, other
`(1,1,2)` boundaries, `(1,2,2)`, joint rank at most four, other physical
branches, higher orders, and the global conjecture remain open.

## Review conclusion

The coloop rank reduction, third-row rank upgrade, exterior square, and
complete source-support split survive the adversarial checks above.  The
claim is appropriately scoped as an exact exclusion of one ordinary-coloop
orbit.  Global Krenn--Gu remains **UNRESOLVED**.
