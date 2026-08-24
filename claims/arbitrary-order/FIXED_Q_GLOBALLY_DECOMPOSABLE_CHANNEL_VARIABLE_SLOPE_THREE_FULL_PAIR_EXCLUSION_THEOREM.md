# Fixed-Q globally decomposable channel variable-slope three-full-pair exclusion

## Status

**Exact characteristic-zero response exclusion and conditional fixed-module
detector.**  `GLD18` proves an all-slope exclusion for a globally decomposable
physical channel when all six pair rows have one common projective slope.  The
common-slope hypothesis is unnecessary.

On the physical `q=2`, `h=0` response window, normalize six independently
chosen `M`-active pair rows and one `M`-active four-port row as

```text
D_e=B_e+p_e K_e,
T=C(B)+t X(B,K).
```

Assume the channel factors through the ports,

```text
K_uv=a_u tensor a_v,
```

all six `D_e` are diagonal, and one complementary pair is three-full.  Then
at least one coefficient in a fixed set of forty-three mixed four-port words
is nonzero, for arbitrary and unrelated values of the six `p_e` and `t`.

Consequently, if the seven normalized rows are legal `GLD15` constant
operator rows on a hypothetical witness, this physical branch is impossible.
The theorem removes synchronization and every cancellation-divisor condition
inside the globally decomposable, `M`-active, three-full branch.  It does not
force legal operator supply, `M`-activity, global decomposability,
three-fullness, or arbitrary-root source coverage; it does not treat pure-`Z`
projective axes, general rank-two channels, or permanent restriction.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md),
- [`GLD18`](FIXED_Q_RESPONSE_VISIBLE_OPERATOR_SLOPE_AND_EDGE_DEPENDENT_CANCELLATION_DIVISOR_THEOREM.md).

## 1. Physical response and edge-dependent identity

Work over a characteristic-zero field `K`.  Let

```text
U={1,2,3,4},             E=binom(U,2).                 (1)
```

Fix one physical residual-pair response with `q=2` and `h=0`.  For every
edge `e={u,v}` let `B_e` be the direct pair block and let

```text
K_e=x_u tensor y_v+y_u tensor x_v.                    (2)
```

Choose arbitrary normalized finite slopes

```text
p_e in K       for e in E,          t in K,           (3)
```

and put

```text
D_e=B_e+p_e K_e,
T=C(B)+t X(B,K).                                      (4)
```

Here `C` and `X` are the complementary-matching compound and polarization
of `GLD18`.  For a complementary partition `e|f`, define

```text
gamma_(ef)=p_e p_f-t(p_e+p_f),
G=gamma_(12,34)+gamma_(13,24)+gamma_(14,23).          (5)
```

Substituting `B_e=D_e-p_eK_e` in (4) gives the exact `GLD18` identity

```text
T=sum_(e|f) [
    D_e D_f
   +(t-p_f)D_e K_f
   +(t-p_e)K_e D_f
   +gamma_(ef)K_e K_f
].                                                    (6)
```

No equality among the seven slopes is assumed.  Equations (3)--(6) are the
all-`M`-active affine chart.  They do not extend by declaration to a pure-`Z`
operator row.

Assume from now on that the physical channel is **globally decomposable**:

```text
K_uv=a_u tensor a_v             for u<v,              (7)
```

with the reversed block given by transpose.  This is a vertex factorization,
not six unrelated edgewise rank-one decompositions.  Write

```text
k_(uv)^c=a_u^c a_v^c,
A_w=product_(u in U) a_u^(w_u).                        (8)
```

For every word `w` and every complementary matching, its `K_eK_f`
coefficient is the same monomial `A_w`.  Hence all three quadratic
corrections in (6) combine to `G A_w`.

## 2. The forty-three-word detector

Assume every `D_e` is diagonal in the fixed ternary GHZ bases.  Fix one named
complementary partition

```text
e={i,j},                   f={r,s}=U-e,                (9)
```

and suppose it is **three-full**:

```text
D_e(c,c)D_f(c,c)!=0             for c=0,1,2.          (10)
```

The detector uses the following fixed mixed words:

1. the thirty-six `2+1+1` words obtained by choosing an edge `g`, repeating
   a colour `c` on `g`, and placing the other two colours in either order on
   `U-g`;
2. the six ordered `2+2` words that put colour `c` on `e` and colour `d` on
   `f`, for `c!=d`;
3. the single `3+1` word `(0,0,0,1)` in the port order `(1,2,3,4)`.

These three families are disjoint, so the ledger contains exactly
`36+6+1=43` mixed words.

### Theorem 1 (variable-slope decomposable-channel detector)

Under (1)--(10), at least one of the forty-three displayed mixed coefficients
of `T` is nonzero.

### Proof

Suppose all forty-three coefficients vanish.  Put

```text
d_g^c=D_g(c,c),
Z_g={c:k_g^c=0}.                                     (11)
```

First prove that the four port vectors in (7) have full ternary support.
For `c!=d`, the named `cc|dd` coefficient of (6) is

```text
d_e^c d_f^d
 +(t-p_f)d_e^c k_f^d
 +(t-p_e)k_e^c d_f^d
 +G k_e^c k_f^d=0.                                  (12)
```

If `c in Z_e` and `d in Z_f` were distinct, (12) would reduce to the nonzero
quantity `d_e^c d_f^d`, contradicting (10).  Thus no two distinct colours
can lie respectively in `Z_e` and `Z_f`.

Suppose `c in Z_e`, and let `a,b` be the other two colours.  The preceding
paragraph gives `Z_f subset {c}`.  Therefore both orientations of the
off-diagonal coefficient `K_f(a,b)` are nonzero.  The `2+1+1` word with
colour `c` repeated on `e` and colours `a,b` on `f` has coefficient

```text
(t-p_f)d_e^c K_f(a,b)=0,                              (13)
```

because every other term containing a `D` block is mixed and every
`K_gK_(U-g)` term contains `k_e^c=0`.  Conditions (10) and the nonzero
off-diagonal factor force `p_f=t`.  But then (12), with any `d!=c`, again
reduces to `d_e^c d_f^d!=0`.  Hence `Z_e` is empty.  The symmetric argument
makes `Z_f` empty.  Since `e|f` covers all four ports, every coordinate of
every `a_u` is nonzero.  In particular every coefficient of every `K_g` and
every monomial `A_w` is nonzero.

Now take any edge `g`, repeat colour `c` on it, and place the other two
colours `a,b` on its complementary edge `bar g`.  Diagonality kills every
`D` term except `D_g(c,c)K_(bar g)(a,b)`.  Equation (6) therefore gives

```text
K_(bar g)(a,b)
 [(t-p_(bar g))d_g^c+G k_g^c]=0.                    (14)
```

Full support makes the prefactor nonzero, so for every `g,c`,

```text
(t-p_(bar g))d_g^c+G k_g^c=0.                        (15)
```

Evaluate the displayed `3+1` word.  In each of its three complementary
matchings, exactly one edge `g` joins two zero-coloured ports and the other
edge is mixed.  The corresponding linear term in (6), together with (15),
is `-G A_w`.  The three linear terms sum to `-3G A_w`, while all quadratic
terms sum to `G A_w`.  Thus

```text
T(0,0,0,1)=-2G A_(0,0,0,1)=0.                       (16)
```

Characteristic zero and full support imply `G=0`.  Apply (15) first to
`g=e` and then to `g=f`.  Three-fullness gives

```text
p_f=t,                      p_e=t.                    (17)
```

Finally, use the named `2+2` word with colour zero on `e` and colour one on
`f`.  Equations (12), (16), and (17) reduce its coefficient to

```text
d_e^0 d_f^1!=0,                                       (18)
```

the final contradiction.  `square`

The proof does not divide by a slope, a cancellation polynomial, a response
coefficient, or a channel minor.  It retains all finite-slope coincidences,
including `p_g=t`, and both `G=0` and `G!=0` until they are decided by mixed
target coefficients.  Characteristic two is excluded exactly at (16).

## 3. Conditional fixed-module witness consequence

Return to one fixed graph, residual pair `Q`, fully specified contraction,
four-port window, GHZ bases, and complete `GLD15` nuisance module.  Suppose:

1. for every pair `e subset U`, its exact joint operator space contains the
   normalized row `(1,p_e)`;
2. the four-port operator space contains `(1,t)`;
3. the resulting physical channel satisfies the one-port factorization (7);
4. one complementary selected pair satisfies (10).

The seven selector functionals and the seven slopes may differ.  The graph,
`Q`, contraction, bases, `M/Z` coefficient axes, and physical response may
not.

### Corollary 2 (conditional witness exclusion)

No hypothetical Krenn--Gu witness satisfies conditions 1--4.

### Proof

Apply the seven constant operator identities to the complete mixed GHZ
equation.  Every selected `D_e` and `T` is target-diagonal in the same fixed
port bases.  Theorem 1 produces a mixed coefficient of `T`, contradicting
the pure GHZ target.  `square`

This corollary does not infer any operator row from an observed response.
Legality remains the complete joint-nuisance condition of `GLD15`.

## 4. Exact frontier and scope ledger

```text
edge-dependent response identity (6):                    INHERITED/REPLAYED;
global K matching-independence A_w:                      PROVED;
zero-support elimination from 2+1+1 and 2+2 words:       PROVED;
full-support scalar relation (15):                       PROVED;
3+1 elimination of the aggregate correction G:          PROVED;
arbitrary finite pair slopes on decomposable channel:    EXCLUDED;
conditional legal fixed-module witness branch:           EXCLUDED;
common pair slope required in this physical class:       FALSE;
M-active legal rows forced on every witness:             UNKNOWN;
globally decomposable channel forced on every witness:    UNKNOWN;
one three-full complementary pair forced:                UNKNOWN;
pure-Z projective axes:                                  UNKNOWN;
general rank-two/nondecomposable physical channel:        UNKNOWN;
arbitrary-root source coverage and promoted attachment:   UNKNOWN;
weighted permanent implication:                          UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

The breadth is one fixed four-port window, all six pair targets, one graph,
one `Q`, and one contraction.  The response depth is pair and four-port.  The
module implication is conditional on seven already legal `GLD15` rows.  The
reconstructed object is the variable-slope selected package `(D_e,T)`.  The
remaining ambiguity is the zero-space, pure-`Z`, nondecomposable,
support-drop, and source-coverage complement.  No permanent consequence is
claimed.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_globally_decomposable_channel_variable_slope_three_full_pair_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_globally_decomposable_channel_variable_slope_three_full_pair_exclusion.py
```

The primary exact SymPy replay constructs the globally decomposable channel,
enumerates all forty-three words, checks (12)--(16) symbolically, and audits
the zero-support and divisor substitutions.  The independent no-import audit
uses a separate sparse-polynomial implementation, constructs `T` directly
from `B=D-pK`, enumerates endpoint-support patterns, and verifies the same
syzygies without importing the primary or `GLD18` replay.  These scripts
audit the bounded identities and finite word ledger.  The arbitrary-field
support implication and legal full-module attachment remain load-bearing.
