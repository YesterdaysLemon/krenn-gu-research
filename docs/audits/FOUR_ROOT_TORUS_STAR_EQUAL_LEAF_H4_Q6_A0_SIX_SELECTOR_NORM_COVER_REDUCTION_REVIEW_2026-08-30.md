# GLD101 a=0 six-selector norm-cover reduction hostile review

## Verdict

**Verdict: PASS for the exact GLD101 norm-cover reduction.**  The tracked
primary and independent direct-matrix audit establish the necessary
degree-548 norm and its exact eight-factor p-support on the stated
normalized characteristic-zero open.  The owner document may carry the
status **Proved exact scoped characteristic-zero norm-cover reduction
(GLD101)**.

**Do not promote offset exclusion.**  The p0/p1, d2, d4, d8, and R110
B/C closures are ignored external evidence.  The tracked certificate
manifest carries their pins and replay guards, but not their polynomial
identities.  They therefore do not justify B=C=0 here.  No physical
empty-set corollary is claimed, and the global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Exact claim audited

On the normalized GLD88/F88 equal-leaf H4 offset chart, with a=0, the
audited statement is

~~~text
V(a,Q6) intersect D(H2*Delta) intersect {rank M(G) <= 6}
  intersect {(B,C) != (0,0)}
    is contained in {N6(p)=0}
    is contained in V((p-1)*p*(p^2+1)*P*H2*R4*R8*R110).
~~~

The second containment is the exact radical support of the primitive
degree-548 norm numerator.  This is a necessary reduction only.  It is not
an assertion that any listed support is a real selector root, a rank point,
or a physical incidence point.

The scope is characteristic zero, pointwise over the complex numbers,
a=0, the GLD88 chart gates, and D(H2*Delta).  H2=0 and Delta=0 are outside
this reduction.  The full E31=0 wall, arbitrary a, other charts, and every
physical downstream obligation are outside scope.

## 1. One-way rank-to-selector bridge

The six generators are actual direct seven-by-seven minors of the
37-by-9 GLD71 syndrome:

~~~text
T0 = det M[(0,1,2,17,25,31,28), (0,1,3,4,6,7,8)],
T1 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,2)],
T2 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,5)],
T3 = det M[(0,1,2,17,25,31,33), (0,1,3,4,6,7,8)],
Y1 = det M[(0,1,17,28,31,32,33), (0,1,3,4,5,6,7)],
X3 = det M[(0,1,17,28,31,32,33), (0,1,2,3,4,6,7)].
~~~

Rank at most six makes these selected minors vanish.  After a=0 and Q6
reduction, their offset support is

~~~text
m = (C, B, BC, B^2, B^2C, B^3)^T.
~~~

At a nonzero offset m is nonzero because its first two coordinates are C
and B.  Consequently the coefficient matrix has a nontrivial kernel and
its determinant vanishes in the Q6 quotient.  This bridge is one-way:

* the six minors do not generate or characterize the full rank ideal;
* selector or norm vanishing is not sufficient for rank; and
* no physical statement follows from the norm alone.

The bridge does not assume B and C are separately nonzero.

## 2. Exact arithmetic and gates

The normalized chart is

~~~text
G = [1  1       1      ]
    [p  q       s      ]
    [a  1+b     1+c    ],

s = (p+q-pq)/(p+q-1),
b = b88(p,q,a)+B,
c = c88(p,q,a)+C.
~~~

With

~~~text
d0 = p+q-1
P  = p^2-p+1
L1 = p^2+2pq-2p-q
L2 = 2pq-p+q^2-2q
e  = 2pq^2-2pq-p-q^2-2q+2
Delta = (p-q)d0 P L1 L2 e,
H2 = 2p^2-2p+1,
~~~

the q-degree-four Q6 relation is the canonical GLD96 relation.  The
quotient leading coefficient is H2, and the six-selector bookkeeping
retains the H2^36 clearing gate.  The primary and audit enforce the
upstream open D(H2*Delta) together with the named GLD88 pivot/chart gates;
they do not silently divide through H2 or Delta.

The exact six-selector norm has degree 548 and 451 p terms.  Its numerator
SHA256 is

~~~text
582f782b1fb1a1824e5d22d8374f52cb25075aab1372f7d06b9607269add79e3
~~~

and the Q6 srepr SHA256 is

~~~text
2ed58764e7c50c8e1510a93b32d2515a9297c03dfe297fed8d9abe5f8e9d71a7
~~~

Up to a nonzero rational unit, the exact factorization is

~~~text
N6(p) =
  (p-1)^36 * p^98 * (p^2+1)^2 * P^43 * H2^99
  * R4^2 * R8 * R110,

R4 = 5p^4-16p^3+30p^2-16p+5,
R8 = 64p^8-256p^7+580p^6-844p^5+946p^4
     -784p^3+388p^2-94p+13,
deg(R110) = 110.
~~~

The factor signature is checked by both tracked arithmetic routes and by
the tracked certificate manifest.  The R110 polynomial is identified by
its exact factor hash in that manifest, not by a finite-field factor list.

## 3. Independent tracked evidence

The primary is

~~~text
claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_six_selector_norm_cover.py
SHA256 BEBAACE6ACB6166E2E18B41D4921CE06CC5178D65A85E04459BC87CDDE3D0346
~~~

It reconstructs the authoritative sparse GLD71 rows, the GLD88 chart, the
six actual minors, the selector determinant, the exact q-norm, the
factor signatures, and the Delta resultant.

The independent audit is

~~~text
claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_six_selector_norm_cover.py
SHA256 09356BD0F3DFB9BEFCED9EBACF3A11711BA4738D33EFC2DADB79ADB1944D42D7
~~~

It does not import the GLD88 verifier or the GLD101 primary.  It locally
transcribes the a=0 chart, rebuilds the direct 37-by-9 matrix, computes the
six minors through a separate matrix-determinant route, and checks the
same norm and factor signatures.

The certificate manifest consumed by both is

~~~text
claims/arbitrary-order/certificates/GLD101_A0_NORM_COVER_CERTIFICATE.json
SHA256 9213A50F96BF6BFFA7A8F8FEFBD8CCA99317F00A1B1863B19E83D1330F79518E
~~~

The manifest's mathematical scope says explicitly that the bridge is
necessary on the nonzero-offset chart, that a norm root is not a physical
rank point, and that ignored solver evidence is not promoted to QQ ideal
membership.

## 4. External factor leaves are not offset closure

The factorization displays eight supports:

| support | treatment in this theorem |
| --- | --- |
| p=0 | retained necessary support; ignored p0/p1 closure is not composed |
| p=1 | retained necessary support; ignored p0/p1 closure is not composed |
| P=0 | a Delta factor and outside D(Delta) |
| H2=0 | outside D(H2); GLD99 is a separate theorem, not silently composed |
| p^2+1=0 | retained support; ignored d2 B/C replays are external |
| R4=0 | retained support; ignored d4 B/C replays are external |
| R8=0 | retained support; ignored d8 B/C replays are external |
| R110=0 | retained support; ignored R110 B/C replays are external |

The ignored external sources include the p0/p1 package, the d2/d4/d8
characteristic-zero B/C Singular sources, and the R110 guarded
q-substitution sources.  Their existence, successful logs, or pins do not
turn the norm reduction into B=C=0.

For provenance, the R110 manifest records:

~~~text
B source SHA256 4ee47062fff4aad750a7dbc543d6d6a65ffbf1dd31feeba5a6ae17229fff6b53
B run          e31-r110-qsubst-B-certificate-hardcheck-v1
B run JSON     75a266666f316ca63a0bf588193cfea622de3f6bd5fb7315d1623e908d316981
B log          8c43caed052017bcd70460544ea7c3a89bc387c5229f937d3b5186d6a8a2b44f
C source SHA256 cadce91edd79cbe287e0c2a19713154996aa09659d40f104711404eb57b75b38
C run          e31-r110-qsubst-C-certificate-hardcheck-v3
C run JSON     d4f19caa7d0510a9c2d1325688e4e15b1dda5b4ded1b3ef05e15235bae828ad2
C log          8c43caed052017bcd70460544ea7c3a89bc387c5229f937d3b5186d6a8a2b44f
~~~

The R110 hardchecks are pinned Singular replays and are not independent
derivations of their large generated sources.  They are deliberately
retained as external provenance only.

## 5. Nonclaims and downstream boundary

GLD101 does not claim:

* B=C=0 on any norm-factor fibre;
* exact offset identities from the ignored p0/p1, d2, d4, d8, or R110
  sources;
* closure of the full E31=0 wall or an arbitrary-a theorem;
* a converse from selectors or norms to syndrome rank;
* a conclusion on H2=0, Delta=0, another chart, gauge, component, source
  branch, profile, root, or order;
* any physical incidence empty-set statement or composition with C_8=1,
  the GLD75/GLD86 bridge, D(Omega), or GLD95;
* a positive-characteristic theorem from modular scouting;
* Fitting-ideal emptiness, source integrability, graph lifting, target
  attachment, global gluing, or global resolution; or
* a refutation or resolution of the global Krenn--Gu conjecture.

The accepted result is exactly the necessary norm-cover reduction on
D(H2*Delta), with its one-way bridge and explicit gates.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.
