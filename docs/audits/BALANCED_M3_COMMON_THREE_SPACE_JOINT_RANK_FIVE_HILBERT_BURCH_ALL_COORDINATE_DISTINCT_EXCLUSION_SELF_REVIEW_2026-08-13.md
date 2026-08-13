# Self-review: all-coordinate-distinct Hilbert--Burch exclusion

Date: 2026-08-13

## Verdict

**Pass for the stated characteristic-zero all-coordinate-distinct
`(1,1,1)` scope.**  The proof excludes the coordinate triangle
`x=lambda e_0`, `y=mu e_1`, `z=nu e_2`.  Together with S2AN--S2AP, it
leaves only the `(1,1,1)` charts with exactly two distinct coordinate
factors and a genuinely noncoordinate third factor.  It does not close that
residual, the other Hilbert--Burch profiles, lower joint rank, other physical
strata, higher orders, or global Krenn--Gu.  Global status remains
**UNRESOLVED**.

## Adversarial checks

### 1. Are the zero cube and three target faces genuinely untouched?

Yes.  The derivative support is exactly

```text
{(i,1,2)} union {(0,j,2)} union {(0,1,k)}.
```

None of the eight cells in
`{1,2} x {0,2} x {0,1}` belongs to that union, and no colour belongs to all
three index sets, so the entire `R x P x Q` permanent is zero.  The exterior
faces use `(0,j,k)`, `(i,1,k)`, and `(i,j,2)` with the same respective binary
index sets.  They also avoid the support.  Their only diagonal cells are
`(0,0,0)`, `(1,1,1)`, and `(2,2,2)`, giving exactly `T_0,T_1,T_2`.

### 2. Are `R`, `P`, and `Q` really two-dimensional?

Yes.  For `R`, the untouched `(1,1,1)` coefficient detects `r_1` while
`(2,1,1)` is zero, and `(2,2,2)` detects `r_2`.  Thus `r_1,r_2` are
independent.  The `(0,0,0)` and `(2,2,2)` coefficients give the analogous
separating pairs for `p_0,p_2` and `q_0,q_1` (using a crossed zero in each
case).  No row-plane equality later in the proof is inferred merely from
notation.

### 3. Does the S2R application see all nine root evaluations?

Yes.  The seven annihilator-basis coordinates are

```text
alpha_1, alpha_2, beta_0, beta_2, gamma_0, gamma_1, g,
```

where

```text
alpha_0=(nu/lambda)g,
beta_1=(nu/mu)g,
gamma_2=-g.
```

If all seven are nonzero, all nine root evaluations are nonzero.  Direct
substitution gives

```text
D_B^T(alpha tensor beta tensor gamma)
 =nu^2 gamma_2^2 (alpha,beta,gamma).
```

For a point of `K^perp`, this is exactly the fully supported product
annihilator forbidden by S2R; no coordinate evaluation is silently omitted.

### 4. Is the passage from torus avoidance to a coloop exact?

Yes.  The four-plane `K^perp` is contained in the union of the seven
coordinate hyperplanes of the seven-dimensional annihilator.  Over the
infinite characteristic-zero field, a linear space contained in a finite
union of proper linear subspaces lies in one member.  If coordinate `j`
vanishes on the four-dimensional relation kernel, the other six rows have
rank at most two.  They have rank exactly two because the omitted row plus
them spans the three-space.  Thus row `j` is a coloop.  This is a pointwise
linear-algebra conclusion, not a genericity promotion.

### 5. Are all six ordinary-row coloop cases in one symmetry orbit?

Yes.  Label an ordinary row by `(c,d)`, where `c` is the coordinate colour
of the Hilbert--Burch factor omitted by its derivative family and `d` is the
row colour.  The six rows are exactly the six ordered pairs with `c!=d`.
Simultaneous root and target-colour permutations apply the full symmetric
group to both entries, transitively.  They preserve the coordinate-triangle
normal form up to the already retained nonzero scalars and Hilbert--Burch
sign convention.  Hence it suffices to treat `q_0`; the combined row `h` is
a separate orbit and is treated separately.

### 6. Does the totally cubic-zero lemma mishandle vector-valued projections?

No.  If all three source projections of the two-plane `S` were nonzero,
choose one nonzero scalar coordinate restriction from each.  The matching
scalar coefficient of `per(S,S,S)=0` says their product is the zero binary
cubic, impossible in the polynomial domain.  Thus one entire source
projection vanishes.  If two vanished, every `per(a,S,S)` would vanish.
With exactly one missing source, its nonzero image is the fixed symmetric
bilinear `X tensor Y` image tensored by the missing-source component of
`a`.  Any two one-dimensional decomposable images therefore share the same
two nonmissing source factor lines.

### 7. Does the quadratic-annihilator fork assume nonzero restrictions?

No.  For `0!=v in S`, the directional derivative on binary cubics has
kernel exactly `span(m^3)`, where `m` annihilates `v`.  If every source
projection were active, choose one nonzero restriction from each.  Unique
factorization forces all three onto `span(m)`; repeating with any other
nonzero restriction forces all coordinate restrictions onto that line,
contrary to their spanning `S^*`.  Zero restrictions simply do not enter
this choice.  A nonzero mixed map rules out two missing sources.  With one
missing source, `per(w,S,S)=0` forces the same component of `w` to vanish,
so both mixed maps use the identical component of `a` and share that source
factor.

### 8. Are the final mixed maps derived without importing touched cells?

Yes.  When `q_0` is the coloop, `R=P=S` and `q_1,h` lie in `S`; the zero
cube gives both `per(q_0,S,S)=0` and `per(q_1,S,S)=0`.  Expanding the exact
annihilator-row relation `q_2=A+B-h`, the `A` term in the `q_0` table is the
first untouched exterior face, the `B` term vanishes on the zero `q_0` row
of the second face, and the `h` term vanishes by the quadratic-annihilator
identity.  The `q_1` table is symmetric.  The resulting maps have images
`T_0` and `T_1`, which share no source factor, contradicting the fork lemma.

### 9. Are the computational checks independent and appropriately scoped?

The primary verifier uses symbolic SymPy matrices, Kronecker products, and
scalar parameters.  The audit imports no repository or third-party module,
uses standard-library `Fraction`, its own elimination and symmetric
permanent, and a third-index-major tensor ordering.  Both replay the exact
derivative, annihilator, torus, support, face, coloop, symmetry, binary-
derivative, and fixed-factor identities.  Neither script is presented as a
replacement for the written finite-union or unique-factorization arguments.

## Scope boundary

This theorem excludes only the all-coordinate-distinct `(1,1,1)`
Hilbert--Burch chart.  Together with S2AN--S2AP it closes the charts with
three coordinate factors, but it must not be cited as a complete `(1,1,1)`,
joint-rank-five, `m=3`, or global exclusion.
