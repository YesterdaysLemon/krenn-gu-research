# Self-review of the residual second-root-coloop coordinate-line localization

## Review verdict

The claimed localization is supported.  S2BD already forces `w_t=0` under
either residual coloop `N subset {beta_j=0}`, `j!=t`.  If both complementary
coordinates of `w` are nonzero, the complete derivative-zero face is a
same-third-row binary diagonal table.  Its first and third row planes and
the complementary middle row lie in the exact three-space
`S=R direct-sum span(A)`; only the selected middle row may escape.  The new
lemma first reduces every plane incidence to the case where the zero third
row is the intersection line, then gives a complete 21-family row-space
orbit cover.  Every family has an exact rational Nullstellensatz identity.

This proves only that `w` is proportional to one of the two coordinates
complementary to `e_t`.  Neither endpoint under either residual coloop is
excluded.  Five other `(1,2,2)` coloop orientations, lower joint rank, other
physical components and pole strata, higher orders, and the global
conjecture remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## Inherited-scope audit

### Does the proof import only results valid for a residual `beta_j` coloop?

Yes.  S2BD gives, for the third colour `k`,

```text
w_t=0,                 p_k in S,                 q(w^perp) subset S,
S=R direct-sum span(A),                           dim S=3.
```

The injectivity of `pi` and `theta` is proved in S2BC before its
`alpha_s`-specific pencil argument.  That proof uses only the S2AZ quotient
formulas, the two projection-independence hypotheses, and exact target
contraction.  It therefore applies unchanged under the residual `beta_j`
coloop.  No conclusion specific to `N subset {alpha_s=0}` is imported.

### Is the same-third-row face complete?

Yes.  When `w_t=0` and `w_jw_k!=0`, the two covectors

```text
n=w_k e_j^*-w_j e_k^*,                 e_t^*
```

form a basis of `w^perp`.  The full product face
`beta_t=gamma(w)=0` annihilates every component of the derivative transpose.
Substitution into the complete target equation gives the two diagonal cells
on the common row `q(n)`, all two crossed cells zero, and all four cells at
`q_t` zero.  This is a polynomial identity on the entire face, not a sampled
slice.

Injectivity makes `span(p_j,p_k)` and `span(q(n),q_t)` two-planes.  The two
nonzero target cells also make the first ordered pair independent.  Both
targets are nonzero and fully transverse.

## Plane-incidence audit

### Does the equal-plane argument require the escaping middle row in `S`?

No.  If the two planes already inside `S` agree, write the third-row basis
in the first-row basis by `L in GL_2`.  At the fixed row `p_0`, symmetry
applied to the coefficient matrix `E_00` kills `L_10`.  At `p_1`, symmetry
applied to `E_10` kills `L_11`.  This makes `L` singular.  Only pointwise
values at `p_0,p_1` are used; their ambient location is irrelevant.

### Why is the zero row exactly the intersection line?

For

```text
ell=a_0r_0+a_1r_1=b_0q_0+b_1q_1,
```

the square map on the middle-row plane has values

```text
a_0b_0c_0T_0,                     a_1b_0c_1T_1.
```

If all `b_0,a_0,a_1` are nonzero, S2AL tangent-line separation is violated.
If `b_0` is nonzero and one `a_i` vanishes, the intersection is a coordinate
first row; its square map has rank-one image on one target, while its mixed
map with the other first row has rank-one image on the other target.  S2AL
mixed factor sharing contradicts full transversality.  Thus `b_0=0`, so the
intersection is `span(q_1)`, the zero third row.  These alternatives exhaust
the nonzero coefficient vector in both ordered bases.

## Orbit-cover audit

### Are the 21 families exhaustive?

Yes.  Once `q_1=R intersect Q`, choose

```text
r_0=e_0, r_1=e_1, q_0=e_2, p_0=e_3,
q_1=a e_0+b e_1,
p_1=c e_0+d e_1+f e_2.
```

If `ab=0`, the intersection is one of two ordered endpoints.  Its row scalar
absorbs the corresponding basis rescaling, leaving all three diagonal basis
scales available to normalize the nonzero support of `p_1`.  The seven
nonempty masks therefore give `2*7=14` families.

If `ab!=0`, use the first two basis scales and the `q_1` row scalar to set
`q_1=e_0+e_1`.  If at most one of `c,d` is nonzero, the `p_1` row scalar and
the remaining basis scales normalize its nonzero entries, leaving masks
`1,2,4,5,6`.  If both are nonzero, one invariant ratio remains.  Normalize

```text
p_1=e_0+tau e_1                         or
p_1=e_0+tau e_1+e_2.
```

This gives five fixed and two one-parameter families.  No continuous orbit
is replaced by finitely many parameter values.

### Are the parameter certificates pointwise or generic?

They are polynomial identities.  The generator does not adjoin `tau^-1`,
saturate by `tau`, or specialize it.  For each of the two parameter systems
the stored rational multipliers satisfy `1=sum h_i f_i` in the polynomial
ring `Q[form coefficients,tau]`.  The identity therefore holds at every
`tau` over every characteristic-zero field, including the required
`tau!=0` locus.  This is stronger than a function-field or generic result.

## Certificate and independence audit

Every family uses the 64 selected source coefficients of the complete eight
row cells.  Only `(source;row)=(000;000)` and `(111;110)` are set to one;
all other selected coefficients are zero.  Any realization of the full
tensor table necessarily solves this subsystem, so a unit-ideal identity is
sufficient even though third source-coordinate lines are not constrained.

The durable artifact contains 21 rational identities and 9,256 sparse
multiplier terms.  Its SHA-256 is
`e822cb443173acbab3604d6e3e28afaf7fd99a3e306731e21c7c7bc5023ac5fc`.

The primary verifier rebuilds every row normal form and all 64 generators
with SymPy before checking the identities.  The independent audit imports no
repository module or third-party package.  It reverses the 25-variable
order, represents the parameter row by its own sparse polynomial, expands
each symmetric permanent through six direct permutations, rebuilds all
generators, and accumulates the rational identities with
`fractions.Fraction`.  The two paths share the certificate semantics and
mathematical normal forms, but not a polynomial library, monomial order,
generator list, or multiplication implementation.

Singular is used only to regenerate the multipliers.  It is not needed for
either replay and its unit-ideal report is not trusted without the replayed
coefficientwise identities.

## Remaining obligations

The result is exactly

```text
N subset {beta_j=0}, j!=t,
  w_t=0 and w_jw_k!=0:                             IMPOSSIBLE;
  w proportional to e_j or e_k:                   OPEN.
```

The four ordered coloop/endpoint cases remain.  The three third-root and two
complementary first-root coloop orientations, joint rank at most four, other
physical components and low-span pole strata, higher orders, and global
resolution also remain open.  Global status stays **UNRESOLVED**.
