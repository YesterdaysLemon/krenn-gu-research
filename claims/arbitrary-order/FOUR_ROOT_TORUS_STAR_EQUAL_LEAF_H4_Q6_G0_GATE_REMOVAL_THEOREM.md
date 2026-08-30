# Four-root torus-star equal-leaf H4 Q6 normalized g0 gate removal (GLD100)

## Status

**Proved exact scoped characteristic-zero theorem (`GLD100`).**

On the normalized GLD88/F88 offset chart `U88`, with
`b=b88(p,q,a)+B`, `c=c88(p,q,a)+C`, the exact implication is

```text
V(Q6) intersect D(E31*H2*Delta) intersect {rank M(G) <= 6}
    is contained in {B=0,C=0} = F88.
```

The identities are computed over `Q` and remain valid after
characteristic-zero base extension.  GLD100 removes the old GLD96 `g0`
localization on this normalized, `E31`-open, `H2`-open subroute.  Composing
with the exact GLD99 `H2=0` theorem gives the normalized implication on
`D(E31*Delta)`.

With the established GLD75/GLD86 incidence bridge on `U88` and the
scale-fixed incidence-center normalization `C_8=1`, the GLD95 F88 endpoint
therefore gives

```text
B_incidence intersect V(I_7(A)) intersect U88 intersect {C_8=1}
  intersect H4 intersect V(Q6) intersect D(E31*Delta)
  intersect D(Omega) = empty.
```

`C_8` is the incidence-center coordinate in the bridge, not the leaf offset
`C`.  The physical `Omega` open remains retained.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

This is an exact local theorem and its stated composition with GLD99 and
GLD95; it does not claim global resolution or coverage outside the written
chart and opens.

## 1. Normalized chart and theorem statement

Use the scale-fixed equal-leaf chart

```text
G = [1  1       1      ]
    [p  q       s      ],
    [a  1+b     1+c    ],

s = (p+q-pq)/(p+q-1).
```

The H4 relation is `pq+ps+qs-p-q-s=0`.  Set

```text
d0 = p+q-1
P  = p^2-p+1
L1 = p^2+2pq-2p-q
L2 = 2pq-p+q^2-2q
e  = 2pq^2-2pq-p-q^2-2q+2
Delta = (p-q)d0 P L1 L2 e.
```

The GLD88 rational functions `b88,c88` define the normalized offsets

```text
b = b88(p,q,a) + B,
c = c88(p,q,a) + C.
```

Here `B,C` are offsets; `C` is not the quartic polynomial called `C4` below.
All statements in this document are over characteristic zero and on the
denominator-safe open `D(Delta)` unless a boundary is explicitly named.

Let `U88` denote this normalized GLD88/F88-offset chart: the displayed
scale-fixed equal-leaf H4 family, with the offsets `b=b88+B` and
`c=c88+C`, restricted to `D(Delta)`.  In the two physical displays below,
`U88` is used together with the scale-fixed incidence-center slice
`C_8=1`.  The GLD75/GLD86 bridge hypothesis on that slice is
`B=0 iff M(G)C=0` and `rank(A)=rank(M(G)[:,0:8])`; hence
`V(I_7(A))` supplies the full syndrome rank-at-most-six condition there.
Here `C_8=1` is the normalization of the incidence-center vector in the
bridge, not the scalar offset `C` above.

The Q6 equation is

```text
Q6 = 2p^4q^2-2p^4q+p^4
     +2p^3q^3-7p^3q^2+5p^3q-2p^3
     +2p^2q^4-7p^2q^3+12p^2q^2-7p^2q+2p^2
     -2pq^4+5pq^3-7pq^2+2pq+q^4-2q^3+2q^2.
```

Let `M(G)` be the 37-by-9 GLD71 syndrome.  The four GLD96 bordered
seven-minors are

```text
T0 = det M[(0,1,2,17,25,31,28), (0,1,3,4,6,7,8)],
T1 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,2)],
T2 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,5)],
T3 = det M[(0,1,2,17,25,31,33), (0,1,3,4,6,7,8)].
```

The two direct detectors used on the exceptional fibres are

```text
D0 = det M[(1,17,28,0,25,31,32), (0,1,2,3,4,5,6)],
D2 = det M[(1,17,28,0,31,32,3), (0,1,2,3,4,5,6)].
```

The normalized gate-removal theorem is:

```text
V(Q6) intersect D(E31*H2*Delta) intersect {rank M(G) <= 6}
    is contained in {B=0,C=0} = F88.
```

Equivalently, the GLD96 `g0` localization is removable on this normalized
chart.  On `g0 != 0` this is the existing GLD96 argument.  On `g0 = 0`, the
`E31` cross-resultant argument forces `B=0`; the pair screen and the exact
branch closures in Sections 2--4 force `C=0`.  Since rank at most six makes
every displayed seven-minor vanish, the extra direct detectors are legitimate
necessary equations in the exceptional branch.

Using the existing GLD75/GLD86 incidence bridge on the normalized
`U88` chart with its `C_8=1` center normalization, and the GLD95 F88
exclusion, the intended physical corollary is

```text
B_incidence intersect V(I_7(A)) intersect U88 intersect {C_8=1}
  intersect H4 intersect V(Q6)
  intersect D(E31*H2*Delta) intersect D(Omega) = empty.
```

After handing the `H2=0` fibre to GLD99, the intended normalized route is

```text
B_incidence intersect V(I_7(A)) intersect U88 intersect {C_8=1}
  intersect H4 intersect V(Q6)
  intersect D(E31*Delta) intersect D(Omega) = empty.
```

The second display is a composition of scoped results, not a new global
theorem.  `Omega` remains a physical-incidence open and is not removed by
this gate.

## 2. Exact necessary pair-resultant cover

On `D(H2*Delta)`, let
`gamma0,...,gamma3` be the primitive `C`-coefficients obtained from the four
GLD96 residuals at `B=0` after exact reduction modulo `Q6`.  A
`g0=0`, `C != 0` point satisfies

```text
Q6 = gamma0 = gamma1 = gamma2 = gamma3 = 0.
```

For `i=1,2,3`, form the pair resultant in `a`, then eliminate `q` against
`Q6`.  The exact all-three gcd has squarefree support

```text
S(p) = p*(p-1)*(p^2+1)*(p^2-2p+2)
       *(p^2-p+1)*(2p^2-2p+1)*A4*C4,

A4 = 5*p^4 - 16*p^3 + 30*p^2 - 16*p + 5,
C4 = 8*p^4 - 16*p^3 + 12*p^2 - 4*p + 5.
```

Thus the eight factors in `S` are a necessary case cover for a common
`Q6,gamma0,...,gamma3` zero.  The unsquared gcd has irrelevant multiplicities
in several factors; only its radical is used here.  Pair resultants are used
only in this necessary direction.  No claim is made that their roots are
sufficient, or that leading-coefficient and degree-drop roots are absent.

The exact branch information is:

| `p` factor | residual `q,a` information | exact treatment |
|---|---|---|
| `p` | branch forces `q=0`, hence `p-q=0` | `Delta=0`; outside `D(Delta)` |
| `p-1` | branch forces `q=1`, hence `p-q=0` | `Delta=0`; outside `D(Delta)` |
| `p^2-p+1=P` | no further data needed | `P` is a factor of `Delta` |
| `2p^2-2p+1=H2` | GLD99 H2/Q6 degree-drop branch | exact scoped GLD99 handoff |
| `p^2+1` | `q=-p`, common `a`-gcd `a` | direct `D0` identity below |
| `p^2-2p+2` | `q=2-p`, common `a`-gcd `1` | no common affine gamma zero |
| `A4` | `(p-2)q-(2p-1)=0`, common `a`-gcd `a` | direct `D0` identity below |
| `C4` | `(2p-1)q-(p+1)=0`, common `a`-gcd `a-p` | direct `D2` identity below |

The denominators `p-2` and `2p-1` in the simplified quartic relations are
units in their respective quotient fields.  The quadratic and quartic
residual q-factors have gcd one with `Delta`, so those branches are not
discarded as Delta-boundary points.

## 3. Fibre identities that remove the surviving C offset

Write `Coff` for the offset `C` in the following identities.  Each identity
is in the indicated quotient field and uses the exact GLD71 sparse syndrome,
the GLD88 family, the row/column sets for `D0,D2` in Section 1, and `B=0`.

### 3.1 The `p^2+1` fibre

The exact pair screen gives `q=-p`; the final specialized gamma gcd is `a`.
For example, the reduced third coefficient has the form

```text
gamma3 = 128*a*(79*p-3),
```

and `79p-3` is a unit modulo `p^2+1`, while all four gammas vanish at
`a=0`.  Hence the four GLD96 `T` equations alone do not remove `Coff` on
this fibre.

The direct seven-minor calculation gives

```text
D0 = 192*(1-p)*Coff^2,
D2 = 0,
```

in `Q[p]/(p^2+1)`.  Since
`gcd(p^2+1,1-p)=1`, the primary and independent quotient-unit witnesses show
that a rank-at-most-six point has `Coff=0`.  The specialized `Delta` is also
certified a unit, so this is an admissible normalized fibre before the
downstream GLD95 F88 exclusion.

### 3.2 The `p^2-2p+2` fibre

The exact pair screen leaves only `q=2-p`.  At that q-value,
`gamma0=gamma3=0`, but the remaining common-a test is empty.  One compact
primitive witness is the reduced resultant

```text
Res_a(gamma1,gamma2)
  = 229507011067464757385625600
    *(36619708247*p - 59459194168)
```

modulo `p^2-2p+2`; its linear factor is nonzero in this quadratic field.
Therefore this branch has no common affine zero of all four gammas.

### 3.3 The quartic `A4` fibre

The exact q relation is

```text
(p-2)*q - (2*p-1) = 0,
```

and the common-a gcd is `a`, so `a=0`.  The direct `D0` identity is

```text
D0 = -(7776/3125)*(p+1)
     *(8171*p^2 - 5068*p + 1965)*Coff^2,
```

in `Q[p]/(A4)`, with `D2=0` in the same specialization.  The coefficient is
nonzero because

```text
gcd(A4, (p+1)*(8171*p^2-5068*p+1965)) = 1.
```

The branch has a certified nonzero `Delta` and therefore cannot be dismissed
as a chart boundary; the displayed direct minor closes it.

### 3.4 The quartic `C4` fibre

The exact q relation is

```text
(2*p-1)*q - (p+1) = 0,
```

and the common-a gcd is `a-p`, so `a=p`.  Here `D0=0`, while the direct `D2`
identity is

```text
D2 = (243/128)*(p-1)
     *(52*p^2 + 2*p + 25)*Coff^2,
```

in `Q[p]/(C4)`.  The coefficient is nonzero because

```text
gcd(C4, (p-1)*(52*p^2+2*p+25)) = 1.
```

Again the specialized `Delta` is certified a unit.  This direct minor closes
the last quartic branch.

## 4. Proof route

1. Take a rank-at-most-six point in the normalized chart on
   `D(E31*H2*Delta)`.  All six displayed seven-minors vanish.
2. Use the existing GLD96 cross-resultant argument on `D(E31)` to obtain
   `B=0`; this part does not require `g0 != 0`.
3. If `C=0`, the point is already on F88.  If `C != 0`, the four `T`
   equations give `gamma0=...=gamma3=0`.
4. The exact necessary pair-resultant cover puts `p` in one of the eight
   factors in Section 2.  The `p` and `p-1` branches force `q=0` and `q=1`,
   respectively, hence `p-q=0` and therefore `Delta=0`; the `P` factor is
    itself a factor of `Delta`.  `H2` is retained for GLD99; the four
    remaining quadratic or quartic fibres are closed by Sections 3.1--3.4.
5. Consequently `C=0`, so the point lies on F88.  Invoke GLD95 for the
   incidence exclusion on `D(Omega)`.
6. For the H2 boundary, use the exact scoped GLD99 six-minor offset result
   on `H2=Q6=0` and `D(Delta)`, then combine the two H2 pieces.  This is why
    the resulting normalized route has `D(E31*Delta)` while the generic
   GLD96 step has `D(E31*H2*Delta)`.

The route uses direct seven-minors only as necessary rank equations.  It does
not assert that the six displayed minors generate the full rank ideal.

## 5. Exact certificate and independent replay

The primary verifier source-recomputes all 111 GLD88 F88 kernel identities,
the raw affine-in-`C` residual identity, the canonical sparse gamma atlas,
all three pair projections, the full-content gcd and radical, every q/gamma
branch, and fresh-process direct minors.  Its immutable source manifest is
checked before any certificate is accepted.  The support rows are

```text
(0,1,2,3,17,25,28,31,32,33)
```

with digest
`c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0`; the
Q6 digest is
`2ed58764e7c50c8e1510a93b32d2515a9297c03dfe297fed8d9abe5f8e9d71a7`.

The primary pins the four primitive gamma coefficients as follows:

| coefficient | terms | `(p,q,a)` degrees | full digest | sparse digest | content |
| --- | ---: | --- | --- | --- | --- |
| `gamma0` | 308 | `(27,3,2)` | `ecc04ca65bf325abe133e0d9dabe709f16d01cc8cb2ff4711d07c683cfc76531` | `a8730bca93a78aeebdfd6923d4c343d44b8968d4489cbfe8bb4426fd94f3d7f8` | `3` |
| `gamma1` | 484 | `(32,3,3)` | `4db77cd0ce9882b9e2f2e7694805153b9e819a8da2e425a853ba427853c65d31` | `9e37dd630d8d74a363c4302067ca877070b96b0bf8ae05f6d324eda561a6e6a2` | `3` |
| `gamma2` | 437 | `(29,3,3)` | `b1afa68aee1f50bf708082d6a9d2f2d6552dd222e6f69a6a5473747d11291232` | `88ecfc18dcc511a0c61dda5da0d4bdb208102bc0e6164d9019c19a05dc8bb3c8` | `3` |
| `gamma3` | 308 | `(27,3,2)` | `c171b5d7205afb6d719fe5b3464fa6347968f41e84b0a829c0a81dddfb4bdb2b` | `6103df0e6a9e7c1279fe00b58eb48974c792f1b80801f768b99d4146bf5fdc3c` | `3` |

The pair projections are pinned by the following exact data:

| pair | resultant degree/digest | q-remainder terms/digest | p content | clearing scale | primitive-clearing digest |
| --- | --- | --- | --- | --- | --- |
| `01` | `544` / `8f1666c2cc18c3c96b2eb2502533593ded9ef2870261c04be057b5a7d32ee32b` | `576` / `0c0abdc92c1b9479a265aa492060965cb046fcd8d13eb2d6c32b6d77fe4149a3` | `p^3*P^10` | `H2^12` | `286f00a9f4bf1e3e54eaed31a96150ed95a9ccc1c2cff6ef08a15272f1118cb8` |
| `02` | `552` / `13f408ae39f9df64130f4ade389f3b1835ba6863278b303d0808fdeaf54f6ef7` | `580` / `53e8eff8d4196bba8a65afa522da5410ca5f6193c99d41fb17efbb04406fe7f4` | `P^10` | `H2^12` | `d90854308021e1c939082fe69cd29891c2bbc5a790509f78af9aac8296f0f141` |
| `03` | `406` / `24ea888f45f850c676c4c89e01bfa01af72ead3abe01cd2103bab9d98f47767e` | `418` / `c3b126f686bd1e437710354e1134fd795ba14193df56a50ebd0eddd4c1a591c3` | `p*P^8` | `H2^9` | `36d30092aa02c2bfa87d747c550eb92f894e890d94f285a7d51d6d597f9ab8b2` |

The complete fibre records are strict: the primary's nonempty
`EXPECTED_FIBRE_CERTIFICATE_HASHES` dictionary is compared unconditionally
with freshly serialized output.  The q/gamma certificate and record hashes
are

| fibre | q certificate | gamma certificate | record |
| --- | --- | --- | --- |
| `p_zero` | `117cd8a1d34c049d7eccff67c109218dc04598bced324d70516d94b1a893c05c` | -- | `ac040719033aadfe063a8d7e0476cbe4ea6346c481eca59e8cfd795e08aec28d` |
| `p_one` | `33a09af34c9cbbbfa23bb121ec65b37c8f62b3dee5b18296e31bb39b37d3ef46` | -- | `e7435826b6f83e266b0c7f33913b3f751a7beb34f82611a14e836f14a9246c19` |
| `p2_minus_2p_plus_2` | `ff7800aa3c73d25cf6c32ec126aa5dcdc170ad77d897fdae611076173d31ac26` | `a621ea79ac02345a4791cc77758c00aaa40e54c54dc931c8251872a8dd79765b` | `9e09bba21de584cbdef71b87adea3434a061ba7a736bad2ed1fa2e2d560431c1` |
| `p2_plus_1` | `f6c68d1dac6f1f3476608ab44b782f3e750b7479bc624a89ba5fe6109566ace0` | `09d20e32246d806291968abb6e75a159c171c64f59fe95e78b01245b79b79539` | `735e214db73cce1c3dab30796ceaf282a0488fc7635af70e4ed5aa5df129e43e` |
| `quartic_A` | `91df50fd7f698a0f258dd0459345e63bec3e821a8b3b307477f3f70281da420a` | `6c7cb7ce998bfc2b3167ff026fa6c8f5888694649e771f06473a19864446767b` | `adcaae32f5078caa889a9371c63ef8d64c8f8b1978be1f6d6910f93ee5986a99` |
| `quartic_C` | `9c1b9105f89f59817bb715a602191584ea565e674643c2818fc3311371fb59b1` | `90e35d6f039377616d5ffbe267f76689632d2db1d33b029f22936f27f33cab8b` | `44b7e8196324d80f376ec1665e30b727671fac95614261c87ddaa9dfda350676` |
| `P` | -- | -- | `8b37f7b9ddacb578bbdde4c89509e551b3d59019da57635cbbce3868eaf800d0` |
| `H2` | -- | -- | `164ff1a0d7fdbb93e68c34cbf6eafb8e669cac5205df888a9c337dd8a65494e2` |

Each q/gamma Bezout witness is serialized as exact polynomial term data:
variable and domain, source polynomials, coefficient polynomials, monic gcd,
the reconstructed identity, and `identity_verified=true`.  Quotient-unit
witnesses use schema `gld100-quotient-unit-v1` and include the numerator or
denominator remainder, its inverse remainder, and their product remainder
equal to one.  q-relation certificates include zero cross-multiplication
remainder and a separately checked q-denominator unit.  The gamma quotient
relation digests, in order `gamma0` through `gamma3`, are

```text
23530d959f75d98a6920695b9878ab02e7e60304c6f88cfbc2911fddb0df1c03
d9f1fdc4b8c6daa8bddd09e4b6413c2b7ae62ae966efa48a2e3a4461601105b7
b9e43cd1dfe9a4890d958a4647648fd335bfe819f303089b59f295f9d81e599c
5a6daf00b0bd95af7075876756f0e8a214cab166aab1b106496a3d3a04365baa
```

The independent audit uses copied immutable sparse supports and written
GLD88/F88 formulae.  It independently accumulates the sparse syndrome and
determinants, reconstructs the gamma atlas, recomputes all three pair
resultants, and derives every specialized q-gcd from those pair outputs with
its own exact q-Bezout implementation.  It checks the q denominator units,
q relations, Delta units, direct determinant identities, and the empty
`Q_other` gamma-gcd.  It does not import the GLD100, GLD96, or GLD99 verifier
modules and does not use GLD99 as an independent premise; GLD99 is only the
named H2 handoff.

The two replays agree on the support digest, gamma atlas, pair eliminants,
degree-374 full-content gcd, degree-18 radical, and all named branch
closures.  The independent q-gcd derivation obtains

```text
p=0: q-gcd q^2
p=1: q-gcd (q-1)^2
Q_gamma: q=-p, gamma-gcd a
Q_other: q=2-p, gamma-gcd 1
A4: (p-2)q-(2p-1)=0, gamma-gcd a, D0=unit*C^2
C4: (2p-1)q-(p+1)=0, gamma-gcd a-p, D2=unit*C^2.
```

## 6. Bounded replay provenance

Canonical primary replay:

```text
run id:       gld100-g0-primary-witness-pinned-final
run record:   .research-runs/gld100-g0-primary-witness-pinned-final/20260830T050152Z-35108/run.json
command:      python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_g0_gate_removal.py
status:       succeeded; child and runner exit code 0
bounded time: 554.929 seconds
script time:  552.244 seconds
runtime:      CPython 3.13.14, SymPy 1.14.0
```

Independent exact audit:

```text
run id:       gld100-independent-audit-hardened-reduced-c4-final
run record:   .research-runs/gld100-independent-audit-hardened-reduced-c4-final/20260830T053134Z-9708/run.json
command:      python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_g0_gate_removal.py
status:       succeeded; child and runner exit code 0
bounded time: 408.051 seconds
script time:  405.936 seconds
runtime:      CPython 3.13.14, SymPy 1.14.0
```

Both bounded runs use exact characteristic-zero arithmetic and exit code zero.
The primary's conclusion is the normalized `D(E31*Delta)` route after the
GLD99 H2 handoff, with the physical `D(Omega)` and GLD95 endpoint retained.

## 7. Nonclaims and retained frontier

GLD100 does not claim:

- a proof of the global Krenn--Gu conjecture, or any change from
  `UNRESOLVED`;
- that the six selected seven-minors characterize the full rank-at-most-six
  ideal; they are used only as necessary rank equations;
- that arbitrary H4/Q6 points enter the written GLD88/F88 offset chart;
- closure of `E31=0`, `Delta=0`, or `Omega=0` for the physical conclusion;
- removal of the physical `Omega` open, the `E31` open, or the `Delta` chart
  boundary;
- coverage of other H4 charts, gauges, components, equal-leaf ranks, source
  branches, profiles, roots, or orders;
- computation or emptiness of the GLD83 pulled-back Fitting ideal, source
  integrability, target attachment, graph lifting, or global gluing;
- sufficiency of a pair resultant root, absence of extraneous resultant
  roots, or pointwise use of a generic/function-field statement without the
  exact branch specialization;
- validity in positive characteristic or under an unlisted field
  specialization; or
- any conclusion about unrelated, withdrawn, superseded, or still-open
  proof-DAG branches.

The theorem removes the `g0` gate only for the exact normalized GLD96/GLD88
subroute stated at the beginning.  Its remaining load-bearing walls are
`E31`, `Delta`, the normalized-chart and `C_8=1` hypotheses, the GLD75/GLD86
bridge, GLD95, GLD99, and the physical `Omega` open.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.
