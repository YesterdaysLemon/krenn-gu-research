# Four-root torus-star equal-leaf H4 Q6 a=0 six-selector norm-cover reduction (GLD101)

## Status and exact scope

**Proved exact scoped characteristic-zero norm-cover reduction (GLD101).**

Let U88 be the normalized GLD88/F88 equal-leaf H4 offset chart, with
the GLD88 chart denominators retained.  The exact statement established by
the tracked primary verifier and its independent direct-matrix audit is

~~~text
V(a,Q6) intersect D(H2*Delta) intersect {rank M(G) <= 6}
  intersect {(B,C) != (0,0)}
    is contained in {N6(p)=0}
    is contained in V((p-1)*p*(p^2+1)*P*H2*R4*R8*R110).
~~~

The second containment is the radical support of the exact primitive
degree-548 norm numerator.  Thus, on the stated open, a full syndrome
rank-at-most-six point with nonzero offset forces p onto one of the eight
listed factor supports.

This theorem stops at that necessary norm-cover reduction.  It does not
prove B=C=0, because the factor-by-factor offset closures are ignored
external evidence and the tracked GLD101 manifest carries their pins but
does not carry the corresponding polynomial identities.  There is no
physical empty-set corollary in this document.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

The statement is characteristic zero and pointwise over the complex
numbers.  It fixes a=0; it is not generic in a.  It is restricted to
D(H2*Delta) and the named GLD88 chart gates.  The H2=0 fibre, Delta=0,
the full E31=0 wall, and all physical downstream obligations remain
separate.

## 1. Normalized chart and gates

Use the scale-fixed equal-leaf chart

~~~text
G = [1  1       1      ]
    [p  q       s      ]
    [a  1+b     1+c    ],

s = (p+q-pq)/(p+q-1).
~~~

The H4 relation is pq+ps+qs-p-q-s=0.  Put

~~~text
d0 = p+q-1
P  = p^2-p+1
L1 = p^2+2pq-2p-q
L2 = 2pq-p+q^2-2q
e  = 2pq^2-2pq-p-q^2-2q+2
Delta = (p-q)d0 P L1 L2 e.
~~~

The offsets are defined by the GLD88/F88 rational functions

~~~text
b = b88(p,q,a) + B,
c = c88(p,q,a) + C.
~~~

Here C is the leaf offset.  It is distinct from the incidence-center
coordinate C_8 used in other bridge statements.  The q-degree-four
polynomial is

~~~text
Q6 = 2p^4q^2-2p^4q+p^4
     +2p^3q^3-7p^3q^2+5p^3q-2p^3
     +2p^2q^4-7p^2q^3+12p^2q^2-7p^2q+2p^2
     -2pq^4+5pq^3-7pq^2+2pq+q^4-2q^3+2q^2.
~~~

Its q-leading coefficient is

~~~text
H2 = 2p^2-2p+1.
~~~

The quotient calculation and its denominator clearing use the explicit
H2^36 gate.  No q-quotient argument in GLD101 is extended over H2=0.
The chart and denominator open is therefore D(H2*Delta), with the
GLD88 pivot/chart conditions included.

## 2. Six actual necessary seven-minors

Let M(G) be the complete 37-by-9 GLD71 syndrome.  The six selectors are
actual direct seven-by-seven minors:

~~~text
T0 = det M[(0,1,2,17,25,31,28), (0,1,3,4,6,7,8)],
T1 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,2)],
T2 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,5)],
T3 = det M[(0,1,2,17,25,31,33), (0,1,3,4,6,7,8)],
Y1 = det M[(0,1,17,28,31,32,33), (0,1,3,4,5,6,7)],
X3 = det M[(0,1,17,28,31,32,33), (0,1,2,3,4,6,7)].
~~~

The row and column order is part of each generator definition.  A
syndrome rank bound of six implies that all six displayed minors vanish.
No converse is used, and these six minors are not claimed to generate the
full rank-at-most-six ideal.

After setting a=0, substituting the GLD88 offsets, and reducing q
coefficients modulo Q6, the six minors have no constant offset term and
are supported on

~~~text
m = (C, B, BC, B^2, B^2C, B^3)^T.
~~~

Write the six equations as K(p,q)m=0 in the Q6 quotient.  If
(B,C) != (0,0), then m is nonzero because its first two entries are C and
B.  Therefore K has a nontrivial kernel and det K(p,q)=0 at every such
rank point.  This is the complete bridge used by GLD101: rank implies
selected minors, and a nonzero offset implies the selector determinant.
There is no reverse implication from selectors or norms to rank.

## 3. Exact norm and factorization

On D(H2), take the q-norm of det K in Q(p)[q]/(Q6), clear the recorded
H2^36 q-reduction denominator, and take the primitive p numerator.  The
tracked primary and independent audit both recompute the same exact
degree-548 norm with 451 p terms:

~~~text
N6 numerator SHA256 =
  582f782b1fb1a1824e5d22d8374f52cb25075aab1372f7d06b9607269add79e3
Q6 srepr SHA256 =
  2ed58764e7c50c8e1510a93b32d2515a9297c03dfe297fed8d9abe5f8e9d71a7
support-row digest =
  c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0
~~~

Up to a nonzero rational unit, the exact primitive factorization is

~~~text
N6(p) =
  (p-1)^36 * p^98 * (p^2+1)^2 * P^43 * H2^99
  * R4^2 * R8 * R110,

R4 = 5p^4-16p^3+30p^2-16p+5,
R8 = 64p^8-256p^7+580p^6-844p^5+946p^4
     -784p^3+388p^2-94p+13,
deg(R110) = 110.
~~~

The degree-110 factor is pinned by its exact factor signature in the
tracked certificate manifest; it is not admitted from a finite-field
factor list.

The tracked evidence surface is:

~~~text
primary:
  claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_six_selector_norm_cover.py
  SHA256 BEBAACE6ACB6166E2E18B41D4921CE06CC5178D65A85E04459BC87CDDE3D0346
independent audit:
  claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_six_selector_norm_cover.py
  SHA256 09356BD0F3DFB9BEFCED9EBACF3A11711BA4738D33EFC2DADB79ADB1944D42D7
certificate manifest:
  claims/arbitrary-order/certificates/GLD101_A0_NORM_COVER_CERTIFICATE.json
  SHA256 9213A50F96BF6BFFA7A8F8FEFBD8CCA99317F00A1B1863B19E83D1330F79518E
~~~

The primary reconstructs the sparse GLD71 rows and selected actual minors.
The independent audit transcribes the a=0 chart, rebuilds the direct
37-by-9 matrix, and uses a separate determinant route.  Both verify the
norm and its exact factor signatures.  This independent verification is
for the necessary norm-cover reduction only.

## 4. Meaning of the eight supports

The norm proves a necessary case cover, not a closure of those cases:

| support | role in GLD101 |
| --- | --- |
| p=0 | retained norm support; the ignored p0/p1 package is not part of this theorem |
| p=1 | retained norm support; the ignored p0/p1 package is not part of this theorem |
| P=p^2-p+1=0 | a factor of Delta, hence outside D(Delta) |
| H2=0 | outside the norm open; GLD99 is a separate exact degree-drop theorem |
| p^2+1=0 | retained support; ignored d2 offset replays are not composed |
| R4=0 | retained support; ignored d4 offset replays are not composed |
| R8=0 | retained support; ignored d8 offset replays are not composed |
| R110=0 | retained support; ignored R110 offset replays are not composed |

The first, second, and last five rows are deliberately not promoted to
B=C=0 conclusions here.  A factor root may be extraneous as a norm root,
and even a genuine selector root is only a necessary over-approximation of
a physical rank point.

## 5. External replay pins and provenance boundary

The certificate manifest records ignored external replay pins for possible
future offset-closure work.  They are not identities in the tracked
GLD101 certificate and are not used to establish the theorem above.

The p0/p1 package is
.research-runs/e31_p0_p1_exact_audit_v10.json with SHA256
1D6BD26F22B875A6A024E8C9D357E4CC5C862EFC66E61371DC22B98EC10AAF9F.
The ignored d2, d4, and d8 B/C sources are:

~~~text
.research-runs/e31_a0_fibre_d2_fae3e839d66d_B_char0.sing
.research-runs/e31_a0_fibre_d2_fae3e839d66d_C_char0.sing
.research-runs/e31_a0_fibre_d4_59d876136007_B_char0.sing
.research-runs/e31_a0_fibre_d4_59d876136007_C_char0.sing
.research-runs/e31_a0_fibre_d8_19e8048b6aa1_B_char0.sing
.research-runs/e31_a0_fibre_d8_19e8048b6aa1_C_char0.sing
~~~

The manifest also records guarded R110 q-substitution pins:

~~~text
B chart source:
  .research-runs/e31_r110_qsubst_B_certificate_hardcheck_v1.sing
  source SHA256 4ee47062fff4aad750a7dbc543d6d6a65ffbf1dd31feeba5a6ae17229fff6b53
  run e31-r110-qsubst-B-certificate-hardcheck-v1
  run JSON SHA256 75a266666f316ca63a0bf588193cfea622de3f6bd5fb7315d1623e908d316981
  log SHA256 8c43caed052017bcd70460544ea7c3a89bc387c5229f937d3b5186d6a8a2b44f
C chart source:
  .research-runs/e31_r110_qsubst_C_certificate_hardcheck_v1.sing
  source SHA256 cadce91edd79cbe287e0c2a19713154996aa09659d40f104711404eb57b75b38
  run e31-r110-qsubst-C-certificate-hardcheck-v3
  run JSON SHA256 d4f19caa7d0510a9c2d1325688e4e15b1dda5b4ded1b3ef05e15235bae828ad2
  log SHA256 8c43caed052017bcd70460544ea7c3a89bc387c5229f937d3b5186d6a8a2b44f
~~~

These R110 artifacts are pinned Singular replays, not an independent
derivation of their large generated sources.  Their chart inverses are
z*B-1 and z*C-1.  The tracked manifest records the hard guards and the
pins as external evidence; it does not import their offset identities into
the norm-cover theorem.

## 6. Nonclaims and downstream boundary

GLD101 does not claim:

* B=C=0 on any of the eight factor supports;
* an exact offset-closure theorem from the ignored p0/p1, d2, d4, d8, or
  R110 runs;
* an arbitrary-a theorem or closure of the full E31=0 wall;
* a converse from the six selectors or their norm to syndrome rank;
* a conclusion on H2=0, Delta=0, Omega=0, another chart, gauge, component,
  source branch, profile, root, or order;
* a physical incidence empty-set statement, including any composition with
  C_8=1, the GLD75/GLD86 bridge, D(Omega), or GLD95;
* positive-characteristic theorem claims from modular scouting;
* Fitting-ideal emptiness, source integrability, graph lifting,
  target attachment, global gluing, or global resolution; or
* a refutation or resolution of the global Krenn--Gu conjecture.

The exact result is the norm-cover reduction on D(H2*Delta), and no more.
The global Krenn--Gu conjecture remains **UNRESOLVED**.
