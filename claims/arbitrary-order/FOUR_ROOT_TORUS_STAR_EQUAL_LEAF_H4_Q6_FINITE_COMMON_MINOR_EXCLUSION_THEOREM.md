# Four-root torus-star equal-leaf H4 Q6 finite common-minor exclusion (GLD95)

## Status and exact scope

**Exact scoped characteristic-zero theorem (`GLD95`).**  On the written
rational three-parameter family `F88` forced by GLD88, the finite common
six-minor residual on `Q6=0` is empty on the full declared `D(Delta)` open.
The calculation explicitly includes the resultant-content fibres on which
the old GLD88 six-pivot `P6` vanishes.  This is a theorem about the written
formula family, not about every H4 point.

Work over `Q` and extend scalars to `C`.  Use the complete scale-fixed
equal-leaf survivor chart and the GLD75/GLD86 incidence bridge.  Put

```text
d0 = p+q-1,
P  = p^2-p+1,
L1 = p^2+2pq-2p-q,
L2 = 2pq-p+q^2-2q,
e  = 2pq^2-2pq-p-q^2-2q+2,
Delta = (p-q)d0 P L1 L2 e.
```

The family `F88` is the following written rational formula family:

```text
G = [1  1       1      ]
    [p  q       s      ],
    [a  1+b     1+c    ],

s = (p+q-pq)/d0,
b = -Nb/(P e),
c = -Nc/(d0 e),
```

where

```text
Nb = -2ap^2q^3+3ap^2q^2-3ap^2q+ap^2
     +2apq^3+2ap+aq^3-3aq^2+3aq-2a
     +p^3q^2-p^3+p^2q^3-3p^2q^2+p^2
     -2pq^3+3pq^2-2p+q^2-3q+2,

Nc = 2apq^3-3apq^2+3apq-ap
     -aq^3+3aq^2-3aq+2a
     +p^2q^2-2p^2q-3pq^2+pq+p-q^2+3q-2.
```

The formula family is interpreted on `D(Delta)`.  The identities defining
the family and its syndrome therefore extend to points where the old
GLD88 pivot `P6` is zero, provided the displayed rational denominators and
the factors in `Delta` remain nonzero.  No implication from an arbitrary
point of `H4 intersect V(Q6)` to this family is asserted.

Let `M(G)` be the fixed `37 x 9` GLD71 syndrome matrix evaluated on `F88`.
Use columns and rows

```text
S   = (0,1,3,4,6,7),
R28 = (0,1,2,17,25,28),
R31 = (0,1,2,17,25,31).
```

Writing the two exact determinants over their common denominator defines
`F28,F31`:

```text
det M[R28,S] = N28/(P^2 e^2),   N28=(p-q)^3 F28,
det M[R31,S] = N31/(P^2 e^2),   N31=d0(p-q)^3 F31.
```

The conclusion is

```text
V(Q6,F28,F31) intersect D(Delta) = empty.
```

Together with the 111 GLD88 block-kernel identities and the GLD75/GLD86
bridge, this gives

```text
B intersect V(I_7(A)) intersect F88 intersect V(Q6)
  intersect D(Omega Delta) = empty.                    (GLD95)
```

The global Krenn--Gu conjecture remains **UNRESOLVED**.  In particular,
GLD95 does not close arbitrary H4 `Q6=0` points outside `F88`, the GLD83
pulled-back Fitting ideal, other charts/components/gauges, source branches,
or other root/order obligations.

## 1. Upstream bridge and exact rank implication

The GLD75/GLD86 bridge identifies the normalized incidence equations with
the syndrome equations:

```text
B=0 iff M(G)C=0,
rank(A) = rank(M(G)[:,0:8]),
C_8=1.
```

Thus a point of `B intersect V(I_7(A))` has syndrome rank at most six.
GLD88 supplies the exact common block-kernel vector on `F88`,

```text
k=(u,v,1),
u=(q^2-q+1)L2/((p-q)d0^3),
v=-P L1/((p-q)d0^3).
```

The primary verifier checks all `3*37=111` block identities.  Hence the
syndrome rank is at most six throughout `F88 intersect D(Delta)`.  Whenever
one of the displayed six-minors is nonzero, the rank is exactly six and
the complete kernel is the three block-supported copies of `k`.  Any
compatible center has proportional rows and therefore has determinant zero,
contradicting the `D(Omega)` gate.  GLD95 closes the only missing case on
this family by proving that the two displayed minors cannot vanish together
on `D(Delta)`.

The leaf determinant identity, retained without cancellation, is

```text
det(G) = -(p-q)(-3a+p+1)L1 L2/(d0 P e).
```

## 2. The exact Q6 and resultant decomposition

The common GLD90 factor is

```text
Q6 = 2p^4q^2-2p^4q+p^4
     +2p^3q^3-7p^3q^2+5p^3q-2p^3
     +2p^2q^4-7p^2q^3+12p^2q^2-7p^2q+2p^2
     -2pq^4+5pq^3-7pq^2+2pq
     +q^4-2q^3+2q^2.
```

It is irreducible over `Q`, of total degree six, and each factor of
`Delta` is coprime to it.  Let

```text
R_a(p,q) = Res_a(F28,F31).
```

The exact replay records

```text
total degree(R_a) = 99,
degree_p(R_a)    = 56,
degree_q(R_a)    = 53,
SHA256(srepr(R_a))
  = fd85a520800c5bda4d93bc66d3ddf4be0fc16fdb1e65281be1a76cc23a3f9c8d.
```

Division of `R_a` by `Q6`, viewed over the generic field `Q(p)`, has a
nonzero q-degree-three remainder.  Its denominator is exactly

```text
H2^47,       H2=2p^2-2p+1,
```

and the remainder `srepr` hash is

```text
0057c78ceea5241553d856ce437f0fb4fd77571c8205eaa96c7c13dce54cec42.
```

After removing the primitive q-polynomial content, the content is exactly

```text
(1/2)(p-1)(p+1)(2p-1)p^4 P^9.
```

The resulting p-eliminant has squarefree degree `36`, with hash

```text
SHA256(srepr(squarefree_eliminant))
  = 86eca671802beaf8cb2cb1f3755494b24ece747f3bc3efb8129cf2263f8c6743,
```

and its squarefree factors are exactly

```text
p-1, p, H0, P, H1, H2, H3, H4, H5, H6,
```

where

```text
H0 = p^2-2p+2,
H1 = p^2+1,
H2 = 2p^2-2p+1,
H3 = 5p^4-16p^3+30p^2-16p+5,
H4 = 8p^4-16p^3+12p^2-4p+5,
H5 = p^6-6p^5+12p^4-16p^3+18p^2-12p+4,
H6 = 5p^12-36p^11+126p^10-316p^9+624p^8
     -984p^7+1272p^6-1344p^5+1146p^4
     -760p^3+372p^2-120p+20.
```

These factors are an exact exhaustive decomposition of the possible finite
common-minor residual.  Modular computations were used only for scouting;
the decomposition and every cover below are over `Q`.

## 3. Generic H-factor cover

For `H0,H1,H3,H4,H5,H6`, exact nested quotient-field gcds recover the
following q and a branches.  In every listed branch the displayed six rows
and the fixed columns `S` give a unit determinant.  The hash is the SHA-256
of the exact SymPy expression of that unit after normalization in the
nested quotient field.

```text
H0:
  q = 0, or q = 2-p;
  a^2 + (-11p/12-1/6)a + 7p/12-1/2 = 0.

H1:
  q = 1, or q = -p;
  a = 0.

H3:
  q = -1, or q = 2/3-6p/5-p^3/3+2p^2/5;
  a = 0.

H4:
  q = 1/2, or q = 2/3-4p^3/3-p+2p^2;
  a = p.

H5:
  q^2+(-p^5/2+2p^4-p^3+p^2-4)q
    -p^5/2+3p^4-6p^3+8p^2-9p+6 = 0,
  a+p^5/6-2p^4/3+2p^3/3-4p^2/3+p/3-1/3 = 0.

H6:
  q^2+B6(p)q+C6(p)=0,
  a+A6(p)=0,
```

where the exact H6 coefficients are

```text
B6(p) = 57p^11/5-3909p^10/50+2569p^9/10-15291p^8/25
        +28872p^7/25-42993p^6/25+10449p^5/5
        -51354p^4/25+39558p^3/25-912p^2+1766p/5-74,

C6(p) = -15p^11/2+239p^10/5-7403p^9/50+1719p^8/5
        -15777p^7/25+22734p^6/25-26991p^5/25
        +5118p^4/5-19038p^3/25+10426p^2/25-763p/5+142/5,

A6(p) = -p^11/24+22p^10/15-959p^9/120+227p^8/10
        -50p^7+347p^6/4-2341p^5/20+2611p^4/20
        -113p^3+1118p^2/15-100p/3+47/6.
```

The exact unit cover is:

| component | branch | unit rows (columns `S`) | unit hash |
| --- | --- | --- | --- |
| `H0` | `q=0` | `(1,17,0,28,4,32)` | `45c2969b26a7e7efa2585489eadb4ef554af37fa646ebdc875458e9ae2afd0f5` |
| `H0` | `q=2-p` | `(1,17,0,28,4,32)` | `fadd23534644e09f245d18c70267beeab53fb4d4a1812352ae4a216b0c61a5e3` |
| `H1` | `q=1` | `(1,17,0,25,28,31)` | `e18c9af590ffbe7cf4d646dbcef7b34d9beab4f8142761984469a7e7415f01ba` |
| `H1` | `q=-p` | `(1,17,0,25,28,31)` | `93724e3a9341a39e0bbc79796dab798b334e066085be3f467d6ccc9dcb8b72d1` |
| `H3` | first | `(1,17,0,25,28,31)` | `0d95bb74a934f840aeffa143c0e8b0444439af55deee0c4f2b6df228f9daec9a` |
| `H3` | second | `(1,17,0,25,28,31)` | `11ecb64cd0892907ff9739bb964cf3cda41cf32fb02087adc428ad48177cacce` |
| `H4` | `q=1/2` | `(1,17,0,28,4,31)` | `89086752d46f7145bd76162679eac0b3391d510b1f05bf23116dfeafd3924e70` |
| `H4` | second | `(1,17,0,28,4,31)` | `d69bbdd0832021bc2e46a421eb7b946318abe7509e84be895d99a56aa53acece` |
| `H5` | quadratic | `(1,17,0,25,4,32)` | `10fb6b29e65080f23b3bb094dd448fac188d8f81b50fcfcf102c76f94d57cc37` |
| `H6` | quadratic | `(1,17,0,25,4,32)` | `0b4623755a43cd5e6ba7a8e15641d264f49d852533900d4a5ddc1827a1a1d36b` |

The `H2` row requires a separate argument.  `H2` is the leading coefficient
of `Q6` as a polynomial in q, so the generic q-division is not valid on
`H2=0`.  Direct specialization in `Q[p]/(H2)` gives `deg_q(Q6)=3`, an
exact resultant of q-degree `50`, and

```text
gcd_q(Q6, Res_a(F28,F31)) = p+q-1 = d0.
```

Therefore every true common point on the H2 fibre is excluded by `D(Delta)`.
The apparent quadratic q branch obtained by generic division is a division
artifact and is not used in this cover.

## 4. Resultant-content fibres and the old P6=0 extension

The four non-P factors in the resultant content, together with the p=0
factor, require direct exact specialization.  Lexicographic Groebner bases
of `(Q6,F28,F31)` at these p-values are:

```text
p=0:
  [a^2 q^2-(5/3)a q^2,
   q^4-2q^3+2q^2].

p=1:
  [a^3-(8/3)a^2+(4/3)a,
   aq^2-2aq+a-2q^2+4q-2,
   q^4-2q^3+2q^2-2q+1].

p=-1:
  [a+(5/9)q^3-(2/3)q^2+q/3+14/9,
   q^4-(16/5)q^3+6q^2-(16/5)q+1].

p=1/2:
  [a+(8/9)q^3-(4/3)q^2-5/18,
   q^4-2q^3+(3/2)q^2-q/2+5/8].
```

After removing the boundary components `q=0` at `p=0` and `q=1` at
`p=1` (both violate `D(Delta)`), the complete retained content components
and their exact unit minors are:

| fibre and component | q modulus; a value | unit rows (columns `S`) | exact unit | unit hash |
| --- | --- | --- | --- | --- |
| `p=0`, first | `q^2-2q+2`; `a=0` | `(1,17,28,0,32,3)` | `-15q` | `943867f4bce314d869a83ccfb7349f34c5f97ca7ddca19f47056da39010780df` |
| `p=0`, second | `q^2-2q+2`; `a=5/3` | `(1,17,25,0,4,32)` | `400q/3` | `ce2109fbaa3262e1bad3f7a6377c17be85b0f81e30b59faf3ee7ef7da687a48c` |
| `p=1` | `q^2+1`; `a=2` | `(1,17,0,25,28,31)` | `24-24q` | `4576a54cb064bf296164af03c67fd6c3f489917e0825bd6c5d8c304ae4fddc22` |
| `p=-1` | `q^4-(16/5)q^3+6q^2-(16/5)q+1`; `a=-(5/9)q^3+(2/3)q^2-q/3-14/9` | `(1,17,0,25,28,31)` | `2106684q^3/625-413244q^2/25+6108084q/625-432324/125` | `7cfe9dcb1cea749581b85f9a9ebab5f42be99ebc8dfa5d7786eddf30692e094a` |
| `p=1/2` | `q^4-2q^3+(3/2)q^2-q/2+5/8`; `a=-(8/9)q^3+(4/3)q^2+5/18` | `(1,17,0,28,4,31)` | `-45q^3/16+45q^2/128-45q/128+225/512` | `191ad4b8b2de39cd364569d75be13e12d332f4cb766eea0d0dc5150da9243d23` |

Each q modulus is handled as an exact quotient algebra, not by sampling its
complex roots.  The unit determinant has numerator and denominator coprime
to the modulus in an independent `Q[q]` gcd check.  On every one of these
five components:

```text
old P6 = det M[(0,1,2,17,19,32),S] = 0,
all six factors of Delta are units,
det(G) is a unit.
```

Thus these are genuine extensions across the old `P6=0` boundary, rather
than points silently discarded by the GLD88 pivot chart.  The `P=0`
content factor is outside `D(Delta)` and is covered upstream by GLD89.

## 5. Exact finite-residual certificate and proof

For the coefficient ideal

```text
J = (Q6, coefficients in a of F28, coefficients in a of F31)
    subset Q[p,q],
```

the exact lexicographic Groebner replay gives

```text
J is zero-dimensional,
the final q eliminant is q^6(q^2-q+1)^4,
((p-q)P)^6 belongs to J.
```

This inherited GLD92 certificate rules out vertical a-lines on `D(Delta)`.
The exact resultant/content decomposition above is exhaustive, and every
factor that can meet `D(Delta)` is either:

1. one of the generic `H0,H1,H3,H4,H5,H6` branches with a unit six-minor;
2. the direct H2 fibre, whose true gcd is `d0`; or
3. one of the five content components with a unit six-minor.

The `P` factor is excluded by `D(Delta)`.  Therefore the alleged common
minor locus `V(Q6,F28,F31)` has no point on `D(Delta)`.

At any point of `F88 intersect V(Q6) intersect D(Omega Delta)`, at least one
of `F28,F31` is therefore nonzero.  Its six-minor makes the syndrome rank
exactly six, while the common block kernel forces every compatible center to
have proportional rows.  This contradicts `det(C) != 0` in `D(Omega)` and
proves the displayed GLD95 exclusion.

## 6. Verification and independent audit

Primary exact verifier:

```text
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_finite_common_minor_exclusion.py
```

The primary imports the committed GLD71 relation builder and GLD88 family
function, reconstructs the full `37 x 9` syndrome, checks all 111 block
identities, computes both exact six-minors, verifies the resultant/content
decomposition, checks the vertical-fibre certificate, performs the nested
generic unit cover, handles H2 directly, and checks all five content
components including `P6=0`.  Its exact result is pinned by the resultant,
remainder, squarefree, generic-unit, and content-unit hashes above.

Independent exact audit:

```text
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_finite_common_minor_exclusion.py
```

The audit imports neither the primary verifier, the GLD71 builder, nor the
GLD88 family builder.  It directly evaluates the copied immutable sparse
supports for rows

```text
{0,1,2,3,4,17,19,25,28,31,32}
```

and an independently written formula copy.  Its support-data SHA-256 is

```text
24cdba204347947370076c621b167f5aac617b9731d30cd22e25504630cf87d3.
```

It independently replays the determinants, resultant decomposition, H2
direct gcd, generic unit determinants, and content units.  For the content
units it additionally uses a separate numerator/denominator gcd route in
`Q[q]`, and directly confirms old `P6=0` and all `Delta` units.  This is a
genuinely different determinant/evaluation route, but it shares the fixed
sparse supports and the written F88 formula as mathematical input; it does
not independently reprove the GLD75/GLD86 bridge or the GLD88 kernel
implication.

## 7. Residual ledger and scope fences

GLD95 closes the finite common-minor residual on `Q6=0` **inside the written
GLD88/F88 rational family over `D(Delta)`**, including every resultant-content
component that survives the open and every old-`P6=0` content component.
It does not claim:

- arbitrary `H4 intersect V(Q6)` points lie in `F88`;
- closure of the full H4 Q6 boundary outside the forced family;
- a computation of the GLD83 pulled-back Fitting ideal;
- coverage of other charts, gauges, survivor components, source branches,
  roots, or orders; or
- a resolution of the global Krenn--Gu conjecture.

The global status remains **UNRESOLVED**.
