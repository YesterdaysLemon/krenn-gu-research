# Arbitrary permanent fixed-pair distinct-two-low reduction theorem

## Status

This note proves an exact characteristic-zero reduction for the fixed
equality-five pair.  Combining the committed same-mode exclusions first
shows that no remaining local mode can be low for both mixed-factor
projection families.  The common exceptional line is therefore absent, and
every low line is one of

```text
Phi_1: A_0, C_0,                 Phi_2: A_1, C_1.
```

The exact double-contraction equations then classify every pair of lows in
distinct modes.  Using that classification, a four-low cover is impossible.
A two-colour line-split argument also excludes every three-low diagram.
Consequently every exact extension has precisely two low modes: one is low
only for `Phi_1`, one is low only for `Phi_2`, they are distinct, and the
other two modes have rank three under both projection families.

For the two surviving low modes, the pairing matrix between the two high
modes is either zero or a nonzero multiple of `E_22`.  The zero branch has
high-mode `A`-ranks `(1,1)`.  In the `E_22` branch the ranks are `(1,2)` or
`(2,1)`; the rank-one high shore is supported only at colour `2`, and at
least one low mode has rank two on its colour-`0,1` `A`-columns.

Two exact rational fixtures show that both final incidence branches survive
all conclusions proved here and the committed singleton-companion rules.
They are deliberately **incidence-only** witnesses: each has a nonzero mixed
target coefficient and hence is not a `Delta_3` restriction or a
counterexample to the conjecture.

This theorem does not exclude the final two-low branches, does not normalize
an arbitrary equality-five pair to the fixed pair, and does not prove
unrestricted permanent nonrestriction.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## 1. Fixed pair and predecessor inputs

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

At the fixed equality-five pair, the complementary quartics are

```text
star(m_1)= x_4x_5 x_1 (x_3-x_2-x_0),
star(m_2)= x_4x_5 x_0 (x_3-x_2-x_1),
star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.                             (1)
```

Let the ordered independent triples

```text
(y_(t,0),y_(t,1),y_(t,2)),                 t=2,3,4,5,
```

span the local planes `L_t`.  Assume the exact target equations

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (2)
```

Split the ambient space as

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5},
J((r_4,r_5),(s_4,s_5))=r_4s_5+r_5s_4.                 (3)
```

Write `A_t:K^3 -> A` for the `A`-projection of the ordered basis of
`L_t`, and put

```text
M_(st)=A_s^T J A_t.                                    (4)
```

The two mixed-factor projections are

```text
Phi_1=(x_1,x_4,x_5,x_3-x_2-x_0),
Phi_2=(x_0,x_4,x_5,x_3-x_2-x_1).                       (5)
```

The committed kernel-support and exceptional-kernel theorems prove that
every restricted projection has rank at least two, each family has at least
one rank-two mode, and every rank-two kernel line is among

```text
Phi_1: N=x_2+x_3,  A_0=x_0+x_3,  C_0=x_0-x_2,
Phi_2: N=x_2+x_3,  A_1=x_1+x_3,  C_1=x_1-x_2.          (6)
```

The common/noncommon and noncommon/noncommon same-mode theorems exclude all
same-mode pairs except the proportional `N/N` case.  The committed `q_-`
and `q_+` theorems exhaust and exclude that last case.  Hence

```text
no L_t is low for both Phi_1 and Phi_2.                 (7)
```

If `N` lay in a local plane, it would lie in both ambient kernels; the
rank-two floor would make that mode low in both families.  Equation (7)
therefore also gives

```text
N lies in no L_t as a low kernel line.                  (8)
```

Every remaining low is consequently noncommon.  Its maximal allowed local
support is

```text
line       family       missing colour       maximal support

A_0        Phi_1               0                  {1,2}
C_0        Phi_1               1                  {0,2}
A_1        Phi_2               1                  {0,2}
C_1        Phi_2               0                  {1,2}.             (9)
```

Its actual support is any nonempty subset of the displayed two-colour set;
the size-one and size-two alternatives are exhaustive.

## 2. Complete distinct-mode pair rule

Take low generators `p` and `q` in two distinct modes.  Write their local
coefficient vectors as `alpha,beta`, with supports `S,T`, and let `s,t` be
the other two modes.  If `sigma_z` denotes the scalar left after double
contraction of channel `z`, comparison with (2) gives

```text
sigma_(m_1) M_(st)=sigma_(m_2) M_(st)=0,
sigma_(d_c) M_(st)=lambda_c alpha_c beta_c E_cc,
                                                   c=0,1,2.          (10)
```

Direct substitution in the committed double-contraction table gives the
following nonzero-channel pattern for the noncommon lines:

```text
low pair                         nonzero mixed       nonzero diagonals

same Phi_1 family                    m_2               as applicable
same Phi_2 family                    m_1               as applicable
A_0,C_1 (same missing colour)        none                 d_1,d_2
C_0,A_1 (same missing colour)        none                 d_0,d_2
A_0,A_1 (different missing)          none                 d_2
C_0,C_1 (different missing)          none                 d_2.       (11)
```

### Lemma 1 (distinct-mode noncommon pair classification)

Every compatible pair is exactly one of the following.

```text
pair type                         support condition          M_(st)

same family                      S intersect T empty             0

cross family, same missing       complementary singletons        0

cross family, different missing  S intersect T empty             0

cross family, different missing  2 in S intersect T          mu E_22,
                                                            mu!=0. (12)
```

There are no other compatible pairs.

### Proof

For a same-family pair, the indicated mixed scalar in (11) is nonzero, so
(10) gives `M_(st)=0`.  The three diagonal equations then force
`alpha_c beta_c=0` for every colour, which is precisely
`S intersect T=empty`.

For a cross-family pair with the same missing colour, the two maximal
supports coincide and both corresponding diagonal scalars in (11) are
nonzero.  If the actual supports met, (10) would first make `M_(st)`
nonzero.  The other nonzero diagonal equation would then either force it to
zero or make it a nonzero multiple of a different matrix unit.  Both are
impossible.  Thus the supports are disjoint.  Two nonempty disjoint subsets
of the same two-element set must be complementary singletons, and (10)
then gives `M_(st)=0`.

For a cross-family pair with different missing colours, the maximal
supports meet only at colour `2`, and `d_2` is the only nonzero scalar in
(11).  If both actual supports contain `2`, the `d_2` equation gives the
last line of (12).  Otherwise the actual supports are disjoint and all
right sides of (10) vanish, so `M_(st)=0`.  This proves the lemma.

Two useful consequences are immediate.  Distinct lows in one family have
disjoint supports, so at most one of them contains colour `2`.  Also every
nonzero complementary pairing matrix forced by two lows is supported only
at `(2,2)`.

## 3. Four low modes are impossible

Suppose all four modes are low.  By (7), the low modes partition into two
nonempty family classes.  Fix any pair of modes `{s,t}` and let `{u,v}` be
its complementary pair.  Since `u,v` are both low, Lemma 1 applied in those
two slots gives

```text
M_(st)=0                  or                  M_(st)=mu E_22. (13)
```

This holds for every one of the six mode pairs.  In particular,

```text
J(A_s e_c,A_t e_c)=0       for all s!=t and c=0,1.     (14)
```

Every quartic in (1) has the two factors `x_4,x_5`.  In a four-linear
evaluation those factors must be supplied by two distinct modes, and their
contribution is one of the pairings in (14).  Hence the pure colour-`0`
coefficient of `T_(d_0)` and the pure colour-`1` coefficient of `T_(d_1)`
both vanish.  This contradicts `lambda_0 lambda_1!=0` in (2).  Therefore

```text
at least one remaining mode is high in both families.  (15)
```

## 4. A two-colour three-line obstruction

We record the rank-one-slice argument needed to exclude three-low diagrams.
It is a two-colour version of the committed `A`-line-split theorem.

Let four two-dimensional local spaces be denoted `V_1,V_2,V_3,V_h`.
Write vectors as `r(y)+a(y)` under `R direct-sum A`.  Suppose

```text
rank(a|V_i)<=1,                         i=1,2,3,        (16)
```

and every pairing involving the distinguished shore vanishes:

```text
J(a(V_h),a(V_i))=0,                     i=1,2,3.        (17)
```

For a quadratic `g` on `R`, let `T_g` be the polarization of `x_4x_5 g`
on the four local spaces.

### Lemma 2 (two-colour three-line obstruction)

Under (16)--(17), two such tensors cannot simultaneously be

```text
T_(g_0)=lambda_0 e_0^* tensor e_0^* tensor e_0^*
                           tensor e_0^*,
T_(g_1)=lambda_1 e_1^* tensor e_1^* tensor e_1^*
                           tensor e_1^*,
lambda_0 lambda_1!=0.                                  (18)
```

### Proof

Ignore any zero `A`-shore among `V_1,V_2,V_3`.  On every nonzero shore
write

```text
a(y)=alpha_i(y)u_i.
```

Condition (17) removes every term using `V_h` as an `A` supplier.  If fewer
than two of the other shores are nonzero, `T_g=0`.  If exactly two are
nonzero, both occur as fixed covector factors `alpha_i` in every nonzero
`T_g`.  They cannot be proportional to both independent local covectors
`e_0^*` and `e_1^*` in (18).

It remains to take three nonzero line shores.  Put

```text
kappa_ij=J(u_i,u_j)
```

and let `G_g` be the polarization of `g`.  Exact polarization gives

```text
T_g=
 kappa_12 alpha_1 alpha_2 G_g(r_3,r_h)
+kappa_13 alpha_1 alpha_3 G_g(r_2,r_h)
+kappa_23 alpha_2 alpha_3 G_g(r_1,r_h).                (19)
```

For one nonzero rank-one slice, restrict mode `i` to `ker alpha_i`.  If its
rank-one factor vanishes there, that factor is proportional to `alpha_i`.
If it does not vanish there, (19) leaves only the term whose `A` suppliers
are the other two modes; uniqueness of factors of a nonzero pure tensor
forces both of their factors to be proportional to their respective
`alpha` covectors.  Thus, for each slice, at most one of the three local
factors fails to align with its fixed `alpha_i`.

Across the two slices in (18), there are at most two failures of alignment.
Among three modes, one mode has no failure.  At that mode both `e_0^*` and
`e_1^*` would be proportional to one fixed `alpha_i`, a contradiction.
This proves the lemma.

## 5. Three low modes are impossible

Suppose exactly three modes are low.  Two, say `a,b`, belong to one family,
the third, say `c`, belongs to the other, and `h` is high in both.  Lemma 1
gives

```text
M_(ch)=0,
M_(ah),M_(bh) in {0, nonzero multiples of E_22}.       (20)
```

The supports of `a,b` are disjoint.  Since an `E_22` case requires both
members of its inducing cross-family pair to contain colour `2`, at most
one of `M_(ah),M_(bh)` is nonzero.

The high mode has nonzero `A`-projection: if `A_h=0`, either map in (5)
would have rank at most two on `L_h`.  First suppose both matrices in the
second line of (20) vanish.  If `A_h` had rank two, nondegeneracy of `J`
would force all three low `A`-maps to vanish, killing every tensor in (1).
Thus `A_h` has rank one.  Every low `A`-image lies in its one-dimensional
orthogonal complement.  In particular, after restricting every local mode
to its colour-`0,1` plane, the three low `A`-maps have rank at most one and
all pairings involving `h` vanish.  Lemma 2 contradicts the `d_0,d_1`
targets in (2).

Now suppose, after relabelling, that

```text
M_(bh)=mu E_22,                 mu!=0,                 (21)
```

while `M_(ah)=M_(ch)=0`.  The rank-one-shore lemma from the committed
distinct-mode support-two theorem applies to (21):

```text
(rank A_b,rank A_h) in {(1,1),(1,2),(2,1)},            (22)
```

and every rank-one shore is supported only at colour `2`.  If `A_h` had
rank two, then (20) would force `A_a=A_c=0`, while (22) would make the
colour-`0,1` columns of `A_b` zero.  The pure `d_0,d_1` coefficients would
again have fewer than two `A` suppliers.  Hence `A_h` has rank one and is
supported only at colour `2`.

Let its nonzero image line be `Kq` and put `Kp=q^perp`.  The two zero
matrices in (20) put all columns of `A_a,A_c` in `Kp`; equation (21) puts
the colour-`0,1` columns of `A_b` there as well.  On the colour-`0,1`
restriction, the three low maps therefore have rank at most one and the
high map is zero.  Lemma 2 gives the same contradiction.  This excludes
every three-low diagram.

Combining Sections 1, 3, and 5 proves the central conclusion:

```text
number of low modes:                                      exactly two;
family distribution:                         one Phi_1, one Phi_2;
the two low modes:                                       distinct;
the other two modes:                    rank three under both families. (23)
```

## 6. The two surviving incidence branches

Let `a,b` be the two low modes and `s,t` the two high modes.  Lemma 1 gives
exactly two possibilities.

### 6.1 The zero branch

If the low supports are disjoint, then

```text
M_(st)=0.                                               (24)
```

Both high `A`-maps are nonzero, because a high projection in (5) has rank
three.  Nondegeneracy of `J` and (24) give

```text
rank A_s=rank A_t=1,
J(im A_s,im A_t)=0.                                    (25)
```

This branch includes the compatible same-missing pairs, for which the two
low supports are necessarily complementary singletons, and the disjoint
support cases for different missing colours.

### 6.2 The `E_22` branch

If the low lines have different missing colours and both actual supports
contain colour `2`, then

```text
M_(st)=mu E_22,                         mu!=0.          (26)
```

The rank-one-shore lemma gives the three preliminary rank possibilities

```text
(rank A_s,rank A_t) in {(1,1),(1,2),(2,1)},            (27)
```

with every rank-one shore supported only at colour `2`.

The pair `(1,1)` is impossible.  Indeed, both high `A`-maps then vanish on
their colour-`0,1` planes.  On the fourfold colour-`0,1` restriction, only
the two low modes can supply `x_4,x_5`.  Their common pairing bilinear form

```text
B=A_a^T J A_b
```

is independent of the diagonal channel.  A nonzero pure `d_0` tensor would
force `B` to be a nonzero multiple of `E_00`, while the pure `d_1` tensor
would force the same `B` to be a nonzero multiple of `E_11`.  This is
impossible.  Hence

```text
(rank A_s,rank A_t) in {(1,2),(2,1)}.                  (28)
```

Finally let `s` be the rank-one high shore.  It is supported only at colour
`2`.  Equation (26) confines the colour-`0,1` columns of the rank-two high
shore to the one orthogonal line to `im A_s`.  If both low modes also had
`A`-rank at most one on their colour-`0,1` columns, the colour-`0,1`
restriction would have one zero `A`-shore and three line shores.  Lemma 2
would contradict the two live diagonal tensors.  Therefore

```text
max(rank A_a|_{0,1}, rank A_b|_{0,1})=2.               (29)
```

Equations (24)--(29) are necessary conditions, not existence statements.

## 7. Exact rational incidence-only sharpness fixtures

The following fixtures show that neither final branch is eliminated by the
proved incidence, rank, and singleton-companion rules alone.  Coordinates
are ordered `(x_0,x_1,x_2,x_3,x_4,x_5)` and each row below lists the three
ordered local columns.

### 7.1 Zero-branch fixture

```text
L_2:
 (0,1,0,0,0,1), (1,0,0,1,0,0), (0,0,0,1,0,1)
L_3:
 (0,1,0,1,0,0), (1,0,0,0,0,1), (0,0,0,1,0,1)
L_4:
 (1,0,0,-1,0,0), (0,1,0,0,1,0), (0,0,0,1,1,0)
L_5:
 (1,0,0,0,1,0), (0,1,0,-1,0,0), (0,0,0,1,1,0).      (30)
```

Exact row reduction gives projection-rank pairs

```text
(2,3), (3,2), (3,3), (3,3).                           (31)
```

The lows are singleton `A_0` at colour `1` and singleton `A_1` at colour
`0`.  The high modes contain the forced companions `U_0=x_0-x_3` at colour
`0` and `U_1=x_1-x_3` at colour `1`, so both committed return cycles close.
All four `A`-ranks are one and `M_(45)=0`.  Every global colour nevertheless
has a nonzero same-colour `A` pairing.

### 7.2 `E_22`-branch fixture

```text
L_2:
 (2,1,0,2,1,0), (2,1,1,-2,0,1), (1,0,0,1,0,0)
L_3:
 (-2,0,0,0,0,1), (-1,0,-1,2,1,0), (0,1,0,1,0,0)
L_4:
 (1,0,0,-1,0,0), (0,1,0,-1,0,0), (-1,1,-2,2,1,0)
L_5:
 (1,0,0,0,1,0), (0,2,0,-2,1,0), (-1,-2,1,0,0,1).   (32)
```

The projection-rank pairs are again (31).  The lows are singleton `A_0`
and `A_1`, both at colour `2`.  Mode `L_4` contains both forced companions
`U_0` at colour `0` and `U_1` at colour `1`.  The four `A`-ranks are

```text
(2,2,1,2),
```

the ranks on colour-`0,1` columns are `(2,2,0,1)`, and

```text
M_(45)=E_22.                                           (33)
```

Thus this fixture meets the sharp boundaries (28)--(29).

Both fixtures are exact over `Q`, but neither satisfies (2).  In each case
direct polarization gives

```text
T_(m_1)(e_0,e_0,e_0,e_0)=-2!=0.                       (34)
```

They are countermodels only to an incidence-only or pigeonhole-only
closure, not counterexamples to permanent nonrestriction.

## 8. Exact scope and replay

```text
all same-mode cross-family lows:                         EXCLUDED BY PREDECESSORS;
common line N in a low mode:                             EXCLUDED;
all distinct-mode noncommon low pairs:                   CLASSIFIED;
four-low diagrams:                                       EXCLUDED;
three-low diagrams:                                      EXCLUDED;
low modes in every exact fixed-pair extension:            EXACTLY TWO;
family distribution:                                     ONE PER FAMILY;
other two modes:                                          HIGH IN BOTH;
zero high-pairing branch:                                 OPEN;
E_22 high-pairing branch:                                OPEN;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.   (35)
```

Replay the exact identities and finite case splits with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py
```

The primary verifier reconstructs the double-contraction table by exact
symbolic polarization, exhausts every noncommon line/support pair, checks
the three-low live-edge pigeonhole, exhausts the rank-one pairing boundary
over an odd finite field, and replays both rational fixtures.  The independent
audit imports neither the primary verifier nor SymPy: it rebuilds the
quartics as square-free monomial dictionaries, uses its own rational row
reduction and polarization code, independently repeats the finite support
classification, and checks the fixtures.  The computations replay displayed
algebra and finite case splits; the written characteristic-zero argument
proves the theorem.
