# Hostile review of the fixed-pair simultaneous-low rank-three sharpness fixture

## Verdict and exact boundary

**PASS, as an exact rational sharpness fixture and explicitly not as a
`Delta_3` restriction.**  No algebraic, rank, basis-change, implementation,
or scope blocker survived hostile review.

For the fixed equality-five pair, the displayed four rational local planes
simultaneously have

```text
ambient local ranks:                      (3,3,3,3);
Phi_1 projection ranks:                   (1,3,2,2);
Phi_2 projection ranks:                   (2,2,3,1);
both mixed-radical tensors:               ZERO;
D^*-output flattening rank:               3;
input flattening ranks:                   (3,1,1,2);
CP tensor rank of the D^*-valued sensor:  3.
```

Independent local basis changes make all three intended monochromatic pure
coefficients nonzero.  Nevertheless, input ranks `(3,1,1,2)` are invariant
under every local `GL_3` change and every invertible output change, whereas
a nondegenerate three-colour diagonal target has ranks `(3,3,3,3)`.  The
fixture is therefore **not** a restriction to `Delta_3` and is not a
counterexample to permanent nonrestriction.  The global Krenn--Gu status
remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_SIMULTANEOUS_LOW_MIXED_ZERO_SENSOR_RANK_THREE_SHARPNESS.md
  verify_arbitrary_permanent_fixed_pair_simultaneous_low_mixed_zero_sensor_rank_three_sharpness.py
  audit_arbitrary_permanent_fixed_pair_simultaneous_low_mixed_zero_sensor_rank_three_sharpness.py
```

Two precision issues found during hostile review were corrected before this
PASS:

1. output rank three is now justified by the independent mode-`2` slice
   factors, equivalently by three ledger rows isolating the outputs, rather
   than merely by the existence of independent output labels;
2. the assembled sensor is correctly typed as `D^*`-valued, in the basis
   dual to `(d_0,d_1,d_2)`.

Neither correction changes the construction or any computed rank.

## 1. Fixed pair and complementary quartics

Independent square-free multiplication agrees with the fixed-pair
predecessors.  In edge order `(01,02,03,12,13,23)`, the product-space basis
is

```text
m_1=(0,1,-1,0,0,-1),       m_2=(0,0,0,1,-1,-1),
d_0=(1,1,0,0,-1,-1),       d_1=(1,0,-1,1,0,-1),
d_2=(0,0,0,0,0,-2).
```

The complementary quartics are exactly

```text
star(m_1)=x_4x_5 x_1(x_3-x_2-x_0),
star(m_2)=x_4x_5 x_0(x_3-x_2-x_1),

star(d_0)=x_4x_5(x_1+x_2)(x_3-x_0),
star(d_1)=x_4x_5(x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5x_0x_1.
```

Thus the projection families in the fixture are the genuine mixed-factor
maps

```text
Phi_1=(x_1,x_4,x_5,x_3-x_2-x_0),
Phi_2=(x_0,x_4,x_5,x_3-x_2-x_1).
```

No alternate sign convention or coordinate ordering is used.

## 2. The signed rational tuple and projection ranks

Direct exact row reduction confirms that each displayed local triple is
independent.  Evaluating the two projection matrices on those twelve
vectors gives

```text
Phi_1: (1,3,2,2),
Phi_2: (2,2,3,1).
```

In particular, neither projection family is everywhere full: `Phi_1`
drops at modes `2,4,5`, and `Phi_2` drops at modes `2,3,5`.  The tuple lies
strictly inside the simultaneous-low residual of the fixed-pair two-sided
theorem.  The rank-one entries in the profiles cause no scope problem; the
predecessor conclusion only requires a rank-at-most-two mode in each
family.

## 3. All mixed zeros and the exact five-word ledger

Full square-free coefficient extraction on all `3^4=81` input words gives

```text
T_(m_1)=T_(m_2)=0
```

entrywise.  Since the displayed triples are bases of the four planes, these
are tensor identities, not sampled zeros.  The off-diagonal products of the
fixed pair lie in `span{m_1,m_2}`, so the whole pair-mixed part vanishes.

The three diagonal-output coordinates have exactly five nonzero words:

```text
0220  (0, 4, 4)
0221  (0, 0,-4)
1220  (0,-4, 0)
2220  (0, 4, 0)
2221  (4, 0, 0).
```

The two independent implementations reproduce the same canonical ledger
hash:

```text
9c32b5a913ef3c4e7fc87eb9eb546ed578437a2c656fe5c5d5358737e57772ea
```

The rows `2221`, `1220`, and `0221` isolate the three output coordinates,
already giving an exact output-flattening rank lower bound of three.

## 4. Factorization, output rank, and CP rank

Let `epsilon_(t,i)` be dual to the displayed basis vector `a_(t,i)`.  The
three output slices factor as

```text
T_d0=4 epsilon_(2,2) tensor epsilon_(3,2)
       tensor epsilon_(4,2) tensor epsilon_(5,1),

T_d1=4 (epsilon_(2,0)-epsilon_(2,1)+epsilon_(2,2))
       tensor epsilon_(3,2) tensor epsilon_(4,2)
       tensor epsilon_(5,0),

T_d2=4 epsilon_(2,0) tensor epsilon_(3,2)
       tensor epsilon_(4,2)
       tensor (epsilon_(5,0)-epsilon_(5,1)).
```

The mode-`2` factors have coordinate rows

```text
(0,0,1),  (1,-1,1),  (1,0,0),
```

whose determinant is nonzero.  Hence the three slice tensors are linearly
independent, and the `D^*` output flattening has rank exactly three.  This
also follows from the three isolating ledger rows above.

Assembling the sensor as

```text
sum_(c=0)^2 T_dc tensor d_c^*
```

gives a three-term rank-one decomposition, so CP rank is at most three.
Output-flattening rank is a lower bound for CP rank, so the CP rank is
exactly three.  Each nonzero fixed output slice is itself rank one and has
multilinear rank `(1,1,1,1)`.

## 5. Exact input nonconciseness

Across the three CP summands, the input factor spans are

```text
mode 2: span{(0,0,1),(1,-1,1),(1,0,0)}       dimension 3;
mode 3: one common epsilon_(3,2) direction    dimension 1;
mode 4: one common epsilon_(4,2) direction    dimension 1;
mode 5: span{epsilon_(5,1),epsilon_(5,0)}     dimension 2.
```

The complementary factors for the three summands include the independent
output directions `d_0^*,d_1^*,d_2^*`, so no cancellation lowers these
span dimensions.  They are exactly the four input flattening ranks

```text
(3,1,1,2).
```

A nondegenerate diagonal target

```text
sum_c lambda_c e_c^* tensor e_c^* tensor e_c^*
               tensor e_c^* tensor d_c^*,
lambda_c!=0,
```

has input flattening rank three at every mode.  Flattening ranks are
preserved by invertible maps on every input factor and on the output factor.
The fixture cannot therefore be locally equivalent to the target, even if
one grants an arbitrary invertible output change.  This is a basis-invariant
obstruction, not a failure of the initially displayed colour labels.

## 6. Alternative bases and pure coefficients

The alternative bases have coordinate-change matrices

```text
mode 2: (a_22, a_21, a_20),
mode 3: (a_32, a_32+a_30, a_32+a_31),
mode 4: (a_42, a_42+a_40, a_42+a_41),
mode 5: (a_51, a_50, a_50+a_52).
```

Their determinants are nonzero, so these are genuine independent local
`GL_3` changes.  Substitution into the factored slices gives

```text
T_d0(000)= 4,
T_d1(111)=-4,
T_d2(222)= 4.
```

The mixed tensors remain identically zero because a basis change cannot
alter a zero tensor.  Direct evaluation also confirms that many other
`d_c` mixed-colour entries remain.  The three desired pure coefficients can
therefore be made nonzero simultaneously, but the tensor is still not
diagonal; input rank proves that no further invertible basis choice can
make it so.

## 7. Independence and focused replay

The primary verifier constructs the five outputs directly from the original
quadratic edge vectors and exact square-free multiplication.  It checks all
81 words, both projection profiles, all five support words, output and input
flattenings, each slice flattening, the alternative bases, and the pure
values with exact SymPy linear algebra.

The no-import audit does not import the primary verifier or SymPy.  It starts
from the independently factored complementary quartics, evaluates their
polarizations by an explicit 24-term permanent sum, and uses a custom
standard-library rational reducer.  It also rechecks the output and input
ranks over `F_3`.  Agreement of the full 81-by-5 ledger hash ties the two
routes to the same signed rational fixture.

Focused replay passed:

```text
new primary exact verifier:                     PASS;
new independent no-import audit:                PASS;
fixed-pair two-sided predecessor primary/audit: PASS/PASS;
fixed-pair full-projection primary/audit:        PASS/PASS;
py_compile:                                     PASS;
Ruff:                                           PASS;
git diff --check:                               PASS.
```

The new package was absent from `origin/main` commit
`4efbbd2c4dc364930809cfceb5486268fa3fd00f`.  This is a repository-level
novelty observation only, not an external priority claim.

## 8. Accepted claims and exclusions

```text
fixed equality-five pair:                              YES;
four rank-three complementary planes:                  YES;
simultaneous projection drop:                          YES;
both full mixed-radical tensors zero:                  YES;
D^* output rank three:                                 YES;
CP tensor rank three:                                  YES;
each output slice rank one:                            YES;
three nonzero monochromatic coefficients in bases:     YES;
input-concise in all four modes:                        NO, (3,1,1,2);
restriction to Delta_3:                                NO;
counterexample to permanent nonrestriction:            NO;
closure of simultaneous-low residual:                  NO;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

This fixture shows that output sensor rank three is a necessary but
insufficient survivor test.  Any actual restriction in the simultaneous-low
residual must also pass the input-conciseness gate `(3,3,3,3)` and all
remaining mixed-colour equations.

Any later integration that changes the live mathematical frontier must
update the canonical frontier and theorem-ledger artifacts under the
repository contract.  This review does not perform that integration.

## Final reviewed hashes

```text
new theorem:
B6A32BE842DB6A5DF243750966AFF25C0DB9E6CB981EA5ABDE52243D2837D128

new primary verifier:
7CF225CDA70EBC35EBC31DD86AF33C1A22F443705809D000AAB2D7C37057EA71

new independent audit:
17E3C1F0844C3AA9EA9D850BFB72DDE039310369FCD3AF156A1DACF4D2A98DCA

fixed-pair two-sided theorem:
A383731E094E0D0E45482AAB889FB8B202FC7A2CF452D8534D5035E737089F36

fixed-pair full-projection theorem:
727F39246FA64C899D1F51377FCB3C58640174C044510F727C796C888798F7C2
```
