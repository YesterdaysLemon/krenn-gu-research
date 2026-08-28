# Maximum-root surplus-two zero-anchor four-deficient pair-class and probe-dependent four-port boundary

## Status

**Candidate exact characteristic-zero localization and receiver-interface
boundary (`GLS68`).**  Continue from the `GLS63` mixed-kernel hierarchy and
the universal `GLS67` pair-class theorem on the zero-anchor, root-order-three,
all-six-rigid branch.  Assume exactly four auxiliary joint maps are deficient.

The `GLS63` incidence and singleton rules followed by every `GLS67` two-open
pair constraint give the exact normalized finite census

```text
137,781 -> 20,778 -> 4,794 profiles,
50 canonical support/rank/zero-count keys.             (1)
```

No profile with two pure-axis injective labels survives.  Among the survivors,
exactly `54` profiles in two canonical keys have two nonaxis labels, no
cross-product coordinate identically zero, and hence a three-colour target
after both nonaxis cross contractions.  Their deficient types are

```text
S_c,S_c,R_c,R_c,       or       S_c,S_c,R_c,T_c.      (2)
```

Those `54` profiles are **not excluded by the displayed direct application**
of the accepted six-vertex theorem.
The cross-product contraction vector at a nonaxis label depends bilinearly on
the two open probe variables.  With two such contractions, the resulting
four-port pair/deck identity has probe bidegree `(3,3)`, whereas an honest
six-vertex matching tensor is separately linear in the two root modes and has
bidegree `(1,1)`.  Specializing the probes makes the contraction vectors fixed
but removes the two roots, leaving a four-port equation rather than a
six-vertex graph.  Thus the visually tempting six-mode reconstruction is an
interface error.

All `4,794` profiles remain open: `54` ternary four-port profiles in two keys
and `4,740` binary or monocolour profiles in forty-eight keys.  The result is a
necessary-profile localization and an exact no-shortcut boundary, not a
four-deficient exclusion.  The three-deficient residual, five- and
six-deficient branches, unique-nonrigid branch, attachment, response,
selector, synchronization/activity, nonzero anchor, arbitrary root order,
and global conjecture remain open.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Parent-theorem checkpoint

The parent proposition attacked is:

> No complete zero-anchor root-order-three all-six-rigid hypothetical witness
> has four deficient auxiliary joint maps.

This attempt starts from the complete `GLS63` hierarchy and applies all six
two-open `GLS67` pair classes simultaneously.  It then tests the unique
fully ternary residual against the strongest nearby finite theorem.  The test
finds a precise obstruction rather than silently applying that theorem: the
effective complementary decks vary with the same probes that would have to
remain open as six-vertex roots.

A successor is load-bearing if it uses the common physical origin of those
probe-dependent decks, proves a genuine probe-independent matching-graph
descent, or excludes the four-port `(3,3)` identity coefficientwise.  Another
support-only subdivision without such coupling would not address the parent
obstruction.

## Dependencies and notation

- [`GLS63`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_MIXED_KERNEL_PARTIAL_UNCONTRACTION_AND_TWO_DEFICIENT_BINARY_LOCALIZATION_THEOREM.md)
  owns the mixed deficient-kernel/nonaxis-cross-product hierarchy, the
  supports `A_n`, the disjoint zero sets `E_a`, the common-support floor, and
  the singleton deficient/nonaxis theorem.
- [`GLS67`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_THREE_DEFICIENT_PAIR_CLASS_AND_P3_ORBIT_LOCALIZATION_THEOREM.md)
  owns the universal two-open pair-class equation and its rank and pure-axis
  consequences.  Its statement is uniform in the number of deficient labels.
- [`GLS58`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ALL_RIGID_KERNEL_CONTRACTION_AND_CROSS_PRODUCT_REDUCTION_THEOREM.md)
  owns the probe-dependent cross products and distinguishes them from fixed
  joint-kernel contractions.
- [`GLS54`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FOUR_SLOT_PARTIAL_UNCONTRACTION_SIX_VERTEX_RECONSTRUCTION_AND_FIVE_LABEL_FLOOR_THEOREM.md)
  records an honest six-vertex reconstruction in which every contracted
  vector is independent of the six vertices left open.
- The accepted [six-vertex exclusion](../finite/n06/SIX_VERTEX_CERTIFICATE.md)
  is an interface control here, not a premise used to eliminate a profile.

Retain the `GLS63` partition

```text
Bhat=N disjoint-union P disjoint-union U,
|N|=4,                 |P|+|U|=2.                    (3)
```

For each colour `a`, put

```text
M_a={n in N:a in A_n},       e_a=|E_a|.              (4)
```

For a colour permutation `{c,d,e}={0,1,2}`, the nine exact rigid deficient
types are

```text
S_c: rank two, A={c};
R_c: rank one, row J=K e_c^*, A={d,e};
T_c: rank two, A={d,e}.                               (5)
```

Each nonaxis label has one of four zero statuses: no coordinate of its cross
product is identically zero, or exactly one of the three coordinates is.
The latter alternatives are mutually exclusive because the `E_a` are
pairwise disjoint.

The census uses a declared normalized convention.  The four deficient labels
are ordered.  For a fixed `p=|P|`, the two complementary labels are put in one
canonical `P/U` order; the nonaxis zero statuses are ordered, while the
irrelevant `X/Y` orientation of a pure-axis label is suppressed.  Thus the
numbers below are not obtained by additionally choosing which complementary
label is pure.  Canonical keys then forget deficient-label order and colour
names and retain only `p`, the deficient types, and the zero-count triple.
The census is exhaustive for precisely these support/rank/zero-count data; it
does not enumerate physical edge arrays or assert that a profile is
realizable.

All identities are over the characteristic-zero polynomial domain in the two
independent probe-variable sets and the generic deficient-kernel coordinates,
or its fraction field when row ranks are discussed.

## 1. Exact four-deficient pair-class census

### Lemma 1 (`GLS63` incidence filter)

For every colour `a`:

1. `|M_a|=4` is impossible;
2. if `|M_a|=3`, then `e_a>=1`;
3. if `|M_a|=3` and `e_a=1`, the unique deficient label outside `M_a` has
   type `R_a`.

### Proof

The first statement follows from the common-support three-zero floor:
`a in A_N` would require `e_a>=3`, while `|U|<=2`.  The second statement is
the `GLS63` one-unquotiented incidence theorem.  In the singleton case its
deficient/nonaxis synchronization theorem makes the missing map rank one
with coordinate readout `a`, which is exactly `R_a`. `square`

### Lemma 2 (`GLS67` pair filter)

Suppose `e_a=0`.  Then `|M_a|<=2`.  For every two-set `R subset N`, define

```text
C_R={a:M_a=R and e_a=0}.                              (6)
```

For the complementary open pair `N-R`:

1. both deficient ranks are at least `|C_R|`;
2. if `P` is nonempty, `|C_R|<=1`;
3. if `P` is empty, `|C_R|<=2`;
4. if `|C_R|=1`, the two open maps cannot both have rank two.

### Proof

If `e_a=0` and `|M_a|>=3`, choose a two-set `R subseteq M_a`.  The universal
`GLS67` pair-class theorem forces `M_a=R`, a contradiction.  Hence a support
of size at least three is impossible.  The four displayed conclusions are
exactly the rank,
pure-quotient flattening, and pure-companion consequences of its common-deck
equation. `square`

### Theorem 3 (normalized finite census)

The exact counts are:

| `p=|P|` | `|U|` | starting profiles | after Lemma 1 | after Lemma 2 |
|---:|---:|---:|---:|---:|
| 0 | 2 | 104,976 | 16,824 | 4,530 |
| 1 | 1 | 26,244 | 3,252 | 264 |
| 2 | 0 | 6,561 | 702 | 0 |
| **total** |  | **137,781** | **20,778** | **4,794** |

The surviving zero-count patterns are:

| `p` | zero-count pattern | profiles for each displayed permutation |
|---:|---|---:|
| 0 | `(0,0,0)` | 54 |
| 0 | each permutation of `(0,0,1)` | 224 |
| 0 | each permutation of `(0,0,2)` | 364 |
| 0 | each permutation of `(0,1,1)` | 904 |
| 1 | each permutation of `(0,0,1)` | 88 |

There are fifty canonical keys: forty-five with `p=0` and five with `p=1`.

### Proof

There are `9^4` ordered deficient-type words.  For fixed `p`, the
`2-p` nonaxis labels have four zero statuses, giving respectively

```text
9^4*4^2=104,976,       9^4*4=26,244,       9^4=6,561. (7)
```

Apply Lemma 1 colour by colour, followed by Lemma 2 for each of the six
two-sets `R`.  This is a finite exhaustive predicate calculation.  The
primary verifier and a separate bit-mask audit independently enumerate the
whole starting set and agree on every row of both tables and on all fifty
canonical keys. `square`

## 2. The unique ternary four-port stratum

The target after cross-contracting all members of `U` retains exactly the
colours with `e_a=0`.  The preceding table therefore shows that a ternary
target occurs precisely when

```text
P=empty,       |U|=2,       (e_0,e_1,e_2)=(0,0,0).  (8)
```

### Lemma 4 (two exact ternary keys)

The stratum (8) contains fifty-four normalized profiles in exactly two
canonical keys:

| deficient types | normalized multiplicity |
|---|---:|
| `S_c,S_c,R_c,R_c` | 18 |
| `S_c,S_c,R_c,T_c` | 36 |

### Proof

With every colour unzeroed, Lemma 2 first gives `|M_a|<=2`.  The combined
rank and singleton pure-companion constraints then force all three `M_a` to
be two-sets.  Testing the nine types (5) leaves precisely the two displayed
multisets.  The first has `3 * 4!/(2!2!)=18` ordered realizations and the
second has `3 * 4!/2!=36`.  Both finite implementations reproduce these
key counts and multiplicities. `square`

For `N={0,1,2,3}` and `U={u,v}`, put

```text
p_t=X_t(z_0,-),       q_t=Y_t(z_1,-),
k_t=p_t cross q_t,                                    (9)
```

and, for `I in binom(N,2)`, define the actual complementary two-port deck

```text
D_(N-I)(z_0,z_1)
 =H_(U union (N-I))(k_u,k_v,-_(N-I)).                (10)
```

The `R=empty,C=U,S=N` member of the same-source hierarchy is

```text
sum_(I in binom(N,2)) g_I(z_0,z_1) tensor D_(N-I)(z_0,z_1)
 =sum_(a=0)^2 mu_a z_(0,a)z_(1,a)(k_u)_a(k_v)_a
       tensor_(n in N)e_(n,a)^*.                    (11)
```

In (8), all three target coefficients in (11) are nonzero polynomials in a
domain.  Equation (11) is an exact restriction of the original physical
graph, and every `D_(N-I)` comes from that one graph.  It is not a collection
of independently selected tensors.

## 3. Why (11) is not an honest six-vertex graph

### Theorem 5 (probe-dependent receiver-interface boundary)

Equation (11) does not, from the stated hypotheses, enter the accepted
six-vertex theorem.  In particular, that theorem cannot eliminate Lemma 4's
fifty-four profiles through the displayed direct reconstruction.

### Proof

Each `p_t` is linear in `z_0`, each `q_t` is linear in `z_1`, and their cross
product `k_t` has bidegree `(1,1)` in `(z_0,z_1)`.  Every perfect-matching
term in (10) evaluates both `u` and `v` once.  Whether `u,v` are paired to
each other or to the two open ports, the resulting deck is homogeneous of
bidegree `(2,2)`.  The pair companion `g_I` has bidegree `(1,1)`.  Hence both
sides of (11) have bidegree

```text
(1,1)+(2,2)=(3,3).                                   (12)
```

An honest six-vertex Krenn--Gu tensor on the two probe vertices and the four
members of `N` must be multilinear in every open vertex.  In particular it
has bidegree `(1,1)` in the two probe variables, with its fifteen edge
blocks fixed independently of the vectors inserted at those vertices.

The natural proposed reconstruction would retain the original root-to-`N`
edges and use `D_(N-I)` as an effective edge on the complementary pair.
But (10) makes that proposed edge depend on `z_0,z_1`, the very root
variables that are supposed to remain open.  It is therefore not a fixed
bilinear edge block.  The same probe variables occur three times on each
shore in (11), exactly as (12) records.

Alternatively, fix one probe pair `(z_0,z_1)`.  Then `k_u,k_v` and all decks
in (10) become fixed, but the roots have also been evaluated.  What remains
is a tensor equality on the four ports `N`, not a graph tensor on six open
vertices.  Generic complex specialization preserves the three nonzero
coefficients but does not restore the two missing multilinear root modes.

Nor may one freeze `k_u(z),k_v(z)` and then reopen independent probe
variables `x_0,x_1`.  The annihilation used to obtain (11) is

```text
X_u(z_0,-)(k_u(z))=Y_u(z_1,-)(k_u(z))=0,             (13)
```

whereas `X_u(x_0,-)(k_u(z))` and `Y_u(x_1,-)(k_u(z))` are generically
nonzero.  Reopening the probes therefore restores all source terms meeting
`u` or `v` and destroys the pair-only equation.

This differs from the honest `GLS54` and `GLS58` reconstructions: there the
contracted vectors are fixed independently of every vertex left open, so
the effective edge blocks are genuine fixed bilinear tensors.  No such
probe-independent descent has been proved for (10).  Therefore the
six-vertex exclusion has no valid input here. `square`

The bidegree mismatch does not prove that no different six-vertex
reconstruction can ever be derived.  It proves that the direct
cross-product-deck identification is invalid and that any future bridge must
supply new same-source factorization or descent data.

## 4. Sharp equation-level control

Target shape alone cannot contradict the ordered pair/deck equation.  On
four abstract ports choose three pairs

```text
I_0={0,1},       I_1={0,2},       I_2={0,3}.          (14)
```

For each colour `a`, assign the `I_a` pair factor to
`e_a^* tensor e_a^*`, assign its complementary deck to the same pure tensor,
absorb any prescribed nonzero target scalar into either selected factor, and
set the other ordered terms to zero.  After normalizing those three scalars,
their sum is exactly

```text
sum_(a=0)^2 tensor_(n in N)e_(n,a)^*.                (15)
```

This is a sharp control only for the abstract six-term equation.  It chooses
pair factors and decks independently, need not respect one set of shore maps,
need not arise from one physical `H`-tensor, and is not a Krenn--Gu witness.
It shows why a valid exclusion must use the integrability omitted by the
control rather than the fact that the right side of (11) is ternary diagonal.

The other `4,740` profiles have binary or monocolour full-cross targets:

```text
p=0: 4,476 profiles;
p=1:   264 profiles;
48 canonical keys total.                              (16)
```

Even a future honest six-vertex descent would not let the accepted ternary
theorem exclude those target supports.

## 5. Exact frontier

```text
four-deficient GLS63/GLS67 normalized census:          PROVED;
137,781 -> 20,778 -> 4,794 profiles:                   PROVED;
50 canonical support/rank/zero-count keys:             PROVED;
two-pure-axis branch:                                  EMPTY;

fully ternary four-port stratum:                       54 profiles / 2 keys;
direct six-vertex reconstruction from cross decks:     INVALID INTERFACE;
those 54 profiles excluded:                            NO;

binary/monocolour stratum:                             4,740 profiles / 48 keys;
all four-deficient profiles:                           OPEN;
three-deficient eight-orbit residual:                  OPEN;
five-/six-deficient branches:                          OPEN;
same-source deck integrability or alternate descent:   OPEN;
unique-nonrigid and every downstream gate:             OPEN;
global Krenn--Gu conjecture:                            UNRESOLVED.         (17)
```

The load-bearing successor should compare the six decks (10) as cofactors of
one common two-contracted physical matching tensor while varying the probes,
or pull (11) back into hierarchy members with one nonaxis label left open.
At minimum it must distinguish physical same-source decks from independently
chosen bilinear factors.  A support count, target-rank argument, or generic
probe specialization alone cannot cross the boundary in Theorem 5.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_four_deficient_pair_class_and_probe_dependent_four_port_boundary.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_four_deficient_pair_class_and_probe_dependent_four_port_boundary.py
```

The primary implementation uses explicit deficient-type objects and set
supports.  The independent audit imports no project code and instead uses
integer support masks and a separately written traversal.  Both enumerate
the full normalized starting set and report the same three stage counts,
zero-pattern totals, count of fifty keys, `54/4,740` split, and two
ternary-key multiplicities.  They do not exchange or compare serialized key
sets.  Both also record the `(3,3)` probe degree and an abstract ternary
pair/deck control.

The programs audit the finite and displayed algebraic leaves.  The written
same-source derivation and receiver-interface distinction are the proof;
neither script proves physical realizability or nonrealizability of any
surviving profile.
