# Hostile review of fixed-pair singleton-exceptional companion propagation

## Verdict and exact scope

**PASS, for the stated fixed-pair, pointwise, characteristic-zero,
singleton-supported exceptional-low scope.**  No contraction, quotient,
rank-nullity, support, colour, return-kernel, dependency, implementation, or
scope blocker survived hostile review.

The package assumes that a rank-two local projection has a kernel generator
on one of the exceptional ambient lines and that this generator is supported
on one local colour.  It proves that another local plane meets an explicit
line or two-plane, forces the local colour of that companion, and computes
the residual kernel obtained by iterating the same argument once.

This is a finite incidence reduction.  It does not prove that every
exceptional low is singleton-supported, that any displayed cycle is
realizable, that the propagating mode is unique, or that the fixed pair is
excluded.  A return arrow means that propagation can return to the original
ambient line; it does not select the original mode uniquely.  Unrestricted
`P_6 -> Delta_3` nonrestriction remains unknown, and the global Krenn--Gu
conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_SINGLETON_EXCEPTIONAL_COMPANION_PROPAGATION_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_singleton_exceptional_companion_propagation.py
  audit_arbitrary_permanent_fixed_pair_singleton_exceptional_companion_propagation.py
```

Load-bearing frozen predecessor:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_EXCEPTIONAL_KERNEL_NECESSITY_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_exceptional_kernel_necessity.py
  audit_arbitrary_permanent_fixed_pair_exceptional_kernel_necessity.py
```

The predecessor in turn imports the exact target equations and forced missing
colours from the frozen kernel-support package.  This review checked those
uses against the committed theorem rather than treating a filename or prior
review as proof.

## 1. Independent quotient and rank-nullity derivation

Let `Q subset R^*` have dimension `d>=2`, set `H=ann_R(Q)`, and quotient
`R` by `H`.  The induced ambient space is

```text
W_bar=(R/H) direct-sum A,             dim W_bar=d+2.
```

If a local three-plane `L` misses `H`, the quotient map is injective on
`L`; hence the images of its three ordered colour vectors remain linearly
independent.  This is the exact hypothesis needed by the one-diagonal
lemma.  No complement of `L`, generic position, or surjectivity is assumed.

For an off-surviving pair of colour labels, the map

```text
w |-> C(y_(s,i),y_(u,j),w) : W_bar -> R/H
```

kills the three-dimensional image of the third local plane.  Rank-nullity
therefore gives

```text
rank <= (d+2)-3=d-1.
```

On the `R/H` summand its restriction is scalar multiplication by the
pairing of the two `A`-components.  A nonzero scalar would have rank `d`,
so every required cross-colour pairing vanishes.  A nonzero surviving
diagonal value forces at least one same-colour pairing to be nonzero.  For
the other two colours in the third mode, the tensor equation then forces
their `R/H` components to vanish, while cross-orthogonality puts both
`A`-components in the same one-dimensional orthogonal complement.  Their
images are dependent, contradicting injectivity of the local triple.

Consequently some remaining local plane meets `H`.  A vector in this
intersection lies in `R`, has zero `A`-part, and annihilates every residual
covector in `Q`; its double contraction is therefore zero in every channel.
If the original singleton colour is `e`, the nonzero `d_e` target makes its
local `e`-coefficient zero.  This justifies the package's propagated
missing-colour statement without confusing ambient support with local
colour support.

## 2. Six exceptional contractions

Independent direct contraction of the five displayed complementary
quartics gives the following residual spans and common kernels.  Here signs
of spanning covectors are immaterial, but all ranks and kernels were checked
over the rationals.

```text
source       residual-span generators          rank   common kernel

Phi_1 N      h_0, h_1                            2     <x_0+x_1,x_2-x_3>
Phi_1 A_0    h_2, h_1, x_1                      3     K(x_0-x_3)
Phi_1 C_0    h_2, h_0, x_1                      3     K(x_0+x_2)

Phi_2 N      h_0, h_1                            2     <x_0+x_1,x_2-x_3>
Phi_2 A_1    h_2',h_0, x_0                      3     K(x_1-x_3)
Phi_2 C_1    h_2',h_1, x_0                      3     K(x_1+x_2)
```

The two copies of `N` are the same ambient line but arise in different
projection families.  The predecessor's forced-zero table gives

```text
N misses 2;  A_0 misses 0;  C_0 misses 1;
             A_1 misses 1;  C_1 misses 0.
```

Thus the singleton hypotheses have exactly the colours listed in the new
theorem: `N` may be on colour `0` or `1`; `A_0` on `1` or `2`; `C_0` on
`0` or `2`; `A_1` on `0` or `2`; and `C_1` on `1` or `2`.  The theorem does
not silently infer singleton support from the predecessor, which proves
only support at most two on exceptional lines.

## 3. Forced companion colours

The four one-dimensional companion kernels are

```text
U_0=x_0-x_3,  V_1=x_0+x_2,
U_1=x_1-x_3,  V_0=x_1+x_2.
```

Their exact contractions give two mixed/diagonal identities apiece:

```text
U_0: m_1=d_2 and m_2=d_1;
V_1: m_1=d_2 and m_2=d_0;
U_1: m_2=d_2 and m_1=d_0;
V_0: m_2=d_2 and m_1=d_1.
```

Because each mixed target vanishes and each diagonal target has a nonzero
coefficient on a distinct local diagonal cell, these identities force two
local coefficients of the companion vector to vanish.  The surviving
colours are respectively

```text
U_0: 0,   V_1: 1,   U_1: 1,   V_0: 0.
```

This inference remains valid for arbitrary nonzero target scalars
`lambda_c`; it uses only their nonvanishing and never identifies them.

For the common-line kernel plane, every companion has

```text
q=s(x_0+x_1)+t(x_2-x_3)=(s,s,t,-t).
```

Direct contraction gives equal `d_0` and `d_1` residuals.  On the target,
those are supported on distinct diagonal cells, so equality forces both the
colour-`0` and colour-`1` coefficients of `q` to vanish.  Since `q` is
nonzero, it is singleton-supported at colour `2`.  Its `d_2` contraction is

```text
-2s(x_0+x_1),
```

and the nonzero `d_2` target therefore forces `s!=0`.  This checks the
claimed active-parameter condition; `t` is allowed to vanish or equal
`-s`.

## 4. One-step return graph

Contracting again by the four forced line companions produces rank-three
residual spans with the following one-dimensional common kernels:

```text
U_0 colour 0 -> K A_0;
V_1 colour 1 -> K C_0;
U_1 colour 1 -> K A_1;
V_0 colour 0 -> K C_1.
```

The propagated vector on the return step misses the displayed companion
colour, in agreement with the predecessor's exceptional missing-colour
table.  The original mode already supplies an allowed return incidence, so
this computation yields no contradiction and forces no third distinct
mode.

For `q=(s,s,t,-t)` with `s!=0`, the residual covectors are generated by

```text
sL-2t x_1,  sL-2t x_0,  (s+t)L,  -2s(x_0+x_1),
L=-x_0-x_1-x_2+x_3.
```

If `t!=0`, the difference of the first two generators supplies
`x_0-x_1`, the last supplies `x_0+x_1`, and either first generator supplies
the independent `L` direction.  The rank is three and the common kernel is
`K N`.  If `t=0`, the span is exactly
`<L,x_0+x_1>`, of rank two, with common kernel

```text
span{N,x_0-x_1}.
```

These are exhaustive because `s!=0`.  In particular, the case `s+t=0`
still lies in the rank-three `t!=0` regime.  The computed graph classifies
the next residual kernel, not the existence or uniqueness of a geometric
cycle.

## 5. Computational replay and independence

Focused replay passed:

```text
new primary exact verifier:                         PASS;
new independent no-import audit:                    PASS;
exceptional-kernel predecessor primary:             PASS;
exceptional-kernel predecessor independent audit:   PASS;
py_compile on both new scripts:                     PASS;
Ruff on both new scripts:                           PASS;
untracked-package whitespace checks:                PASS.
```

The primary verifier uses SymPy to reconstruct every residual span and
kernel, verify all forced-colour identities symbolically, and classify the
common-plane return for symbolic `s,t`.  The independent audit imports
neither the primary module nor SymPy: it reconstructs the square-free
quadratics from coefficient dictionaries, contracts them directly, and
uses custom rational row reduction.  It also stress-tests the quotient rank
gap and orthogonal-line step over `F_3`, `F_5`, and `F_7`.  Those finite-field
checks audit displayed linear algebra only; the written argument is the
characteristic-zero proof.

Selected exact outputs were:

```text
six exceptional family-line cases:                    6;
exceptional residual ranks:                      2 or 3;
four forced line-companion identities:                 4;
four exact line-return kernels:                        4;
common-plane rational parameter samples:               5;
finite fields used for rank-gap stress:             3,5,7.
```

## 6. Accepted boundary

```text
fixed pair and exact full target:                         YES;
exceptional low is singleton-supported:                  ASSUMED;
companion line or plane in another mode:                  PROVED;
companion local colour and N-plane s!=0:                  PROVED;
one-step residual-kernel return graph:                    PROVED;
existence, uniqueness, or exclusion of a cycle:           OPEN;
support-two exceptional lows:                             OPEN HERE;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

## Final reviewed hashes

```text
new theorem:
EF703D8B5EA711945D6384A93F2542F8A84F2D5140FBB2B7D2F1CB944D25EA57

new primary verifier:
DA739D69E795B7A030969B5C180A0999610A32259E7C9A6371F472E6C6E34B0F

new independent audit:
5B6527C7D37D66299E3244FFC2C248D44DD3BF126E177DD3CB7354F86D666B76

exceptional-kernel predecessor theorem:
2FAB590264EDE5999F55540F2234BE2055637386B978D77469F592F58B004B60

exceptional-kernel predecessor primary verifier:
256D1F4DEB3639E912E41C426E2D28E5FCB384C72DCDB00F9592064D33C904E5

exceptional-kernel predecessor independent audit:
90014EC8E37B0F48F26BD4A9528E235F2FC26D5E757948E34B1744B1B743D6F1
```
