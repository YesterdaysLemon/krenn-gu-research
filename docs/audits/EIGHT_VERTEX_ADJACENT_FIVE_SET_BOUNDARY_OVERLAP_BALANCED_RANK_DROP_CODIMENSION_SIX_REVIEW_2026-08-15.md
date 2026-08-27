# Hostile review of the adjacent-overlap balanced codimension-six theorem

## Verdict and scope

**PASS, as an affine set-theoretic dimension gain rather than an S3
exclusion.**  For a fixed adjacent pair of five-sets at eight vertices, every
hypothetical ternary witness on the all-balanced rank-drop branch belongs to
a fixed closed subset of the full `252`-dimensional affine block space of
dimension at most `246`.

Equivalently, the adjacent boundary-overlap envelope gains one further
codimension after `B_all` is imposed:

```text
adjacent overlap alone:             codimension at least 5;
adjacent overlap inside B_all:      codimension at least 6.
```

The theorem neither empties the residual nor proves exact codimension,
transversality, independence across the 420 adjacent pairs, or a witness
exclusion.  The S3 branch and global Krenn--Gu conjecture remain
**OPEN/UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  EIGHT_VERTEX_ADJACENT_FIVE_SET_BOUNDARY_OVERLAP_BALANCED_RANK_DROP_CODIMENSION_SIX_THEOREM.md
  verify_eight_vertex_adjacent_five_set_boundary_overlap_balanced_rank_drop_codimension_six.py
  audit_eight_vertex_adjacent_five_set_boundary_overlap_balanced_rank_drop_codimension_six.py
```

## 1. The predecessor leaves exactly sixty equality sources

For an exact synchronization set of size `r`, the root cost is
`delta_R=2r-a_R` and the fourteen overlap blocks impose
`20-binomial(r,2)` independent evaluation equations.  After adjoining the
other fourteen free physical blocks, the full affine source dimension is

```text
246+binomial(r,2)-delta_R.
```

Every non-equality exact-sync source has dimension at most `246`.  Dimension
`247` occurs only when all four common roots synchronize and one common
nonconstant selector `f:{0,1,2}->A` serves both five-sets.

The sixty labelled selectors form two symmetry orbits:

```text
fibre type (2,1):       36;
fibre type (1,1,1):     24.
```

These are labelled source pieces.  Selector nonuniqueness prevents promotion
of the count to a statement about distinct image components.

## 2. The equality source is an irreducible vector bundle

For fixed `f`, its synchronized root base is a product of coordinate
projective spaces.  The common factors have total dimension five and the two
outer roots add four, so the base `Y_f` is projective, irreducible, and
nine-dimensional.

The six common-edge and eight outer-edge evaluations act on fourteen
different nine-dimensional affine block coordinates.  At a nonzero root
tuple each evaluation functional is nonzero and therefore surjective.  Their
joint kernel is a rank-238 vector bundle over `Y_f`.  Thus

```text
J_f is irreducible,       dim J_f=9+238=247.
```

Whole-zero blocks are already points of these affine hyperplane fibres.
They are lower-dimensional subbundles, not missing projective boundary
branches.

## 3. The balanced full-sensor chart lies on every source

Use the synchronized common four-set as the balanced root shore.  For each
common root `z_i`, its annihilator is two-dimensional; choose a basis
`a_i,b_i`.  Set the common root blocks to `b_i tensor b_j` and initially set
the cross blocks to the diagonal chart `delta_ij a_i tensor ell_j` at
contraction points with `ell_j(s_j)=1`.

All fourteen overlap evaluations vanish through their common-root factor.
The eight balanced sensor columns are the eight parity-selected binary words
in the independent pairs `(a_i,b_i)`, so the sensor has rank eight and the
graph is outside `B_all`.

Replacing the diagonal scalar matrix by

```text
C(t)=I+t(J-I)
```

preserves every evaluation.  A full-rank minor is nonzero at `t=0`, so it
remains nonzero for a nonzero `t` away from finitely many roots.  This makes
all sixteen cross blocks nonzero.  Nonzero internal blocks on the other shore
complete an all-28-block fixture.

Therefore `J_f` is not contained in the pullback of `B_all`.  Since `B_all`
is affine closed, its pullback is a proper closed subset of irreducible
`J_f`, hence has dimension at most `246`.

## 4. Proper projection closes the argument

The root base `Y_f` is projective, so projection from
`Y_f times A^252` to coefficient space is proper.  The equality-source
intersection with `B_all` therefore has a closed coefficient image of
dimension at most `246`.

The non-equality exact-sync pieces are locally closed and already have source
dimension at most `246`.  Taking closures of their projected images cannot
increase dimension.  A finite union over selector pairs and exact-sync
pieces is therefore the claimed fixed closed codimension-at-least-six
envelope.

This is a support-dimension argument.  It proves no Cartier equation,
nonzerodivisor, reduced intersection, multiplicity, regular embedding, or
transverse cut.

## 5. The affine formulation is load-bearing

`B_all` is defined by coefficients of maximal sensor minors in contraction
variables.  Sensor entries sum perfect-matching monomials that use different
sets of edge blocks.  Independent rescaling of one physical block therefore
need not multiply a sensor minor by one common weight.

The theorem correctly works in the full affine block space.  It does not
claim that `B_all` descends to the predecessor's independently projectivized
fourteen-block space.

## 6. Exact fixtures and independent evidence

The primary verifier uses SymPy to check:

- the `36+24` selector-orbit split and nine-dimensional root bases;
- the `247 -> 246` incidence arithmetic;
- all-28-blocks-nonzero full-sensor fixtures in both selector orbits, each
  with exact rank eight and an `8x8` minor `-698301`; and
- a common-quadratic equality survivor with exact sensor rank seven and
  nonzero `7x7` minor `-13436928`.

The independent audit imports neither the primary module nor SymPy.  It uses
custom exact rational rank/determinant routines, a separate selector count,
the permanent formula for the binary chart, generic root fixtures different
from the primary's coordinate fixtures, and a direct complete-deck tensor
walk.  Its two full-rank minors are `56562381` and `904998096`; it reproduces
the common-quadratic rank-seven minor `-13436928`.

The scripts are bounded audits of formulas and fixtures.  The universal
result is proved by irreducibility, the explicit full-sensor chart, proper
closed intersection, and source-dimension arguments.

## 7. The cut is nonempty

Set all 28 blocks equal to

```text
Q=[[0,0,1],[0,1,0],[1,0,0]].
```

Use synchronized common roots `(e_0,e_0,e_0,e_1)` and both outer roots
`e_0`.  All fourteen overlap evaluations vanish, and the roots support one
selector of each orbit.  The proved common-quadratic theorem places this
graph in `B_all`; direct reconstruction gives sensor rank exactly seven at
one contraction.

This model prevents the false conclusion that the balanced cut empties the
codimension-five residual.  It is not a witness: the common-quadratic orbit
is separately excluded by its two-flattening rank-six versus GHZ rank-three
mismatch.

## 8. Mistakes retained as useful boundaries

1. **Projectivize the 14 overlap blocks and intersect with `B_all`.** Not
   justified; independent block scalings need not preserve the balanced
   sensor equations.  The accepted proof is affine in all 28 blocks.
2. **Add a separate whole-zero-block branch.** Unnecessary in the direct
   affine incidence bundle.  Zero blocks already lie inside its fibres.
3. **A proper cut is automatically transverse or empty.** False.  The proof
   gives only a one-dimensional support bound, and the common-`Q` fixture
   shows the cut is nonempty.
4. **Sixty selectors mean sixty components.** False without uniqueness of
   selector support.  Only the labelled source-orbit count is used.

## 9. Accepted proof-topology update

```text
adjacent five-set overlap:                           CODIMENSION >=5;
same overlap inside B_all in full affine space:      CODIMENSION >=6;
former dimension-247 sources contained in B_all:     NO;
balanced equality residual nonempty:                 YES;
additivity across adjacent pairs:                    NOT PROVED;
eight-vertex witness exclusion:                      OPEN;
S3 all-balanced witness exclusion:                   OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

## Replay result

The two new replays, both codimension-five predecessor replays, `py_compile`,
Ruff, repository hygiene, migration-tool tests, fourteen-vertex lattice
tests, link-rewrite idempotence, and Git whitespace checks pass on the final
index-complete candidate tree.  The final reviewed theorem SHA-256 is
`741E3B6F3E9B29AB4F5CA59E33323CE48324536AA5209F48E8FAAD40E22312AF`.
