# Hostile review of U7D complete same-multidegree saturation exclusion

## Verdict and provenance

**PASS, as an exact fixed-template eight-vertex exclusion and an explicit
arbitrary-order boundary.**  The complete `(4,4,0)` word block of the `U7D`
endpoint-label table contains ten singleton compatible fibres.  Any one of
their target-zero equations is a matching monomial, hence a unit after the
complete nonzero `r=1` Laurent localization.  The saturated ideal and its
elimination in `Q[H]` are therefore both `(1)`.

This is not a stronger holonomy polynomial.  It says that the fixed `U7D`
label support cannot satisfy its complete active-multidegree target block at
all.  No theorem forces the same singleton or unit-ideal phenomenon for an
arbitrary active cycle or at arbitrary order.  The `r=1` branch and the
global Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. The requested word block is complete

There are exactly

```text
binomial(8,4)=70
```

words with four zeroes, four ones, and no twos.  The primary verifier groups
all `105` physical perfect matchings by their induced endpoint-label word.
The no-import audit reverses the loops: for each of the `70` words it uses a
target-constrained least-unused-vertex recursion to enumerate every
compatible matching.

They independently agree on the exact fibre histogram

```text
57 empty;
10 singleton;
 3 binomial.
```

The theorem displays all `13` nonempty fibres, so the finite certificate can
be inspected without trusting a hidden search output.  Empty words are still
counted and contribute the tautological equation `0=0`; no supported word is
silently omitted.

## 2. The three binomials are exactly the imported active cycle

The only two-term fibres are

```text
00001111,
00110011,
01010101.
```

Under the predecessor's specialized amplitudes, each contains one diagonal
term of value `1` and one offdiagonal term of value `-1`.  Thus the census
recovers the complete cycle equations and the already-proved value `H=-1`.

No additional multi-term fibre is being treated as binomial, and no
aggregate term is dropped.  The new conclusion arises from the other ten
words, not from strengthening the imported multiplication argument.

## 3. One singleton is already a Laurent-unit certificate

For

```text
omega=00011011
```

the complete fibre is

```text
{01|24|37|56}.
```

The target coefficient is therefore exactly

```text
lambda_01 lambda_24 lambda_37 lambda_56.
```

All four variables are inverted in the complete nonzero physical torus.  The
displayed reciprocal monomial multiplies this generator to one.  Hence the
full ideal is the unit ideal without a Groebner basis or a random
specialization.  The independent audit repeats the argument with the
different singleton word `10110010` and matching `06|17|23|45`.

The conclusion remains exact if pure normalizations, all three cycle
binomials, the definition of `H`, and the established transport identities
are also included: adding generators to an ideal already containing one
cannot restore properness.

## 4. Saturation and elimination are not conflated

Before localization, a singleton equation forces at least one physical
amplitude to vanish.  It therefore exits the complete nonzero `r=1` support
stratum.  After saturation by the product `L` of all physical amplitudes,

```text
(J:L^infinity)=(1).
```

In the Laurent ring this is simply `I=(1)`, so

```text
I intersect Q[H]=(1).
```

This is decisive outcome B, not outcome A.  There is no compatible solution
set on which a new nonconstant `P(H)` could be interpreted.  Calling the
unit ideal a stronger holonomy equation would obscure the actual support
exclusion and is correctly rejected by the theorem.

The only denominator is the explicitly stated product of physical
amplitudes.  No exceptional divisor or characteristic-zero factor is
cancelled in the unit proof.

## 5. Transport, grading, and algebraic coupling remain distinct

The selected bridge transport closes cyclically on the three binomial
words.  Word-shore rematching and the chosen cofactor-active responses also
remain within that data.

Transport preservation of multidegree is one-way.  It does not prove that
all `70` words are transport-reachable merely because they have the same
colour counts.  The complete block is imposed because the GHZ target
requires every mixed coefficient to vanish, not because the existing
transport theorem connects every word.

Several singleton monomials share edge variables with cycle terms.  This is
an algebraic overlap, not a transport theorem.  Once all target equations
are imposed, elimination may use the shared ring and every generator; it
does not turn a singleton word into a new active-cycle vertex.

The review accepts the checkpoint because all four notions are stated
separately:

```text
shared physical variables;
same multidegree;
proved bridge/rematching transport;
ideal-theoretic elimination.
```

## 6. Colour permutations are scoped correctly

In the unpermuted `U7D` table, the balanced `{0,2}` and `{1,2}` word blocks
each have `70` empty fibres.  They do not contain permuted active cycles.

If the **entire** endpoint-label table is globally relabelled by a colour
permutation, compatibility gives a bijection of fibres.  The `57/10/3`
histogram and unit certificate then move to the correspondingly permuted
multidegree.  Both checkers test all six global relabellings.

This avoids assuming a colour symmetry that the original fixed table does
not possess.

## 7. Computational independence and proof role

The primary checker imports the predecessor's tuple-coded table and generic
matching generator.  It performs one matching-first census, compares the
full supported-fibre dictionary with the written certificate, represents
Laurent monomials by edge-exponent counters, and checks the imported cycle
and all global relabellings.

The no-import audit independently encodes endpoint labels as decimal codes.
It performs `70` target-word-first constrained recursions, uses a different
unit word, reconstructs `H` with independent numerator and denominator
ledgers, and rebuilds each colour-permuted table from its raw rows.  It
imports no repository module and shares neither the primary traversal order
nor its fibre grouping implementation.

The bounded exact programs establish the complete fibre census.  The
saturation and elimination claims are the one-line Laurent inverse argument
in the written theorem.

## 8. Accepted proof-topology update

```text
U7D fixed complete label support
  -> three (4,4,0) cycle binomials and H=-1             PROVED;
  -> complete (4,4,0) block has ten singleton fibres    PROVED;
  -> saturated fixed-template ideal is (1)              PROVED;
  -> fixed support reaches hypothetical witness locus   FALSE;

arbitrary active-cycle same-degree unit/syzygy lemma     OPEN;
aggregate active fibres                                  OPEN;
cross-multiplicity coupling                              OPEN;
pure cofactor branching/even cycles                      OPEN;
deeper-blocker branch                                    OPEN;
r=1 matrix-unit branch                                   OPEN;
global Krenn--Gu conjecture                              UNRESOLVED.
```

No new frontier node is warranted.  The result sharpens the fixed `U7D`
boundary and identifies the exact missing arbitrary-order lemma.

## Strongest fresh-referee objection

The `U7D` table was already known not to be a witness, so a new exclusion of
the same table could be dismissed as merely finding another failing word.
The response is scope-specific: the prior obstruction lay in multidegree
`(7,1,0)` and could not touch `H` through established transport.  This
checkpoint answers the explicitly different complete-block question in the
cycle's own `(4,4,0)` grading, proves the exact saturated elimination ideal,
and shows that the local template exits by a Laurent unit rather than a
holonomy syzygy.  Its value is the rigorous local decision and the resulting
arbitrary-order unit-or-syzygy obligation, not a claim that the global branch
has been closed.
