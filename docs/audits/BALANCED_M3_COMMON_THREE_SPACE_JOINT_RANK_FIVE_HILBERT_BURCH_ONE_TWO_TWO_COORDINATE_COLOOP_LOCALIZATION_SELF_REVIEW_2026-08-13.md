# Self-review of the `(1,2,2)` coordinate-coloop localization

## Review verdict

The claimed localization is supported.  Every characteristic-zero
joint-rank-five Hilbert--Burch `(1,2,2)` point can, after root symmetry and
an exact kernel-basis gauge, be written with

```text
x=lambda e_s,       c=mu e_t,       y_t=0.
```

Its four-dimensional relation kernel lies in one of nine ordinary
root-coordinate hyperplanes.  Seven orientations leave exactly the fixed
two-plane `R=rho(e_s^perp)`; the other two are the complementary first-root
coloops.

This does not exclude the profile.  All nine coloop orientations remain live
proof obligations.  The global conjecture remains **UNRESOLVED**.

## Scope audit

### Is the coordinate-chart choice exhaustive?

Yes.  S2AG proves `x` coordinate and at least one of `c,w` coordinate.
Swapping roots two and three sends

```text
span{(x,y,z),(0,c,w)}
```

to `span{(x,z,y),(0,w,c)}`.  Thus the `w`-coordinate chart is the same
argument with roots two and three exchanged.

### Is the gauge `y_t=0` legitimate?

Yes.  Replace the first kernel generator by

```text
(x,y,z)-(y_t/mu)(0,c,w).
```

Its second component loses exactly its `t` coordinate.  The kernel span is
unchanged.  The combination `y tensor w-c tensor z`, and hence every
Hilbert--Burch block, is unchanged.  Adding a multiple of `w` to `z` also
preserves independence of `z,w`.

No target-coordinate property is inferred from this non-coordinate kernel
basis change.

## Derivative audit

### Are the blocks and derivative exact?

Substitution into the S2AG Hilbert--Burch minors gives

```text
B_23=y tensor w-mu e_t tensor z,
B_13=-lambda e_s tensor w,
B_12=lambda mu e_s tensor e_t.
```

Differentiating in the three root factors gives the displayed derivative.
Both kernel generators vanish coefficientwise.  Since the two factor pairs
in `B_23` are independent, that block has matrix rank two.  The derivative
has rank seven by the S2AG Hilbert--Burch equality case; both implementations
also replay an exact rank-seven instance.

### Is the annihilator correct?

Pairing a direct-sum covector `(alpha,beta,gamma)` with the two kernel
generators gives exactly

```text
lambda alpha_s+beta(y)+gamma(z)=0,
mu beta_t+gamma(w)=0.
```

Their coefficient rows are independent because the first generator has a
nonzero first projection while the second does not.

## Recovery and torus audit

### Is the transpose recovery scalar exact?

The first transposed component has scalar

```text
beta(y)gamma(w)-mu beta_tgamma(z).
```

Using `gamma(w)=-mu beta_t` and
`beta(y)+gamma(z)=-lambda alpha_s` changes it to
`lambda mu alpha_sbeta_t`.  The second and third components give the same
scalar directly.  Hence

```text
D_B^T(product)=lambda mu alpha_sbeta_t(alpha,beta,gamma)
```

on all of `L`, with no division by `alpha_s` or `beta_t`.

### Why does S2R give nine ordinary coordinate hyperplanes?

At a fully supported point all nine evaluations are nonzero, in particular
`alpha_sbeta_t!=0`.  If that point lay in `N=K^perp`, recovery would make
the product functional annihilate `D_B(K)=U`, contrary to S2R.  Thus the
nine ordinary coordinate hyperplanes cover `N`.  Their restrictions to `L`
are proper, and the infinite-field finite-union lemma puts `N` in one fixed
hyperplane.

The conclusion is a boundary localization, not a claim that an arbitrary
coordinate coloop is itself inconsistent.

### Why does each coloop complement have row dimension two?

The selected coordinate hyperplane has dimension six inside `L` and
contains the complete four-dimensional kernel `N` of `H^T|L`.  Its image
therefore has dimension exactly two by rank--nullity.

## Seven-row and fixed-plane audit

### Do the seven displayed rows really parameterize `L`?

Yes.  The two `r_i`, two `g_j`, and three `h_k` arise by taking the free
coordinates

```text
alpha_i (i!=s), beta_j (j!=t), gamma_k
```

and solving the two annihilator equations.  The gauge `y_t=0` is
load-bearing in the formula for `g_j`.  Their seven preimages are independent
and therefore form a basis of `L`.

The quotient formulas for raw `r,p,q` follow by summing those basis rows.

### Why is `R=rho(e_s^perp)` two-dimensional?

If a nonzero `alpha in e_s^perp` had `r(alpha)=0`, it would annihilate the
first projection of all of `K=image H`.  First-factor contraction by `alpha`
would then kill `D_B(K)`: the first derivative summand is killed on `K`, and
the other two have first factor `e_s`.  The same contraction kills the
all-cross term because its row is zero.  It cannot kill the nonzero diagonal
target contraction `sum alpha_iT_i`.  This contradiction proves injectivity.

This is an exact target-consistency argument, not a numerical rank
observation.

### Which hyperplanes contain `R`?

The copy `(alpha,0,0)`, `alpha_s=0`, lies in `L`.  It is contained in
`alpha_s=0`, every `beta_j=0`, and every `gamma_k=0`.  Each corresponding
six-row image is two-dimensional and contains the already two-dimensional
`R`, so it equals `R`.  These are seven hyperplanes.

For `alpha_a=0` and `alpha_b=0`, only one of the two basis lines of `R`
survives.  Those are exactly the two residual orientations.  The count
`7+2=9` is exhaustive.

## Computational independence

The primary verifier uses SymPy and checks the gauge invariance, blocks,
rank-seven derivative, two kernel generators, symbolic recovery identity,
nine proper restrictions, exact seven-parameter basis, and hyperplane
incidence.

The independent audit imports neither SymPy nor the primary verifier.  It
uses `fractions.Fraction`, its own Kronecker construction, and a separate
Gaussian eliminator.  It independently rebuilds the gauge, derivative,
recovery samples, nine coordinate restrictions, and seven parameter columns.

Neither script proves the target-consistency injectivity argument or the
finite-union lemma by computation; those are the written proof.

## Remaining obligations

The seven equal-`R` orientations and two complementary first-root coloops are
still open.  The next useful step is to contract the complete target equation
on `beta_t=0`, `gamma(w)=0`, producing a binary exterior face whose row
geometry can be tested against those nine coloop normal forms.

The `(1,2,2)` profile is therefore localized but not excluded.  Lower joint
ranks, other physical component types, higher orders, and global resolution
also remain open.  Global Krenn--Gu status is **UNRESOLVED**.
