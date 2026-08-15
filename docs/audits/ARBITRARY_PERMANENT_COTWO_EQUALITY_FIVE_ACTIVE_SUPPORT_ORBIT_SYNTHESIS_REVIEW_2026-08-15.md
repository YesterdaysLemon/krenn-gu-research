# Hostile review of the co-two equality-five active-support orbit synthesis

## Verdict and scope

**PASS, within the stated characteristic-zero, omitted-pair, and necessary-
condition scope.**  No mathematical, dependency, support-exhaustiveness,
orbit-label, converse, or implementation blocker survived hostile review.

For every omitted pair `{a,b}` in a characteristic-zero weighted diagonal
restriction `P_r -> Delta_3`, the package proves

```text
dim B_ab=5
  => |supp(U_a+U_b)|=4
  => the underlying unbased pair has type (3,1), (4,1), or (4,2).
```

Consequently, an omitted pair whose active support has size at least five
satisfies

```text
dim B_ab>=6,
dim A_S<=binomial(r,2)-3.
```

The three labels classify the underlying pair after monomial coordinate
changes and internal basis changes.  They do not classify based colour
frames under the `Delta_3` stabilizer, construct the other `r-2` modes, or
prove that any displayed pair extends to a full restriction.  Unrestricted
`P_6 -> Delta_3`, arbitrary-order permanent nonrestriction, and the global
Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_COTWO_EQUALITY_FIVE_ACTIVE_SUPPORT_ORBIT_SYNTHESIS_THEOREM.md
  verify_arbitrary_permanent_cotwo_equality_five_active_support_orbit_synthesis.py
  audit_arbitrary_permanent_cotwo_equality_five_active_support_orbit_synthesis.py
```

No theorem, primary-verifier, or no-import-audit edit was required.

## 1. Frozen dependency audit

The package composes four independently owned theorems.  Each declared
commit is an ancestor of the reviewed branch, is the last commit touching
the named theorem, and reproduces the pinned bytes:

```text
4a3a0988f4fc837844bbcd3a57fa408a7850c521
  co-two product-sensor corank-two strengthening
  theorem SHA-256
  486CC700D12F99FC72997DB918D816EFCF5368AE6B45ADF722A4AA38ABF0D0B8

82928ccdc1faaa2519671e9d13680519f068038c
  r=4 pair-dimension-five orbit classification
  theorem SHA-256
  4B7FCCCCF68B55E1DDEACB7328B7469A8A82F36AA2AB0303E9094519A95FC5BC

e9e9d47643c4d8dbcb6bf194de66f84fc37b746c
  active-support-five equality exclusion
  theorem SHA-256
  DE7FA0633E0D79796A5F76528F7B79BC99655F3F0F549133DF4651B71F6E83D2

e486e693f20672ffdf6e6a82f1214f30fb243b9b
  active-support-at-least-six equality exclusion
  theorem SHA-256
  D55AA47CDA33CC749522164AC477935798B9E6BEE1DEF41EDAADA80BE9E645F7
```

Both synthesis scripts also pin the primary-verifier and independent-audit
hashes for every dependency, for twelve pinned files in total.  Direct
SHA-256 recomputation reproduced all twelve values.  All eight dependency
replays passed.  The synthesis therefore does not silently consume a newer
or differently scoped dependency.

The imported statements have the exact scopes needed here:

1. a full restriction supplies independent local triples, pair dimension at
   least five, restricted complement-pairing rank three, mixed products in
   the left radical, diagonal products independent modulo it, and
   `dim A_S+dim B_ab<=binomial(r,2)+3`;
2. the `r=4` equality-five theorem classifies five unbased monomial orbits
   and makes exactly three pair-level `Delta_3` admissible;
3. a full-active-support equality-five pair in five coordinates is not
   pair-level admissible; and
4. the same exclusion holds on every full active support of size at least
   six.

The last two dependencies classify existing nonadmissible equality pairs;
they do not assert that equality-five pairs themselves are absent.

## 2. Full restriction forces pair-level admissibility

Let `B=B_ab` and let

```text
M={q in B:<q,A_S>=0}
```

be the left radical of the complement pairing.  Under `dim B=5`, pairing
rank three gives

```text
dim M=5-3=2.
```

Every mixed product `u_(a,c)u_(b,d)`, with `c!=d`, belongs to `M`.  The
three same-colour products have residue classes forming a basis of `B/M`.
It remains important to prove that the mixed products span all of `M`, not
merely a subspace of it.

Let `W` be their span and `D` the span of the three diagonal products.  The
diagonal residue classes are independent, so

```text
dim D=3,                 D intersect M=0.
```

The nine products of the two local bases span `B=U_aU_b`, hence

```text
B=W+D.
```

Since `W subset M`, the directness above gives

```text
5=dim B=dim W+3,
```

so `dim W=2` and `W=M`.  Therefore the restriction's own colour bases obey
exactly the pair-level `Delta_3` equality condition: the mixed products span
a two-plane and the three diagonal products are independent modulo it.

This implication is one-way.  A pair-level admissible frame supplies no
complementary modes and no full restriction.

## 3. Active-coordinate deletion is exact

Put

```text
T=supp(U_a+U_b),                 m=|T|.
```

Both local spaces have dimension three, so `m>=3`.  If `m=3`, both equal
the full linear coordinate space on `T`, and every product lies in its
three-dimensional square-free quadratic part.  This contradicts
`dim B_ab=5`; hence `m>=4`.

For arbitrary `m`, every coefficient outside `T` is identically zero on
both spaces.  Deleting those coordinates identifies their containing
subalgebra with `Z_m`.  It preserves:

- both three-plane dimensions;
- each of the nine products coefficient by coefficient;
- the span and dimension of `B_ab`;
- the mixed-product span; and
- independence of the diagonal products modulo that span.

Thus the support-five and support-at-least-six exclusion theorems apply to
the deleted pair without a genericity, specialization, or ambient-`r`
assumption.

The support cases are exhaustive:

```text
m<3:  incompatible with a three-dimensional local space;
m=3:  ambient square-free quadratic dimension is only 3;
m=4:  routed to the exact r=4 orbit classification;
m=5:  excluded by the active-support-five theorem;
m>=6: excluded by the active-support-at-least-six theorem.
```

The unique possible equality-five active support in a full restriction is
therefore `m=4`.

## 4. Normal support is not active support

After moving the four active coordinates to `x_0,...,x_3`, each local
three-plane is a hyperplane.  The `r=4` classification uses labels

```text
(s,k)=(common support size of the two hyperplane normals,
       smaller sign-block size).
```

That `s` is normal support, not the active coordinate support of the pair.
In particular, the `(3,1)` normals omit one coordinate, but the omitted
coordinate axis lies in both hyperplanes.  Its pair is active on all four
ambient coordinates.  The `(4,1)` and `(4,2)` normals use all four
coordinates, and their pairs are also active on all four.

The complete `r=4` equality-five list is

```text
coincident support-three hyperplane,
(2,1), (3,1), (4,1), (4,2).
```

The first two fail the invariant rank-one admissibility criterion.  Since a
full restriction supplies an admissible frame by Section 2, only

```text
(3,1), (4,1), (4,2)
```

survive.  The theorem's three displayed rational frames independently
replayed with mixed rank two and total product rank five.  Their unique
annihilator support-graph degree multisets are respectively

```text
(2,1,1,0), (3,1,1,1), (2,2,2,2),
```

so these three surviving unbased orbits are pairwise distinct.  The graph
degree invariant is used only to separate these three: the coincident
support-three orbit shares a graph type with `(4,1)` but is already
distinguished in the owning classification by intersection dimension.

## 5. Sensor corollary

Now assume only that the omitted pair in a full restriction has active
support at least five.  The co-two strengthening first gives

```text
dim B_ab>=5.
```

Equality would force pair-level admissibility and then contradict the
support-five or support-at-least-six exclusion.  Since dimension is
integral,

```text
dim B_ab>=6.
```

With `N=binomial(r,2)`, the unchanged perfect-pairing dimension inequality
is

```text
dim A_S+dim B_ab<=N+3.
```

Substitution gives exactly

```text
dim A_S<=N+3-6=N-3.
```

This is conditional on the active support of the particular omitted pair.
It neither asserts that all omitted pairs have support at least five nor
that any omitted pair has dimension exactly five.

## 6. Converse and status attacks

The following stronger readings were explicitly tested and are not made by
the package:

- an unbased pair of one of the three surviving types necessarily extends
  to a full restriction;
- every admissible based frame in a surviving unbased orbit is equivalent
  under the `Delta_3` stabilizer;
- the three displayed frames satisfy equations from the other `r-2` modes;
- every omitted pair in a putative restriction has active support at least
  five;
- every omitted pair has product dimension five;
- exclusion of support-five and larger equality pairs excludes the
  active-support-four residual; or
- the new sensor bound alone proves permanent nonrestriction.

The theorem consistently phrases the orbit conclusion as necessary and the
sensor improvement as conditional.  Its `UNKNOWN/UNRESOLVED` boundary is
therefore preserved.

## 7. Computational independence and replay

The primary verifier uses SymPy exact rational linear algebra.  It checks
all twelve frozen dependency hashes, the three bases and normal equations,
normal sign-split labels, active support, mixed rank, total rank, direct-sum
growth, explicit mixed generators, annihilator graph degrees, and the
dimension arithmetic.

The independent audit imports neither the primary verifier nor SymPy.  It
uses a separate `Fraction` row reducer, a separate modular reducer over
`F_5` and `F_7`, independently reconstructs the product tables and
annihilator checks, verifies the twelve dependency hashes, and routes every
support case.  Its finite-field replays are convention checks, not a
replacement for the characteristic-zero implication from the four written
dependencies.

Focused replay passed:

```text
synthesis primary exact verifier:              PASS;
synthesis independent no-import audit:         PASS;
all eight dependency primary/audit replays:    PASS;
py_compile:                                    PASS;
Ruff check:                                    PASS;
Ruff format check:                             PASS;
untracked-file whitespace checks:              PASS.
```

The synthesis audit reproduced dependency-manifest digest

```text
e81cb7a28f6f290770caf074650705ada7be7ae620a153705272fe9f6059d91f
```

and product-table digest

```text
29e7ae1dd211de2db11cbeef3d98e17b6734c00c82e227997fd43f95732dc6b8.
```

## 8. Accepted boundary

```text
full-restriction equality-five pair active support:       EXACTLY FOUR;
surviving unbased equality-five pair types:               THREE;
surviving labels:                                         (3,1),(4,1),(4,2);
active support at least five forces dim B_ab>=6:           PROVED;
then dim A_S<=binomial(r,2)-3:                             PROVED;
based-frame Delta_3-stabilizer classification:             OPEN;
extension of a surviving pair through all other modes:     OPEN;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

## Final reviewed hashes

```text
theorem:
9399CCB4286583A1F1E90BD7025E706B3DE47C652214BB1E8B7C8F6BA986A6D5

primary verifier:
517E778C7E0B994C2F94653303F85B4537125E174F9F5C96CEEE0F5BC721BE99

independent audit:
53BD2AFA681E3177F7014E3F9F379328A5F5839D4D82EB08E74A242561685A66
```
