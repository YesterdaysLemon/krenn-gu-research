# Self-review: Hilbert--Burch `(1,1,2)` central-colour coloop exclusion

Date: 2026-08-13

Claim under review:

[`BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_CENTRAL_COLOUR_COLOOP_EXCLUSION_THEOREM.md`](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_CENTRAL_COLOUR_COLOOP_EXCLUSION_THEOREM.md)

Global status after this claim: **UNRESOLVED**.

## Scope and adversarial questions

### 1. What exact residual is excluded?

Only the central-colour ordinary-coloop orbit in the distinct-colour
central coordinate-pair chart of S2AS:

```text
alpha_t=0,                         beta_s=0,
```

where `x=lambda e_s`, `y=mu e_t`, and `s,t,u` are distinct.  The repeated
outer-factor divisors `w proportional e_s` and `z proportional e_t` remain
outside the hypotheses.  The same-colour chart and the outer
coordinate-pair charts are also not treated.

### 2. Is the central-coloop row geometry different from S2AT's geometry?

Yes.  For `alpha_t=0`, it is `r_t` itself that is outside the two-plane
spanned by the other six annihilator rows.  The rows

```text
r_u,p_s,p_u,h_0,h_1,h_2
```

span a two-plane `S`, and `P=span(p_s,p_u)=S`.  The full seven-row image
still has dimension three, so `r_t notin S`.

### 3. Why does the same zero table survive when `r_t` is the coloop?

The table is an untouched physical identity, not a consequence of the
coloop.  In the distinct-colour chart the only nonzero target on

```text
span(r_t,r_u) x span(p_s,p_u) x image theta
```

is the `(u,u,u)` cell.  Hence every value on `r_t x S x Q` vanishes, while
`per(r_u,p_u,q_u)=T_u` remains nonzero.

### 4. Is `dim Q=3` proved independently of which ordinary row is the coloop?

Yes.  Modulo `V=H^T((ker D_B)^perp)`, the third rows have quotient

```text
q(gamma)=gamma(z)A+gamma(w)B.
```

The induced map from the full root dual modulo the derivative-kernel
annihilator to `W/V` is an isomorphism, so `A,B` are independent modulo
`V`.  Independence of `z,w` gives quotient rank two.  The common normal
`n in z^perp intersect w^perp` supplies a nonzero row `q(n)=h(n) in S`;
if it vanished, third-root contraction would kill the all-cross term and
`D_B(K)=U` but not the GHZ target.  Thus `Q` has dimension three.

### 5. Does the exterior face still become a square even though `r_t` is outside `S`?

Yes.  S2AS gives

```text
per(r_t,B,q(gamma))=c gamma_t T_t
```

on `z^perp`.  Choose `gamma` with `gamma_t gamma(w)!=0`, possible by the
two explicit outer-line hypotheses.  Since
`q(gamma)=gamma(w)B+h(gamma)` and `h(gamma) in S`, the zero
`r_t x S x Q` table kills the `h(gamma)` term and gives the nonzero square
`per(q(gamma),q(gamma),r_t)`.

### 6. Why does one-source support fail?

If `r_t=x in X`, the nonzero square fixes the `Y,Z` factor lines of `T_t`.
The zero table gives conjugate `Y,Z` components on `S`.  If the conjugating
functional is zero, `S subset X` and the two `S` rows in the core cannot
produce any permanent.  If it is nonzero, every third row has matching
`Y,Z` components and every decomposable core value shares one of the two
fixed lines with `T_t`, contrary to the full transversality of `T_u`.

### 7. Why does two-source support fail?

For `r_t=x+y`, set

```text
L(v)=x tensor v_Y+v_X tensor y.
```

The square is `2 L(q) tensor q_Z`, so both factors are nonzero.  The zero
table makes all `p in S` and `q' in Q` lie in conjugate fibres of

```text
M(v)=(L(v),v_Z).
```

The kernel of `M` is the one-dimensional line `span(x,-y,0)`.  A fibre
over one projective value therefore has dimension at most two, but
`dim Q=3`.

### 8. In the full-source case, which tangent space contains the square?

The tangent space at the repeated vector `q`, not the tangent space at
`r_t`.  Precisely,

```text
(1/2)per(q,q,r_t)
 =r_X tensor q_Y tensor q_Z
  +q_X tensor r_Y tensor q_Z
  +q_X tensor q_Y tensor r_Z.
```

This distinction is load-bearing.  The primary and independent replays
construct the map directly from the six-term permanent and do not replace
`q` by `r_t`.

### 9. Why must a decomposable tangent tensor share at least two base lines?

Project the tangent space to the three quotients obtained by modding out
two base factor lines.  A decomposable tensor in the tangent space has zero
image in each quotient.  For each pair, at least one of the corresponding
factor lines must be the base line.  The three pair conditions force at
least two shared base lines.

### 10. What if the square vector `q` has only two source components?

After permutation write `q=a+b` with `a in X`, `b in Y`.  For
`r_t=x+y+zeta`, put

```text
D=x tensor b+a tensor y,
M(p)=p_X tensor b+a tensor p_Y.
```

The zero equation is `D tensor p_Z+M(p) tensor zeta=0`.

- If `D!=0`, its exact kernel is the two-plane spanned by
  `(-x,-y,zeta)` and `(a,-b,0)`.  The common annihilator of that plane with
  `r_t` is exactly `span(q)`, contradicting `dim Q=3`.
- If `D=0`, the kernel is `span(a,-b,0) direct-sum Z`.  A two-plane inside
  `Z` has zero core.  Any other two-plane contains one nonzero `Z` row and
  one row with nonzero conjugate component; their two zero equations again
  force every `q' in Q` into `span(q)`.

These are exact linear alternatives, not a generic-rank assertion.

### 11. What if `q` has all three source components and `q_X` is independent of `r_X`?

Decomposability lets us write

```text
q=(a,b y,c zeta),                 b c!=0,
```

where `a` and `x=r_X` are independent.  If `b+c!=0`, the zero-map kernel
is an exact two-plane parametrized by the scalars on `y,zeta`; substituting
its two basis rows into the common annihilator equation leaves only
`span(q)`, too small for `Q`.  If `b+c=0`, the kernel is exactly `X`, so the
two `S` rows cannot produce the nonzero core.

### 12. What if all components of `q` align with those of `r_t`?

Write `q=(A x,b y,c zeta)`.  The zero-map coefficients are the three pair
sums

```text
A+c,                         A+b,                  b+c.
```

They cannot all vanish in characteristic zero with `b,c!=0`.

- If zero or one coefficient vanishes, every kernel row has at least two
  source components on the corresponding base lines.  Every decomposable
  core value therefore shares a factor with `T_t`.
- If exactly two vanish, after permutation the kernel is
  `X direct-sum Y`.  Quotienting the remaining zero table by the `Z` base
  line forces all of `Q` to have that fixed `Z` line, because the binary
  tangent map has only a one-dimensional kernel.  The core again shares
  the `Z` factor with `T_t`.

### 13. Are boundary values such as `b+c=0` silently divided away?

No.  The proof treats them separately.  The primary replay checks the
moving-factor `b=-c` kernel and the aligned zero-/one-/two-pair-sum
strata.  The independent audit rebuilds each kernel by rational row
reduction.  No coefficient used as a divisor is allowed to vanish in the
branch where division occurs.

### 14. Is `beta_s=0` covered by a valid symmetry?

Yes.  Swap roots one and two and their source factors, exchange `z,w`, and
exchange target colours `s,t`.  The normal form, outer-line hypotheses,
untouched table, and exterior-square construction are preserved.
`alpha_t=0` becomes `beta_s=0`.

### 15. What exactly is closed after this claim?

S2AT already excludes the third-colour ordinary coloops `alpha_u,beta_u`.
This claim excludes `alpha_t,beta_s`.  Therefore every ordinary coloop in
the distinct-colour central coordinate-pair chart is impossible away from
the two repeated outer lines.

The repeated outer lines, same-colour central chart, outer coordinate-pair
charts, other `(1,1,2)` boundaries, `(1,2,2)`, joint rank at most four,
other physical branches, higher orders, and the global conjecture remain
open.

## Review conclusion

The central-coloop plane, exact third-row rank, exterior square, all
one-/two-/three-source cases, and every tangent degeneracy survive the
adversarial checks above.  The theorem closes one exact chart, not the
whole `(1,1,2)` profile.  Global Krenn--Gu remains **UNRESOLVED**.
