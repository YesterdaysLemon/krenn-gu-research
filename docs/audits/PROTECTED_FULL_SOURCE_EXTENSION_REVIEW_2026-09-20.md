# Independent review: protected full-source extension barriers

## Verdict and exact scope

I accept
[`PROTECTED_SCAFFOLD_FULL_SOURCE_EXTENSION_BARRIERS.md`](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_FULL_SOURCE_EXTENSION_BARRIERS.md)
as a proved package of three mechanism obstructions over `C`:

1. the uniform-leaf AB equations alone do not extend the common-star
   rank-one argument to arbitrary hollow protected-K4 fillings;
2. invertible intercomponent physical blocks forbid a target-visible
   cut-null separator; and
3. protected-edge-fixing diagonal degenerations with nonnegative supported
   crossing exponents freeze the matching terms needed on component-constant
   faces.

These statements do not prove SFULL. The two Laurent controls fail displayed
full physical equations, the rational and generic no-cut controls have
nonzero mixed coefficients, and the frozen-core theorem does not show that a
hypothetical full source has no deletable entry outside the frozen set. The
full split-leaf transfer and full-source cut-supply implications remain open.
There is no arbitrary-witness-to-scaffold reduction. The global Krenn--Gu
conjecture remains **UNRESOLVED**.

I found no mathematical blocker in the reviewed package. I did not use or
endorse any external consultation that failed to return a report.

The owner, two companions, and input fixture were inspected at these SHA-256
values over LF-normalized text bytes:

```text
owner:
627dc792380377098c3be7f90423a879f3825f2543c0fa58ce3cc2b466de4053

primary companion:
1479da66660f59dd5ba588be91ea85a9dcb1aee11fc4bb806d7b8e5ed620e1fe

independent audit:
d8e72fa81b5cd52663c3c7275b60bae434b40ef3636f81c08650040416a426c9

n=8 control fixture:
6b380343cb282d2750be95622c1683e8a4e72a043314b42283858eff346578ee
```

The pinned programs are
[`verify_protected_full_source_extension.py`](../../claims/arbitrary-order/verify_protected_full_source_extension.py)
and
[`audit_protected_full_source_extension.py`](../../claims/arbitrary-order/audit_protected_full_source_extension.py).
The fixture is
[`eight_vertex_scaffold_subsystem_controls.json`](../../tests/fixtures/eight_vertex_scaffold_subsystem_controls.json).

## Source formula and corrected provenance

An earlier scratch display in `tmp/general-probe-parent/RESULT.md` omitted the
`d_u=0` compatibility factor and assigned a grouped dot product to one fixed
internal matching. I identified that defect during continuation review. The
scratch author corrected it before integration. The durable owner now makes
the required distinction, and both physical matchers had already enforced
the endpoint colors directly. I reviewed the corrected version rather than
the defective scratch display.

For one fixed physical perfect matching, a component with no crossing
vertices uses exactly one protected matching `M_c`; its factor is

```text
delta(x_u,c) delta(y_u,c).
```

It contributes `r_u[c]s_u[c]`. The dot product appears only after grouping
the three global matchings obtained by using `M_0`, `M_1`, or `M_2` at that
component while holding all exterior choices fixed. For local crossing
degree two, the unique remaining protected edge gives `delta(y_u,c)` when
it joins two leaves and `delta(x_u,c)delta(y_u,c)` when it joins the center
and a leaf. Crossing degree four has no internal compatibility factor.
These cases exhaust every local restriction of a physical perfect matching.

After the grouped internal cancellation, the separated terms are exactly
those in which every active component has the leaf-leaf internal type and
all crossing edges are center-center or leaf-leaf. The crossed centers and
selected leaves then form two independent component matchings, so this part
factors as one outer product `A B^T`. Mixed center-leaf routing, center-leaf
internal edges, and degree-four components exhaust the remainder `E`.
Therefore the displayed identity

```text
S = A B^T + E
```

is a complete physical classification. It makes no rank claim about `E`,
and every factor comes from the same physical array.

## Exact n=8 controls

The v2 and v3 fixture families put `r_cd` and `-r_cd^(-1)` on two crossing
positions for each ordered unequal color pair and zero on every other
crossing entry. The six parameters are independent Laurent units.

Both companions reconstruct all 105 physical perfect matchings. The primary
first builds the projection over the 96 hollow crossing coordinates and
then specializes it. The independent audit instead evaluates each physical
word directly from the fixture support, without importing the primary.
For both v2 and v3, every one of the 81 uniform-leaf AB words equals its full
ternary GHZ target as an identity over the six-variable integer Laurent
ring. This is exhaustive for the declared `k=2` AB slice.

The four PSCF probes therefore give the target matrix
`[[2,1],[1,2]]`. At the unit specialization, the v2 class table in the owner
is reproduced exactly. Its separated part is `[[0,0],[-1,0]]`, while the
remainder is `[[2,1],[2,2]]`; the BB-BB class alone has determinant `-1`.
The degree-four class vanishes in this control. Thus arbitrary hollow
fillings can repair the common-star rank defect without degree-four terms.

Neither control is a full source. Direct matching enumeration gives exactly
one supported matching for each displayed zero-target word:

```text
v2  00020011  (01)(27)(36)(45)  = -r_01/r_21
v2  01000002  (07)(16)(23)(45)  =  r_02 r_10
v3  00010221  (01)(27)(34)(56)  = -r_01/r_10.
```

These Laurent monomials are nonzero at every allowed specialization. The
controls disprove the AB-only implication stated by the owner; they do not
contradict the accepted complete `k=2` exclusion or supply a full witness.

## No-cut theorem and its controls

Write the contracted target matrix as `D=R Q^T`. If a protected color-`c`
edge crosses the cut, cut-nullity kills every entry of the color-`c`
rank-one summand. Rank two therefore requires at least two protected color
matchings with no cut edge. The union of any two is a connected four-cycle
inside each K4, so every K4 lies wholly on one shore.

Rank `D=2` also forces both `R` and `Q` to have rank two. If every local probe
pair on one shore spanned at most a line, the two global product rows would
be proportional or one would vanish. Hence a local two-plane occurs on each
shore. The block joining the selected vertices is intercomponent and
invertible. It maps the right two-plane to a two-plane whose bilinear
annihilator in `C^3` is one-dimensional, so the left two-plane cannot
annihilate it. This contradiction proves the no-cut statement for every
component count for which the setup is defined; the proof itself has no
`k>=5` threshold.

The explicit rational control is valid for every `k>=2`. Giving every
intercomponent block the hollow matrix with zero diagonal and unit
off-diagonal entries yields determinant two. Global constant words retain
their unique protected matching. A nonuniform component-constant word has
its protected term one and only additional zero-or-one matching terms, so
its coefficient is a positive integer rather than zero. The array is a
nonwitness with no target-visible cut datum.

The generic corollary has `k>=5` scope only because the linked accepted
scaffold owner supplies its maximum-root-five and full-outside-span open at
that threshold. Simultaneous invertibility of the finitely many free hollow
blocks is a nonempty open, and the mixed coefficient's nonvanishing is
another nonempty open. Their intersection with the owner's open is nonempty
in its irreducible affine parameter space. I checked this interface and did
not re-audit the full upstream scaffold chain. The corollary does not assert
the full nonzero source equations on the resulting control.

## Frozen core and exact 12/12 cover

For a component-constant word `alpha`, the compatible all-protected matching
is unique. Every matching monomial for that word has diagonal exponent

```text
sum_v h_(v,alpha_v).
```

The protected matching computes the same sum as zero. Protected factors
have exponent zero and every supported crossing exponent is assumed
nonnegative, so every crossing edge used by any supported matching for
`alpha` must individually have exponent zero. Its nonzero value is unchanged
in the limit.

The union `E_fr` of these crossing entries is therefore fixed pointwise by
every admissible degeneration. The conclusion persists through a finite
sequence because each original matching and its protected comparison remain
present after every preceding step. For `k>=2`, a nonuniform
component-constant word has target zero but protected contribution one, so
at least one nonzero crossing matching is required for cancellation. Thus
`E_fr` is nonempty, and no such sequence can erase every crossing while
preserving the component-constant equations.

The alternating-cycle expansion is equivalent and exact. Relative to the
protected matching, each supported matching has a unique vertex-disjoint
union of alternating cycles. Conversely, toggling a vertex-disjoint
collection of supported cycles gives one matching. The coefficient is the
hard-core sum of their crossing products, including the empty term one.
Every such product has exponent zero, and a mixed component target requires
the nonempty products to sum to `-1`.

Both durable companions additionally verify the sharper finite statement
for v2 and v3. For each ordered unequal pair `(a,b)`, the word
`(a,a,a,a,b,b,b,b)` has exactly two supported physical matchings: the
protected term `+1` and one matching using both support entries with product
`r_ab(-r_ab^(-1))=-1`. The left endpoints form a protected color-`a` edge,
and the right endpoints form a protected color-`b` edge. The six ordered
color rows cover all 12 crossing entries in each family. Consequently every
supported crossing coordinate of either control belongs to `E_fr`; neither
control admits even one strict support deletion by this class of potential.
The split-leaf failures combine entries from different ordered-color rows.

A separate same-session scratch derivation also proved sequential
persistence, and its checker reconstructed the same two terms for every row
and confirmed the 12/12 cover. It is supplementary corroboration, not a
durable theorem dependency and not separate-human refereeing.

This frozen-core result is a limitation of homogeneity-only support descent.
It does not rule out deleting an entry outside `E_fr`, does not prove the
invariant quotient inconsistent, and does not establish SFULL. No Stiemke,
orbit-closure, or invariant-theory assertion from the scratch discussion was
promoted into the owner.

## Reproducible evidence and audit limits

The final primary and independent programs passed in separate bounded runs
with a 900-second and 8192-MiB ceiling. At the process boundary, the primary
took 0.38 seconds and the audit took 0.36 seconds. The supplementary frozen
matching replay took 0.36 seconds under the same limits. Ruff and Python
compilation passed for both durable programs.

```text
python claims/arbitrary-order/verify_protected_full_source_extension.py
python claims/arbitrary-order/audit_protected_full_source_extension.py
python -m ruff check claims/arbitrary-order/verify_protected_full_source_extension.py claims/arbitrary-order/audit_protected_full_source_extension.py
python -m py_compile claims/arbitrary-order/verify_protected_full_source_extension.py claims/arbitrary-order/audit_protected_full_source_extension.py
```

The finite programs establish the stated n=8 Laurent identities, unique
split-word detectors, matching-class table, protected-K4 cut combinatorics,
explicit block determinant, and 12/12 frozen matching cover. The
arbitrary-order no-cut and frozen-core conclusions rest on the written
proofs, not finite extrapolation. The generic corollary imports only the
scope explicitly supplied by its linked scaffold owner. No external theorem
was invoked, and no Lean formalization or kernel check is supplied.

The primary and audit use different derivations and do not import each
other. This is independent separate-agent checking within one research
session. I did not re-audit every upstream protected-scaffold result, the
global conjecture, or any proposed full-source transfer beyond the exact
claims recorded here.
