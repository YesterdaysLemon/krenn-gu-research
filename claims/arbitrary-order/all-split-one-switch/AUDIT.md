# Independent audit of the all-split one-switch control

Date: 2026-09-22

## Verdict

**PASS at the stated finite mechanism-obstruction scope.**

The displayed `k=5` array is an exact countercontrol to any implication that
uses only one oriented family of one-switch rows, binary Hamiltonicity, and
the single hollow resource cycle to force a missing predecessor resource.
It is not a full source, does not disprove the bidirectional K4 straddling
lemma, and does not resolve the all-split residual or the Krenn--Gu
conjecture.

## What was checked independently

`independent_replay.py` shares only the displayed finite arrays with the
primary replay.  It reconstructs the protected matchings with the local XOR
involutions, derives resource assignments from the physical permutations,
uses a separate functional-graph cycle decomposition, and directly counts
perfect matchings of one selected physical-color graph.  It imports no
primary helper.

The independent replay establishes all of the following exactly:

1. `P,Q` are hollow Hamilton permutations and satisfy
   `P m_A P^-1=m_B`, `Q m_A Q^-1=m_C`.
2. Their derived resource maps are the displayed `FAB,FAC`.
3. Every literal forward switch `H_R(P->Q)` has one directed cycle, with
   lengths

   ```text
   16,14,13,15,18,13,11,11,11,18.
   ```

   The full `A` resources on those cycles agree with the claimed
   predecessor-compatibility sets.
4. The resource order

   ```text
   0,1,2,3,6,5,4,8,9,7
   ```

   selects an actual predecessor for every root, makes one hollow `C_30`,
   and saturates every forward base-`A` one-switch row.
5. Exactly 160 of the `2^10` endpoint orientations of the `B--C` resources
   make `D_BC` Hamilton.  For every such orientation the base-`A` forward
   system passes and the corresponding base-`B` and base-`C` systems fail.
6. The reverse base-`A` root condition succeeds only at roots `0,9`.
   Root `1` gives the displayed mixed physical word

   ```text
   22022002222020222122.
   ```

7. The independent replay reconstructs the two-switch physical word

   ```text
   01002002010000112012
   ```

   on the canonical all-straight support and counts its physical perfect
   matchings directly.  The count is exactly **one**.  This is a literal
   support-level proof of a nonzero mixed coefficient and does not rely only
   on replaying the switched-cycle formula.
8. The six-vertex auxiliary example satisfies both oriented root conditions,
   while its conjugate matchings do not commute.  Since it also lies outside
   `|V|=4k` and physical hollowness, it refutes only an unrestricted
   cyclic-order proof with the physical K4 hypotheses omitted.  It does not
   isolate the Klein relation as the sole necessary missing hypothesis.

The primary replay independently checks the same finite array, the 160-case
orientation enumeration, the forward/reverse systems, and the displayed
mixed witnesses.  Both scripts pass from a neutral working directory using
only the Python standard library.

## Quantifier and parent correspondence

For base color `A`, the forward switch is the source word with background
`B` and one exceptional `C` resource; the only `B->C` boundary is the
resource-cycle edge from the actual predecessor `R^-` into the exceptional
root `R`.  The parent boundary-hitting condition therefore requires every
directed cycle to contain all four endpoints of `R^- union R`.  The finite
control satisfies this requirement for every root.

Interchanging background and exceptional colors gives `H_R(Q->P)`.  A full
source supplies this opposite orientation as well.  The control fails that
root condition, and it also has an explicit multi-switch mixed word with a
unique matching.  Consequently it refutes only the forward-only mechanism;
it is not a counterexample to the full boundary obligation or to full-source
elimination.

The open bidirectional K4 straddling lemma has the correct logical direction:
a proof would contradict the simultaneous pair of root systems supplied by
a hypothetical full source.  Neither replay proves that all-order lemma.

## Review repair and evidence boundary

During review, the primary script's auxiliary six-vertex check initially
called a cycle routine over the global 20-vertex domain and failed with a
`KeyError`.  The owner made the routine domain-size-parametric.  The corrected
primary replay and the independent replay both pass; the hashes below refer
only to the corrected files.

The exhaustive `2^10` enumeration is exhaustive for the endpoint
orientations of this displayed `k=5` control.  It is not an exhaustive cover
of all `k`, all all-split supports, or all full-source equations.

## Reproduction

From repository root (or use the corresponding absolute script paths from a
neutral working directory):

```text
python claims/arbitrary-order/all-split-one-switch/replay.py
python claims/arbitrary-order/all-split-one-switch/independent_replay.py
```

Reviewed hashes:

```text
README.md             8B795957259187123579681A2157908BFA97C42846CB9259C39112BF7504A8B2
replay.py             D71EFB56390918964C4308B35700447270C1813786A41B8263C30FCDABEBBFA4
independent_replay.py A539D60BCCBE37B811D52D6AACB1F26611A24034474C6BECC567552FD2767945
```
