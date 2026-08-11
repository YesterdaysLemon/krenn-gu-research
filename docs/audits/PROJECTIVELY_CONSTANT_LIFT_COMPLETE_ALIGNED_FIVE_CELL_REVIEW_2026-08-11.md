# Hostile review of the complete aligned five-cell detector

## Verdict and provenance

This record reviews
[`PROJECTIVELY_CONSTANT_LIFT_COMPLETE_ALIGNED_FIVE_CELL_TWO_OPEN_DETECTOR_THEOREM.md`](../../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_ALIGNED_FIVE_CELL_TWO_OPEN_DETECTOR_THEOREM.md)
as a conditional characteristic-zero theorem.

Review verdict: **accept complete conditional two-open detection in the
aligned common-two-row, projectively constant `q=0,r=5` cell**, after the
focused scripts and the full publication floor pass.  The exact conclusion is
that collective invisibility is impossible: at least one of the four
non-aligned roots has a nonzero complete two-open detector.

This review does not accept witness exclusion, fixed-root injectivity,
arbitrary permanent nonrestriction, extraction/gluing, or global resolution.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

Codex reconstructed the coefficient systems and incidence argument directly
from the owning fixed-layer theorems.  The review is durable adversarial
reasoning, not independent human review.  A first draft incorrectly claimed
that the `RRRRT` full common kernel survived only when all four ratios were
equal.  Hostile reconstruction found and preserved a second primitive-cube-
root divisor.  The corrected divisor still has kernel dimension one, so the
published detector implication survives without forcing the false
strengthening.

## 1. Exact imported obligation

The reviewed branch assumes all of the following.

1. The outside graph is in the aligned common-two-row, projectively constant
   consecutive-lift branch.
2. `q=0`, `r=5`, and the five outside modes form the fixed restriction

   ```text
   P_5(h_1,h_2,h_3,h_4,b)
     =sum_(c=0)^2 X_c e_c^(tensor 5),
   X_0 X_1 X_2!=0.                                  (1)
   ```

3. Every local map in (1) has rank three, every persistent root row family
   has full cross-mode span, and the four companions form the imported
   rank-two frame.
4. At a dependent mode `w`, collective invisibility gives an inactive set

   ```text
   I_w={p:P_4(h_p,a,a,b;B-{w})=0},       |I_w|>=2.   (2)
   ```

5. The five-mode row-pair theorem, the pair/triple/four-row Hall hierarchy,
   and the exact two-singleton `P_5` obstruction apply to (1).

The complex-only Hall and two-singleton statements transfer to any
characteristic-zero instance used here: its finitely many coefficients and
nonzero minors descend to a finitely generated extension of `Q`, which embeds
in `C` while preserving the tensor equality, zero supports, and nonzero
ranks.  The collision calculations themselves do not assume algebraic
closure.

## 2. The physical-row quota and exhaustive type words

The preceding fixed-layer theorem proves `b_w!=0` at every outside mode.
Thus every dependent `a/b` pair is exactly

```text
R: a_w=lambda_w b_w, lambda_w!=0;
B: a_w=0, b_w!=0.                                   (3)
```

The separately imported lifted-row Hall quota is

```text
p_a=#{w:a_w!=0}>=3q+2=2.                             (4)
```

At `q=0,r=5`, (4) permits at most three `B` defects.  This is a fixed-layer
consequence, not a detector calculation.  It removes the apparent four- or
five-`B` structural zero from the actual lifted diagonal identity.

After the already detected zero-, one-, two-, and three-defect cells, the
remaining type words are therefore exactly

```text
four defects: RRRRT, RRRBT, RRBBT, RBBBT;
five defects: RRRRR, RRRRB, RRRBB, RRBBB.             (5)
```

No `A`, `Z`, four-`B`, five-`B`, or additional proportionality type is hidden
outside (5).

## 3. Reconstructed four-defect kernels

Write

```text
K_w=ker(h -> P_4(h,a,a,b;B-{w})).                    (6)
```

The labelled collision identity is

```text
P_4(h,a,a,b)
 =2 sum_(i!=j) h_i tensor b_j tensor
    (tensor_(k notin {i,j}) a_k).                    (7)
```

### Three `B` modes

For `B` modes `u,v,w` and the two non-`B` modes `x,y`, deletion of `u`
leaves

```text
2 a_x tensor a_y tensor
  (h_v tensor b_w+b_v tensor h_w).                   (8)
```

Hence a pair of the three deletion kernels puts a row on the `b` line at all
three `B` modes, while the triple intersection is zero at all three and free
only at `x,y`.  Characteristic zero is used when the three scalar pair sums
force all three scalars to vanish.

### `RRRRT`: the missed divisor

Put `mu_i=1/lambda_i`.  After the off-line coordinates vanish, write

```text
h_i=alpha_i b_i, h_t=A a_t+B b_t+C c_t,
x_i=alpha_i/lambda_i.                                (9)
```

For every deleted regular index `u`, direct coefficient comparison gives

```text
X_u+B M_u=0,
X_u M_u-Y_u+A M_u=0,
C M_u=0,                                             (10)
```

with `X_u=sum_(i!=u)x_i`, `M_u=sum_(i!=u)mu_i`, and
`Y_u=sum_(i!=u)x_i mu_i`.  The four first equations give
`x_i=-B mu_i`.  A nonzero solution has `B!=0`, `C=0`, and

```text
e_2(mu_i:i!=u)=c M_u,              c=A/(2B).         (11)
```

Subtracting two copies of (11) yields

```text
(mu_v-mu_u)(sum_(k notin {u,v})mu_k-c)=0.            (12)
```

For four distinct values, two pairs sharing one endpoint make two other
values equal.  For a multiset `(a,a,d,e)`, the pairs `(a,d)` and `(a,e)` make
`d=e`.  Equation (12) also excludes a `3+1` split.  The surviving multisets
are exactly

```text
(a,a,a,a),
(a,a,d,d) with a!=d and a^2+ad+d^2=0.               (13)
```

In each case the full common kernel is one line, generated by

```text
(-b_0,-b_1,-b_2,-b_3,2c a_t+b_t),                   (14)
```

where `c=a` or `a+d`.  The second case is visible over `C` and invisible on a
rational ratio grid.  The original equal-ratios-only strengthening is
therefore **falsified and retained as such**.  The proof uses only the valid
uniform conclusion `dim intersection K_w<=1`.

### `RRRBT` and `RRBBT`

For three regular ratios, the `RRRBT` intersection is zero unless

```text
lambda_0+lambda_1+lambda_2=0.                        (15)
```

At (15) it is one line.  Direct substitution verifies the generator printed
in the theorem.  The reduction divides only by the three explicitly nonzero
regular ratios and by `3`, permitted in characteristic zero; no ratio
difference or `e_2` divisor is removed.

For `RRBBT`, the full common kernel is two-dimensional for every pair of
nonzero regular ratios.  Both `B` blocks vanish identically in that kernel.
This zero-at-both-`B` conclusion, rather than a generic-rank claim, is the
piece used by the detector proof.

### Four-defect inactive sets

At any retained defect, three deletion kernels force their inactive roots
onto its `b` line.  Local rank three makes the union of the corresponding
inactive sets have size at most two.  Since every inactive set has size at
least two, the `RRRRT`, `RRRBT`, and `RRBBT` patterns force one common root
pair in all four kernels.

- The first two common kernels have dimension at most one, so the two root
  families would be proportional.  Their five local pair spans have total
  coordinate-incidence capacity at most five, below the pair-Hall quota six.
- In `RRBBT`, both root rows vanish at both `B` modes, contradicting the
  five-mode row-pair incidence theorem directly.

For `RBBBT`, the three `B` inactive sets are exact pairs with empty triple
intersection.  Their only membership degree sequences are `(2,2,1,1)` and
`(2,2,2,0)`.  The latter leaves rank at most two at every `B` mode.  In the
former, local rank at a selected `B` mode requires both singleton-degree
roots to be inactive only there, which cannot hold at either of the other
two `B` modes.

## 4. Reconstructed five-defect cases

The same three-`B` argument excludes `RRBBB`.  The remaining cases use the
following exact coefficients.

### `RRRRB`

A regular deletion forces every retained regular value onto its `b` line.
Its retained-`B` coefficient is

```text
tau_u=e_2(lambda_v:v regular, v!=u).                 (16)
```

At least one `tau_u` is nonzero.  Otherwise, multiplying by nonzero
reciprocal products gives `sum_v mu_v-mu_u=0` for all four `u`; characteristic
zero then forces every nonzero reciprocal to vanish.  The four regular
inactive sets are one pair, and a nonzero `tau_u` connects the `B` inactive
set to it.  That pair lies on the `b` line at all five modes, below pair Hall.

### `RRRBB`

The two `B` inactive sets are one pair `J`; the three regular inactive sets
are one pair `K`.  The coefficient connecting the two pairs at a `B` mode is

```text
sigma=e_2(lambda_0,lambda_1,lambda_2).                (17)
```

If `sigma!=0`, local rank gives `J=K`, and pair Hall fails.  If `sigma=0`,
there are exactly three set-theoretic possibilities.

- `J=K`: the same pair-Hall contradiction.
- `J,K` share one root: `{b} union J` is a line at the three regular modes
  and at most a plane at the two `B` modes, so its triple-Hall capacity is
  `3+4=7<9`.
- `J` and `K` are complementary: this is the basis-free `3|2` line split
  reviewed below.

No division by `sigma` is made on its zero divisor.

### `RRRRR`

For deletion `u` and retained mode `v`, the exact off-line coefficient is

```text
q_uv=e_2(lambda_w:w notin {u,v}).                    (18)
```

With `mu_i=1/lambda_i` and `S=sum_i mu_i`, nonzero reciprocal products give

```text
q_uv=0 iff mu_u+mu_v=S.                              (19)
```

Let `F` contain the nonzero `q_uv` edges and let `H` join deletion indices
with a common `F` neighbour.  An `F`-isolated vertex would make the other four
reciprocals equal to `S-mu_u`; the sum equation forces that common nonzero
value to be zero.  Thus `F` has no isolated vertex.

The zero relation in (19) has a rigid value-class form: complementary value
classes give complete bipartite zero components, and a value `S/2` gives a
zero clique.  Checking the partitions of five vertices shows that `H` can be
disconnected only for

```text
mu=(a,a,a,a,-2a),          zero graph K_4;
mu=(-2a,-2a,a,a,a),        zero graph K_(2,3).       (20)
```

The exact graph verifier independently checks all `2^10` labelled zero graphs
by rational linear algebra; 15 labelled disconnected cases survive, namely
five `K_4` and ten `K_(2,3)` labellings.  This bounded census audits the
five-vertex classification; the value-class argument is the arbitrary-field
proof.

If `H` is connected, all inactive sets are one pair on the `b` line at every
mode.  For `K_4`, a triple has capacity `4*1+1*3=7<9`.  For `K_(2,3)`, triple
Hall reaches its lower bound nine only when the three-part inactive pair is
disjoint from both two-part pairs.  Those two pairs are then the same
complement, producing the final `3|2` split.

## 5. Basis-free `3|2` Hall bridge

Let the roots split into complementary pairs `J,K`, and the modes into
`U,V` with sizes three and two.  Assume `b,J` lie on one line at every mode
of `U`, while `b,K` lie on one line at every mode of `V`.

Row-pair incidence makes each such line a target coordinate axis.  At a
fixed `u in U`, call the axis `beta`, write `K={k_1,k_2}`, and consider the
four-row sets

```text
Q_i={b} union J union {k_i}.                          (21)
```

Local rank three gives the following basis-free dimensions.

- At each of the three `U` modes, `Q_i` is the plane `span(b,k_i)` and can
  contain at most two target coordinate axes.
- At each of the two `V` modes, `b,J` already span the full local target
  dual, so `Q_i` contains all three axes.

The total incidence capacity is `3*2+2*3=12`.  Four-row Hall requires each of
three colours in at least four modes, also 12.  Equality is forced at every
step.  Therefore both `span(b_u,k_(i,u))` are coordinate planes.  They are
distinct because the local map has rank three, so they are exactly the two
coordinate planes through the `beta` axis.

Consequently the two target coordinates other than `beta` pull back to the
two distinct singleton source rows `k_1,k_2`: the rows `b,J` have only a
`beta` component, and each `k_i` lies off `beta` in a different coordinate
plane.  This is exactly the hypothesis of the two-singleton `P_5`
obstruction.  No cross-mode basis identification or coordinate assignment is
used.

## 6. Computational independence and replay meaning

The SymPy primary verifier builds the labelled collision matrices from (7)
and checks:

- the `p_a>=2` type census;
- the three-`B` pair and triple kernels;
- the complete equal/cube-root/generic `RRRRT` divisor ledger;
- the `RRRBT` sum-zero line and the uniform `RRBBT` plane;
- all five-regular cofactor coefficients and the exact zero-graph census;
- one- and two-`B` forcing coefficients; and
- inactive-pair, triangle-degree, and Hall-capacity ledgers.

The independent audit imports no repository module and no computer algebra.
It constructs every coefficient through a recursive four-row permanent,
performs its own exact row reduction, and implements the quadratic field
`Q(w)` with `w^2+w+1=0` so the falsified rational-only strengthening cannot
regress.  It separately checks 256 rational `RRRRT` charts, the cube-root
chart, 64 `RRRBT` charts, 16 `RRBBT` charts, the three-`B` kernels, all exact
zero graphs, and independent bitmask Hall ledgers.

Neither script proves the arbitrary-field implication.  The written
coefficient, value-class, incidence, and support argument supplies the proof;
the scripts are exact convention and falsification checks.

## 7. Acceptance and residual boundary

Accepted after publication gates:

- the lifted quota excludes four and five `B` defects in this fixed layer;
- (5) exhausts the residual four- and five-defect cells;
- every word in (5) has at least one nonzero collective detector; and
- together with the preceding sequence, the complete aligned projective
  `q=0,r=5` cell is conditionally detected.

Explicitly **UNKNOWN**:

- whether a hypothetical witness exists or is excluded in this cell;
- fixed-root detector injectivity;
- any aligned `q=0,r>=6` or `q>=1` cell;
- every unfactorized outside graph;
- arbitrary weighted-permanent nonrestriction; and
- universal extraction, synchronization, and local-to-global gluing.

The original global conjecture remains **UNRESOLVED**, and this theorem has no
Lean formalization.

## Strongest fresh-referee objection

A fresh referee should first rederive the equality case in the four-row Hall
argument without choosing compatible bases across modes, then verify that its
two distinct planes really give two singleton target pullbacks at one local
map.  In parallel, the referee should reconstruct the `RRRRT` reciprocal
system (10)--(13), because any further unrecorded divisor with common-kernel
dimension at least two would invalidate the pair-Hall contradiction.  The
present proof and two exact implementations find no such residual.
