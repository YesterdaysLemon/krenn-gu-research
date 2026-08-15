# Hostile review of the concise simultaneous-low sharpness fixture

## Verdict and exact scope

**PASS, as an exact rational boundary fixture and explicitly not as a
`Delta_3` restriction.**  No algebraic, rank, basis-change, implementation,
or scope blocker survived hostile review.

For the fixed equality-five pair, the displayed four local planes satisfy

```text
ambient local ranks:                         (3,3,3,3);
Phi_1 projection ranks:                      (2,2,2,2);
Phi_2 projection ranks:                      (1,3,2,2);
both mixed-radical tensors:                  ZERO;
five one-factor flattening ranks:            (3,3,3,3,3);
largest exhibited two-factor rank:           9;
five-way CP tensor rank:                     AT LEAST 9.
```

Independent local basis changes make all three intended monochromatic pure
coefficients nonzero.  The fixture nevertheless is not diagonal: its fixed
output slices have multilinear ranks greater than one, and an exact
two-versus-three flattening has rank nine.  A nondegenerate three-colour
diagonal target has CP rank exactly three.  This construction is therefore
not a permanent restriction or counterexample.  The global Krenn--Gu
status remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_SIMULTANEOUS_LOW_CONCISE_MIXED_ZERO_SLICE_RANK_SHARPNESS.md
  verify_arbitrary_permanent_fixed_pair_simultaneous_low_concise_mixed_zero_slice_rank_sharpness.py
  audit_arbitrary_permanent_fixed_pair_simultaneous_low_concise_mixed_zero_slice_rank_sharpness.py
```

The first simultaneous-low sharpness fixture and the fixed-pair two-sided
projection-drop package were replayed as predecessors.  The present result
is stronger than the first fixture only as a sharpness boundary: it passes
input and output conciseness, but it still fails the exact target.

## 1. Pair convention and local tuple

Independent square-free multiplication agrees with the fixed-pair
predecessors.  The complementary quartics are

```text
star(m_1)=x_4x_5x_1(x_3-x_2-x_0),
star(m_2)=x_4x_5x_0(x_3-x_2-x_1),
star(d_0)=x_4x_5(x_1+x_2)(x_3-x_0),
star(d_1)=x_4x_5(x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5x_0x_1.
```

The sensor is correctly typed as `D^*`-valued in the basis dual to
`(d_0,d_1,d_2)`.  Its two mixed-factor maps are

```text
Phi_1=(x_1,x_4,x_5,x_3-x_2-x_0),
Phi_2=(x_0,x_4,x_5,x_3-x_2-x_1).
```

Exact rational row reduction confirms that each displayed local triple has
rank three.  Evaluating the projection matrices gives the profiles

```text
Phi_1=(2,2,2,2),
Phi_2=(1,3,2,2).
```

Both families therefore contain low modes; the tuple lies in the residual
left open by the two-sided theorem.

## 2. Mixed zeros and full conciseness

Direct evaluation of all `3^4=81` words gives

```text
T_(m_1)=T_(m_2)=0
```

entrywise.  Because the displayed triples are bases, these are complete
four-linear tensor identities, not sampled equations.  The off-diagonal
products of the fixed pair lie in `span{m_1,m_2}`, so the whole pair-mixed
part vanishes.

The three words

```text
0021  (-2,0,0),
0011  (0,-2,0),
0010  (0,0,-2)
```

isolate the three `D^*` coordinates.  Thus the output flattening has rank
three.  Exact one-factor flattening of the full five-way tensor gives rank
three at each of `L_2,L_3,L_4,L_5,D^*`.  The construction is concise at all
five factors, so the non-Delta conclusion cannot be attributed to the input
rank defect of the first sharpness fixture.

The two independent implementations reproduce the same canonical
81-by-5 ledger hash:

```text
75cb40627e831f485850b34dd41a18959e2f808e8d1fbaabdc5487cde3ab34a7
```

## 3. Fixed output slice ranks

For the three fixed output coordinates, exact input-mode flattenings give

```text
T_d0: (2,3,3,2),
T_d1: (2,2,3,2),
T_d2: (2,3,2,2).
```

Every nonzero rank-one four-tensor has multilinear rank `(1,1,1,1)`.
Therefore no fixed output slice here is rank one.  Invertible local basis
changes preserve these ranks, and nonzero diagonal output rescaling merely
rescales each slice.  No such transformation can turn this sensor into the
fixed-output diagonal target.

This argument uses the actual fixed diagonal output directions of the pair.
The stronger full-tensor argument below also allows arbitrary output mixing.

## 4. Exact rank-nine flattening certificate

The ten unordered two-factor flattening ranks of the five-way tensor are

```text
L_2 L_3: 8,      L_2 L_4: 7,      L_2 L_5: 8,
L_2 D^*: 6,      L_3 L_4: 8,      L_3 L_5: 9,
L_3 D^*: 8,      L_4 L_5: 8,      L_4 D^*: 8,
L_5 D^*: 6.
```

The load-bearing `L_3 tensor L_5` flattening is a `9 x 27` exact integer
matrix.  In lexicographic complementary coordinates `(L_2,L_4,D^*)`, the
columns

```text
(0,0,0), (0,0,2), (0,1,1), (0,1,2), (0,2,0),
(1,0,1), (1,0,2), (1,2,1), (2,0,0)
```

form a `9 x 9` minor of determinant

```text
-1024.
```

This independently pins rank nine over `Q`; it is not a numerical rank or
tolerance result.  Every matrix flattening rank is a lower bound for CP
tensor rank, so the full five-way tensor has CP rank at least nine.

A nondegenerate three-colour diagonal tensor is the sum of three rank-one
terms and has output rank three, hence CP rank exactly three.  Tensor rank
and matrix-flattening ranks are invariant under
`GL_3^4 x GL(D^*)`.  The fixture is not equivalent to the target even after
an arbitrary invertible output change.

## 5. Alternative colour bases

The four displayed coordinate-change matrices in the theorem have nonzero
rational determinants.  They therefore define genuine independent local
`GL_3` changes.  Direct substitution gives

```text
T_d0(000)= 2,
T_d1(111)= 2,
T_d2(222)=-2.
```

The mixed-radical tensors remain zero because zero is basis invariant.
Other fixed-output mixed-colour entries survive, as they must from the
slice-rank and tensor-rank obstructions.  Thus all intended pure values can
be nonzero simultaneously, but this fact does not repair the non-Delta
tensor.

## 6. Computational independence and replay

The primary verifier constructs the five outputs from the original edge
quadratics using exact square-free multiplication and uses SymPy only for
exact ranks.  It checks every ledger word, both projection profiles, all
five one-factor and ten two-factor flattenings, all twelve fixed-slice mode
ranks, the alternative bases, and the three pure values.

The no-import audit does not import the primary verifier or SymPy.  It starts
from independently factored complementary quartics, evaluates each by an
explicit 24-term permanent sum, and uses custom rational Gaussian
elimination.  Agreement on all rank ledgers and the full ledger hash provides
a genuinely different implementation route.

Focused replay passed:

```text
new primary exact verifier:                         PASS;
new independent no-import audit:                    PASS;
first simultaneous-low fixture primary/audit:       PASS/PASS;
fixed-pair two-sided predecessor primary/audit:      PASS/PASS;
py_compile:                                         PASS;
Ruff:                                               PASS;
git diff --check:                                   PASS.
```

The new package was absent from `origin/main` commit
`4efbbd2c4dc364930809cfceb5486268fa3fd00f`.  This is a repository-level
novelty observation only, not an external priority claim.

## 7. Accepted boundary

```text
fixed equality-five pair:                          YES;
four rank-three local planes:                      YES;
both mixed-radical tensors zero:                   YES;
simultaneous projection drop:                      YES;
output flattening rank three:                      YES;
all four input flattening ranks three:             YES;
all three monochromatic values nonzero in bases:   YES;
each fixed output slice rank one:                  NO;
five-way tensor rank three:                        NO, rank at least 9;
restriction to Delta_3:                            NO;
counterexample to permanent nonrestriction:        NO;
closure of simultaneous-low residual:              NO;
global Krenn--Gu conjecture:                        UNRESOLVED.
```

The resulting next survivor gate is exact for this fixed output basis: all
three nonzero diagonal slices must be rank-one four-tensors, and their three
factor lines must span each local dual three-space.  Conciseness and output
rank alone are insufficient.

Any later integration that changes the live mathematical frontier must
update the canonical frontier and theorem-ledger artifacts under the
repository contract.  This review does not perform that integration.

## Final reviewed hashes

```text
new theorem:
78673A99369ADB2427C6C3F9867D90FDB752C00FDFBDC4A89F094F43564F405F

new primary verifier:
DF8D414938E44245EB8082BBEAA652D57E70DDA4EEB7DD663E5468643B15B369

new independent audit:
45BF0AE22EBDEF2E44F41BC13233FAA1E9F0D96C1A40142FFC6D22CB8535D779

first simultaneous-low sharpness theorem:
B6A32BE842DB6A5DF243750966AFF25C0DB9E6CB981EA5ABDE52243D2837D128

fixed-pair two-sided theorem:
A383731E094E0D0E45482AAB889FB8B202FC7A2CF452D8534D5035E737089F36
```
