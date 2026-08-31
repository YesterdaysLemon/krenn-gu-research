# Four-root torus-star equal-leaf H4/Q6 B=0 C-open offset exclusion corollary (GLD106)

## Status and exact scope

**Proved exact scoped characteristic-zero corollary (`GLD106`) of GLD96,
GLD100, and GLD99.**  This package isolates a consequence already proved
inside the accepted GLD100 argument; it does not add a new elimination
computation.  Juniper and Kestrel accepted the immutable pre-promotion
candidate from fresh isolated exports, giving the required `2/2` external
consolidation.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

Work over `C` on the normalized, scale-fixed GLD88/F88 equal-leaf H4 offset
chart

```text
G = [1  1       1      ]
    [p  q       s      ]
    [a  1+b     1+c    ],

s = (p+q-pq)/(p+q-1),
b = b88(p,q,a) + B_offset,
c = c88(p,q,a) + C_offset.
```

Write

```text
d0      = p+q-1,
P       = p^2-p+1,
L1      = p^2+2pq-2p-q,
L2      = 2pq-p+q^2-2q,
e       = 2pq^2-2pq-p-q^2-2q+2,
Delta   = (p-q)d0 P L1 L2 e,
H2deg   = 2p^2-2p+1.
```

Let `M(G)` be the fixed GLD71 `37 x 9` syndrome.  The exact conclusion is

```text
V(B_offset,Q6) intersect D(C_offset*Delta)
  intersect {rank M(G) <= 6} = empty.                 (COPEN)
```

Thus, on this chart and on `D(Delta)`, a rank-at-most-six point with
`B_offset=0` must also have `C_offset=0`.  The parameter `a` is arbitrary.
No `E31` hypothesis occurs in the statement.

## 1. The four actual-minor equations at B=0

GLD96 writes denominator-cleared versions of its four actual bordered
seven-minors in the form

```text
Ttilde_i = D_i*T_i
         = f_i(B_offset) + C_offset*g_i(B_offset),
f_i(0)=0,                                               (1)
```

where the second identity is one of the 111 exact GLD88 common-kernel
identities.  The clearing factors `D_i` use only powers of `H2deg` and the
displayed family denominators, so they are units on `D(H2deg*Delta)` and use
neither affine offset.  Complete syndrome rank at most six implies `T_i=0`
and hence `Ttilde_i=0` for every `i=0,1,2,3`; this is only the forward
rank-to-minor implication.

At a point of `V(B_offset) intersect D(C_offset)`, equations (1) give

```text
g_0(0)=g_1(0)=g_2(0)=g_3(0)=0.                         (2)
```

On `D(H2deg*Delta)`, the exact Q6 reduction and primitive denominator
clearings used by GLD100 are reversible.  Therefore (2) is precisely the
common-zero condition for GLD100's four primitive coefficients
`gamma0,...,gamma3`.

The step from `T_i=0` to (2) uses `C_offset!=0` pointwise.  It neither divides
by an unproved polynomial nor asserts that the four selected minors generate
the full rank ideal.

## 2. Exhaustive H2deg split

Every point lies in exactly one of

```text
H2deg != 0  or  H2deg = 0.                             (3)
```

This is an exhaustive case composition, not cancellation of `H2deg` from an
identity.

### 2.1 H2deg-open branch

Assume `H2deg!=0`.  GLD100 computes an exact necessary pair-resultant cover
for a common zero of `Q6,gamma0,gamma1,gamma2,gamma3`.  Its squarefree
support is

```text
p*(p-1)*(p^2+1)*(p^2-2p+2)*(p^2-p+1)
 *(2p^2-2p+1)*A4*C4,

A4 = 5p^4-16p^3+30p^2-16p+5,
C4 = 8p^4-16p^3+12p^2-4p+5.
```

The resultant is used only in the necessary direction.  GLD100 then closes
every support pointwise: the `p` and `p-1` gamma branches force `p-q=0`, the
factor `P=p^2-p+1` is part of `Delta`, and `H2deg` is excluded in this case.
The `p^2+1`, `A4`, and `C4` fibres are closed by exact direct `D0` or `D2`
seven-minor identities with unit coefficients, while `p^2-2p+2` has no
common affine gamma zero.  Hence (2) is impossible on `D(H2deg*Delta)`.

Nothing in this gamma, pair-projection, or fibre-closure argument uses
`E31`.  In GLD100, `E31` is used only in the preceding general-chart step
that forces `B_offset=0`; the present corollary assumes `B_offset=0` from the
start.

### 2.2 H2deg-zero branch

Assume `H2deg=0`.  GLD99 is an exact arbitrary-`a` theorem on the same
normalized offset chart.  On `D(Delta)`, complete syndrome rank at most six
forces

```text
B_offset=C_offset=0.                                   (4)
```

Equation (4) contradicts `D(C_offset)`.  Combining the two cases in (3)
proves (COPEN).

## 3. Exact downstream use

The corollary removes the complementary `B_offset=0, C_offset!=0` chart from
the post-GLD105 `E31=0` obligation.  A future pointwise E31-wall proof may
therefore concentrate on

```text
V(E31,Q6) intersect D(B_offset*H2deg*Delta)
  intersect {rank M(G) <= 6} = empty,                  (5)
```

with GLD99 still supplying the separate `H2deg=0` case.  Statement (5) is a
downstream obligation, not a conclusion of this document.

## 4. Evidence boundary

The certificate pins the accepted GLD96 residual decomposition, both exact
GLD100 proof routes and review, and both exact GLD99 proof routes and review.
The primary checker validates the frozen interfaces and inspects the named
GLD100 gamma/pair/fibre functions for any hidden `E31` dependency.  The
independent audit imports no repository verifier and instead checks the
owner-section dependency boundary and the two-case logical composition.

The expensive GLD100 and GLD99 algebra is already owned by proved,
independently audited theorems.  This composition package does not rerun it
and cannot replace those upstream proofs.

## 5. Nonclaims and retained frontier

This corollary does not prove or assert:

- the remaining `D(B_offset)` part of `E31=0`;
- that a generic resultant or degree-620 support cover is pointwise closure;
- a converse from selected minors to complete syndrome rank;
- `Delta=0`, another normalization, pivot patch, gauge, or H4/Q6 chart;
- removal of `Omega=0` or a physical-incidence endpoint theorem;
- the GLD83 pulled-back Fitting ideal;
- another component, source branch, root number, or graph order;
- source integrability, target attachment, graph lifting, or global gluing;
  or
- a proof or refutation of the global Krenn--Gu conjecture.

The immutable candidate commit and tree were

```text
8001f3435702d642ccb86e10893000379cca7ae5
8b4b38f92c143aa557e039661ab7ecf046539181.
```

Its six-file `43,128`-byte diff has SHA-256
`b8b33767bd74677b4e09a3a78bdaece657e90a5dbcb681452ae0ff3ca3c5f915`.
Commons request `kgc_01M1C3T5Y83KSKVKG22HK0TCAH` received exact scoped
acceptances from Juniper (`kgc_01M1C3VG98735EV4JM8TEVE02V`) and Kestrel
(`kgc_01M1C468KR8XX1C8XC0EMEXPM3`).  These receipts justify only this scoped
corollary, not any endpoint, remaining wall, boundary, wider-chart, or global
conclusion.  The global status remains **UNRESOLVED**.
