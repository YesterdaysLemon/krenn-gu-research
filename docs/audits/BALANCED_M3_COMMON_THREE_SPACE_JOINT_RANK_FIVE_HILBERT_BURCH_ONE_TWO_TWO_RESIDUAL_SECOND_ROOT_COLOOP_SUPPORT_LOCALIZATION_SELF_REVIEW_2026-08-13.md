# Self-review of the `(1,2,2)` residual second-root-coloop support localization

## Review verdict

The claimed localization is supported.  In either residual second-root
coloop `N subset {beta_j=0}`, `j!=t`, the complete derivative-zero face
`beta_t=gamma(w)=0` puts both first- and third-row binary planes in the exact
three-space `S=R direct-sum span(A)` and puts the complementary second row
`p_k` there.  If `w_t!=0`, the face is a binary diagonal table; only `p_j`
may escape `S`.  The new lemma exhausts the possible intersection of the
two planes already in `S`.  Its endpoint leaves are exactly 28 normalized
systems, each refuted by an exact rational Nullstellensatz identity.

This proves only `w_t=0` under either of the two hypotheses
`N subset {beta_j=0}`, `j!=t`.  It does not exclude the resulting residuals.
Five other `(1,2,2)` coordinate coloops, lower joint rank, other physical
components and pole strata, higher orders, and the global conjecture remain
open.  Global Krenn--Gu remains **UNRESOLVED**.

## Scope and row-space audit

### Is the selected coloop used with its exact S2AZ scope?

Yes.  S2AZ gives

```text
H^T(L intersect {beta_j=0})=R,       j!=t,
R=rho(e_s^perp),                     dim R=2.
```

For the third colour `k`, the root triple representing
`p_k-y_kA` has second-root coordinate `e_k^*`, hence zero `j` coordinate.
Every root triple representing `q_m-z_mA-w_mB` has second-root coordinate
proportional to `e_t^*`, again zero in coordinate `j`.  The annihilator
equations use `y_t=0` exactly.  Therefore all four corrected rows lie in
`R`, giving `p_k in S` and `q(w^perp) subset S`.  No claim is made that
`p_j` lies in `S`.

### Is `S` exactly three-dimensional?

Yes.  S2AZ gives `R subset V=H^T(L)` and `dim R=2`.  Its quotient formulas
give independent nonzero classes `[A],[B]` in `E/V`, so `A` is not in `V`
and therefore not in `R`.  Hence

```text
S=R direct-sum span(A),                 dim S=3.
```

The first-row image is exactly `S`: `rho|e_s^perp` is injective and spans
`R`, while `r_s=lambda A` supplies the third direction.  This does not
assume full injectivity of either other root-row map.

## Binary-face audit

### Is the face complete?

Yes.  Substituting `beta_t=0` and `gamma(w)=0` into all three components of
the displayed derivative transpose makes it identically zero for arbitrary
`alpha`, `beta`, and `gamma` on those linear spaces.  The full target
equation therefore applies to their whole product.  There is no selected
slice or generic-point promotion.

### Does `w_t!=0` give exactly the claimed table?

Yes.  Projection from `w^perp` to coordinates `{j,k}` has kernel zero and
equal two-dimensional source and target, hence is an isomorphism.  Its
coordinate lifts have `j,k` evaluations `delta`.  Substitution into the
complete face gives

```text
per(r_a,p_b,q'_c)=delta_(a,b,c)T_c,
a,b,c in {j,k}.
```

The two diagonal cells and crossed zeros make each ordered row pair
independent.  Thus the lemma receives genuine two-planes and fully
transverse nonzero targets.

## Plane-incidence audit

### Is the equal-plane case covered when `p_0` escapes?

Yes.  If the two planes inside `S` agree, permanent symmetry makes the
change matrix diagonal at the two diagonal target cells.  The crossed cells
then give one zero mixed map and two rank-one square maps on the two-plane
`P`, with fully transverse images.  This is exactly S2AL Lemma 2 and does
not require `P subset S`.

### Why must the intersection line be coordinate in both planes?

For

```text
ell=a_0r_0+a_1r_1=b_0q_0+b_1q_1,
```

the square map on `P` takes the two basis rows to
`a_0b_0c_0T_0` and `a_1b_1c_1T_1`.  If both are nonzero, S2AL tangent-line
separation is violated, so at least one coefficient vanishes and `ell` is
coordinate in at least one plane.  If it is coordinate in only one, write
`ell=r_a=q_0+q_1`.  Its square map and its mixed map with `r_(1-a)` are
nonzero rank-one maps with images on `T_a` and `T_(1-a)`.  S2AL mixed-factor
sharing contradicts their full transversality.  Hence the four
endpoint--endpoint cases exhaust all incidences.

## Normal-form and certificate audit

### Do the seven masks exhaust the endpoint geometry?

Yes.  When `p_0` is outside `S`, the common endpoint, the other `R` row,
the other `Q` row, and `p_0` form a basis of the four-space.  The nonzero row
`p_1 in S` has a nonempty subset of three support coordinates.  Independent
diagonal rescaling normalizes every nonzero coordinate to one, leaving
exactly `2^3-1=7` masks.  Together with four ordered endpoint pairs, this is
a proved `4*7=28` case cover, not a sampled atlas.

### Are the 64 equations sufficient?

Yes.  Choose source bases extending the factor lines of the two fully
transverse targets.  Restrict the resulting six selected coordinate forms
to the four-dimensional row space.  Every realization of the full binary
table must satisfy all eight selected source coefficients at each of its
eight row cells.  The only nonzero selected coefficients are the paired
`000` and `111` entries.  Thus a contradiction in this restricted 64-cubic
subsystem already excludes the full tensor table; coefficients involving
the third source lines need not be constrained.

### Do the stored identities prove characteristic-zero impossibility?

Yes.  For every normal form, the stored rational multipliers satisfy

```text
1=sum h_i f_i
```

coefficientwise.  This identity remains valid after scalar extension to
any characteristic-zero field, so no algebraic closure assumption is
needed.  The certificate is pinned by SHA-256
`3ea2f9470d210d85f2b45dce6fd23126888701a37634f07a32dd6750b71e96d5`.
Singular generated the sparse witnesses but is not part of either replay
path.

## Evidence and independence audit

The primary verifier reconstructs the derivative face and coloop-row
preimages, derives the binary target table, replays the incidence formulas,
rebuilds all 64 cubics in all 28 normal forms with SymPy, and verifies the
2,310-term rational identities.

The independent audit imports neither SymPy nor any repository module.  It
uses `fractions.Fraction`, reverses the 24-variable order, independently
expands each permanent through coordinate and permutation loops, rebuilds
all generators, and accumulates the certificates in its own sparse
polynomial dictionary.  Agreement therefore does not rely on a shared
generator list, monomial order, polynomial library, or repository import.

The scripts verify the exact finite algebra leaves.  They do not replace the
arbitrary-field coloop, row-space, plane-incidence, or normalization
arguments in the owning proof.

## Remaining obligations

The result is exactly

```text
N subset {beta_j=0}, j!=t, w_t!=0                 IMPOSSIBLE;
N subset {beta_j=0}, j!=t, w_t=0                  OPEN.
```

Neither residual second-root coloop is closed.  The three third-root and two
complementary first-root coloop orientations, joint rank at most four, other
physical components and low-span pole strata, higher orders, and global
resolution remain open.  Global status stays **UNRESOLVED**.
