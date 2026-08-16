# Hostile review of fixed-pair two-low zero-branch exclusion

## Verdict and exact scope

**PASS, for the stated fixed-pair, pointwise, characteristic-zero zero
branch.**  No low-line orientation, projective-scaling, high-rank,
covector-independence, tensor-factor, same-slot, two-term-cancellation,
orthogonal-line, field, quantifier, dependency, implementation, or scope
blocker survived hostile review.

Assume the committed same-mode exclusions and distinct-two-low reduction.
Thus the four remaining tensor slots consist of one `Phi_1`-only low, one
`Phi_2`-only low, and two modes high for both projection families.  This
package proves that the pairing matrix between the two high `A`-images
cannot be zero.

It does not exclude the surviving nonzero-`E_22` branch, normalize an
arbitrary equality-five pair to the fixed pair, or prove unrestricted
permanent nonrestriction.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_TWO_LOW_ZERO_BRANCH_EXCLUSION_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py
  audit_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py
```

Load-bearing frozen dependency:

```text
commit aa21e10
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_REDUCTION_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py
  audit_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py
```

## 1. Reduction data and all four low generators

After a harmless permutation of the four symmetric tensor slots, the
predecessor gives

```text
a: Phi_1-only low, with line A_0 or C_0;
b: Phi_2-only low, with line A_1 or C_1;
s,t: high for both families;
A_s^T J A_t=0.
```

For

```text
l_1=x_3-x_2-x_0,                 l_2=x_3-x_2-x_1,
h_1=x_1+l_1,                     h_2=x_0+l_2,
```

direct contraction gives the complete four-row table

```text
low generator     opposite mixed quadratic     contracted residual

A_0               x_0 l_2                      h_2=(1,-1,-1,1)
C_0               x_0 l_2                      h_2=(1,-1,-1,1)
A_1               x_1 l_1                      h_1=(-1,1,-1,1)
C_1               x_1 l_1                      h_1=(-1,1,-1,1).
```

Indeed `x_0(p)=l_2(p)=1` for both `p in {A_0,C_0}`, while
`x_1(q)=l_1(q)=1` for both `q in {A_1,C_1}`.  Multiplying a projective
generator by a nonzero scalar multiplies the entire contracted equation by
that scalar, so no normalization-dependent zero or independence claim is
being made.  The proof uses neither the singleton nor support-two
realization of either low line.  The family labels remain fixed; only the
positions of their two low slots may be exchanged.  That relabelling is
legitimate because complete polarization and the exact target are symmetric
in the four local slots.

## 2. Rank-one high shores and forced covector independence

The high maps `A_s,A_t` are nonzero.  If one vanished, either projection
family on that local three-space would have only its two displayed
`R`-covectors and hence rank at most two.  Nondegeneracy of `J` in the
two-dimensional space `A`, together with

```text
J(im A_s,im A_t)=0,
```

then forces both maps to have rank one.  Thus, for nonzero vectors and
covectors,

```text
A_s=u rho_s,                 A_t=v rho_t,             J(u,v)=0.
```

On either high shore, rank three of `Phi_2` says

```text
x_0|L, l_2|L, rho|L
```

are independent.  Since `h_2=x_0+l_2`, elementary column addition gives

```text
det(x_0,l_2,rho)=det(x_0,h_2,rho),
```

so `rho` and `h_2|L` are independent.  The identical argument for
`Phi_1` gives independence of `rho` and `h_1|L`.  This applies separately
to both `s` and `t`; in particular none of the residual covectors used in
the separation step can vanish.  No quotient-dimension or generic-rank
assumption is hidden here.

## 3. Legal mixed contractions and two-term separation

Contract `T_(m_2)=0` once, and only once, in the low slot `a` by its
`Phi_1` exceptional vector.  On the remaining ordered slots `(b,s,t)`,
complete polarization gives

```text
 J(A_b(-),u) tensor rho_s tensor h_2|L_t
+J(A_b(-),v) tensor h_2|L_s tensor rho_t
+J(u,v) h_2|L_b tensor rho_s tensor rho_t=0.
```

The third summand vanishes because `J(u,v)=0`.  The current frozen theorem
has the corrected factor order

```text
h_2|L_b tensor rho_s tensor rho_t;
```

this review was restarted on those corrected bytes.  That term assigns
`x_4,x_5` to the two high slots and the residual covector to the remaining
low slot, exactly as complete polarization requires.

Because `rho_s` and `h_2|L_s` are independent, one can evaluate first on a
vector killing `h_2|L_s` but not `rho_s`, and then on one killing `rho_s`
but not `h_2|L_s`.  The nonvanishing of `h_2|L_t` and `rho_t` separately
forces

```text
J(A_b(-),u)=J(A_b(-),v)=0.
```

The family-reversed contraction of `T_(m_1)=0`, once in slot `b` by its
`Phi_2` exceptional vector, similarly gives

```text
J(A_a(-),u)=J(A_a(-),v)=0.
```

Thus

```text
im A_a, im A_b subset u^perp intersect v^perp.
```

Each displayed contraction inserts one vector into one actual local slot.
The two low contractions occur in separate equations.  No same-mode double
contraction, implicit slot reuse, or movement of a vector between local
spaces occurs.

## 4. Exhaustive two-dimensional closure

If `u,v` are independent, their common orthogonal complement is zero, so
`A_a=A_b=0`.  The only remaining possible `A` suppliers are `s,t`, whose
pairing matrix is zero by hypothesis.

If `u,v` are dependent, write `v=cu` with `c!=0`.  The high-high zero
pairing gives `J(u,u)=0`.  In a nondegenerate two-dimensional space an
isotropic line is self-orthogonal, so

```text
(Ku)^perp=Ku.
```

Both high images and, by the mixed contractions, both low images lie in
`Ku`.  Every cross-mode `J`-pairing therefore vanishes in this case as
well.  Independent versus dependent is exhaustive over the stated field;
there is no missing anisotropic dependent case because dependence plus
`J(u,v)=0` itself forces isotropy.

Every term in the polarization of an `x_4x_5 g` quartic assigns `x_4` and
`x_5` to two distinct tensor slots and is weighted by exactly one of these
cross-mode `J`-pairings.  Hence every target tensor would vanish, contrary
to, for example,

```text
T_(d_0)(e_0,e_0,e_0,e_0)=lambda_0!=0.
```

This is the final diagonal contradiction: once every pairing is zero, no
pair of distinct modes can supply the two `A` factors.

## 5. Field, quantifier, and audit boundary

The proof is pointwise for every exact fixed-pair extension satisfying the
predecessor hypotheses and every nonzero `lambda_c`.  It uses only
finite-dimensional linear algebra, nondegeneracy of `J`, complete
polarization, and nonzero projective scalars.  Characteristic zero keeps
the displayed coefficient `2` nonzero and is exactly the inherited scope.
There is no appeal to order, positivity, algebraic closure, genericity,
numerical approximation, or a finite-field-to-characteristic-zero
inference.

The finite-field runs are error-detecting audits of the tensor identities,
separation lemma, and orthogonal-line dichotomy.  The written argument,
not the finite enumeration, proves the characteristic-zero statement.

## 6. Computational replay and independence

Focused current-byte replay passed:

```text
zero-branch primary exact verifier:                    PASS;
zero-branch independent no-import audit:               PASS;
distinct-two-low predecessor primary:                  PASS;
distinct-two-low predecessor no-import audit:          PASS;
py_compile on new and predecessor scripts:             PASS;
Ruff on new and predecessor scripts:                   PASS;
tracked and untracked whitespace checks:               PASS.
```

The primary verifier checked all four exceptional-generator contractions,
four direct symbolic factorizations, the determinant identity, `421824`
`F_3` cancellation cases, and the `F_5` orthogonal dichotomy (`64`
independent and `32` dependent pairs).

The audit imports neither the primary module nor SymPy.  It independently
rebuilds the square-free quartics, checks `216` direct polarization fixture
entries, checks `19683` determinant-grid cases (`11808` full-rank cases),
replays `421824` `F_3` cancellation cases, and checks the `F_7` dichotomy
(`216` independent and `72` dependent pairs).  The committed predecessor
audit likewise reports `primary_imported: false` and
`symbolic_library_used: false`.

## 7. Accepted boundary

```text
fixed equality-five pair:                              ASSUMED;
exactly two distinct noncommon lows, one per family:    ASSUMED;
other two modes high for both families:                 ASSUMED;
zero high-high pairing branch:                          EXCLUDED;
nonzero E_22 high-high branch:                          OPEN;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```

## Final reviewed hashes

```text
new theorem:
236065BB239059865C91105D49590693E5D9121DD1A0BBB365863A7667FCF0CA

new primary verifier:
85504804E6BF5A056C53E6E8FDD93B999AB56A0C2E63187E24C590840C58600D

new independent audit:
7CB12A912E30C6A44AAC784CE6786E822106BA7A59E3EB396BE9DB33244CEDF6

distinct-two-low predecessor theorem:
87BD9CCC45C07088465C27FB4032BCC34DDB7004789A3FC28ECA36F3BFA67D1E

distinct-two-low predecessor primary verifier:
20ECAA638C7AFDFB11187925C76AA6DD9F142E63AE41AD5220F27FA70518290A

distinct-two-low predecessor independent audit:
F8A1350BD36DA6CFCEBCA674791F44B6DBCF00BD782F53B6319E609005658D56
```
