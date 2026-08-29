# Maximum-root surplus-two zero-anchor six-deficient one-`T_0` off-port-core full-source nonextension and coupled-correction boundary

## Status

This is theorem package **GLS73**.  It continues the top-down Family-A
`r=1` descent from `GLS72` and proves that the exact sharpness control there
cannot be repaired by changing only the edges incident to its silent `T_0`
port.  In fact the theorem allows those five incident edges to be replaced
arbitrarily, not merely by kernel-invisible corrections, and allows every
unused probe-map coefficient compatible with the one-silent chart.

Two coefficients of the complete six-open source identity give the
contradiction.  The nonzero colour-zero diagonal forces one transverse
coefficient of `W_25` to be nonzero.  A mixed `P_0Q_2` word, whose target is
zero, isolates the same coefficient through `W_14W_25` and forces it to
vanish.

This is an exact **nonextension theorem for one physical off-port core** and
a coupled-correction boundary.  It does not exclude the complete Family-A
`r=1` key: a hypothetical source may change an edge not incident to the
silent port and thereby open another cancelling deck channel.  No typed
profile is removed.  The six-deficient residual remains `98,355 / 81`, and
the global Krenn--Gu conjecture remains **UNRESOLVED**.

## 0. Parent source identity

Use the complete zero-anchor root-order-three identity owned by `GLS61`.
There are two probe variables with coordinates

```text
P_a=z_(0,a),                 Q_a=z_(1,a),              a=0,1,2,
```

and six auxiliary labels `0,...,5`.  At auxiliary label `i`, write the two
probe shores as `p_i(P)` and `q_i(Q)`, and put

```text
g_ij=p_i tensor q_j+q_i tensor p_j.
```

For physical auxiliary-edge tensors `W_ij`, let `H_I` be the perfect-matching
tensor on the even set `I`.  The complete identity is

```text
sum_({i,j} subset {0,...,5}) g_ij tensor H_({0,...,5}-{i,j})
 =sum_(a=0)^2 mu_a P_aQ_a tensor_(i=0)^5 e_(i,a),     (1)
```

where `mu_0 mu_1 mu_2!=0`.  Equation (1) is an identity in both probe
variables and all six auxiliary covector slots.

Use the Family-A crossed triangle normalization

```text
p_0=P_1 e_(0,1),             q_0=Q_2 e_(0,2),
p_1=P_2 e_(1,2),             q_1=0,
p_2=0,                       q_2=Q_1 e_(2,1).         (2)
```

Ports `3,4` have type `R_0`, so every one of their probe coefficients lies
on `K e_(i,0)`.  Port `5` is the selector-silent `T_0` port:

```text
[P_0]p_5=[Q_0]q_5=0.                                  (3)
```

Both equalities in (3) are equalities of full local covectors.  They do not
mean only that one `e_(5,0)` coordinate vanishes.

Write

```text
[P_0]p_3=A e_(3,0),            [Q_0]q_3=B e_(3,0),
[P_0]p_4=C e_(4,0),            [Q_0]q_4=D e_(4,0).    (4)
```

The one-silent bridge gives

```text
c_34=AD+BC!=0.                                         (5)
```

After the legal label/probe exchange used in `GLS72`, take

```text
A D!=0.                                                (6)
```

All other coefficients of the maps in (2)--(4), including the complete
rank-two row map at port `5`, remain arbitrary.

## 1. The fixed off-port core

Choose bases at ports `3,4` so that

```text
x_3=e_(3,1),       y_3=e_(3,2),
x_4=e_(4,1),       y_4=e_(4,2).
```

Fix only the ten physical edges whose endpoints avoid port `5` to their
values in the `GLS72` common-edge control:

```text
W_01=e_(0,0)e_(1,0),
W_02=W_03=W_04=0,
W_12=0,
W_13=e_(1,1)x_3+e_(1,0)y_3,
W_14=-e_(1,0)x_4,
W_23=0,
W_24=e_(2,2)y_4,
W_34=0.                                                (7)
```

No condition is imposed on

```text
W_05,W_15,W_25,W_35,W_45.                              (8)
```

Thus (8) includes every kernel-invisible lift of `GLS72` equation (35), but
also arbitrary changes of the restrictions of those five edges.  The result
below is therefore stronger than a transverse-only-lift exclusion.

## 2. Two-coefficient nonextension theorem

### Theorem 2.1 (the off-port core (7) has no full GHZ-source completion)

There are no choices of the five incident edges (8), of the unused probe-map
coefficients, or of nonzero target weights `mu_a` for which (1)--(7) hold.

### Proof

Put

```text
xi=[e_(2,0)e_(5,0)]W_25.                              (9)
```

First take the `P_0Q_0` coefficient of (1) and then its all-colour-zero local
word.  By (2)--(4), the only source pair with a nonzero `P_0Q_0` coefficient
is `{3,4}`; its coefficient is `c_34`.  The matching expansion

```text
H_(0125)=W_01W_25+W_02W_15+W_05W_12                  (10)
```

and (7) give

```text
[e_(0,0)e_(1,0)e_(2,0)e_(5,0)]H_(0125)=xi.
```

Consequently the selected coefficient of (1) is

```text
c_34 xi=mu_0.                                         (11)
```

Equations (5) and `mu_0!=0` imply

```text
xi!=0.                                                (12)
```

Now take the mixed probe coefficient `P_0Q_2` and the auxiliary local word

```text
omega=e_(0,2)e_(1,0)e_(2,0)e_(3,0)x_4e_(5,0).       (13)
```

Its target coefficient is zero.  The pair `{0,3}` contributes because
`[Q_2]q_0=e_(0,2)` and `[P_0]p_3=Ae_(3,0)`.  Its complementary deck is

```text
H_(1245)=W_12W_45+W_14W_25+W_15W_24.                 (14)
```

On the word left after removing slots `0,3`, the first matching in (14)
vanishes because `W_12=0`; the third cannot use `e_(2,0)x_4` because
`W_24=e_(2,2)y_4`; and the second gives `-xi`.  Hence the `{0,3}` term in
(13) is `-Axi`.

For completeness, no other source pair contributes to (13):

1. every pair using port `4` as a probe endpoint has local factor
   `e_(4,0)`, not `x_4`;
2. port `5` has no `P_0` coefficient by (3);
3. the only remaining possible pair is `{3,5}`, using the `Q_2` coefficient
   of `q_5`; its complementary deck is `H_(0124)`, but (7) gives

   ```text
   [e_(0,2)e_(1,0)e_(2,0)x_4]H_(0124)=0              (15)
   ```

   across all three matchings `W_01W_24`, `W_02W_14`, and `W_04W_12`.

Thus the zero mixed target coefficient is exactly

```text
-A xi=0.                                              (16)
```

Since `A!=0` by (6), equation (16) gives `xi=0`, contradicting (12).
`square`

### Corollary 2.2 (a repair must change the off-port core)

No completion of the `GLS72` sharpness control can be obtained by modifying
only edges incident to its silent `T_0` port, even if those modifications
are allowed to change their kernel restrictions arbitrarily.

Any surviving Family-A `r=1` source must change at least one edge in (7).
At the two-row interface above, it must either open the currently zero
`H_(0124)` coefficient in (15) or change one of the other matching channels
in (10) or (14) while preserving the already proved `GLS72` restrictions.
That is a genuinely coupled off-port source-integrability obligation.

## 3. Exact scope and frontier

This package proves

```text
GLS72 exact edge control:                     locally compatible;
arbitrary incident-edge completion
  with the GLS72 off-port core fixed:                     EMPTY;
complete Family A r=1 key:                                OPEN;
unchanged inherited six-deficient residual:     98,355 / 81;
global Krenn--Gu conjecture:                         UNRESOLVED.          (17)
```

The theorem does not say that every point of the localized
`alpha=a=b=0` branch has the off-port normal form (7).  It therefore removes
no profile.  It also does not construct a graph witness or a source-level
counterexample.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_one_t0_off_port_core_full_source_nonextension.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_one_t0_off_port_core_full_source_nonextension.py
```

The primary verifier enumerates every source-pair contribution and every
four-deck matching to the two selected coefficients with symbolic arbitrary
incident-edge entries and arbitrary unused probe coefficients.  It recovers
`c_34 xi-mu_0` and `-Axi` exactly.

The independent audit uses a separate sparse monomial representation and
finite-field substitutions.  It checks the complete pair/matching support of
both rows, including the zero `H_(0124)` repair channel, without importing
the primary verifier.  The source-level provenance, the legal activity
orientation, and the conclusion that the wider Family-A key stays open are
written mathematics.  The residual count is inherited from `GLS72`, not
recomputed by either GLS73 script.  Neither program proves the global
conjecture.
