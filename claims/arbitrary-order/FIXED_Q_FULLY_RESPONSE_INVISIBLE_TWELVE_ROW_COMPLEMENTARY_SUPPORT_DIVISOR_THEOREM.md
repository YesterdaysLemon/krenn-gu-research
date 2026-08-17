# Fixed-Q response-map-zero support classification and five-row detector

## Status

**Exact characteristic-zero response-support classification and conditional
fixed-module witness boundary.**  `GLD18` proves that every legal joint
`M/Z` operator space lies in the kernel of the realized mixed-response map

```text
R_S(a,b)=[aM_S+bZ_S] modulo the pure GHZ output space.  (1)
```

This theorem classifies the strongest response-map-zero stratum, where `R_S=0` for
all six pair targets and the four-port target.  On one complementary
partition, six ordered mixed colour words in each of `M_U` and `Z_U` give
twelve scalar rows.  Their simultaneous vanishing has an exhaustive support
classification.  A fixed subset of only five scalar rows already detects any
three-full complementary pair.  On the full twelve-row zero locus, one
three-full selected edge forces the opposite raw pair response to vanish.
The conclusions are independent of hidden operator slopes, common-line or
quadratic-cancellation equations, and `M`-active normalization.

The theorem does **not** prove that `R_S=0` on every hypothetical witness,
force any operator space or selector, exclude the resulting support-divisor
locus, integrate a response control into a full witness, or imply a permanent
restriction.  A selected pure response is not the same as `R_S=0`.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md)
- [`GLD18`](FIXED_Q_RESPONSE_VISIBLE_OPERATOR_SLOPE_AND_EDGE_DEPENDENT_CANCELLATION_DIVISOR_THEOREM.md)

## 1. Physical response conventions

Work over a characteristic-zero field `K`.  Fix one physical `q=2`
response, one graph, residual pair `Q`, fully supported contraction, ternary
GHZ basis, and four-port set

```text
U={1,2,3,4}.                                           (2)
```

Let `h in K` be the residual scalar.  For each pair `e={u,v}`, write

```text
M_e=B_e,
Z_e=hB_e+K_e,
K_e=x_u tensor y_v+y_u tensor x_v,    rank K_e<=2.    (3)
```

For a six-tuple `Y` of pair blocks, put

```text
C(Y)=sum_(e|f) Y_e Y_f,
X(B,K)=sum_(e|f)(B_e K_f+K_e B_f),                    (4)
```

where the sums run over the three complementary matchings of `U`.  The
four-port layers are

```text
M_U=C(B),
Z_U=hC(B)+X(B,K).                                     (5)
```

If `R_e=0`, then both columns in (3) are diagonal in the fixed GHZ basis;
hence `B_e` and `K_e` are diagonal separately.  If `R_U=0`, then both tensors
in (5) are pure, and therefore `C(B)` and `X(B,K)` are pure separately.

Fix a complementary partition `e|f`.  Write

```text
B_e=diag(b_e^0,b_e^1,b_e^2),
K_e=diag(k_e^0,k_e^1,k_e^2),                          (6)
```

and similarly for `f`.  For ordered colours `c!=d`, let `cc|dd` denote the
word that has colour `c` at the endpoints of `e` and colour `d` at the
endpoints of `f`.

Pair diagonality kills the two other complementary matchings on this word,
so its two actual response coefficients are

```text
m_(ef)^(c,d):=M_U(cc|dd)=b_e^c b_f^d,
z_(ef)^(c,d):=Z_U(cc|dd)
 =h b_e^c b_f^d+b_e^c k_f^d+k_e^c b_f^d.             (7)
```

There are six ordered pairs `(c,d)` and hence twelve scalar rows in (7).

## 2. Exhaustive complementary support classification

For a diagonal block `Y`, let

```text
supp Y={c:Y(c,c)!=0}.                                 (8)
```

### Theorem 1 (twelve-row support classification)

Assume all six `B_g,K_g` are diagonal and, for one complementary partition
`e|f`, all twelve rows in (7) vanish.  Then exactly one of the following
support alternatives holds.

1. **Both direct blocks nonzero.**  There is one colour `s` such that

   ```text
   supp B_e, supp B_f, supp K_e, supp K_f subset {s}. (9)
   ```

2. **Exactly one direct block nonzero.**  Suppose `B_e!=0,B_f=0`.

   - if `|supp B_e|>=2`, then `K_f=0`;
   - if `supp B_e={s}`, then `supp K_f subset {s}`.

   The block `K_e` is arbitrary subject to physical diagonality and
   `rank K_e<=2`.  The symmetric statement holds after exchanging `e,f`.

3. **Both direct blocks zero.**  The blocks `K_e,K_f` are arbitrary diagonal
   physical blocks of rank at most two.

Conversely, every support pattern in alternatives 1--3 makes all twelve rows
in (7) vanish.

### Proof

Since `m_(ef)^(c,d)=0` for every `c!=d`,

```text
b_e^c b_f^d=0                 for c!=d.               (10)
```

If both `B` supports are nonempty, their Cartesian product lies in the
diagonal `{(0,0),(1,1),(2,2)}`.  Therefore both supports equal the same
singleton `{s}`.  With (10), the second equation in (7) reduces to

```text
b_e^c k_f^d+k_e^c b_f^d=0     for c!=d.               (11)
```

Taking `c=s,d!=s` and then `c!=s,d=s` confines both `K` supports to `{s}`.
This is alternative 1.

If `B_e!=0,B_f=0`, equation (11) is `b_e^c k_f^d=0` for `c!=d`.  If
`supp B_e` contains at least two colours, then for every `d` one may choose a
different `c` in `supp B_e`, so `k_f^d=0`.  If `supp B_e={s}`, the same
equation kills `k_f^d` for every `d!=s`.  This is alternative 2.  When both
direct blocks vanish, (10)--(11) impose no condition beyond the physical
rank bound, giving alternative 3.  The converse is immediate from (7).
`square`

The classification is coefficientwise.  It does not divide by an observed
response value, choose a slope after seeing the target, or use a module
selector.

## 3. Slope-free support divisor and twelve-row detector

Choose arbitrary coefficient rows at the two pair targets,

```text
(alpha_e,beta_e), (alpha_f,beta_f) in K^2,            (12)
```

and define their physical outputs

```text
D_e=alpha_e M_e+beta_e Z_e
   =(alpha_e+h beta_e)B_e+beta_e K_e,                 (13)
```

and similarly for `f`.  No nonzero or `M`-active normalization is assumed.

### Corollary 3.1 (universal complementary support divisor)

Under Theorem 1, for every choice (12),

```text
A_(ef):=prod_(c=0)^2 D_e(c,c)D_f(c,c)=0.             (14)
```

Equivalently, no projective pair package has both `D_e` and `D_f`
three-full.

### Proof

In alternative 1, both selected blocks are supported on at most `{s}`.  In
alternative 2, the side with zero direct block is supported on at most one
colour or is zero.  In alternative 3, both selected blocks are scalar
multiples of diagonal physical `K` blocks and hence each has support at most
two.  Thus at least one factor in (14) vanishes in every case.  `square`

### Corollary 3.2 (five-row coefficient detector)

Assume all six `B_g,K_g` are diagonal and fix arbitrary pair rows (12).  Let
`sigma` be the colour cycle

```text
sigma(0)=1,       sigma(1)=2,       sigma(2)=0.       (15)
```

If `D_e,D_f` are both three-full, then at least one of the five actual response
coefficients

```text
M_U(cc|sigma(c)sigma(c))                 c=0,1,2,
Z_U(cc|sigma(c)sigma(c))                 c=0,1        (16)
```

is nonzero.  Thus fifteen fixed scalar rows cover the three complementary
partitions of one four-port set.

### Proof

Put `a_g=alpha_g+h beta_g`, so `D_g=a_gB_g+beta_gK_g`.
Assume the five rows vanish and both selected blocks are three-full.  Choose a
colour `z` with `k_e^z=0`, which exists because `rank K_e<=2`.  Fullness gives
`a_e b_e^z=D_e(z,z)!=0`.  The `M` row for `z` therefore gives
`b_f^(sigma(z))=0`.

If `z=0` or `z=1`, the corresponding `Z` row, after its zero `M` term is
removed, equals `b_e^z k_f^(sigma(z))`.  Its vanishing makes the
`sigma(z)` coefficient of `D_f` zero, a contradiction.

It remains `z=2`, so `b_f^0=0`.  Choose a missing colour `w` of `K_f`.  If
`w=0`, then `D_f(0,0)=0`.  If `w=1`, the zero `M` and `Z` rows for `c=0`
give

```text
b_e^0 b_f^1=0,        k_e^0 b_f^1=0.                 (17)
```

If `b_f^1` were nonzero, both `b_e^0,k_e^0` would vanish, contradicting
fullness of `D_e`; hence `b_f^1=0` and `D_f(1,1)=0`.  The case `w=2` is the
same argument with the rows for `c=1`.  Every case contradicts three-fullness.
`square`

This is a bounded response detector, not a claim that any row is legally
attached to a target equation.  No minimality below five rows is asserted.

## 4. Response-map-zero witness corollary

Return to the complete fixed-`Q` `GLD18` maps (1).

### Theorem 2 (response-map-zero support localization and opposite annihilation)

Suppose the full fixed-`Q` mixed GHZ equation holds and

```text
R_g=0 for all six pairs g,        R_U=0.              (18)
```

Then, for every complementary partition `e|f` and every choice of pair
operator coefficients, the support polynomial (14) vanishes.  In
particular, this applies to any legal rows chosen from the complete-nuisance
spaces `C_e`, including unequal rank-one lines, pure coordinate axes, and
rank-two spaces.

More strongly, if one selected block `D_e` is three-full, then the opposite
raw pair response vanishes:

```text
B_f=K_f=0,         f=U-e.                             (19)
```

Consequently the set of three-full selected edges is an intersecting family
in `K_4`; it has size at most three and, at size three, is a star or a
triangle.

The simultaneous hypothesis (18) is forced if each of the seven targets has
`k_S=2`, because `GLD18` then forces every `R_S=0`.  It also allows any target
with a rank-one response-invisible line and full map `R_S=0`.  A target with
`k_S=0` is included only when `R_S=0` is assumed independently.  A rank-one
pure-axis line whose one selected output is pure may instead be
response-visible; that weaker condition does not imply (18).

### Proof

The pair equations in (18) make `B_g` and `hB_g+K_g` diagonal, hence make
`K_g` diagonal.  The four-port equation makes `C(B)` and
`hC(B)+X(B,K)` pure, hence makes `X(B,K)` pure.  Therefore all twelve rows in
(7) vanish on every complementary partition.  Apply Corollary 3.1.  `square`

For the stronger claim, suppose `D_e` is three-full.  Theorem 1 first forces
`B_f=0`: if both direct blocks were nonzero, alternative 1 would confine
`B_e,K_e`, and hence `D_e`, to one colour.  If `|supp B_e|>=2`, alternative 2
already gives `K_f=0`.  It remains the case

```text
supp B_e={z},       supp K_f subset {z}.              (20)
```

Fullness of `D_e` and `rank K_e<=2` then force `K_e` to have rank two, with
the other two colours `a,b` active and `z` missing.

Write the physical shore vector at port `u` and colour `c` as

```text
v_u^c=(x_u^c,y_u^c),
q((r,s),(r',s'))=rs'+sr'.                             (21)
```

At an endpoint `i` of `e`, the vectors `v_i^a,v_i^b` are independent: the
`a,b` submatrix of the diagonal rank-two block `K_e` has rank two.  For either
endpoint `r` of `f`, diagonality of the cross edge `K_(ir)` gives

```text
q(v_i^a,v_r^z)=q(v_i^b,v_r^z)=0.                     (22)
```

The form `q` is nondegenerate and `v_i^a,v_i^b` are a basis, so `v_r^z=0`.
This holds at both endpoints of `f`, whence `k_f^z=0`.  Together with (20),
this proves `K_f=0` and establishes (19).  The intersecting-family statement
is the elementary classification of pairwise-intersecting edges in `K_4`.
`square`

This theorem localizes the response-map-zero witness stratum to all three
support divisors without requiring a four-port operator selector.  It does
not prove that branch empty.

## 5. Sharp controls

The following are exact response or formal-module controls, not hypothetical
witnesses or counterexamples.

### 5.1 Pure normalization survives on the divisor

Set `h=0`, `K=0`, and support the three colours of `B` on the three perfect
matchings:

```text
B_12=B_34=E_00,
B_13=B_24=E_11,
B_14=B_23=E_22.                                      (23)
```

All pair responses are diagonal,

```text
M_U=e_0^tensor4+e_1^tensor4+e_2^tensor4,   Z_U=0.    (24)
```

and (18) holds with all three pure four-port coefficients equal to one.
Each complementary partition is nevertheless confined to one colour, so
(14) vanishes for every pair-row choice.  The three displayed complementary
products are nonzero, one in each colour, so this control also retains
three-colour pair-depth activity across different matchings.  Pure
normalization and activity do not exclude the response-map-zero support
stratum.

### 5.2 The annihilation conclusion is attained

Take `h=0` and the pair-row coefficients `(alpha,beta)=(1,1)`.  Set

```text
x_1=x_2=e_0+e_1,       y_1=y_2=e_0-e_1,
x_3=y_3=x_4=y_4=0,     B_12=E_22,                    (25)
```

with every other direct block zero.  Then

```text
K_12=diag(2,-2,0),      D_12=diag(2,-2,1),
C(B)=X(B,K)=0,          B_34=K_34=0.                 (26)
```

Thus an isolated three-full selected edge can occur on a physical
response-map-zero window, and its opposite raw response vanishes exactly as
Theorem 2 asserts.  The theorem localizes this branch; it does not exclude it.

### 5.3 Four-port invisibility is load-bearing

If `K=0` and every `B_g=I_3`, all six pair maps have zero mixed part and every
direct pair block is three-full, but `C(B)` has nonzero mixed `2+2` words.
Thus pair invisibility alone does not imply (14).

More sharply, set `h=0`, use the pair row `(1,1)`, and take the physical
rank-two channel

```text
K_g=diag(2,-2,0)                                     (27)
```

on every edge, support `B_14=B_23=E_22`, and put every other `B` block zero.
Then `C(B)=e_2^tensor4` is pure and
`D_14=D_23=diag(2,-2,1)` for coefficient row
`(1,1)`, but

```text
X(B,K)(22|00)=2.                                     (28)
```

So the residual-present four-port purity in (18) is separately
load-bearing.

### 5.4 The physical rank bound is load-bearing

Formally take `B_e=B_f=0` and `K_e=K_f=I_3`.  All twelve rows vanish and the
pure-`Z` blocks are three-full.  This violates only the physical bound
`rank K<=2` and is not a physical `q=2` response.

### 5.5 A pure selected axis need not make the map zero

At module level, take `C=K(0,1)`, a mixed tensor `M=E_01`, and `Z=0`.  Then
`C=ker R` while `R!=0`; the pure-`Z` operator line is response-visible, not a
response-map-zero target.
This prevents replacing (18) by purity of one selected combination.

## 6. Exact frontier and scope ledger

```text
twelve-row complementary support classification:       PROVED;
five-row-per-complement detector:                        PROVED;
slope-free support polynomial identity:                 PROVED;
fully R=0 seven-target localization:                     PROVED;
three-full edge forces opposite raw response zero:       PROVED;
pure-M / pure-Z / unequal / rank-two row coverage:       PROVED;
physical rank-two sharpness:                             PROVED;
pure normalized response-map-zero control:               PROVED;
R_S=0 forced on every witness:                          UNKNOWN;
response-map-zero support-divisor stratum excluded:      UNKNOWN;
nonzero legal pair rows forced on that branch:           UNKNOWN;
cross-window integration and activity:                  UNKNOWN;
weighted permanent implication:                        UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.
```

Scope:

- **field:** characteristic zero;
- **breadth:** one fixed graph, residual pair, contraction, basis, and named
  four-port set, with all six pair responses and both four-port layers;
- **module depth:** the complete nonempty-even fixed-`Q` deck only in the
  conditional witness corollary;
- **response depth:** pair and four-port layers;
- **reconstructed object:** none; the result is a support classification,
  a five-row mixed detector per complement, and
  opposite-pair annihilation;
- **ambiguity:** arbitrary projective pair-row choices survive, but their
  outputs lie on all three complementary support divisors under (18);
- **target implication:** exact localization of the response-map-zero
  stratum, not its exclusion;
- **permanent implication:** none.

## Verification boundary

The focused primary replay is

```text
python claims/arbitrary-order/verify_fixed_q_fully_response_invisible_complementary_support_divisor.py
```

It uses exact SymPy tensor enumeration and separately enumerates all
`8^2*7^2=3136` diagonal support configurations for one complement.  It checks
the twelve response formulas, alternatives 1--3, the fixed five-row detector,
the universal support divisor, an exact physical fixture attaining opposite
raw-pair annihilation, and the sharp controls.

The independent audit is

```text
python -I claims/arbitrary-order/audit_fixed_q_fully_response_invisible_complementary_support_divisor.py
```

It imports neither SymPy nor the primary.  It uses standard-library sparse
tensor dictionaries, direct perfect-matching enumeration, set-theoretic
support classification, and raw physical endpoint vectors for the controls.

The replays audit the bounded formulas and finite support ledger.  The
arbitrary-field implication from the full response maps, the exact support
classification, the common-shore orthogonality proof of general opposite
annihilation, and the conditional witness interpretation remain the
load-bearing written proof.
