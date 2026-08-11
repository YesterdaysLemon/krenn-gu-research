# Projectively constant lift: complete aligned five-cell two-open detector

## Status

**Complete conditional two-open detection in the aligned common-two-row,
projectively constant `q=0,r=5` cell.**  This is an exact conditional
characteristic-zero theorem.  Work in the tight cell

```text
q=0,                  r=5,                  |B|=5.    (1)
```

Then, for every local `a/b` rank pattern, every nonzero regular ratio, every
rank-two companion frame, and every persistent-root activity pattern, at
least one non-aligned root has a nonzero complete two-open detector.

Equivalently, the conditional aligned projective `q=0,r=5` cell has **no
collectively invisible point**.  The preceding theorem handles at most three
local defects.  This theorem closes all four- and five-defect cells by
combining:

- the lifted physical-row quota, which excludes four or more `b`-only modes;
- exact four-defect common collision kernels;
- an arbitrary-ratio cofactor graph for five regular defects;
- exact one- and two-`B` forcing;
- a three-`B` triangle kernel; and
- a four-row Hall bridge from the final complementary `3|2` line swap to the
  exact two-singleton `P_5` obstruction.

This is complete **detector** closure only.  It does not exclude a graph
witness, prove fixed-root injectivity, treat `q=0,r>=6` or `q>=1`, address an
unfactorized outside graph, or supply universal extraction/gluing.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Imported five-cell and incidence interfaces

Use the hypotheses and notation of the
[`complete three-defect theorem`](PROJECTIVELY_CONSTANT_LIFT_COMPLETE_THREE_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md).
The four non-aligned roots are

```text
P={1,2,3,4}.                                          (2)
```

Their fixed five-mode restriction is

```text
P_5(h_1,h_2,h_3,h_4,b)
 =sum_(c=0)^2 X_c e_c^(tensor B),
X_0 X_1 X_2!=0.                                      (3)
```

Every local flattening of (3) has rank three, and every persistent root row
family `h_p` has full cross-mode span.  Put

```text
S_w=span(a_w,b_w),
D={w in B:dim S_w<=1}.                                (4)
```

The preceding theorem proves

```text
b_w!=0                         at every outside mode. (5)
```

Thus every defect is exactly one of

```text
R: a_w=lambda_w b_w, lambda_w!=0;       B: a_w=0.    (6)
```

For `w in D`, define the retained collision operator, its kernel, and the
inactive roots by

```text
R_(p,w)=P_4(h_p,a,a,b;B-{w}),
K_w={h:R_(-,w)=0},
I_w={p in P:h_p in K_w}.                              (7)
```

If all four collective two-open coefficients vanish, the imported
three-activity theorem gives

```text
|I_w|>=2                         for every w in D.    (8)
```

Four permanent-incidence facts apply to (3).

1. Every source-row pair span contains a target coordinate covector at every
   mode, and every target colour occurs in at least two pair-span labels.
2. Every source-row triple span contains each target colour in at least three
   modes.
3. Every source-row four-set span contains each target colour in at least
   four modes.
4. If two target-coordinate pullbacks at one local map are supported on two
   distinct singleton source rows, the exact
   [`two-singleton obstruction`](../p5/coordinate-cegar/P5_TWO_SINGLETON_COORDINATE_OBSTRUCTION.md)
   excludes the restriction.

The first fact is the
[`five-mode row-pair incidence theorem`](ARBITRARY_PERMANENT_FIVE_MODE_ROW_PAIR_INCIDENCE_THEOREM.md);
the next two are the
[`kernel Hall hierarchy`](../p5/frontier/P5_KERNEL_HALL_HIERARCHY.md).
The Hall hierarchy and two-singleton obstruction are written over `C`.  Their
characteristic-zero use here follows by the descent already used in the
preceding theorem: all coefficients and required nonzero minors descend to a
finitely generated extension of `Q`, embed in `C`, and preserve the tensor
identity, zero supports, and nonzero ranks.  No algebraic-closure assumption
is made in the collision calculations below; the cube-root divisor in
Lemma 2 is retained whenever it exists in the working field.

Finally import the
[`lifted physical-row quota`](PROJECTIVELY_CONSTANT_LIFT_ROW_QUOTAS_AND_MINIMAL_CELL_TWO_OPEN_DETECTOR_THEOREM.md).
At `q=0` it says

```text
p_a=#{w in B:a_w!=0}>=2.                              (9)
```

By (5)--(6), (9) gives the decisive bound

```text
#{B-type defects}<=3.                                (10)
```

Thus the structural four-`B` zero of the preceding detector theorem cannot
occur inside the complete lifted diagonal identity.

## 2. Exact retained collision facts

Normalize `b_w` to the first local basis vector at a defect.  At a regular
defect write `a_w=lambda_w b_w`; at a transverse mode use a local
`a_w,b_w` basis.  The labelled expansion is

```text
P_4(h,a,a,b)
 =2 sum_(i!=j) h_i tensor b_j tensor
    (tensor_(k notin {i,j}) a_k).                    (11)
```

We use four consequences of (11).

### Lemma 1 (the three-`B` triangle)

Let `u,v,w` be three `B` modes and let `x,y` be the other two outside modes.
Both `a_x,a_y` are nonzero.  After deleting `u`, (11) factors as

```text
R_(p,u)
 =2 a_x tensor a_y tensor
   (h_(p,v) tensor b_w+b_v tensor h_(p,w)),           (12)
```

up to the fixed mode order.  Therefore

```text
h in K_u
iff h_v=-gamma b_v, h_w=gamma b_w
    for some gamma;                                  (13)
```

the values at `u,x,y` are free.  For distinct `B` modes, a pair intersection
puts the row on the `b` line at all three `B` modes.  The triple intersection
is exactly

```text
h_u=h_v=h_w=0,             h_x,h_y arbitrary.        (14)
```

The last implication uses characteristic zero: the three pair relations give
`alpha_u+alpha_v=alpha_u+alpha_w=alpha_v+alpha_w=0`.

### Lemma 2 (four-defect full common kernels)

Let `t` be the unique transverse mode.  The full intersections of all four
defect-deletion kernels are as follows.

1. For `RRRRT`, put `mu_i=1/lambda_i`.  The intersection always has
   dimension at most one.  It is nonzero exactly in either of the following
   two cases:

   ```text
   mu_0=mu_1=mu_2=mu_3=a;                            (15a)
   (mu_0,mu_1,mu_2,mu_3)=(a,a,d,d) up to relabelling,
       a!=d,                 a^2+ad+d^2=0.           (15b)
   ```

   Thus (15b) is the primitive-cube-root divisor over an algebraic closure;
   it is absent over the rationals but cannot be omitted in characteristic
   zero.  In either nonzero case the kernel is generated by

   ```text
   (-b_0,-b_1,-b_2,-b_3,2c a_t+b_t),                (15c)
   ```

   where `c=a` in (15a) and `c=a+d` in (15b).  In particular,
   (15c) becomes `(-b_0,-b_1,-b_2,-b_3,(2/L)a_t+b_t)` when all
   `lambda_i=L`.

2. For `RRRBT`, with regular ratios `lambda_0,lambda_1,lambda_2`, the
   intersection is zero unless

   ```text
   lambda_0+lambda_1+lambda_2=0.                     (16)
   ```

   Under (16) it is one-dimensional.  A nonzero generator has regular
   blocks

   ```text
   h_i=lambda_i(lambda_i-lambda_j)(lambda_i-lambda_k)b_i,
   {i,j,k}={0,1,2},                                  (17)
   ```

   `B` block and transverse block

   ```text
   h_B=-3 lambda_0 lambda_1 lambda_2 b_B,
   h_t=-2 sum_i lambda_i^2 a_t
       +3 lambda_0 lambda_1 lambda_2 b_t.             (18)
   ```

3. For `RRBBT`, with regular ratios `L,M`, the intersection is the exact
   two-dimensional family

   ```text
   h_R0=-(L/M)alpha b_R0-L beta b_R0,
   h_R1=alpha b_R1,
   h_B0=h_B1=0,
   h_t=beta a_t.                                     (19)
   ```

### Lemma 3 (five-regular cofactor graph)

Suppose all five defects are regular.  For distinct modes `u,v` put

```text
q_uv=e_2(lambda_w:w in B-{u,v}).                     (20)
```

If `h in K_u` and `q_uv!=0`, then

```text
h_v in <b_v>.                                        (21)
```

Indeed, the component of (11) with `h_v` off the `b_v` line is `2q_uv`
times a nonzero product of the other local `b` rows.  Put

```text
mu_i=1/lambda_i,             S=sum_i mu_i.            (22)
```

Since the ratios are nonzero,

```text
q_uv=0        iff        mu_u+mu_v=S.                 (23)
```

Let `F` be the forcing graph with edge `uv` when `q_uv!=0`, and let `H` join
two deletion indices when they have a common neighbour in `F`.

The graph `F` has no isolated vertex.  Moreover, if `H` is disconnected,
then, up to relabelling and common scaling of the `mu` values, exactly one of
the following occurs:

```text
four-plus-one: mu=(a,a,a,a,-2a),   Z=K_4;
two-plus-three: mu=(-2a,-2a,a,a,a), Z=K_(2,3),        (24)
```

where `Z` is the zero graph complementary to `F`.

### Lemma 4 (one- and two-`B` five-defect forcing)

For `RRRRB`, every regular-deletion kernel forces the row onto the `b` line
at every retained regular mode.  Write

```text
tau_u=e_2(lambda_v:v regular, v!=u).                 (25)
```

At least one `tau_u` is nonzero.  For such `u`, `K_u` also forces the retained
`B` value onto its `b` line, while `K_B` forces the value at regular mode `u`
onto its `b` line.

For `RRRBB`, let

```text
sigma=e_2(lambda_0,lambda_1,lambda_2).                (26)
```

Every regular-deletion kernel forces both retained `B` values onto their
`b` lines, and every `B`-deletion kernel forces every regular value onto its
`b` line.  A `B`-deletion kernel forces the other `B` value onto its `b` line
exactly when `sigma!=0`.

### Proof of Lemmas 1--4

Lemma 1 is the displayed factorization.  We give the arbitrary-ratio
reduction for Lemma 2 explicitly, because its exceptional divisors are
load-bearing.

For `RRRRT`, write

```text
h_i=alpha_i b_i,       h_t=A a_t+B b_t+C c_t,
x_i=alpha_i/lambda_i,  mu_i=1/lambda_i,              (19a)
```

where `c_t` completes `a_t,b_t` to a local basis.  The off-line retained
coordinates first force this form.  For every deleted regular index `u`,
the `b_t`, `a_t`, and `c_t` coefficients of (11), after division only by
the nonzero product of the three retained ratios, are

```text
X_u+B M_u=0,
X_u M_u-Y_u+A M_u=0,
C M_u=0,                                             (19b)
```

where

```text
X_u=sum_(i!=u)x_i,  M_u=sum_(i!=u)mu_i,
Y_u=sum_(i!=u)x_i mu_i.                              (19c)
```

The first family and characteristic zero give `x_i=-B mu_i` for all `i`.
If `B=0`, then all `x_i,A,C` vanish because the four `M_u` cannot all be
zero.  Hence a nonzero kernel vector has `B!=0`, `C=0`, and, with
`c=A/(2B)`,

```text
e_2(mu_i:i!=u)=c M_u                     for every u. (19d)
```

Subtracting the equations for `u` and `v` gives

```text
(mu_v-mu_u)(sum_(k notin {u,v})mu_k-c)=0.            (19e)
```

If all four reciprocals are distinct, apply (19e) to `(0,1)` and `(0,2)`:
the two complementary sums force `mu_1=mu_2`.  If exactly three values occur,
write the multiset as `(a,a,d,e)`; the pairs `(a,d)` and `(a,e)` force
`a+e=a+d`, hence `d=e`.  Thus at least three distinct values are impossible.
A `3+1` two-value split
would give both `c=2a` from (19e) and `c=a` from the three-equal deletion.
Thus only `4` or `2+2` multiplicities remain.  The all-equal case gives
`c=a`.  For `(a,a,d,d)`, (19d) is equivalent to

```text
(a-d)(a^2+ad+d^2)=0,                                 (19f)
```

and the distinct-value branch is exactly (15b), with `c=a+d`.  Substitution
gives (15c).  This proves both the complete divisor classification and the
uniform one-dimensional bound.  In particular, the tempting stronger claim
that only equal regular ratios survive is false on the cube-root divisor
(15b).

For `RRRBT`, write the three regular components as `alpha_i b_i`, the
`B` component as `delta b_B`, and the transverse component as above.
The three regular deletions give

```text
delta=-B,       C=0,
alpha_i/lambda_i-B/lambda_i=kappa,
A=-2 kappa.                                           (19g)
```

The `B` deletion then gives

```text
3 kappa+2B sum_i(1/lambda_i)=0,
2B(lambda_0+lambda_1+lambda_2)=0.                    (19h)
```

A nonzero vector has `B!=0`, so (16) is necessary.  Solving (19g)--(19h)
under (16) yields (17)--(18), with no difference or symmetric polynomial
silently divided away.  Direct substitution proves sufficiency and the
one-dimensionality.

For `RRBBT`, the same labelled equations force both `B` components to zero
and leave two free scalars.  Solving without division except by the nonzero
regular ratios `L,M` gives exactly (19).  Direct substitution and a rank-13
minor prove that the family is neither smaller nor larger.

For Lemma 3, the off-line component at `v` has coefficient (20).  Multiplying
`q_uv` by the three nonzero reciprocals on the complementary modes gives
`S-mu_u-mu_v`, proving (23).  Zero neighbours of a fixed `mu` value all have
the complementary value `S-mu`; hence the zero graph is a disjoint union of
complete bipartite complementary-value components and possible cliques on
the value `S/2`.  A direct five-vertex component check shows that the
common-neighbour graph can disconnect only for `K_4` or `K_(2,3)`.  Summing
the five `mu` values then gives the two ratios in (24).  A forcing-isolated
vertex would require the other four `mu` values all to equal `S-mu_u`; the
sum equation makes that common value zero, impossible.

For Lemma 4, deleting a regular mode in `RRRRB` leaves three regular modes
and one `B` mode.  Assigning `b` to the `B` mode leaves a nonzero product of
two regular ratios for every retained regular off-line component.  The
coefficient at the retained `B` mode is `tau_u`.  If all four `tau_u`
vanished, the regular reciprocals would satisfy

```text
sum_v mu_v-mu_u=0                    for every u,
```

forcing every `mu_u` and their sum to be zero.  The `RRRBB` statements follow
similarly: two zero `a` rows force `h,b` onto the two `B` modes, while after
one `B` deletion the remaining `B` coefficient is exactly (26).

The primary verifier reconstructs every matrix, special kernel, cofactor
graph, and exceptional graph type.  The independent audit instead uses a
recursive permanent, rational row reduction, an exact implementation of
`Q(omega)` with `omega^2+omega+1=0`, and a separate value-graph census.  The
arbitrary-ratio claims are the labelled coefficient proof above.

## 3. The final fixed-layer bridge

### Lemma 5 (complementary `3|2` line swap is impossible)

Suppose the four roots split into two pairs

```text
P=J disjoint-union K,                                 (27)
```

and the five modes split into `U disjoint-union V`, with

```text
|U|=3,                 |V|=2,                        (28)
```

such that

```text
b and both J rows lie on one line at every u in U;
b and both K rows lie on one line at every v in V.   (29)
```

Then (3) is impossible.

### Proof

At every mode, row-pair incidence applied to `b` and either row on its local
line makes that line a target coordinate line.  Fix `u in U`, call its colour
`beta_u`, and write `K={k_1,k_2}`.  Local rank three says that each `k_i` is
off the `beta_u` line and that the two quotient directions are independent.

For each `i`, apply the four-row Hall quota to

```text
Q_i={b} union J union {k_i}.                          (30)
```

At each mode of `U`, its span is a plane and contains at most two target
coordinates.  At each mode of `V`, the rows `b` and `J` already span the full
three-dimensional local space, so `Q_i` contains all three coordinates.
Thus the total coordinate-incidence capacity is

```text
3*2+2*3=12.                                          (31)
```

Four-row Hall requires four incidences for each of three colours, also
twelve.  Equality holds everywhere.  In particular

```text
span(b_u,k_(1,u)),       span(b_u,k_(2,u))            (32)
```

are coordinate planes.  They are distinct, because otherwise
`b_u,k_(1,u),k_(2,u)` would span at most a plane.  Hence they are the two
coordinate planes through the `beta_u` axis.

The two target colours other than `beta_u` are therefore supported at mode
`u` on the two distinct singleton source rows `k_1,k_2`: the three rows
`b,J` have only `beta_u` components, and each of the two remaining rows lies
in a different coordinate plane through that axis.  This is exactly the
two-singleton coordinate obstruction.  Contradiction.

## 4. Four defects always detect

Assume `|D|=4` and collective invisibility.  By (10), the possible type words,
up to permutation, are

```text
RRRRT,                 RRRBT,                 RRBBT,                 RBBBT.
                                                               (33)
```

### Theorem 6 (four-defect detector)

Every word in (33) has some nonzero collective detector.

### Proof

First suppose there are at most two `B` modes.

For `RRRRT` or `RRRBT`, every deletion kernel puts a row on the `b` line at
every other defect.  Fix a defect `v`.  All roots in

```text
union_(u in D-{v}) I_u                               (34)
```

therefore lie with `b_v` on one line.  If that union contained three roots,
the fifth fixed source row could raise the local span only to two.  Hence the
union has size at most two.  The three sets in (34) each have size at least
two by (8), so they are one common pair.  Varying `v` shows

```text
I_u=J,                         |J|=2,                 (35)
```

for all four defects.

For `RRBBT`, apply the same argument at either `B` defect.  Every other
deletion kernel forces its retained value there onto the `b` line, so the
three other inactive sets are one pair.  Comparing the two `B` modes again
gives (35).

The two root row families in `J` now lie in the appropriate full common
kernel of Lemma 2.  In `RRRRT` and `RRRBT` that kernel has dimension at most
one.  The two nonzero root families are proportional, so their local pair
span has capacity at most one coordinate at each of five modes, below the
pair-Hall requirement of six total colour incidences.  In `RRBBT`, (19)
makes both root rows zero at both `B` modes, contradicting the nonempty
row-pair incidence required at every mode.

It remains `RBBBT`.  Use only the three `B` inactive sets.  Lemma 1 and local
rank show that each has size exactly two.  A root cannot lie in all three,
because (14) would support its row family at only the two non-`B` modes.
The membership degrees are therefore

```text
(2,2,1,1)                 or                 (2,2,2,0).    (36)
```

In the second pattern, the three degree-two roots belong to pair
intersections and lie with `b` on one line at every `B` mode, leaving local
rank at most two.  In the first pattern, local rank at a chosen `B` mode
requires both singleton-degree roots to have their sole membership there;
the same cannot hold at either other `B` mode.  This is the exact `BBB`
triangle argument from the preceding theorem.  All four words detect.

## 5. Five defects always detect

Assume `|D|=5` and collective invisibility.  Bound (10) leaves

```text
RRRRR,                 RRRRB,                 RRRBB,                 RRBBB.
                                                               (37)
```

The three-`B` word `RRBBB` is excluded by the last paragraph of Theorem 6,
with the two non-`B` modes now both regular.  We treat the other three words.

### Theorem 7 (`RRRRB` detector)

The `RRRRB` cell has some nonzero collective detector.

### Proof

At a regular mode, the three inactive sets belonging to the other regular
deletions are forced onto its `b` line.  Local rank and (8) make those sets a
common pair; varying the regular mode gives

```text
I_u=J                         for all regular u.      (38)
```

Choose `u` with `tau_u!=0` from Lemma 4.  At regular mode `u`, both `J`
(using another regular deletion) and `I_B` (using the `B` deletion) lie on
the `b_u` line.  Local rank forces `I_B=J`.  At the `B` mode, `K_u` and
`tau_u!=0` put the two `J` roots on its `b` line as well.  Thus the two roots
in `J` have local pair spans of dimension at most one at all five modes,
contradicting the six pair-incidence quota.

### Theorem 8 (`RRRBB` detector)

The `RRRBB` cell has some nonzero collective detector.

### Proof

At every regular mode the two `B` inactive sets are forced onto the local
`b` line, so they are one pair `J`.  At either `B` mode all three regular
inactive sets are forced onto the local `b` line, so they are one pair `K`:

```text
I_B0=I_B1=J,             I_R0=I_R1=I_R2=K.           (39)
```

If `sigma!=0`, Lemma 4 forces both pairs onto the same line at a `B` mode;
local rank gives `J=K`.  The common pair is then on the `b` line at every
mode, contradicting pair incidence.

Suppose `sigma=0`.  If `J=K`, the same pair-incidence contradiction applies.
If the pairs form a diamond, apply triple Hall to `{b} union J`.  Its span is
a line at all three regular modes and at most a plane at both `B` modes, for
total incidence capacity

```text
3*1+2*2=7<9.                                         (40)
```

Thus a diamond is impossible.  The only remaining alternative is

```text
P=J disjoint-union K.                                 (41)
```

At the three regular modes `b,J` lie on one line; at the two `B` modes
`b,K` lie on one line.  Lemma 5 excludes exactly this complementary `3|2`
line swap.

### Theorem 9 (`RRRRR` detector)

The all-regular five-defect cell has some nonzero collective detector.

### Proof

Use the forcing graph `F` and equality graph `H` of Lemma 3.  At a mode `v`,
all roots in

```text
union_(u neighbour v in F) I_u                       (42)
```

lie on the `b_v` line by (21).  Local rank makes this union a set of size at
most two.  Since `F` has no isolated vertex, (8) makes every `I_u` an exact
pair.  Deletion indices joined in `H` therefore have equal inactive pairs.

If `H` is connected, all five inactive sets equal one pair `J`.  Every mode
has a forcing neighbour, so both `J` rows lie on the local `b` line at all
five modes.  Pair incidence is impossible.

Suppose `H` is disconnected.  In the four-plus-one case of (24), let `A` be
the four-vertex zero clique and `s` the remaining vertex.  The four inactive
sets indexed by `A` equal one pair `J`; write `K=I_s`.  At all four `A` modes
the rows in `K` lie with `b` on one line.  The triple `{b} union K` has
incidence capacity at most

```text
4*1+1*3=7<9,                                         (43)
```

contradicting triple Hall.

In the two-plus-three case, let `A={a_0,a_1}` and let `C` be the three-vertex
part.  The three inactive sets indexed by `C` equal one pair `J`; put
`K_i=I_(a_i)`.  At the three `C` modes, `{b} union J` spans a line.  At mode
`a_0` its span has dimension one, two, or three according as `J` equals,
overlaps, or is disjoint from `K_1`; the analogous statement holds with
`a_0,a_1` exchanged.  Triple Hall requires total capacity at least nine, but

```text
3*1+3+3=9.                                           (44)
```

Equality is possible only if `J` is disjoint from both `K_0,K_1`.  Hence

```text
K_0=K_1=P-J,                                         (45)
```

and the three `C` modes versus the two `A` modes form the complementary
`3|2` line swap of Lemma 5.  This final possibility is impossible.

Theorems 7--9 and the three-`B` argument close every word in (37).

## 6. Complete aligned five-cell boundary

Combine Theorems 6--9 with the preceding detector sequence:

```text
q=0,r=5 with no local defects:                         DETECTED;
q=0,r=5 with one, two, or three local defects:         DETECTED;
q=0,r=5 with four local defects:                       DETECTED;
q=0,r=5 with five local defects:                       DETECTED;
complete aligned projective q=0,r=5 cell:              DETECTED;
existence or exclusion of a witness in that cell:      OPEN;
fixed-root detector injectivity:                       UNKNOWN;
q=0,r>=6, q>=1, and unfactorized cells:                UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.         (46)
```

The lifted row quota, fixed `P_5` layer, root-row full span,
three-activity theorem, pair/triple/four-row incidence quotas, and
two-singleton obstruction are imported at their existing scopes.  The new
content is the four-/five-defect collision classification, reciprocal
cofactor graph, exceptional-ratio reduction, and complementary line-swap
bridge.  No finite search proves the arbitrary-ratio theorem.

This result removes the aligned `q=0,r=5` local detector leaf from the live
frontier.  It does not connect a nonzero detector to global witness
nonexistence and does not transport to larger cells or an unfactorized
outside graph.  The theorem has not been formalized in Lean.  Its preserved
scope and adversarial reconstruction are in the
[`2026-08-11 review record`](../../docs/audits/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_ALIGNED_FIVE_CELL_REVIEW_2026-08-11.md).

## Replay

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_complete_aligned_five_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_complete_aligned_five_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_complete_aligned_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_aligned_five_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_complete_aligned_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_aligned_five_cell_detector.py
```

The primary verifier reconstructs the symbolic collision matrices, special
four-defect kernels (including the cube-root divisor), five-regular cofactors,
exceptional graph types, inactive-set ledgers, and Hall capacities.  The
independent no-import audit uses a recursive permanent, rational elimination
over independent ratio grids, its own exact `Q(omega)` arithmetic, a
separately derived reciprocal graph census, and bitmask Hall ledgers.  These
are bounded convention and falsification checks.  The characteristic-zero
result is the written coefficient, incidence, and support proof above.
