# All-pair binary coherence for the incidence quotients

## Status

**Exact coordinate-free classification.**  The degree-five four-face
rectangle proved that every physical common-core realization must satisfy a
rank-one condition in each of the 21 two-mode incidence quotients.  This note
solves the compatibility of those 21 conditions symbolically.

Let

```text
E_i=<epsilon_i^0,epsilon_i^1>,
U_i=span{R_i,p : p in P},
q_i:E_i -> V_i^*/U_i.                                  (1)
```

Put `x_i=q_i(epsilon_i^0)` and `y_i=q_i(epsilon_i^1)`.  If

```text
dim span{x_i tensor x_j, y_i tensor y_j} <= 1           (2)
```

for every pair `i<j`, then exactly one of the following global alternatives
holds.

1. Every `q_i` has rank at most one.  Equivalently, every incidence span
   `U_i` meets the binary colour plane `E_i` nontrivially.
2. There is one exceptional mode `g` at which `q_g` has rank two.  At every
   other mode, at least one pure colour is killed:

   ```text
   epsilon_i^0 in U_i  or  epsilon_i^1 in U_i.          (3)
   ```

Both alternatives occur in exact sharp models.  Therefore the 21 quotient
conditions have been converted into a global incidence dichotomy, but not
into a contradiction.  No graph family, colour word, alignment, or support
is enumerated.

## 1. The five intrinsic local types

Only the ordered pair `(x_i,y_i)` inside its span matters.  There are five
basis-free types:

```text
0:  x_i=0,  y_i=0;
X:  x_i!=0, y_i=0;
Y:  x_i=0,  y_i!=0;
B:  x_i,y_i are nonzero and proportional;
G:  x_i,y_i are linearly independent.                  (4)
```

The letters stand for zero, the two coordinate axes, a binary common line,
and a genuine binary plane.  This is a partition, not a choice of normal
form.

### Lemma 1 (two decomposable tensors)

Let `a,c` be nonzero vectors in one vector space and `b,d` nonzero vectors in
another.  Then

```text
a tensor b  and  c tensor d are proportional
iff
a and c are proportional, and b and d are proportional. (5)
```

Proof.  The reverse implication is immediate.  Conversely, if
`a tensor b=lambda c tensor d`, choose a functional nonzero on `b` and
contract the second factor to see that `a` is proportional to `c`.  Contract
the first factor similarly.  The tensor is nonzero, so `lambda!=0`.

## 2. Pair compatibility

Condition (2) is automatic if either of its two decomposable tensors is zero.
If both are nonzero, Lemma 1 says that the two local pairs must each have type
`B`, rather than type `G`.  It follows immediately that

```text
G is compatible with 0, X, Y;
G is incompatible with B or G;
0, X, Y, B are mutually compatible in every pairing.   (6)
```

This five-type rule is the whole all-pair problem.

### Theorem 2 (binary quotient coherence dichotomy)

Assume (2) for all pairs.

- If there is no `G` mode, every local map has rank at most one.  This is
  alternative 1.
- If a `G` mode exists, (6) excludes every other `G` and every `B`.  Hence it
  is unique, and all remaining modes have type `0`, `X`, or `Y`.  Types
  `0,Y` kill `epsilon_i^0`; types `0,X` kill `epsilon_i^1`.  This is
  alternative 2.

Conversely, either alternative together with the stated local type
restrictions satisfies every pair condition by (6).  Thus the dichotomy is
necessary and sharp.

## 3. Translation back to incidence spans

The kernel of `q_i:E_i -> V_i^*/U_i` is `E_i intersect U_i`.  Therefore

```text
rank q_i <= 1  iff  E_i intersect U_i !=0.              (7)
```

At a nonexceptional mode in alternative 2, type `X` means
`epsilon_i^1 in U_i`, type `Y` means `epsilon_i^0 in U_i`, and type `0`
means both.  Type `B`, which would put only a mixed binary direction in
`U_i`, is forbidden in the presence of the exceptional genuine plane.

For seven cores the result can be read as the incidence quota

```text
either: all 7 terminal-incidence spans meet E_i;
or:    6 spans contain an actual pure axis, and one mode misses E_g.     (8)
```

This is stronger than checking the 21 quotient ranks independently: it says
how every allowed degeneracy must glue across the core modes.

## 4. Sharp models

Both branches survive at the level of (2).

### Common-line branch

Take every quotient one-dimensional and set

```text
x_i=1,                y_i=lambda_i,    lambda_i!=0.     (9)
```

Every pair in (2) consists of two scalars, hence has rank one.  Here every
mode has type `B`; the incidence span meets `E_i` in the mixed line
`<epsilon_i^1-lambda_i epsilon_i^0>`.

### One-genuine-plane branch

At one mode `g`, take `x_g=e_0,y_g=e_1`.  At each other mode choose either

```text
(x_i,y_i)=(1,0)  or  (0,1).                            (10)
```

For a pair involving `g`, one of the two tensors in (2) is zero.  For a pair
away from `g`, either the same is true or both tensors are zero.  Thus all 21
conditions hold.  This shows why the coordinate-axis clause in alternative
2 cannot be strengthened using quotient ranks alone.

These are quotient data, not asserted full-ledger graphs.

## 5. Consequence for the `2+2+1` frontier

Apply Theorem 2 to the necessary conditions from
`P7_221_DEGREE5_INCIDENCE_QUOTIENT_RECTANGLE_FLATTENING_THEOREM.md`.
Every physical realization of the formal ledger with the fixed common
terminal block must lie in one of the two incidence strata (8).

The next obstruction can therefore be split without any alignment search:

1. exclude or realize the all-seven binary-plane intersection stratum;
2. exclude or realize the one-genuine-plane/six-pure-axis stratum.

The pure ledger, degree-one/degree-three equations, or an overlapping
colour-pair rectangle must still be used.  The theorem alone does not prove
that either stratum is empty.

## Scope wall

Proved:

- the exact five-type classification of every local binary quotient;
- the complete global compatibility of all 21 pairwise rank conditions;
- the two sharp global alternatives (8);
- exact abstract models showing both alternatives survive.

Not proved:

- that the quotient models lift to one physical graph satisfying the ledger;
- incompatibility with the colour-2 diagonal direction;
- a degree-one, degree-three, or degree-seven obstruction on either stratum;
- the `P_7 -> Delta_3` restriction or the global Krenn--Gu conjecture.

The exact frontier is

```text
all 21 pair quotient constraints:  CLASSIFIED;
all-seven mixed-line stratum:      UNKNOWN;
one-plane/six-axis stratum:        UNKNOWN;
global Krenn--Gu:                  UNRESOLVED.          (11)
```

## Replay

```powershell
uv run --with sympy python verify_p7_221_all_pair_incidence_quotient_binary_coherence.py
python audit_p7_221_all_pair_incidence_quotient_binary_coherence.py
python -m py_compile verify_p7_221_all_pair_incidence_quotient_binary_coherence.py audit_p7_221_all_pair_incidence_quotient_binary_coherence.py
uv run --with ruff ruff check verify_p7_221_all_pair_incidence_quotient_binary_coherence.py audit_p7_221_all_pair_incidence_quotient_binary_coherence.py
```

The replays check the five intrinsic normal forms, the exact symbolic
compatibility rule (6), both seven-mode sharp models, and the kernel/rank
translation.  They perform no graph, word, alignment, support, or parameter
search.
