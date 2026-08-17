# Maximal-root surplus-two complete-deck sensor and higher-surplus depth boundary

## Status

**Exact characteristic-zero Universal Supply theorem on one determinantal
branch, with a sharp linear depth wall.**  Let `R` be a maximum torus-root
set of order `r>=2` in a hypothetical ternary Krenn--Gu witness, and let the
outside set have order `r+s`, where `s` is the even maximal-root surplus.
Leaving all root slots open, rather than evaluating them only at the selected
root vectors, gives an exact companion expansion.  A term using `p`
root--root edges contains an outside principal hafnian of order

```text
s+2p.                                                   (1)
```

Thus the contracted maximal-root equation is only the grade `p=0` member of
an exact uncontracted root-companion sensor.

At surplus two this sensor contains every nonempty even member of the same
outside principal hafnian deck; the empty member is the structural scalar
one.  If the companion sensor is injective over the outside function field,
the uncontracted GHZ target uniquely reconstructs the complete physical deck.
More minimally, a fixed residual pair is linearly identifiable by this sensor
exactly when the sensor kernel has zero projection to its residual-absent and
residual-present coordinates.  That condition is sufficient to recover the
actual physical paired family and legally supply the block-polarized `q=2`
response charts required by the response-atlas theorem.  Its failure does not
produce a second physical hafnian deck; it only records failure of this
linear sensor to certify uniqueness.

The full-rank condition is nonvacuous.  For every `r>=3` there is an explicit
maximum-root, triple-blocker graph-side chart with sensor rank

```text
2^(r+1)-1,                                               (2)
```

the number of nonempty even outside deck members.  This proves that the
rank-drop condition is a proper ambient determinantal boundary even after the
maximum-root and blocker-incidence requirements are imposed.  It does **not**
prove that the full-rank open meets the hypothetical-witness locus.

At every surplus `s>=4`, the residual edge `H_Q` and every residual-absent
pair `H_{uv}` lie below the depth floor (1) and occur in no root companion
column.  Hence no linear root-word selector can supply even the constant and
pair anchors of a complete `q=2` response.  Nonlinear target coupling,
cross-window information, or a different complete-deck sensor is then
essential.

Complete-deck supply is not permanent extraction.  It does not prove that the
corrected two-row channel has a weighted diagonal target, does not force a
three-group identifying overlap, and does not turn a rank defect into a mixed
GHZ coefficient.  Those implications remain separate.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. The uncontracted root-companion expansion

Work over a characteristic-zero field `K`.  Let

```text
Omega=R disjoint-union B,
|R|=r,                  |B|=r+s,                      (3)
```

where `s>=0` is even.  Fix fully supported root vectors `x_i`, `i in R`,
such that

```text
W_ij(x_i,x_j)=0                    for i!=j.           (4)
```

For every even `I subset B`, let `H_I` be the physical perfect-matching
tensor of the graph induced by `I`, with `H_empty=1`.

Fix vectors `z_u` at the outside modes while leaving every root slot open.
For `D subset B`, define the root companion tensor `G_D(z_D)` by choosing

1. a partial matching `P` among the roots;
2. a bijection from the roots not used by `P` to `D`;
3. the corresponding root--root and root--outside edge blocks;

and summing their products.  Equivalently `G_D=0` unless

```text
|D|<=r,                 |D| congruent r (mod 2).       (5)
```

### Theorem 1 (surplus-graded companion expansion)

The full tensor with the root slots open is

```text
T_W(-_R,z_B)
 =sum_(D subset B, (5)) G_D(z_D) H_(B-D)(z_(B-D)).    (6)
```

If the root partial matching has `p` edges, then its outside hafnian label
`I=B-D` satisfies

```text
|D|=r-2p,                 |I|=s+2p.                   (7)
```

For a hypothetical ternary witness, the left side of (6) is the known target
tensor

```text
J_R(z_B)
 =sum_(c=0)^2
    product_(u in B) z_u[c]
    tensor_(i in R) e_(i,c)^*.                        (8)
```

### Proof

Restrict a perfect matching of `R union B` to the root vertices.  The roots
matched to one another form a unique partial matching `P`.  Every remaining
root has a distinct outside partner, giving a bijection to a set `D`.  The
remaining outside set `B-D` is matched internally and contributes `H_(B-D)`.
Conversely one root partial matching, one such bijection, and one perfect
matching of `B-D` reconstruct one full perfect matching.  This is a
weight- and multiplicity-preserving bijection and proves (6).

If `P` has `p` edges, it occupies `2p` roots, so `|D|=r-2p`.  Subtracting
from `|B|=r+s` gives (7).  Equation (8) is the original GHZ equality with the
outside slots evaluated.  No genericity, division, or selector is used.

Evaluating all open root slots at `x_R` kills every term with `p>0` by (4).
The remaining grade `p=0` is exactly the fixed-surplus maximal-root identity.
Thus the additional grades in (6) use genuine uncontracted target equations;
they are not inferred from the contracted fixed layer alone.

## 2. Adjacent `q=2` response grades

Fix a named pair

```text
Q={q_0,q_1} subset B,          U=B-Q.                 (9)
```

For every even `T subset U`, the residual-absent and residual-present deck
members are

```text
M_T=H_T,                    Z_T=H_(Q union T).         (10)
```

### Corollary 2 (adjacent-grade rule and depth floor)

Whenever both members in (10) occur in (6), their root--root grades are

```text
p_M=(|T|-s)/2,              p_Z=p_M+1.                (11)
```

Consequently:

1. at `s=0`, the complete even deck occurs and the base equation already
   extracts the known weighted `P_r` restriction;
2. at `s=2`, every nonempty even deck member occurs, while `H_empty=1` is
   known structurally;
3. at `s>=4`, `Z_empty=H_Q` and every `M_{uv}=H_{uv}` have order two and
   occur in no companion column.

In case 3, no root word and no linear combination of root words is a
selector for those missing labels.

### Proof

Substitute `|I|=|T|` and `|I|=|T|+2` into (7).  This gives (11).  At
surplus two the possible orders are `2,4,...`, through the largest legal even
subset of `B`; together with the empty scalar these are all even subsets.
At `s>=4`, order two lies strictly below the minimum in (7), so the named
columns are absent, not merely dependent.  Linear combinations cannot create
a column absent from every summand of (6).

This is a linear observability wall.  A target-specific nonlinear identity
between different physical hafnian depths is additional information and is
not ruled out.

## 3. The surplus-two deck sensor

Now put `s=2`.  Let

```text
X=product_(u in B) P(V_u),
E_+=direct-sum_(empty!=I subset B, |I| even) O_X(1_I),
F=(tensor_(i in R) V_i^*) tensor O_X(1_B).            (12)
```

For each nonempty even `I`, multiplication by the companion
`G_(B-I)`, a section on the complementary outside modes, defines a bundle map

```text
Gamma_2:E_+ -> F.                                    (13)
```

It has

```text
rank E_+=2^(r+1)-1.                                  (14)
```

Over the function field `K(X)`, equation (6) is

```text
Gamma_2(H)=J_R.                                      (15)
```

### Theorem 3 (complete-deck and fixed-pair supply)

Suppose the data come from one physical ternary graph and satisfy the GHZ
target equality.

1. If `Gamma_2` has column rank `2^(r+1)-1` over `K(X)`, then (15) uniquely
   determines every nonempty even `H_I`.  The structural value
   `H_empty=1` completes the deck.
2. Fix `Q` as in (9).  Let `C_Q` be the nonempty even labels meeting `Q` in
   zero or two vertices, and let `N_Q` be the labels meeting it in one.
   Among unrestricted `K(X)`-rational coordinate arrays satisfying (15), the
   complete `C_Q` coordinate family is uniquely determined exactly when

   ```text
   pi_(C_Q)(ker Gamma_2)=0.                            (16)
   ```

   Equivalently,

   ```text
   rank[Gamma_(N_Q) Gamma_(C_Q)]-rank Gamma_(N_Q)
     =|C_Q|=2^r-1.                                    (17)
   ```

   When this condition holds, it in particular recovers the actual physical
   paired family (10).  When it fails, this linear sensor alone does not
   certify uniqueness; no second regular or physical hafnian deck is implied.
3. Let `P_2` be the set of all pair labels in `B`.  If

   ```text
   pi_(P_2)(ker Gamma_2)=0.                           (17a)
   ```

   then the target uniquely identifies every physical outside edge block.
   Those labeled pair blocks generate the complete same-graph hafnian deck
   by the ordinary matching recurrence.  For every chosen residual pair they
   also reconstruct the residual incidence rows in their physical gauge.

On either branch of the conclusion, the recovered objects are the actual
multilinear principal tensors of the original graph.  Hence they give, after
contracting the fixed named residual pair, fully block-polarized physical
`q=2` responses `M,Z` on every port subset.  They satisfy dual-Wick, use the
same residual incidence rows on every restriction, and have trivial physical
atlas holonomy.

### Proof

Full column rank makes (15) have at most one solution over `K(X)`.  The
physical graph supplies one global regular solution, so the unique rational
solution is exactly its principal hafnian deck.  No pole-removal or Wick
completion assumption is inserted: existence and physicality precede the
linear reconstruction.

For the fixed pair, two unrestricted rational coordinate arrays give the
same target precisely when their difference lies in `ker Gamma_2`.  Their
`C_Q` coordinates are equal for every such pair exactly when (16) holds.
Splitting the columns into `N_Q` and `C_Q` gives the quotient-rank statement
(17).  This is the standard labeled linear-selector criterion applied to the
present full ternary root sensor.  Since the actual graph deck is one such
array, the condition recovers it.  Conversely a kernel vector need not obey
regularity or the nonlinear matching recurrences, so failure of (16) is not
a physical nonuniqueness theorem.

For item 3, a loopless block graph is determined by its pair tensors.  The
perfect-matching recurrence constructs every higher `H_I` from those blocks,
and contraction of the reconstructed `Q`--port blocks gives its two residual
rows.  This proves the additional conclusion.

Finally, (10) are literal restrictions of the recovered graph deck.  The
physical response factorization and common residual rows follow from the
matching partition defining the residual-relative response.  One graph's
global rows trivialize every overlap transition.

The theorem supplies data, not GLQ2 identifiability: a useful atlas still
needs three mutually cross-observed rank-two port groups on each overlap.

## 4. A full-rank maximum-root chart

The rank hypothesis in Theorem 3 is not an empty ambient condition.

Choose, at each root, independent covectors `a_i,b_i,c_i`.  Label

```text
B={u_1,...,u_r,q_0,q_1}.                              (18)
```

At one outside evaluation, prescribe the root companions

```text
W_ij=b_i tensor b_j,
W_(i,u_j)(-,z_(u_j))=delta_(ij) a_i,
W_(i,q_0)(-,z_(q_0))=b_i,
W_(i,q_1)(-,z_(q_1))=c_i.                            (19)
```

For `D={u_i:i in S} union E`, put `l=r-|S|`.  Direct matching gives

```text
E=empty, l even:
  G_D=(l-1)!! a_S b_(S^c);

E={q_0}, l odd:
  G_D=l!! a_S b_(S^c);

E={q_1}, l odd:
  G_D=(l-2)!! sum_(j notin S) a_S c_j b_(S^c-{j});

E={q_0,q_1}, l even>=2:
  G_D=(l-1)!! sum_(j notin S) a_S c_j b_(S^c-{j}).    (20)
```

Use `(-1)!!=1`.

### Theorem 4 (explicit full-rank chart)

The columns in (20) are linearly independent.  Hence (19) has companion
sensor rank `2^(r+1)-1` for every `r>=2`.

For every `r>=3`, a parameterized realization of (19) may additionally be
chosen so that:

- the displayed root set is maximum-cardinality;
- every root vector is in the coordinate torus;
- every outside mode is a triple blocker, so all three blocker quotas hold;
- the sensor remains full rank.

This maximum-root chart is not asserted to satisfy the GHZ target equality.

### Proof

For each `S!=[r]`, parity permits exactly one column in (20) containing no
`c` and one containing exactly one `c`.  For `S=[r]`, only the all-`a`
column remains.  The no-`c` columns are distinct `a/b` basis words.  The
one-`c` sums for different `S` have disjoint `a`-supports, and their supports
are disjoint from every no-`c` word.  Characteristic zero keeps all displayed
double factorials nonzero.  There are

```text
2^r+(2^r-1)=2^(r+1)-1                                (21)
```

independent columns.

For compatibility with maximum roots, work over `C`.  Take `a_i=e_0^*`,
`c_i=e_2^*`, take `b_1=e_1^*`, and for `i>=2` choose

```text
x_i=(1,lambda_i,mu_i) in (C^*)^3,
b_i=e_1^*-lambda_i e_0^*,                            (22)
```

with any torus `x_1`.  Then every evaluated root--root edge in (19) is zero:
among a pair of roots, at least one index is at least two and its `b` value
vanishes.

Realize all clean contractions (19) first.  Give each private `u_i` its sole
nonzero root edge `a_i tensor e_0^*`; give every root--`q_0` edge the block
`b_i tensor e_0^*`; and give every root--`q_1` edge the block
`c_i tensor e_0^*`, at torus outside points with `e_0^*(z_u)=1`.  The
assigned nonzero coordinate edges are `e_0^* tensor e_0^*` from root `i` to
`u_i`, `e_1^* tensor e_0^*` from root `1` to `q_0`, and
`e_2^* tensor e_0^*` from root `2` to `q_1`.  At this clean parameter value,
every outside evaluated row span contains `e_0^*` and the sensor is exactly
the full-rank sensor (19).

At every outside mode, use two nonassigned roots to add
parameter-multiplied bilinear blocks whose evaluations at `x_R` are the two
remaining coordinate covectors.  Such a block exists after matching the one
compatibility scalar between its prescribed contraction at `z_u` and its
prescribed evaluated row at `x_i`; an explicit interpolation is

```text
g tensor eta + xi tensor H - g(x_i) xi tensor eta,    (23)
```

where `xi(x_i)=eta(z_u)=1`, the root contraction is `g`, and the evaluated
outside row is `H`, with `H(z_u)=g(x_i)`.  Scaling these perturbations by
independent parameters makes their contractions perturb the clean columns
polynomially.  At parameter zero the minor proved nonzero above is its
nonzero constant term.  Since `C` is infinite, choose all parameters nonzero
off the zero sets of that minor and of the finitely many assigned-edge
evaluations.  Every outside evaluated row span then contains
`e_0^*,e_1^*,e_2^*`, every assigned edge remains nonzero, and the sensor
remains full.

Finally make every outside--outside block a nonzero coordinate monomial.
Two outside torus vectors can then never be zero-coupled.  If a torus-root
configuration contains one outside vertex, its assigned coordinate edge
prevents it from containing the assigned old root, so its size is at most
`r`.  The displayed `R` already has size `r`, proving maximum cardinality.

This construction meets the graph-side maximum-root and blocker-incidence
conditions only.  It does not prove that the determinantal open meets the
witness variety.

## 5. Coordinate-absorption and permanent interfaces

In the coordinate two-residual branch of the maximal-root theorem, write
`C` for the old blocker union, so `|C|=r+2`, and retain
`Q_0={q_0,q_1}` for the two original nonblocker residuals.  Promoting `q_0`
gives roots `R_0=R union {q_0}` and outside set
`B_0=C union {q_1}`; promoting `q_1` separately gives
`R_1=R union {q_1}` and `B_1=C union {q_0}`.  Both are surplus-two cells.

Fix any named residual pair `Q_* subset C`, with the same contractions in
the original graph, and apply Theorem 3 to each promoted cell.  If both
promoted sensors satisfy (16) for `Q_*`, they reconstruct paired response
charts on

```text
(C-Q_*) union {q_1},        (C-Q_*) union {q_0}.       (24)
```

Their overlap is `C-Q_*`, of order `r>=3`, and the reconstructed tensors
agree because they
are restrictions of the same original graph.  If the overlap also contains
three rank-two cross-observed port groups, the response-atlas theorem gives
its unique `O(J)` transition.  Rank observability and overlap identifiability
are distinct hypotheses.

There is also an exact target-attachment formula, but it requires another
grade.  In a surplus-two cell with `rho` roots, choose `Q={q_0,q_1}` and put
`U=B-Q`.  For a root pair `A={i,j}`, the corrected response rows `a,b` give

```text
Pi_(A,Q)
 =sum_(u<v in U) K_uv tensor
    P_(rho-2)(H_w[R-A]:w in U-{u,v})
 =P_rho(H_(R-A);a;b).                                 (25)
```

Thus if an independently legal root-pair selector makes `Pi_(A,Q)` weighted
diagonal with three nonzero weights, it extracts `P_rho -> Delta_3`.
Deck supply alone does not provide that target statement.

## 6. Exact frontier

```text
uncontracted companion expansion and grade rule:       PROVED;
surplus-two complete deck present in the root sensor:   PROVED;
full-sensor complete-deck reconstruction:               PROVED CONDITIONAL;
fixed-pair kernel criterion for linear sensor:          NECESSARY AND SUFFICIENT;
fixed-pair criterion for physical deck supply:          SUFFICIENT;
pair-block kernel-projection criterion:                 SUFFICIENT FOR ALL CHARTS;
full-rank maximum-root/triple-blocker ambient chart:    PROVED;
surplus >=4 low q=2 columns in root words:              ABSENT;
full-rank or Q-observable sensor forced in every witness: UNKNOWN;
three-group GLQ2 overlap forced after supply:            UNKNOWN;
corrected channel weighted diagonal:                    UNKNOWN;
nuisance-free root-pair target selector:                 UNKNOWN;
all-balanced rank-drop witness exclusion:                UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

The breadth used by the positive theorem is one complete uncontracted
surplus-two root sensor, or two such sensors after coordinate absorption.
Its depth is every root--root grade of that one cell.  The reconstructed
hidden object is the complete physical outside deck.  The transition group
on later identifying `q=2` overlaps is `O(J)`.  Agreement supplies a common
physical response graph; it does not by itself glue a permanent restriction.
Rank disagreement is a determinantal supply failure, not a mixed target
coefficient.

## Focused checks

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_complete_deck_sensor_and_higher_surplus_depth_boundary.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_complete_deck_sensor_and_higher_surplus_depth_boundary.py
```

The primary verifier builds the companion columns by an exact matching
recurrence, checks the formulas and ranks through `r=7`, and checks the
surplus-grade and fixed-pair label counts.  The independent no-import audit
uses residual-to-root injections and disjoint pivot supports rather than the
primary recurrence, together with a separate grade ledger and capacity
counts.  These bounded replays audit (7), the cardinality in (17), and (20);
they do not compute a symbolic `Gamma_2` kernel.  The arbitrary-order matching
bijection, quotient-rank criterion, maximum-root construction, and
basis-support argument above are the proof.

Dependencies:

- [`MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md`](MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md)
- [`LOWER_MIXED_ROOT_JET_DELETION_LABEL_TOMOGRAPHY_AND_SQUAREFREE_GAUGE_THEOREM.md`](LOWER_MIXED_ROOT_JET_DELETION_LABEL_TOMOGRAPHY_AND_SQUAREFREE_GAUGE_THEOREM.md)
- [`TWO_RESIDUAL_RESPONSE_ATLAS_IDENTIFYING_OVERLAP_AND_HOLONOMY_BOUNDARY_THEOREM.md`](TWO_RESIDUAL_RESPONSE_ATLAS_IDENTIFYING_OVERLAP_AND_HOLONOMY_BOUNDARY_THEOREM.md)
