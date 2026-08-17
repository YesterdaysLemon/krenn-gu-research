# Common-contraction, tensor Wick, and all-depth response hostile review — 2026-08-17

## Verdict

**Accepted at the frozen hashes recorded below. No P0 or P1 defect remains.**

The review initially found three publication blockers:

1. the swallowed-pure certificate checkers used unary `+Counter`, which
   discarded negative coefficients and could conceal a false signed identity;
2. the all-depth theorem claimed the complete affine fibre without proving
   the arbitrary quadratic-tensor direction;
3. its first proposed `K_(3,3)` multi-edge control,
   `x_1x_4-x_1x_5-x_2x_4+x_2x_5`, was not in the Wick kernel and caused both
   focused scripts to fail.

All were repaired.  The signed checkers now retain every nonzero signed
coefficient.  The all-depth theorem now proves the arbitrary-`T` equivalence
from the degree-four component of `(exp(T)-1)Q_K`.  The false rectangle was
replaced by `T=x_1x_3-x_1x_2`, for which
`T(x_1+x_2+x_3)=0`; both independent exact implementations pass.  Scope
wording, theorem numbering, README summary, and the `GLD9`--`GLD12` frontier
and typed edges were reread after repair.

These are theorem-sized but scoped results.  They do not prove universal
selector survival, legal seven-port target attachment, witness-locus helper
forcing, coefficient purity, paired `(M,Z)` agreement, or a permanent
restriction.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Frozen artifacts

Base HEAD before the untracked package:

```text
e4564908c592ebf4d85b892ec6f56ba9dc319612
```

```text
GLD9 theorem   654C48E125E068B81D9310BB1FF8C3BAAD0B5B4ACE8BC70CECE6B81FC7329E3B
GLD10 theorem  101ED0F612422EB6025C3DD4B6CA69D81FCAD40BBE2BA77969BC0B89875F90B9
GLD11 theorem  FDF3785D6759FEA47AD453EA0ACF32FBF4354579FF80B1D0EDF2522F768188D2
GLD12 theorem  A45C20FF2ED4B4E1E99AD6A2A6E78248C4763B17FCB4F46A7618CCE7BE79C6D4

GLD9 primary   2A2150908869D97B8B2528FDD0BE975DC8457B279E2255785DDCD8D317F471B3
GLD9 audit     D3515DB384CAB1E82D838AC45DF60EE12F76EA24B0CAF92E9F0577B4076B8C3E
GLD10 primary  A4BF6C0938D3802C3E64AB6D8636E058553692204B0C7E4132B21B253A7D92D6
GLD10 audit    48340470229E6627224DF4E51BCC336FBB2467206BABECA3FC5FD8733713F80
GLD11 primary  B9724879235AA532070864B389BB0615DEF363BD667361C2DD843C10C62E61DB
GLD11 audit    3CB7D619F697601A96E2ED75CB906536D58237709D77A4A375B13FD3623E9ADF
GLD12 primary  75A7B4D466A203987F25289676DFE79DEF957206848D8A9A488283D76DBF9ABD
GLD12 audit    233607CB5ADF3E1F257728403C31615B3FE12BC45B9F5554F8685D9DAB4663C1

README          E761ED65832923B43E7D04C95C733BAC017BCDB19205C2713A29C4FF0C5C5B35
frontier        064A9BB1C2E21731F84E6878DA5F5A89BF5BD2B0538FCA65C4ACC9EBF6394DD6
```

## GLD9: maximal-rank common-contraction synchronization

The finite-open intersection proof is correct over a characteristic-zero
field.  For each target, a nonzero maximal-rank nuisance minor and a nonzero
augmented minor define a principal open on the contraction torus.  The
Laurent coordinate ring is a domain, so the finite product of these minors
is nonzero; an infinite field supplies a rational torus point outside its
zero set.

The witness tier correctly retains a nonzero response coordinate.  At the
common point, selector survival and response nonvanishing combine with the
`GLD7` rank-at-most-one theorem to give quotient rank exactly one.  The
response-zero exception remains explicit.

The selectors need not be graph-independent.  They are fixed after the
graph, `Q`, and common contraction are fixed, are constant in the open-port
variables, and are exact against every nuisance column.  They are not
selected merely because an observed output happened to be diagonal, so the
construction is noncircular.

The disjoint controls `B_1=[t-1]`, `B_2=[t-2]`, `g_1=g_2=[1]` correctly show
that arbitrary rank-drop survival points need not synchronize.  The theorem
therefore removes only the common-contraction problem; it does not force any
individual maximal-rank survival point.

## GLD10: seven-port five-helper tensor Wick cover

The three endpoint branches are exhaustive and correct:

- two nonzero endpoint vectors give the seven-port support-union injective
  block and a selector on at most twenty-one rows;
- exactly one zero endpoint isolates an outside-degree-one block and uses at
  most six rows;
- two zero endpoints isolate `K_pq B_uv` in one row, with characteristic zero
  and five bi-supported helpers guaranteeing a nonzero helper pair.

Repeating this coefficientwise recovers all `21*9=189` direct-pair tensor
coefficients from the same thirty-five four-port tensors.

The observable diagonal-pair entry criterion is now complete.  Two rank-two
diagonal frames align through their common nonzero diagonal lines.  A
rank-one third port first aligns one line, while the rank-two pair aligns the
other; later rank-one ports cannot carry several collinear colour columns
because their diagonal pair matrix would then violate rank-one diagonality.
No zero port survives the no-isolated-port assumption.

The theorem remains downstream of legal attachment of all thirty-five
same-`Q` `z_4` tensors.  It does not extend the six-port thirty-one-row
attachment theorem to seven ports, force helper nonisotropy on witnesses,
attach deeper rows, or give a coefficient-pure detector or permanent
restriction.

## GLD11: simultaneous swallowed-pure physical control

The graph construction is exact in characteristic zero.  The incidence proof
establishes that the four roots form a maximum-cardinality torus zero set: an
outside vertex excludes its three incident roots, and the complete outside
graph prevents two outside vertices from sharing a larger zero set.  Every
outside mode is a rank-three blocker.

Pure normalization, the zero Hamming-one shell, and local concision follow
from the displayed coefficient structure and identity flattening minors.  The
six pair responses equal three and the four-port response equals fifteen,
hence all seven are nonzero in characteristic zero.

All twenty-one active pure classes are explicitly represented in the
complete nuisance spaces.  The repaired primary and audit checkers preserve
negative coefficients when verifying these identities.  Independent exact
recomputation finds every signed residual equal to the claimed single pure
word.  The nuisance-rank computation separately confirms membership for all
three colours and all seven targets.

The displayed mixed ten-mode coefficient equals one, so the construction is
not a GHZ witness.  It is a graph-side sharpness control showing that
maximum-root incidence, blocker saturation, local concision, pure
normalization, the Hamming-one shell, and response nonvanishing do not exclude
simultaneous swallowed-pure quotient rank zero.  It is not a witness-locus
fibre or counterexample.

## GLD12: complete tensor h-zero Z fibre

For arbitrary `B,T in A(W)_2` at fixed `K`,

```text
Z_(B+T)-Z_B = exp(B)(exp(T)-1)Q_K.
```

If `TQ_K=0`, every higher `T^jQ_K` vanishes.  Conversely, after multiplication
by the unit `exp(-B)`, the degree-four component is exactly `TQ_K`, while all
later terms have degree at least six.  Therefore

```text
Z_(B+T)=Z_B  iff  TQ_K=0,
```

and the complete residual-present fibre is exactly

```text
B + ker(mu_K:A(W)_2 -> A(W)_4).
```

Thus equality of the complete tensor `z_4` layer is information-complete for
every deeper residual-present `Z` layer on the same named finite port union.
Restriction gives equality on every principal subwindow of that union.  This
is equality of complete tensors, not merely diagonality, purity, or selected
target shapes.

For a nonzero tensor supported on one edge, tensor-product noncancellation
and distinct labelled supports prove the two-vertex-cover if-and-only-if.  The
corrected genuine multi-edge control is

```text
Q_K=(x_1+x_2+x_3)(x_4+x_5+x_6),
T=x_1x_3-x_1x_2,
```

so `TQ_K=0`, although neither support edge is itself a two-vertex cover.  Both
exact implementations replay this cancellation and the complete all-depth
equality.

The `K_(5,2)` and star examples are genuine physical rank-two residual
channels with no isolated port and every diagonal pair block of rank at most
one.  Their direct arrays vary while `K` stays fixed.  The residual-absent
tower changes because the degree-two part of `exp(B+T)-exp(B)` is `T`; these
are consequently not paired `(M,Z)` fibres or same-graph ambiguities.

The general affine classification is a response-algebra theorem.  It does
not assert that every tensor-kernel direction satisfies maximum-root
incidence, local concision, or the mixed GHZ equations.  A scalar-word `GLD8`
kernel can also disappear after full tensor polarization.

## Independent checks

All eight focused commands pass independently:

```text
maximal-nuisance-rank synchronization primary replay: PASS
maximal-nuisance-rank synchronization independent audit: PASS
seven-port five-helper tensor Wick primary replay: PASS
seven-port five-helper tensor Wick independent audit: PASS
four-root simultaneous swallowed-pure primary replay: PASS
four-root simultaneous swallowed-pure independent audit: PASS
full-tensor h-zero Z fibre primary replay: PASS
full-tensor h-zero Z fibre independent audit: PASS
```

`python -m ruff check` passes for all eight scripts, and
`python -m ruff format --check` reports all eight already formatted.  The
Markdown whitespace/conflict scan and tracked README/frontier
`git diff --check` pass.

The primary/audit pairs use distinct polynomial or matching representations
where appropriate.  They remain finite exact replays and controls; the
written torus, tensor-support, graph-incidence, and arbitrary-`T` arguments
are load-bearing.

## Frontier and exact remainder

The `GLD9`--`GLD12` frontier entries and typed edges accurately record the
advances:

- `GLD9` synchronizes individually available maximal-rank selectors but
  supplies none by itself;
- `GLD10` supplies a full tensor-word cover only after seven-port row
  attachment and helper hypotheses;
- `GLD11` proves graph-side sharpness but is excluded from the witness locus
  by a mixed coefficient;
- `GLD12` closes deeper residual-present `Z` recovery beyond complete tensor
  `z_4`, while leaving target-shape, attachment, and paired-response routes
  open.

Still **UNKNOWN**: individual maximal-rank quotient survival and response
nonvanishing for every witness target; exclusion of the simultaneous
swallowed-pure locus using the full mixed equations; legal same-`Q`
attachment of all thirty-five seven-port four-row tensors; witness forcing of
the five-helper branch or another exhaustive tensor cover; coefficient-pure
mixed detection; three-colour activity; physical witness integration of
tensor-kernel fibres; paired `(M,Z)` identification; and any
weighted-diagonal permanent implication.

The global Krenn--Gu conjecture remains **UNRESOLVED**.
