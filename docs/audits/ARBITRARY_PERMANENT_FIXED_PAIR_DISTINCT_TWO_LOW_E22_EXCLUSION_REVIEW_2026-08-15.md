# Hostile review of fixed-pair distinct-two-low `E_22` exclusion

## Verdict and exact scope

**PASS, for the stated fixed-pair, pointwise, characteristic-zero
exclusion.** No dependency, coefficient-support, orientation, tensor-slot,
polarization-scalar, residual-table, common-kernel, rank, support-cover,
field, implementation, or scope blocker survived hostile review.

Assume the exact fixed-pair target equations and the reviewed
distinct-two-low reduction.  If the two high modes have pairing

```text
M_(st)=mu E_22,                  mu!=0,
```

then the target equations have no solution.  Thus the nonzero `E_22`
branch of that reduction is empty.

This package does not prove the distinct-two-low reduction itself, does not
address the zero high-pairing branch, does not normalize an arbitrary
equality-five pair to the fixed pair, and does not resolve unrestricted
permanent nonrestriction.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_E22_EXCLUSION_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py
  audit_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py
```

The initial theorem draft used the word `support` without explicitly
binding it to the local coefficient row of the normalized pure-`R` low
generator.  That was a genuine statement ambiguity.  Before this verdict,
the author replaced it by

```text
p=sum_c alpha_c y_(a,c),       q=sum_c beta_c y_(b,c)
```

and explicitly stated that the supports are those of `alpha` and `beta`.
This review applies only to the repaired final theorem bytes recorded below.

## 1. Frozen dependency and exhaustive input

The current-byte distinct-two-low theorem and both of its checkers replayed
successfully.  It gives exactly the following data used here:

```text
two low modes a,b in distinct slots;
a low only for Phi_1 and b low only for Phi_2;
two remaining modes high for both families;
M_(st)=mu E_22, mu!=0;
high A-ranks (1,2) or (2,1);
the rank-one high A-map supported only at colour 2;
low pair A_0/A_1 or C_0/C_1;
both low coefficient supports contain colour 2;
at least one low A-map has rank two on colours 0,1.
```

Relabelling the two high modes so that `s` is the rank-one shore and `t`
the rank-two shore is legitimate: `J` is symmetric and `E_22` is equal to
its transpose.  Consequently

```text
A_s e_0=A_s e_1=0,       rank A_s=1,       rank A_t=2.
```

For an `A_0/A_1` low pair, the coefficient supports are respectively
`{2}` or `{1,2}` and `{2}` or `{0,2}`.  For a `C_0/C_1` pair, they are
respectively `{2}` or `{0,2}` and `{2}` or `{1,2}`.  Hence the four line
rows and the singleton/support-two split used in the proof are exhaustive;
no empty, one-colour-away-from-`2`, same-missing, common-line, or same-mode
case belongs to this branch.

The high-rank profiles and the rank-two-low alternative were also checked
against the reviewed support-two incidence dependency.  This use is not
circular: the predecessor leaves `E_22` explicitly open, while the present
package consumes its necessary conditions and adds the full target
equations.

## 2. Independent residual-table derivation

Write

```text
h_2 = x_0-x_1-x_2+x_3,
h_2'= -x_0+x_1-x_2+x_3.
```

Direct bilinear contraction of the five displayed residual quadratics by
the four normalized low directions gives:

```text
line   zero mixed row   d_2 row   other diagonal row       extra colour

A_0       h_2           -2x_1       h_2+2x_2                    1
C_0       h_2           -2x_1       h_2-2x_3                    0
A_1       h_2'          -2x_0       h_2'+2x_2                   0
C_1       h_2'          -2x_0       h_2'-2x_3                   1.
```

For example, contracting `A_0=x_0+x_3` into
`x_0(x_3-x_2-x_1)` gives `h_2`, while contracting it into
`-2x_0x_1` gives `-2x_1`.  The primary verifier derives all twenty channel
contractions from factorized quadratics.  The audit separately rebuilds
them as square-free edge dictionaries.

Each displayed triple has rank three.  Solving the three equations gives
the exact one-dimensional common kernels

```text
A_0: K(1,0,0,-1),       C_0: K(1,0,1,0),
A_1: K(0,1,0,-1),       C_1: K(0,1,1,0).
```

The factors `2` are the only field-sensitive feature in these row and
kernel calculations.  Characteristic zero is therefore sufficient.

## 3. Tensor-slot legality and the rank-two gate

This was the main hostile target.  Contract a pure-`R` low vector in one
input slot of `x_4x_5g`.  Three distinct input modes `u,s,t` remain.  Fix
colour `i=0,1` in mode `s`.  Because `A_s e_i=0`, both polarization terms
which assign either `x_4` or `x_5` to mode `s` vanish.  The sole surviving
supplier assignment uses modes `u` and `t`, so the matrix on their local
coefficient spaces is exactly

```text
g(r_(s,i)) B_(ut),       B_(ut)=A_u^T J A_t.
```

The primary verifier checks this scalar-one identity symbolically for every
distinct nonzero residual.  The no-import audit checks it on all coordinate
basis triples with an independent monomial-dictionary polarizer.  Even a
different nonzero polarization convention would preserve the zero and rank
contradictions, but the stated convention in fact has no omitted scalar.

Every contraction and every `A`-supplier assignment above uses different
tensor slots.  No low is contracted twice, no two vectors from one local
plane are inserted into distinct tensor slots, and the matrix `B_(ut)`
always belongs to the two uncontracted shores named by its indices.

If `A_u` and `A_t` both have rank two, they are onto the two-dimensional
space `A`.  Since `J:A -> A^*` is an isomorphism and
`A_u^T:A^* -> K^3` is injective,

```text
rank(A_u^T J A_t)=2.
```

Equivalently, for any nonzero selected minors,

```text
det B_(ut)[I,J]
 = det(A_u[:,I]) det(J) det(A_t[:,J]) != 0.
```

Both implementations check all nine selected-minor identities by separate
symbolic representations.

## 4. Orientation I

Suppose the `Phi_1` low mode `a` has rank two on its colour-`0,1`
columns.  Then `A_a` and `A_t` are onto, so

```text
rank B_(at)=2.
```

Contract the family-`2` low in mode `b`.  It is `A_1` or `C_1`.  In
colours `i=0,1` of the rank-one high mode `s`, the mixed target and the
off-target `d_2` coefficient both vanish.  Since `B_(at)` is nonzero, the
two residual equations force

```text
h_2'(r_(s,i))=0,       x_0(r_(s,i))=0.
```

If the coefficient support of the low generator is the singleton `{2}`,
its other diagonal target also vanishes.  The appropriate third row in the
table therefore puts both `r_(s,0)` and `r_(s,1)` on the same one-dimensional
common-kernel line.  Their `A`-parts vanish as well, so the full local
columns `y_(s,0),y_(s,1)` are dependent, contradicting independence of the
ordered local triple.

If the coefficient support is `{k,2}`, then `beta_k!=0`.  At colour `k`
in mode `s`, the live diagonal target instead gives

```text
g_k(r_(s,k)) B_(at)=beta_k lambda_k E_kk.
```

The right side is nonzero of rank one.  Thus the residual scalar on the
left is nonzero, making the left side rank two, a contradiction.  This
handles both `A_1` and `C_1`, and both of their possible supports.

## 5. Orientation II and case exhaustion

If the colour-`0,1` rank of `A_a` is not two, the predecessor's exact
maximum condition forces the family-`2` low map `A_b` to have rank two
there.  Contract the family-`1` low in mode `a`.  Now

```text
rank B_(bt)=2,
```

and the mixed and off-target `d_2` equations force

```text
h_2(r_(s,i))=0,        x_1(r_(s,i))=0,       i=0,1.
```

For singleton support, the third zero residual places both columns on the
`A_0` or `C_0` common-kernel line and violates local independence.  For
support `{k,2}`, the live diagonal equation equates a nonzero rank-two
matrix with a nonzero multiple of `E_kk`, again impossible.

The maximum condition selects orientation I whenever the first low has
rank two and orientation II otherwise.  If both have rank two, orientation
I already applies.  Across the two orientations the proof explicitly
covers

```text
A_0, C_0, A_1, C_1
times
singleton {2}, support {k,2}.
```

Thus family exchange, colour `0/1` exchange, both different-missing pairs,
both choices of the rank-two low shore, and all eight line/support cases
are covered.  No genericity, algebraic closure, order, positivity,
finite-field inference, or unproved converse is used.

## 6. Computational replay and independence

Focused current-byte replay passed:

```text
new primary exact verifier:                    PASS;
new independent no-import audit:               PASS;
distinct-two-low dependency primary/audit:     PASS/PASS;
support-two incidence primary/audit:           PASS/PASS;
py_compile on all six replayed scripts:         PASS;
Ruff on all six replayed scripts:               PASS;
tracked diff whitespace check:                  PASS;
new-package trailing-whitespace scan:           PASS.
```

The primary verifier uses SymPy to derive the residuals, quartic
contraction scalars, high-slice identities, selected minors, common kernels,
and support split.  The audit imports neither the primary module nor SymPy;
it uses `Fraction`, independent edge/monomial dictionaries, a separate row
reducer, and a separate polarization evaluator.  It checks `20` quartic
contractions, `1152` basis high-slice evaluations, all `9` selected-minor
identities, all `4` common kernels, both orientations, and all `8`
line/support cases.

The executables replay the displayed exact algebra.  The written
characteristic-zero rank and case argument proves the exclusion.  Both
executables preserve the global `UNRESOLVED` status.

## 7. Accepted boundary

```text
fixed equality-five pair:                              ASSUMED;
exact distinct-two-low reduction:                      ASSUMED, REVIEWED;
nonzero high pairing M_(st)=mu E_22:                   EXCLUDED;
zero high-pairing branch:                              NOT ADDRESSED HERE;
arbitrary equality-five normalization:                 NOT PROVED HERE;
unrestricted P_6 -> Delta_3:                           UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.
```

## Final reviewed hashes

```text
new theorem:
925284C772176125855BF99199B6789E430355A0D4F87553E727CA746B206925

new primary verifier:
00BA077A4F4023ECA875C2B9DD826D8FFC2690723CBA16B1C6737720A611E2FC

new independent audit:
0B640BF86F7C495821705D3489307ECA668BFD6951AF342B18665E2B577473B8

distinct-two-low dependency theorem:
87BD9CCC45C07088465C27FB4032BCC34DDB7004789A3FC28ECA36F3BFA67D1E

distinct-two-low dependency primary:
20ECAA638C7AFDFB11187925C76AA6DD9F142E63AE41AD5220F27FA70518290A

distinct-two-low dependency audit:
F8A1350BD36DA6CFCEBCA674791F44B6DBCF00BD782F53B6319E609005658D56

support-two incidence dependency theorem:
8C6B0EB9AA3BDD885A0703AB1EE902456045A7DEA89B66E0C097654F1189631F

support-two incidence dependency primary:
F7998E863E519BC1620384D94D9E3BF9F318907C7795A65BD50BD1A8195DF54B

support-two incidence dependency audit:
455E7196E534818602AA7385A54DF748DE5A9329F88E7E3CF10B8A2E7CB9CA32
```
