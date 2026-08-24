# Maximum-root surplus-two zero-anchor rank-one pure-probe orientation and hafnian splicing boundary theorem

## Status and scope

**Exact characteristic-zero root-order-three continuation and exact natural-
splice no-go; the all-rank-one branch remains open.**  Work at an actual
hypothetical Krenn--Gu witness in the `GLS57` zero-anchor chart

```text
r=3,       A={a_0,a_1},
Bhat=Q disjoint-union Uhat,       |Bhat|=6,
omega=W_(a_0,a_1)=0,                                      (1)
```

and retain all `GLS57` hypotheses: every auxiliary joint probe map has rank
one and is torus-rigid.  Write its unique coordinate readout as

```text
X_t=x_t tensor e_(t,kappa(t))^*,
Y_t=y_t tensor e_(t,kappa(t))^*,                          (2)
```

and let `P_c={s_c,t_c}` be the exact `2+2+2` colour partition.  This note
proves the following.

1. For every `P_c`, at least one complete old-probe shore is coordinate-pure:

   ```text
   x_(s_c),x_(t_c) in K e_(a_0,c)^*
   or
   y_(s_c),y_(t_c) in K e_(a_1,c)^*.                    (3)
   ```

   The opposite shore has an exact projective anti-synchronization normal
   form.  Zero individual root edges are retained.  Every label nevertheless
   has a nonzero coordinate-pure edge to at least one old probe, and one old
   probe carries whole-shore purity for at least two colour pairs.
2. After any fully supported contraction of both old probes, the six-label
   tensor is exactly the one-edge hafnian first variation

   ```text
   F_Bhat(Theta,W)=sum_(D in binom(Bhat,2))
                    Theta_D tensor H_(Bhat-D)(W),         (4)
   ```

   and is a weighted ternary diagonal tensor with all three weights nonzero.
   Treating the contracted companion blocks `Theta_D` themselves as the
   edges of a new six-vertex graph cannot reconstruct (4): their complete
   hafnian is supported only on the nonconstant `2+2+2` word `kappa`.
3. The other natural tangent splice is also impossible.  There are no vertex
   weights `(a_t)` for which

   ```text
   Theta_(s,t)=(a_s+a_t)W_(s,t)                          (5)
   ```

   on all fifteen pairs.  Trace zero would make (4) vanish; nonzero trace
   would make the original internal array `W` an honest six-vertex
   three-colour witness, contradicting the accepted six-vertex theorem.

This is `GLS60`.  It supplies new pointwise raw pure-probe structure and
excludes the direct-companion and vertex-gauge splices.  It does **not**
classify non-gauge first variations, prove a legal six-vertex reconstruction,
produce a permanent restriction, prove complete-nuisance survival, normalize
a legal selector, synchronize promoted response rows, force pointwise
response activity, supply any named downstream receiver, treat the higher-
rank rigid branch, cover `r>=4`, or close the strategic node.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## Dependencies and provenance

The proof uses exactly these committed interfaces.

- [`GLS57`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ALL_RANK_ONE_RIGID_COLOUR_PAIRING_AND_PROMOTED_RESPONSE_SUPPLY_THEOREM.md)
  supplies (1)--(2), the exact partition `P_0,P_1,P_2`, the pure pair
  equations, and the complete first-variation target.
- [`GLS42`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_RESIDUAL_EXCESS_HAFNIAN_FIRST_VARIATION_AND_ACTIVE_VERTEX_GAUGE_BOUNDARY_THEOREM.md)
  supplies the named hafnian first-variation and vertex-gauge identities.
  Both identities are also reproved here in the specialized six-label form.
- The accepted [`six-vertex theorem`](../finite/n06/SIX_VERTEX_CERTIFICATE.md)
  excludes complex six-vertex graph matching tensors with three nonzero
  diagonal target colours.
- The [`P_6` equality-five theorem`](ARBITRARY_PERMANENT_P6_COTWO_EQUALITY_FIVE_FULL_EXTENSION_EXCLUSION_THEOREM.md)
  and [`P_6` spanning-tree boundary`](ARBITRARY_PERMANENT_P6_COTWO_SPANNING_TREE_RADICAL_AND_SIMULTANEOUS_FACTOR_COMPATIBILITY_BOUNDARY.md)
  fix the separate meaning and open status of a six-factor permanent
  restriction.

The new content is the rank-one two-shore orientation lemma, its exact
anti-synchronization normal form, the companion-graph support obstruction,
the application of the vertex-gauge identity to an actual fully supported
`GLS57` contraction, and the resulting receiver-interface correction.  No
external literature claim is used.

## 1. Pairwise pure-probe orientation

For `P_c={s,t}`, `GLS57` gives a nonzero `h_c` and

```text
h_c(x_s tensor y_t+x_t tensor y_s)
 =e_(a_0,c)^* tensor e_(a_1,c)^*.                       (6)
```

### Theorem 1 (pure-shore alternative)

For every colour `c`, (3) holds.  More precisely, in the first alternative
there are scalars `a,b`, not both zero, such that

```text
x_s=a e_(a_0,c)^*,        x_t=b e_(a_0,c)^*,
a y_t+b y_s=h_c^(-1)e_(a_1,c)^*,                        (7)
```

and, after quotienting the second probe space by its coordinate line, one
has for some quotient vector `r_c`

```text
bar y_s=a r_c,             bar y_t=-b r_c.              (8)
```

In the second alternative there are scalars `a,b`, not both zero, with

```text
y_s=a e_(a_1,c)^*,        y_t=b e_(a_1,c)^*,
b x_s+a x_t=h_c^(-1)e_(a_0,c)^*,
bar x_s=a r_c,             bar x_t=-b r_c.              (9)
```

The alternatives may overlap.

#### Proof

Put

```text
X=[x_s x_t],       Y=[y_s y_t],       J=[[0,1],[1,0]].  (10)
```

The left side of (6), without `h_c`, is `X J Y^T` and has rank one.  If both
`X` and `Y` had rank two, then `Y^T` would surject onto `K^2`, `J` would be
invertible, and `X` would inject `K^2` into the first probe space.  Their
product would have rank two, a contradiction.  Thus `rank X<=1` or
`rank Y<=1`.

If `rank X<=1`, its nonzero image contains the first factor of the nonzero
right side of (6), so `im X=K e_(a_0,c)^*`.  This gives the first line of
(7), with `(a,b)!=(0,0)`.  Substitution into (6) gives its second line.
Modulo `K e_(a_1,c)^*`, the latter says

```text
a bar y_t+b bar y_s=0.                                  (11)
```

The kernel of the nonzero row `(b,a)` is generated by `(a,-b)`, including
the boundaries `a=0` or `b=0`; hence (8).  The `rank Y<=1` case is the
transposed argument and gives (9). `square`

The same proof can be written denominator-free by retaining
`h_c(a y_t+b y_s)=e_(a_1,c)^*` and its transpose.  The displayed inverse is
only a consequence of the already proved `h_c!=0`; no divisor or rank-minor
fibre is removed.

### Corollary 1.1 (labelwise and two-colour raw purity)

Each label in `P_c` has a nonzero coordinate-pure edge to at least one old
probe.  After choosing one valid alternative in (3) for each colour, one of
the two probes is the pure shore for at least two colour pairs.

#### Proof

In the first alternative, if `a!=0` then the `a_0--s` edge is nonzero pure;
if `a=0`, then `b!=0` and (7) makes `y_s=h_c^(-1)b^(-1)e_(a_1,c)^*`, so the
other probe edge at `s` is nonzero pure.  The same argument with `a,b`
exchanged treats `t`; (9) is symmetric.  Finally, three chosen shores occupy
two probes, so one probe occurs at least twice. `square`

This is raw physical incidence structure.  It is not a legal target-pure
anchor or a complete-nuisance surviving selector.

## 2. The contracted tensor and the direct-companion no-go

Choose probe vectors `z_0,z_1` with all six coordinates nonzero.  For every
pair `D={s,t}`, put

```text
Theta_D^z=
 (x_s(z_0)y_t(z_1)+x_t(z_0)y_s(z_1))
 e_(s,kappa(s))^* tensor e_(t,kappa(t))^*.              (12)
```

Let `H_I(W)` be the principal physical matching tensor on `I`, with
`H_empty=1`, and define `F_Bhat^z` by (4).

### Theorem 2 (exact six-label first variation)

The probe contraction of the complete `GLS57` identity is

```text
F_Bhat^z
 =sum_(c=0)^2 z_(0,c)z_(1,c)
   tensor_(t in Bhat)e_(t,c)^*.                         (13)
```

Equivalently,

```text
F_Bhat^z=[u]H_Bhat(W+u Theta^z).                        (14)
```

All three weights in (13) are nonzero.

#### Proof

Contract the two open probe slots in the `GLS57` identity by `z_0,z_1`.
Each companion becomes exactly (12), and the target contracts to (13).

For (14), expand one perfect-matching monomial of `H_Bhat(W+uTheta^z)`.
Its coefficient of `u` is the sum in which exactly one matched edge uses
`Theta^z` and every other edge uses `W`.  Summing first over the selected
pair and then over the perfect matchings of its four-label complement gives
(4).  Full support of `z_0,z_1` makes every displayed target weight nonzero.
`square`

### Theorem 3 (direct-companion graph support obstruction)

If the fifteen tensors `Theta_D^z` are used as the edge blocks of a
six-vertex graph, then

```text
H_Bhat(Theta^z)
 in K tensor_(t in Bhat)e_(t,kappa(t))^*.               (15)
```

The word `kappa` has two entries of each colour and is nonconstant.  Hence
`H_Bhat(Theta^z)` has zero coefficient on every diagonal word and cannot
equal the nonzero weighted diagonal tensor (13).  Moreover, (15) is zero or
decomposable, so no invertible local changes of basis can repair the direct
companion construction: its one-versus-five flattening rank is at most one,
whereas the same flattening of (13) has rank three.

#### Proof

Every edge block `Theta_(s,t)^z` is supported only at the local cell
`(kappa(s),kappa(t))`.  A perfect matching uses every label exactly once, so
every one of its monomials is supported at the same global word `kappa`.
Summing proves (15).  Local invertible maps preserve flattening rank, and the
three nonzero diagonal summands in (13) occupy independent rows and columns
of the displayed flattening. `square`

The exact rational control used by both verifiers realizes the orientation
split, including a zero individual probe edge, and gives

```text
H_Bhat(Theta^z)=18 tensor_(t in Bhat)e_(t,kappa(t))^*.  (16)
```

It is a sharp local control for (15), not a physical Krenn--Gu witness or a
counterexample.

## 3. Vertex-gauge splicing is impossible

### Theorem 4 (actual-witness vertex-gauge exclusion)

At every fully supported probe contraction above, no scalars `(a_t)` satisfy
(5) for all pairs.

#### Proof

Suppose (5) holds and put `tau=sum_t a_t`.  In any perfect matching, the
sum of the marked-edge factors `a_s+a_t` is `tau`, because every vertex
occurs exactly once.  The matching expansion of (4) therefore gives the
specialized `GLS42` identity

```text
F_Bhat^z=tau H_Bhat(W).                                  (17)
```

If `tau=0`, (17) contradicts the three nonzero coefficients in (13).  If
`tau!=0`, then `H_Bhat(W)=tau^(-1)F_Bhat^z` is the matching tensor of an
honest six-vertex graph with three nonzero diagonal target colours.  Over a
subfield of `C`, an invertible diagonal change at any one vertex normalizes
the three nonzero target weights to one, so this contradicts the accepted
six-vertex theorem.

For an arbitrary characteristic-zero ground field, the finitely many edge,
probe, weight, and inverse coefficients generate a finitely generated field
over `Q`, which embeds into `C`.  The embedding preserves all polynomial
equalities and every declared nonzero value, so the same contradiction
applies. `square`

In particular `Theta^z` cannot be a common scalar multiple of `W`.  Theorem
4 excludes the tangent to vertex rescaling; it does not classify all
non-gauge arrays or all ways that both `W` and `Theta^z` might enter a new
graph construction.

## 4. Receiver-interface correction

Three objects must remain distinct.

1. The accepted six-vertex theorem takes six ternary vertex spaces and
   fifteen pair edge blocks `B_(s,t)` and excludes

   ```text
   H_Bhat(B)=weighted Delta_3.                            (18)
   ```

2. The tensor in (13) is the **first variation** `[u]H(W+uTheta)`.  It is not
   itself `H(Theta)` by Theorem 3, and Theorem 4 excludes the natural
   vertex-gauge identification with `H(W)`.
3. Repository notation `P_6` means the six-factor **permanent** tensor.  A
   pullback is specified by six labelled three-planes in `K^6` and has

   ```text
   P_6(u_(0,c_0),...,u_(5,c_5))
    =[x_0...x_5] product_(i=0)^5 u_(i,c_i).              (19)
   ```

   A weighted `P_6 -> Delta_3` restriction would enter the separate open
   permanent nodes `PR`, `PR6`, and `PRT`; it is not accepted or excluded by
   the six-vertex theorem.  The unrestricted `P_6` restriction problem is
   explicitly open on current main.

Earlier `GLS57` prose said that a weighted `P_6` restriction would be
"accepted by the committed six-vertex theorem."  That sentence conflated
(18) and (19).  This theorem corrects the interface without claiming that no
future, separately proved bridge between the two tensor families can exist.

## 5. Exact boundary

```text
field:                                                   CHARACTERISTIC ZERO;
root order:                                              r=3;
source chart:                                            GLS57 all-six-rigid/all-rank-one;
response/divisor fibres:                                 ALL retained;

pairwise pure old-probe shore:                           PROVED;
opposite-shore projective anti-synchronization:           PROVED;
labelwise nonzero pure probe edge:                        PROVED;
one probe pure on at least two colour-pair shores:        PROVED;

fully supported contracted tensor is hafnian variation:  PROVED;
direct companion array is a six-vertex reconstruction:   PROVED IMPOSSIBLE;
vertex-gauge splice to the internal graph:                PROVED IMPOSSIBLE;
weighted P6 accepted by the six-vertex theorem:           INTERFACE ERROR CORRECTED;

non-gauge six-vertex reconstruction:                      OPEN;
permanent P6 extraction or nonrestriction:                OPEN;
complete nuisance survival / legal selector:              OPEN;
response synchronization and selected activity:           OPEN;
named receiver and target-pure anchor:                     OPEN;
higher-rank rigid / unique-nonrigid coupling:              OPEN;
arbitrary-root and nonzero-anchor coverage:                OPEN;
strategic-node closure:                                    OPEN;
global Krenn--Gu conjecture:                               UNRESOLVED.       (20)
```

## Verification

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_one_pure_probe_orientation_and_hafnian_splicing_boundary.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_one_pure_probe_orientation_and_hafnian_splicing_boundary.py
```

The primary verifier checks all nine Cauchy--Binet minors symbolically, the
exact orientation normal forms and sharp alternatives, all `729` six-label
coefficients of the hafnian deformation identity, `1458` nonzero-trace and
trace-zero gauge coefficients, the `105=15+90` zero-anchor matching census,
the direct-companion support and coefficient `18`, and the `15`-hafnian
versus `720`-permanent monomial census.

The independent audit imports neither the primary verifier nor project code.
It exhausts all `816` admissible pure-target companion quadruples over `F_3`
and finds `384/384/48` points on the first-only/second-only/both orientation
cells, with `424` zero-edge boundary points.  It separately uses bit-mask
perfect matchings to compare the full contracted eight-vertex expansion with
the six-label first variation on all `729` words, rechecks the companion
support, derives the gauge identity by marked matching edges, and audits the
two tensor-type censuses.

The finite-field census and exact controls audit the algebra and its boundary;
the written rank and matching proofs carry the characteristic-zero theorem.
