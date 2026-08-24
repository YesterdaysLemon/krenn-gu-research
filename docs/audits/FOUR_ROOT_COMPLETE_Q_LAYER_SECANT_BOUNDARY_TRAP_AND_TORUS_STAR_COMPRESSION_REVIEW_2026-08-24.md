# Hostile review: four-root complete Q-layer secant boundary trap

Date: 2026-08-24

## Verdict

**Accept at the declared reduction and compression scope.**  The package
constructs the complete contracted nuisance map, supplies a basis-independent
third-secant boundary criterion, classifies the fully supported rank-two
residual pair, and compresses the corresponding maximal-star family to one
fixed `44`-dimensional space.  It does not evaluate the decisive restricted
secant saturation and therefore does not exclude that family.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

The first staged snapshot was rejected pending four repairs: justify affine
dependence on the star slope, stage the frontier/README/review artifacts,
separate projective secant notation from the affine cone used in saturation,
and stop attributing normal-form exhaustiveness to representative script
checks.  All four were repaired before this acceptance.  The hostile council
found no mathematical contradiction after those repairs.

Reviewed artifacts:

- [`FOUR_ROOT_COMPLETE_Q_LAYER_SECANT_BOUNDARY_TRAP_AND_TORUS_STAR_COMPRESSION_THEOREM.md`](../../claims/arbitrary-order/FOUR_ROOT_COMPLETE_Q_LAYER_SECANT_BOUNDARY_TRAP_AND_TORUS_STAR_COMPRESSION_THEOREM.md);
- [`verify_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py`](../../claims/arbitrary-order/verify_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py);
- [`audit_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py`](../../claims/arbitrary-order/audit_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py);
- the Buczynski--Landsberg and Qi records in
  [`catalog/literature/sources.json`](../../catalog/literature/sources.json).

## 1. Exact claim under review

`GLD69` proves that the six internal port-pair labels alone have image of
dimension `21` on a maximal star and `19` on a maximal triangle, with weighted
concise GHZ outside both.  Nine labels still meet the residual pair `Q`.

The reviewed package makes one parent construction from all fifteen labels:

```text
N_full = <Q_A>
       + sum_(r in {xi,eta}) sum_u E_u^* tensor K_u^r
       + sum_(I in binom(U,2)) E_I^* tensor B_I.
```

The raw presentation has `1+24+54=79` columns.  If a complete contracted
coefficient identity exists, its weighted four-port diagonal belongs to this
space.  No quotient functional, targetwise selector, response nonvanishing,
or source promotion is silently added.

The package then proves two reductions:

1. the desired target is an epsilon-nonzero point of the complex third Segre
   secant, so trapping the nuisance/secant intersection on `epsilon=0` is a
   sufficient contradiction;
2. on the fully supported residual-coordinate maximal-star locus, every
   nonisotropic quotient slope gives one fixed `44`-dimensional nuisance
   space.

The radical-membership calculation on that fixed space remains open.

## 2. Type and complete-label audit

After the residual target slots are contracted, the label `Q` contributes the
single four-port tensor

```text
P_4(A_0-,A_1-,A_2-,A_3-).
```

Each of the eight residual--port labels leaves one arbitrary covector on its
labelled port and one three-port companion with either `xi` or `eta`, giving
`2*4*3=24` columns.  Each of six port--port labels leaves two arbitrary local
covectors and the common pullback of `J=P_4(xi,eta,-,-)` on the complementary
ports, giving `6*9=54` columns.

The primary verifier and independent audit build these columns by different
traversals and recover the same exact layer ranks.  In particular, the
projection-full triangle has

```text
rank(R_xi+R_eta+Q)=22,
rank(P_U)=19,
rank(N_full)=35,
dim(N_full/P_U)=16.
```

The `Q` direction is load-bearing.  Omitting it gives the incorrect quotient
dimension `15`; the theorem and frontier use the corrected value `16`.

## 3. Hostile check of the epsilon characterization

The degree-three contraction uses one alternating tensor in each ternary
mode.  Expanding an honest three-term decomposition leaves only the six
common colour permutations and gives

```text
epsilon(T)=6 lambda_0 lambda_1 lambda_2
           product_u det[a_(u0) a_(u1) a_(u2)].
```

Thus it is nonzero exactly on locally invertible three-term decompositions.
The primary verifier checks this formula with four independent integer basis
changes; the no-import audit evaluates the full `6^4` contraction.

The boundary direction uses Buczynski--Landsberg's complex normal forms, not
an inference from samples.  On a tangent-plus-point form, after selecting the
pure third-vector point, two tangent monomials can supply the second local
vector in at most two of four modes.  On the second-jet and two-tangent forms,
a monomial supplies the third local vector in only one mode, so three selected
monomials cannot supply it in all four.  One determinant therefore vanishes
in every boundary type.  The invariant also vanishes on `sigma_2` by closure.

This establishes, over `C`,

```text
GHZ_3 = sigma_3(Segre((P^2)^4)) intersect D_P(epsilon).
```

No characteristic-free normal-form theorem is claimed.

## 4. Hostile check of the saturation criterion

Yang Qi's Theorem 1.4 is used only set-theoretically.  For four local vector
spaces of dimension three, the pulled-back equation family retains both the
`4 x 4` generalized-flattening minors and the relevant degree-four Strassen
equations.  The package does not call the flattening minors alone a defining
ideal.

For the `79`-column map `b`, write `I_N=b^*I_sec` and
`e_N=epsilon(b(z))`.  Projectively, `D_P(epsilon)` is the nonvanishing open;
affinely, Qi's homogeneous equations cut out the cone over the third secant.
Hilbert's Nullstellensatz gives

```text
P(N_full) intersect GHZ_3 = empty
  <=> (I_N:e_N^infinity)=<1>
  <=> e_N in radical(I_N).
```

The kernel of `b` causes no projective ambiguity: `e_N` vanishes there, so it
is removed by the principal open.  Conversely, every nuisance tensor has a
preimage.  The criterion is exact for the strong orbit-intersection question.

At graph level only the empty direction is conclusive.  A nonunit saturation
would give an algebraic GHZ-orbit tensor in `N_full`, not necessarily the
particular graph target and not a graph witness.  The theorem states this
boundary explicitly.

## 5. Hostile check of the root-torus classification

When every `xi_i eta_i` is nonzero, a root-diagonal change sets `eta` to the
all-one vector without changing the projective nuisance space.  Put
`r_i=xi_i/eta_i`.  The residual form has

```text
J_ij=r_k+r_l
```

on complementary coordinates.  `GLD69` factors a rank-two zero-diagonal form
as `ell tensor m+m tensor ell` with disjoint supports.  The supports must
cover all four coordinates; otherwise a zero row forces three nonzero ratios
to be pairwise negatives, impossible in characteristic zero.

A `2+2` support partition would give ratios `(a,-a,b,-b)`, but the resulting
cross block has determinant `-4ab`, whereas the factorization makes it rank
one.  Hence the partition is `1+3`, and the three ratios in the large part
equal the negative of the singleton ratio.  This proves the unique pattern
`(1,1,1,-1)` up to scaling and permutation.

The independent `F_7` census finds exactly `24` nonzero ratio patterns with
rank two, all of this canonical type.  That census audits the formulas; the
written characteristic-zero argument is the proof.

## 6. Hostile check of the all-slope star certificate

With canonical residual vectors and radical basis, every maximal torus star
has port-image bases

```text
A_0(h)=[r_0,r_1,(1,0,0,h)],
A_i(h)=[r_0,r_1,(1,0,0,-h)],  i=1,2,3,
```

for `h!=0`.  Every occurrence of `h` lies in one root coordinate.  A nonzero
permanent monomial uses that root row at most once, so every raw-column entry
is affine in `h`.

The primary certificate obtains a `44`-column basis at `h=1`, verifies that
the constant coefficients of all `79` columns already lie in that span, and
checks the affine relation at `h=0,1,2`.  Thus `N_star(h)` is contained in the
fixed `h=1` space for every `h`.  On pinned rows and columns, the determinant
is certified as

```text
510015580149921683079168 h^33.
```

Each entry is affine, so this determinant has degree at most `44`; equality
with the displayed polynomial at `45` exact integer values proves the
polynomial identity.  It is nonzero for every `h!=0`, giving equality and
rank `44` for the entire family.  This is not interpolation from too few
samples and does not extend to `h=0`.

The no-import audit reconstructs the permanent by subset dynamic programming,
reverses the label order, and independently finds the same fixed space at six
signed nonzero slopes.  Those samples are corroboration, not the proof of all
slopes.

## 7. Sharp controls and failed strengthenings

### 7.1 Use epsilon alone

Rejected.  The single `Q` generator in the fixed star space has

```text
epsilon=-288,
balanced flattening ranks=(5,5,5).
```

It is epsilon-nonzero but visibly outside `sigma_3`.  A scalar separator that
ignores the secant equations cannot work.

### 7.2 Use balanced flattening minors as a complete secant test

Not established.  Rank at most three in every balanced flattening is
necessary for `sigma_3`, and proving that epsilon-nonzero forces one rank jump
on the fixed space would be a sufficient shortcut.  The package correctly
retains Qi's Strassen equations in the fallback criterion and leaves the
shortcut open.

### 7.3 Infer a target or graph from a nonempty orbit intersection

Rejected.  Local basis changes make empty orbit intersection a universal
certificate, but a surviving orbit point need not satisfy the graph's fixed
target coordinates, uncontracted equations, source conditions, or same-graph
integrability.

### 7.4 Include the scalar-zero star in the torus compression

Rejected by scope and exact ranks.  The scalar-zero control has

```text
rank(R_xi+R_eta+Q)=16,
rank(P_U)=rank(N_full)=21,
rank(N_full+D)=24.
```

It lies outside the nonzero-coordinate ratio argument and is not obtained by
setting `h=0` in the torus proof.

### 7.5 Promote the triangle control to a universal triangle theorem

Rejected.  The displayed projection-full centre establishes the corrected
rank `35` and quotient `16`, but general triangle centres and residual support
strata have not been classified into one fixed space.

## 8. Verification evidence

The primary verifier reports:

```text
four-root complete-Q-layer secant reduction: PASS
  epsilon target / honest / boundary: (6, 3240, (0, 0, 0, 0))
  exact layer ranks:
    scalar_zero_star: (16, 21, 21, 24, 22, 22, 22, 22)
    torus_star: (24, 21, 44, 46, 45, 45, 44, 45)
    projection_full_triangle: (22, 19, 35, 38, 36, 36, 36, 36)
  torus-star rank / determinant samples / constant:
    (44, 45, 510015580149921683079168)
  Q-only epsilon / balanced ranks: (-288, (5, 5, 5))
```

The independent audit reports:

```text
independent GLD70 complete-Q-layer audit: PASS
  layer ranks:
    scalar: (16, 21, 21, 24)
    torus: (24, 21, 44, 46)
    triangle: (22, 19, 35, 38)
  epsilon target / Q / boundary: (6, -288, (0, 0, 0))
  torus-star sampled fixed-space ranks: (44, 44, 6, 44)
  F7 rank-two / canonical ratio patterns: (24, 24)
```

The scripts replay exact identities, rank calculations, and certificate
semantics.  They do not claim that a saturation, Groebner calculation,
finite-field search, or graph enumeration has been completed.

## 9. Accepted frontier delta

The live maximal-profile parent obligation changes as follows:

- the nine `Q`-meeting labels now belong to one exact complete map rather than
  an informal synchronization target;
- the complex concise-GHZ question is one epsilon-open third-secant
  intersection with a complete set-theoretic equation route;
- every fully supported rank-two maximal star is represented by one fixed
  `44`-space, so a single radical-membership certificate would close that
  entire algebraic family;
- the exact quotient beyond the pair layer is `23` for that star and `16` for
  the projection-full triangle;
- residual-coordinate boundaries, the general triangle centre, lower port
  ranks, smaller survivor families, source supply, uncontracted integration,
  and global resolution remain open.

The next theorem should attack the fixed-space radical membership or produce
an exact countermodel to the proposed balanced-minor shortcut.  Another
targetwise sibling theorem would not address the new parent obstruction.
