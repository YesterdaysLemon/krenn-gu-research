# Pair/four-port diagonal interference review

Date: 2026-08-16
Global status: **UNRESOLVED**

## 1. Question and falsification target

PR #179 left a precise target-coupled question: can the complete two-residual
pair layer together with the entire four-port mixed target force the corrected
channel to be diagonal, or expose an actual mixed GHZ coefficient?

The hostile test retained one physical same-graph residual pair, all six pair
blocks on four ternary ports, and the complete four-port response.  It did not
assume the residual-absent deck, a permanent restriction, target-pure sensor
inversion, or common rows reconstructed from unrelated pair factorizations.

External Qwen and Claude OMP reports suggested this bounded test and a
cross-cut interference lane.  They were used only as conjecture and steering
sources.  Their pair-depth-only examples were not witnesses because they
failed the four-port target equations, and they are not counted as evidence.

## 2. Exact accepted theorem

For pair responses `D_uv=hB_uv+K_uv`, with

```text
K_uv=a_u b_v+b_u a_v,
C(X)=X_12 X_34+X_13 X_24+X_14 X_23,
```

the full physical matching partition gives

```text
hT=C(D)-C(K).
```

The corrected compound is

```text
C(K)=2 sum_(|A|=2) a_A b_(A^c),
```

so every one-port flattening has rank at most two.

If the six pair tensors and the four-port tensor are exactly attached by
nuisance-free constant synchronized target selectors, three complementary
active colours at one port define a `3 x 3` mixed-coefficient grid `G`.  The
corresponding submatrix of `C(D)` is `diag(g_0,g_1,g_2)` with every `g_c`
nonzero, while the corrected submatrix has rank at most two.  Therefore

```text
det(diag(g_0,g_1,g_2)-hG)=0.
```

At `h=0` the active stratum is impossible.  At `h!=0`, at least one of the
nine displayed entries of `G` is an actual nonzero mixed GHZ coefficient.

The target attachment is an input.  A selector must output exactly the same
physical `D_uv` and `T` tensors, after only known nonzero constant
normalization or an independently proved constant target-diagonal nuisance
subtraction.  Function-field inverses, contracted scalar reconstructions,
and independently factorized pair blocks do not qualify.

## 3. Exact sharpness and route refutation

The unrestricted implication is false over `Q`.  One physical response has
rank-two residual frames at all four ports, diagonal pair responses, and

```text
T=3 e0^4+(4/3)e1^4+e2^4,
```

while `K_12` and `K_34` have nonzero mixed entries.  All `78` mixed
four-port coefficients vanish.  Replacing `K` by `-K` and `B` by `D+K`
preserves the complete pair and four-port response data but changes the
corrected channel; residual `O(J)` gauge cannot do this because it preserves
every `K_uv`.

The control has exactly two active colours at each port.  It proves that the
three-active hypothesis cannot be omitted from this two-depth route, not that
every possible detector needs that hypothesis.  It is one legal response
slice, not a Krenn--Gu graph witness.

At `h=0`, pair data give `D=K`, so mixed corrected blocks are directly
excluded by pair target diagonality.  Two explicit direct decks nevertheless
have identical `D` and `T=0`, proving that the residual-absent deck is still
not supplied.

## 4. Proof topology

```text
breadth:          one complete K4 port window, all six pairs;
depth:            residual-present pair and four-port layers;
hidden data used: one common physical residual pair and two incidence rows;
transition group: none in this one-chart theorem;
agreement output: a nine-word detector only on the three-active stratum;
gluing output:    none;
permanent output: none.
```

The theorem advances bounded obstruction: once the window is legally
attached, the port, three activity witnesses, three nonzero products, and nine
mixed target entries form a uniform finite certificate.  It is not a uniform
witness-locus theorem because universal attachment and the zero/one/two-active
branches remain open.

For simultaneous co-two compatibility, `C(K)` is one all-six-pair invariant
on `K_4`; it does not identify degree-one factors or replace the existing
mixed-radical target obligations.

## 5. Hostile review and repairs

Three independent read-only lanes attacked the statement and proof topology.
The following material repairs were made before acceptance:

1. target attachment was promoted from prose to an exact input requiring the
   same physical tensors and constant nuisance-free selectors;
2. hidden residual rows were described as assumed by physicality, not
   reconstructed;
3. the camouflage conclusion was narrowed from global necessity to sharpness
   for this route;
4. the `h=0` conclusion was separated from the nonzero-`h` mixed detector;
5. verifier coverage was narrowed to the representative-port grid replay and
   the positive-sign six-vertex matching expansion; and
6. the primary's sign check was described as coefficientwise invariance, not
   a second physical-graph replay.

After these repairs, the mathematical hostile reviewer found no remaining
tensor-ordering, field, `h=0`, physical-realization, `O(J)`, or activity
counterexample defect.  A separate proof-topology reviewer accepted the
conditional edge and required that no proved `GLS2 -> GLD3` supply edge be
drawn.  Subagent agreement was not treated as proof; the written derivations
and exact replays carry the evidence.

## 6. Independent computational evidence

The primary uses SymPy polynomial expansion, exhausts `216` activity grids at
one representative port, and checks every positive-sign pair coefficient and
all `81` positive-sign four-port words, including the direct six-vertex
matching expansion.

The independent audit imports neither SymPy nor the primary.  It uses
standard-library `Fraction` arithmetic, a bitmask perfect-matching generator,
sparse word dictionaries, and separate Gaussian elimination.  It checks:

- all `15` six-vertex perfect matchings and the three pair matchings;
- the interference identity on all `81` words;
- the six assignment words with multiplicity two and rank two in every
  one-port flattening of an independent nondegenerate control;
- all `216` representative-port grids and `1,944` selected mixed entries;
- both signs of the asymmetric camouflage control; and
- the two distinct `h=0` direct decks.

The finite programs replay the displayed identities and controls.  They do
not prove the arbitrary-field theorem, supply target selectors, or establish
an exhaustive witness-locus branch cover.

## 7. Residual branch and next lane

The narrowest positive Universal Supply obligation is now:

1. legally attach one same-`Q` four-port package whose six `D_uv` tensors and
   `T` are exact outputs of constant target selectors;
2. force three nonzero complementary activity products at one port; or
3. close the exact zero/one/two-active residue with one additional window or
   depth.

The separate cross-cut lane has a noncircular uncontracted formulation.  Two
cut equations define a common-pair compatibility class in a cokernel and a
pair-ambiguity projection of the joint kernel.  A left syzygy can be target
coupled through the fixed empty-deck normalization.  Exact controls show both
that two cuts can improve pair identifiability and that the committed physical
rank-drop fibre can remain invisible to two cuts.  This is the next serious
breadth lane, not part of the present theorem.

## 8. Frozen hashes and final replay

The repaired theorem and its two replay surfaces were frozen at these SHA-256
hashes:

```text
DCF896C9391ABEE3A49B7DC0B2F85130A40494BFC53394AED4F372363B031854  TWO_RESIDUAL_PAIR_FOUR_PORT_DIAGONAL_INTERFERENCE_AND_CAMOUFLAGE_BOUNDARY_THEOREM.md
6BAAA807B951492D01187124BD1B33F11004A938B29D0408ED104FBEBF394572  verify_two_residual_pair_four_port_diagonal_interference_and_camouflage_boundary.py
1C446FE5ABBD76311D1A08CB0781E94D69193711B722946DD220BF6F6F6E3D54  audit_two_residual_pair_four_port_diagonal_interference_and_camouflage_boundary.py
```

At those hashes, the primary and independent audit passed.  The three owning
upstream primary/audit pairs for residual-relative dual Wick, top two-port
observability, and same-graph target-selector coupling also passed.  Ruff
check and format check passed, as did `py_compile`.

On the staged repository candidate, `check_hygiene.py` passed, the migration
suite passed `191/191`, the cycle-cover lattice suite passed `14/14`, and the
link rewriter reported zero changes.  The cached diff passed
`git diff --check` and there was no unstaged change.  Final mathematical,
proof-topology, and evidence-independence hostile reviews all returned
`ACCEPT` on the repaired scope.

This evidence certifies the scoped conditional detector and counterboundary
only.  It does not supply the target-attached window from every witness,
close the zero/one/two-active strata, extract a permanent restriction, or
resolve the Krenn--Gu conjecture.
