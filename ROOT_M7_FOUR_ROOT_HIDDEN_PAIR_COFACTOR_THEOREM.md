# Root `m=7` four-root hidden-pair cofactor theorem

## Status

This is an exact characteristic-zero lower-jet theorem in the uniform-axis
five-root/two-residual cell.  It turns the four-root derivative into a
named relation between the two previously hidden intermediate cofactors.
On a rank-two scalar-form chart, both cofactors are individually forced
into the binary diagonal blocker plane; on the rank-one chart, one exact
linear combination is forced there.

Compatibility with the all-root derivative also proves that at least two
distinct internal four-root hafnian sectors are active.  This is the first
nontrivial cross-deletion-depth constraint beyond the earlier span theorem.
It does not prove that one of the five hidden pairs has rank two, so the
arbitrary `P_7` system and the global Krenn--Gu conjecture remain unknown.

## Setup

Let

```text
R={r_0,...,r_4}, Q={q_0,q_1},
S_i=ker e_2^*,
D_01=span{D_0,D_1}, D_c=e_c^(tensor 7).                (1)
```

Write `C_D=H_(V-D)` for the complementary blocker cofactor after the fixed
contractions.  Assume throughout the projectively constant root--blocker
derivative hypothesis

```text
B_(r_i,u)(y,-)=0 for every blocker u and every y in S_i.
```

This vanishing removes blocker companion classes from the deletion ledgers
below; merely defining `S_i` would not suffice.  Normalize the two surviving
GHZ colour coefficients to one.  Keeping arbitrary nonzero scalars
`lambda_0,lambda_1` changes none of the span, rank, gcd, or ideal
conclusions.

On each binary tangent plane put

```text
x_i=e_0^* restricted to S_i,
y_i=e_1^* restricted to S_i,
X=product_i x_i, Y=product_i y_i.                     (2)
```

The two forms `X,Y` are independent and coprime.

## The all-root frame fixes the top cofactor plane

When all five roots vary, parity leaves exactly the two companion classes
`A={q_0}` and `A={q_1}`.  Hence

```text
g_0 tensor C_(R union {q_0})
+g_1 tensor C_(R union {q_1})
 =X tensor D_0+Y tensor D_1.                          (3)
```

The right flattening has rank two, so `g_0,g_1` are independent.  Quotient
the blocker tensor space by `D_01`.  Equation (3) becomes a sum of two
independent scalar forms tensored with the two quotient classes, forcing

```text
C_(R union {q_0}), C_(R union {q_1}) in D_01.          (4)
```

They form a basis of `D_01`, since the blocker-side rank in (3) is also two.
Consequently

```text
span{g_0,g_1}=span{X,Y}.                              (5)
```

## Four-root hidden-pair equation

Fix `k` and let `I=R-{r_k}`.  The only parity-legal companion sets among
the fixed vertices `{r_k,q_0,q_1}` are

```text
empty, Q, {r_k,q_0}, {r_k,q_1}.                       (6)
```

Write their scalar four-root forms as

```text
h_k, q_k, p_(k0), p_(k1),
```

respectively.  The exact derivative identity is

```text
h_k tensor C_I
+q_k tensor C_(I union Q)
+p_(k0) tensor C_(R union {q_0})
+p_(k1) tensor C_(R union {q_1})
 =X_I tensor D_0+Y_I tensor D_1.                      (7)
```

After quotienting by `D_01`, the top and target terms vanish:

```text
h_k tensor bar(C_I)+q_k tensor bar(C_(I union Q))=0.   (8)
```

This yields the complete rank trichotomy.

1. If `h_k,q_k` are independent, then

   ```text
   C_I,C_(I union Q) in D_01                          (9)
   ```

   individually.  Every mixed blocker coefficient of both named cofactors
   is zero.
2. If `q_k=mu_k h_k !=0`, then

   ```text
   C_I+mu_k C_(I union Q) in D_01.                    (10)
   ```

3. If exactly one form is nonzero, its cofactor lies in `D_01`.  If both
   vanish, this derivative sees neither cofactor.

For any named mixed word `w`, including `0000102`, (8) gives the scalar-form
identity

```text
[w]C_I h_k+[w]C_(I union Q) q_k=0.                    (11)
```

Thus rank two kills the two coefficients separately, while rank one gives
their exact proportional cancellation.

There is also an exact-value refinement.  If `h_k` is exposed relative to
`span{q_k,p_(k0),p_(k1)}`, choose a dual functional `L` that is one on
`h_k` and zero on the other three forms.  Applying `L` to (7) gives

```text
C_I=L(X_I)D_0+L(Y_I)D_1.                              (12)
```

The analogous assertion holds for the two-endpoint cofactor.

## At least two internal sectors are active

Expand the all-root forms by the root paired to the endpoint:

```text
g_t=sum_(k=0)^4 L_(kt) h_k,                           (13)
```

where `L_(kt) in S_k^*` is the tangent root-to-`q_t` edge form.  Let

```text
K_act={k:h_k !=0 and (L_(k0),L_(k1)) !=(0,0)},
J=(h_k:k in K_act).                                   (14)
```

By (5), an invertible constant change of basis in (13) expresses both
`X` and `Y` as elements of `J`.  Therefore

```text
V(J) subset V(X,Y),
J:X^infinity=J:Y^infinity=(1),
gcd{h_k:k in K_act}=1.                                (15)
```

In particular

```text
|K_act|>=2.                                           (16)
```

If there were only one active `h_k`, it would divide both coprime monomials
`X,Y`.  The count two is sharp for the expansion identity alone: formally,

```text
h_0=product_(i!=0)x_i, L_(00)=x_0,
h_1=y_0 product_(i=2)^4 y_i, L_(11)=y_1
```

gives `g_0=X,g_1=Y`.  This formal sharpness model need not come from common
root-edge hafnians; excluding it requires a stronger simultaneous
realizability theorem.

## Verification

Run:

```text
uv run --with sympy python verify_root_m7_four_root_hidden_pair_cofactor_theorem.py
python audit_root_m7_four_root_hidden_pair_cofactor_theorem.py
```

The scripts check the deletion parity ledger, the rank-two/rank-one quotient
relations, the two-active gcd argument, and the formal sharpness model.
They are symbolic sanity checks of the displayed linear algebra.  Equations
(3)--(16) are the proof.

## Boundary

```text
top two cofactors:                         BINARY DIAGONAL BASIS;
five four-root hidden pairs:              EXACT EQUATIONS;
rank-two hidden pair:                     BOTH COFACTORS DIAGONAL;
rank-one hidden pair:                     ONE COMBINATION DIAGONAL;
active internal four-root sectors:        AT LEAST TWO;
existence of a rank-two hidden pair:       UNKNOWN;
common root-edge realization obstruction: UNKNOWN;
global Krenn-Gu conjecture:                UNRESOLVED.
```
