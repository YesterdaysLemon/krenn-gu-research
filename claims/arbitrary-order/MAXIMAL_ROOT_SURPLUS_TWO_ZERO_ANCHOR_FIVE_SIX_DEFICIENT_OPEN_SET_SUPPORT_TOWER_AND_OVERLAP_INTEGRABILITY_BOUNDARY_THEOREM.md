# Maximum-root surplus-two zero-anchor five-/six-deficient open-set support tower and overlap-integrability boundary

## Status

**Proved exact characteristic-zero higher-deficient parent localization
(`GLS69`).**  Continue on the zero-anchor, root-order-three, all-six-rigid
branch from the `GLS63` same-source mixed hierarchy and the universal `GLS67`
pair classes.

For every colour `a`, define its deficient missing set and its complete
minimal open set by

```text
D_a=N-M_a,             L_a=D_a disjoint-union E_a.   (1)
```

The first result below identifies the formal coefficient/colour-term support
of **every** hierarchy member exactly:

```text
colour a survives on open set T  iff  L_a subseteq T. (2)
```

All restrictions from `T` to a smaller open set are literal faces of one
physical tensor identity.  Evaluating a deficient open slot at its generic
kernel vector, or a nonaxis open slot at its cross product, gives the
corresponding smaller-set equation.  This proves open-set support extraction
and face synchronization; it does not prove that the synchronized tower is
inconsistent.

The exact normalized higher-deficient censuses are:

```text
five deficient, P=1:  59,049 -> 18,270 ->  2,640, 12 keys;
five deficient, U=1: 236,196 -> 79,095 -> 24,435, 89 keys;
six deficient:       531,441 ->276,750 -> 99,855
                                      -> 99,180, 86 keys.  (3)
```

For five deficient labels, every survivor has a minimal `L_a` of size two or
three.  This does **not** reduce the complete tower to pair and triangle
equations: in the one-nonaxis branch, 270 profiles also have a five-open
colour equation, and 150 of those profiles have no size-two minimum.  Thus
the large and small faces must be coupled.

For six deficient labels, the minimum `|D_a|` is two, three, or four.  Every
three-open target has at most two colours.  The pair predicates first leave
`99,855` profiles in 90 support/type orbits.  The actual three-open source
span excludes 675 of them in four orbits, leaving `99,180` profiles in 86
orbits.  An exact `P_3 -> Delta_2` restriction over `Q(omega)` shows that
binary triangle shape alone is nevertheless noncontradictory.

No entire five- or six-deficient branch is closed by this theorem.  The
post-span residuals, the eight three-deficient orbits, all four-deficient
profiles, unique-nonrigid branch, attachment, response, selector,
synchronization/activity beyond the face maps, nonzero anchor, arbitrary
root order, and global conjecture remain open.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## Parent-theorem checkpoint

The parent proposition attacked is:

> No complete zero-anchor root-order-three all-six-rigid hypothetical witness
> has five or six deficient auxiliary joint maps.

This attempt does not select one support fibre.  It gives a formula for the
whole Boolean open-set tower, proves that every face uses restrictions of the
same physical decks, exhausts every five-/six-deficient support/rank profile,
applies the first exact three-open source-span obstruction, and tests the
remaining binary triangle mechanism against a sharp exact control.  The
result is a precise obstruction rather than a branch closure: face
synchronization is automatic, but the required contradiction must use the
coefficientwise dependence of different faces on the common physical edge
array.

A successor is load-bearing if it proves a restriction-separation theorem
for the shared decks, produces an exact common-graph countermodel satisfying
the whole tower, or derives a genuine lower-order fixed-edge descent.  Merely
replaying one minimal face or treating its one-port decks as independent does
not address the parent.

## Dependencies, field, and notation

- [`GLS63`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_MIXED_KERNEL_PARTIAL_UNCONTRACTION_AND_TWO_DEFICIENT_BINARY_LOCALIZATION_THEOREM.md)
  owns the mixed deficient-kernel/nonaxis-cross-product hierarchy, the
  supports `A_n`, the disjoint zero sets `E_a`, and the common/singleton
  incidence theorems.
- [`GLS67`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_THREE_DEFICIENT_PAIR_CLASS_AND_P3_ORBIT_LOCALIZATION_THEOREM.md)
  owns the universal two-open pair class and its rank and pure-axis
  constraints.
- [`GLS68`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FOUR_DEFICIENT_PAIR_CLASS_AND_PROBE_DEPENDENT_FOUR_PORT_BOUNDARY_THEOREM.md)
  records why a probe-dependent cross-product pullback is not automatically
  a fixed-edge six-vertex graph.
- The accepted zero, pure, and binary controls for `P_3` are recorded in the
  `GLS67` dependencies.  They are source controls, not graph witnesses.

Work over the characteristic-zero polynomial domain in the two independent
probe-variable sets and independent generic coordinates on every deficient
kernel, or its fraction field `F` when ranks are used.  Exact controls may
extend scalars to a finite characteristic-zero extension; no finite-field or
numerical observation is promoted to a proof.

Retain

```text
Bhat=N disjoint-union P disjoint-union U,             (4)
```

and for each colour put

```text
M_a={n in N:a in A_n},
D_a=N-M_a,
E_a={u in U:(k_u)_a is the zero polynomial},
L_a=D_a disjoint-union E_a.                           (5)
```

The union in `L_a` is disjoint because `D_a subseteq N` and
`E_a subseteq U`.

For a colour permutation `{c,d,e}={0,1,2}`, use the nine rigid deficient
types

```text
S_c: rank two, A={c};
R_c: rank one, row J=K e_c^*, A={d,e};
T_c: rank two, A={d,e}.                               (6)
```

Each nonaxis cross product has no identically zero coordinate or exactly one
such coordinate.  The `E_a` are pairwise disjoint.

## 1. Universal open-set support extraction

Fix an arbitrary set

```text
T subseteq N union U.                                 (7)
```

Put

```text
R=N-T,                 C=U-T,                 S=T union P. (8)
```

Contract each `n in R` at its independent generic kernel vector `x_n`,
contract each `u in C` at `k_u`, and leave `S` open.  For every `p in P`,
quotient its open covector space by the active full-row line.  Write

```text
q_(P,a)=tensor_(p in P) pi_p(e_(p,a)^*),              (9)
```

with the empty tensor understood as one.  Every `q_(P,a)` is nonzero.

For `I in binom(T,2)`, let

```text
Hbar_I^T
 =(tensor_(p in P) pi_p)
   H_(Bhat-I)(x_R,k_C,-_((T-I) union P)).             (10)
```

This is an evaluation and quotient of the actual complementary physical
deck from the original graph.

### Theorem 1 (exact open-set equation)

Every hierarchy member (7) satisfies

```text
sum_(I in binom(T,2)) g_I tensor Hbar_I^T
 =sum_(a:L_a subseteq T) lambda_(T,a)
       tensor_(t in T)e_(t,a)^* tensor q_(P,a),       (11)
```

where every displayed `lambda_(T,a)` is a nonzero polynomial.

### Proof

Apply the `GLS63` hierarchy with the sets (8).  A source pair meeting a
contracted deficient label is killed by its joint-kernel vector.  A source
pair meeting a contracted nonaxis label is killed by its cross product.  A
pair meeting `P` is killed after the active-line quotient.  Thus precisely
the pairs inside `T` remain, with the same physical decks (10).

Before suppressing nonzero constants, the target coefficient in colour `a`
is

```text
mu_a z_(0,a)z_(1,a)
 product_(n in R)(x_n)_a product_(u in C)(k_u)_a.     (12)
```

For a generic kernel vector, `(x_n)_a` is nonzero exactly when
`a in A_n`, or equivalently `n notin D_a`.  Hence the deficient product is
nonzero exactly when `D_a subseteq T`.  The nonaxis product is nonzero
exactly when every member of `E_a` was left open, equivalently
`E_a subseteq T`.  The polynomial ring is a domain, so the whole coefficient
is nonzero exactly when `L_a subseteq T`.  This proves (11). `square`

### Corollary 1.1 (minimal support class)

Choose `L` inclusion-minimal among `{L_0,L_1,L_2}` and set `T=L`.  The target
colours in (11) are exactly

```text
C_L={a:L_a=L}.                                       (13)
```

Thus every profile has a minimal same-source leaf.  Its target class may
contain one, two, or three colours, and it may retain the extra `P`-quotient
factor.  The class is nonempty.  Minimality does not make the complementary
physical decks independent.

### Theorem 2 (face synchronization)

Let `t in T`.

1. If `t in N`, evaluate the `t`-slot of (11) at `x_t`.
2. If `t in U`, evaluate that slot at `k_t`.

In either case the resulting equation is exactly the hierarchy member for
`T-{t}`.  These face maps commute for different labels.

### Proof

Every source term whose pair `I` contains `t` is killed by the corresponding
kernel or cross-product identity.  In every term with `t notin I`, evaluating
the physical deck (10) merely moves `t` from the open set into the contracted
set, producing `Hbar_I^(T-{t})`.

On the target, a deficient evaluation retains colour `a` exactly when
`t notin D_a`; a nonaxis evaluation retains it exactly when `t notin E_a`.
Together with `L_a subseteq T`, this is equivalent to
`L_a subseteq T-{t}`.  Scalar evaluation multiplies the existing coefficient
by the same factor appearing in the smaller hierarchy member.  Evaluations
on distinct tensor factors commute. `square`

In particular, evaluating one slot of a three-open equation recovers the
single complementary two-open pair equation.  It does not produce a new sum
of three pair equations.  Evaluating all three deficient slots kills every
pair companion.  The pair leaves are synchronized faces, not three extra
independent constraints.

### Corollary 2.1 (exact open-set overlap ledger)

Let

```text
s=#{n in N:|A_n|=1},       e=|E_0 union E_1 union E_2|. (14)
```

Then

```text
sum_a |L_a|=|N|+s+e,
sum_(a<b)|L_a intersection L_b|=s,
L_0 intersection L_1 intersection L_2=empty.         (15)
```

### Proof

A deficient label with a singleton support is missing from two colours and
contributes two to the first sum and one to the pair-intersection sum.  A
deficient label with a two-colour support is missing from one colour and
contributes one and zero, respectively.  Thus the deficient contributions
are `|N|+s` and `s`.  Every nonaxis zero label belongs to exactly one `E_a`,
so it adds one to the first sum and none to an intersection.  No deficient
support is empty and the three `E_a` are disjoint, proving the triple
intersection statement. `square`

### Corollary 2.2 (two-open floor for five/six deficient maps)

If `|N|` is five or six, then `|L_a|>=2` for every colour.

### Proof

If `D_a` were empty, then `a in A_N`; the common-support theorem would
require at least three members of `E_a`, but `|U|<=1`.  If
`D_a={n}` and `E_a` were empty, the one-unquotiented incidence theorem would
force `E_a` to be nonempty.  These exhaust the possibilities with
`|L_a|<=1`. `square`

Hence no source-free zero- or one-open contradiction exists.  At the floor
`|L_a|=2`, the source retains one formal pair term.  When `E_a=empty`, this
is the `GLS67` pair class.  When `|N|=5`, `U={u}`, `E_a={u}`, and
`D_a={n}`, the `GLS63` singleton theorem instead forces the deficient map at
`n` to be `R_a`; `GLS67` does not directly apply because contracting `u`
would kill colour `a`.

### Corollary 2.3 (sharp support-only overlap controls)

The overlap ledger and the two-open floor do not force a pair leaf.  The
following exact type profiles pass the finite predicates used below:

- for six deficient labels, `S_0^2,S_1^2,S_2^2` has
  `(|L_0|,|L_1|,|L_2|)=(4,4,4)`, with three pure minimal target classes and
  pairwise-overlapping open sets;
- for five deficient labels and `P=1`, the word
  `S_0,S_0,S_1,S_1,S_2` has open sizes `(3,3,4)`;
- the same five-deficient word with `U=1` and `E_2={u}` has open sizes
  `(3,3,5)`.

These are support/rank controls, not physical graph witnesses.  They show
that a closure argument must use source/deck integrability rather than only
the cardinalities or intersections of the `L_a`.

## 2. Exact finite predicates

Let `m=|N|`.  The `GLS63` rules used in the censuses are:

1. if `|M_a|=m`, then `|E_a|>=3`;
2. if `|M_a|=m-1`, then `E_a` is nonempty;
3. if `|M_a|=m-1` and `|E_a|=1`, the unique missing deficient map is `R_a`.

For every `(m-2)`-set `R subset N`, the `GLS67` class is

```text
C_R={a:M_a=R and E_a=empty}.                          (16)
```

If `k=|C_R|`, both complementary open deficient maps have rank at least
`k`; `P!=empty` gives `k<=1`, `P=empty` gives `k<=2`, and `k=1` is impossible
when both open maps have rank two.

These are necessary support/rank predicates.  Passing them does not assert
that the corresponding maps and decks extend to a physical witness.

The finite convention orders all deficient labels and all nonaxis zero
statuses.  For five deficient labels, the remaining label is considered in
the separate `P=1` and `U=1` branches; the pure-axis `X/Y` orientation is
suppressed because the predicates use only the existence of `P`.  Canonical
keys quotient deficient-label permutations and colour permutations while
retaining the branch and zero-count data.  For six deficient labels, every
auxiliary label is deficient.  These are normalized support/type keys, not
physical edge-array orbits.

## 3. Five-deficient census and five-open overlap

### Theorem 3 (exact five-deficient census)

| branch | starting | after `GLS63` | after `GLS67` | canonical keys |
|---|---:|---:|---:|---:|
| `P=1,U=0` | 59,049 | 18,270 | 2,640 | 12 |
| `P=0,U=1` | 236,196 | 79,095 | 24,435 | 89 |

For the pure-axis branch, the sorted deficient missing-size distribution is:

| `(|D_0|,|D_1|,|D_2|)` | profiles |
|---|---:|
| `(2,2,2)` | 540 |
| `(2,2,3)` | 720 |
| `(2,3,3)` | 810 |
| `(2,3,4)` | 120 |
| `(3,3,3)` | 360 |
| `(3,3,4)` | 90 |

For the nonaxis branch, the corresponding distribution is:

| `(|D_0|,|D_1|,|D_2|)` | profiles |
|---|---:|
| `(1,2,2)` | 810 |
| `(1,2,3)` | 1,440 |
| `(1,3,3)` | 720 |
| `(1,3,4)` | 240 |
| `(1,4,4)` | 15 |
| `(2,2,2)` | 3,420 |
| `(2,2,3)` | 7,320 |
| `(2,2,4)` | 720 |
| `(2,3,3)` | 6,150 |
| `(2,3,4)` | 1,680 |
| `(2,3,5)` | 60 |
| `(2,4,4)` | 60 |
| `(3,3,3)` | 1,440 |
| `(3,3,4)` | 360 |

The nonaxis zero-status totals are `2,880` with no zero and `7,185` for each
specified zero colour.

The minimum complete-open-set sizes are:

| branch | `min_a |L_a|=2` | `min_a |L_a|=3` | keys in size-three residual |
|---|---:|---:|---:|
| `P=1,U=0` | 2,190 | 450 | 3 |
| `P=0,U=1` | 17,475 | 6,960 | 30 |

### Proof

There are `9^5` ordered deficient-type words.  The pure-axis branch has one
zero-status choice and the nonaxis branch has four, giving the starting
counts.  Apply the predicates of Section 2 colour by colour and to all ten
three-set pair classes.  Canonicalize under `S_5 x S_3`.  Two independent
finite implementations reproduce every displayed total. `square`

The size-three `P=1` leaf still carries the nonzero quotient factor at the
pure-axis slot in (11); it is a four-factor equation before any additional
functional is chosen.  The size-three `U=1` leaf is an honest three-open
member of the nonlinear probe-dependent hierarchy, not automatically a
fixed-edge three-vertex graph.

### Lemma 4 (genuine five-open overlap)

In the nonaxis branch, 270 surviving profiles have some `|L_a|=5`.  Of
these, 150 profiles in two canonical keys have no size-two minimum.  Hence
their synchronized tower contains both a size-three minimal leaf and a
different five-open colour equation.

A representative support profile is

```text
S_0,S_0,S_0,S_1,S_1,       E_0={u}.                  (17)
```

It has sorted deficient missing sizes `(2,3,5)` and complete open-set sizes
`(3,3,5)`.

### Proof

The finite census directly gives the two counts and keys.  For (17), colour
zero is absent from the two `S_1` supports and gains the open nonaxis label;
colour one is absent from the three `S_0` supports; colour two is absent from
all five deficient supports.  This gives `(3,3,5)`. `square`

Therefore a theorem about only inclusion-minimal leaves cannot close the
five-deficient branch.  Theorem 2 does not establish that the five-open
member is redundant, so its interior coefficient equations and common-deck
information must be retained.

## 4. Six-deficient census and triangle ceiling

Here `P=U=empty`, so `L_a=D_a`.  The `GLS63` one-unquotiented incidence rule
forces `|M_a|<=4`, or equivalently `|D_a|>=2`.

### Theorem 5 (exact six-deficient pair-level census)

Before using any three-open source span, the finite stages are

```text
531,441 -> 276,750 -> 99,855 profiles,               (18)
```

and the pair-level residual has ninety canonical keys.  Its sorted
missing-size table is:

| `(|D_0|,|D_1|,|D_2|)` | keys | profiles |
|---|---:|---:|
| `(2,2,2)` | 4 | 2,430 |
| `(2,2,3)` | 10 | 15,840 |
| `(2,2,4)` | 8 | 5,040 |
| `(2,3,3)` | 12 | 23,760 |
| `(2,3,4)` | 11 | 15,120 |
| `(2,3,5)` | 2 | 1,440 |
| `(2,4,4)` | 4 | 1,575 |
| `(2,4,5)` | 1 | 180 |
| `(3,3,3)` | 14 | 14,880 |
| `(3,3,4)` | 13 | 14,400 |
| `(3,3,5)` | 4 | 1,800 |
| `(3,3,6)` | 1 | 60 |
| `(3,4,4)` | 4 | 2,880 |
| `(3,4,5)` | 1 | 360 |
| `(4,4,4)` | 1 | 90 |

By minimum open size this is:

| minimum `|D_a|` | keys | profiles |
|---:|---:|---:|
| 2 | 52 | 65,385 |
| 3 | 37 | 34,380 |
| 4 | 1 | 90 |

### Proof

Enumerate all `9^6=531,441` ordered type words, impose the Section 2
predicates for all fifteen four-set pair classes, and canonicalize under
`S_6 x S_3`.  The primary set implementation and independent bit-mask
implementation agree on every displayed aggregate. `square`

### Theorem 6 (three-open target ceiling and rank-one span obstruction)

For a triple `T subset N`, the exact target support is

```text
{a:D_a subseteq T}.                                  (19)
```

It has size at most two.  More strongly, if `i in T` has deficient type
`R_c`, then

```text
#{a:D_a subseteq T and a!=c} <= 1.                  (20)
```

Applying (20) to the pair-level census removes exactly 675 profiles in four
`S_6 x S_3` type-profile orbits, not physical source/edge-array orbits:

| removed type orbit, up to colour | profiles |
|---|---:|
| `S_0^2 R_0^4` | 45 |
| `S_0^2 R_0^3 T_0` | 180 |
| `S_0^2 R_0^2 T_0^2` | 270 |
| `S_0^2 R_0 T_0^3` | 180 |

Thus the final source-span stage is

```text
99,855 -> 99,180 profiles, 90 -> 86 canonical keys.
```

Only the `(2,2,4)` row of Theorem 5 changes, from `5,040 / 8` profiles/keys
to `4,365 / 4`.  The final minimum-size split is:

| minimum `|D_a|` | keys | profiles |
|---:|---:|---:|
| 2 | 48 | 64,710 |
| 3 | 37 | 34,380 |
| 4 | 1 | 90 |

Across all twenty triples and every post-span profile, the exact maxima are:

| maximum triple-target size | keys | profiles |
|---:|---:|---:|
| 0 | 1 | 90 |
| 1 | 76 | 95,685 |
| 2 | 9 | 3,405 |

Among the last row, 3,360 profiles have one binary triangle and 45 have four
binary triangles.

### Proof

The target formula is Theorem 1.  If all three colours survived on `T`, every
deficient label outside `T` would belong to every `M_a`; its support `A_n`
would contain all three colours.  No deficient rigid type in (6) has such a
support.

Work in the common fraction field `F` fixed above; no probe or kernel vector
is specialized and no deck or target coefficient is inverted.  Write
`T={i,j,k}`.  Up to the harmless fixed source normalization,

```text
g_ij=p_i tensor q_j+q_i tensor p_j,
```

so the source has the form

```text
g_ij tensor d_k^ij+g_ik tensor d_j^ik+g_jk tensor d_i^jk.
```

At mode `i`, the first two terms have their local source row in `row J_i`,
while the last contributes at most the one extra row `d_i^jk`.  Hence the
local source image is contained in

```text
row J_i+F d_i^jk.                                    (21)
```

The target flattening at `i` has image spanned by the distinct coordinate
lines `e_(i,a)^*` for `a` in (19): their complementary diagonal coordinate
tensors are linearly independent and their coefficients are nonzero.  If
`i` has type `R_c`, quotienting (21) by `row J_i=F e_(i,c)^*` leaves dimension
at most one.  This proves (20).  Two independent finite implementations
apply it to every profile/triple and give all displayed removals and final
counts. `square`

### Corollary 6.1 (outside-row colours are exactly opposite pair faces)

For `T={i,j,k}` and any chosen `i in T`,

```text
{a:D_a subseteq T and e_(i,a)^* notin row J_i}
 ={a:D_a={j,k}}.
```

Indeed, `e_(i,a)^* notin row J_i` is equivalent to `a in A_i`, hence to
`i notin D_a`.  Together with `D_a subseteq T` and the two-open floor
`|D_a|>=2`, this forces `D_a=T-{i}`; the converse is immediate.

More completely, if `C_I={a:D_a=I}`, then the two-open floor gives the
disjoint decomposition

```text
C_T=C_{ij} disjoint-union C_{ik} disjoint-union C_{jk}
       disjoint-union {a:D_a=T}.
```

Consequently, the tempting no-target/zero-companion route is vacuous here.
If the pair `{j,k}` has no target colour, every triangle target row at `i`
already lies in `row J_i`.  The next restriction-separation theorem must
couple nonzero pure or binary pair faces, not seek an outside-row direction
above a zero pair face.

### Corollary 6.2 (the sole binary pair-class profile)

If one two-open pair class has two target colours, then the complete
post-span profile is, up to colour and label permutations,

```text
S_c^2 T_c^4.
```

There are exactly 45 labelled profiles in this one canonical key.  Each has
four binary triangles, one for every third label outside the common missing
pair.

To see this, let the pair target colours be `{a,b}` and let `c` be the third
colour.  The two open endpoints omit both `a,b`, so the pair theorem makes
them rank-two `S_c` types.  Every outside label contains both `a,b` in its
support and is therefore `R_c` or `T_c`.  An `R_c` outside label would violate
(20) on the triangle formed with the pair, so all four are `T_c`.  Choosing
the colour and the unordered endpoint pair gives `3*binom(6,2)=45`.

The other 3,360 profiles with a binary triangle have only one such triangle:
its two colours come from distinct proper pair classes and/or an exact
three-set class.  They therefore require a different multi-face coupling
than the common binary pair class.

Thus the accepted ternary finite-vertex exclusion has no input on a
three-open face.  Pure and binary `P_3` restrictions require their own
same-source coupling.

## 5. Exact binary triangle control

Let `{a,b,c}={0,1,2}` and let `omega` satisfy

```text
omega^2+omega+1=0.                                   (22)
```

On each of three modes set

```text
p=a+c,       q=a+omega c,       h=(a+omega^2 c)/6.  (23)
```

Then

```text
(tensor_i L_i)P_3
 =a tensor a tensor a + c tensor c tensor c,
L_i(P)=p,       L_i(Q)=q,       L_i(H)=h.            (24)
```

### Proof

All three local maps are equal, so the restriction is symmetric.  On the
diagonal vector `(x,y)` its cubic is

```text
6 p q h
 =(x+y)(x+omega y)(x+omega^2 y)
 =x^3+y^3.                                           (25)
```

A symmetric trilinear tensor in characteristic zero is determined by its
diagonal cubic, proving (24).  Direct expansion gives the eight coefficients
`(1,0,0,0,0,0,0,1)`. `square`

The rows in (23) all lie in the `a,c` plane, while `p,q` are independent and
their cross product is a nonzero multiple of the missing `b` direction.
Thus this is compatible with a rank-two `S_b` local map.  It is a sharp
fixed-fibre row/deck control.  The rows `h` are not proved to be simultaneous
evaluations of one global physical `H`-tensor, and the control is not a
Krenn--Gu witness.

For example, the six-deficient support word `S_1^3 R_1^3` has

```text
D_0=D_2={the three S_1 modes},
D_1={the three R_1 modes}.                            (26)
```

One complementary triple therefore has a binary target and the other a pure
target.  The local binary control (24) and the accepted pure controls show
that neither face shape is contradictory in isolation.  Their simultaneous
common-graph realization, together with every four-/five-/six-open member,
is exactly part of the unresolved integrability obligation.

## 6. Exact frontier and next lemma

```text
open-set target support L_a subseteq T:                 PROVED;
all open-set face maps use the same physical decks:     PROVED;
face restrictions commute:                              PROVED;

five-deficient census:                                  PROVED;
P=1 residual:                                           2,640 / 12 keys OPEN;
U=1 residual:                                          24,435 / 89 keys OPEN;
U=1 profiles with a five-open colour:                      270 OPEN;

six-deficient pair-level census:                       PROVED;
rank-one three-open span exclusion:                      675 / 4 keys PROVED;
six-deficient post-span residual:                      99,180 / 86 keys OPEN;
ternary three-open six-deficient target:                IMPOSSIBLE;
binary/pure/zero three-open targets:                     ALGEBRAICALLY OPEN;

whole-tower shared-deck restriction separation:         OPEN;
five-/six-deficient branch exclusion:                   OPEN;
three-/four-deficient residuals:                        OPEN;
unique-nonrigid and every downstream gate:              OPEN;
global Krenn--Gu conjecture:                             UNRESOLVED.       (27)
```

The load-bearing successor is not another target-support count.  It must use
that, for every pair `I`, all tensors

```text
H_(Bhat-I)(x_R,k_C,-)                                  (28)
```

are restrictions of one physical matching deck as `R,C,T` vary.  Theorem 2
already identifies their boundary values with the smaller hierarchy faces.
What remains is a restriction-separation or polarization statement showing
that the interior coefficients of the three-, four-, five-, and six-open
members cannot simultaneously have the formal colour-term supports in (11),
or an exact countermodel showing that they can.

For six deficient labels and `T={i,j,k}`, define the actual one-slot deck

```text
d_k^ij=H_(Bhat-{i,j})(x_(N-T),-_k),
```

and cyclically.  The three-open equation has the form

```text
g_ij tensor d_k^ij+g_ik tensor d_j^ik+g_jk tensor d_i^jk
 =sum_(a:D_a subseteq {i,j,k}) theta_a
       e_(i,a)^* tensor e_(j,a)^* tensor e_(k,a)^*.  (29)
```

Evaluating the `k`-slot at `x_k` kills the last two source terms and recovers
the single pair equation for `{i,j}` with

```text
D_ij=d_k^ij(x_k).                                     (30)
```

This exact relation is necessary but tautologically compatible with the pair
leaf.  The missing theorem must use the uncontracted variation of all three
rows and their higher-open parents, rather than counting (28) as a new
equation or choosing the rows independently.

The sharp first test case is the sole binary pair-class profile
`S_c^2 T_c^4`.  Its nonzero binary pair equation propagates to four triangle
faces.  At each outside `T_c` port, quotienting by `row J_k` recovers only
the expected one-dimensional quotient of that pair face and leaves the
row-space component of `d_k^ij` uncontrolled.  A load-bearing successor must
couple those four row-space components through their common four-, five-,
and six-open physical parents.  The 3,360 single-binary-triangle profiles
instead couple distinct pure pair/exact-three-set classes and remain a
separate residual family.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_five_six_deficient_minimal_open_set_and_overlap_integrability_boundary.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_five_six_deficient_minimal_open_set_and_overlap_integrability_boundary.py
```

The primary implementation uses explicit deficient-type objects and set
supports.  The independent audit imports no project code, uses integer masks,
and separately checks (2) on one representative of every canonical profile
and every open-set mask.
Both reproduce the stage counts, key counts, missing-size tables, minimum
leaf splits, five-open overlap, triangle-span exclusion, post-span
triangle-target maxima, and binary-triangle multiplicity.  The primary
verifies (24) exactly over `Q(omega)`; the
independent audit replays it in `F_7`, where `omega=2`, only as a check of the
displayed characteristic-zero identity.

The programs audit the finite and displayed algebraic leaves.  The written
same-source derivation and face-synchronization proof carry the hierarchy.
Neither program proves physical realizability or exclusion of a surviving
profile.
