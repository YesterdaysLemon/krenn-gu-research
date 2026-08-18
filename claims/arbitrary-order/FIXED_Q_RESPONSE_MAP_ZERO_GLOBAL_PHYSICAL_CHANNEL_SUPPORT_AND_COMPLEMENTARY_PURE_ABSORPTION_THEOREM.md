# Fixed-Q response-map-zero global physical-channel support and complementary pure absorption

## Status

**Exact characteristic-zero common-shore classification and conditional
full-witness reduction.**  Continue on the literal all-seven response-map-zero
stratum of `GLD19`.  The six corrected pair blocks are not six unrelated
rank-two diagonal matrices: they come from four common two-dimensional
physical shores.  This theorem classifies their simultaneous colour support
on `K_4`.

At most two corrected colours can occur.  With one corrected colour, its
nonzero-edge graph is any nonempty four-vertex graph except `P_4`.  With two
corrected colours, each colour graph is a clique on its participating
vertices.  These conditions are necessary and sufficient at the physical
response-window support level.

For a raw pair edge `e`, let

```text
F={e:supp B_e union supp K_e={0,1,2}}.                (1)
```

An edge lies in `F` exactly when some projective pair row is three-full.  By
`GLD19`, its opposite raw response is zero.  Hence `F` is an intersecting
`K_4` family: empty, one edge, two adjacent edges, a three-edge star, or a
triangle.  On a hypothetical witness, every opposite zero pair is a
`GLD15` pure-target-quotient-rank-zero target.  A maximal star or triangle
therefore forces three simultaneous complementary pure-absorption targets.

This is an exhaustive global support normal form and a reduction to a smaller
named algebraic obstruction.  It does **not** exclude that obstruction, force
any projective row to be a legal complete-nuisance operator row, construct a
selector, integrate a response window into a witness, or imply a permanent
restriction.  Exact physical star, triangle, normalized `K=0`, and dense
two-colour controls survive.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Dependencies:

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md)
- [`GLD19`](FIXED_Q_FULLY_RESPONSE_INVISIBLE_TWELVE_ROW_COMPLEMENTARY_SUPPORT_DIVISOR_THEOREM.md)

## 1. Common physical shores

Work over a characteristic-zero field `K`.  Fix one graph, residual pair
`Q`, fully supported residual contraction, ternary GHZ basis, and four-port
set

```text
U={1,2,3,4}.                                           (2)
```

Retain the arbitrary residual scalar `h in K`.  Literal response-map zero at
the six pair targets and the four-port target gives the `GLD19` conclusions

```text
B_e,K_e diagonal for all e in binom(U,2),
C(B),X(B,K) pure.                                     (3)
```

The corrected blocks have one common physical shore realization

```text
K_uv=x_u tensor y_v+y_u tensor x_v.                   (4)
```

For a port `u` and colour `c`, put

```text
v_u^c=(x_u^c,y_u^c) in K^2,
q((r,s),(r',s'))=rs'+sr'.                             (5)
```

Then

```text
K_uv(c,d)=q(v_u^c,v_v^d).                             (6)
```

The form `q` is nondegenerate.  Diagonality in (3) says

```text
q(v_u^c,v_v^d)=0       for u!=v and c!=d.             (7)
```

Call a colour **corrected-active** if `K_uv(c,c)!=0` on some edge.

### Theorem 1 (at most two corrected-active colours)

At most two colours are corrected-active.

### Proof

First take active edges `uv` of colour `c` and `rs` of a different colour
`d`, and suppose the edges are distinct.  Choose an endpoint `w` of `rs`
outside `uv`.  Equation (7) puts both `v_u^c` and `v_v^c` in the line
`(v_w^d)^perp`.  Their pairing is nonzero, so this line is nonisotropic.
Interchanging the two active edges shows that the `d`-edge lies on the
orthogonal nonisotropic line.  Thus two colours occurring on distinct edges
determine two orthogonal nonisotropic lines.

Now suppose three colours are active and choose two of them, `c,a`, with
distinct active edges.  They determine orthogonal nonisotropic lines
`L_c,L_a`.  Take any active edge of the third colour `d`.  If that edge is
distinct from the chosen `c`-edge, the preceding argument puts it on
`L_c^perp=L_a`.  If it is the same edge, the two cross-colour zero entries on
that edge again put both `d` endpoints on `L_a`.  Compare this `d`-edge with
the chosen `a`-edge.  If the edges are distinct, the argument would require
`L_a` to be orthogonal to itself; if they are the same, one off-diagonal entry
on that edge gives the same contradiction.  In either case this contradicts
that `L_a` is nonisotropic.  The only remaining possibility has all three
colours active on one edge, making the diagonal `3 x 3` block `K_e` rank
three, whereas (4) has rank at most two.  `square`

## 2. One- and two-colour support graphs

For a corrected-active colour `c`, let

```text
E_c={uv:K_uv(c,c)!=0}.                                (8)
```

### Theorem 2 (one-colour graph)

If exactly one colour is corrected-active, `E_c` can be every nonempty simple
graph on four labelled vertices except `P_4`.

### Proof of necessity

Suppose `E_c` is the path `12,23,34`.  Write `v_u=v_u^c`.  The nonedges
`13` and `14` put `v_3,v_4` on the common line `v_1^perp`.  The edge `34`
makes that line nonisotropic.  The nonedge `24` then puts `v_2` on its
orthogonal line, contradicting the edge `23`.  Relabelling excludes every
labelled `P_4`.  `square`

### Proof of sufficiency

Use the rational vectors

```text
0=(0,0),  x=(1,0),  y=(0,1),
p=(1,1),  r=(1,-1).                                  (9)
```

The following shore lists realize the nine nonempty alternatives; permuting
the four entries realizes every labelling.  Four zero shores separately
realize the zero-colour channel.

| Graph | Shore vectors |
|---|---|
| `K_2` | `0,0,x,y` |
| `P_3+K_1` | `0,y,x,x` |
| `K_(1,3)` | `y,x,x,x` |
| `K_3+K_1` | `0,x,p,p` |
| `2K_2` | `p,p,r,r` |
| paw | `x,p,p,r` |
| `C_4` | `x,x,p,r` |
| `K_4-e` | `x,x,p,p` |
| `K_4` | `x,p,p,p` |

Direct evaluation under (5) gives exactly the displayed nonzero-edge graphs.
`square`

### Theorem 3 (two-colour clique classification)

If exactly two colours `c,d` are corrected-active, each of `E_c,E_d` is a
clique on a vertex subset of size at least two.

Unless both colours occur only on the same isolated edge, there are two
orthogonal nonisotropic lines `L_c,L_d` such that every nonzero participating
`c`-vector lies on `L_c` and every nonzero participating `d`-vector lies on
`L_d`.

Conversely every ordered pair of such vertex subsets is physically realized.

### Proof

If the two colours occur on distinct active edges, the proof of Theorem 1
produces the orthogonal nonisotropic lines.  For any further `c`-edge, if it
differs from the chosen `d`-edge, (7) puts both of its endpoint vectors on
`L_d^perp=L_c`; if it equals the chosen `d`-edge, the two same-edge
off-diagonal zero coefficients put its `c`-endpoint vectors on that same
line.  The symmetric argument applies to every further `d`-edge.  Since
each line is nonisotropic, every pair of its nonzero participating vectors
has nonzero pairing.  The support graph is therefore the complete graph on
those vertices.  If both colours occur only on one common edge, both graphs
are already `K_2`.

For the converse, put `p=(1,1)` at exactly the selected vertices in colour
`c`, put `r=(1,-1)` at exactly the selected vertices in colour `d`, and put
all other shore vectors to zero.  Since

```text
q(p,p)=2,       q(r,r)=-2,       q(p,r)=0,            (10)
```

the two support graphs are precisely the requested cliques and every
off-diagonal colour coefficient vanishes.  `square`

### Corollary 3.1 (exact corrected-support ledger)

There are exactly

```text
1+3*51+3*11^2=517                                    (11)
```

labelled physical corrected-support triples `(supp K_e)_e`.

Indeed, there is one zero channel.  With one active colour, there are three
colour choices and `63-12=51` nonempty labelled graphs: all nonempty graphs
except the twelve labelled copies of `P_4`.  With two active colours, there
are three colour pairs and eleven vertex subsets of size at least two for
each clique.

This is a support classification.  It neither fixes coefficients nor counts
graph or witness fibres.

## 3. Global response-map-zero support normal form

Write

```text
S_e=supp B_e,          T_e=supp K_e.                  (12)
```

For a complementary pair `e|f`, the exact `GLD19` alternatives are:

1. if `S_e,S_f` are both nonempty, they are one common singleton `{s}` and
   `T_e,T_f subset {s}`;
2. if `S_e` is nonempty and `S_f` is empty, then `T_f=empty` when
   `|S_e|>=2`, while `T_f subset S_e` when `|S_e|=1`; the symmetric statement
   holds after exchanging `e,f`;
3. if `S_e=S_f=empty`, then `T_e,T_f` are arbitrary physical diagonal
   supports.

Theorem 1--3 plus these three independent complementary-pair alternatives
are necessary and sufficient for a labelled raw support pattern on the
physical response-map-zero window.  Sufficiency means that rational common
shores and diagonal direct blocks can be chosen so that the seven response
maps have zero mixed part.  It is not integration into the full GHZ witness
equation.

### Lemma 4 (full-capable edge criterion)

Define `F` by (1).  Then `e in F` exactly when there are projective pair
coefficients `(alpha,beta)`, not both zero, for which

```text
D_e=alpha M_e+beta Z_e
   =(alpha+h beta)B_e+beta K_e                       (13)
```

is three-full.

### Proof

Necessity is immediate.  Conversely put `a=alpha+h beta`.  The map
`(alpha,beta) -> (a,beta)` is invertible for arbitrary `h`.  If
`S_e union T_e` is all three colours, each diagonal coefficient of
`aB_e+beta K_e` is a nonzero linear form in `(a,beta)`.  Over the infinite
field `K`, choose one projective point outside their at most three zero
points.  Every diagonal coefficient is then nonzero.  `square`

The row in Lemma 4 is a response-control row.  It need not belong to the
legal complete-nuisance operator space `C_e`.

**Response-window scope note.**  `GLD19`, Theorem 2 states opposite
annihilation inside its fixed-`Q` witness corollary, but the proof of that
stronger conclusion uses only literal pair/four-port response-map zero, its
complementary support alternatives, the physical rank bound, and the common
shores.  Those hypotheses already hold on the response window considered
here.  No companion coefficient or legal-operator hypothesis enters.  The
proof is replayed below for the possibly nonlegal row supplied by Lemma 4.

### Theorem 5 (intersecting full-capable family)

For every `e in F`, its opposite edge `bar e` has

```text
B_(bar e)=K_(bar e)=0.                               (14)
```

Consequently `F` is exactly one of

```text
empty; one edge; two adjacent edges; K_(1,3); K_3.   (15)
```

### Proof

Choose the three-full row from Lemma 4 and write `f=bar e`.  First `B_f=0`.
Indeed, if `B_e` is nonzero too, the first complementary alternative confines
`B_e,K_e`, hence `D_e`, to one colour.  If `B_e=0` while `B_f` is nonzero,
the second alternative confines `K_e` to at most the singleton support of
`B_f`, or makes it zero.  Both conclusions contradict three-fullness.

If `|supp B_e|>=2`, the second complementary alternative now gives `K_f=0`.
If `B_e=0`, the physical bound `rank K_e<=2` contradicts three-fullness of
`D_e`; hence the only remaining case is

```text
supp B_e={z},             supp K_f subset {z}.       (14a)
```

The other two colours `a,b` must be active in the diagonal block `K_e`.
Therefore its `a,b` submatrix has rank two.  At either endpoint `i` of `e`,
the shore vectors `v_i^a,v_i^b` are consequently independent.  For either
endpoint `r` of `f`, diagonality on the cross edge `ir` gives

```text
q(v_i^a,v_r^z)=q(v_i^b,v_r^z)=0.                    (14b)
```

Nondegeneracy of `q` makes `v_r^z=0`.  This holds at both endpoints of `f`,
so the last possibly supported diagonal coefficient of `K_f` vanishes.
Thus (14) holds using response-window data alone.

No two edges of `F` can now be disjoint.  The list (15) is the elementary
classification of intersecting edge families in `K_4`.  `square`

### Maximal star and triangle cells

If `F` is a star, every raw block on the opposite leaf triangle is zero.  If
`F` is a triangle, every raw block on the opposite three-edge star is zero.
The corrected-channel normal forms on the three full-capable edges are:

| Active corrected colours | Star profiles | Triangle profiles |
|---:|---|---|
| zero | `(0,0,0)` | `(0,0,0)` |
| one | `(1,0,0)`, `(1,1,0)`, or `(1,1,1)` | `(1,0,0)`, `(1,1,0)`, or `(1,1,1)` |
| two | `(2,0,0)` or `(1,1,0)` | `(2,0,0)`, `(1,1,0)`, `(2,1,1)`, or `(2,2,2)` |

Here a profile is the sorted triple of support sizes `|T_e|`.  The three
one-colour profiles correspond to every nonempty star or triangle subgraph.
For two colours in a star, clique closure forces each colour to occupy only
one star edge.  For two colours in a triangle, each clique is either one edge
or the whole triangle.  On every full-capable edge, `S_e` contains every
colour missing from `T_e`; overlap is unrestricted.

### Corollary 5.1 (exact raw support ledger)

Combining all 517 physical corrected-support triples with the three exact
complementary-pair alternatives leaves `467715` labelled raw `(B,K)` support
patterns:

| Active `K` colours | `F=empty` | single | adjacent pair | star | triangle |
|---:|---:|---:|---:|---:|---:|
| 0 | 4096 | 1536 | 192 | 4 | 4 |
| 1 | 109248 | 58464 | 10512 | 312 | 312 |
| 2 | 141651 | 110736 | 27864 | 432 | 2352 |

The `F=empty` cell alone has `254995` support patterns.  In the `K=0`
subcell, each complementary matching has eighteen allowed direct-support
pairs, giving `18^3=5832` exact physical response-window patterns.  The
finite ledger is exhaustive for support masks because Theorem 1--3 prove the
physical corrected-support cover and `GLD19` proves the complementary-pair
cover.  It is not a witness enumeration.

## 4. Full-witness complementary pure absorption

Return to the complete fixed-`Q` companion equation of `GLD15`.  Let `q_f`
be the pure target quotient rank at a pair target `f`, and write its quotient
witness equation as

```text
sum_(c=0)^2 alpha_c[d_(f,c)] tensor w_(f,c)
 =bar g_M tensor M_f+bar g_Z tensor Z_f.              (16)
```

The three `w_(f,c)` are independent and the fully supported contraction has
`alpha_c!=0`.

### Theorem 6 (opposite pure-target absorption)

If `e in F` and `f=bar e`, then

```text
M_f=Z_f=0,        [d_(f,c)]=0 for c=0,1,2,
q_f=0.                                                (17)
```

Thus one full-capable edge forces one complete pair-target pure-absorption
obstruction; two adjacent edges force two; and a maximal star or triangle
forces three simultaneous pure-rank-zero targets on the complementary
triangle or star.

### Proof

Equation (14) gives `M_f=B_f=0` and `Z_f=hB_f+K_f=0`.  The right side of
(16) is zero.  Independence of the three port words and nonvanishing of the
three `alpha_c` force every pure class `[d_(f,c)]` to vanish in the complete
joint nuisance quotient.  This is (17).  `square`

The conclusion is pure-target absorption only.  It does not force the two
desired companion classes to vanish, decide the operator rank `k_f`, or
exclude the target.  In particular, `q_f=0,r_f=0,k_f=2` is allowed by
`GLD15`.

## 5. Sharp controls

All controls below are physical response windows unless explicitly called
formal.  None is a hypothetical witness or counterexample.

1. **Maximal star and triangle.**  Set `K=0`, put `B_e=I_3` on the three
   edges of a star (respectively triangle), and put every opposite raw block
   to zero.  Then `C(B)=X(B,K)=0`, all seven response maps are zero for every
   `h`, and `F` is the named maximal family.
2. **Normalized three-colour `F=empty` cell.**  Put colour `c` on the two
   edges of the `c`-th complementary matching and take `K=0`.  Then
   `C(B)=sum_c e_c^tensor4`, all three pure coefficients are nonzero, and no
   edge is full-capable.
3. **Dense corrected `F=empty` cell.**  Take
   `K_e=diag(2,-2,0)` on every edge and `B=0`.  This comes from the same two
   shore vectors at every port; it has two corrected-active `K_4` colour
   graphs and all seven response maps zero.
4. **Dense two-colour triangle profile.**  Put the same two shore vectors on
   three ports and zero shores at the fourth, so
   `K_e=diag(2,-2,0)` on the triangle and zero on its spokes.  Put
   `B_e=E_22` on the triangle.  Then `F` is the triangle and its profile is
   `(2,2,2)`.
5. **Two-colour star profile.**  Use the orthogonal lines generated by
   `(1,1)` and `(1,-1)` on two distinct centre-leaf edges.  Supply the
   missing direct colours on those edges and take a full direct block on the
   third star edge.  This realizes `(1,1,0)` with the opposite leaf triangle
   raw-zero.
6. **Common-shore sharpness.**  Formal one-colour `P_4` support and the formal
   three-colour star

   ```text
   K_12=E_00,       K_13=E_11,       K_14=E_22
   ```

   satisfy all edgewise diagonal rank and response-support equations with
   `B=0`, but Theorem 1--2 prove that neither has one common physical shore
   realization.

These controls show that support equations alone cannot exclude the maximal
cells or the large `F=empty` residue.

## 6. Exact frontier and scope ledger

```text
at most two corrected-active colours globally:             PROVED;
one-colour supports are exactly nonempty graphs but P4:     PROVED;
two-colour support graphs are exactly two cliques:          PROVED;
517 physical corrected-support triples:                    PROVED;
467715 raw response-map-zero support patterns:              PROVED;
full-capable edges form the five intersecting K4 types:     PROVED;
maximal star/triangle corrected-channel atlas:              PROVED;
opposite pair target has GLD15 pure quotient rank zero:     PROVED;
support-only exclusion of maximal star/triangle:             FALSE;
three corrected-active colours physically realizable:       FALSE;
one-colour P4 physically realizable:                         FALSE;
some nonzero legal pair operator row forced:               UNKNOWN;
triple pure-absorption obstruction excluded:               UNKNOWN;
F=empty cell excluded by full mixed witness equations:     UNKNOWN;
response-map zero forced on every hypothetical witness:    UNKNOWN;
cross-window integration and activity:                     UNKNOWN;
weighted permanent implication:                           UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

Scope:

- **field:** characteristic zero;
- **breadth:** one fixed graph, residual pair, fully supported contraction,
  GHZ basis, and one four-port `K_4` window;
- **module depth:** the complete nonempty-even fixed-`Q` deck only for
  Theorem 6;
- **response depth:** pair and four-port layers;
- **reconstructed object:** the exact common-shore corrected-support type and
  the full-capable intersecting family;
- **ambiguity:** `467715` support-mask cells, led by the `254995`-cell
  `F=empty` residue and the maximal star/triangle pure-absorption cells;
- **target implication:** one to three exact `GLD15` pure-rank-zero pair
  targets, not a mixed coefficient contradiction;
- **permanent implication:** none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_response_map_zero_global_physical_channel_support_and_pure_absorption.py
python -I claims/arbitrary-order/audit_fixed_q_response_map_zero_global_physical_channel_support_and_pure_absorption.py
```

The primary exact replay uses SymPy rational shores, complete four-port word
enumeration, the 517 corrected-support atlas, a matchingwise dynamic count of
the raw support ledger, and all positive and negative controls.  The
independent audit imports neither SymPy nor the primary.  It uses
standard-library `Fraction`, direct bilinear-form evaluation, recursive raw
support enumeration, and a separately implemented response tensor.

The programs audit the finite ledgers, response identities, rational
fixtures, and pure-absorption linear algebra.  The arbitrary-field
common-shore classification, the physical support-cover proof, the
projective avoidance argument, and the full-witness quotient implication
remain the load-bearing written proof.
