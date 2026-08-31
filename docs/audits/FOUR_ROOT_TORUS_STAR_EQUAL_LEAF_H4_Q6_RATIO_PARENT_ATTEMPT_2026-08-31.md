# GLD103 ratio parent attempt: the all-zero coefficient leaf

## Status and purpose

This is the serious parent-theorem attempt for the generic-a all-zero
coefficient branch. It is a proof-topology and obligation document, not a
promotion of a theorem. The global Krenn--Gu conjecture remains
**UNRESOLVED**.

The intended result is GLD103: an exact characteristic-zero exclusion on one
normalized GLD88/F88 H4 chart, with arbitrary symbolic a, Q6=0,
rank M <= 6, and the all-zero coefficient branch

    G_T0 = G_T1 = G_T2 = G_Y1 = G_X3 = 0.

The localizer is D(B*H2*Delta). At this checkpoint the primary and
arithmetic/audit material that motivated this document is still in ignored
research-run output. No clean-clone tracked primary-plus-independent-audit
package has landed, so the parent proposition below remains a candidate
obligation and the corresponding review must remain DRAFT/PENDING.

This attempt is load-bearing because the five nonzero-coefficient pivot
patches cover only the open sets D(G_i). Their complement is exactly the
all-zero leaf; omitting it leaves a genuine gap in the coefficient cover.

## 1. Exact parent proposition

Let k be an algebraically closed field of characteristic zero. On the
normalized GLD88/F88 equal-leaf H4 chart, let M(G) be the fixed 37-by-9
GLD71 syndrome matrix. The parent proposition under attack is

    Q6(p,q) = 0,
    rank M(G) <= 6,
    B*H2(p)*Delta(p,q) != 0,
    G_T0 = G_T1 = G_T2 = G_Y1 = G_X3 = 0
        => contradiction.                                      (GLD103)

The five G_i are coefficient polynomials obtained from five actual
denominator-cleared 7-by-7 minors. The assertion is pointwise over the
stated algebraically closed field, but every proposed certificate must be an
exact polynomial identity over QQ (with only the displayed open
denominators inverted) before scalar extension. This is a scoped branch
claim, not a statement about all charts, all H4 components, or the global
conjecture.

The selected actual minors are:

| name | rows of M(G) | columns of M(G) |
| --- | --- | --- |
| T0 | (0,1,2,17,25,31,28) | (0,1,3,4,6,7,8) |
| T1 | (0,1,2,17,25,31,32) | (0,1,3,4,6,7,2) |
| T2 | (0,1,2,17,25,31,32) | (0,1,3,4,6,7,5) |
| Y1 | (0,1,17,28,31,32,33) | (0,1,3,4,5,6,7) |
| X3 | (0,1,17,28,31,32,33) | (0,1,2,3,4,6,7) |

The rank hypothesis supplies vanishing of every actual 7-by-7 minor, hence
these five. That implication is one-way; vanishing of the five selected
minors is not asserted to imply rank M <= 6.

## 2. Chart, equations, and gates

Use the scale-fixed leaf

    G = [1  1       1      ]
        [p  q       s      ],
        [a  1+b     1+c    ],

    s = (p+q-pq)/(p+q-1).

The H4 relation is pq+ps+qs-p-q-s=0. Write the GLD88/F88 family as

    b = b88(p,q,a) + B,
    c = c88(p,q,a) + C.

The written family denominators are controlled by

    d0 = p+q-1,
    P  = p^2-p+1,
    L1 = p^2+2*p*q-2*p-q,
    L2 = 2*p*q-p+q^2-2*q,
    e  = 2*p*q^2-2*p*q-p-q^2-2*q+2,
    Delta = (p-q)*d0*P*L1*L2*e,
    H2 = 2*p^2-2*p+1.

The finite q-algebra uses the exact GLD88/F88 residual

    Q6 = 2*p^4*q^2 - 2*p^4*q + p^4
         + 2*p^3*q^3 - 7*p^3*q^2 + 5*p^3*q - 2*p^3
         + 2*p^2*q^4 - 7*p^2*q^3 + 12*p^2*q^2 - 7*p^2*q + 2*p^2
         - 2*p*q^4 + 5*p*q^3 - 7*p*q^2 + 2*p*q
         + q^4 - 2*q^3 + 2*q^2.

The theorem target is the open D(B*H2*Delta). The E31 wall/equation is
neither imposed nor inverted in this attempt.

The raw minors are cleared only by parameter-only denominators, with no
independent primitive normalization of their B-coefficients and no
unrecorded content cancellation.  A later local-fibre calculation may divide
one complete P_i(B) by one recorded nonzero rational content; that uniform
whole-generator unit scaling is checked by exact reconstruction. In the
all-pairs source the bookkeeping localizer is

    ClearingGate = P^23 * H2^45.

It is redundant on the theorem open: P divides the displayed Delta, so P
is a unit on D(Delta), and H2 is already a unit on D(H2). Integer contents
introduced by exact clearing are units in characteristic zero. Thus

    D(B*H2*Delta*ClearingGate) = D(B*H2*Delta)

for this characteristic-zero statement. This simplification is only an
open-set equality; it does not authorize cancellation outside the stated
D(H2*Delta) domain or removal of a genuine chart denominator.

## 3. Ratio reduction and the Gamma identity

For each selected minor, let A_i be its exact parameter-cleared polynomial
in the quotient QQ(p,a)[q]/(Q6). The raw c-degree calculation and the
GLD88 common-kernel identities give

    A_i(B,C) = F_i(B) + C*G_i(B),
    F_i(0) = 0,
    F_i(B) = B*f_i(B).

On D(B), use the physical ratio

    t = C/B.

Then every selected equation has the common-factor form

    A_i = B*(f_i(B) + t*G_i(B)).

Write the ratio equations as

    H_i(B,t) = f_i(B) + t*G_i(B).

Thus an actual selected-minor zero on D(B) gives H_i=0 for every selected
index i. This is the parent mechanism being synthesized: it puts all five
selected equations in one ratio system instead of treating five unrelated
coefficient inversions as a theorem.

For any pair i,j, define the exact cross-polynomial and its B-divided
version by

    K_ij       = F_i*G_j - F_j*G_i,
    Gamma_ij   = K_ij/B
               = f_i*G_j - f_j*G_i.

The identity K_ij = B*Gamma_ij is polynomial because every F_i is divisible
by B. If the two actual equations vanish, then

    A_i = A_j = 0  =>  K_ij = 0  =>  Gamma_ij = 0 on D(B).

This is the Gamma identity used in the coefficient reduction. It is a
necessary consequence of the common ratio equations, not a converse:
Gamma_ij=0 does not reconstruct A_i=A_j=0, does not reconstruct t, and does
not imply the full syndrome rank condition. In particular, the all-zero
coefficient branch must not be replaced by an unjustified specialization
C=0.

## 4. All-zero coefficient/Fitting reduction

On the complementary branch

    G_T0 = G_T1 = G_T2 = G_Y1 = G_X3 = 0,

the rank-to-minor bridge gives A_T0=0. Since A_T0=F_T0 on this branch and
B is a unit, the exact factorization

    F_T0 = B*P0

gives P0=0. Set

    P0 = F_T0/B,
    P1 = G_T0,
    P2 = G_T1,
    P3 = G_T2,
    P4 = G_Y1,
    P5 = G_X3.

Each P_i is a polynomial of B-degree at most two. Write

    P_i = k_i0 + k_i1*B + k_i2*B^2,

and let Kcoef be the resulting 6-by-3 coefficient matrix. At a point of
the all-zero branch,

    Kcoef * (1, B, B^2)^T = 0.

The vector is nonzero because its first coordinate is one. Consequently all
`binomial(6,3)=20` maximal 3-by-3 row minors in the coefficient/Fitting ideal
vanish. The tracked cover needs only the six exact minors

    D012, D013, D014, D015, D023, D123,

where the subscripts record the corresponding row triples of Kcoef. This is
a one-way reduction from the physical rank hypothesis to a necessary
coefficient/Fitting locus. It is not a converse from the six determinants
back to a rank-at-most-six point, and it is not the GLD83 pulled-back
physical Fitting ideal.

The coefficient split is exhaustive:

    one of the five G_i is nonzero
        (a pivot patch D(G_i)),
    or all five G_i vanish
        (the present leaf).

The first alternative is outside this document. The second alternative is
therefore not an optional refinement; it is the exact complement of the
pivot cover.

## 5. Exact eleven-factor cover and proposed leaf routes

The theorem-relevant part of the exact p-only cover to be discharged from
Q6=D012=D013=D014=D015=D023=D123=0 is its squarefree radical support:

    p*(p-1)*P*H2*(p^2+1)*R4*R8*C4*F4
      *(p^2-2*p+2)*F40 = 0.                         (1)

Raw cover multiplicities can change with recorded parameter-only clearing
scalars.  They must be reported and reconciled by the durable primary and
audit, but they are not used to delete or add a squarefree support factor.
The factors and their intended exact routes are:

| factor | route and scope |
| --- | --- |
| p | the exact p=0 nonzero-offset fibre supplied by GLD102 |
| p-1 | the exact p=1 nonzero-offset fibre supplied by GLD102 |
| P=p^2-p+1 | outside D(Delta), since P divides Delta |
| H2=2*p^2-2*p+1 | outside D(H2); it is the q-leading/degree-drop gate |
| p^2+1 | determinant-fibre Macaulay certificate |
| R4=5*p^4-16*p^3+30*p^2-16*p+5 | determinant-fibre Macaulay certificate |
| R8 | determinant-fibre Macaulay certificate |
| C4=8*p^4-16*p^3+12*p^2-4*p+5 | determinant-fibre Macaulay certificate |
| F4=5*p^4-4*p^3+12*p^2-16*p+8 | direct all-zero-branch localized Macaulay certificate |
| p^2-2*p+2 | direct all-zero-branch localized Macaulay certificate |
| F40 | quotient-gcd identity and nonzero multiplication norm |

Here R8 is the exact degree-eight residual factor pinned by the
determinant-fibre calculation, and F40 is the exact degree-40 residual
factor, not a numerical factor sampled at finitely many p-values. The four
determinant-fibre routes (C4, R8, p^2+1, R4) must retain their Macaulay
identities and their fibre localizers. The F4 and p^2-2*p+2 leaves use the
localized ideal `<Q6,P0,...,P5,z*B*Delta-1>` of the all-zero branch itself,
rather than silently replacing it by a selected-minor converse or calling it
the GLD83 physical Fitting ideal.

For F40, the intended exact quotient-algebra leaf is an unnormalized
relation of the form

    u134*D134 + u145*D145 = c

in k[q]/(Q6)[a] over k = QQ[p]/(F40), followed by the exact nonzero
multiplication norm of c down to QQ. This is a quotient-gcd certificate,
not a claim based on a modular rank count. The relation, norm, and all
source identities still need a durable tracked primary and an independently
derived audit before they can be called proof evidence.

For reproducibility, a promoting full replay must explicitly set the neutral
arithmetic controls `GLD103_FACTOR_MATRIX_INVERSE=1` and
`GLD103_FACTOR_NO_FINAL_INVERSE=1`.  The certificate records both effective
values and whether they came from those environment variables; a run that
silently relies on their defaults is diagnostic rather than the pinned
publication replay.

## 6. Adversarial controls and neutral computation

The sharp control for this parent attempt is the nonconverse boundary:

* rank M <= 6 implies every actual 7-by-7 minor vanishes;
* the five selected minor equations, the Gamma equations, or the six
  coefficient determinants do not imply rank M <= 6;
* the coefficient branch G_i=0 is not the endpoint B=C=0;
* the ratio t=C/B exists only on the declared B-open;
* a resultant factor cover is a necessary support cover until every factor
  fibre has its own exact contradiction.

A modular subset-lift/RREF attempt at the degree-40 leaf timed out without a
verdict. That **neutral modular timeout** is neither positive evidence nor a
mathematical obstruction; it cannot be used to promote or reject GLD103.
The proposed F40 route is the exact quotient-gcd/nonzero-norm route above.

The exact branch is load-bearing for the parent theorem. A proof of only the
five D(G_i) pivot patches would cover the open union
D(G_T0) union ... union D(G_X3) and would say nothing on its complement.
The all-zero coefficient/Fitting reduction is the mechanism that makes that
complement finite and exposes the eleven-factor cover. It is consequently
the next parent-level obligation, not a cosmetic third sibling.

## 7. Scope fences

Even a successful GLD103 leaf would not claim:

* any pivot branch where a G_i is inverted;
* the B=0 endpoint or any C-open endpoint argument;
* the E31 wall or equation, whether imposed or inverted;
* Delta=0 or H2=0;
* another normalized chart, H4 component, source branch, root, or root order;
* the GLD83 physical pulled-back Fitting ideal unless separately supplied;
* a converse from selected minors, coefficient determinants, or Gamma
  identities to physical incidence or full rank;
* physical incidence/global resolution or a global Krenn--Gu resolution.

The parent-attempt proof-topology delta is therefore conditional: it
identifies the all-zero leaf and its exact load-bearing subobligations, but
it does not change the live global frontier by itself.
