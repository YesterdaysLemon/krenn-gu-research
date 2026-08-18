# Fixed-Q response-map-zero dead-colour h-gate and dense companion absorption

## Status

**Exact characteristic-zero subcell exclusion and companion normal form.**
Continue on the literal all-seven response-map-zero locus of `GLD19` and the
global common-shore atlas of `GLD20`.  Suppose exactly two corrected colours
are active and at least one of their support graphs is `K_4`.  The third
colour is dead at every contracted physical shore.  The `K_4` hypothesis
then forces every direct block to use only that globally complete colour.

This is an exhaustive `F=empty` subcell containing exactly `63` corrected
support types and `1347` compatible labelled raw support patterns.  On the
complete fixed-`Q` witness equation, the all-dead-colour four-port word has
only the residual-pair deck label `Q`.  Hence every hypothetical witness in
the subcell satisfies

```text
h!=0,
G_U(-_R;a^4)=(alpha_a/h)e_a^(tensor R).               (1)
```

Thus the entire `h=0` portion of those `1347` support patterns is excluded.
For `h!=0`, (1) is an exact nonzero pure root-to-four-port companion-slice
obstruction: eighty root coefficients vanish and one is prescribed nonzero.
Hamming-one coefficients solve the two one-`Q` companions at every port of
the second clique.

In the dense `K_4/K_4` cell, all direct blocks vanish.  Twenty-four mixed
`2+1+1` port words, grouped into twelve two-orientation packages, force twelve
simultaneous desired companion columns into explicit nine-column nuisance
images.  A nonzero augmented minor is a predetermined bounded mixed detector.

The theorem does **not** exclude the `h!=0` residue, force an augmented minor
to be nonzero, manufacture a legal `GLD15` operator row, or integrate a
formal companion array into the same graph.  Indeed `G_U=J_Q/h` and all other
abstract companion coefficients zero solve the complete fixed-`Q` linear
equation whenever `h!=0`; principal-permanent root-companion integrability is
load-bearing.  No witness or counterexample is constructed.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md)
- [`GLD19`](FIXED_Q_FULLY_RESPONSE_INVISIBLE_TWELVE_ROW_COMPLEMENTARY_SUPPORT_DIVISOR_THEOREM.md)
- [`GLD20`](FIXED_Q_RESPONSE_MAP_ZERO_GLOBAL_PHYSICAL_CHANNEL_SUPPORT_AND_COMPLEMENTARY_PURE_ABSORPTION_THEOREM.md)

## 1. Fixed-contraction physical shores

Work over a characteristic-zero field `K`.  Fix one graph, residual pair

```text
Q={q_0,q_1},
```

fully supported residual contraction `z_Q`, ternary GHZ basis, and four-port
set `U`.  Retain the arbitrary contracted residual scalar

```text
h=H_Q(z_Q).                                            (2)
```

For each port `u` and colour `s`, put

```text
x_u^s=H_(q_0,u)(z_(q_0),e_s),
y_u^s=H_(q_1,u)(z_(q_1),e_s),
v_u^s=(x_u^s,y_u^s),                                  (3)
q((r,t),(r',t'))=rt'+tr'.
```

These are shores at the one fixed contraction, not uncontracted `Q--U` edge
tensors.  The corrected pair block is

```text
K_uv(s,t)=q(v_u^s,v_v^t).                             (4)
```

Literal response-map zero makes every `B_e,K_e` diagonal and the four-port
layers pure.  Let `E_s` be the edge-support graph of `K_e(s,s)`.

### Lemma 1 (the missing corrected colour has zero shores)

Suppose exactly two colours `c,d` are corrected-active and let `a` be the
third colour.  Then

```text
v_u^a=0                 for every u in U.             (5)
```

### Proof

In the ordinary two-colour case, `GLD20` gives two orthogonal nonisotropic
lines `L_c,L_d`, and each active support is a clique on at least two
vertices.  For a fixed `u`, choose a `c`-participant and a `d`-participant
different from `u`.  Cross-colour diagonality puts `v_u^a` in both
`L_c^perp=L_d` and `L_d^perp=L_c`, so it is zero.

In the exceptional case where both colours occur only on one common edge,
the two active vectors at either endpoint are independent because the
corresponding diagonal `2 x 2` block has rank two.  Cross-colour diagonality
against that endpoint kills `v_u^a` at every other port, and the opposite
endpoint kills it on the common edge.  This proves (5).  `square`

The lemma is broader than the subcell below.  The `K_4` hypothesis is needed
to eliminate the missing colour from every direct block.

## 2. The one-complete-clique subcell

Assume from now on

```text
E_c=K_4,             E_d=K_(A_d),
2<=|A_d|<=4.                                           (6)
```

When both graphs are `K_4`, either active colour may be called `c`.

### Theorem 2 (direct support localization)

Every direct block is empty or supported only in the complete colour:

```text
supp B_e subset {c}                 for every e.      (7)
```

Consequently the subcell is contained in `F=empty`, and colour `a` is dead
in the full same-graph sense relevant to the fixed contraction:

```text
B_e(a,a)=K_e(a,a)=0,
x_u^a=y_u^a=0.                                         (8)
```

If `u notin A_d`, then also `v_u^d=0`.

### Proof

Fix `e` and let `f` be its opposite edge.  Since `E_c=K_4`, the corrected
support `T_f` contains `c`.  If `B_e` is nonzero and `B_f` is zero, the
second `GLD19` alternative either makes `K_f=0` or confines it to the
singleton support of `B_e`; hence that singleton must be `{c}`.  If both
direct blocks are nonzero, the first alternative confines both and both
corrected blocks to one common singleton, again necessarily `{c}`.  This
proves (7).  Equations (5) and (7) give (8), and no raw `B/K` support union
contains all three colours.

For `u notin A_d`, cross-colour diagonality against a complete-colour vector
puts `v_u^d` on `L_d`.  Its zero same-colour pairing with a `d`-participant
puts it on `L_d^perp`.  Nonisotropy gives `v_u^d=0`.  `square`

### Corollary 2.1 (exact support ledger)

The subcell has exactly `63` labelled corrected-support types and `1347`
compatible labelled raw `(B,K)` support patterns:

| Secondary support | Corrected types | Raw patterns per type | Raw patterns |
|---|---:|---:|---:|
| `K_2` | 36 | 32 | 1152 |
| `K_3` | 24 | 8 | 192 |
| `K_4` | 3 | 1 | 3 |

### Proof

There are three unordered active-colour pairs.  With exactly one complete
colour, choose which colour is complete and choose one of six two-vertex or
four three-vertex secondary sets.  This gives `3*2*6=36` and `3*2*4=24`
types.  Both colours complete gives three more.

On a complementary matching, the secondary clique occupies zero, one, or
two of its edges.  The `GLD19` alternatives and (7) then permit respectively
four, two, or one direct-support pairs.  A `K_2` meets one matching once and
the other two zero times, giving `2*4^2=32`.  A `K_3` meets every matching
once, giving `2^3=8`.  Two complete cliques permit only the zero direct
array.  Therefore

```text
36*32+24*8+3=1347.                                    (9)
```

This is an exhaustive support-mask bridge.  It is not a graph-fibre or
witness count.  `square`

## 3. The all-dead-colour coefficient

Retain the complete fixed-`Q` companion equation of `GLD15`:

```text
Gamma_Q(H)=J_Q.                                       (10)
```

Its domain has the `31` labelled nonempty even deck summands
`I subset Q union U`.  The coefficient of `H_I` is `G_((Q union U)-I)`.
For a companion tensor with `U` slots, write `G_D(-_R;omega)` for evaluation
of those slots at the port word `omega`, leaving the four root slots open.
The fixed contraction gives

```text
J_Q=sum_(s=0)^2 alpha_s e_s^(tensor R) tensor e_s^(tensor U),
alpha_s!=0.                                           (11)
```

### Lemma 3 (dead-colour deck ledger)

On the port word `a^4`, every deck coordinate in (10) vanishes except

```text
H_Q=h.                                                 (12)
```

### Proof

The six possible label types besides `Q` are checked directly.  A port-pair
label uses `B_e(a,a)=0`; a `Q`-plus-pair label uses
`Z_e(a,a)=hB_e(a,a)+K_e(a,a)=0`; and a one-`Q` pair uses a vanished shore
from (8).  Every matching in a one-`Q` triple uses either such a shore or one
missing-colour direct edge.  The four-port label is a matching product of
missing-colour direct edges.  Every matching in the full `Q union U` label
uses either two vanished `Q--U` shores or the `Q` edge and a vanished
four-port direct matching.  The empty label is not in the complete
surplus-two domain.  Only (12) remains.  `square`

### Theorem 4 (residual-scalar exclusion and pure companion slice)

Every hypothetical witness in the `1347`-pattern subcell satisfies (1).
In particular, its `h=0` part is empty.

### Proof

Evaluate (10) on `a^4` and use Lemma 3.  Equation (11) gives the root-tensor
identity

```text
h G_U(-_R;a^4)=alpha_a e_a^(tensor R).                (13)
```

The right side is nonzero because the residual contraction is fully
supported.  Hence `h!=0`, and division gives (1).  The root tensor space has
dimension `3^4=81`, so the other eighty root coefficients vanish and the
all-`a` coefficient equals `alpha_a/h`.  `square`

This is a full coefficient of the complete same-graph equation, not a
formal response control and not a consequence of one selected pure operator
line.

### Theorem 5 (Hamming-one companion equations)

For every port `t` and active colour `l in {c,d}`, the mixed port word with
colour `l` at `t` and `a` elsewhere gives

```text
h G_U(-;a^(U-t) l_t)
 +x_t^l G_({q_1} union (U-t))(-;a^(U-t))
 +y_t^l G_({q_0} union (U-t))(-;a^(U-t))=0.           (14)
```

For `t in A_d`, the shore matrix

```text
V_t=[[x_t^c,y_t^c],[x_t^d,y_t^d]]                    (15)
```

is invertible, and the two equations solve

```text
[G_({q_1} union (U-t)); G_({q_0} union (U-t))]
 =-h V_t^(-1)
   [G_U(-;a^(U-t)c_t); G_U(-;a^(U-t)d_t)].            (16)
```

For `t notin A_d`, equation (14) with `l=d` reduces to

```text
G_U(-;a^(U-t)d_t)=0.                                  (17)
```

### Proof

On a Hamming-one word, the same label check as Lemma 3 leaves only `I=Q`
and the two one-`Q` pair labels `{q_0,t}`, `{q_1,t}`.  The target coefficient
is zero because the port word is mixed, giving (14).  At a secondary-clique
port the two nonzero shore vectors lie on the distinct lines `L_c,L_d`, so
(15) is invertible and gives (16).  Outside that clique `v_t^d=0`; combine
(14) with `h!=0` to obtain (17).  `square`

## 4. Dense two-colour companion absorption

Assume now

```text
E_c=E_d=K_4.                                          (18)
```

### Lemma 6 (dense direct vanishing)

Every direct block vanishes:

```text
B_e=0                 for all six e.                  (19)
```

### Proof

The corrected support on the edge opposite any `e` is `{c,d}`.  If `B_e`
were nonzero, the relevant `GLD19` alternative would make that opposite
corrected block zero or confine it to one singleton, a contradiction.
`square`

Fix `e={u,v}`, write its complement as `{w,x}`, choose a repeated active
colour `s`, let `r` be the other active colour, and retain `a` as the missing
colour.  Use the two oriented port words

```text
omega^+=(s,s,r,a),        omega^-=(s,s,a,r),          (20)
```

where the first two positions are `u,v` and the last two are `w,x`.  Combine
all `81` root words with both orientations, giving `162` scalar rows.

Index the rows by `(rho,epsilon)` in `{0,1,2}^R x {+,-}`.  Put
`ell_u=ell_v=s` and `ell_w=ell_x=r`.  Define the following nine explicitly
orientation-masked companion columns:

```text
N_Q(rho,epsilon)=G_U(rho;omega^epsilon),

N_(q,t)(rho,epsilon)
 =1_(omega_t^epsilon=ell_t)
  G_((Q union U)-{q,t})
    (rho;omega^epsilon restricted to U-{t})           (21)
```

for `q in Q` and `t in U`.  Thus the columns at `w` and `x` are zero on the
orientation in which that singleton has the dead colour `a`; this masking is
part of the definition.  Let `N_(e,s)` be the `162 x 9` matrix with these
columns, and let

```text
nu_(e,s)=(h,(H_(q,t)(ell_t))_(q in Q,t in U)).        (22)
```

Finally define the desired column by

```text
g_(e,s)(rho,epsilon)
 =G_(U-e)(rho;omega^epsilon restricted to U-e).       (23)
```

### Theorem 7 (twelve simultaneous dense absorptions)

Every hypothetical witness in the dense cell satisfies

```text
rank[N_(e,s)|g_(e,s)]=rank N_(e,s)                   (24)
```

for all six edges and both active repeated colours: twelve two-orientation
packages, comprising twenty-four mixed port words and `1944` scalar root
coefficients in total.

### Proof

On either word (20), Lemma 6 kills all residual-absent labels and every
one-`Q` triple.  Pair diagonality kills every residual-present pair except
`Q union e`.  The dead shore kills the one-`Q` pair at the `a` singleton.
Thus each orientation contains `H_Q`, six one-`Q` pair coordinates, and the
shared desired coordinate

```text
H_(Q union e)(s,s)=K_e(s,s)!=0.                       (25)
```

Across both orientations, the nuisance union is exactly the nine columns
listed above.  Coefficientwise, (10) is therefore

```text
N_(e,s) nu_(e,s)+K_e(s,s)g_(e,s)=0.                  (26)
```

Division by the nonzero diagonal entry proves (24).  `square`

Every nonzero `10 x 10` minor of the augmented `162 x 10` matrix is a
predetermined coefficient-pure mixed detector.  Such minors are sufficient,
but are not exhaustive when `rank N_(e,s)<9`.  Equation (24), rather than
one chosen minor, is the exact statement.  These scalar coefficient rows are
not asserted to factor as legal complete-nuisance `GLD15` operator rows.

## 5. Sharp controls

The physical controls below are graph-side response or coefficient windows,
not witnesses or counterexamples.  The abstract linear control is labelled
separately.

1. **The excluded divisor is attained physically.**  Put
   `v_u^c=(1,1)`, `v_u^d=(1,-1)`, and `v_u^a=0` at all ports, take `B=0`,
   and set `h=0`.  Then every corrected block is
   `diag(2,-2,0)`, all seven response maps are zero, and the support lies in
   the dense cell.  Theorem 4 proves that no full witness can have this
   fixed-`Q` chart.
2. **The pure slice is nonempty at same-graph coefficient level.**  Keep the
   rational one-complete-clique channel, take `h!=0`, and graft one private
   root-to-port edge in missing colour `a` for each root/port pair in a fixed
   perfect matching.  Scaling one edge by `alpha_a/h` gives exactly the slice
   in (1).  This meets the new necessary coefficient data but is not claimed
   to meet every witness coefficient.
3. **The complete linear equation alone is insufficient.**  For any outside
   deck with `h!=0`, the abstract assignment

   ```text
   G_U=J_Q/h,             G_D=0 for D!=U              (27)
   ```

   satisfies `Gamma_Q(H)=J_Q`, (1), all Hamming-one equations, and all dense
   absorptions.  It need not be a principal-permanent companion family of the
   same graph.
4. **Dense detector properness.**  Add root-to-port edges only on one
   complement `U-e` and one nonzero root--root edge.  One selected
   `G_(U-e)` coefficient is nonzero while the nine nuisance coefficients
   vanish, so (24) fails and one mixed coefficient detects the graph.  With
   every root--root edge zero, all `G_(U-e)` vanish and the twelve absorptions
   hold trivially.  The outside dense response data are unchanged.
5. **The complete clique is load-bearing.**  Put both corrected colours only
   on one common edge and put one missing-colour direct singleton on another
   edge whose opposite corrected block is zero.  This is allowed by `GLD19`
   and has `F=empty`, but a missing-colour port-pair label survives on `a^4`;
   Lemma 3 no longer applies.

The exact private-root constructions can also be placed on the clean `GLD5`
chart.  Its root--root parameter is independent of `h`; the new obstruction
therefore neither manufactures nor forbids legal selector supply.

## 6. Exact frontier and scope ledger

```text
missing corrected-colour shores vanish with two colours:  PROVED;
B support lies in the complete corrected colour:          PROVED;
63 corrected / 1347 raw support patterns:                 PROVED;
all 1347 patterns lie in F=empty:                          PROVED;
h=0 portion of this full-witness subcell:                    EMPTY;
h!=0 pure root-to-four-port companion slice:              PROVED;
Hamming-one companion solve on secondary clique:          PROVED;
dense K4/K4 forces B=0 and has three raw masks:            PROVED;
twelve dense nine-nuisance absorptions:                    PROVED;
some dense augmented minor universally nonzero:           UNKNOWN;
h!=0 one-complete-clique subcell excluded:                 UNKNOWN;
pure companion slice integrated into same-graph witness:  UNKNOWN;
nonzero legal complete-nuisance operator package forced:  UNKNOWN;
other F=empty support cells excluded:                      UNKNOWN;
maximal star/triangle pure absorption excluded:            UNKNOWN;
weighted permanent implication:                           UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

Scope:

- **field:** characteristic zero;
- **breadth:** one fixed graph, residual pair, fully supported contraction,
  four roots, and one four-port window;
- **response hypothesis:** literal full-map zero at all six pair targets and
  the four-port target;
- **support subcell:** exactly two corrected-active colours, with at least one
  corrected support graph `K_4`;
- **excluded part:** precisely the contracted scalar divisor `h=0` in the
  `1347`-pattern subcell;
- **surviving obstruction:** nonzero pure `G_U(a^4)` plus Hamming-one
  relations, and twelve additional companion absorptions in the dense cell;
- **integrability boundary:** the formal assignment (27) is not a same-graph
  root-companion construction;
- **permanent implication:** none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_response_map_zero_dead_colour_h_gate_and_dense_companion_absorption.py
python -I claims/arbitrary-order/audit_fixed_q_response_map_zero_dead_colour_h_gate_and_dense_companion_absorption.py
```

The primary exact replay uses SymPy rational shores, complete enumeration of
the `31` labelled deck summands on the pure word, all eight dense Hamming-one
words, one proper-secondary outside-port word, and all twelve paired
`2+1+1` packages.  It also checks the `63/1347` support ledger, abstract rank
semantics, and exact positive/negative fixtures.  The independent audit
imports neither SymPy nor the primary.  It uses standard-library `Fraction`,
a separate sparse polynomial hafnian, direct raw-support products, and
independent rational elimination.

The programs audit the finite bridges, fixed-word survivor ledgers, rational
shore controls, pure-slice linear algebra, and abstract absorption-rank
semantics.  They do not instantiate a witness's actual `162 x 9` companion
matrices.  The arbitrary-field shore proof, use of the complete `GLD19`
alternatives, the coefficient identity (26), and the same-graph
interpretation of the full companion equation remain the load-bearing
written proof.  The private-root and `GLD5` controls in Section 5 are written
properness boundaries, not exhaustive scripted graph searches.
