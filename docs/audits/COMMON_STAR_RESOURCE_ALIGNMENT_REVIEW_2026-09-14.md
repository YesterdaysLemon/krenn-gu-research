# Independent review: common-star resource alignment

## Review conclusion

The proposed resource-completeness supply implication RCS is false.  There is
an exact common-star array over `Q(sqrt(3))` satisfying every singleton and
double-component source equation and the complete physical source subsystem
through four minorities, while each connected state-graph resource is
noncomplete tripartite.  The same array has an explicit nonzero mixed
component coefficient `2^(-360)`, so it is a countercontrol to RCS only.  It
is not a CSQ4 model, a full GHZ witness, or a Krenn--Gu counterexample.

A stronger downstream consumer survives: if the state graph for just one
binary color pair is a union of complete bipartite components, singleton and
double-component equations plus one global component target exclude the
array.  The countercontrol has this binary-biclique property for all three
pairs and is therefore a sharp control for the distinction between the false
tripartite alignment supply and the still-viable binary supply.

The global Krenn--Gu conjecture remains **UNRESOLVED**.  No Lean formalization
or external mathematical result was reviewed.

The accepted artifacts were reviewed at the following SHA-256 values over
LF-normalized text bytes:

```text
resource-alignment owner:
c8d53491b56d66c6bc70ff9402977106380b49070b311ef4bf0400dd89407016

PSCS owner with binary consumer:
32813b338296b2b922beb8be841edb1c4bc2d362423ed21cc298efb2cb673454

primary verifier:
9acd384712a028577028d8fb8a6cdea47d17981546f5038845750b88e955f675

fixture:
3d1202eb76b4e73fa7ced40941bd450832674a1217dcd72ec90b1b6857a4ad17

independent audit:
47b85f51d9698130cd67e51d0a339ee2a43e269090f9d1fb15c4ad18dd1352ff
```

The independent program is
[`audit_common_star_resource_alignment_control.py`](../../claims/arbitrary-order/audit_common_star_resource_alignment_control.py).
It imports neither the primary verifier nor project scientific code.  It
reconstructs the local matrices and cover from its own formulas rather than
reading the fixture.  The primary verifier and independent audit therefore
use distinct data and implementation routes.

## Exact local construction

Put

```text
t=(-1+sqrt(3))/2,
A=[[1,t,1],[1,1,t],[t,1,1]].
```

For ordered base color pairs define

```text
M_01=A^T,  M_12=A,  M_02=I,
M_dc=M_cd^T,
N_cd=-M_cd^(-T).
```

Clone every base index with `f in {0,1}`.  For a color `c` and another color
`d`, let `z_cd=(1,1)` when `d` is the smaller of the two alternatives to `c`,
and let `z_cd=(1,2+sqrt(3))` otherwise.  On the local states `(c,i,f)` and
`(d,j,h)`, set

```text
A'_(cd)=M_cd[i,j] z_cd[f] z_dc[h],
B'_(cd)=N_cd[i,j]/(2 z_cd[f] z_dc[h]).                 (1)
```

The reverse ordered matrices are transposes, so (1) defines actual symmetric
physical center and leaf entries.  Their Hadamard product is
`Q'_(cd)=Q_cd/2` on every clone pair, where `Q_cd=M_cd Hadamard N_cd`.

The independent exact arithmetic checks all 36 S1 rows and all 36 S1
columns.  It also checks all 180 ordered off-diagonal same-color S2 entries
and all 216 oriented distinct-color S2 entries.  Every residual is zero.
These are the actual identities

```text
(A_dc B_cd) Hadamard (B_dc A_cd) = 2 Q_dc Q_cd
```

off diagonal, and

```text
Q_de = 2 Q_dc Q_ce - (A_dc B_ce) Hadamard (B_dc A_ce).
```

The local `01` and `12` supports are complete `K_(6,6)` graphs.  The local
`02` support is three disjoint `K_(2,2)` blocks.  Their tripartite union is
connected, has 18 states and 84 edges, and is not the complete
`K_(6,6,6)`, which would have 108 edges.

Orientation is load-bearing.  The independent mutation swaps the `01` base
orientation while preserving the reverse-transpose physical convention.
S1 and the same-color identities continue to pass, but 144 of the 216
distinct-color S2 entries acquire nonzero residuals.  This prevents a
transpose convention error from passing merely because the support and port
sums are unchanged.

## Independent cover reconstruction

The resource set is `SL(2,F_5)`, of order 120.  For clone `f` and color `c`,
use the right multipliers

```text
T_0=(I, (1,1,0,1), (3,2,4,3)),
T_1=(I, (2,4,4,1), (4,2,1,2)).
```

An old component `(f,g)` places its color-`c` state in resource `g T_fc`.
Replace it with three physical components `(i,f,g)`, one for each base index
`i`.  Resource-local states `(c,i,f)` receive the factors (1).

The independent audit enumerates `SL(2,F_5)` directly and rebuilds every
membership and gadget.  It obtains:

```text
resources:                          120
physical components:               720
physical vertices:                 2880
gadgets:                            10080
nonzero crossing physical entries: 20160
ordered port degrees:              2 or 6
one label per physical pair:       yes
```

For two different old components, direct enumeration finds that 26,880 old
pairs share no resource and 1,800 share exactly one.  Copies of the same old
component share three resources, but they occupy the same state color in each
shared resource.  Since all gadgets have unequal endpoint colors, no gadget
joins such copies.  This proves the one-label simple-component condition after
cloning; it is not inferred from girth alone.

Every color state of every new physical component occurs in exactly one
resource.  Therefore each global `A_cd,B_cd,Q_cd` matrix is a disjoint union,
after separate row and column permutations, of the checked local blocks.
Pairs of copies of one old component are still distinct local same-color rows,
so they are included among the 180 off-diagonal same-color checks.  This
justifies lifting the local S1/S2 identities to all global singleton and
double-component rows.

## Exhaustive four-minority classification

This section independently checks the source classification used to pass from
the local/global matrix identities to the entire physical subsystem through
four minorities.

Fix a constant background color.  Every crossing physical edge has at least
one minority endpoint because every gadget label has unequal endpoint colors.
A word with at most four minority physical vertices can therefore use at most
four crossing edges in a supported perfect matching.

At each protected K4 component, the number of crossed physical vertices is
even: all remaining local vertices must be paired internally.  A used
component consequently has crossing degree two or four.  Degree four is
impossible within four crossing edges.  The other endpoint degrees would be
either one further degree-four component, requiring four physical edges on
one component pair when a gadget supplies only two, or two degree-two
components.  In the latter case the degree equations force two doubled
component edges, and both doubled gadgets use the first component's unique
center edge, which is impossible.

Every used component thus has crossing degree two.  Its two crossing entries
are either its center and one leaf (`AB`) or two distinct leaves (`BB`); two
center entries cannot occur.  The crossing component multigraph is a union of
cycles.  With at most four edges, the only possibilities are a two-cycle, a
triangle, a four-cycle, or two two-cycles.

- A two-cycle uses the center and leaf entries of one gadget.  Both endpoint
  components are monochromatic in that gadget's endpoint colors.  Within the
  minority budget this is exactly a singleton-component row, already checked
  by S1.  Two nontrivial two-cycles cost at least eight minorities.
- A triangle cannot contain adjacent `A` edges because a component has only
  one center.  A `BBB` triangle costs at least six minorities.  The only
  surviving form is `ABB`.  At its `BB` component, the center and the third
  leaf must retain the background color; the two crossed leaves have the
  other two colors.  Both `AB` components must retain background-colored leaf
  triples.  One or both of their centers are minorities, giving exactly the
  U3 and U4 ABB families.
- A four-cycle with no `A` edge has four `BB` components and costs at least
  eight minorities.  With one `A` edge, its two `BB` components already cost
  four and an endpoint center contributes a fifth.  With two `A` edges they
  must alternate; the two intervening leaf constraints force at least six
  minorities.  Three `A` edges are impossible because adjacent `A` edges
  would reuse a center.

This exhausts every supported physical perfect matching.  The only possible
nonzero rows through four minorities are therefore pure rows, the singleton
component rows, and the ABB U3/U4 triangle rows.  Cancellations inside U3 are
not discarded by this classification; each summand is still supported on an
actual component triangle.

The independent cover enumeration finds exactly 8,640 actual component
triangles.  Every triangle lies in one resource and is coherent: its two
incident gadget labels use the same state color at each physical component.
An ABB triangle is incoherent at its `BB` component because its two incident
leaf gadgets use two distinct state colors.  Hence every U3 and U4 ABB
monomial is absent.  Pure rows are automatic and the singleton rows are the
already checked S1 equations.  There is no omitted noncomponent U4 family.

As a negative control, the independent checker inserts one incoherent ABB
triangle into three literal protected K4 components.  A direct 12-vertex
hafnian recursion gives its U4 word source exactly `1`, against target zero.
Thus triangle coherence, rather than mere triangle locality, is essential.

## Explicit full-target failure

Color every clone-zero physical component zero and every clone-one component
two.  In each resource, the selected states are `(0,i,0)` and `(2,i,1)` for
`i=0,1,2`.  Since `M_02=I`, they form three disjoint compatible gadgets, each
with product `-1/2`.  Globally the 360 compatible component edges cover every
physical component once.

The independent audit also constructs the literal scalar graph on all 2,880
physical vertices.  It has 360 weighted four-cycles, one for each selected
gadget, and 720 isolated protected unit edges.  Each four-cycle has source
`1-1/2=1/2`, so the exact full source is

```text
2^(-360) != 0.
```

The component word contains 360 zeros and 360 twos and has target zero.  This
explicit failure is why the control refutes only the RCS resource-alignment
implication.  It does not satisfy all component targets.

## Binary-biclique consumer

Fix one color pair, say zero and one, and suppose every connected component
of its bipartite state graph `H_01` is complete bipartite.  In one such block,
the singleton row sums total `-|R_0|` and the singleton column sums total
`-|R_1|` over the same edge weights.  Hence its two part sizes agree; write
the block as `K_(m_R,m_R)`.  The no-unique-port lemma, which uses the
same-color double rows, gives `m_R>=2`.

Represent each physical component `u` as a directed edge from the block
containing `(u,0)` to the block containing `(u,1)`.  Every block has indegree
and outdegree `m_R`.  There is no loop, because completeness would otherwise
give the forbidden state edge `(u,0)(u,1)`.  A finite balanced directed graph
has a simple directed cycle.

Start with the all-zero component word and switch to one exactly the physical
components represented by the cycle edges.  At each cycle block, remove the
outgoing color-zero state `X` and add the incoming color-one state `Y`.  Its
selected compatible graph is a star, and the singleton normalization at `Y`
gives the exact factor

```text
1 + sum_(Z != X) q_ZY = -q_XY != 0.                  (2)
```

Off-cycle blocks contribute one, and different binary blocks have no
compatible edge between them.  The full source is the product of the nonzero
factors (2).  If there are `R` blocks, then `k=sum_R m_R>=2R`; the cycle
changes at least one and at most `R<k` components.  The word is mixed, so its
target is zero, a contradiction.

This proof needs completeness for only one binary pair.  The third color and
alignment among the three binary decompositions are irrelevant.  It uses the
double equations only to exclude `m_R=1`.  The independent size-one mutation
has three `K_(1,1)` blocks arranged in a directed 3-cycle with `q=-1`.  The
cycle switches all three components and produces the pure word `111` with
source and target both one.  This shows exactly why `m_R>=2` is needed for
mixedness.

The countercontrol has `H_01` and `H_12` components `K_(6,6)` and `H_02`
components `K_(2,2)`.  It is therefore excluded by the binary-biclique
consumer once full component targets are imposed, in agreement with its
explicit `2^(-360)` failure.  The strictly sharper remaining supply question
is whether the RCS antecedent forces at least one binary state graph to be a
union of bicliques.  The countercontrol does not refute that statement.

## Replay and evidence boundary

Run the independent audit from the repository root:

```text
python -X utf8 claims/arbitrary-order/audit_common_star_resource_alignment_control.py
```

It writes full JSON to standard output by default.  `--output PATH` writes an
LF-terminated receipt and emits a compact pass status.  The independent audit
reconstructs its matrices, group, memberships and gadgets without reading the
fixture.  The primary verifier separately reads the durable fixture, checks
237 local physical pure/one-change/two-change sources, checks the matrix
identities, reconstructs the cover, and replays the scalar failure.  Both
routes pass, but the finite programs corroborate rather than replace the
analytic four-minority classification and cover bridge above.

The misorientation, incoherent-triangle and size-one-cycle controls all fail
the specific mathematical step they mutate.  Ruff, Python compilation and
portable replay pass for the independent checker.  No process remains
running.
