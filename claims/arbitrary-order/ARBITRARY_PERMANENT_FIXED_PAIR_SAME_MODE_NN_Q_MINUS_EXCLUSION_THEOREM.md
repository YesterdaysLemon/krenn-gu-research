# Arbitrary permanent fixed-pair same-mode `N/N`, `q_-` exclusion

## Status

This note closes one exact characteristic-zero branch of the proportional
same-mode common-line residual at the fixed equality-five pair.  Suppose a
remaining local plane contains the common exceptional line

```text
N=K(x_2+x_3)
```

as the restricted kernel line of both mixed-factor projections.  The exact
target equations propagate that incidence to a singleton companion in

```text
span{x_0+x_1,x_2-x_3}.
```

There are only two projective companion possibilities.  This note proves
that

```text
q_-=x_0+x_1-x_2+x_3
```

is impossible, for both singleton- and support-two-supported occurrences of
`N`.  The other possibility

```text
q_+=x_0+x_1
```

is **OPEN HERE**.  Thus this is a scoped branch exclusion, not an exclusion
of every same-mode `N/N` incidence.  It does not prove unrestricted
permanent nonrestriction.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

The proof uses only legal contractions: two different vectors from one
local plane are never inserted into two different tensor slots.  All fields
below have characteristic zero.

## 1. Fixed pair and predecessor inputs

Work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2)
```

and split

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5},
J((r_4,r_5),(s_4,s_5))=r_4s_5+r_5s_4.                 (1)
```

At the fixed equality-five pair the five complementary quartics are

```text
star(m_1)= x_4x_5 x_1(x_3-x_2-x_0),
star(m_2)= x_4x_5 x_0(x_3-x_2-x_1),
star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.                            (2)
```

For the four remaining ordered local triples assume the full target
equations

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (3)
```

Put

```text
h_0=-x_0+x_1+x_2+x_3,       h_1= x_0-x_1+x_2+x_3,
h_2= x_0-x_1-x_2+x_3,       h_2'=-x_0+x_1-x_2+x_3,
M=x_0+x_1,                   L=-x_0-x_1-x_2+x_3.       (4)
```

The kernel-support boundary theorem proves that a local occurrence of `N`
misses colour `2` and has support one or two.  The singleton propagation
theorem supplies the companion used below when that support is one.  For
support two, the short extension in Section 2 supplies the same companion.
The double-contraction incidence theorem supplies the rank-one pairing
background, but every use needed for the present exclusion is restated and
proved here.

## 2. The companion and its two projective branches

Contracting (2) with

```text
N=x_2+x_3
```

gives, after suppressing `x_4x_5`,

```text
m_1=m_2=d_2=0,          d_0=h_0,          d_1=h_1.    (5)
```

The common annihilator of the nonzero residual covectors is

```text
H_N=ann_R(h_0,h_1)=span{M,x_2-x_3}.                   (6)
```

### Lemma 1 (support-two `N` also propagates to `H_N`)

If `N` has local support `{0,1}`, another local plane contains a nonzero
vector `q` in `H_N`, and `q` is singleton-supported at colour `2`.

### Proof

Rescale the two active local columns so that

```text
N=y_(t,0)+y_(t,1).                                    (7)
```

Modulo `H_N`, equation (5) and the target give an `R/H_N`-valued cubic on
the other three local triples which is zero except at the `000` and `111`
cells, and is nonzero at both cells.  If all three local planes were
disjoint from `H_N`, their images in

```text
(R/H_N) direct-sum A
```

would still be three-dimensional.  Cross-colour zero slices have rank at
most one on the four-dimensional quotient ambient space, while a nonzero
`J`-scalar on its two-dimensional `R/H_N` summand would have rank two.  The
usual two-active-colour lemma therefore applies: every colour-2 `A` column
in those three modes is zero.  In the original pure `2222` coefficient,
only the removed mode could then supply an `A` factor.  A quartic with the
factor `x_4x_5` needs two distinct modes to supply the two `A` factors, so
that coefficient would vanish, contrary to `lambda_2!=0`.  Hence another
local plane meets `H_N`.

Let `0!=q` lie in that intersection.  Legally contracting (3) in the two
distinct modes containing `N` and `q`, equation (5) and `q in H_N` make the
entire left side zero.  The `d_0` and `d_1` right sides are nonzero scalar
multiples of the colour-0 and colour-1 coefficients of `q`, respectively.
Both coefficients therefore vanish.  Since the local triple is
independent, `q` is a nonzero multiple of its colour-2 column.  This proves
the lemma.

For singleton `N`, the same conclusion is exactly the common-line case of
the committed singleton propagation theorem.  Thus in both support cases
we may write, projectively,

```text
q=sM+u(x_2-x_3),                 s!=0,                 (8)
```

and `q` occurs at colour `2` in another local mode.  The inequality `s!=0`
also follows directly from the live `d_2` target: the `d_2` contraction in
(9) below would otherwise vanish.

Direct contraction gives

```text
m_1: sL-2u x_1,             m_2: sL-2u x_0,
d_0=d_1: (s+u)L,            d_2: -2sM.                (9)
```

The first four target contractions are zero and the last is nonzero.  If
`u!=0` and `s+u!=0`, the zero residuals span `L,x_0,x_1` and hence contain
the live residual `M`, a contradiction.  Consequently exactly two
projective possibilities survive:

```text
q_+=M                                      (u=0),
q_-=M-x_2+x_3                              (u=-s).     (10)
```

Only the second branch is treated below.

## 3. A quotient pair gate for `q_-`

For `q_-`, equation (9) becomes

```text
m_1=h_2',       m_2=h_2,       d_0=d_1=0,
d_2=-2M.                                                (11)
```

The three nonzero residuals span `N^perp`.  Put

```text
D=R/KN,                    W=D direct-sum A,
e=class(M) in D.                                          (12)
```

For `x,z,w in W`, with components `r(.) in D` and `a(.) in A`, define

```text
B_x(z,w)=r(z)J(a(x),a(w))+r(w)J(a(x),a(z))
                         +r(x)J(a(z),a(w)).              (13)
```

### Lemma 2 (zero/live pair gate)

Let `U,V` be three-dimensional subspaces of `W`.  Suppose `0!=u in W` and
`v in W` satisfy

```text
B_u|_(U,V)=0,
B_v|_(U,V)=e tensor rho tensor sigma !=0               (14)
```

for nonzero scalar covectors `rho on U` and `sigma on V`.  Then both
`A`-projection maps have rank one, and their coefficient rows are
proportional to `rho` and `sigma`:

```text
a(z)=rho(z)p,          a(w)=sigma(w)q                  (15)
```

after rescaling nonzero `p,q in A`.

### Proof

An `A`-rank-zero shore is impossible.  If, for example, `a(U)=0`, then
`U` is a three-dimensional copy of `D` and

```text
B_v(z,w)=r(z)J(a(v),a(w)).                              (16)
```

This either vanishes or has three-dimensional output, whereas (14) is
nonzero with one-dimensional output.  The same argument applies to `V`.

An `A`-rank-two shore is also impossible.  Suppose `a(U)=A`.  A nonzero
pure-`D` vector in `ker(a|V)`, inserted into `B_u=0`, first forces
`J(a(u),a(U))=0`, hence `a(u)=0`.  Then the nondegeneracy of `J`, the
surjectivity of `a(U)`, and the already-proved nonzero `A`-image of `V`
force `r(u)=0`.  This contradicts `u!=0`.  The other shore is symmetric.
Thus both ranks are one.

Write their rank-one factorizations as

```text
a(z)=alpha(z)p,         a(w)=beta(w)q.                 (17)
```

The kernels of `alpha` and `beta` are two-dimensional pure-`D` planes.
For `z in ker alpha`, equation (13) reads

```text
B_v(z,w)=r(z) beta(w) J(a(v),q).
```

The output-line condition in (14) forces `J(a(v),q)=0`; otherwise the
two-dimensional space `r(ker alpha)` would lie in `Ke`.  Symmetrically,
`J(a(v),p)=0`.  Hence

```text
B_v=r(v)J(p,q) alpha tensor beta.                      (18)
```

It is nonzero, so uniqueness of the two factor lines in a nonzero rank-one
bilinear form gives `alpha proportional rho` and
`beta proportional sigma`.  Rescaling `p,q` proves (15).

After contracting `q_-` at its colour-2 mode, take `u` to be any surviving
off-colour direction in the original `N` mode modulo `KN`, and take `v` to
be its colour-2 vector.  Equations (3) and (11) give exactly

```text
B_u(U,V)=0,
B_v(U,V)=nonzero multiple of e tensor e_2^* tensor e_2^*.
                                                               (19)
```

If neither of the last two local planes contains `N`, both images are
three-dimensional in `W`, so Lemma 2 says

```text
a(y_(U,0))=a(y_(U,1))=a(y_(V,0))=a(y_(V,1))=0.        (20)
```

The hypotheses `u!=0` and `dim U=dim V=3` are precisely where the
no-second-`N` condition is used.

## 4. Exclusion when there is no second `N`

### 4.1 Singleton original `N`

Suppose `N` is singleton-supported at colour `c in {0,1}`.  In the pure
colour-`c` coefficient, the `N` vector is pure `R`, and (20) makes the two
last-mode vectors pure `R`.  Only the `q_-` companion mode can have a
nonzero `A` part.  It is therefore impossible to supply both factors
`x_4,x_5` in any quartic (2).  The live `d_c` coefficient is zero, contrary
to `lambda_c!=0`.

### 4.2 Support-two original `N`

Normalize (7).  Because `N` is pure `R`,

```text
a(y_(t,1))=-a(y_(t,0)).                                (21)
```

In the all-colour-zero `d_0` coefficient, (20) leaves only the original
mode and the companion mode as possible `A` suppliers.  Replace the
original colour-0 vector by its colour-1 vector while leaving all other
slots at colour 0.  Any term using the original vector's `R` part still
has at most one `A` supplier and vanishes.  The only potentially nonzero
term pairs its `A` part with the companion-mode `A` part, and (21) changes
its sign.  Therefore

```text
T_(d_0)(1,0,0,0)=-T_(d_0)(0,0,0,0).                   (22)
```

The left side is an off-diagonal target entry and hence zero; the right
side is `-lambda_0`, which is nonzero.  This contradiction excludes the
support-two case.

For completeness, a support-two `N` cannot coexist with any second-mode
occurrence of `N`.  The legal double contraction `i_N i_N star(d_0)` and
`i_N i_N star(d_1)` is the same nonzero quadratic `2x_4x_5`.  If the second
`N` is singleton, one of the two target channels is nonzero and the other
zero; if it has support two, the same remaining pairing matrix would be a
nonzero multiple of both `E_00` and `E_11`.  Both alternatives are
impossible.  Thus Section 4.2 exhausts the support-two branch.

## 5. The collapsed second-singleton-`N` cycle

It remains to treat singleton original `N` when a second local plane also
contains `N`.  Equal singleton colours are impossible by the identical
nonzero double contractions just used.  A support-two second occurrence is
also impossible because one of its active coefficients meets the first
singleton colour and makes one channel live while the other remains zero.
After interchanging colours `0,1`, normalize distinct modes `a,c` by

```text
y_(a,0)=N,                  y_(c,1)=N.                 (23)
```

### 5.1 Companion in a third mode

First suppose `q_-=y_(b,2)` lies in a third mode `b`, and call the fourth
mode `d`.  Write `A_t` for the `2 by 3` matrix of `A`-projections in mode
`t`.  The legal double contraction in modes `a,c` has zero target in both
`d_0,d_1`, and (2) gives

```text
A_b^T J A_d=0,                  rank A_b+rank A_d<=2.   (24)
```

Neither rank can be zero.  For example, if `A_d=0`, contraction by `N` in
mode `a` makes the zero `d_1` cubic equal

```text
(A_b^T J A_c) tensor (h_1 R_d)=0,
```

while the live `d_0` cubic makes `A_b^T J A_c` nonzero.  Hence
`h_1R_d=0`.  Contracting by `N` in mode `c` then requires a live `d_1`
cubic with the same final factor `h_1R_d`, a contradiction.  The case
`A_b=0` is symmetric.  Therefore the two ranks in (24) are `(1,1)`.

Write

```text
A_b=p alpha^T,        A_d=q gamma^T,
J(p,q)=0,             alpha_2=0,                       (25)
```

where the last equality uses the pure-`R` companion `y_(b,2)=q_-`.  Define
coefficient rows

```text
beta_j    =J(p,A_c e_j),       delta_j  =J(A_c e_j,q),
pi_i      =J(A_a e_i,p),       epsilon_i=J(A_a e_i,q),
X=h_0R_b, Y=h_1R_b,            Z=h_0R_d, W=h_1R_d.     (26)
```

The two legal single contractions, in tensor orders `(b,c,d)` and
`(b,a,d)`, are exactly

```text
X tensor delta tensor gamma + alpha tensor beta tensor Z
  =lambda_0 e_0 tensor e_0 tensor e_0,
Y tensor delta tensor gamma + alpha tensor beta tensor W=0,

X tensor epsilon tensor gamma + alpha tensor pi tensor Z=0,
Y tensor epsilon tensor gamma + alpha tensor pi tensor W
  =lambda_1 e_1 tensor e_1 tensor e_1.                 (27)
```

Quotient the first tensor factor by `K alpha`.  Since `alpha_2=0`, if
`alpha` is proportional to neither `e_0` nor `e_1`, the first and fourth
equations have nonzero images and force `gamma` to be proportional to both
`e_0` and `e_1`, impossible.

If `alpha=e_1` after rescaling, (27) successively gives

```text
delta,gamma proportional e_0,       epsilon=0,
pi,W proportional e_1,              Z=0,
Y=0,                                beta=0.            (28)
```

If `alpha=e_0`, the colour-swapped deduction is

```text
epsilon,gamma proportional e_1,     delta=0,
beta,Z proportional e_0,            W=0,
X=0,                                pi=0.              (29)
```

In both cases `alpha_2=gamma_2=0`, so the colour-2 columns of `A_b,A_d`
vanish.  The final pairing argument must retain the correct case-dependent
zero rows.  In (28), `beta_2=epsilon_2=0`, hence

```text
A_c e_2 in p^perp=Kq,        A_a e_2 in q^perp=Kp.
```

In (29), `delta_2=pi_2=0`, and the two memberships are interchanged.  The
equalities of orthogonal lines hold because `A` is two-dimensional,
`J` is nondegenerate, `p,q` are nonzero, and `J(p,q)=0`; they also cover
the proportional isotropic case.  In either case

```text
J(A_a e_2,A_c e_2)=0.                                 (30)
```

Thus the only two modes that could supply the `A` factors in the pure
`2222` coefficient pair to zero, while the other two colour-2 columns have
no `A` part.  Every quartic in (2) has zero `2222` coefficient, contrary to
the live `d_2` target.

### 5.2 Companion in the second `N` mode

The only other possibility is that the second `N` mode itself contains

```text
N at colour 1,              q_- at colour 2.           (31)
```

Let `Theta` send a residual covector to the cubic tensor on the other three
legal slots.  Contracting `N` in this one mode gives

```text
Theta(h_0)=0,               Theta(h_1)!=0,
```

whereas contracting `q_-` in the same slot, in a separate legal
evaluation, gives

```text
Theta(h_2)=Theta(h_2')=0.
```

But the exact covector identity

```text
h_1=h_0+h_2-h_2'                                      (32)
```

forces `Theta(h_1)=0`, a contradiction.  This closes the coincident
companion case without ever inserting `N` and `q_-` into separate slots.

## 6. Theorem and exact boundary

### Theorem 3 (same-mode `N/N`, `q_-` exclusion)

Under (1)--(3), suppose one remaining local plane contains `N` as the
common restricted kernel line for both mixed-factor projections.  If the
companion forced by Section 2 is projectively

```text
q_-=x_0+x_1-x_2+x_3,
```

then the target equations have no solution.  This holds whether the
original `N` has singleton or support-two local support, and whether a
second singleton `N` occurrence is absent, lies in the companion mode, or
lies in a third mode.

Combining Sections 2--5 proves the theorem.  The exact scope is

```text
same-mode common kernel line N/N:                       ASSUMED;
singleton or support-two local support of N:           EXHAUSTIVE;
forced companion q_-:                                  EXCLUDED;
forced companion q_+:                                  OPEN HERE;
all same-mode N/N incidences:                          NOT EXCLUDED;
unrestricted P_6 -> Delta_3:                           UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.     (33)
```

## 7. Two discarded shortcuts

Two failed shortcuts are retained because they delimit the proof.

1. The equation `B_u(U,V)=0` alone does **not** force the desired ranks or
   support.  Exact abstract survivors exist.  Lemma 2 needs the simultaneous
   nonzero one-output-line equation for `B_v`.

2. `A`-rank one alone does **not** align the rank-one coefficient row with
   local colour `2`.  The alignment uses the full output-line condition and
   the two-dimensional pure-`D` kernels on both three-dimensional quotient
   shores.  When a second `N` collapses a quotient shore, that argument is
   unavailable; Section 5 uses the uncontracted diagonal slices instead.

Finite-field searches were useful hostile evidence for these corrections,
but no modular count is used as a characteristic-zero proof or as a case
cover.

## 8. Exact replay

Run

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_same_mode_nn_q_minus_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_same_mode_nn_q_minus_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_same_mode_nn_q_minus_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_same_mode_nn_q_minus_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_same_mode_nn_q_minus_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_same_mode_nn_q_minus_exclusion.py
```

The primary verifier reconstructs every contraction and residual span,
checks the no-second-`N` support split and factor-sign identity, replays the
zero/live pair-gate algebra, and compares all 108 entries of the four
rank-`(1,1)` tensors in (27) against a direct complete-polarization
evaluator.  It also checks both coordinate forks and the final colour-2
pairing.

The independent audit imports neither the primary verifier nor SymPy.  It
rebuilds the quartics from square-free edge dictionaries, uses its own
rational row reduction and polarization code, and replays the second-`N`
identities on an exact separating suite.  Its finite-field checks are
reported separately as stress evidence only.  The scripts replay the
displayed algebra; the written characteristic-zero argument proves the
theorem.
