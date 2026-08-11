# Hostile review of complete pure-target moment-compatible odd holonomy

## Verdict and provenance

**PASS, as an exact sharpness theorem and proof-route boundary.**  The
displayed eight-vertex table has all `28` nonzero one-matrix-unit physical
pairs, all three pure target coefficients exactly one, a strict positive
endpoint-balance certificate, three complete binomial active-cycle fibres,
and odd invariant holonomy `H=-1`.  The imported coercive-convexity theorem
therefore supplies an actual squared-amplitude moment-balanced
representative preserving those identities.

The table also has an explicitly exposed nonzero mixed coefficient.  It is
not a Krenn--Gu witness or counterexample.  The accepted conclusion is only
that completion, pure normalization, moment balance, proper nonrigidity, and
odd binomial holonomy are mutually compatible before the remaining mixed
target equations are imposed.  The `r=1` branch and the global conjecture
remain **UNKNOWN/UNRESOLVED**.

## 1. Complete physical support is checked literally

The row table contains every unordered pair of eight vertices exactly once.
Every row carries one endpoint-label pair and a nonzero scalar `1` or `-1`.
Thus this is complete physical `r=1` support in the precise matrix-unit
sense.

That fact does not mean the tensor support is the GHZ target support.  The
coefficient of a word is still an aggregate over compatible physical
matchings, and the exposed word in Section 5 below is nonzero.  The theorem
keeps these two uses of "support" separate.

## 2. Pure normalization and cycle binomiality use complete fibres

The primary checker enumerates all `105` perfect matchings of `K_8`.  The
independent audit reaches the same matchings by least-set-bit deletion and
packs endpoint words in base three.  They agree that the table induces `101`
word fibres.

For each constant word, the complete compatible fibre consists of the one
matching displayed in the theorem, and its physical product is one.  No
unlisted pure term is silently discarded.

For each of the three selected mixed words, the complete fibre has exactly
two terms: one diagonal term of weight `1` and one offdiagonal term of weight
`-1`.  Hence each coefficient vanishes for the asserted binomial reason.
This is stronger than displaying two cancelling terms without excluding
additional compatible matchings.

## 3. The odd holonomy is a genuine invariant, not a sign convention

The six bridge edges and six cross edges are distinct.  Their signed
incidence vector has zero sum at every vertex-label coordinate, while its
edge support is nonempty.  It therefore defines a nonzero Laurent character
invariant under arbitrary nonzero local diagonal scaling.

All bridge products are `1`; the product of the three cross-core products is
`-1`.  Consequently

```text
H=product_i lambda(B_i)/lambda(E_i)=-1=(-1)^3.
```

Both checkers reconstruct the endpoint-character cancellation directly.
The conclusion is not that every odd cycle has holonomy `-1`; it is that an
exact odd binomial cycle can consistently have the value required by its
three mixed equations.

## 4. Auxiliary balance is not confused with physical magnitude

The displayed integers `p_e` are all strictly positive and give load seven
at every vertex in every colour.  They certify the strict endpoint-balance
hypothesis for the fixed label support.

The original physical amplitudes all have modulus one, and their endpoint
counts are not vertex-independent.  The theorem explicitly does **not** set
`|lambda_e|^2=p_e` and does not claim that the final moment loads equal
seven.  This avoids the principal semantic hazard in importing the
endpoint-balance theorem.

## 5. The moment-balanced representative is exact but existential

The preceding moment theorem applies to any nonzero amplitude vector on a
strictly balanced label support.  Its proof uses the positive `p_e` only to
make the squared-norm exponential functional coercive on the zero-colour-sum
GHZ torus.  Strict convexity then gives an exact minimizing edge-exponent
orbit.  It does not require the input table already to realize the complete
GHZ tensor.

Under the resulting positive gauge, every term in one word fibre receives
the same character.  Therefore:

- the three binomial zero coefficients remain zero;
- each constant-word coefficient remains exactly one because the gauge has
  colourwise product one;
- the Laurent holonomy remains exactly `-1`; and
- a nonzero exposed coefficient remains nonzero.

The checker replays this covariance under a nontrivial rational gauge.  The
existence of the actual moment minimizer comes from the written
coercive-convexity proof, not from a numerical optimizer.  No algebraic
formula for that minimizer is claimed.

## 6. The exposed word prevents witness promotion

The mixed word

```text
00000100
```

has the unique compatible matching `04|17|26|35`, which is offdiagonal and
has product one.  Its coefficient is therefore exactly one before gauge and
a positive nonzero character after gauge.

This single coefficient is sufficient to reject every witness or
counterexample interpretation of the table.  The other mixed coefficients
need not be classified for that purpose, and no finite census is promoted
to an arbitrary-order exclusion.

## 7. Proper nonrigidity does not close the gap

Direct evaluation gives

```text
S_0=S_1={1,2,3,4,5,6},
S_2={0,7}.
```

All three sets are nonempty and proper.  Positive diagonal scaling preserves
the endpoint labels, so the moment-balanced representative has the same
sets.  This sharpens the boundary beyond an example with a globally rigid
unused colour, but it still says nothing about propagation under **all**
mixed target equations.

## 8. Computational independence

The primary verifier represents endpoint labels as tuples, generates
recursive perfect matchings, builds exact rational coefficient ledgers,
performs rational incidence elimination, and applies a power-of-two gauge.

The no-import audit separately encodes each row by a decimal label code,
uses a bitmask traversal and packed ternary words, reconstructs matchings as
28-bit sets, collects endpoint loads directly, assembles the Laurent
numerator and denominator independently, and uses a power-of-three gauge.
It imports no repository module and shares no fibre implementation with the
primary verifier.

Both programs audit the bounded exact table.  The complex moment existence
statement is the imported written analytic theorem, not an empirical output
of either program.

## 9. Accepted proof-topology update

The new node is `U7D`:

```text
U1C actual moment normal form
             +
U7C binomial Laurent holonomy
             |
             v
U7D complete/pure/moment-compatible odd-cycle sharpness
             |
             v
U7 remaining mixed-equation phase exclusion             OPEN
```

The earlier sparse example proved only that odd binomial holonomy was not a
formal sign contradiction.  `U7D` additionally rules out deriving the
contradiction from complete physical support, all three pure target
coordinates, strict endpoint balance, the actual moment gauge, or proper
nonrigidity alone.

The remaining phase obligation is narrower but still substantive: use
additional mixed coefficient equations to exclude aggregate or binomial
holonomy on the **full witness locus**, or close one of the other exact exits.

## Strongest fresh-referee objection

The example does not satisfy the full target equations, so it cannot show
that an odd binomial cycle occurs in a hypothetical witness.  It only shows
that several powerful necessary conditions fail to exclude the cycle before
the remaining mixed equations are used.  The theorem passes because it
states exactly that sharpness boundary, exhibits the missing mixed equation,
and leaves witness-locus exclusion and the global conjecture open.
