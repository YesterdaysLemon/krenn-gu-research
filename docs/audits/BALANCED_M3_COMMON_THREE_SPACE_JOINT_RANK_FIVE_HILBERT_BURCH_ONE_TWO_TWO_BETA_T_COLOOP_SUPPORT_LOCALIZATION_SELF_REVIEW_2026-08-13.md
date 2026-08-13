# Self-review of the `(1,2,2)` `beta_t`-coloop support localization

## Review verdict

The claimed localization is supported.  In the S2AZ gauge, the distinguished
second-root coloop `N subset {beta_t=0}` forces `w` onto one of the two target
coordinate lines complementary to `e_t`.  It also proves that the second-
and third-root row maps are injective, forces `y` coordinate when `s=t`, and
forces `span(z,w)` to contain a target coordinate different from `e_s`.

This does not exclude the two coordinate endpoints for `w`.  The other eight
coordinate coloops are untouched.  The global conjecture remains
**UNRESOLVED**.

## Scope and inheritance audit

### Is `beta_t` one of the S2AZ alternatives?

Yes.  S2AZ produces the nine ordinary coordinate hyperplanes
`alpha_i=0`, `beta_j=0`, and `gamma_k=0`.  Its gauge singles out the
coordinate `t` through `c=mu e_t`; this theorem treats only `beta_t=0`.

No symmetry claim identifies this orientation with every other `beta_j` or
with a `gamma_k` orientation, because the normal form treats `y,z,w` and the
gauge coordinate asymmetrically.

### What does the coloop hypothesis actually imply?

It implies that the image of the six-dimensional hyperplane
`L intersect {beta_t=0}` is the exact two-plane `R`.  The proof uses only
covectors that visibly lie in that hyperplane.  It does not infer that raw
rows `p(beta)` or `q(gamma)` lie in `R`; the correction terms involving
`A=lambda^(-1)r_s` are retained:

```text
p(beta)-beta(y)A in R,
q(gamma)-gamma(z)A in R.
```

Thus the main complete face lies in `R+span(A)`, a space of dimension at
most three.  No equality `A in R` is assumed.

## Root-row rank audit

### Why are `pi` and `theta` injective?

The full row image has dimension five and the image `V` of the
seven-dimensional derivative-kernel annihilator has dimension three.  The
S2AZ quotient formulas make `E/V` the two-space with basis `[A],[B]`.

The quotient of `pi` is the rank-two map

```text
beta |-> beta(y)[A]+mu beta_t[B],
```

because `y,e_t` are independent.  Its kernel is the line
`y^perp intersect e_t^perp`.  If its nonzero generator `u` had `p(u)=0`,
second-root contraction by `u` would kill the all-cross term and all of
`D_B(K)`, while the target diagonal contraction is nonzero.  Therefore that
kernel line supplies a third independent row direction.

The same argument applies to

```text
gamma |-> gamma(z)[A]+gamma(w)[B]
```

and the line `z^perp intersect w^perp`.  Thus both maps have rank three and
are injective.  In particular `q_t` cannot vanish; this is the load-bearing
fact that removes the apparent support-two endpoint.

## Complete-face audit

### Is the `3 x 2 x 2` derivative-zero face exact?

Yes.  In the transposed derivative, the three component scalars are

```text
beta(y)gamma(w)-mu beta_t gamma(z),
-lambda alpha_s gamma(w),
lambda mu alpha_s beta_t.
```

They vanish identically when `beta_t=gamma(w)=0`, with no annihilator or
genericity assumption.  Since `U=D_B(K)`, the complete target equation gives

```text
per(r(alpha),p(beta),q(gamma))
 =sum_i alpha_i beta_i gamma_i T_i
```

on the entire displayed product of linear spaces.

### Why does `w_t!=0` give a complete binary cube?

The restriction `w^perp -> span(e_a,e_b)^*` has determinant proportional to
`w_t`.  When it is nonzero, the two coordinate lifts of `e_a^*,e_b^*`
exist.  Substitution into the complete face gives all eight binary cells,
not merely the two desired diagonal cells.

The diagonal and crossed cells make each of the three row pairs independent.
Their span lies in a space of dimension at most three.  If it is
two-dimensional, all three row planes agree and the equal-plane calculation
from S2AN applies; if it is three-dimensional, the complete S2AN incidence
lemma applies.  Thus `w_t=0` without assuming exact ambient dimension three.

## Auxiliary-face and incidence audit

### Are the two auxiliary faces derivative-zero?

Yes.  Let

```text
span(u)=y^perp intersect e_t^perp,
span(v)=z^perp intersect w^perp.
```

Substitution into the displayed transpose shows it vanishes on

```text
alpha_s=0, beta=u, gamma arbitrary,
alpha_s=0, gamma=v, beta arbitrary.
```

The resulting complete target identities are exact.  The rows `p(u)` and
`q(v)` lie in `R`, because their pure direct-sum covectors belong to
`L intersect {beta_t=0}`.

### Why do two active target coordinates give a contradiction?

The two first-root rows outside `s` form a basis of `R`.  Express `p(u)` or
`q(v)` in that basis.  If both coefficients are nonzero, its square map
contains two fully transverse targets, contrary to the S2AL tangent-line
lemma.  If one coefficient vanishes, the surviving square and mixed maps are
rank-one onto fully transverse targets, contrary to S2AL mixed factor
sharing.  Injectivity of `theta` or `pi` ensures that the two target
coordinate functionals on the varying three-dimensional shore are
independent.

For `u`, two active coordinates can occur only when `s=t`; their product is
`-y_a y_b`, so `y` must be coordinate.  For `v`, at least one coordinate
outside `s` must vanish.  Since `v` is the normal to `span(z,w)`, this is
equivalent to that plane containing some `e_i` with `i!=s`.

## Support-two boundary audit

### Is the split exhaustive once `w_t=0`?

Yes.  Because `w` is nonzero, either exactly one of `w_a,w_b` is nonzero,
which makes `w` a target-coordinate vector, or both are nonzero.

### Why is the genuinely two-supported case impossible?

Its annihilator has basis

```text
w_b e_a^*-w_a e_b^*,       e_t^*.
```

The first row gives two fully transverse target diagonals on a common third
row and the second gives the other six zero cells.  Injectivity of `theta`
makes `q_t` nonzero.  It is independent of the first row, because
proportionality would turn either nonzero diagonal into zero.  The resulting
three two-planes again lie in a space of dimension at most three.  The
equal-plane case or the complete same-third-row lemma of S2AO gives a
contradiction.  Hence `w` has exactly one complementary coordinate.

## Computational independence

The primary verifier uses SymPy to check the main derivative-zero face,
the two row-rank forks, both auxiliary derivative-zero faces, the
coordinate-plane normal identity, and both complete binary tables.

The independent audit imports neither SymPy nor the primary verifier.  It
uses `fractions.Fraction`, its own Kronecker construction, cross product, and
Gaussian elimination to rebuild the same faces, restriction bases, row
ranks, and tables.

The scripts replay the displayed identities.  The S2AL coefficient fork and
the S2AN/S2AO plane-incidence obstructions are written proof dependencies,
not relabelled computational results.

## Remaining obligations

The live residual in this orientation consists of

```text
w proportional to e_a or e_b,
s=t only if y is also coordinate,
span(z,w) containing e_i for some i!=s.
```

Neither endpoint is proved realizable.  The other eight `(1,2,2)` coloops,
lower joint rank, other physical component types, higher orders, and global
resolution remain open.  Global Krenn--Gu status is **UNRESOLVED**.
