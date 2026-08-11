# Hostile review of exposed mixed-fibre transport isolation

## Verdict and provenance

**PASS, as an exact negative route-closure theorem with a bounded Laurent
countermechanism.**  The proof correctly separates three facts that could
otherwise be conflated:

1. the `U7D` exposed word rejects that fixed complete label support by a
   one-monomial target equation;
2. the exposed word is not in the active transport multidegree carrying the
   cycle holonomy; and
3. the table's only additional exact zero mixed fibre is compatible with a
   one-parameter family retaining `H=-1`.

The result does not exclude a hypothetical witness, aggregate holonomy,
pure cofactor flow, or the deeper branch.  The `r=1` matrix-unit branch and
the global Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. The exposed equation is complete, not a selected term

Both checkers enumerate all `105` perfect matchings on eight vertices and
agree that the fixed label support induces `101` words.  For

```text
eta=00000100
```

the complete fibre is exactly

```text
{04|17|26|35}.
```

The amplitude product is nonzero on the complete matrix-unit torus.  Hence
the target equation is not a cancellation relation but the monomial
equation

```text
lambda_04 lambda_17 lambda_26 lambda_35=0.
```

After Laurent localization this monomial is a unit.  Before localization it
forces a physical amplitude to vanish.  The theorem therefore correctly
classifies the equation as fixed-support exclusion, not as a polynomial
constraint on `H`.

## 2. The matching categories are not silently merged

The exposed matching has one offdiagonal edge `35` and the pure residual
`04|17|26`.  There is no diagonal matching, no second offdiagonal term, and
no aggregate parameter in the complete fibre.

The deeper-blocker alternative is not another monomial that should have
been added to this coefficient equation.  It is an outcome of applying the
imported square/hexagon bridge theorem to a cofactor-active core satisfying
its parity hypotheses.  The review accepts the theorem's explicit statement
that no deeper term is present in the fibre classification.

## 3. Odd shore parity blocks the imported transport operation

The exposed word has multiplicities `(7,1,0)`.  It has no diagonal perfect
matching, and its one cross edge gives cross counts `(1,0,0)`, which do not
have common parity.

The active cycle lies in multiplicity `(4,4,0)`.  Imported bridge transport
preserves all three multiplicities.  Therefore no sequence of the
established transport operations connects the exposed word to the cycle.

This does not claim that arbitrary equations of different multidegrees
cannot share variables.  It says only that the proved `U7B` operation does
not provide the missing cross-multiplicity bridge.  The theorem preserves
that exact scope.

## 4. The additional mixed equation is a genuine local coupling

The only zero mixed fibre beyond the three active-cycle words is

```text
nu=02001121,
F(nu)={02|16|35|47, 03|16|24|57}.
```

Both terms are offdiagonal.  They share the nonzero edge `16`, and after
saturation the equation is

```text
lambda_02 lambda_35 lambda_47
+lambda_03 lambda_24 lambda_57=0.
```

This shares the cross edges `24,35` with the first cycle equation and the
residual edges `02,57` with the third.  It is not algebraically disjoint from
the cycle data.

Its multiplicities are `(3,3,2)`, however, so its diagonal aggregate is zero
by parity.  Its two offdiagonal terms cancel, making the offdiagonal
aggregate zero as well.  It is an internally zero fibre, not another active
transport vertex.  Thus adjoining it to the already closed three-cycle does
not create an unrecorded successor obligation under the existing theorem.

## 5. The Laurent family is exact and all denominators are surfaced

For invertible `t`, the family changes only

```text
lambda_35=t,       lambda_24=-t^(-1),
lambda_47=t^(-2), lambda_06=t^2,
lambda_12=lambda_14=-1,
```

and leaves all other amplitudes one.  Direct multiplication gives:

```text
three pure coefficients:                 (1,1,1);
three cycle fibres:                       1+(-1)=0;
neighbour fibre:                          t^(-1)-t^(-1)=0;
local cycle ratios:                       (-1,-1,-1);
holonomy:                                 -1;
exposed coefficient:                      t.
```

The excluded divisor `t=0` is stated.  There are no other denominators.  The
fixed positive endpoint-balance certificate depends on labels rather than
these amplitudes, so the imported moment theorem applies over `C` after any
nonzero specialization.  Positive gauge scales each word coefficient by a
nonzero character and cannot repair the exposed nonzero coefficient.

## 6. The elimination conclusion is exact

The three cycle equations give `H+1` in the selected Laurent ideal.  The
family defines a quotient homomorphism to `Q[t,t^(-1)]` with `H` mapping to
`-1`, so the ideal is proper and its intersection with `Q[H]` lies in the
kernel `(H+1)`.  Since it already contains `H+1`, the intersection is
exactly

```text
(H+1).
```

Adding the exposed monomial equation makes the Laurent ideal the unit ideal.
The theorem correctly refuses to describe that inconsistency as a stronger
holonomy polynomial.

## 7. Computational independence

The primary checker uses the committed predecessor's matching/label
conventions and a new sparse Laurent representation over `Q(t)`.  It
classifies full fibres, transport multidegrees, pure normalizations, strict
balance, and the cycle circulation.

The no-import audit independently hard-codes decimal endpoint labels,
Laurent exponents, and balance weights; traverses matchings by least-set-bit
deletion; stores matchings as 28-bit sets; packs words in base three; and
reconstructs the holonomy numerator and denominator separately.  It tests a
different nontrivial rational specialization (`t=3` rather than `t=2`).
It shares no matching traversal or Laurent-ledger implementation with the
primary checker.

The bounded programs audit the exact table and family.  The transport
grading and elimination statements are the written proofs, not inferred
from finite enumeration alone.

## 8. Accepted proof-topology update

```text
U7C active binomial cycle
  -> H=-1                                              PROVED;

U7D exposed word
  -> one nonzero monomial on the fixed support         PROVED;
  -> existing transport path to H                      FALSE;

cycle plus one locally coupled zero mixed fibre
  -> exact Q(t) family with H=-1                       PROVED;
  -> stronger elimination relation in H                FALSE;

same-multidegree mixed coupling or new cross-grading law OPEN;
aggregate holonomy                                      OPEN;
pure cofactor branching/even cycles                     OPEN;
deeper-blocker branch                                   OPEN;
r=1 matrix-unit branch                                  OPEN;
global Krenn--Gu conjecture                             UNRESOLVED.
```

No new frontier node is warranted.  This is a sharpened negative boundary
inside `U7D -> U7`, not a new positive reduction or an exclusion of `U7`.

## Strongest fresh-referee objection

The family satisfies only four selected mixed zero equations, not the full
target system.  It therefore cannot show that odd holonomy occurs in a
hypothetical witness.  It proves the narrower and useful statement that the
specific exposed `U7D` word is transport-isolated and that the table's one
additional locally coupled zero fibre does not strengthen the holonomy
elimination ideal.  Any successful continuation must use further equations
with a proved coupling mechanism; the review accepts no broader claim.
