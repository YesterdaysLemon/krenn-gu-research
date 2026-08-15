# Arbitrary permanent fixed-pair `A`-line-split rank-one-slice exclusion

## Status

This note proves an exact characteristic-zero exclusion inside the
simultaneous-low residual for the fixed equality-five pair.  Split the six
complement variables as

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},             A=span{x_4,x_5}.
```

If one of the four remaining local three-planes has zero projection to
`A` and each of the other three has one-dimensional projection to `A`, then
three nonzero rank-one fixed diagonal slices force at least two input-mode
flattening ranks to be at most two.  In particular, the resulting
`D^*`-valued sensor is not concise and cannot be locally equivalent to
`Delta_3`.

The proof does not use the two mixed-zero equations.  It therefore excludes
the entire indicated projection-rank family, including its simultaneous
mixed-zero sublocus.  It does not show that every simultaneous-low point has
this projection profile, does not classify the remaining rank-two
incidences, and does not normalize an arbitrary equality-five pair to the
fixed pair.  Unrestricted permanent nonrestriction remains unknown, and the
global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Fixed diagonal sensors

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

For the fixed pair, the three diagonal product classes have complementary
quartics

```text
star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.                              (1)
```

Write

```text
star(d_c)=x_4x_5 g_c,                    c=0,1,2,        (2)
```

where every `g_c` is a square-free quadratic in `R`.  Let
`L_2,...,L_5 subset K^6` be three-dimensional local spaces.  The restricted
four-linear tensor is

```text
T_c(y_2,y_3,y_4,y_5)
 =[x_0x_1x_2x_3x_4x_5]
   d_c y_2y_3y_4y_5.                                    (3)
```

Equivalently, (3) is the polarization of the complementary quartic
`star(d_c)` on the four inputs.  No bases of the `L_t` are fixed in the
statement.

Put `D=span{d_0,d_1,d_2}`.  The displayed classes are independent, and
`(d_0^*,d_1^*,d_2^*)` denotes their dual basis.

## 2. Statement

Let `pi_A:K^6 -> A` be the coordinate projection.  Assume that, after a
permutation of modes `2,3,4,5`,

```text
rank(pi_A|L_2)=rank(pi_A|L_3)=rank(pi_A|L_4)=1,
rank(pi_A|L_5)=0.                                      (4)
```

### Theorem 1 (`A`-line-split rank-one slices are nonconcise)

Suppose every tensor (3) is nonzero and decomposable:

```text
T_c=f_(2,c) tensor f_(3,c) tensor f_(4,c) tensor f_(5,c),
0!=f_(t,c) in L_t^*.                                   (5)
```

Then at least two modes `t in {2,3,4}` satisfy

```text
dim span{f_(t,0),f_(t,1),f_(t,2)} <= 2.                (6)
```

Equivalently, for the `D^*`-valued sensor

```text
S=sum_(c=0)^2 d_c^* tensor T_c,                         (7)
```

at least two input flattening ranks are at most two.  Hence `S` is not
input-concise and no action of `GL(L_2) x ... x GL(L_5)`, even together
with an arbitrary invertible output change on `D^*`, can turn it into
`Delta_3`.

The same conclusion holds if the two fixed mixed tensors are also required
to vanish; that extra hypothesis is simply unused.

## 3. Exact line-split factorization

For `y in K^6`, write

```text
y=r(y)+a(y),                 r(y) in R, a(y) in A.       (8)
```

On `A` put

```text
J((s_4,s_5),(t_4,t_5))=s_4t_5+s_5t_4.                  (9)
```

For a square-free quadratic `g in Z(R)_2`, define the symmetric bilinear
form

```text
G_g(r,r')=sum_(i<j) g_ij(r_i r'_j+r_j r'_i),            (10)
```

the polarization of `g`.

Condition (4) gives nonzero `u_t in A` and nonzero
`alpha_t in L_t^*` such that

```text
a(y)=alpha_t(y)u_t,                     t=2,3,4,         (11)
```

while `a(y)=0` on `L_5`.  Put `kappa_(st)=J(u_s,u_t)`.
Exactly two of modes `2,3,4` must supply `x_4,x_5` in (3).  Therefore, for
every square-free quadratic `g` and all local inputs,

```text
T_g(y_2,y_3,y_4,y_5)
 =kappa_23 alpha_2(y_2)alpha_3(y_3)G_g(r(y_4),r(y_5))
 +kappa_24 alpha_2(y_2)alpha_4(y_4)G_g(r(y_3),r(y_5))
 +kappa_34 alpha_3(y_3)alpha_4(y_4)G_g(r(y_2),r(y_5)).  (12)
```

This is a coefficient identity in the square-free algebra.  It requires no
genericity and remains valid when one or more `kappa` vanish.

## 4. One exceptional line factor per slice

Fix `c` and abbreviate the four factors in (5) by `f_t`.  For
`s in {2,3,4}`, restrict (12) to `ker(alpha_s)` in mode `s`.  Only the term
whose two `A`-supplying modes are the other two survives.  For example,

```text
T_c|_(ker(alpha_2) x L_3 x L_4 x L_5)
 =kappa_34 alpha_3 tensor alpha_4 tensor
   (G_(g_c)|_(r(ker alpha_2) x r(L_5))).                 (13)
```

There are two cases.

1. If `f_s|ker(alpha_s)=0`, then the two nonzero covectors `f_s` and
   `alpha_s` have the same kernel, so `f_s` is proportional to `alpha_s`.
2. If `f_s|ker(alpha_s)!=0`, the restricted pure tensor from (5) is
   nonzero.  Equation (13) and uniqueness of the factors of a nonzero pure
   tensor force the factors at the other two `A`-line modes to be
   proportional to their respective `alpha` covectors.

Consequently, for each fixed slice `c`, at most one of

```text
f_(2,c), f_(3,c), f_(4,c)                               (14)
```

fails to be proportional to the corresponding `alpha_t`.

Let `n_t` count the slices `c` for which `f_(t,c)` is not proportional to
`alpha_t`.  The preceding paragraph gives

```text
n_2+n_3+n_4 <= 3.                                       (15)
```

At least two of the three integers `n_t` are at most one.  At either such
mode, at least two of the three covectors `f_(t,c)` are proportional to the
same `alpha_t`, so their span has dimension at most two.  This proves (6).

Finally, the output directions `d_c^*` in (7) are independent and every
other factor in (5) is nonzero.  Thus the mode-`t` flattening rank of `S`
is exactly

```text
dim span{f_(t,0),f_(t,1),f_(t,2)}.                      (16)
```

The nonconciseness and `Delta_3` exclusion follow.

## 5. Exact rational fixtures and discovery boundary

The profile was isolated after a deterministic but **sampled** search
over `F_3`.  Its discovery ledger was:

```text
mixed-zero simultaneous-low quadruples inspected: 74,620
with D^*-output rank three:                            25
with all three fixed slices rank one:                   9
input-concise among those 25:                            5
input-concise and all three slices rank one:             0
```

The search sampled its first three local planes and was not an exhaustive
enumeration of all quadruples.  These counts are exploratory audit evidence,
not a proof, case cover, probability estimate, or characteristic-zero
statement.

All nine rank-one-slice hits admit the coefficientwise signed lift
`2 -> -1` to `Q`.  Direct exact replay gives, for every lift,

```text
both mixed tensors:                         zero;
D^*-output rank:                            3;
three fixed-slice multilinear ranks:        (1,1,1,1);
A-projection-rank multiset:                 {1,1,1,0};
input-flattening-rank multiset:             {3,2,1,1};
joint mixed-radical-dimension multiset:     {3,3,5,5}.   (17)
```

The two radical-five modes are exactly the two input-rank-one modes in
these nine fixtures.  For each such mode, the radical hyperplane has an
equation `x_4+x_5=0` or `x_4-x_5=0`.  These additional regularities are
properties of the nine sampled fixtures, not conclusions of Theorem 1.
The lifts are boundary witnesses for the need to distinguish output rank
and rank-one fixed slices from input conciseness; they are not
`Delta_3` restrictions.

The canonical compact-JSON encoding of the nine ordered `F_3` tuples used
by both replays has SHA-256

```text
b24836d1b7f47f7de00f045d15015b3568cf6a63958402c3d3c4d2b2765e19ad. (17a)
```

## 6. Exact scope and replay

```text
one A-zero mode plus three A-line modes:                  INCLUDED;
nonzero rank-one d_0,d_1,d_2 slices:                      ASSUMED;
at least two input flattening ranks <=2:                  PROVED;
mixed-zero equations:                                    NOT USED;
nine signed rational discovery fixtures:                 EXACT REPLAY;
74,620-point F_3 ledger:                                  SAMPLED ONLY;
other A-projection profiles:                              OPEN HERE;
general simultaneous-low residual:                       OPEN;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.   (18)
```

Replay with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_a_line_split_rank_one_slice_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_a_line_split_rank_one_slice_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_a_line_split_rank_one_slice_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_a_line_split_rank_one_slice_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_a_line_split_rank_one_slice_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_a_line_split_rank_one_slice_exclusion.py
```

The primary verifier checks (12) symbolically, exhausts the exceptional-mode
count, and replays the nine signed rational fixtures with exact arithmetic.
The independent audit imports neither the primary verifier nor SymPy.  It
checks the line-split factorization on every ambient basis tensor for all
projective `A`-line triples over `F_3`, independently exhausts the
exception pattern, and replays the integer fixture ledgers with a custom
row reducer.  These computations check identities and the fixture data;
the written argument proves Theorem 1.
