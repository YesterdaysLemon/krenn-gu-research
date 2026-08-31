# Four-root torus-star equal-leaf H4 Q6 all-zero coefficient branch exclusion (GLD103)

## Status and exact scope

**Proved exact scoped characteristic-zero theorem (GLD103).** The tracked
primary, independent audit, and clean-checkout replay prove the all-zero
coefficient branch below on `D(B*H2*Delta)` for symbolic arbitrary `a`.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

Let k be an algebraically closed field of characteristic zero. Use the
normalized GLD88/F88 equal-leaf H4 chart

    G = [1  1       1      ]
        [p  q       s      ],
        [a  1+b     1+c    ],

    s = (p+q-pq)/(p+q-1),
    b = b88(p,q,a) + B,
    c = c88(p,q,a) + C.

Let M(G) be the GLD71 37-by-9 syndrome matrix and let Q6(p,q) be the
written GLD88/F88 residual. Put

    H2 = 2*p^2-2*p+1,
    P  = p^2-p+1,
    Delta = (p-q)*(p+q-1)*P
            *(p^2+2*p*q-2*p-q)
            *(2*p*q-p+q^2-2*q)
            *(2*p*q^2-2*p*q-p-q^2-2*q+2).

Explicitly, the residual used here is

    Q6 = 2*p^4*q^2 - 2*p^4*q + p^4
         + 2*p^3*q^3 - 7*p^3*q^2 + 5*p^3*q - 2*p^3
         + 2*p^2*q^4 - 7*p^2*q^3 + 12*p^2*q^2 - 7*p^2*q + 2*p^2
         - 2*p*q^4 + 5*p*q^3 - 7*p*q^2 + 2*p*q
         + q^4 - 2*q^3 + 2*q^2.

The exact open is D(B*H2*Delta). The E31 wall/equation is not imposed or
inverted. The five selected actual 7-by-7 minors are:

| name | rows | columns |
| --- | --- | --- |
| T0 | (0,1,2,17,25,31,28) | (0,1,3,4,6,7,8) |
| T1 | (0,1,2,17,25,31,32) | (0,1,3,4,6,7,2) |
| T2 | (0,1,2,17,25,31,32) | (0,1,3,4,6,7,5) |
| Y1 | (0,1,17,28,31,32,33) | (0,1,3,4,5,6,7) |
| X3 | (0,1,17,28,31,32,33) | (0,1,2,3,4,6,7) |

The all-zero coefficient branch is

    G_T0 = G_T1 = G_T2 = G_Y1 = G_X3 = 0.              (A0)

## Theorem statement

The GLD103 target conclusion is the empty intersection

    { Q6=0 }
    intersect D(B*H2*Delta)
    intersect { rank M(G) <= 6 }
    intersect V(G_T0,G_T1,G_T2,G_Y1,G_X3)
    = empty.                                             (GLD103)

The statement is symbolic in arbitrary a; no specialization or inversion
of a is part of the theorem. It is an exclusion of this one coefficient
leaf, not a claim about the full H4 chart or the physical global incidence
variety.

## Reduction carried by the claim

After parameter-only exact denominator clearing in QQ(p,a)[q]/(Q6), each
selected minor has the affine-C form below.  No coefficient of a polynomial
in B is primitive-normalized independently of the other coefficients.  A
later fibre checker may divide one *whole* generator P_i(B) by one recorded
nonzero rational content; this is a uniform unit scaling and is checked by
exact reconstruction, not an unrecorded content cancellation.

    A_i(B,C) = F_i(B) + C*G_i(B),
    F_i(B) = B*f_i(B).

The first identity is exact in the cleared quotient; the second follows from
the GLD88 common-kernel identities at B=C=0. On D(B), set t=C/B:

    A_i = B*(f_i(B) + t*G_i(B)).

Define the ratio equations

    H_i(B,t) = f_i(B) + t*G_i(B).

The selected-minor equations therefore imply H_i=0 for all five selected
indices on D(B). For pairs define

    K_ij = F_i*G_j - F_j*G_i,
    Gamma_ij = K_ij/B
              = f_i*G_j - f_j*G_i.

Thus A_i=A_j=0 implies K_ij=Gamma_ij=0 on D(B). This is a one-way
rank/minor-to-coefficient bridge. Gamma vanishing, selected-minor
vanishing, and coefficient-determinant vanishing are not converses to
rank M<=6 or to the full physical incidence equations.

On (A0), the rank hypothesis supplies A_T0=0; because F_T0=B*P0 and B is
a unit, it gives P0=0. Set

    P0 = F_T0/B,
    P1 = G_T0,  P2 = G_T1,  P3 = G_T2,
    P4 = G_Y1,  P5 = G_X3.

Each P_i is quadratic in B (degree at most two). If

    P_i = k_i0 + k_i1*B + k_i2*B^2,

then the 6-by-3 coefficient matrix Kcoef=(k_ir) satisfies

    Kcoef*(1,B,B^2)^T = 0.

The vector is nonzero, so all `binomial(6,3)=20` maximal 3-by-3
coefficient/Fitting minors vanish.  The exact cover uses only the following
six necessary minors; the other fourteen are consequences at a branch point
but are not needed to compute the cover:

    D012, D013, D014, D015, D023, D123.                 (F)

This is only a necessary reduction. The six equations in (F) do not
reverse the rank bridge, and they are not the GLD83 pulled-back physical
Fitting ideal.

## Exact factor cover

The theorem uses the exact squarefree radical support of the necessary
p-only cover from Q6=0 and (F):

    p*(p-1)*P*H2*(p^2+1)*R4*R8*C4*F4
      *(p^2-2*p+2)*F40 = 0.                             (C)

The eleven factors are discharged, in scope, as follows:

| factor | exact treatment |
| --- | --- |
| p, p-1 | the exact nonzero-offset fibres handled by GLD102 |
| P=p^2-p+1 | outside the open because P divides Delta |
| H2=2*p^2-2*p+1 | outside the open; it is the q-leading/degree-drop gate |
| p^2+1, R4, R8, C4 | determinant-fibre Macaulay certificates |
| F4=5*p^4-4*p^3+12*p^2-16*p+8 | direct all-zero-branch localized Macaulay |
| p^2-2*p+2 | direct all-zero-branch localized Macaulay |
| F40 | quotient-gcd relation with a nonzero multiplication norm |

Here

    R4 = 5*p^4-16*p^3+30*p^2-16*p+5,
    C4 = 8*p^4-16*p^3+12*p^2-4*p+5,

and R8 and F40 are the exact pinned degree-eight and degree-40 residual
factors in the certificate package. The four determinant-fibre leaves
retain their Macaulay identities and fibre localizers. The F4 and
p^2-2*p+2 leaves use the localized ideal
`<Q6,P0,...,P5,z*B*Delta-1>` of the all-zero branch itself.  This is not the
GLD83 physical Fitting ideal, and no selected-minor converse is being
smuggled into the argument. The F40 leaf is the
exact quotient-gcd/nonzero-norm route; modular rank observations are not a
replacement for it.

Raw resultant multiplicities depend on the explicitly recorded
parameter-only clearing normalization and are not used as a theorem premise.
The clean-clone primary and audit must nevertheless report and reconcile
them.  Resultant degree-drop or infinity artifacts are harmless only because
every retained interior support factor receives its own direct exact fibre
certificate.

## Clearing-gate interpretation

The raw source records

    ClearingGate = P^23 * H2^45.

On D(H2*Delta), this gate is redundant: P|Delta, H2 is already inverted,
and all integer contents are characteristic-zero units. Hence the
computationally convenient localization

    D(B*H2*Delta*ClearingGate)

is exactly D(B*H2*Delta) for this claim. This does not extend the theorem to
Delta=0 or H2=0, and it does not authorize cancellation outside the
declared open.

## Explicit nonclaims

GLD103 does not claim any of the following:

* exclusion of the pivot branches where one of the five G_i is inverted;
* the B=0 endpoint or another C-open endpoint;
* the E31 wall/equation, whether imposed or inverted;
* Delta=0 or H2=0;
* any other chart, H4 component, source branch, root, or root order;
* a converse from selected minors, Gamma identities, or coefficient/Fitting
  determinants to rank M<=6;
* physical incidence or a global resolution of the Krenn--Gu conjecture.

The tracked exact primary, independent audit, clean-checkout replay, and
adversarial review establish only this scoped empty-set theorem.  They do not
change any nonclaim above or the global **UNRESOLVED** status.
