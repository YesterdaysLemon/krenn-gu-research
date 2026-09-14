# Eight-vertex physical boundary quotient on the 134-entry support

## Status and scope

This is an **exact finite limitation of one cancellation mechanism** on one
fixed physical support. It is not an exclusion of that support, a weighted
witness, a classification of eight-vertex witnesses, or an all-order result.
The unrestricted `n=8` problem and the global Krenn--Gu conjecture remain
**UNRESOLVED**.

The computation starts from commit
`049cc885b825c2de13e6d6f00d1a9422b49f7ef3` and the preserved 134-entry
physical projection. The projection is one checked Boolean support assignment,
not a realization by complex weights.

## Reconstructed source consequence

Physical entries use one-based ids

```text
id(W_uv[a,b]) = 9 * (u*(15-u)/2 + v-u-1) + 3*a + b + 1
```

for `u<v`; reversing an edge also reverses its endpoint colours. Starting from
the complete perfect-matching expansions at the four words

```text
00000010, 00000110, 00100000, 00100100,
```

impose only the following 17 source zero assumptions:

```text
19, 73, 92, 109, 163, 181, 182, 190, 199,
200, 208, 209, 217, 229, 230, 235, 238.
```

The derivation requires exactly these six physical entries to be nonzero:

```text
38, 55, 82, 118, 121, 247.
```

All unlisted entries remain arbitrary. In particular, no nonzero assumption is
made on entries `172`, `173`, `226`, `227`, or `244`, or on the proper
cofactors below. Put

```text
a=118, b=121, c=172, d=173, x=38, y=82,
z0=244, z1=247, s=226, t=55, e=227,
H=h(0145;0000),
K0=h(012467;000010), K1=h(012467;001000).
```

Direct expansion after the 17 zeros gives term counts `10,8,10,8` and

```text
F1 = a*z1*H + c*K0 + a*e*t*y
F2 = a*x*y*z1 + d*K0
F3 = b*(s*t*y + z0*H) + c*K1
F4 = b*x*y*z0 + d*K1.
```

Let `D=s*z1-e*z0`, `N=a*b*t*y*D`, and

```text
R = a*z1*(d*F3-c*F4) - b*z0*(d*F1-c*F2).
```

Sparse integer-polynomial expansion verifies `R=d*N` and

```text
N*F2 - K0*R = a^2*b*t*x*y^2*z1*D.
```

Thus, if all four `Fi` vanish, the six nonzero assumptions force

```text
g226*g247 = g227*g244.
```

This is division-free. In particular, it does not fix a proper-cofactor value
or support.

For vertex map `[0,6,2,3,7,5,1,4]` and common colour map `[0,2,1]`, the
fixture satisfies all mapped premises and the consequence becomes

```text
g88*g91 = g82*g97.
```

All four factors are live on the fixture.

## Bounded exact experiment

The declared budget was one local Python process, 120 seconds wall time, and
2 GiB memory. The main run completed in under two seconds; its independent
audit completed in under ten seconds. No `n=10` archive replay was run.

The probe exhausts all `8! * 3! = 241920` allowed vertex/common-colour images
of the source premises. Exactly two images apply to the support:

- one has both consequence monomials live and yields the single distinct
  relation above;
- one has both consequence monomials zero;
- none has exactly one live side, so this orbit gives no support
  contradiction.

It then enumerates every complete full-word perfect-matching fibre on the
support. Among all 6,558 mixed words there are 52,840 live matching monomials.
The smallest mixed fibre has three terms; no mixed fibre has zero, one, or two
terms. The pure-word fibre sizes are 5, 8, and 10.

Finally, the probe quotients every mixed fibre by the exact integer lattice of
the live boundary relation. No two matching monomials are identified, no
fibre becomes a singleton Laurent class, and the closest fibre still has
three terms in three classes. Structurally, the relation sides are

```text
W14[2,0]*W15[0,0]  and  W14[0,0]*W15[2,0].
```

Each side repeats vertex 1, whereas a perfect-matching monomial uses every
vertex once. A relation side therefore cannot occur as a submonomial of a
full-word matching term. Direct termwise transport of this binomial is inert
on the full fibres.

## Reproduction and independent check

The frozen result is
[`eight_vertex_physical_boundary_quotient_134.json`](../../../tests/fixtures/eight_vertex_physical_boundary_quotient_134.json).
It pins the physical-support bytes at SHA-256
`75cef4c3c16323a01b115d59bdbf19ddfe2b8e46a3a330333631837a6c9941fe`.

Reproduce the result exactly with:

```text
python tools/explore/probe_physical_boundary_quotient_134.py \
  tests/fixtures/recursive_physical_support_n8_four_cut_survivor_134.json \
  --expected tests/fixtures/eight_vertex_physical_boundary_quotient_134.json
```

Run the independently implemented SymPy/bitmask audit with:

```text
python claims/finite/n08/audit_eight_vertex_physical_boundary_quotient_134.py
```

The audit reconstructs the four source equations and division-free identity,
uses a separate physical-id formula and matching generator, repeats the full
orbit and fibre census, and checks directly that no same-word matching pair
differs by the live relation.

## Interpretation and next obligation

This result eliminates only direct Laurent quotienting by all applicable
images of this one reconstructed boundary consequence. It does not say that
larger source equations, shared proper coefficients, or combinations across
different words cannot exclude the support. The three nearest placements of
the earlier 25-literal pattern remain diagnostics, not an exhaustive witness
classification. Its bichromatic physical pattern is not applied to an
all-diagonal source without a proved transformation.

The single best next step is a bounded exact Laplace-module calculation at
the shared vertex 1: retain the complete six-vertex cofactors as common
polynomial coefficients, add the verified boundary relation, and test
degree-bounded S-polynomial or Macaulay combinations without assigning those
cofactors values or supports.

No current-frontier update is made because this experiment proves no new
theorem, withdraws none, closes no frontier branch, and changes no reduction
edge. It records a precise obstruction to one proposed mechanism only.
