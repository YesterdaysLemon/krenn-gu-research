# Hostile review of matrix-unit GHZ diagonal-torus endpoint balance

## Verdict and provenance

**PASS, as an exact support-minimality theorem and a sharp active-transport
boundary.**  The proof establishes an exact alternative for a fixed
matrix-unit label support:

- either a GHZ-preserving integral diagonal one-parameter subgroup gives
  nonnegative exponent to every physical block and positive exponent to at
  least one block; or
- every physical edge has positive integral multiplicity in an
  endpoint-label multicover with vertex-independent colour loads.

The first alternative produces a same-target graph with strictly smaller
support.  It follows that a globally support-minimal hypothetical witness in
the matrix-unit branch must satisfy the second alternative.

The eight-vertex table is accepted only as sharpness.  It has exact pure
targets and two target-correct active fibres joined by the exact forced
ternary bridge label pattern, but it has another mixed coefficient equal to
one.  It is not a witness or counterexample, and therefore does not certify
absence or presence of the imported geometric deeper component.  The `r=1`
branch and global Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. The diagonal action preserves exactly the GHZ target

For an exponent array `beta_(v,c)`, an edge with endpoint labels `(a,b)` is
scaled by

```text
t^(beta_(u,a)+beta_(v,b)).
```

Every matching uses one endpoint label at every vertex, so the whole
coefficient of a word `chi` is scaled by

```text
t^(sum_v beta_(v,chi(v))).
```

For a constant colour-`c` word this exponent is `sum_v beta_(v,c)`.  The
three zero-sum conditions in the theorem therefore fix all three nonzero
GHZ coordinates, while every mixed target coordinate remains zero.  No
claim is made that this torus fixes an arbitrary tensor.

The sign convention is immaterial: replacing `beta` by `-beta` exchanges
the two local-action conventions.  The proof fixes the convention by
defining the transformed edge coefficient explicitly and checks the target
coefficient directly.

## 2. Negative local exponents do not invalidate the limit

An erasing direction may have negative individual `beta_(v,c)`.  The local
diagonal matrices are consequently singular or unbounded at `t=0`.  That is
not the limiting object used in the theorem.

The physical edge exponent is the **sum at the two labels actually carried
by that matrix unit**.  Every such sum is nonnegative by hypothesis.  Thus
all physical blocks have finite limits, and at least one tends to zero.
Each perfect-matching coefficient is a polynomial in those finite edge
entries.  Equality with `Delta_(n,3)` holds for every nonzero `t`, hence also
at `t=0`.  The limiting graph is a valid same-order realization with fewer
nonzero blocks.

The limit may leave the maximum-root-one stratum.  That is allowed and is
load-bearing: support minimality is global among hypothetical graph
realizations, not minimality only inside the open complete-matrix-unit
stratum.

## 3. The theorem of alternatives has the right strictness

Let `S` be the image of the zero-colour-sum exponent subspace in edge
exponent space.  The erasing case is exactly

```text
S intersect R_(>=0)^E != {0}.
```

If this fails, `S` is disjoint from the standard nonnegative simplex.
Strict separation gives a functional which vanishes on the subspace and is
strictly positive on every coordinate vertex of the simplex.  Hence every
edge coefficient `p_e` of the functional is strictly positive.

Orthogonality to `S` says that the transpose incidence load belongs to the
orthogonal complement of the zero-colour-sum space.  That complement is
exactly the span of the three global colour-sum vectors.  This yields one
common load `q_c` for every vertex in colour `c`.

All matrices and cones are rational.  A nonempty relatively open positive
cell in the rational orthogonal subspace contains a rational point; clearing
denominators gives positive integers.  Conversely, pairing a positive
balance with a nonzero nonnegative exponent vector gives a strictly positive
number and zero simultaneously.  The two alternatives are therefore
mutually exclusive as stated.

Weak nonnegative dual weights would not suffice: an edge with zero dual
weight could still be erased.  The proof correctly obtains and uses strict
positivity on **every** physical edge.

## 4. The common loads really are positive on a target realization

The linear alternative alone permits a common colour load to be zero if no
edge ever carries that local label.  A realization of `Delta_(n,3)` cannot
have this defect.  Its nonzero constant colour-`c` coefficient contains at
least one nonzero pure-`c` perfect-matching term, so every vertex has an
incident half-edge labelled `c`.  Strict positivity of every balance weight
then gives `q_c>0`.

This inference uses only the finite expansion of a nonzero coefficient.  It
does not assume positivity or absence of cancellation among complex terms.

## 5. Auxiliary balance weights are not physical amplitudes

The integers `m_e` come from a real separating functional on the label
incidence matrix.  The physical edge amplitudes `lambda_e` remain arbitrary
nonzero complex numbers.  In particular, endpoint balance does not supply:

- a positive measure on perfect matchings;
- a triangle inequality for a mixed coordinate;
- equality between a cross-edge product and its bridge product;
- noncancellation of a pure-shore hafnian; or
- a termwise coupling of diagonal and offdiagonal responses.

The multicover language is accepted only as an exact integer incidence
certificate.  Treating `m_e` as amplitudes would be a status-changing error.

## 6. The eight-vertex sharpness table is exact and properly scoped

The primary and independent checkers agree on all of the following:

```text
physical pairs present:                     28 of 28;
label load at every vertex:                 (3,2,2);
pure coefficients:                          (1,1,1);
perfect matchings enumerated:               105;
chi_0 diagonal/offdiagonal values:           (1/2,-1/2);
chi_1 diagonal/offdiagonal values:           (1/2,-1/2);
an exposed mixed coefficient:               1.
```

At `chi_0`, the cross core is exactly the one-each ternary triad

```text
04=(0,1), 15=(1,2), 23=(2,0).
```

Its forced bridges are present with the required labels

```text
24=(0,0), 05=(1,1), 13=(2,2),
```

and, with residual edge `67`, induce `chi_1`.  Since `chi_1` also has
nonzero diagonal and offdiagonal aggregates of opposite sign, the table
realizes the support, word-change, and scalar algebra of the transport case,
not merely a support-level word flip.  It is not an instance of the full
trichotomy because it fails other target coordinates.

The next selected binary core at `chi_1` has the opposite bridge labels on
`05` and `67`, so it fails the next no-deeper forced square pattern.  No
geometric deeper-component conclusion is drawn from a nonwitness table, and
the table does not construct an active holonomy cycle.  The unique exposed
matching for `(0,0,0,0,0,0,2,0)` proves immediately that the table fails the
full mixed target system.

Every physical block is a nonzero coordinate monomial, so no pair of torus
vectors can annihilate an edge.  The asserted maximum torus-root number one
is therefore exact for the table, despite its failure to be a witness.

## 7. Computational independence

The primary verifier uses recursive labelled perfect matchings, a split
diagonal/offdiagonal ledger, explicit endpoint loads, and direct integer
Laurent exponents.  It also supplies an erasing direction for the earlier
six-vertex active table.

The independent audit imports no primary code.  It encodes endpoint labels
as decimal pairs, uses a least-set-bit compatible-hafnian recursion, counts
half-edges directly, checks the Laurent pairing on separately generated
zero-sum exponent arrays, and audits the bridge labels through compatibility
masks.  Both finite programs audit the table and sign conventions.  Neither
program is presented as a computational proof of the arbitrary-order strict
alternative; that proof is the separation and limiting argument in the
claim document.

## 8. Accepted proof-topology update

```text
support-minimal matrix-unit GHZ realization
  -> no support-erasing diagonal GHZ direction          PROVED
  -> positive all-edge endpoint-label multicover        PROVED
  -> common colour loads q_0,q_1,q_2 all positive       PROVED
  -> local active-transport algebra excluded by balance FALSE
  -> balance plus full mixed equations closes r=1       OPEN

r=1 matrix-unit branch:                                 OPEN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

The endpoint-balance node is an additional necessary condition on every
support-minimal candidate.  It does not replace the active-response,
partial-bridge, or deeper-blocker nodes and does not change their lifecycle
or mathematical status.

## Strongest fresh-referee objection

The tempting overstatement is to call the positive incidence multicover a
positive decomposition of the GHZ amplitudes and then rule out complex
cancellation by convexity.  That is false: the multicover weights are dual
certificates for the **label support**, not the physical complex weights.
The theorem is accepted because it uses positivity only to forbid a
nonnegative support-erasing exponent direction, and because the balanced
eight-vertex table explicitly demonstrates exact active transport while
retaining many nonzero mixed coefficients.
