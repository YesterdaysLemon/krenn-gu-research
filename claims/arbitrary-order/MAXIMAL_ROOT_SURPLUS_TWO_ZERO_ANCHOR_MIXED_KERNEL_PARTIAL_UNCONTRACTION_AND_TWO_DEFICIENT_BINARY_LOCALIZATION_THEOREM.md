# Maximum-root surplus-two zero-anchor mixed-kernel partial uncontraction and two-deficient binary localization

## Status and scope

**Exact characteristic-zero same-source hierarchy, parent attempt, and
root-order-three two-deficient localization (`GLS63`).**  Return to the
complete zero-anchor tensor before contracting the auxiliary labels.  Any
deficient label may now be contracted at an independent generic vector in
its whole joint kernel, while any injective nonaxis label may be contracted
at its cross product.  Leaving every pure-probe-axis label open gives one
compatible hierarchy in which a physical pair is structurally retained
exactly when both of its endpoints remain open.

For an arbitrary deficient set, row-space and active-line quotients give
exact common-support incidence constraints.  If a target colour is visible
on every deficient kernel, at least three distinct injective nonaxis labels
must have that identically zero cross-product coordinate.

When exactly two labels are deficient, these constraints, a new
deficient/nonaxis singleton classification, and a two-dimensional
pure-companion lemma exclude every profile except one sharply localized
family:

```text
both deficient maps have rank two and the same kernel K e_c;
there are no injective pure-probe-axis labels;
all four remaining labels are injective and nonaxis;
at least three have zero cross-product coordinate c;
none has zero cross-product coordinate d or e;
the deficient-pair companion is nonzero binary diagonal on {d,e}. (1)
```

The higher-open equations do **not** presently exclude (1).  Exact
fibre-level three-port and four-port mixed-orientation controls show that the
off-colour parts of the nonaxis pair companions can cancel through decks
belonging to one common physical source table at the displayed fibres.  The
remaining obligation is a
function-field restriction-separation theorem coupling those higher-open
decks to the nonzero binary deficient-pair contraction.

This is a serious parent-theorem attempt and an exact localization, not
source integrability, synchronization, attachment, a branch closure, or a
global proof.  Profiles with exactly two deficient labels remain open on
(1); profiles with three or more deficient labels, the unique-nonrigid
branch, nonzero anchor, and every downstream gate remain open.  The global
Krenn--Gu status remains **UNRESOLVED**.

## Parent-theorem checkpoint

The parent proposition attacked here is:

> Every complete zero-anchor, root-order-three, all-six-rigid hypothetical
> witness with at least two deficient auxiliary joint maps is incompatible
> with the three-colour GHZ target.

Its quantifiers retain one actual physical graph, all complete mixed target
equations, every deficient kernel vector, and all cross-product choices.
`GLS58` supplies the one- and two-kernel physical contractions; `GLS61` and
`GLS62` supply the compatible open-set and quotient mechanisms.  The
intended consumers are an exhaustive source exclusion or an honest
lower-order GHZ/permanent restriction, followed separately by response,
selector, synchronization, nuisance-survival, activity, and anchor gates.

The attempt below synthesizes those mechanisms across the whole deficient
set, tests the exact rank-one, rank-two support-one, rank-two support-two,
pure-axis, zero-cross-product, and mixed-orientation controls, and reaches
the precise residual (1).  The three- and four-port controls in Section 9
are exact no-go examples for the proposed termwise-separation route.  Thus a
further local refinement is load-bearing only if it proves the final
restriction-separation statement in Section 10 or supplies a different
reusable implication edge.

## Dependencies and provenance

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  owns the complete promoted two-probe physical identity.
- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md)
  owns the zero-anchor branch.
- [`GLS55`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TORUS_KERNEL_CONTRACTION_AND_FIVE_RIGID_LABEL_FLOOR_THEOREM.md)
  owns torus rigidity and the rigid deficient-rank classification.
- [`GLS58`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ALL_RIGID_KERNEL_CONTRACTION_AND_CROSS_PRODUCT_REDUCTION_THEOREM.md)
  owns the arbitrary deficient-kernel contraction and the shared-edge
  polarization
  `D_uv=hW_uv+a_u tensor b_v+b_u tensor a_v`.
- [`GLS61`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_CROSS_PRODUCT_PARTIAL_UNCONTRACTION_AND_INJECTIVE_NONAXIS_EXCLUSION_THEOREM.md)
  owns the cross-product partial-uncontraction hierarchy and the injective
  nonaxis orientation obstruction.
- [`GLS62`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_EXACTLY_ONE_DEFICIENT_ROW_QUOTIENT_EXCLUSION_THEOREM.md)
  owns the exactly-one-deficient exclusion and its row/active-line quotient
  mechanism.

No complementary deck below is introduced as an independent tensor.  Every
one is an evaluation or quotient of the original physical `H`-tensor from
the same graph.

## 1. The mixed-kernel same-source hierarchy

Let `Bhat` be the six auxiliary labels at root order three.  Put

```text
p_t=X_t(z_0,-),       q_t=Y_t(z_1,-),
k_t=p_t cross q_t.                                      (2)
```

Let `N` be the set of deficient labels, `P` the injective pure-probe-axis
labels, and `U` the injective nonaxis labels.  Thus

```text
Bhat=N disjoint-union P disjoint-union U.              (3)
```

Choose arbitrary contraction sets

```text
R subseteq N,          C subseteq U,                   (4)
```

and, independently for every `n in R`, let `x_n` be the generic vector of
`K_n=ker J_n`.  Put

```text
S=Bhat-(R union C).                                     (5)
```

Every pure axis lies in `S`.  Contract `n in R` at `x_n`, contract `u in C`
at `k_u`, and leave every label of `S` open.

### Theorem 1 (mixed-kernel partial uncontraction)

For every choice (4),

```text
sum_(D in binom(S,2))
  g_D(z_0,z_1)
    tensor H_(Bhat-D)(x_R,k_C,-_(S-D))

 =sum_(a=0)^2 mu_a z_(0,a)z_(1,a)
      product_(n in R)(x_n)_a
      product_(u in C)(k_u)_a
      tensor_(s in S)e_(s,a)^*.                       (6)
```

This is an identity over the polynomial ring in the probe variables and
independent kernel coordinates.

### Proof

Apply the declared partial evaluation to the complete `GLS8` zero-anchor
identity.  If a physical pair meets a contracted deficient label `n`, its
companion contains `p_n(x_n)` or `q_n(x_n)`, both zero because `x_n in K_n`.
If it meets a contracted nonaxis label `u`, its companion contains
`p_u(k_u)` or `q_u(k_u)`, both zero by the cross-product identities.  A pair
with both endpoints in `S` is not killed by this argument and retains its
actual complementary physical deck.  Thus the structurally retained pair
set is exactly `binom(S,2)`; a retained term may still evaluate to zero.
The target evaluation is the right side of (6). `square`

Equation (6) includes `GLS61` when every contracted label uses its cross
product and includes the `GLS58` kernel contractions when deficient labels
are contracted.  It is one hierarchy on one graph, not an atlas assembled
from separately selected local restrictions.

## 2. Kernel supports and quotient notation

For `n in N`, define

```text
A_n={a : e_(n,a)^*|_(K_n) !=0}.                       (7)
```

Torus rigidity gives

```text
rank J_n=1: A_n is a two-colour set;
rank J_n=2: A_n is the one- or two-colour support
            of its kernel line.                       (8)
```

Rank zero is not rigid.  For each colour put

```text
E_a={u in U : (k_u)_a is the zero polynomial}.        (9)
```

The three `E_a` are pairwise disjoint by the `GLS61` injective nonaxis
classification.

Over the fraction field `F`, let

```text
rho_n: V_n^* tensor F -> (V_n^* tensor F)/(row J_n),
pi_p:  V_p^* tensor F -> (V_p^* tensor F)/(F a_p),    (10)
```

where `a_p` is the active full-row covector at a pure axis.  Then

```text
rho_n(e_(n,a)^*)!=0 iff a in A_n,
pi_p(e_(p,a)^*)!=0 for every a.                       (11)
```

Every pair companion meeting a `rho_n`-quotiented deficient slot or a
`pi_p`-quotiented pure slot is killed in that companion factor.

## 3. General deficient-set incidence

For `T subseteq N`, write

```text
A_T=intersection_(t in T) A_t.                        (12)
```

### Lemma 2 (one-unquotiented incidence)

For every `n in N`,

```text
a in A_(N-{n})  implies  E_a!=empty.                  (13)
```

### Proof

In (6), leave `N union P` open and cross-contract every member of `U`.
Quotient every deficient slot except `n`, quotient every pure slot, and
leave `n` unquotiented.  Every source pair is killed: a pair not meeting a
pure slot has at least one endpoint among the quotiented deficient labels,
unless both endpoints equal the single label `n`, which is impossible.

If `a in A_(N-{n})` and `E_a` were empty, its target coefficient and every
quotiented factor would be nonzero.  The untouched coordinate at `n`
separates colour `a` from every other target colour.  Contradiction. `square`

For exactly two deficient labels `n,m`, (13) gives

```text
A_n union A_m subseteq {a:E_a!=empty}.                (14)
```

### Lemma 3 (common-support three-zero floor)

For every colour visible on every deficient kernel,

```text
a in A_N  implies  |E_a|>=3.                          (15)
```

### Proof

First suppose `U` is nonempty.  If `|E_a|<=1`, choose `u in U` with
`E_a subseteq {u}`.  Leave `N union P union {u}` open and quotient all
deficient and pure slots.  The only open nonaxis label is `u`, so every
source pair is killed.  The `u`-coordinate isolates the nonzero colour-`a`
target, a contradiction.  Hence `|E_a|>=2`.

If `E_a={u,v}`, leave `N union P union {u,v}` open and use the same
quotients.  The only possible source term is

```text
g_(uv) tensor Hbar_(uv).                              (16)
```

Every target colour outside `A_N` is killed by some deficient quotient.
Every other colour in `A_N` has at least two disjoint zero labels, all
contracted outside `{u,v}`.  Thus the target in (16) is one nonzero pure
colour-`a` tensor.  The equality forces `Hbar_(uv)!=0`; applying a functional
nonzero on that actual deck forces `g_(uv)` to be pure at `(a,a)`.  This
contradicts the four `GLS61` nonaxis orientation pairs.

If `U` is empty, Lemma 2 already contradicts any member of `A_N`; the same
conclusion is vacuous.  Thus (15) holds in every case. `square`

Consequently

```text
3|A_N|<=|U|<=6-|N|.                                   (17)
```

In particular `|A_N|<=1` whenever `|N|>=2`, and `A_N` is empty whenever
`|N|>=4`.

## 4. Singleton deficient/nonaxis synchronization

### Lemma 4 (singleton geometry)

Assume `|N|>=2`.  Fix `n in N` and a colour

```text
a in A_(N-{n}),       E_a={u}.                        (18)
```

Then `J_n` has rank one, its sole row is the coordinate readout `a`, and

```text
A_n={0,1,2}-{a}.                                      (19)
```

More precisely, if `u` has the `X`-orientation at `a`, then

```text
X_n=0,       row Y_n=K e_a^*,                         (20)
```

and the `Y`-orientation is symmetric.

### Proof

Leave `N union P union {u}` open.  Quotient every deficient slot except
`n`, quotient every pure slot, and leave `n,u` unquotiented.  Every pair is
killed except possibly `{n,u}`.  By Lemma 2 and disjointness, every target
colour other than `a` is killed by a quotient or by a contracted nonaxis
zero.  Hence the actual equality forces `g_(nu)` to be nonzero and pure at
`(a,a)`.

If `u` has the `X`-orientation, project its factor off the `a`-axis.  The
opposite shore has nonzero complementary projection, so purity forces
`p_n=0`, hence `X_n=0`.  The companion becomes `q_n tensor p_u`; its purity
and nonvanishing force `row Y_n=K e_a^*`.  The other orientation is
symmetric. `square`

This lemma is a synchronization statement, not automatically a
contradiction.  It becomes contradictory when `n` was assumed rank two or
when the singleton colour also lies in `A_n`.

## 5. Exact two-deficient support classification

Assume from now on

```text
N={n,m}.                                               (21)
```

By (14), every colour in `A_n union A_m` has a nonempty `E`-set.  A colour
in the intersection needs at least three zero labels by Lemma 3.  A
singleton `E_a` belonging to `A_m` forces `n` to be rank one with
`A_n={0,1,2}-{a}`, and symmetrically.

### Lemma 5 (two-support census)

Exactly one of the following can remain after Lemmas 2--4:

1. **same singleton:**

   ```text
   A_n=A_m={c},       |E_c|>=3,       |P|<=1;          (22)
   ```

2. **distinct singletons:**

   ```text
   A_n={c}, A_m={d}, c!=d,
   P=empty, |E_c|=|E_d|=2, E_e=empty.                 (23)
   ```

In both cases `n,m` have rank two and pure-coordinate kernel lines.  No
rank-one or rank-two support-two deficient map survives.

### Proof

If one support, say `A_n`, has two colours, its two disjoint `E`-sets are
nonempty.  At most one can be a singleton, because Lemma 4 would assign two
different sole readouts to `m`; the other has size at least two.  Comparing
with the nonempty colours in `A_m`, and using the three-zero bound on every
intersection colour, gives at least five required nonaxis labels in every
possible one/two, two/one, or two/two support arrangement.  But `|U|<=4`.

Thus both supports are singletons and both maps are rank two.  If they
coincide, Lemma 3 gives (22).  If they differ, Lemma 4 rules out a singleton
zero for either colour because the opposite map has rank two.  Hence each
zero set has size at least two; disjointness and `|U|<=4` give exactly (23).
`square`

The primary and independent finite audits replay this entire labelled
support/rank census rather than relying only on the preceding count prose.

## 6. A two-dimensional pure-companion no-go

### Lemma 6 (rank-two maps cannot have a nonzero pure companion)

Let `J_s,J_t` both have rank two, and let coordinate lines `L_s,L_t` lie in
their respective row spaces.  Then

```text
g_(st)=p_s tensor q_t+q_s tensor p_t                 (24)
```

cannot be nonzero and supported only on `L_s tensor L_t`.

### Proof

Choose a nonzero quotient functional

```text
alpha:row J_s -> (row J_s)/L_s.                       (25)
```

Put `A=alpha p_s` and `B=alpha q_s`, viewed as linear forms in the two
independent probe variables.  Applying `alpha` to the first factor of (24)
gives

```text
A(z_0)q_t(z_1)+B(z_1)p_t(z_0)=0.                     (26)
```

If both `A,B` are nonzero, fix one probe point on which each is nonzero.
Equation (26) puts the complete images of both `X_t` and `Y_t` on one common
line, contradicting `rank J_t=2`.

If `A!=0,B=0`, then (26) gives `Y_t=0`.  Rank two makes `X_t` span
`row J_t`.  Apply the quotient by `L_t` to the second factor of (24); its
nonzero value on `X_t` forces `Y_s=0`, making (24) zero, a contradiction.
The case `A=0,B!=0` is symmetric.  Finally `A=B=0` would put both shores of
`J_s` on `L_s`, contradicting rank two. `square`

The zero-companion boundary is retained: the lemma excludes only a
**nonzero** pure companion.

## 7. Excluding the distinct and pure-axis trunks

In the distinct-singleton profile (23), use (6) with `S={n,m}`.  The four
cross-contracted nonaxis labels kill colours `c,d`; colour `e` has no zero
and survives.  The complementary deck is a scalar, so the nonzero equality
would make `g_(nm)` pure at `(e,e)`.  Since

```text
e_e^* in row J_n cap row J_m,                          (27)
```

Lemma 6 gives a contradiction.  Thus (23) is empty.

Now take (22) with `P={p}`.  Then `U=E_c` has three labels.  Use
`S={n,m,p}` and quotient only the pure slot.  Every source pair meeting `p`
dies; the remaining source is

```text
g_(nm) tensor hbar_p.                                 (28)
```

Colours `d,e` both survive.  Their images in the pure-slot quotient are
linearly independent because the active full-row covector has a nonzero
`c`-coordinate.  Across the flattening

```text
(n,m) | (p),                                           (29)
```

the source (28) has rank at most one while the target has rank two.  Hence
the one-pure-axis same-singleton profile is empty.

Finally take (22) with `P=empty`, so `|U|=4`.  If exactly three labels lie in
`E_c` and the fourth lies in `E_d` or `E_e`, the `S={n,m}` equation has one
surviving complementary colour and again forces a nonzero pure companion,
contradicting Lemma 6.

### Theorem 7 (exactly-two-deficient binary localization)

Every complete zero-anchor root-order-three all-six-rigid witness with
exactly two deficient joint maps lies in the single residual family (1).
Equivalently, after relabelling colours,

```text
K_n=K_m=K e_c,
row J_n=row J_m=span{e_d^*,e_e^*},
P=empty,
E_d=E_e=empty,
|E_c| in {3,4}.                                       (30)
```

Moreover the `S={n,m}` member of (6) is

```text
h_(nm) g_(nm)
 =lambda_d e_(n,d)^* tensor e_(m,d)^*
  +lambda_e e_(n,e)^* tensor e_(m,e)^*,
h_(nm),lambda_d,lambda_e !=0.                         (31)
```

Thus the deficient companion is binary diagonal over `F`.

## 8. The binary residual is algebraically nonempty

The binary conclusion (31) is not itself contradictory.  On the common row
plane take, schematically,

```text
p_n=e_d^*,       q_n=e_e^*,
p_m=e_e^*,       q_m=e_d^*.                           (32)
```

Then both joint maps have rank two and kernel `K e_c`, while

```text
g_(nm)=e_d^* tensor e_d^*+e_e^* tensor e_e^*.         (33)
```

This is a local probe-row control, not a complete graph witness.  It proves
that the next argument must use the other same-source decks rather than
reapply a rank or pure-companion obstruction to (31).

## 9. Higher-open cancellation controls

Let

```text
Z=E_c,       |Z| in {3,4}.                            (34)
```

Leave `n,m` and a subset `T subseteq Z` open, contract the other injective
labels, and quotient the `n,m` slots by their common row plane.  Only pairs
inside `T` remain.  If `T` is a proper subset of `Z`, the colour-`c` target
is killed by a contracted zero label and the equation is homogeneous.  If
`T=Z`, it has a nonzero pure colour-`c` target.  In particular, the
two-open equations say that each projected complementary deck vanishes upon
the remaining cross-product contractions; they do not say that the
uncontracted deck tensor is zero.

### Control 9.1 (three-port mixed-orientation triangle)

Let `Z={u,v,w}`.  Pair-open vanishing permits the one-port projected decks

```text
h_i in span_F{p_i,q_i},       h_i(k_i)=0.             (35)
```

Give `u,v` the `X`-orientation at `c` and `w` the `Y`-orientation.  Hence

```text
p_u,p_v,q_w in K e_c^*,
q_u,q_v,p_w have nonzero complementary projection.   (36)
```

Choose

```text
h_u=-p_u,       h_v=-p_v,       h_w=p_w.              (37)
```

Direct expansion in labelled-factor order gives

```text
g_(uv) tensor h_w
 +g_(uw) tensor h_v
 +g_(vw) tensor h_u
 =-2 p_u tensor p_v tensor q_w,                       (38)
```

a nonzero pure colour-`c` tensor.  The all-`X` and all-`Y` patterns fail,
but every mixed orientation has an analogous solution.

At the displayed fibre, this is compatible with one common physical edge
table.  Let `x` be the fourth, nonzero-`c` label and choose the displayed
contractions so that

```text
W_(nm)(x_n,x_m)=1,
W_(nx)(x_n,k_x)=1,
W_(mx)(x_m,k_x)=0,
W_(xi)(k_x,-)=h_i+r_i,
W_(mi)(x_m,-)=-r_i,
W_(ni)(x_n,-)=0                                      (39)
```

for `i=u,v,w`.  The physical four-label matching deck on `{n,m,x,i}` is
then exactly `h_i`.  The `r_i` cancel inside that same deck, and (35) gives
the pair-open vanishing.  Thus (38) does not rely on independently assigned
decks.

### Control 9.2 (four-port six-pair cancellation)

For `|Z|=4`, give two ports the `X`-orientation and two the `Y`-orientation.
At one exact fibre write

```text
M_r=e_c tensor r+r tensor e_c,
M_s=e_c tensor s+s tensor e_c.                        (40)
```

The two same-orientation companions are `M_r,M_s`; every cross-orientation
companion is `e_c tensor e_c+r tensor s`.  Assign the complementary
two-port decks

```text
D_(12)=-M_r/2,       D_(34)=-M_s/2,
D_(13)=D_(14)=D_(23)=D_(24)=e_c tensor e_c.           (41)
```

Then exact expansion gives

```text
sum_({i,j} subseteq Z)
  g_(ij) tensor D_(Z-{i,j})
 =4 e_c tensor e_c tensor e_c tensor e_c.             (42)
```

The six decks can share the `GLS58` polarization: take `h=1` and set
`W_ij=D_ij-a_i tensor b_j-b_i tensor a_j`.  This is a fibre-level sharp
control, not a complete GHZ witness, but it refutes any claim that the
shared-edge polarization alone prevents the cancellation.

## 10. Exact remaining restriction-separation obligation

The load-bearing successor is now:

> **Deficient-overlap restriction-separation.**  Prove that a common
> physical deck tuple satisfying every homogeneous proper-subset equation
> from Section 9 and producing the pure colour-`c` full-set target must have
> zero `S={n,m}` residual contraction; equivalently, show that the triangle
> camouflage (37)--(39) and the four-port analogue cannot coexist over the
> function field with the nonzero binary equation (31).

The theorem must control the `hW_uv` branch.  Pairwise polarization and
pointwise deck sharing are insufficient, as Controls 9.1--9.2 show.  A proof
may instead produce a legal honest lower-order receiver, but it must retain
the complete same-source compatibility and every nonzero gate required by
that receiver.

## 11. Exact frontier

```text
mixed deficient-kernel / cross-product hierarchy:      PROVED;
common deficient-support three-zero floor:              PROVED;
singleton deficient/nonaxis synchronization:            PROVED;
exactly-two support/rank classification:                 PROVED;
distinct-kernel and pure-axis two-deficient trunks:      EXCLUDED;
exactly-two residual (30)-(31):                          OPEN / LOCALIZED;
triangle and four-port termwise-separation route:        REFUTED;
three-or-more-deficient profiles:                        OPEN;
restriction-separation / source integrability:           OPEN;
response/selector/synchronization/activity package:      OPEN;
nonzero-anchor and arbitrary-root strategic node:        OPEN;
global Krenn--Gu conjecture:                             UNRESOLVED. (43)
```

## 12. Verification boundary

The primary verifier replays the complete support-only and typed finite
censuses, the rank-two pure-companion and pure-axis flattening leaves, the
binary control, and the three-/four-port identities.  The independent audit
uses only the Python standard library and shares no project imports.  These
scripts audit the finite and displayed algebraic leaves; the written
same-source tensor proof remains the proof.

From repository root run

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py
```
