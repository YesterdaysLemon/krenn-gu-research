# Projectively constant lift: complete three-defect five-cell detector

## Status

**Exact conditional characteristic-zero detector theorem and boundary
reduction.**  Work in the aligned common-two-row, projectively constant tight
cell

```text
q=0,                  r=5,                  |B|=5.    (1)
```

For each outside mode put

```text
S_w=span(a_w,b_w),
D={w in B:dim S_w<=1}.                                (2)
```

Then two new conclusions hold.

1. A mode with `b_w=0` is incompatible with the fixed five-mode permanent
   restriction.  Thus every actual defect has `b_w!=0` and is exactly one of

   ```text
   R: a_w=lambda_w b_w, lambda_w!=0     (regular);
   B: a_w=0,              b_w!=0        (b-only).     (3)
   ```

2. If `|D|=3`, at least one non-aligned root has a nonzero complete two-open
   detector, for every one of the four remaining type multisets

   ```text
   RRR,                 RRB,                 RBB,                 BBB.    (4)
   ```

Together with the preceding five-cell theorems, this gives conditional
detection for **every aligned projective `q=0,r=5` cell with at most three
local `a/b` defects**.  It also excludes every `A`- or `Z`-type defect at the
fixed `P_5` layer, independently of the number of defects.

This is not witness exclusion.  It does not prove fixed-root injectivity,
treat cells with four or five `R/B` defects, treat `q=0,r>=6` or `q>=1`,
address an unfactorized outside graph, or supply universal
extraction/gluing.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Imported five-cell system

Use the hypotheses and notation of the
[`three-activity theorem`](PROJECTIVELY_CONSTANT_LIFT_THREE_ACTIVITY_AND_MIXED_DEGENERATE_TWO_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md).
The four non-aligned roots are

```text
P={1,2,3,4}.                                          (5)
```

Their fixed five-mode restriction is

```text
P_5(h_1,h_2,h_3,h_4,b)
 =sum_(c=0)^2 X_c e_c^(tensor B),
X_0 X_1 X_2!=0.                                      (6)
```

Every local flattening of (6) has rank three, and every persistent root row
family `h_p=(h_(p,w))_(w in B)` has full cross-mode span.  For a defect `w`,
put

```text
R_(p,w)=P_4(h_p,a,a,b;B-{w}),
I_w={p in P:R_(p,w)=0}.                               (7)
```

Collective invisibility means that all four projective two-open coefficients
`C_i` vanish.  The imported three-activity theorem then gives

```text
|I_w|>=2                         for every w in D.    (8)
```

We also import two exact facts about the fixed restriction (6).

- The
  [`five-mode row-pair incidence theorem`](ARBITRARY_PERMANENT_FIVE_MODE_ROW_PAIR_INCIDENCE_THEOREM.md)
  says that the local span of every two source rows contains a target
  coordinate covector at every one of the five modes.
- The
  [`two-singleton coordinate obstruction`](../p5/coordinate-cegar/P5_TWO_SINGLETON_COORDINATE_OBSTRUCTION.md)
  excludes a `P_5 -> Delta_3` restriction when two target-coordinate
  pullbacks are supported on two distinct singleton source rows.  In
  particular, it excludes a local `2+1+1` coordinate-row profile together
  with one zero source row.

The second theorem is stated over `C`, which is enough over every
characteristic-zero field here.  Indeed, a hypothetical restriction and all
of its nonzero minors use finitely many coefficients.  They descend to a
finitely generated field over `Q`, which embeds in `C`; the tensor equality,
the zero pattern, and the nonzero minors survive that embedding.  The
nonzero weights `X_c` may first be normalized at one target mode without
changing any source-row support.

## 2. A zero `b` row is impossible

### Lemma 1 (fixed-layer `A/Z` exclusion)

Every mode of (6) has

```text
b_w!=0.                                               (9)
```

Consequently a dependent pair `a_w,b_w` is of type `R` or `B` in (3); the
previously named types

```text
A: a_w!=0,b_w=0,              Z: a_w=b_w=0           (10)
```

cannot occur in an actual fixed five-cell restriction.

### Proof

Suppose `b_w=0`.  For every root `p`, apply row-pair incidence to the source
pair `{b,h_p}`.  Its local span at `w` is the line `<h_(p,w)>`, so that line
must contain a target coordinate covector.  Thus each of the four root rows
is a nonzero coordinate row at `w`.

Local rank three forces all three coordinate axes to occur among those four
rows.  Their multiplicities are therefore `2+1+1`, while the fifth source row
`b_w` is zero.  The two singleton colours are supported on two distinct
source rows, contradicting the imported two-singleton obstruction.  This
proves (9).  If `dim S_w<=1`, (9) leaves exactly the alternatives in (3).

## 3. Exact three-defect collision ledger

Let the three defects be `u,v,w` and the two transverse modes be `s,t`.
At a regular defect write

```text
a_z=lambda_z b_z,                 lambda_z!=0.        (11)
```

Choose an independent local basis `(a_z,b_z,c_z)` at a transverse mode and
normalize `b_z` to the first basis vector at a defect.  Expanding

```text
P_4(h,a,a,b)
 =2 sum_(i!=j) h_i tensor b_j tensor
    (tensor_(k notin {i,j}) a_k)                     (12)
```

in the labelled word basis gives the following exact retained-operator
table.  The rank is the rank on the twelve retained local coordinates; the
deleted value of `h` is free.

| retained types | rank | every retained kernel row satisfies |
|---|---:|---|
| `RRTT` | 10 | `h_R in <b_R>` and `h_T in S_T` |
| `RBTT` | 9 | `h_R,h_B in <b>` and `h_T in S_T` |
| `BBTT` | 5 | `h_B in <b_B>`; the transverse values are free |

Coefficient comparison in (12) also gives the exact intersections below.
They are statements about full five-mode row families, not graph witnesses.

### Lemma 2 (`RRB` intersections)

Suppose `u,v` are regular, `w` is `B`, and `s,t` are transverse.  Then

```text
ker R_(-,u) intersection ker R_(-,w)={0},
ker R_(-,v) intersection ker R_(-,w)={0}.             (13)
```

The remaining common kernel has dimension three.  In the normalized chart it
is

```text
h_u=(gamma-lambda_u(alpha+beta)) b_u,
h_v=(gamma-lambda_v(alpha+beta)) b_v,
h_w=-gamma b_w,
h_s=alpha a_s+gamma b_s,
h_t=beta  a_t+gamma b_t.                             (14)
```

In particular, every row in this common kernel lies in `S_s` and `S_t` at
the transverse modes.

### Lemma 3 (`RRR` ratio intersections)

Suppose `u,v,w` are regular.

1. If `lambda_u!=lambda_v`, then

   ```text
   ker R_(-,u) intersection ker R_(-,v)={0}.          (15)
   ```

2. If `lambda_u=lambda_v`, that pair intersection has dimension two and all
   its defect values lie on the corresponding `b` lines, while its values at
   `s,t` lie in `S_s,S_t`.
3. The triple intersection is zero unless

   ```text
   lambda_u=lambda_v=lambda_w=L.                     (16)
   ```

   Under (16) it is the one-dimensional family

   ```text
   h_u=h_v=h_w=0,
   h_s=-rho((2/L)a_s+b_s),
   h_t= rho((2/L)a_t+b_t).                           (17)
   ```

For completeness, when `lambda_u=lambda_v=L` and `lambda_w=M!=L`, a basis
of the pair intersection is given by the following two five-block rows:

```text
(-L(2L+M)b_u, -L(2L+M)b_v, M(L+2M)b_w,
 (L-M)a_s, (L-M)a_t),

(L(L+M)(2L+M)b_u, L(L+M)(2L+M)b_v,
 -M(L+M)(L+2M)b_w,
 -2(L+M)(L-M)a_s-LM(L-M)b_s, LM(L-M)b_t).            (18)
```

When `M=L`, a basis is

```text
(-b_u,-b_v,b_w,0,0),
(0,0,0,-((2/L)a_s+b_s),((2/L)a_t+b_t)).              (19)
```

The second row of (19) is precisely the triple kernel (17).

### Lemma 4 (`RBB` triple intersection)

Suppose `u` is regular and `v,w` are `B`.  The common kernel of all three
deletions is two-dimensional:

```text
h_u=-lambda_u(alpha+beta)b_u,
h_v=h_w=0,
h_s=alpha a_s,
h_t=beta a_t.                                       (20)
```

### Lemma 5 (`BBB` intersections)

Suppose all three defects are `B`.  For distinct defects `u,v`, with third
defect `w`, their pair intersection is

```text
h_u=-gamma b_u,       h_v=-gamma b_v,       h_w=gamma b_w,
h_s,h_t arbitrary.                                      (21)
```

The triple intersection is therefore

```text
h_u=h_v=h_w=0,       h_s,h_t arbitrary,              (22)
```

and has dimension six.

### Proof of Lemmas 2--5

Use (12), first comparing every coefficient containing a local third-basis
vector.  This gives the forced-line and forced-plane entries in the table.
The words with two transverse `b` entries then determine the defect-line
coefficients, the words with one transverse `b` entry determine the mixed
coefficients, and the pure-`a` word supplies the final scalar relation.

For `RRB`, these relations are exactly (13)--(14).  In the lexicographic
labelled-word row order used in the replay, the regular/`B` stacks have
full-rank minors

```text
-196608 lambda_u^3 lambda_v^7,
 196608 lambda_u^7 lambda_v^3.                        (23a)
```

so no exceptional nonzero regular ratio is omitted.  For `RRR`, stacking two
deletions has a full-rank minor

```text
196608 lambda_v^3 lambda_w^7
       (lambda_u-lambda_v)^2.                         (23b)
```

Here the first deletion contributes rows `0,...,80`, the second contributes
rows `81,...,161`, each block is ordered by the words
`(0,0,0,0),...,(2,2,2,2)`, and the selected rows are

```text
0,1,3,4,5,7,9,18,27,54,81,82,84,108,135.            (23c)
```

Thus (15) follows without a genericity assumption.  Substitution at equality
gives (18)--(19), and stacking
the third deletion leaves exactly (17).  The same comparison gives (20),
while with three zero `a` rows the only possibly nonzero part of a retained
collision assigns `h,b` to the two retained `B` modes; this is exactly
(21)--(22).  No division other than by the nonzero regular ratios is used.

The primary verifier reconstructs all matrices and candidate bases directly.
The no-import audit instead evaluates labelled permanents recursively and
uses rational row reduction over a grid containing equal, unequal, and
opposite regular ratios.

## 4. The `RRB` and `RRR` cells detect

### Theorem 6 (`RRB` detector)

An exactly-three-defect `RRB` cell has some nonzero `C_i`.

### Proof

Assume collective invisibility.  Let `I_u,I_v` be the inactive sets at the
regular defects and `I_w` the inactive set at the `B` defect.  By (8), all
three have size at least two.  Equation (13) and full root-row span make

```text
I_u intersection I_w=empty,
I_v intersection I_w=empty.                          (24)
```

There are only four roots, so `I_w` is a two-set and both regular inactive
sets equal its two-element complement.

Rows in `I_w` belong to the `RRTT` kernel, hence lie in `S_s,S_t` at both
transverse modes.  Rows in its complement belong to the common regular
kernel (14), and have the same property.  Thus all four roots and the fixed
row `b` lie in the two-plane `S_s` at mode `s`, contradicting the rank-three
flattening of (6).  Collective invisibility is impossible.

### Theorem 7 (`RRR` detector)

An exactly-three-defect `RRR` cell has some nonzero `C_i`.

### Proof

Assume collective invisibility.  First, every inactive set has size exactly
two.  The lower bound is (8).  If, say, `|I_u|>=3`, the `RRTT` row in the
table puts those three roots on the `b_v` line at another regular defect
`v`.  Together with `b_v`, four fixed source rows lie on one line and the
fifth can raise their span to at most two, contradicting local rank three.

If the three ratios are pairwise distinct, (15) makes the three two-element
inactive sets pairwise disjoint, impossible on four roots.

If exactly two ratios agree, relabel so that

```text
lambda_u=lambda_v!=lambda_w.                         (25)
```

The unequal-ratio intersections make `I_w` disjoint from both `I_u` and
`I_v`.  Hence `I_u=I_v=P-I_w`.  The two roots in the common equal-ratio
kernel and the two roots in the `w`-deletion `RRTT` kernel all lie in
`S_s,S_t`.  Again every fixed source row lies in `S_s`, contradicting rank
three.

It remains that all three ratios are equal.  A root cannot lie in all three
inactive sets: (17) would support its row family at only the two transverse
modes, so its cross-mode span would have dimension at most two.  Three
two-subsets of a four-set, with empty triple intersection, have one of the
two degree sequences

```text
(2,2,1,1)                 or                 (2,2,2,0).    (26)
```

In the first sequence every root lies in at least one inactive set, and the
`RRTT` table puts every root in `S_s,S_t`, giving the same transverse
rank-two contradiction.  In the second sequence, three roots each lie in a
pair intersection.  Lemma 3 puts those three roots and `b` on one line at
every regular defect, while the remaining root can raise the local span only
to two.  This final contradiction proves the theorem.

## 5. The `RBB` and `BBB` cells detect

### Theorem 8 (`RBB` detector)

An exactly-three-defect `RBB` cell has some nonzero `C_i`.

### Proof

Let `u` be regular and `v,w` be `B`.  Under collective invisibility, each
`B` inactive set has size exactly two.  The lower bound is (8).  If
`|I_v|>=3`, the `RBTT` kernel puts those roots on the `b_w` line at the other
`B` defect; together with `b_w`, local rank is at most two.

If `I_v union I_w=P`, every root belongs to an `RBTT` kernel and hence lies
in `S_s,S_t` at the transverse modes, again contradicting rank three.  Thus
the two `B` sets either agree or form a proper three-root diamond.  A diamond
puts its three-root union on the `b_u` line by the `RBTT` table.  Together
with `b_u` this leaves only one row off the line, so a diamond is impossible.
Consequently

```text
I_v=I_w=J,                         |J|=2.             (27)
```

At either `B` defect, the two roots in `J` lie on the `b` line.  The two
complementary roots must both be off that line and independent modulo it in
order to give local rank three.  But every root in `I_u` belongs to a `BBTT`
kernel and lies on the `b` line at both `B` defects.  Therefore (8) forces

```text
I_u=J.                                                (28)
```

Lemma 4 now makes the two `J` root values zero at both `B` defects.  At one
such mode the three remaining source rows are `b` and the two complementary
roots, and they have rank three.  Row-pair incidence applied to a zero root
and each remaining row makes all three nonzero rows coordinate rows on three
distinct axes.  The local profile is therefore three singleton coordinate
rows plus two zero rows.  In particular it has two target coordinates
supported on distinct singleton source rows, contradicting the imported
two-singleton obstruction.  Hence some detector is nonzero.

### Theorem 9 (`BBB` detector)

An exactly-three-defect `BBB` cell has some nonzero `C_i`.

### Proof

Assume collective invisibility.  As above, the `BBTT` table and local rank
give

```text
|I_u|=|I_v|=|I_w|=2.                                 (29)
```

No root belongs to all three sets: by (22) its row family would be supported
at only the two transverse modes and could not have full cross-mode span.
Thus the membership degrees again have one of the two forms (26).

For `(2,2,2,0)`, each of the three degree-two roots lies in a pair common
kernel.  Equation (21) puts those three roots and `b` on one line at every
`B` defect, leaving local rank at most two.

For `(2,2,1,1)`, consider any defect, say `u`.  Every root belonging to one
of the other two inactive sets lies on the `b_u` line by the `BBTT` table.
Local rank three therefore requires two roots whose only inactive-set
membership is `I_u`.  The degree sequence has exactly two singleton roots,
so both would have to belong only to `I_u`.  They cannot simultaneously have
their sole membership at either of the other two defects.  Local rank fails
there.  Both degree patterns are impossible, proving the theorem.

## 6. Exact residual boundary

Combining Lemma 1 and Theorems 6--9 with the preceding five-cell results
gives

```text
any q=0,r=5 mode with b_w=0:                           IMPOSSIBLE FIXED LAYER;
q=0,r=5 with zero, one, or two local defects:          DETECTED;
q=0,r=5 with exactly three local defects:              DETECTED;
q=0,r=5 with four or five R/B defects:                 OPEN;
existence or exclusion of a witness in the cell:       OPEN;
fixed-root detector injectivity:                       UNKNOWN;
q=0,r>=6, q>=1, and unfactorized cells:                UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.         (30)
```

The four-/five-defect boundary is genuine for this argument.  With at least
four `B` modes, every five-mode pair tensor

```text
P_5(h_p,h_q,a,a,b)                                   (31)
```

vanishes for row-count reasons: the three rows `h_p,h_q,b` cannot cover four
modes on which `a` is zero.  This does not construct a witness and does not
show that the remaining cells survive other detectors; it only prevents an
unjustified extrapolation of the present two-open activity mechanism.

The lift, fixed layer, companion classification, three-activity theorem,
root-row full span, row-pair incidence theorem, and two-singleton obstruction
are imported at their existing scopes.  The `b=0` exclusion, exact `R/B`
collision intersections, inactive-set classification, and four
three-defect contradictions are proved here.  The theorem has not been
formalized in Lean.  Its preserved scope and adversarial reconstruction are
in the
[`2026-08-11 review record`](../../docs/audits/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_THREE_DEFECT_FIVE_CELL_REVIEW_2026-08-11.md).

## Replay

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_complete_three_defect_five_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_complete_three_defect_five_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_complete_three_defect_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_three_defect_five_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_complete_three_defect_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_three_defect_five_cell_detector.py
```

The primary verifier reconstructs symbolic collision matrices, determinant
minors, exact common-kernel bases, coordinate-singleton profiles, and every
inactive-set ledger.  The independent no-import audit uses a recursive
permanent and rational row reduction over equal, unequal, and opposite
regular ratios, plus a separate bitmask census.  These are bounded convention
and falsification checks.  The characteristic-zero result is the written
incidence, kernel, local-rank, and support proof above.
