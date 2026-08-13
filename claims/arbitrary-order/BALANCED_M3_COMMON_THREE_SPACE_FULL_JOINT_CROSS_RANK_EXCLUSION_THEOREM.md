# Balanced `m=3` common-three-space full-joint-cross-rank exclusion

## Status

**Exact characteristic-zero exclusion of the full-joint-cross-rank part of
the S2Q common-three-space stratum.**  In the notation of S2U, no invertible
joint cross map

```text
H:(X direct-sum Y direct-sum Z)
  -> A_1 direct-sum A_2 direct-sum A_3                 (1)
```

can have its block permanent in

```text
J + A_1 tensor e_(2,s) tensor e_(3,s).                (2)
```

In fact the proof only uses the weaker consequence that every output row
whose root-2 and root-3 colours differ is zero.  It closes the arbitrary
nonmonomial cancellation left open in S2U and strictly contains the prior
monomial, source-aligned, and two-source exceptional-row exclusions.

This does **not** close the common-three-space branch: joint cross rank at
most eight remains open, as do the multi-boundary, `beta=0`, collapsed
cross-column, rank-one, pair-plane, higher-order, and all-balanced branches.
It proves neither a global witness exclusion nor a counterexample.  Global
Krenn--Gu remains **UNRESOLVED**.

## 1. The off-diagonal zero grid

Use the rows of the three root block rows of `H` as marked bases

```text
R=(r_0,r_1,r_2),
P=(p_0,p_1,p_2),
Q=(q_0,q_1,q_2)                                       (3)
```

of three three-planes in

```text
W=X direct-sum Y direct-sum Z.                        (4)
```

Invertibility says that all nine vectors in (3) form a basis of `W`.

For `p,q in W`, define the three polarized pair products

```text
A(p,q)=p_Y tensor q_Z+q_Y tensor p_Z in Y tensor Z,
B(p,q)=p_X tensor q_Z+q_X tensor p_Z in X tensor Z,
C(p,q)=p_X tensor q_Y+q_X tensor p_Y in X tensor Y.   (5)
```

For pair tensors `(A,B,C)`, define the shared derivative

```text
D_(A,B,C)(x,y,z)
 =x tensor A+B tensor y+C tensor z.                   (6)
```

The coefficient of the block permanent on output row `(a,b,c)` is exactly

```text
D_(A(p_b,q_c),B(p_b,q_c),C(p_b,q_c))(r_a).            (7)
```

Every word allowed by (2) has equal root-2 and root-3 colours.  Therefore

```text
R subset ker D_(A(p_b,q_c),B(p_b,q_c),C(p_b,q_c))
whenever b!=c.                                        (8)
```

If one source projection of `R` is zero, `R` is contained in two source
summands and the preceding two-source theorem excludes it.  It remains to
treat the case in which all three source projections of `R` are nonzero.

## 2. The derivative-kernel dichotomy

We need two elementary tensor lemmas.

### Lemma 1 (pairwise shared-factor intersection)

For nonzero `A in Y tensor Z` and `B in X tensor Z`, the three-spaces

```text
X tensor A,
B tensor Y                                             (9)
```

intersect in dimension at most one.  A nonzero intersection occurs exactly
when

```text
A=y tensor t,
B=x tensor t                                           (10)
```

up to reciprocal nonzero scalars, and then the intersection is
`span(x tensor y tensor t)`.

### Proof

An equality `x tensor A=B tensor y` has rank one across both the
`X|(Y tensor Z)` and `(X tensor Z)|Y` flattenings.  The two flattenings force
the factorizations in (10), including the shared `Z` factor.  The converse
is immediate.  QED.

### Lemma 2 (three nonzero summands have at most two syzygies)

If `A,B,C` in (6) are all nonzero, then

```text
dim ker D_(A,B,C)<=2.                                 (11)
```

### Proof

By Lemma 1, the kernel of each coordinate projection from `ker D` has
dimension at most one.  If `dim ker D>=3`, the union of those three proper
linear subspaces cannot cover `ker D` over an infinite field.  Choose

```text
(x,y,z) in ker D,          x,y,z all nonzero.          (12)
```

Reduce the relation `xA+By+Cz=0` modulo the line `span(x)`.  Equality of the
remaining rank-one `Y` and `Z` tensors gives vectors

```text
b in X,  c in Y,  d in Z
```

such that

```text
A=-y tensor d-c tensor z,
B= x tensor d+b tensor z,
C= x tensor c-b tensor y.                             (13)
```

These are the signed `2 x 2` minors of

```text
[ x  y   z ]
[ b  c  -d ].                                         (14)
```

Both rows of (14) are syzygies.  Conversely the elementary
`2 x 3`-minor/Hilbert--Burch calculation says that every syzygy with
coefficients respectively linear in `X,Y,Z` is their scalar linear
combination.  There is no hidden common factor: the three nonzero minors
have multidegrees `011`, `101`, and `110`, whose coordinatewise minimum is
`000`.  Thus the indicated degree-one syzygy space has dimension at most
two, contradicting `dim ker D>=3`.  This proves (11).  QED.

Now restrict `(A,B,C) -> D_(A,B,C)|_R`.  If it has a nonzero kernel vector,
then `R` lies in the kernel of the corresponding `D`.

- One nonzero member among `A,B,C` makes one source projection of `R` zero.
- Three nonzero members are impossible by Lemma 2.
- With exactly two nonzero members, Lemma 1 says either the relation space is
  zero or the two pair tensors have one shared factor.

Hence, after permuting sources, the only noninjective full-support case is

```text
A=y tensor t,
B=-x tensor t,
C=0,                                                   (15)
```

whose derivative kernel is

```text
Z direct-sum span(x+y).                               (16)
```

A three-plane in (16) with nonzero projections to all sources has, after
basis changes, exactly one of the two normal forms

```text
R=span(x+y,       z_1,z_2),
R=span(x+y+z_0,   z_1,z_2).                           (17)
```

The first has rank-two `Z` projection and the second rank three.  We have
proved the exhaustive dichotomy

```text
D|_R injective;                                       REGULAR
or R has one of the synchronized forms (17).          EXCEPTIONAL       (18)
```

## 3. The regular derivative case

In the regular case, (8) forces all three tensors in (5) to vanish.  For
fixed nonzero `q`, let

```text
Z(q)={p:A(p,q)=B(p,q)=C(p,q)=0}.                      (19)
```

Equality of two rank-one tensors gives the exact support classification

```text
q supported on one source:    Z(q)=that source, dim 3;
q supported on two sources:   dim Z(q)=1;
q supported on three sources: Z(q)=0.                 (20)
```

The last line uses characteristic different from two: the three pair
relations give alternating proportionalities, and the remaining equation is
`2 lambda q_Y tensor q_Z=0`.

For each `c`, the two independent vectors `p_b`, `b!=c`, lie in `Z(q_c)`.
Thus every `q_c` is pure in one source summand.  If two `q_c` use different
summands, their shared off-diagonal `p_b` lies in the zero intersection of
those summands.  If all three use the same summand, all three `p_b` do too,
putting six independent rows in a three-space.  Both alternatives contradict
invertibility.

## 4. The exceptional derivative case

Put `R` in (17), and set

```text
ell_minus=span(x-y),
ell_plus =span(x+y),
L=Z direct-sum ell_minus,
M=Z direct-sum span(x,y).                              (21)
```

Equations (8) now say that the pair products in (5) have the form (15).
A direct rank-one-tensor calculation gives every `q` whose zero-divisor
space has dimension at least two:

| position of `q` | `Z_R(q)` |
|---|---|
| `q in X\{0}` | `X` |
| `q in Y\{0}` | `Y` |
| `q in Z\{0}` | `Z direct-sum ell_minus` |
| `q in ell_minus\{0}` | `Z direct-sum ell_plus` |
| `q=alpha(x-y)+z`, `alpha!=0`, `z!=0` | `Z` |

No other `q` has two independent zero divisors.  For completeness, when
`q_X=alpha x` and `q_Y=beta y`, the remaining vector equation is

```text
(alpha+beta)p_Z+lambda(alpha-beta)q_Z=0,               (22)
```

which yields exactly the last three rows of the table.  If either nonzero
`q_X` or `q_Y` is not on its distinguished line, the rank-one equations
leave at most one scalar zero divisor.

Therefore every `q_c` lies in

```text
X union Y union L.                                    (23)
```

If one lies in `X`, its kernel is `X`; nonzero pairwise intersections force
all three `q_c` and all three `p_b` into `X`, contradicting independence.
The same holds for `Y`.  The only remaining possibility is

```text
q_0,q_1,q_2 in L.                                     (24)
```

Every zero-divisor space in the table for a point of `L` lies in `M`, so all
three `p_b` lie in `M` as well.  But (17) also gives `R subset M`, and

```text
dim M=5.                                               (25)
```

All nine rows of `H` would lie in a five-space, the final contradiction.

## 5. Proof-topology consequence

The S2U branch now has the exact status

```text
joint cross rank 9:                         IMPOSSIBLE;
joint cross rank <=8:                       OPEN;
other common-three-space component types:  OPEN;
rank-one / pair-plane / m>=4 branches:      OPEN;
global Krenn--Gu conjecture:                UNRESOLVED.                (26)
```

The largest immediate S2 continuation is no longer the block-permanent rank
floor.  It is to couple the joint-rank-at-most-eight locus to the S2T
multi-boundary, `beta=0`, and collapsed cross-column trichotomy.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_full_joint_cross_rank_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_full_joint_cross_rank_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_full_joint_cross_rank_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_full_joint_cross_rank_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_full_joint_cross_rank_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_full_joint_cross_rank_exclusion.py
```

The primary replay checks the 20 kernel-incidence normal forms over `Q`
(18 injective and exactly the two synchronized exceptions), the sharp
two-syzygy Hilbert--Burch boundary, both exceptional derivative kernels, all
seven ordinary support orbits, seven exceptional zero-divisor orbits, and
both 27-pattern pigeonholes.  The independent no-import audit uses its own
`Fraction` elimination, reconstructs the 20 rational projection triples
from their kernels, and independently checks the pair-product ranks and
category covers.  Lemmas 1--2 and the calculations in Sections 3--4 are the
arbitrary characteristic-zero proof; the finite atlas is an exact replay,
not a replacement for the proof.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_MONOMIAL_ROOT_EDGE_LOCALIZATION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_MONOMIAL_ROOT_EDGE_LOCALIZATION_THEOREM.md)
- [`BALANCED_M3_FULL_JOINT_CROSS_RANK_TWO_SOURCE_EXCEPTIONAL_ROOT_ROW_OBSTRUCTION.md`](BALANCED_M3_FULL_JOINT_CROSS_RANK_TWO_SOURCE_EXCEPTIONAL_ROOT_ROW_OBSTRUCTION.md)
