# Hostile review: least-core complementary-shore response and portal dichotomy

## Verdict

**SCIENTIFIC PASS at the corrected exact scope.  No P0, P1, or P3 finding
remains.**

The hostile-reviewed theorem core is frozen at commit
`47bca7d3bd3f714338a4f0c40170c9fb54db7163`.  Subsequent rebases preserve the
three Git blobs below exactly.  The canonical hashes are computed from those
tracked LF-normalized blobs, not from platform-dependent working-tree line
endings.

| Artifact | SHA-256 | Git blob |
|---|---|---|
| theorem | `e776f0ad967ddb8338891fd88f514aa32e4d64a66967596a048ae409d5e55a63` | `b9ae148b3c00761ba8c413cb73ab7bf6e84ad320` |
| primary verifier | `15546a915ebd8cf33b65595a815f399992d9b65a0c4837c2e4863616811f3c31` | `9c346c8b0fa4350f558fc0764644096567b56e0b` |
| independent audit | `158ead2aff75de2cbc678417a21bacdcea6203813647ee750f375ff62d473309` | `5e92d669cbe1c47f3d43dbd67b229f47e6865ede` |

The corrected theorem proves an edgewise opposite-colour zero response from
the globally least all-bridge pure core, the exact support/size/attachment
dichotomy for those response shores, disjoint opposite-colour active
neighbour sets across every core edge, a conditional exterior portal and a
co-two independent-set residual, and a same-colour conformal-completion or
minimum-crossing portal dichotomy.  It does **not** force opposite-colour
active neighbours to leave the least shore, exclude a co-two exterior, force
a response shore to be supported, produce a target-lattice unit, or exclude a
witness.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Claim reconstruction

The load-bearing chain is:

1. In the simultaneous balanced all-bridge specialization, choose a globally
   least supported pure zero `(e,S)` and put `C=V-S`.  The imported least-core
   theorem makes its first-cofactor graph `A` connected, bipartite, and
   matching-covered.  Every allowed edge `f in A` has
   `h_e(S-f)!=0`.
2. Applying the mixed complementary-product identity to `S-f` gives

   ```text
   h_e(S-f) h_d(C union f)=0
   ```

   for each `d!=e`.  Hence every edgewise response shore `C union f` has zero
   colour-`d` hafnian.
3. If that response shore is support-matchable, global leastness gives
   `|S|<=|C|+2`, equivalently `2|S|<=n+2`.  If `2|S|>n+2`, every response
   shore is therefore support-unmatchable.  This is a dichotomy about
   support; the algebraic zero alone does not supply a perfect matching.
4. In the supported case, take a least conformally admissible pure zero
   inside the response shore.  Fixed nonzero matchings on its response-shore
   complement and on `S-f` complete every residual term into one mixed target
   fibre.  Multiplicativity preserves the cancellation and every matching-
   exponent difference.
5. For a core edge `xy` and another colour `d`, let `k` be the third colour.
   Both a colour-`e` core edge and a colour-`d` active edge flip `b_k`.  A
   common colour-`d` active neighbour of `x` and `y` would therefore force
   `b_k(x)=b_k(y)`, contradicting the core edge.  The two full neighbour sets
   are disjoint, and active-score positivity makes both nonempty.
6. If both endpoints have exterior active neighbours and the rest of `C` is
   colour-`d` matchable, those edges support the response shore and Step 3
   applies.  When `|C|=2` and `|S|>=6`, two adjacent vertices with exterior
   active neighbours would support a four-vertex response zero, contradicting
   global leastness.  Thus the exterior-neighbour vertices form an independent
   set in `A`; the co-two exterior itself remains open.
7. In colour `e`, a perfect matching on `C` termwise completes the original
   least relation.  Otherwise choose a full colour-`e` matching with the
   fewest cut crossings.  Symmetric difference with any core perfect matching
   yields alternating portal paths.  If the image in `C` of any nonempty
   union of path endpoint pairs were matchable, switching all selected paths
   and that complementary matching would strictly reduce the crossing count.
   Hence every such image is support-unmatchable.
8. A full matching in another colour completes the original relation when it
   has no crossing edge.  With exactly two crossings whose endpoints in `S`
   form an allowed core edge, it supports the associated response shore.
   Four-or-more portals and nonallowed two-portal pairs are explicitly left
   open.

## The rejected own-bit shortcut

An earlier candidate used a stronger transition rule than the imported
all-bridge authority.  A saturated colour-`c` edge must flip the two bits
other than `b_c`; its own bit `b_c` is free.  Thus, for `e=0,d=1,k=2`,

```text
000 -> 111
```

is an allowed colour-`d` transition: it flips the required `b_0,b_2`, also
flips its own bit `b_1`, and preserves `b_1 xor b_2`.  Consequently no
argument based on `q=b_d xor b_k` forces colour-`d` active neighbours outside
`S`.

The unpublished candidate heads `24b8a171f1ad605b21a137c4d92c44c49815438e`
and `2dd6ff021db2e37c8d023c162e55810548bd7882` used that invalid shortcut.
They are **withdrawn and not publishable evidence**.  The corrected theorem
retains only the valid shared-neighbour separation, conditional exterior
portal, and co-two independent-set conclusion.

## Adversarial checks

| Attack | Result |
|---|---|
| A nonzero allowed-edge coefficient might not expose a nonzero deletion cofactor | **Rejected.** Its two factors are nonzero by the definition of the least-core edge set. |
| The mixed-cut product might apply to an empty or full shore | **Rejected.** `|S|>=4`, so `S-f` is nonempty, proper, and even. |
| A response hafnian zero might silently imply support | **Rejected explicitly.** Supported and unsupported response shores are separate alternatives. |
| The size bound might use local rather than global minimality | **Rejected.** The theorem assumes the globally least supported zero over all colours and eligible shores. |
| The conformal attachment might change matching-exponent differences | **Rejected.** Every residual term is unioned with the same two fixed matchings on disjoint shores. |
| A colour-`d` edge might preserve its own bit | **Rejected as an assumption.** Both own-bit choices are retained; `000 -> 111` is replayed explicitly. |
| Active degree might force exterior neighbours | **Rejected explicitly.** Positive degree is global and opposite-colour active edges may remain inside `S`. |
| Disjoint neighbour sets might depend on own-bit preservation | **Rejected.** It uses only the forced flip of the third bit `b_k`. |
| The co-two independent set might already exclude the co-two exterior | **Rejected explicitly.** It only says every core edge has an endpoint outside the exterior-neighbour set, separately for each other colour. |
| The minimum-crossing switch might work only for one portal path | **Rejected.** The proof switches an arbitrary nonempty subfamily simultaneously and matches the full corresponding image in `C`. |
| A two-portal matching might always align with an allowed core edge | **Rejected explicitly.** Nonaligned pairs remain an open boundary. |
| A cancelling subrelation in one complete fibre might be a unit | **Rejected explicitly.** Other terms in that fibre can compensate it; no target-lattice generation claim is made. |

## Computational evidence and independence

The primary replay

```powershell
python -B claims/arbitrary-order/verify_matrix_unit_least_core_complementary_shore_response_and_portal_dichotomy.py
```

uses closed exact `2 x 2` and `3 x 3` permanent formulas for two hand-built
rational controls.  One has a matchable complement and a cancelling completed
subrelation; the other has an unmatchable complement and a genuine minimum
two-crossing portal.  It also checks the complete eight-type normal-bit table
while retaining both choices of the active colour's own bit.

The independent replay

```powershell
python -I claims/arbitrary-order/audit_matrix_unit_least_core_complementary_shore_response_and_portal_dichotomy.py
```

imports neither repository code nor the primary verifier.  It converts the
controls to hollow symmetric matrices, uses a separate cached exact hafnian
recursion, represents matching switches as edge sets, and implements the bit
transitions with integer masks.  Both routes replay `000 -> 111` and the valid
shared-neighbour separation.

These scripts are exact finite checks of displayed mechanisms and sharpness
boundaries.  They perform no graph-family enumeration and no witness search;
the arbitrary-order quantifiers are carried by the written proof.  Primary,
isolated audit, byte compilation, Ruff `0.16.2`, hygiene, and diff checks all
PASS on the corrected blobs.

## Scope firewall

```text
characteristic-zero simultaneous balanced all-bridge branch: ASSUMED;
globally least supported pure cancellation:                  ASSUMED;
connected bipartite matching-covered least core:             IMPORTED;
allowed-edge opposite-colour response zeros:                 PROVED;
supported-response size bound and mixed attachment:          PROVED;
large-shore response family support-unmatchable:             PROVED;
active neighbour sets across a core edge disjoint:           PROVED;
conditional exterior active-pair response:                   PROVED;
co-two exterior-neighbour set independent for |S|>=6:        PROVED;
opposite-colour active neighbours necessarily exterior:      FALSE / NOT CLAIMED;
co-two exterior excluded:                                    NOT PROVED;
same-colour completion / minimum-crossing portal dichotomy:   PROVED;
every induced nonempty portal-pair image unmatchable:         PROVED;
zero-/aligned-two-portal other-colour trigger:                PROVED;
some response shore support-matchable:                       UNKNOWN;
all other-colour matchings have at most two portals:          UNKNOWN;
all two-portal endpoint pairs are allowed:                    UNKNOWN;
target-lattice unit or aggregate-port exclusion:              UNKNOWN;
localized cut equals the globally least core:                UNKNOWN;
deeper-blocker exclusion:                                    UNKNOWN;
global Krenn--Gu conjecture:                                  UNRESOLVED.
```

The publication review's sole P2 finding was integration: because this result
changes the live decision surface, its publishing change must update the
arbitrary-order README, `docs/current-frontier.md`, and the theorem ledger.
Those navigation edits close the integration finding but do not strengthen
any mathematical claim above.
