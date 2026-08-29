# Hostile review: six-deficient binary-triangle parent taxonomy, proper-face deck kernel, and pair-class exclusion

## Verdict

**PASS, with corrected scope.**  The `GLS70` theorem is accepted as an exact
characteristic-zero same-source localization and exclusion of the sole
six-deficient binary pair-class key.

The accepted conclusions are:

- the `3,360` profiles having exactly one binary triangle split into exactly
  two structural families and eight type-profile keys;
- their first target-bearing same-source parents are as stated;
- the other `45` binary-triangle profiles are exactly the one
  `S_c^2 T_c^4` key;
- its binary pair equation has the forced crossed separated normalization;
- the proper-face restriction map of its complementary four-port deck has
  a sixteen-dimensional ambient kernel, with an explicit physical hafnian
  direction;
- proper-face non-identifiability does not save the key: the pure four-open
  equation forces a transverse old-probe coefficient at some outside port,
  and that port's binary triangle gives an exact contradiction; and
- the six-deficient residual is therefore `99,135` profiles in `85` keys.

This does not close the other `99,135` profiles, either five-deficient
branch, another deficient-count branch, the unique-nonrigid branch, a
downstream attachment gate, or the global conjecture.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## Artifacts reviewed

- [`GLS70` theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_BINARY_TRIANGLE_PARENT_TAXONOMY_AND_PROPER_FACE_DECK_KERNEL_THEOREM.md)
- [primary verifier](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_binary_triangle_parent_taxonomy_and_proper_face_deck_kernel.py)
- [independent audit](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_binary_triangle_parent_taxonomy_and_proper_face_deck_kernel.py)
- [`GLS69` parent](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FIVE_SIX_DEFICIENT_OPEN_SET_SUPPORT_TOWER_AND_OVERLAP_INTEGRABILITY_BOUNDARY_THEOREM.md)
- [`GLS63` hierarchy owner](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_MIXED_KERNEL_PARTIAL_UNCONTRACTION_AND_TWO_DEFICIENT_BINARY_LOCALIZATION_THEOREM.md)

## 1. Independent finite replay

The primary object/set implementation and independent integer-mask
implementation separately reproduce

```text
531,441 -> 276,750 -> 99,855 -> 99,180,
```

with `86` post-span keys.  Both find binary-triangle multiplicities

```text
one binary triangle:   3,360 profiles / 8 keys;
four binary triangles:    45 profiles / 1 key.
```

For the one-triangle stratum, both implementations recover only:

```text
Family A: S_0 R_2 R_1 R_0^(3-r) T_0^r,
          counts 360, 1,080, 1,080, 360;

Family B: S_0^3 R_0^(3-r) T_0^r,
          counts 60, 180, 180, 60.
```

The missing-set reconstruction separately verifies the two-pair versus
two-exact-triple alternatives.  No pair-plus-exact-triple profile occurs.
This absence is an exhaustive finite consequence, not a silently asserted
general support lemma.

Deleting the four-triangle key independently gives

```text
99,180 / 86 -> 99,135 / 85.
```

## 2. Pair normalization audit

The first draft's appeal to four-factor CP uniqueness was insufficient:
before normalization, a map such as `p_s` is a two-factor tensor between an
old-probe space and a local output space and need not itself be decomposable.
The accepted proof instead expands the four local `a,b` output coordinates.

Writing the eight scalar old-probe forms as `A,B,C,D,E,F,G,H`, the two
diagonal and two off-diagonal equations are

```text
A tensor G+E tensor C=alpha P_a tensor Q_a,
A tensor H+F tensor C=0,
B tensor G+E tensor D=0,
B tensor H+F tensor D=beta P_b tensor Q_b.
```

If all eight forms were nonzero, the two zero equations would pair their
factors proportionally.  The diagonal equations would then be two invertible
linear combinations of `A tensor D` and `B tensor C`.  Their span would equal
the plane spanned by `P_a tensor Q_a` and `P_b tensor Q_b`.  The only
decomposable lines in that plane are its generators, but both combinations
would have two nonzero coefficients.  This is impossible.

The endpoint, colour, and old-probe symmetries are transitive on the eight
forms.  Setting one representative form to zero makes the opposite diagonal
product rank one and nonzero; the adjacent zero equation kills one more
form, the other diagonal does the same, and the last zero equation separates
the independent `P_a,P_b` forms.  This gives the crossed normalization
uniquely up to the stated symmetries and scalings.

In particular, after naming the target colours `a,b`, one may write

```text
p_s proportional to z_(0,a)e_(s,a)^*,
q_s proportional to z_(1,b)e_(s,b)^*,
p_t proportional to z_(0,b)e_(t,b)^*,
q_t proportional to z_(1,a)e_(t,a)^*.
```

Thus both endpoint `p` maps have zero `z_(0,c)` coefficient and the two
endpoint `q` maps use independent scalar forms `z_(1,a),z_(1,b)`.  This is
stronger and cleaner than merely saying the `q` maps do not share a common
form.

## 3. Pure four-open coefficient audit

Contracting `s,t` at their fixed kernel lines leaves the exact open set
`U`.  Its right side is a nonzero pure-`c` tensor with probe monomial
`z_(0,c)z_(1,c)`.  Every complementary tensor on the left is a physical
edge/deck evaluation independent of the two old-probe variables.  Therefore
if every outside `p_u` had zero `z_(0,c)` coefficient, the entire left side
would have zero `z_(0,c)` coefficient.  This contradicts the right side.

The accepted inference is precisely:

```text
there exists u in U with [z_(0,c)]p_u != 0.
```

It is not an assertion that the local `c` coordinate of `p_u` is nonzero;
the coefficient is a possibly non-coordinate covector in `V_u^*`.

The review rejects calling this general equation a separated `P_4`
restriction.  Its effective deck contains

```text
eta W_uv+a_u tensor b_v+b_u tensor a_v,
```

and the `eta W_uv` term need not factor through two fixed source rows.
`GLS70` uses only old-probe independence, so no `eta=0` hypothesis is
needed.

## 4. Triangle coefficient audit

Choose the outside port supplied by Section 3.  In its synchronized binary
triangle, the `z_(0,c)` coefficient of the pair term is zero by the pair
normalization.  The other two terms share the same nonzero local factor
`[z_(0,c)]p_u`.  Cancelling that vector gives

```text
q_s(z_1) tensor d_t+d_s tensor q_t(z_1)=0.
```

Taking the independent `z_(1,b)` and `z_(1,a)` coefficients forces
`d_t=d_s=0`.  The primary and independent programs separately encode this
as a `27 x 6` exact coefficient matrix and find rank six (over `Q` and
`F_101`, respectively).

The remaining pair term is `g_st tensor d_u`.  Its two probe monomials force
the one fixed deck `d_u` to lie simultaneously on the independent coordinate
lines `F e_(u,a)^*` and `F e_(u,b)^*`, with a nonzero coefficient on each.
This is impossible.  No relationship between independently chosen decks is
assumed: all three decks are actual restrictions, and allowing them to be
arbitrary fixed covectors only weakens the hypotheses.

## 5. Proper-face kernel and sharp scope

For `v_u=e_a+lambda_u e_b`, the annihilator is the two-plane

```text
A_u=Ann(v_u)=row J_u.
```

The common kernel of the four one-slot evaluations is exactly
`tensor_u A_u`, of dimension `2^4=16`.  Since those evaluations are included
in the complete proper-face map, adding multiple-slot evaluations does not
shrink the kernel.  The direct-sum proof in the theorem is exact over the
common characteristic-zero field.  Separate rational and modular row
reductions give ambient rank `65` and nullity `16`.

The physical control correctly uses a separate slope `lambda_u` at every
port:

```text
R=tensor_u(e_(u,b)^*-lambda_u e_(u,a)^*).
```

Three nonzero matching products realize

```text
H_U=e_a^tensor4+kappa R.
```

The free direction vanishes under every proper restriction of this one
four-port deck.  The review rejects two stronger readings:

1. the four kernel slopes have not been proved equal; and
2. invisibility in the complementary `H_U` proper-face tower is not
   invisibility in the entire six-label source hierarchy, because changing
   a physical `U`-edge can affect other complementary decks.

The exclusion in Section 4 is compatible with this sharpness result: it
uses a different source term in the pure four-open equation, not another
proper-face reconstruction of `H_U`.

## 6. Residual-formula corrections

The hostile derivation caught and repaired two tempting overstatements.

- If `d_u=h tau e_(u,a)^*+r_u`, the unquotiented triangle residual includes
  `g_st tensor r_u`; the other two source terms do not alone equal the
  displayed target-row residual.
- A two-port deck is not the product of its one-port remainders.  Its
  unquotiented remainder is an arbitrary member of
  `row J_u tensor V_v^*+V_u^* tensor row J_v`.

Equations (19) and (22) in the accepted theorem retain these terms.  Their
quotients are tautological pair faces; they are not independent equations.

## 7. Replays

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_binary_triangle_parent_taxonomy_and_proper_face_deck_kernel.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_binary_triangle_parent_taxonomy_and_proper_face_deck_kernel.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_binary_triangle_parent_taxonomy_and_proper_face_deck_kernel.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_binary_triangle_parent_taxonomy_and_proper_face_deck_kernel.py
```

At review time both exact programs pass.  The finite-field calculations
audit integer/rank identities only; the written proof owns the
characteristic-zero theorem and the same-source semantics.

## Final scope

`GLS70` is a genuine top-down branch closure: it uses a larger pure
four-open parent to force a coefficient and descends to one smaller binary
triangle.  It removes one complete type-profile key, not the six-deficient
parent, root-order-three all-rigid branch, maximum-root node, or conjecture.
The next load-bearing work is the distinct Family A/Family B common-source
integrability problem, not another quotient of the excluded pair class.
