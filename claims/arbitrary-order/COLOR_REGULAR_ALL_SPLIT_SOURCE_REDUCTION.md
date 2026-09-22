# Color-regular all-split source reduction

Date: 2026-09-22

## Status and exact obligation

This note proves four all-order necessary conditions for a hypothetical full
source in the color-regular all-split family:

1. every two-color physical transition permutation is Hamiltonian;
2. the colored resource graph is one cycle; and
3. every two-lane resource edge has normalized product `-1`; and
4. a diagonal state gauge removes every remaining complex weight, giving
   protected rungs +1 and crossing-lane pairs (+1,-1).

It also gives the exact coefficient of every mixed functional-cycle word.
The remaining obstruction is purely combinatorial: every nonconstant switch
system would have to make every one of its directed cycles saturate at least
one color-transition boundary.  No proof that such saturation is impossible
is claimed here, so this does not yet exclude the all-split family or close
the degree-two parent.

All statements retain actual nonzero weights.  No generic specialization,
free cofactor, support-only cancellation, or finite-order extrapolation is
used.

This is node ASSR, a reduction for the degree-two SFULL parent. It uses
the protected K4 scaffold on k>=2 components, hollow crossings, and actual
nonzero complex weights. Protected weights may be normalized to one;
the pure coefficient in each color is one. Color regularity and the
all-split property are explicit hypotheses, not an arbitrary-source
normal form. The global Krenn--Gu conjecture remains **UNRESOLVED**.
The proof has a separate-agent audit; no Lean formalization is supplied.

## 1. Setting

Let `V` be the physical vertices.  For every color `a`, let `M_a` be the
protected perfect matching, with nonzero protected edge weights.  A colored
resource is an edge of one `M_a`, carrying its two color-`a` states.

For each ordered pair of distinct colors `(a,b)`, assume the supported
`a--b` crossings form a physical bijection

```text
tau_ab : V -> V,             tau_ba=tau_ab^(-1),
```

and that `tau_ab` maps every `M_a` resource bijectively onto an `M_b`
resource.  Equivalently,

```text
tau_ab m_a = m_b tau_ab.                              (1)
```

There is exactly one crossing from every state to each foreign color and no
other crossing support.  Thus every state has crossing degree two.

On colored resources, the three layer matchings form a two-regular graph
`F`: every resource has one neighbor of each foreign color.  Each component
of `F` is a cycle whose colors repeat `0,1,2` in one of the two orientations.
In the protected-K4 order `|V|=4k`, `F` has `6k` vertices.

For a resource edge `g={R,S}`, let its two crossing lane weights be
`gamma_g,delta_g` and its protected resource weights be `w_R,w_S`.  Define
the normalized actual signature

```text
sigma_g = gamma_g delta_g / (w_R w_S).                (2)
```

All denominators are nonzero.  With unit protected weights this is simply
the two-lane crossing product.

## 2. Every binary transition is Hamiltonian

Fix distinct colors `a,b` and define

```text
D_ab = tau_ab m_a.                                    (3)
```

This is a permutation of `V`; (1) also gives `D_ba=D_ab^(-1)`.  For every
directed cycle `C` of `D_ab`, start with the constant word `a` and change the
vertices of `C` to `b`.  If `u->v` is a cycle arc, its matching edge is the
actual crossing

```text
(m_a(u),a) -- (v,b).
```

Exactly the paired-resource block balance applies.  An `M_a` resource with
zero, one or two endpoints on `C` selects respectively its protected edge,
one displayed crossing, or the protected edge of its `M_b` target resource.
The third color is absent, so every crossing involving it is disabled.
The word has exactly one supported matching.

If `C` is proper, the word is mixed and contradicts a full source.  Since
`D_ab` is a permutation, absence of a proper cycle means it is one directed
Hamilton cycle.  Therefore

```text
D_01, D_12, D_20 (and their inverses) are Hamiltonian. (4)
```

The spanning cycle changes the whole word from pure `a` to pure `b`, so (4)
is the exact stopping point of the binary argument.

## 3. A full source forces one resource cycle

Suppose `F` has at least two components.  Fix a base color `a`, call the
other colors `b,c`, and label every component of `F` by either `b` or `c`,
using both labels.  For every `a`-resource, choose its neighbor of the label
of its `F` component.  This pairs every `a`-resource with one foreign
resource.  Define a functional digraph `D` on `V` by using the corresponding
crossing in (3), and choose any simple directed cycle `C` of `D`.

The usual cycle word again has a forced paired-block matching.  Physical
overlap between chosen foreign resources causes no conflict: the targets on
the simple directed cycle are distinct.  More importantly, no omitted scalar
edge is compatible:

* an unchosen foreign resource has a unique `a`-neighbor in `F`, namely the
  `a`-resource which chose the other color, so none of its states is selected;
* a `b--c` crossing stays inside one `F` component, whose selected foreign
  resources all have only one of the two colors.

Thus the cycle word has exactly one matching.  If `C` is proper, it contains
a foreign color while an outside vertex remains `a`.  If `C` spans `V`, all
endpoints of every `a`-resource occur, so every component label contributes
its full foreign resources; the use of both labels makes the word contain
both `b` and `c`.  The word is mixed in either case, a contradiction.

Hence a hypothetical full source in this family must have

```text
F = one colored resource cycle.                       (5)
```

## 4. Exact switched-cycle coefficient

Fix a base color `a`.  Orient the single resource cycle and write it as

```text
A_i -- B_i -- C_i -- A_(i+1),       i modulo |V|/2,   (6)
```

where the letters denote resource colors `a,b,c`.  Choose an arbitrary
label word

```text
s_i in {b,c}.
```

Pair `A_i` with `B_i` when `s_i=b`, and with `C_(i-1)` when `s_i=c`.  Define
the associated functional digraph `D_s` on physical vertices by

```text
D_s(u)=tau_ab(m_a(u))  for u in A_i and s_i=b,
D_s(u)=tau_ac(m_a(u))  for u in A_i and s_i=c.         (7)
```

Let `Gamma` be any simple directed cycle of `D_s`.  Color every vertex
outside `Gamma` by `a`; a cycle target receives the foreign color of its
incoming selected arc.  This is a physical word because cycle targets are
distinct.

Ignoring crossings between colors `b,c`, the selected resource blocks have
the unique directed-cycle matching `M_Gamma`.  Every unchosen `a--b` or
`a--c` crossing is disabled: its target colored resource is not chosen by
any other `a`-resource, since the corresponding resource layer is a
bijection.

The only remaining possible scalar edges lie at transitions

```text
s_i=b,        s_(i+1)=c,                              (8)
```

where both `B_i` and `C_i` were chosen.  Such transitions are pairwise
resource-disjoint. Simultaneously saturated transitions are also physically
disjoint in the actual word: a shared physical vertex in differently colored
full resources would require two colors at the same vertex.  The two `b--c` crossing lanes at (8) produce an
alternative matching if and only if both endpoints of `A_i` and both
endpoints of `A_(i+1)` belong to `Gamma`.  Indeed, exactly then `B_i` and
`C_i` are fully selected and `M_Gamma` uses both protected edges; replacing
them by the two crossing lanes gives the only alternating `C4`.  If either
resource is partial, a boundary crossing leaves the base-color mate of a
partial foreign state unmatched, so it cannot occur in a second perfect
matching.  Distinct transitions cannot combine into a larger alternating
cycle because they are disjoint and every partial boundary terminates at a
base-color state.

Call a transition (8) **saturated by Gamma** when these four endpoints lie
on `Gamma`, and let `partial_s(Gamma)` be the set of saturated transitions.
Factoring the nonzero weight `W_Gamma` of `M_Gamma`, the exact coefficient is

```text
T(w_Gamma)
  = W_Gamma product_(i in partial_s(Gamma)) (1+sigma_(B_i C_i)).  (9)
```

This formula includes every supported matching of the actual word.

If `s` is nonconstant, `w_Gamma` is always mixed.  A proper cycle retains
color `a` outside.  A spanning cycle contains both a resource labeled `b`
and one labeled `c`, and therefore both foreign colors.  Full-source
vanishing in (9) consequently forces:

> For every nonconstant `s` and every directed cycle `Gamma` of `D_s`, at
> least one transition saturated by `Gamma` has signature `-1`.            (10)

## 5. Every resource-edge signature is minus one

Take `s_j=c` at one index and `s_i=b` everywhere else.  Its only transition
of form (8) is `i=j-1`, namely the resource edge
`B_(j-1)--C_(j-1)`.  Equation (10) says that every directed cycle of this
one-switch functional graph contains both endpoints of `A_(j-1)` and both
endpoints of `A_j`, and

```text
sigma_(B_(j-1) C_(j-1))=-1.                          (11)
```

Since distinct directed cycles are vertex-disjoint, the switched functional
graph has exactly one directed cycle.  Varying `j` proves (11) for every
resource edge of color type `{b,c}`.  Repeating with each choice of base
color gives

```text
sigma_g=-1 for every edge g of F.                     (12)
```

Thus the weak singleton statement that at least one of two products is
minus one sharpens, under all full mixed rows, to an actual all-edge identity.
The proof also forces the stated four-endpoint saturation for every
one-resource switch.

## 6. Sharp remaining obstruction

After (12), equation (9) becomes

```text
T(w_Gamma)=0
```

whenever `Gamma` saturates even one transition.  Therefore all functional-
cycle rows used above are consistent precisely when the following purely
combinatorial condition holds:

> **Boundary-hitting obligation.** For every nonconstant binary label word
> `s` on the `a`-resources, every directed cycle of `D_s` contains both
> endpoints of `A_i` and `A_(i+1)` for at least one transition
> `s_i=b,s_(i+1)=c`.                                    (13)

A proof that some `s,Gamma` violates (13) would exclude the entire
color-regular all-split family.  Conversely, the identities already derived
cannot themselves give a weight contradiction: the local factor `1-1`
annihilates every saturated cycle word.  One must either disprove (13) using
the three Hamilton permutations and protected matching involutions, or use a
physical row which splits one lane of a saturated boundary and therefore
does not retain the full factor in (9).

In Hamilton coordinates for `P=D_ab`, a one-switch target gives a useful
equivalent form of the saturation constraint.  If `A_j={u,v}` switches to
targets `{x,y}`, the unique switched cycle can contain both `u,v` only when,
after orienting the endpoints suitably, the forward `P`-path from `x` hits
`v` before `u` and the forward path from `y` hits `u` before `v`.  Thus the
two target endpoints lie on opposite `P`-arcs cut by `u,v`.  The reverse
one-switch row gives the analogous condition with the two Hamilton orders
interchanged.  These mutual straddling conditions are necessary, but no
all-order contradiction from them is asserted here.

This is a strict sharpening of the degree-two parent: the residual is one
weighted resource ladder with all normalized edge products fixed to `-1`
and the boundary-hitting condition (13), rather than an arbitrary
color-regular support.

## 7. Global gauge convention

Write the physical vertex set as `V`, with `|V|=4k`.  A colored resource is
one protected edge, so there are `2k` resources of each color and `6k`
resources in all.  Write the single resource cycle as

```text
R_0 -- R_1 -- ... -- R_(6k-1) -- R_0.
```

Choose temporary endpoint names `0,1` on every `R_i`.  Its protected edge
has nonzero weight `w_i`.  The resource edge `R_i--R_(i+1)` is a crossing
bijection.  Let `epsilon_i` be `0` if it preserves the endpoint names and
`1` if it swaps them.  Let its lane from endpoint `0` have weight `alpha_i`
and its other lane have weight `beta_i`.  All these numbers are nonzero.

A diagonal state gauge assigns a nonzero number `h_(i,p)` to each colored
state and replaces an edge weight `W_xy` by

```text
h_x h_y W_xy.
```

For a fixed physical color word, every perfect-matching monomial is
multiplied by the same product of its selected-state gauges.  Therefore a
gauge preserves whether every word coefficient is zero or nonzero.

First normalize every protected rung independently, for example with

```text
h_(i,0)=1,       h_(i,1)=w_i^(-1).
```

Every rung then has weight one.  Since the normalized resource signature
is `-1`, the transformed crossing weights obey

```text
alpha_i beta_i = -1.                                  (G1)
```

For a full source, the product of the protected weights of each fixed color
is its pure-word coefficient and equals one.  Hence the product of this
first gauge over all states selected by any pure word is also one.  The
normalization preserves the three pure coefficients, not only their
nonvanishing.

The residual gauges preserving every rung have the form

```text
(h_(i,0),h_(i,1))=(t_i,t_i^(-1)).                    (G2)
```

## 8. The only possible circular gauge obstruction

Under (G2), the transformed `alpha_i` lane is

```text
alpha_i t_i t_(i+1)^((-1)^epsilon_i).
```

Forcing it to equal `+1` gives the recurrence

```text
t_(i+1)
  = alpha_i^(-r_i) t_i^(-r_i),
r_i=(-1)^epsilon_i.                                  (G3)
```

Thus one turn around the resource cycle sends

```text
t_0  |->  C t_0^s,
s = product_i (-r_i)
  = (-1)^(sum_i epsilon_i),                          (G4)
```

because the cycle length `6k` is even.  Here `C` is an explicit nonzero
monomial in the `alpha_i`; its value is irrelevant.  If the total endpoint
twist is odd, then `s=-1` and closure of (G3) requires only

```text
t_0^2=C,
```

which always has a nonzero solution over `C`.  With this choice every
`alpha_i` lane is `+1`.  Equation (G1), together with preservation of the
product of the two lanes by the residual gauge, then makes every `beta_i`
lane `-1`.

It remains to prove that the total endpoint twist is indeed odd; this is
where the full-source Hamilton conclusions enter.

## 9. Hamilton parity forces odd endpoint twist

For distinct colors `a,b`, the physical layer bijection is `tau_ab`, and
the protected matching involution is `m_a`.  The binary transition

```text
D_ab=tau_ab m_a
```

is a Hamilton cycle on `4k` physical vertices.  Consequently

```text
sgn(D_ab)=(-1)^(4k-1)=-1.
```

The involution `m_a` is a product of `2k` transpositions, so

```text
sgn(m_a)=(-1)^(2k)=+1,
sgn(tau_ab)=-1.                                      (G5)
```

Orient `F` in color order `a,b,c,a,...` and set

```text
T_a=tau_ca tau_bc tau_ab.
```

Each layer intertwines the corresponding protected matchings, so `T_a`
commutes with `m_a`.  Since `F` is one resource cycle, `T_a` induces one
cycle on the `2k` protected `M_a` resources.  The lift of any resource
permutation to its two endpoints has sign equal to the square of the
resource-permutation sign, hence `+1`.  The remaining sign of `T_a` is
exactly the parity of the endpoint flips accumulated while traversing the
entire resource cycle.  On the other hand, (G5) gives

```text
sgn(T_a)=sgn(tau_ca)sgn(tau_bc)sgn(tau_ab)=(-1)^3=-1.
```

Therefore the endpoint-flip parity is odd:

```text
sum_i epsilon_i = 1 mod 2.                           (G6)
```

Equations (G3)--(G6) prove the global canonical gauge.  There is no residual
winding holonomy parameter.

## 10. Exact path factorization for every physical word

A physical word selects exactly one state at each of the `4k` physical
vertices, hence it selects `4k` states among `6k` two-state resources.
At least `2k` resources are empty.  Deleting the empty resources cuts the
circular ladder into ordinary resource paths.

The global gauge already gives every such path canonical weights.  More
locally, even without (G6), any path can be gauged to rung weights `+1` and
lane weights `+1,-1`, because recurrence (G3) has no closure condition.
For a fixed selected-state set, the gauge factor is common to all its
perfect matchings.  Hence the actual coefficient has the exact form

```text
(nonzero state-gauge monomial)
  * (integer signed perfect-matching sum of the induced canonical paths).
                                                               (G7)
```

Different nonempty path components use disjoint states, so the integer in
(G7) factors over them.  In particular, for a path of `m` consecutive fully
selected resources, let `Z_m` be its canonical signed matching sum.  The
leftmost rung is either used, leaving `m-1` resources, or the two inter-rung
lanes are used, contributing their product `-1` and leaving `m-2`
resources.  Thus

```text
Z_0=Z_1=1,
Z_m=Z_(m-1)-Z_(m-2).                                 (G8)
```

The sequence is periodic with period six:

```text
1, 1, 0, -1, -1, 0, ...,
```

so

```text
Z_m=0  iff  m=2 mod 3.                               (G9)
```

For a component-constant physical word, every resource is either fully
selected or empty.  Its coefficient is therefore zero exactly when at
least one selected-resource run has length `2 mod 3`.  This is the precise
discrete form of all macro equations in the canonical all-split residue.

For a general physical word, resources may have occupancies `0,1,2`; (G7)
still removes all complex weights, but the associated signed path count is
not classified here.


## 11. Exact criterion for every selected resource path

### Straightening a path

Starting at one endpoint of the resource path, relabel the two endpoints of
each successive resource so that every crossing bijection is straight.
The path has no monodromy condition.  The diagonal path gauge from
Sections 7--10 then makes every protected rung `+1`, every upper lane
`+1`, and every lower lane `-1`.

Call an occupied resource **full** when both states are selected and a
**singleton** when only one state is selected.  Record a singleton's rail
as `0` or `1` in these straightened names.

### Forced singleton pairing

Let the singleton resources, from left to right, be

```text
S_1,S_2,...,S_r.
```

The full prefix to the left of `S_1` contains an even number of vertices.
The state at `S_1` cannot match to the left: such an edge would remove one
vertex from that prefix and leave an odd number of prefix vertices with no
other edge crossing its left boundary.  Hence the prefix must match
internally, and the singleton at `S_1` must match to the right.

After that first crossing is chosen, every intervening full resource is
forced.  Its state reached from the left is already matched; the other state
must use its right crossing.  Thus the path propagates deterministically,
switching rails once at every intervening full resource.  It can terminate
at `S_2` if and only if that singleton lies on the propagated rail.  When it
does, this entire chain has a unique matching and a nonzero weight.

The state of `S_2` is now consumed from the left, so no selected edge joins
the remaining suffix through `S_2`.  The same parity argument applies to
the full run between `S_2` and `S_3`: it must close internally, `S_3` must
exit right, and it pairs forcibly with `S_4`.  Iterating proves:

* the singleton count `r` must be even;
* the singletons pair consecutively as
  `(S_1,S_2),(S_3,S_4),...`;
* if `m_j` full resources lie strictly between
  `S_(2j-1)` and `S_(2j)`, their rails must obey

```text
rail(S_(2j)) = rail(S_(2j-1)) xor (m_j mod 2).       (P1)
```

Equation (P1) is stated after straightening.  Intrinsically, start at the
first singleton, traverse its crossing, switch to the other endpoint at
each full resource, and follow the next crossing bijection; the terminal
state must be the second singleton.

If `r` is odd, the last unpaired singleton is forced toward the right and
propagates to the path boundary, where one state remains unmatched.  The
coefficient is zero.

### Free full runs and the exact product

Remove every successfully paired forced singleton chain.  What remains is
a disjoint union of **free full runs**:

* the prefix before `S_1`;
* the runs between `S_2` and `S_3`, between `S_4` and `S_5`, and so on; and
* the suffix after `S_r`.

If there are no singletons, the whole selected path is one free full run.
For a free full run of length `m`, its signed matching sum is

```text
Z_0=Z_1=1,
Z_m=Z_(m-1)-Z_(m-2),
```

and therefore `Z_m=0` exactly when `m=2 mod 3`.

Let `U_j` be the nonzero signed weight of the `j`-th forced singleton
chain.  The exact selected-path coefficient is

```text
T_path
  = (product_j U_j) (product_free_runs Z_(length)).  (P2)
```

when the singleton count is even and every endpoint condition (P1) holds;
otherwise it is zero.  The factors are independent because a consumed
even singleton cuts every selected edge between the left and right
remainders.

Consequently:

> **Canonical path criterion.** A maximal selected resource path has
> nonzero coefficient if and only if (i) it has an even number of
> singletons, (ii) every consecutive odd/even singleton pair satisfies the
> forced rail-transport condition (P1), and (iii) every free full run has
> length different from `2 mod 3`.

Every nonzero path coefficient is `+1` or `-1` in the canonical gauge.
The coefficient of a physical word is the product of its maximal path
coefficients, multiplied by the common nonzero state-gauge monomial from
Sections 7--10.


## 12. Canonical combinatorial target

Every hypothetical full source in this all-split family is equivalent,
under a coefficient-zero-preserving gauge which also preserves the three
pure coefficients, to its canonical signed resource ladder. The physical
vertex grouping and protected K4 incidence are retained, not freely
rearranged. Thus the next all-order obligation is to find a mixed physical
word with nonzero signed path coefficient in every such residue. Concretely, the word must select one colored state per physical vertex
so that every occupied resource path has even singleton count, correct
forced pair transport, and no free full run of length 2 modulo 3. These
conditions are necessary and sufficient for that word to have nonzero
coefficient. The boundary-hitting condition in Section 6 is necessary for
a full source but not a sufficient description of all its equations.

## Evidence and parent boundary

The exact all-order argument above supplies the quantifiers. The independent
finite replay audit_all_split_switched_factorization.py exhausts 4,096
endpoint-bijection patterns in one k=2 resource topology and checks 94,208
switched-cycle words against literal physical matching enumeration, with
distinct prime signatures. It is a stress test of the coefficient identity,
not a finite cover of the all-order parent.

The separate audit_all_split_ladder_gauge.py reconstructs a literal k=2
Hamilton example, derives its odd twist and nontrivial rational gauge
closure, and checks exact coefficient covariance for all 6,561 physical
words. This corroborates the gauge argument rather than proving that the
canonical signed residue is impossible.

The independent audit_all_split_path_criterion.py checks all paths through
length eight, every endpoint twist and every nonempty occupancy pattern:
1,007,769 exact comparisons (941,104 zero and 66,665 nonzero). The written
forced-chain proof gives the arbitrary-length criterion; the replay is
corroboration, not extrapolation from those path lengths.

The all-split assumption is additional to color regularity. The
[C8 transport](DEGREE_TWO_SOURCE_TRANSPORT_AND_LOCAL_BOUNDARY.md) covers a
different source-side branch and does not prove every layer is split.
The [transition-closed consumer](RESOURCE_SIMPLE_TRANSITION_CLOSED_EXCLUSION.md)
does not apply to the repeated-color resource cycle left here.

See the [independent review](../../docs/audits/ALL_SPLIT_SOURCE_REDUCTION_REVIEW_2026-09-22.md)
and [degree-two parent brief](../../docs/strategy/degree-two-source-parent-review-2026-09-22.md).
