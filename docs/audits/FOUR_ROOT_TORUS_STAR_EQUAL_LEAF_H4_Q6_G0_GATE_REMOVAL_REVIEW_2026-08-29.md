# GLD100 g0 gate-removal hostile review

## Verdict

**Verdict: PASS for the exact `GLD100` scope.**  The source-recomputed
primary certificate and the no-import independent audit both pass on frozen
supports and exact arithmetic.  Together with the already proved GLD96,
GLD99, and GLD95 edges identified below, this is sufficient to promote the
owner to a proved scoped characteristic-zero theorem.

The promotion is narrow.  It removes the `g0` gate only on the normalized
GLD88/F88 offset route.  The combined normalized implication retains
`D(E31*Delta)`; its physical incidence consequence additionally retains
`C_8=1`, the GLD75/GLD86 bridge, `D(Omega)`, and the GLD95 F88 endpoint.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Exact claim audited

Let

```text
U88 = {scale-fixed equal-leaf H4 chart, b=b88+B, c=c88+C}
      intersect D(Delta).
```

Here the leaf offset `C` is distinct from the incidence-center coordinate
`C_8`.  The primary generic theorem is

```text
U88 intersect V(Q6) intersect D(E31*H2*Delta)
  intersect {rank M(G) <= 6}
    is contained in {B=0,C=0} = F88.
```

GLD96 supplies `B=0` on this open; that cross-resultant subargument never
uses `g0` and does not invert `R31`.  At `B=0`, GLD100 proves the missing
`C=0` implication.  GLD99 separately supplies the `H2=0`, `Q6=0`,
`D(Delta)` degree-drop branch, so the combined normalized implication is on
`D(E31*Delta)`.  GLD95 is used only after `B=C=0`, as the downstream F88
endpoint.

On the `C_8=1` incidence-center slice, the corresponding physical statement
is

```text
B_incidence intersect V(I_7(A)) intersect U88 intersect {C_8=1}
  intersect H4 intersect V(Q6) intersect D(E31*Delta)
  intersect D(Omega) = empty.
```

No part of this review removes `E31`, `Delta`, or physical `Omega`.

## Authoritative bounded replays

The accepted primary run is:

```text
run id:       gld100-g0-primary-witness-pinned-final
run record:   .research-runs/gld100-g0-primary-witness-pinned-final/20260830T050152Z-35108/run.json
command:      python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_g0_gate_removal.py
status:       succeeded; child and runner exit code 0
elapsed:      554.929 seconds (script runtime 552.244 seconds)
runtime:      CPython 3.13.14, SymPy 1.14.0
final line:   GLD100 g0 gate-removal exact certificate: PASS
```

The accepted independent run is:

```text
run id:       gld100-independent-audit-hardened-reduced-c4-final
run record:   .research-runs/gld100-independent-audit-hardened-reduced-c4-final/20260830T053134Z-9708/run.json
command:      python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_g0_gate_removal.py
status:       succeeded; child and runner exit code 0
elapsed:      408.051 seconds (script runtime 405.936 seconds)
runtime:      CPython 3.13.14, SymPy 1.14.0
final line:   GLD100 independent exact audit: PASS (scoped leaf computational audit; global Krenn--Gu remains UNRESOLVED and no global proof is claimed)
```

Both commands run through `tools/research/run_bounded.py` in the recorded
runs.  The ignored run logs are execution provenance; the durable scripts,
owner, frozen hashes, and this review are the repository evidence.

## Exact primary certificate surface

The primary recomputes the ten-row GLD71 support

```text
rows = (0,1,2,3,17,25,28,31,32,33)
support digest = c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0
```

and checks a full source manifest for GLD71, GLD88, GLD95, GLD96, and GLD99.
It reconstructs all four affine-in-`C` residual coefficients, including the
raw denominator identities, exact `Q6` quotient inverses, primitive contents,
and canonical sparse hashes.  It then recomputes all three pair projections.

The exact common full-content gcd has

```text
degree                 374
sha256                 f8bfaa97e9d980852df37e1c98bc82769aba0ab3a762452b55bb0696697d42d2
squarefree degree      18
squarefree sha256      dd930e75eaf842e522b08b661739c53693bb5a7de45414851651e36f291d4361
```

Its radical is the eight-factor necessary cover

```text
p, p-1, p^2+1, p^2-2p+2, p^2-p+1,
2p^2-2p+1, 5p^4-16p^3+30p^2-16p+5,
8p^4-16p^3+12p^2-4p+5.
```

Every retained fibre record is compared unconditionally with a frozen hash.
The records include canonical exact Bezout coefficients and identities,
pair-content and clearing-scale unit witnesses, q-relation denominator
inverses, `Delta` unit or divisibility witnesses, direct-minor coefficient
inverses, canonical direct determinants, the `P` divisor record, and the
pinned GLD99 `H2` handoff.  There is no truthiness or empty-map bypass.

## Necessary projection and exhaustive fibre closure

The pair-resultant bridge is used only in the valid direction

```text
Q6 = gamma0 = gamma1 = gamma2 = gamma3 = 0
    => p lies over a common root of all three pair eliminants.
```

Resultant roots may be extraneous.  That causes no gap because all eight
support factors are retained and closed separately:

| support | exact closure |
| --- | --- |
| `p` | audit and primary derive q-gcd `q^2`; it divides specialized `Delta` |
| `p-1` | derive q-gcd `(q-1)^2`; it divides specialized `Delta` |
| `P=p^2-p+1` | exact displayed factor of `Delta` |
| `H2=2p^2-2p+1` | retained degree drop, handed to proved GLD99 |
| `p^2+1` | derive `q=-p`, gamma gcd `a`; `D0=192(1-p)C^2` with unit coefficient |
| `p^2-2p+2` | derive `q=2-p`; common affine gamma gcd is `1` |
| `A4` | derive `(p-2)q=2p-1`, gamma gcd `a`; exact unit times `C^2` in `D0` |
| `C4` | derive `(2p-1)q=p+1`, gamma gcd `a-p`; exact unit times `C^2` in `D2` |

`H2` is the literal q-leading coefficient of `Q6`.  The generic quotient
calculation therefore localizes at `H2`, and GLD99 handles that locus rather
than any silent cancellation.  Likewise every removed pair content and
clearing scale is proved to be a unit before specialization.

## Independent audit boundary

The independent script imports none of the primary, GLD96, GLD99, or
exploratory run modules.  It copies the sparse supports and written family
formulas, reconstructs the generic gammas, recomputes all pair resultants and
both gcd variants, and derives all six specialized q-gcds from its own raw or
primitive pair outputs.  The `p=0` computation intentionally uses raw
resultants because removed p-content vanishes there.

For every nonboundary quadratic or quartic fibre the audit replays the common
gamma gcd.  For the three direct branches it computes sparse exact
determinants and independently evaluates the dense 7-by-7 permutation
determinant at `C=0,1,2`, after asserting degree at most two.  Three exact
values determine those polynomials.  It also cross-checks that each q root
derived from the pair projection is the same q root used by the gamma/direct
replay.

This is independent at the derivation, import, representation, and dense
determinant-control layers.  It still shares the mathematical GLD71/GLD88
inputs and SymPy's exact polynomial arithmetic; it is an independent
computational audit of the proof leaf, not a second independent mathematical
proof of all upstream theorems.

## Adversarial findings and repairs

The hostile review found and required the following repairs before PASS:

1. Empty/conditional fibre pins were replaced by a complete, unconditional
   eight-record map.
2. Console-wrapped gamma and pair hashes were replaced by exact machine-read
   values and checked against a clean replay.
3. Hash-only gcd coefficients were replaced by serialized exact Bezout
   witnesses with verified identities.
4. Pair clearing scales, q denominators, `Delta`, and direct `C^2`
   coefficients received explicit inverse witnesses.
5. The audit's optional gamma path became mandatory for every retained
   branch.
6. The audit now derives its q-gcds from its own pair outputs and links those
   roots to the subsequent branch calculations.
7. A one-point dense control became a three-point exact polynomial control.

Two hardened audit attempts failed before the accepted run: one tried to
coerce an algebraic alias as a polynomial in the source symbol, and one left
`p` unspecialized in the expected `C4` gcd `a-p`.  Both are implementation
failures, not mathematical evidence.  The corrections were exercised by the
accepted full run.  An earlier long substitution attempt was intentionally
terminated by its owning process after preserving its log; reducing modulo
the fibre before algebraic substitution produced the same exact operation
with bounded cost.

## Parent-theorem checkpoint

GLD100 is a parent-level synthesis, not a third nearby sibling refinement.
Its exact parent proposition is the normalized `D(E31*Delta)` offset
implication.  It combines the GLD96 `B=0` mechanism, the all-fibre `C=0`
cover, the GLD99 degree-drop theorem, and the GLD95 endpoint.  The proof
topology delta is the removal of both `g0` and `H2` from that combined route.

The sharp controls were the extraneous resultant fibres, the `H2` degree
drop, the `p=0,1` content strata, the quartic denominator units, and the
direct rank minors.  The resulting next load-bearing parent obligation is
`E31=0` on `D(Delta)`, not another refinement of a closed fibre.  `Delta=0`
remains a separate boundary synthesis.

## Retained obligations

GLD100 does not close `E31=0`, `Delta=0`, or `Omega=0` for the physical
incidence conclusion.  It does not cover arbitrary H4/Q6 points outside the
written GLD88/F88 offset chart, other gauges or charts, unequal-leaf or other
components, source branches, roots, or orders.  The GLD83 pulled-back Fitting
ideal, raw-response and higher-rank lanes, source integrability, graph
lifting, target attachment, and global gluing remain open.  Positive
characteristic and unlisted specialization claims are outside scope.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.
