# Hostile review: `P_6` co-two equality-five full-extension exclusion

## Verdict and exact scope

**PASS, for the stated characteristic-zero `P_6` equality-five branch.**

No support-exhaustiveness, based-frame, orbit-transport, endpoint-coverage,
field, dependency, implementation, or scope blocker survived review.  The
audited conclusion is exactly:

```text
an exact weighted P_6 -> Delta_3 restriction
  => dim B_ab>=6 for every omitted pair {a,b}
  => dim A_S<=12 for every complementary co-two sensor.      (1)
```

This verdict does **not** exclude the simultaneous `dim B_ab>=6` residual,
does not prove unrestricted `P_6 -> Delta_3` nonrestriction, and does not
extend the `P_6` endpoint arguments to `P_r` for `r!=6`.  Arbitrary-order
permanent nonrestriction remains unknown.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## 1. Reviewed surface

The new package was reviewed at the following normalized-LF SHA-256 values:

```text
theorem:
  bd3428b41fd4bca2d57641de279e58e5d9c1b8f81dad287fe1ce731cade3a9de
primary:
  1dcb2fc490dbd1ab393063f43a74232ebe31d0cd77bfbf65aefeebe16831ca16
independent audit:
  016f812e01bdb3d1adb91b11b2eb2f2331d70bd5fedd24bca49cbd361385e0ac
```

Both implementations independently pin thirty-six upstream theorem,
primary, audit, and hostile-review files.  Their ordered dependency-manifest
digests agree exactly:

```text
6f43c88ac31bd8b189dd308f13ce2270c0ec5dfd87da0857813cfe1208769c89. (2)
```

The same PR repairs newline portability in eight load-bearing legacy replay
scripts.  Section 7 reviews those changes separately; they do not change any
theorem, expected digest, mathematical assertion, or proof branch.

## 2. Proof topology

Assume an exact weighted restriction and an omitted pair with
`dim B_ab=5`.  The synthesis uses the following acyclic chain:

1. symmetry of `P_6` moves the arbitrary omitted pair to the first two
   source slots;
2. the equality-five support theorem forces active support four, supplies
   pair-level `Delta_3` admissibility from the actual colour bases, and
   leaves unbased types `(3,1)`, `(4,1)`, `(4,2)`;
3. the based-frame theorem classifies every admissible colour frame inside
   those three unbased types;
4. permanent covariance proves that every classification equivalence and
   exchange of the two omitted modes preserves exact extendibility in both
   directions;
5. six hostile-reviewed pointwise endpoint packages exclude the six
   exchange classes; and
6. the co-two floor `dim B_ab>=5`, integrality, and the excluded equality
   case give `dim B_ab>=6`, while the sum bound gives `dim A_S<=12`.

No endpoint conclusion is fed back into a classification hypothesis.  No
pair-level admissible frame is treated as a full extension.  No numerical or
finite-field observation is used as the characteristic-zero proof.

## 3. Exhaustiveness of the based-frame cover

The exact based classification has raw admissible triple counts and orbit
profiles

```text
type      raw triples   ordered orbit sizes   after exchange

(3,1)         2                 2                  2
(4,1)        14              1,6,6,1             2,12
(4,2)        12               4,4,4              4,4,4.     (3)
```

Thus there are `1+2+3=6` exchange classes.  The endpoint routing is

```text
(3,1), unique                         -> triangle 012;

(4,1), k=2 or k=1                    -> displayed mixed star 013;
(4,1), k=3 or k=0                    -> pure star 014;

(4,2), e=0                           -> displayed fixed 013;
(4,2), e=1                           -> fixed e=1 025;
(4,2), e=2                           -> fixed e=2 024.       (4)
```

For `(4,1)`, omitted-mode exchange sends `k` to `3-k`, so the two pairs in
(4) are exactly the exchange orbits.  For `(4,2)`, exchange fixes `e`; none
of its three rows merge.

The primary derives (3) again from the characteristic-zero pivot charts and
the upstream group generators.  The audit starts from a separate raw triple
catalog and independently constructs the finite groups.  It partitions all
`2+14+12=28` triples without importing the primary or the upstream
classifier.  Both routes obtain the same six classes and orbit sizes.

### The `025` collision

The numerical representative labels are local to an unbased type.  In
particular,

```text
(4,1), k=1, representative 025 -> mixed star 013 by exchange;
(4,2), e=1, representative 025 -> fixed-e=1 endpoint 025.   (5)
```

Conflating the two `025` rows would leave one based orbit unaudited and use
the fixed endpoint on the wrong pair.  The theorem, primary, and independent
audit all key the route by `(unbased type, invariant)`, and both explicitly
assert the distinct outcomes in (5).

## 4. Covariance and relabeling attack

The support theorem begins with an arbitrary unordered omitted pair, while
the endpoint packages use the first two ordered modes.  The transition is
legitimate for two separate reasons:

1. `P_6` is symmetric in all six source slots, so a source-mode permutation
   preserves every constant or mixed colour word in the target; and
2. exchange of the first two displayed slots is explicitly covered by the
   orbit-transport theorem.

The `r=4` coordinate transformations act on the four active coordinates.
Extending them by the identity on the two inactive coordinates gives one
common coordinate monomial map on `K^6`, exactly the operation allowed by
the transport theorem.  No independent coordinate change is applied in
different source modes.

The classification also uses only a common colour permutation and
independent nonzero rescalings of the three displayed vectors.  Under the
transport formula the new target weight is a product of the old nonzero
weight, the two vector scalars, and the nonzero monomial character.  Hence a
live diagonal coefficient cannot be transported to zero.

All operations are invertible.  Pointwise nonextendibility therefore
transports both from and back to each classified frame; the proof does not
use a one-way normalization.

## 5. Endpoint-interface audit

Each row of (4) is owned by a distinct reviewed endpoint:

```text
class                 theorem scope                         verdict

triangle 012          displayed based (3,1), P_6             PASS
mixed star 013        displayed based (4,1), P_6             PASS
pure star 014         based (4,1), k=3, P_6                  PASS
fixed e=0 013         displayed based (4,2), P_6             PASS
fixed e=1 025         based (4,2), e=1, P_6                  PASS
fixed e=2 024         based (4,2), e=2, P_6                  PASS.      (6)
```

Every endpoint assumes the same characteristic-zero field and the complete
five-dimensional pair-product target: two mixed zero tensors and three
nonzero diagonal tensors on the other four modes.  Those are exactly the
conditions supplied by an exact `P_6 -> Delta_3` restriction when
`dim B_ab=5`.  The synthesis does not select a subsystem of the target.

The pointwise endpoint packages do not themselves claim orbit transport.
That missing edge is supplied only once, by the separately reviewed
covariance theorem.  Conversely, the transport package's old residual list
does not claim the three new endpoints; the synthesis explicitly adds them.

## 6. Scope and dimension audit

The endpoint proofs polarize complementary quartics on exactly four
remaining source modes.  They prove `P_6` statements.  Nothing in the
composition turns them into `P_r` statements for another order.  The new
theorem and frontier use `P_6` throughout.

For `P_6`, there are `binomial(6,2)=15` omitted pairs.  Since the chosen pair
in the contradiction was arbitrary, the equality-five exclusion applies to
all fifteen, not merely to one convenient pair.  The exact arithmetic is

```text
dim B_ab>=5 and dim B_ab!=5       => dim B_ab>=6;
dim A_S+dim B_ab<=15+3=18         => dim A_S<=12.           (7)
```

Equation (7) is a necessary sensor boundary.  It does not solve the
simultaneous mixed-target incidence or show that the fifteen sensor
conditions are incompatible.  The proof therefore stops at the
dimension-at-least-six residual.

## 7. Newline-portability repair

Before the repair, a fresh Windows checkout produced eight false dependency
failures:

```text
support synthesis primary/audit;
displayed triangle endpoint primary/audit;
displayed star endpoint primary/audit;
displayed fixed-e=0 endpoint primary/audit.                 (8)
```

The frozen expected hashes were Git-style LF hashes, while those scripts
hashed or compared raw CRLF working-tree bytes.  The complete repair is:

```text
primary scripts:
  path.read_bytes()
    -> path.read_bytes().replace(b"\r\n",b"\n") before SHA-256;

Git-object audits:
  current_worktree_bytes
    -> current_worktree_bytes.replace(b"\r\n",b"\n") before blob equality.
                                                                    (9)
```

The eight-file diff is exactly `31` insertions and `11` deletions.  No
expected digest, frozen path, Git commit, theorem marker, proof topology,
rank computation, or scope fence changed.  The same normalization had
already been reviewed for the based-classification and covariance packages.

After (9), all eighteen upstream primary/audit scripts pass sequentially on
the Windows checkout.  The repair is fail-closed: a content change other
than the checkout newline representation still changes the normalized hash
or differs from the frozen Git blob.

## 8. Primary/audit independence

The new primary imports two exact upstream replay modules because its job is
to compose their characteristic-zero catalog and covariance interfaces.  It
uses SymPy through those modules, resolves every pivot chart, checks all
eight integral representatives, evaluates all `3^6` colour words in the
transport fixture, and exhausts the six-class endpoint map.

The independent audit is run with `python -I`.  It imports neither the
primary, any upstream verifier, nor SymPy.  It uses:

- hard-coded raw admissible-triple catalogs and permutation generators;
- a standalone permutation-group closure and orbit partitioner;
- a standalone `Fraction` Gaussian reducer;
- independently entered integral frames; and
- separate integer arithmetic for the fifteen-pair sensor consequence.

The two routes share only the frozen mathematical data named by the theorem,
not an implementation or imported result.  Agreement of their manifest
digest, orbit sizes, endpoint routes, frame ranks, and sensor bound is
meaningful independent evidence.

## 9. Hostile failure-mode checklist

```text
support theorem used as a converse:                         REJECTED;
pair-level admissibility mistaken for extension:            REJECTED;
unbased orbit used without based-frame classification:      REJECTED;
classification equivalence used without tensor covariance:  REJECTED;
mode exchange applied with the wrong k action:               REJECTED;
e=1 and e=2 merged under exchange:                           REJECTED;
(4,1)-025 conflated with (4,2)-025:                          REJECTED;
pointwise endpoint silently promoted to another orbit:       REJECTED;
nonzero target weight lost under rescaling:                  REJECTED;
P_6 endpoint promoted to arbitrary r:                        REJECTED;
one omitted-pair conclusion promoted without arbitrariness:  REJECTED;
sensor rank bound promoted to P_6 nonrestriction:            REJECTED;
finite-field stress evidence used as proof:                  REJECTED;
global status strengthened:                                  REJECTED.       (10)
```

## 10. Focused replay verdict

```text
new synthesis primary:                                  PASS;
new synthesis independent audit under python -I:        PASS;
all eighteen upstream primary/audit scripts:             PASS;
Python compilation of the new scripts:                   PASS;
Ruff check of the new and repaired scripts:               PASS;
Ruff format check of the new scripts:                     PASS;
mechanical eight-file portability diff audit:             PASS.
```

## 11. Accepted boundary

```text
P_6 equality-five co-two branch:                         EXCLUDED;
all fifteen P_6 pair-product dimensions:                 AT LEAST SIX;
all fifteen complementary sensor dimensions:             AT MOST TWELVE;

dimension-at-least-six simultaneous incidence:           OPEN;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
equality-five exclusion for P_r, r!=6:                   NOT CLAIMED;
arbitrary-order permanent nonrestriction:                UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```
