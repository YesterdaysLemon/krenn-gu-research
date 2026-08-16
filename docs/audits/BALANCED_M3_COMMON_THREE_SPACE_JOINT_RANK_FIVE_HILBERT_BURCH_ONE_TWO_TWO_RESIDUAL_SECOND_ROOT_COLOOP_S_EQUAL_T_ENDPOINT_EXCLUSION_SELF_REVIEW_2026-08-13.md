# Self-review of the residual second-root-coloop `s=t` endpoint exclusion

## Review verdict

The claimed slice exclusion is supported.  S2BF places the first- and
third-row planes and a nonzero line of the middle-row plane in one
at-most-three-space on every determinant-pencil member.  At a coordinate
endpoint with `s=t`, a generic pencil member is a same-third-row binary table
with both fully transverse targets active.  The new lemma excludes this even
when the middle-plane intersection is not a target-indexed row.

The result proves only `s!=t` under a residual `beta_j` coloop endpoint.  It
does not exclude the endpoint charts with `s in {j,k}` or any other open
branch.  Global Krenn--Gu remains **UNRESOLVED**.

## Scope and face audit

### Does `s=t` really make `z,w` a basis of `e_t^perp`?

Yes.  S2BF gives `z_t=w_t=0` in this slice.  The inherited `(1,2,2)` profile
requires `z,w` independent.  They are therefore two independent vectors in
the two-plane `e_t^perp` and form its basis.  No coordinate of `z` or `w`
is divided by individually.

### Does the required generic projective direction exist over every
characteristic-zero field?

Yes.  As `[h:kappa]` varies, the normal `kappa z-hw` traverses every
projective line in `e_t^perp`, because `(z,w)` is a basis.  Its annihilator
line inside `e_t^perp` also traverses the projective line bijectively.  The
conditions `h!=0`, `(gamma_*)_j!=0`, and `(gamma_*)_k!=0` remove at most
three projective points.  A characteristic-zero field is infinite, so a
direction remains.  This is finite hyperplane avoidance, not a generic-point
or algebraic-closure argument.

### Is the second-root coordinate lift exact?

Yes.  With `s=t` and `y_t=0`, the normal of

```text
P_delta={beta:kappa beta(y)-h mu beta_t=0}
```

has `t` coordinate `-h mu`, which is nonzero at the chosen direction.
Projection to the `j,k` coordinates is therefore an isomorphism.  Its two
coordinate lifts can have nonzero `t` components; the proof never replaces
them by pure coordinate covectors.  In the target equation `alpha_t=0`, so
those lift components contribute no target cell.

### Is the target table complete?

Yes.  The derivative transpose vanishes for every
`alpha_t=0`, `beta in P_delta`, and `gamma in Q_delta`.  Writing

```text
Q_delta=span(e_t^*,gamma_*)
```

and using coordinate lifts of `P_delta` gives

```text
per(r_a,p(beta^b),q(gamma_*))
 =delta_(a,b)(gamma_*)_aT_a,
per(r_a,p(beta^b),q_t)=0,
```

for all `a,b in {j,k}`.  Both active coefficients are nonzero by the chosen
direction.  This is the full eight-cell table, not a selected sample.

## Common-space audit

S2BF's construction applies to every projective direction under the residual
`beta_j` coloop.  The evaluation-kernel row of `Q_delta` lies in `R`.  A
nonzero row of `P_delta intersect {beta_j=0}` either lies in `R` or can be
paired with a `Q_delta` row having the opposite evaluation pair, whose row
sum lies in `R`.  Hence `R`, `q(Q_delta)`, and a nonzero line of
`p(P_delta)` lie in one at-most-three-space.  Injectivity of `pi,theta` is
proved in S2BC from the S2AZ gauge alone.  Thus neither the middle
intersection nor either row plane collapses silently.

## Generalized same-third-row audit

### Does the old plane-incidence reduction depend on a named middle row
lying in the common space?

No.  Equality of the first and third planes is excluded by permanent
symmetry evaluated at the two middle rows; their ambient locations are not
used.  For distinct planes, the square values on their intersection line
give the same tangent-line and mixed-factor alternatives.  Therefore the
zero third row is exactly the first/third-plane intersection independently
of the middle-plane incidence.

### Are all middle-plane intersections covered?

Yes.  If the entire middle plane lies in the common space, S2AO applies.  If
its intersection is either target-indexed middle row, S2BE applies after an
optional label exchange.  Otherwise it is

```text
span(a p_0+b p_1),        ab!=0,
```

which independent row rescaling normalizes to `span(p_0+p_1)`.

After setting `r_0=e_0,r_1=e_1,q_0=e_2,p_0=e_3`, the zero third row is
either an endpoint of `R` or generic in `R`, and the nonzero vector
`p_0+p_1` lies in `span(e_0,e_1,e_2)`.  The simultaneous diagonal action is
the same one classified in S2BE:

- 14 endpoint-support families;
- five generic fixed-support families;
- two generic parameter families.

In every family the actual escaping row is the normalized intersection row
minus `e_3`.  Thus the escape component is retained exactly.  The two
parameter families use `tau` symbolically; no nonzero parameter is replaced
by finitely many samples.

## Certificate and independence audit

Each family has 64 necessary selected source-coordinate equations.  Only
`(source;row)=(000;000)` and `(111;110)` are one; all other selected
coefficients vanish.  A full table realization must solve this subsystem, so
a unit-ideal identity is sufficient even though unused third source lines are
unconstrained.

The compact certificate contains 21 rational identities and 44,806 sparse
multiplier terms.  Its SHA-256 is
`ceb0c69b151523c43219d294806d50a1e1b2905bc7237c6a3709451fc868b9a0`.
The two parameter identities hold in the polynomial ring `Q[...,tau]` and
use no inverse, saturation, or specialization.

The primary verifier reconstructs every row, permanent, and generator with
SymPy.  The independent audit imports no repository module or third-party
package, reverses all 25 variables, represents `tau` by its own sparse map,
and rebuilds every permanent by six direct permutations with
`fractions.Fraction`.  Neither replay imports the generator or trusts a
stored generator list.

The optional generator reuses only the predecessor's proved Singular orbit
emitter, then makes the explicit row replacement `p_1 -> p_1-e_3`.  Singular
is not needed for replay, and its unit report is not trusted without the two
coefficientwise identity checks.

## Remaining obligations

The exact result is

```text
N subset {beta_j=0}, j!=t, w=e_l:
  s=t:                                           IMPOSSIBLE;
  s in {j,k}, subject to S2BF:                  OPEN.
```

The remaining endpoint charts, three third-root coloops, two complementary
first-root coloops, lower joint rank, other physical components and pole
strata, higher orders, and the global conjecture remain open.  Global status
stays **UNRESOLVED**.
