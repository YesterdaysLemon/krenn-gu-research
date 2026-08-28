# Four-root torus-star equal-leaf H4 Q6-boundary dense minor exclusion (GLD92)

## Status and exact scope

**Exact scoped characteristic-zero theorem (`GLD92`).** This package closes a
dense principal-open subset of the `Q6=0` boundary **inside the rational
three-parameter family already forced by GLD88**. It is not a closure of the
whole H4 `Q6` boundary: no argument here proves that an arbitrary
rank-at-most-six point on `H4 intersect V(Q6)` lies in the GLD88 family.

Work over `Q` and extend scalars to `C`. Use the complete scale-fixed
equal-leaf survivor chart and the GLD75/GLD86 incidence bridge. In the H4
chart, put

```text
d0 = p+q-1,
P  = p^2-p+1,
L1 = p^2+2pq-2p-q,
L2 = 2pq-p+q^2-2q,
e  = 2pq^2-2pq-p-q^2-2q+2,
Delta = (p-q)d0 P L1 L2 e.
```

Let `F88` denote the GLD88 rational three-parameter family on this chart:

```text
G = [1  1       1      ]
    [p  q       s      ],
    [a  1+b     1+c    ],

s=(p+q-pq)/d0,
(b,c)=(b_88(p,q,a),c_88(p,q,a)).
```

The exact rational functions `b_88,c_88` are the `h4_family` functions in
the linked GLD88 verifier; the present primary reconstructs that family and
does not infer it numerically. Their denominators are among `P,d0,e`.
Write `K_G=-3a+p+1` for the leaf-determinant factor recorded exactly below.
The normalized
`D(Omega)` gate already requires `det(G) != 0` and `det(C) != 0`; the
additional factor in `det(G)` is retained rather than divided away.

Let `M(G)` be the fixed `37 x 9` GLD71 syndrome matrix on `F88`. Define two
six-row minors using the fixed columns

```text
S=(0,1,3,4,6,7),
R28=(0,1,2,17,25,28),
R31=(0,1,2,17,25,31).
```

Let `N28,N31` be the exact determinant numerators after putting the two
minors over a common denominator, and define `F28,F31` by

```text
det M[R28,S] = N28/(P^2 e^2),   N28=(p-q)^3 F28,
det M[R31,S] = N31/(P^2 e^2),   N31=d0(p-q)^3 F31.
```

The explicit common factor of the preceding GLD90 pivots is

```text
Q6 = 2p^4q^2-2p^4q+p^4
     +2p^3q^3-7p^3q^2+5p^3q-2p^3
     +2p^2q^4-7p^2q^3+12p^2q^2-7p^2q+2p^2
     -2pq^4+5pq^3-7pq^2+2pq
     +q^4-2q^3+2q^2.
```

Define the dense Q6 open and its retained residual by

```text
U_dense = (D(F28) union D(F31)) intersect V(Q6) intersect D(Omega Delta),
Z_fin   = V(Q6,F28,F31) intersect D(Omega Delta).
```

Then the exact set-theoretic conclusion is

```text
B intersect V(I_7(A)) intersect F88 intersect U_dense = empty.       (GLD92)
```

Here `D(F28) union D(F31)` is a union of principal opens, not `D(F28 F31)`;
at least one of the two alternative six-minors is required. The complement
of this union on the Q6 family is the explicitly retained `Z_fin`. GLD92
proves that `Z_fin` is finite on the displayed `D(Delta)` open, but neither
enumerates nor excludes it.

The theorem leaves `Z_fin`, the coefficient boundaries `L1=0`, `L2=0`, and
`e=0`, the full H4 `Q6` boundary outside `F88`, the GLD83 Fitting pullback,
other charts/components/gauges/source branches, and all wider proof
obligations open. The global Krenn--Gu conjecture remains **UNRESOLVED**.

The leaf determinant on `F88`, checked by the primary, is

```text
det(G) = -(p-q)(-3a+p+1)L1 L2/(d0 P e).              (1)
```

Thus the factor that must remain nonzero in `D(Omega)` is `K_G=-3a+p+1`. No affine zero
block or determinant factor is removed by the Q6 argument.

## 1. Upstream bridge and the GLD88 family

The GLD75/GLD86 bridge identifies the incidence equations on the normalized
survivor chart with the syndrome equations:

```text
B=0 iff M(G)C=0,
rank(A) = rank(M(G)[:,0:8]),
C_8=1.
```

Consequently, a point of `B intersect V(I_7(A))` has full syndrome rank at
most six. This is the only use of the seven-minor ideal in GLD92.

GLD88 supplies the exact family `F88` on its named H4 Schur chart and the
common block-kernel vector

```text
k=(u,v,1),
u=(q^2-q+1)L2/((p-q)d0^3),
v=-P L1/((p-q)d0^3).
```

After substituting `F88`, the primary checks all `3*37=111` block-kernel
identities. Therefore `rank(M(G)) <= 6` throughout this rational family on
the declared denominator open. If either displayed six-minor is nonzero,
the rank is exactly six. Its three-dimensional kernel is then precisely the
three block-supported copies of `k`, so every compatible center has rows
proportional to `k^T` and hence has determinant zero. This contradicts the
`D(Omega)` center determinant gate.

This rank/kernel implication is why GLD92 is a theorem on `F88`; the
GLD90 argument does not supply the missing implication from all of
`H4 intersect V(Q6)` into `F88`.

## 2. Exact minor identities and hashes

The two determinants are evaluated over `Q` before any specialization. The
common denominator is exactly `P^2 e^2`, and the stripped factors are
irreducible over `Q` of total degrees `20` and `18` respectively.

| minor | rows | numerator degree `(p,q,a)` | terms | exact factorization metadata | numerator `srepr` SHA-256 | canonical polynomial SHA-256 |
| --- | --- | ---: | ---: | --- | --- | --- |
| `N28` | `(0,1,2,17,25,28)` | `23` (`deg_a=3`, `deg_q=13`) | `618` | `(p-q)^3 * F28`, `deg(F28)=20` | `55bfba7b569752acb072ad0922d273e55d70651782e93394a14f9c23098727b8` | `28e72c0b5af9d79c1bf39adc4b84ac10c8b68599f037b21563a78a48bc578d55` |
| `N31` | `(0,1,2,17,25,31)` | `22` (`deg_a=3`, `deg_q=12`) | `577` | `(p+q-1)(p-q)^3 * F31`, `deg(F31)=18` | `352948a2c113f32f10b90520592cb266cb455853297a664964478fdd7369b18f` | `8d7662c4a47da61c9322ed2c45091a204f6e5cb0d9b5b3eb89892582d7a3d8d3` |

The exact division of each numerator by `Q6`, viewed as a polynomial in
`q` over `Q(p,a)`, has nonzero remainder of `q`-degree `3`:

```text
N28 remainder srepr SHA-256:
  8efab099320d2e498167c86999ac90adfeb85f2d80d3bd1f4b4e7539577298ef
N31 remainder srepr SHA-256:
  b05d58c3177d7d0c8ea1b54cf7931f0a8e73b314518c748031f9be847d331912
```

Thus neither minor numerator is divisible by `Q6`. Since `Q6` is
irreducible over `Q` of total degree `6`, each of `D(F28)` and `D(F31)` is
a nonempty dense principal open of the irreducible Q6 curve, subject to the
inherited `D(Omega Delta)` gate. The primary also checks that each of
`p-q`, `d0`, `P`, `L1`, `L2`, and `e` is coprime to `Q6`, so the declared
Delta-open is not lost identically on this divisor.

## 3. Why the common residual is finite on the declared open

Let

```text
R_a(p,q) = Res_a(F28,F31).
```

The exact resultant has total degree `99`, degree `53` in `q`, and

```text
R_a srepr SHA-256 =
  fd85a520800c5bda4d93bc66d3ddf4be0fc16fdb1e65281be1a76cc23a3f9c8d,
gcd(R_a,Q6) = 1.
```

The `q`-division remainder of `R_a` by `Q6` has degree `3` and

```text
0057c78ceea5241553d856ce437f0fb4fd77571c8205eaa96c7c13dce54cec42.
```

Therefore `F28` and `F31` have no common component whose projection
dominates the irreducible Q6 curve. A resultant alone can miss a vertical
`a`-line at a special `(p,q)`, so GLD92 checks this boundary explicitly.

Let `J` be the coefficient ideal in `Q[p,q]` generated by `Q6` and all
coefficients in `a` of `F28` and `F31`. The exact lexicographic Groebner
certificate is

```text
J is zero-dimensional,
the final q eliminant is q^6 (q^2-q+1)^4,
((p-q)P)^6 belongs to J.
```

Hence every base point at which both polynomials vanish identically in `a`
already lies on `(p-q)P=0`, outside `D(Delta)`. On the declared open there
are no vertical `a`-lines. Combined with the resultant coprimality, this
proves that `Z_fin` is a finite (zero-dimensional) common-minor residual on
`D(Omega Delta)`. The statement is deliberately only finiteness; the
finite points are not solved for here.

## 4. Proof of the scoped exclusion

Take a point of `F88 intersect V(Q6) intersect D(Omega Delta)` in `D(F28)`. The denominator
`P^2e^2` is a unit on `D(Delta)`, and `p-q` is a unit there, so the `N28`
factorization makes the `R28,S` six-minor nonzero. The 111 GLD88 kernel
identities give syndrome rank at most six, hence rank exactly six. The
complete kernel is the three block copies of `k`, so any center satisfying
`M(G)C=0` has proportional rows and `det(C)=0`. This contradicts
`D(Omega)`.

The same argument with `N31` applies at a point in `D(F31)`. These two cases
give the union `D(F28) union D(F31)` and prove GLD92. Points where both
factors vanish are exactly the retained `Z_fin`; no assertion is made there.

## 5. Verification and independent audit

Primary exact replay:

```text
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_boundary_dense_minor_exclusion.py
```

The primary imports the committed GLD71 relation builder and GLD88 family
function, reconstructs the full `37 x 9` syndrome, checks all 111 kernel
identities, derives both exact minors, verifies the denominator and factor
metadata, proves `Q6` irreducible and Delta-factor coprimality, computes the
`a`-resultant, and checks the vertical-fibre Groebner certificate. Its output
is the exact scoped claim above, with `global_conjecture_resolved: false`.

Independent sparse-support audit:

```text
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_boundary_dense_minor_exclusion.py
```

The audit imports neither the primary, GLD71 builder, nor GLD88 family
builder. It directly evaluates the seven fixed sparse supports needed by the
two minors, using an independently written coefficient loop and a copied
explicit rational family, then repeats the exact determinant, Q6 division,
resultant, and vertical-fibre checks. Its support-data SHA-256 is

```text
9bea8532ac1a79352508e04db8eca836402a9153edb18fa45e94a012d63162f8.
```

This is a genuinely distinct determinant/evaluation route, but it shares
the fixed sparse supports and the GLD88 rational family as mathematical
input. It does not independently reprove the GLD75/GLD86 incidence bridge
or the GLD88 common-kernel lemma; those remain upstream dependencies.

## 6. Residual ledger

| locus or obligation | GLD92 disposition |
| --- | --- |
| `F88 intersect V(Q6) intersect D(Omega Delta F28)` | excluded by `M28` |
| `F88 intersect V(Q6) intersect D(Omega Delta F31)` | excluded by `M31` |
| `Z_fin = V(Q6,F28,F31) intersect D(Omega Delta)` | finite residual, not enumerated or excluded |
| arbitrary `H4 intersect V(Q6)` outside `F88` | not addressed; no family-forcing implication claimed |
| `L1=0`, `L2=0`, `e=0` coefficient boundaries | open |
| `P=0`, `d0=0` | handled in the separate GLD89 scope, not reproved here |
| GLD83 pulled-back Fitting ideal | not computed |
| other charts/components/gauges/source branches | open |
| global Krenn--Gu conjecture | **UNRESOLVED** |
