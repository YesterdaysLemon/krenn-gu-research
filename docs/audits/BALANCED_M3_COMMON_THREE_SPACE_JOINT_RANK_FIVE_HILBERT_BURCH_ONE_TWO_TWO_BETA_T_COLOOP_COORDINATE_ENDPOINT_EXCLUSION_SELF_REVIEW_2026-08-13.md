# Self-review of the `(1,2,2)` `beta_t`-coloop coordinate-endpoint exclusion

## Review verdict

The claimed endpoint exclusion is supported.  S2BA leaves exactly the two
possibilities `w proportional to e_a` and `w proportional to e_b`, where
`a,b` are complementary to `t`.  Either endpoint turns the complete
derivative-zero face into a single-cell `3 x 2 x 2` permanent table.  The new
two-partner radical lemma excludes that table by an exhaustive split on the
source support of its zero second row.

Together with S2BA, this closes the distinguished `beta_t` coordinate-coloop
orientation.  It does not address the other eight `(1,2,2)` coloops.  Global
Krenn--Gu remains **UNRESOLVED**.

## Inherited-scope audit

### Is the ambient shore really three-dimensional?

Yes.  S2AZ--S2BA define

```text
E=image H^T,             V=H^T((ker D_B)^perp),
A=lambda^(-1)r_s,        R=rho(e_s^perp).
```

The exact dimensions are `dim E=5`, `dim V=3`, and `dim R=2`.  The classes
of `A,B` form a basis of `E/V`, so `A` is not in `V`; meanwhile `R subset V`.
Thus `S=R direct-sum span(A)` has dimension exactly three, not merely at most
three.  The two first-root rows outside `s` form a basis of `R`, while
`r_s=lambda A`.  Therefore `rho:A_1^*->S` is an isomorphism.

### Do all four endpoint face rows lie in that shore?

Yes.  Under `beta_t=0`, S2BA proves

```text
p(beta)-beta(y)A in R.
```

Under `gamma(w)=0`, it proves

```text
q(gamma)-gamma(z)A in R.
```

At `w=e_a`, the latter hyperplane is `gamma_a=0`.  Hence
`p_a,p_b,q_b,q_t` all lie in `S`.  Injectivity of `pi` and `theta`, already
proved by exact target contractions in S2BA, makes these rows nonzero and
makes `Q=span(q_b,q_t)` a two-plane.

## Single-cell table audit

### Is the table complete rather than sampled?

Yes.  The derivative transpose vanishes identically on the product face
`beta_t=gamma(w)=0`; the complete target equation holds for every first-root
covector and every point of both two-dimensional factor spaces.  At
`w=e_a`, coordinate substitution gives

```text
per(S,p_a,Q)=0,
per(S,p_b,q_t)=0,
per(r(alpha),p_b,q_b)=alpha_b T_b.
```

There is no omitted target: `{a,b}` and `{b,t}` intersect only in `b`.
Because `rho` is an isomorphism and `T_b` is nonzero, the last line is a
nonzero rank-one map on all of `S`.

### Is endpoint symmetry legitimate?

Yes.  The proof labels the chosen complementary coordinate `a` and the
remaining one `b`; no step distinguishes their names.  Repeating the same
argument after interchanging `a,b` excludes the second endpoint.  No symmetry
with a different coloop orientation is claimed.

## Radical-lemma audit

### Is the source-support split exhaustive?

Yes.  The row `p_a` is nonzero by injectivity of `pi`, so it has one, two,
or three nonzero components in `W=X direct-sum Y direct-sum Z`.  Source
permutation covers all orientations inside each support size.

### Full support

For `p=x+y+z`, the square map has the exact two-dimensional kernel

```text
span(x-y,x-z).
```

Since the two-plane `Q` lies in that kernel, equality holds.  The additional
mixed zeros at `x-y` and `x-z` force every `v in S` to have the same scalar
on its `x,y,z` components, so `S=span(p)`.  This contradicts `dim S=3`.
No generic component or basis choice is used.

### Two-source support

For `p=x+y`, square zero puts `Q` in `X direct-sum Y`.  The mixed equation is

```text
(x tensor q_Y+q_X tensor y) tensor v_Z=0.
```

If any `v_Z` is nonzero, the two-plane `Q` lies in the one-dimensional kernel
`span(x-y)`.  Otherwise the whole shore misses `Z`, and every permanent on
the shore vanishes, including the claimed surviving cell.

### Pure support

For `p=x`, substituting `v=q` gives

```text
2 x tensor q_Y tensor q_Z=0.
```

Characteristic zero is used here.  Every point of `Q` lies in one of the two
linear spaces `X direct-sum Y` and `X direct-sum Z`; a two-plane cannot be the
union of two proper subspaces, so it lies in one.  The full mixed zero then
either removes the remaining source from `S`, killing all permanents, or
forces `Q subset X`.

In the last case, for every nonzero `q in Q`,

```text
per(v,d,q)=q tensor(v_Y tensor d_Z+d_Y tensor v_Z).
```

The bracket is independent of which pure `X` partner is chosen.  Therefore
the zero `q_t` map and the purportedly nonzero `q_b` map have exactly the same
kernel behavior.  The single surviving cell is impossible.

## Evidence and independence audit

The primary SymPy replay checks all six ordered endpoint choices, the exact
full-support square and common-radical ranks, the two-source square and mixed
kernel ranks, the missing-source zero cube, and equality of the two pure-X
partner kernels.

The independent audit imports neither SymPy nor the primary verifier.  It
uses `fractions.Fraction`, its own Gaussian elimination, and a deliberately
different Z-major tensor convention.  It reconstructs the endpoint table
and all support-atlas ranks independently.

The scripts replay identities and linear-algebra dimensions.  They do not
replace the arbitrary-vector argument or silently promote a finite sample.

## Remaining obligations

This result closes

```text
N subset {beta_t=0}                                 IMPOSSIBLE.
```

The other eight coordinate-coloop orientations from S2AZ still require
their own exact normal forms.  Joint rank at most four, other physical
component types, other low-span pole strata, higher orders, and the global
conjecture remain open.  Global status stays **UNRESOLVED**.
