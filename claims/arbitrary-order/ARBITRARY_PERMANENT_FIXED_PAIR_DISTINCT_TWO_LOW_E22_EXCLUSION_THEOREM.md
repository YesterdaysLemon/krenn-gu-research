# Arbitrary permanent fixed-pair distinct-two-low `E_22` exclusion

## Status

This note proves an exact characteristic-zero exclusion for the nonzero
high-pairing branch in the fixed equality-five pair.  Its input is the
distinct-two-low reduction:

```text
exactly two low modes, one for each projection family and in distinct slots;
the other two modes are high for both projection families;
their A-pairing is mu E_22, with mu!=0;
their A-ranks are (1,2) or (2,1);
the rank-one high shore is supported only at colour 2;
at least one low shore has A-rank two on its colour-0,1 columns.
```

The full mixed-zero and diagonal target equations contradict these data.
The proof treats both different-missing low pairs, both orientations of the
rank-two low shore, and both possible low supports (singleton `2` and
support `{k,2}`).  Thus the `E_22` branch is empty.

The zero high-pairing branch remains open here.  This note does not normalize
an arbitrary equality-five pair to the fixed pair and does not prove
unrestricted permanent nonrestriction.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## 1. Fixed pair and exact inputs

Let `K` have characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

Split the ambient space as

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5},
J((r_4,r_5),(s_4,s_5))=r_4s_5+r_5s_4.                 (1)
```

At the fixed equality-five pair the complementary quartics are

```text
star(m_1)= x_4x_5 x_1 (x_3-x_2-x_0),
star(m_2)= x_4x_5 x_0 (x_3-x_2-x_1),
star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.                            (2)
```

For four ordered independent local triples assume the exact targets

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (3)
```

Write `r_(u,c)` and `a_(u,c)` for the `R`- and `A`-parts of the
colour-`c` vector in mode `u`, and let

```text
A_u=(a_(u,0),a_(u,1),a_(u,2)).                         (4)
```

Use the distinct-two-low reduction and call the low modes `a,b`, with
`a` low for `Phi_1` and `b` low for `Phi_2`.  Call the high modes `s,t`,
relabelled so that

```text
rank A_s=1,             rank A_t=2,
A_s e_0=A_s e_1=0,
A_s^T J A_t=mu E_22,                  mu!=0.           (5)
```

The different-missing low pair is one of

```text
(A_0,A_1)       or       (C_0,C_1).                    (6)
```

Rescale its pure-`R` generators to the displayed representatives and write

```text
p=sum_c alpha_c y_(a,c),              q=sum_c beta_c y_(b,c).
```

Each coefficient row has actual support either `{2}` or `{k,2}`, where its
additional allowed colour `k` is displayed below.  Finally,

```text
max(rank A_a|_{0,1}, rank A_b|_{0,1})=2.               (7)
```

## 2. Exact residual table

Put

```text
h_2 = x_0-x_1-x_2+x_3,
h_2'= -x_0+x_1-x_2+x_3.                               (8)
```

Direct contraction of the five quadratics in (2) gives the rows relevant
to the proof:

```text
line   zero mixed residual   d_2 residual   other diagonal residual   k

A_0          h_2                -2x_1       h_2+2x_2   (from d_1)      1
C_0          h_2                -2x_1       h_2-2x_3   (from d_0)      0
A_1          h_2'               -2x_0       h_2'+2x_2  (from d_0)      0
C_1          h_2'               -2x_0       h_2'-2x_3  (from d_1)      1. (9)
```

The mixed residual in the second column has zero target.  Since every low
support contains colour `2`, the `d_2` contraction has a nonzero pure
colour-`2` target.  The last residual has zero target when the low is
singleton-supported at `2`, and a nonzero pure colour-`k` target when the
support is `{k,2}`.

The three covectors in each row of (9) are independent.  Their exact common
kernels are

```text
A_0: K(1,0,0,-1),             C_0: K(1,0,1,0),
A_1: K(0,1,0,-1),             C_1: K(0,1,1,0).        (10)
```

Characteristic zero is used here through the nonvanishing of `2`.

## 3. The rank-two high-slice gate

We isolate the only tensor calculation needed below.

### Lemma 1 (rank-two high-slice gate)

Let a pure-`R` vector in one low mode be contracted into a quartic
`x_4x_5 g`, leaving modes `(u,s,t)`.  Suppose

```text
A_s e_0=A_s e_1=0.
```

For `i=0,1`, the colour-`i` slice in mode `s`, viewed as a matrix on
the local coefficient spaces of modes `u,t`, is exactly

```text
g(r_(s,i)) B_(ut),             B_(ut)=A_u^T J A_t.    (11)
```

If `rank A_u=rank A_t=2`, then `rank B_(ut)=2`.

### Proof

The polarization of `x_4x_5 g` is the sum over the three choices of the
two `A`-supplier modes.  In the colour-`i` slice, both terms which use mode
`s` as an `A` supplier vanish.  The remaining term uses modes `u,t` as the
two suppliers and evaluates `g` on `r_(s,i)`, giving (11) with no omitted
scalar.

For the rank statement, `A_t:K^3 -> A` is onto.  The form `J` identifies
`A` with `A^*`, and `A_u^T:A^* -> K^3` is injective because `A_u` is onto.
Their composition `A_u^T J A_t` therefore has rank two.  Equivalently, if
`I,J` select nonzero `2 by 2` column minors of `A_u,A_t`, then

```text
det B_(ut)[I,J]=det(A_u[:,I]) det(J) det(A_t[:,J])!=0. (12)
```

This proves the lemma.

## 4. Orientation I: the `Phi_1` low has rank two

Assume first

```text
rank A_a|_{0,1}=2.                                    (13)
```

Then `A_a` is onto `A`, as is `A_t`, so Lemma 1 says

```text
B_(at)=A_a^T J A_t                  has rank two.      (14)
```

Contract the actual pure-`R` low vector in mode `b`.  It is either `A_1`
or `C_1`.  For `i=0,1`, slice the residual cubics at colour `i` in mode
`s`.  The zero mixed target and the off-target `d_2` entries, together
with (9), (11), and `B_(at)!=0`, give

```text
h_2'(r_(s,i))=0,                  x_0(r_(s,i))=0.      (15)
```

There are two exhaustive support cases.

### 4.1 Singleton support `{2}`

The other diagonal contraction has zero target.  Equation (11) therefore
also makes its residual covector vanish on both `r_(s,0),r_(s,1)`.
By (10), both vectors lie on the same one-dimensional line: the `A_1` row
gives `K(0,1,0,-1)`, and the `C_1` row gives `K(0,1,1,0)`.

But their `A`-parts are both zero by (5).  Thus the full local columns
`y_(s,0),y_(s,1)` are proportional, contradicting independence of the
ordered local triple.

### 4.2 Support `{k,2}`

The last target in (9) is now live.  At colour `k` in mode `s`, equation
(11) reads

```text
g_k(r_(s,k)) B_(at)=beta_k lambda_k E_kk,              (16)
```

where `beta_k lambda_k!=0`.  The right side has rank one.  It is nonzero,
so `g_k(r_(s,k))!=0`; the left side consequently has rank two by (14), a
contradiction.

This excludes both family-`2` lines and both of their supports under (13).

## 5. Orientation II: the `Phi_2` low has rank two

If (13) does not hold, equation (7) gives

```text
rank A_b|_{0,1}=2.                                    (17)
```

Contract the actual family-`1` low vector in mode `a` instead.  Lemma 1,
with `u=b`, gives

```text
B_(bt)=A_b^T J A_t                  has rank two.      (18)
```

For `i=0,1`, the zero mixed residual and the off-target `d_2` entries now
give

```text
h_2(r_(s,i))=0,                   x_1(r_(s,i))=0.      (19)
```

If the low support is `{2}`, its other diagonal residual is zero too.
Equation (10) again puts both pure-`R` columns of mode `s` on one line:
`K(1,0,0,-1)` for `A_0`, or `K(1,0,1,0)` for `C_0`.  This contradicts
local independence.  If the support is `{k,2}`, the live colour-`k` slice
instead equates a nonzero scalar multiple of the rank-two matrix `B_(bt)`
to a nonzero multiple of the rank-one matrix `E_kk`, the same contradiction
as (16).

Thus orientation II is impossible as well.

## 6. Theorem and exact boundary

### Theorem 2 (distinct-two-low `E_22` exclusion)

Under (1)--(7), the exact target equations (3) have no solution over a
field of characteristic zero.

Indeed, (7) chooses orientation I or II.  Sections 4 and 5 exhaust the four
exceptional lines and the singleton/support-two split in each orientation.
This proves the theorem.

Combined with the distinct-two-low reduction, the exact boundary is

```text
number of low modes:                                  EXACTLY TWO;
family distribution:                              ONE PER FAMILY;
nonzero high-pairing branch M_(st)=mu E_22:             EXCLUDED;
zero high-pairing branch M_(st)=0:                         OPEN;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.     (20)
```

The incidence-only `E_22` fixture in the predecessor note does not
contradict the theorem: it violates a mixed-zero equation.  The present
argument pinpoints why incidence data alone survived while the full target
does not.

## 7. Exact replay

Run

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py
```

The primary verifier derives the complete residual table from the five
factorized quadratics, checks all direct polarization scalars, proves the
selected-minor identity (12), and checks every common kernel and support
branch.  The independent audit imports neither the primary verifier nor
SymPy: it rebuilds the square-free quadratics as edge dictionaries, uses a
separate rational reducer and polarization evaluator, and independently
replays both orientations and the rank mismatch.  The scripts replay the
displayed algebra; the written characteristic-zero argument proves the
theorem.
