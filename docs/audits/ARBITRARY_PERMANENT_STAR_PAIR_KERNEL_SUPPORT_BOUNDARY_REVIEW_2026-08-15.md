# Hostile review of the star-pair kernel-support boundary theorem

## Verdict and exact scope

**PASS, for the displayed based `(4,1)` star frame, pointwise,
characteristic-zero, full-`Delta_3` scope.**  No mathematical, quantifier,
slot, characteristic, dependency, or implementation blocker survived hostile
review.

For every local mode of this explicit star pair, the reviewed package proves

```text
rank(Phi_1|L_t) >= 2,             rank(Phi_2|L_t) >= 2.
```

More precisely, every nonzero local kernel vector lies on one of the
following family-labelled ambient lines:

```text
Phi_1: K(x_1+x_2), K(x_0+x_2), K(x_0-x_1),
Phi_2: K(x_1+x_2), K(x_0+x_3), K(x_0+x_1+x_2+x_3).
```

Together with the already reviewed two-sided projection-drop predecessor,
this makes the minimum local rank in each family exactly two.  This is a
necessary localization only.  The exceptional-line incidence problem
remains open, and no displayed incidence is asserted to be realizable.  The
result does not automatically transport to another based representative of
the unbased `(4,1)` orbit or to either inequivalent admissible equality-five
orbit.  Unrestricted `P_6 -> Delta_3` nonrestriction is unknown, and the
global Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_STAR_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
  verify_arbitrary_permanent_star_pair_kernel_support_boundary.py
  audit_arbitrary_permanent_star_pair_kernel_support_boundary.py
```

Load-bearing predecessor:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_STAR_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md
```

The `r=4` pair-orbit classification was also replayed as provenance for the
displayed Delta-admissible star frame.  It is not used to transport the new
pointwise theorem between based frames.

## 1. Star frame, kernels, and determinant pencils

Independent square-free multiplication reproduces the nine pair products,
their five-dimensional span, and the two-dimensional mixed span.  Edge
complementation gives the displayed quartics

```text
star(m_1)=x_4x_5 x_3(x_0+x_1-x_2),
star(m_2)=x_4x_5 (x_0-x_3)(x_1-x_2),

star(d_0)=x_4x_5(
  x_0x_1+x_0x_3-x_1x_2+2x_1x_3-x_2x_3),
star(d_1)=-x_4x_5 x_2(x_0+x_1-x_3),
star(d_2)=2x_4x_5x_0x_3.
```

Solving the four defining equations of each projection directly gives

```text
ker(Phi_1)={(a,b,a+b,0,0,0)},
ker(Phi_2)={(a,b,b,a,0,0)}.
```

After suppressing the common factor `x_4x_5`, direct polarization gives the
ten single contractions in the theorem.  For `Phi_1`, the four residual
columns `(m_2,d_0,d_1,d_2)` have determinant

```text
8a^2 b(a+b).
```

For `Phi_2`, the columns `(m_1,d_0,d_1,d_2)` have determinant

```text
-8a^2 b(a-b).
```

Thus the exceptional projective directions are exactly

```text
Phi_1: a=0, b=0, a+b=0,
Phi_2: a=0, b=0, a=b.
```

There is no hidden algebraic closure, projective normalization, or omitted
root in this step.  Away from those directions the applicable mixed
residual and three diagonal residuals form a basis of the full
first-four-coordinate covector space.

## 2. Generic residual tensor and cross-orthogonality

Write the ambient space as

```text
R direct-sum A,
R=K^{0,1,2,3}, A=K^{4,5},
J((s_4,s_5),(t_4,t_5))=s_4t_5+s_5t_4.
```

After contracting a generic kernel vector in one local slot, the
polarization of each residual quartic `x_4x_5 h` is evaluation by `h` of

```text
C(y,z,w)=r(y)J(a(z),a(w))
        +r(z)J(a(y),a(w))
        +r(w)J(a(y),a(z)).
```

Because the four residual covectors are a basis, the full exact target
equations determine a vector identity in `R` on the three remaining ordered
colour bases:

```text
C(y_(s,i),y_(u,j),y_(v,l))=0 unless i=j=l,
C(y_(s,e),y_(u,e),y_(v,e))!=0 iff alpha_e!=0.
```

This is stronger than a scalar sensor observation and uses all entries of
the tensor-wide mixed zeros and diagonal targets.

For distinct colours `i!=j`, the map

```text
w |-> C(y_(s,i),y_(u,j),w)
```

kills the independent three-space `L_v`, so its rank is at most three.  On
the four-dimensional `R` summand it is scalar multiplication by

```text
J(a(y_(s,i)),a(y_(u,j))).
```

A nonzero scalar would have rank at least four.  Hence every different-colour
pair in different modes is `J`-orthogonal.

The resulting two-dimensional case split is exhaustive.  If each mode's
`A`-image has dimension at most one, an active colour forces both endpoint
modes to support only that colour, and a second active pair among three modes
cannot use another colour.  If one mode has two independent columns of
colours `e,f`, all third-colour columns in the other modes vanish.  When both
`e,f` are active, nonzero outside columns lie on the two distinct orthogonal-
complement lines, and they force the first mode's third-colour column to
vanish as well.  Therefore at most two colours are active, and in the
two-active case every column at the remaining colour is zero.

The proof uses only the safe implication

```text
alpha_e!=0  =>  colour e is active.
```

A nonzero diagonal value of `C` must contain a nonzero same-colour `J`
pairing.  The converse could fail by cancellation and is not used.

## 3. The two-support and one-support obstructions

If the removed kernel vector had support on exactly two local colours, those
would be the two active colours.  Every `A`-part at the third colour would
vanish in all three remaining modes.  In the original four-mode pure
coefficient at that third colour, the distinct factors `x_4,x_5` must be
supplied by distinct slots.  Only the removed mode's third-colour basis
vector could have a nonzero `A`-part, so the coefficient is zero, contrary
to its nonzero diagonal target.  This is slot-correct: the argument does not
mistake the removed kernel vector for the removed mode's third-colour basis
vector.

Thus a generic kernel vector would have singleton local support.  The final
obstruction is also exact.  More generally let `W=D direct-sum A`, with
`dim D=d>=2`, and suppose three independent local triples have only one
surviving diagonal value of the analogous `D`-valued tensor `C`.

For any colour pair other than the surviving pair, the corresponding map
`W -> D` kills an independent three-space.  Its rank is at most

```text
dim W-3=d-1,
```

whereas a nonzero `J` scalar on the `D` summand would have rank `d`.
Therefore every such pairing vanishes.  A nonzero surviving diagonal value
supplies a nonzero same-colour pairing between two modes.  In the third
mode, both off-colour vectors then have zero `D`-part and lie in the same
one-dimensional orthogonal complement in `A`.  They are dependent,
contradicting independence of that local triple.

Taking `D=R` excludes every generic direction in both kernel pencils.  This
argument is field-linear and uses no positivity, roots, or closure.

## 4. Exceptional lines and the delicate `Phi_2` identity

On five of the six family-labelled exceptional directions, one diagonal
residual vanishes and the corresponding nonzero pure target forces the
listed local coefficient to vanish:

```text
common N=x_1+x_2:                  alpha_2=0,
Phi_1 B_0=x_0+x_2:                 alpha_0=0,
Phi_1 C_0=x_0-x_1:                 alpha_1=0,
Phi_2 B_1=x_0+x_3:                 alpha_1=0.
```

The remaining `Phi_2` line is not treated by pretending that another
diagonal channel vanishes.  At `a=b!=0`, direct contraction gives the exact
ambient tensor identity

```text
i_(p_2(a,a)) star(d_0)=2 i_(p_2(a,a)) star(m_1).
```

The entire mixed target `T_(m_1)` is zero, so the contracted `d_0` target is
zero.  Since `lambda_0!=0`, this forces `alpha_0=0` on

```text
K(x_0+x_1+x_2+x_3).
```

No division by a target coefficient other than its stated nonvanishing is
hidden here, and the identity is applied in the same removed slot on both
sides.

Hence every nonzero local kernel vector lies on one of the three ambient
lines for its family and misses the claimed colour.  The theorem correctly
does not strengthen these missing-colour statements to singleton support or
claim realizability.

## 5. Finite-union rank floor and predecessor dependence

For fixed `k,t`, put

```text
S=L_t intersect ker(Phi_k).
```

The generic exclusion places every nonzero element of `S` in a union of
three ambient lines.  A characteristic-zero field is infinite, and a
vector space over an infinite field cannot be a finite union of proper
linear subspaces.  Therefore `dim S<=1`.  Rank-nullity on the
three-dimensional `L_t` gives

```text
rank(Phi_k|L_t)>=2.
```

The two-sided predecessor is used only for the complementary upper bound:
each projection family has at least one mode of rank at most two.  Combining
the bounds gives

```text
min_t rank(Phi_1|L_t)=min_t rank(Phi_2|L_t)=2.
```

The predecessor does not say that the minimizing modes coincide, and the
new theorem does not infer that they do.

## 6. Characteristic, quantifier, and transport boundaries

Characteristic zero is correctly stated.  It makes the determinant factors
`8` and `-8` nonzero, keeps `J` nondegenerate, and supplies the infinite-field
finite-union argument.  The odd finite-field enumerations are checks of the
identities and case split only; they are not proofs of the characteristic-
zero theorem.

Every conclusion is pointwise for the displayed ordered star frame and four
independent local triples satisfying the complete exact target equations.
The proof uses tensor-wide mixed zeros, all three nonzero diagonal tensors,
and contractions in the same fixed slot.  It is not a Hamming-shell result,
not a generic-orbit statement, not a converse, and not a normalization
theorem.

Accepted boundary:

```text
displayed star pair, every local Phi_k rank at least two: PROVED;
kernel vectors localized to three lines per family:      PROVED NECESSARY;
one rank-two mode in each family:                         PROVED NECESSARY;
exceptional-line incidence classification/exclusion:     OPEN;
other based frames in the unbased (4,1) orbit:            NOT TREATED;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

## 7. Computational replay and independence

The primary verifier reconstructs the pair table, both kernel pencils, all
ten square-free single contractions, both determinants, the exceptional
`Phi_2` identity, the `R direct-sum A` factorization, and the rank gaps.  It
also exhausts the two-dimensional active-colour lemma over `F_3` and `F_5`.

The no-import audit imports neither the primary verifier nor SymPy.  It
rebuilds the complementary cores, contracts them with a separate integer
matrix implementation, computes both bivariate determinants by a standalone
Leibniz expansion, and independently exhausts the active-colour lemma.  Its
finite-field counts agree with the primary implementation:

```text
F_3 compatible triples: 3207; two-active triples: 186,
F_5 compatible triples: 6579; two-active triples: 426.
```

The written rank argument, rather than these finite enumerations, proves the
one-surviving-diagonal obstruction.  The independently reviewed star
two-sided predecessor and the pair-orbit provenance package were replayed
without modification.

Focused final replay passed:

```text
new primary exact verifier:                    PASS;
new independent no-import audit:              PASS;
star two-sided predecessor primary/audit:     PASS/PASS;
r=4 pair-orbit provenance primary/audit:      PASS/PASS;
py_compile on all replayed scripts:           PASS;
Ruff on all replayed scripts:                 PASS;
git diff --check on tracked changes:          PASS.
```

## Final reviewed hashes

```text
new theorem:
2B44641806EEE9B14D2F9DCC692C2E8E1CB9917832A9C2FD9E658243ACFE51F5

new primary verifier:
73406FF9C62A2113341BBC97E36E2E4F4151CF399E72EEBFD831A05944744124

new independent audit:
0D4F649C78577158E39577FB5CBDDA1A0057534E75A803F1EB73F25726DA5721

star two-sided theorem:
76AEBB661CA3E89DF3E4228954B0D7CB3D736414A4AB22C2EBC9A2C84A774D62

star two-sided primary verifier:
223B61126635FE59987B75684CFA6FCA1173737913CEAD0F46D98AA3A8C3DF1B

star two-sided independent audit:
CD4D833DB7CB132FCFED02A0BD2353799E184DAC3DFAC9EC5F714F998F614311

r=4 pair-orbit theorem:
4B7FCCCCF68B55E1DDEACB7328B7469A8A82F36AA2AB0303E9094519A95FC5BC

r=4 pair-orbit primary verifier:
C99410B5D01F6BFB71B7C8F07859A83376BBF38A935B6F5313E4983A6BECFF07

r=4 pair-orbit independent audit:
62F1D4EDEBDAEE01D9F61DD43E705568DC18188A39EBFEE4A2FE971572961E03
```
