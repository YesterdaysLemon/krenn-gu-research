# Independent audit: color-regular all-split resource-cycle reduction

Date: 2026-09-22

Audit status: **PASS**.  The resource-cycle necessary conditions in
`claims/arbitrary-order/COLOR_REGULAR_ALL_SPLIT_SOURCE_REDUCTION.md` follow with their stated
scope.  In particular, the switched-cycle coefficient includes all actual
matching sectors even with physical overlaps, and varying the switch and
base color forces every resource-edge signature to be `-1`.

This does not prove that the remaining boundary-hitting obligation is
impossible and does not exclude the full all-split family.

## Binary and resource-component reductions

For fixed colors `a,b`, the map `D_ab=tau_ab m_a` is a permutation.  On a
directed cycle, the usual protected/crossing balance gives exactly one
matching because the third color is absent.  A proper cycle produces a
mixed word, so every `D_ab` must be Hamiltonian in a hypothetical full
source.  The inverse convention is also correct:

```text
D_ba=tau_ab^-1 m_b=m_a tau_ab^-1=D_ab^-1.
```

If the resource graph `F` has multiple components, labeling each component
uniformly by one of the two foreign colors and using both labels disables
every foreign-foreign edge.  A state of an unchosen foreign resource cannot
be selected through another same-color resource because each color's
resources partition the physical vertices.  Thus physical overlap across
different colors does not add a term.  Any functional cycle gives a unique
mixed word: a proper cycle retains base color `a`, while a spanning cycle
contains both foreign labels.  Hence `F` must be one cycle.

## Exact switched-cycle sectors

For a label word `s`, let `M_Gamma` be the directed-cycle matching.  State
layer bijectivity shows that no unchosen `a--b` or `a--c` lane can occur:
every selected foreign target has one possible `a` preimage, already
accounted for by the cycle construction.

The only additional enabled scalar edges can lie in a block `B_i--C_i`
where `s_i=b` and `s_(i+1)=c`.  Consider one of its crossing lanes.

* If either incident foreign resource is only partially selected, the
  endpoint in that resource is matched by `M_Gamma` to a base-color `a`
  state.  That `a` state has no enabled `b--c` edge.  Hence an alternating
  path using this lane terminates and cannot become a perfect-matching
  repair, even by joining lanes from another transition.
* Both lanes are enabled and usable precisely when the cycle contains both
  endpoints of `A_i` and both endpoints of `A_(i+1)`.  Then `B_i` and `C_i`
  are fully selected, `M_Gamma` uses their two protected edges, and the only
  alternative replaces those edges with the two crossing lanes.

This also handles physical overlap.  Two simultaneously saturated
transitions cannot share a physical vertex: their full resources would
require that vertex to have two different word colors.  Thus the saturated
`C4` flips are physically disjoint in the actual word and may be chosen
independently.  Unsaturated blocks cannot combine because each partial lane
has the base-color terminus just described.  Therefore the coefficient is
exactly

```text
W_Gamma * product_(saturated i) (1+sigma_(B_i C_i)).
```

There is no unlisted larger alternating-cycle sector.

The owner's phrase “pairwise resource-disjoint” is correct at the colored
resource level.  For maximum clarity in a promoted proof, it would help to
add the stronger actual-word statement above: simultaneous saturation makes
the blocks physically disjoint, while every unsaturated lane terminates at
an `a` state.  This is an explanatory improvement, not a mathematical
blocker.

## One-switch forcing and saturation

With only `s_j=c`, the selected targets are all `B_i` except `B_j`, plus
`C_(j-1)`.  A spanning functional cycle would make the selected target
multiset a bijection of all physical vertices.  Relative to the partition by
the `B_i`, that is possible only if `C_(j-1)` and `B_j` are the same physical
edge.  Distinct protected matchings in a K4 share no edge, so this equality
is impossible.  Every functional cycle is therefore proper and its word has
zero target coefficient.

There is exactly one `b->c` transition, at `i=j-1`.  The product formula
then implies that every directed cycle must saturate that transition and

```text
sigma_(B_(j-1) C_(j-1))=-1.
```

If any cycle missed one of the four source endpoints, its coefficient would
be the nonzero baseline monomial.  Since distinct functional cycles are
vertex-disjoint but every one must contain the same four endpoints, the
one-switch functional graph has exactly one directed cycle.

As `j` varies, the forced edge `B_(j-1)--C_(j-1)` runs through every
`{b,c}` edge of `F`.  Repeating the identical argument with base colors
`b` and `c` forces respectively every `{c,a}` and `{a,b}` edge.  These three
types partition the edges of the colored resource cycle, so no edge is
missed: every normalized signature is `-1`.

## Independent finite stress replay

`audit_all_split_switched_factorization.py` constructs a literal two-component
protected K4 system whose resource graph is one `C12`.  It exhausts:

* all `2^12=4096` straight/swapped endpoint bijections on the resource
  edges;
* all 14 nonconstant switch words; and
* every directed cycle of each switched functional graph.

For each resulting physical word it enumerates all 105 perfect matchings
and compares the complete weight multiset against the baseline term times
the independent factors from saturated transitions.  Distinct primes mark
the twelve resource-edge signatures, so missing or combined transition
sectors cannot hide numerically.  The replay checked 94,208 cycle words,
6,400 saturated-transition occurrences, and 105,216 unsaturated-transition
occurrences.  It passed the exact factorization in every case.

This finite replay tests conventions and overlap patterns; the arguments
above supply the all-order quantifiers.

## Accepted proof-topology delta

Inside a hypothetical full source in the color-regular all-split family:

1. all six ordered binary transitions are Hamiltonian (three up to inverse);
2. `F` is one `C_(6k)` resource cycle;
3. every resource edge has normalized product `-1`; and
4. every functional cycle for every nonconstant switch word must hit a
   saturated `b->c` boundary.

The last condition is a residual combinatorial obligation.  The local
`1-1` factors show why the switched-cycle rows already used cannot by
themselves yield a further weight contradiction.


The scratch proof was independently reviewed at SHA-256
0E4130FECF32859CB36F75078D33779F30B629840823134D14FD547072869544;
this audit was frozen at FE812E83E461BF404F1275BE237F1090AE6C59A9DF10848C1BA5E2EB6C79A014.
The promoted proof incorporates the requested physical-disjointness
clarification. This is same-session separate-agent review, not independent
human refereeing or formal kernel verification.


## Independent gauge audit: global gauge of the all-split signed ladder

Date: 2026-09-22

Audit status: **PASS**.  The gauge construction in
Sections 7--10 of the owning all-split source reduction has the correct
orientation, closes over the circular resource ladder, preserves the exact
pure coefficients, and reduces every remaining nonzero scalar weight to the
canonical `+1/-1` ladder.  The reduction is conditional on the previously
proved all-split residue and does not exclude the canonical ladder.

## Gauge covariance and protected normalization

Under a diagonal state gauge `W_xy -> h_x h_y W_xy`, every matching monomial
of a fixed physical word is multiplied by

```text
product_(selected states x) h_x.
```

This factor is common to every matching because each matching covers every
selected state once.  Hence all zero coefficients are preserved exactly.

For a protected resource `R_i` of weight `w_i`, the preliminary choice
`(h_(i,0),h_(i,1))=(1,w_i^-1)` makes its protected edge weight one.  For a
fixed color, the product of these gauge factors over the pure word is the
inverse of the product of that color's protected resource weights.  The
original pure coefficient is precisely that protected product and equals
one in a full source.  The gauge factor is therefore also one, and the pure
coefficient remains exactly one.  Residual gauges `(t_i,t_i^-1)` have unit
product on every resource and continue to preserve all three pure
coefficients.

The preliminary gauge changes the product of the two lanes on
`R_i--R_(i+1)` by `(w_i w_(i+1))^-1`.  Thus the already proved normalized
signature `-1` becomes the literal identity

```text
alpha_i beta_i=-1.
```

## Circular recurrence

If endpoint zero maps to endpoint `epsilon_i`, its residual gauge multiplier
is

```text
t_i * t_(i+1)^r_i,  r_i=(-1)^epsilon_i.
```

Setting the transformed `alpha_i` lane to one gives

```text
t_(i+1)=alpha_i^(-r_i) t_i^(-r_i).
```

After `L=6k` steps, the exponent of `t_0` is

```text
product_i(-r_i)=(-1)^L product_i r_i
               =(-1)^(sum_i epsilon_i).
```

Thus an odd total endpoint twist gives the closure map `t_0 -> C/t_0` and
the sole closure equation `t_0^2=C`.  Since `C` is nonzero and the coefficient
field is the complex numbers, a nonzero solution always exists.  The second
lane becomes `-1` because the residual gauge preserves the product of the
two lane weights for both straight and swapped endpoint maps.

## Hamilton parity and orientation

Each protected involution `m_a` is a product of `2k` transpositions on
`4k` physical vertices, so it has sign `+1`.  The Hamilton permutation
`D_ab=tau_ab m_a` is a `4k`-cycle and has sign `-1`.  Therefore every layer
permutation `tau_ab` has sign `-1`, including inverse orientations.

Orient the single resource cycle as

```text
A_i -- B_i -- C_i -- A_(i+1).
```

With ordinary right-to-left composition,

```text
T_a=tau_ca tau_bc tau_ab
```

takes an `M_a` resource once forward around the induced `2k`-cycle of
`a`-resources.  The intertwining identities
`tau_ab m_a=m_b tau_ab` show directly that `T_a` centralizes `m_a`.

The endpoint lift of a resource permutation has sign equal to the square of
the resource-permutation sign, hence `+1`.  Its remaining sign is the xor of
the endpoint flips accumulated along the three layer maps.  Over the full
`a`-resource orbit this traverses every edge of the `6k` resource cycle
exactly once.  Meanwhile

```text
sgn(T_a)=sgn(tau_ca) sgn(tau_bc) sgn(tau_ab)=-1.
```

Therefore the total resource-cycle twist is odd.  This is exactly the parity
needed by the circular recurrence; there is no unaccounted orientation
inverse or residual holonomy.

## Path coefficient rule

A word selects `4k` states among `6k` two-state resources, so at least `2k`
resources are empty.  Empty resources cut the canonical circular ladder
into path segments.  Gauge covariance makes each original coefficient a
nonzero word-gauge monomial times an integer signed matching sum on those
segments.

When a segment consists of `m` fully selected resources, its canonical sum
satisfies

```text
Z_0=Z_1=1,
Z_m=Z_(m-1)-Z_(m-2).
```

The minus sign is the product of the two inter-resource lane weights.  The
sequence `1,1,0,-1,-1,0,...` has period six, so `Z_m=0` exactly for
`m=2 mod 3`.  A component-constant word has only occupancy-zero and
occupancy-two resources, hence its coefficient vanishes exactly when one
selected-resource run has this length.  General physical words may also
contain singly occupied resources; the gauge reduction remains valid, and
the separate path audit below checks their complete classification in
Section 11 of the owner.

## Independent exact replay

`audit_all_split_ladder_gauge.py` constructs a literal two-component, single-`C12`
all-split ladder.  It searches the 4096 endpoint-bijection patterns for one
whose three binary transitions are Hamiltonian, finding bitmask `7` with odd
twist.  It assigns rational lane products `-1`, including a nontrivial first
lane weight `4`, solves the closure recurrence exactly in `Fraction`
arithmetic, and obtains the canonical `+1/-1` lanes.

It then enumerates all 105 physical perfect matchings for every one of the
`3^8=6561` physical words and verifies

```text
T_after(word) = (product selected-state gauges) T_before(word).
```

All three pure coefficients remain exactly one.  This is a convention and
implementation check; the parity and recurrence arguments above provide
the all-order result.

## Scope

The accepted implication is:

> Any hypothetical full source in the color-regular all-split residue is
> diagonally state-gauge equivalent to the same physical support with every
> protected rung `+1` and every resource edge carrying lanes `+1,-1`.

The physical grouping of states is unchanged, all zero equations and pure
targets are preserved, and no complex weight modulus remains.  Finding a
mixed word with nonzero canonical signed count is still an open combinatorial
obligation.


The gauge proof was reviewed at SHA-256
1B399D14EBB995E39A4C21EDDB6ED9523EF0CCFB9FDC32A6FC13E9A49E2E32E5;
the independent report at
1A06D25CB2E0B247ABD1706BD0A10860D1F7F0B8F7D6DC9A9816E5228223F6D8.


## Independent path audit: canonical signed resource-path criterion

Date: 2026-09-22

Audit status: **PASS**.  The necessary-and-sufficient criterion in
Section 11 of the owning all-split source reduction is complete.
It accounts for every matching of an occupancy-`0/1/2` resource path,
including arbitrary endpoint twists, and its exact product formula is
correct.

## Forced singleton chains

Empty resources cut the circular ladder, so fix one maximal nonempty path.
Let its leftmost singleton be `S_1`, preceded by `m` full resources.  The
prefix has `2m` selected states.  If `S_1` used its lane to the left, that
edge would consume one prefix state and leave `2m-1` prefix states.  The
singleton has only that one selected endpoint, so no second edge crosses
the same boundary.  The odd remainder cannot match.  Therefore the prefix
matches internally and contributes its full-run sum `Z_m`; `S_1` is forced
to the right.

Once that lane is used, each intervening full resource has one state already
consumed from the left.  Its rung is unavailable and its other state must
use the unique lane to the right.  This propagates deterministically until
the next singleton `S_2`.  A matching exists exactly when the forced lane
arrives at the selected state of `S_2`, and then the entire chain is unique.
After `S_2` is consumed, the remaining suffix has no usable edge through it,
so the same prefix argument restarts at `S_3`.

This proves without a planarity or genericity assumption that:

* the singleton count must be even;
* singleton resources pair consecutively;
* each pair has one forced chain, present exactly when its transported rail
  matches the terminal singleton; and
* an odd last singleton remains unmatched at the path boundary.

After straightening the endpoint bijections, `m` intervening full resources
switch the propagated rail `m` times, giving

```text
rail(S_2)=rail(S_1) xor (m mod 2).
```

The intrinsic transport formulation in the owner is equivalent and remains
valid for arbitrary straight/swapped endpoint maps.

## Free full runs and exact factorization

Removing the forced consecutive singleton chains leaves precisely:

* the full prefix before `S_1`;
* a full run between each consumed even singleton and the next odd
  singleton; and
* the full suffix after the last singleton.

If there are no singletons, the whole path is one such run.  These runs have
no matching edge to a forced chain, so their signed sums factor.  A full run
of length `m` satisfies

```text
Z_0=Z_1=1,
Z_m=Z_(m-1)-Z_(m-2),
```

because using the two forward lanes contributes their product `-1`.
Consequently `Z_m=0` exactly when `m=2 mod 3` and otherwise `Z_m` is `+1`
or `-1`.

The path coefficient is therefore the product of the unique forced-chain
weights and all free-run `Z_m` factors.  It is nonzero exactly when the
singleton count is even, every consecutive pair aligns, and no free run has
length `2 mod 3`.  There is no alternative nonconsecutive singleton pairing:
the leftmost-singleton parity argument forces the first pair before the
suffix is considered.

## Twists and gauge scope

On a path, endpoint names can be transported so every lane bijection is
straight.  The residual diagonal path gauge has no circular closure
condition and can make the two lanes `+1,-1`.  In the already canonical
global ladder this gauge uses only signs, so transforming back changes a
nonzero path coefficient only by `+1` or `-1`.  Thus the owner's statement
that every nonzero canonical path coefficient is a sign is correct.

For the original weighted array, the global gauge multiplies the coefficient
of a fixed physical word by one common nonzero state monomial.  Hence the
nonvanishing criterion is unchanged and maximal path factors remain
independent.

## Independent exhaustive replay

`audit_all_split_path_criterion.py` directly builds each selected signed
ladder graph and computes its perfect-matching sum by recursive exact integer
arithmetic.  Independently, it evaluates the closed criterion by propagating
rails, multiplying forced lane signs, and applying the `Z_m` recurrence.

The replay exhausts every nonempty path of length one through eight, all
`2^(m-1)` straight/swapped endpoint patterns, and all `3^m` nonempty
occupancy patterns (`singleton-0`, `singleton-1`, or full).  It checked
1,007,769 cases: 941,104 zero coefficients and 66,665 nonzero coefficients.
Every exact signed sum agreed with the criterion.

This is a finite convention check.  The parity/forcing proof above supplies
the all-order quantifier.

## Scope consequence

The all-split residual has now reduced to a concrete transversal problem:
choose one colored state at every physical vertex so that every maximal
selected resource path has even aligned singleton pairs and avoids bad free
full runs.  The criterion does not itself prove that such a mixed physical
word always exists.  It sharpens the open obligation without changing the
global `UNRESOLVED` status.


The path proof was reviewed at SHA-256
0023EF2F1303C4CB9CAAF90B7E16549DFE8167C9CF893CE996C9B5E303364AA2;
the independent report at
4FA6E7140281ED1800B4F451B9EFF7E36CF188C07D0C8B95593E7B4DAB0F4FF1.
