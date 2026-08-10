# The two axis cofactors coexist with full-span residual ports

## Status

**Exact arbitrary-order characteristic-zero realization and proof-route
no-go.**  Let `m>=5` be odd.  There is one legal loopless symmetric
three-colour graph on an odd blocker set

```text
B={b_0,...,b_(m-1)}
```

and two fixed residual endpoints `q_0,q_1` such that all of the following
hold simultaneously.

1. The endpoint--endpoint value is zero.
2. Both blocker-to-endpoint row families span `(K^3)^*`.
3. The two endpoint-deletion matching tensors are exactly

   ```text
   H_(B union {q_0}) = D_0+D_1,
   H_(B union {q_1}) = D_0-D_1,
   D_c=e_c^(tensor m).                                (1)
   ```

   Thus they are independent, contain no mixed-colour coefficient, and
   frame the exact binary diagonal plane required by the all-axis
   two-endpoint full-root jet.
4. Every residual four-vertex block has the torus-zero two-port form

   ```text
   W_uv=a_u tensor b_v+b_u tensor a_v.                (2)
   ```

For odd root count `r=m-2`, in particular the five-root/seven-blocker cell,
the parity-allowed full-root deletion classes are precisely the complements
`B union {q_0}` and `B union {q_1}`.  Hence simultaneous principal-hafnian
realizability of those two classes, mixed-colour cancellation inside them,
the zero residual edge, and full port-row span cannot close the axis branch.
The next obstruction must use lower-root deletion cofactors, the shared
root-row/`P_m` equations, or nonprojective compatibility.

This residual gadget does **not** supply root rows making the two-port tensor
equal `Delta_3`, and is not a Krenn--Gu counterexample.  It proves a sharp
boundary for one proof route only.  The arbitrary-order local-to-global
reduction and the global Krenn--Gu conjecture remain **UNRESOLVED**.  No
finite field is used.

## Alternating path

Fix the endpoint vectors to

```text
z_0=z_1=(1,1,1).                                      (3)
```

On the blocker path put

```text
B_(b_i,b_(i+1)) = e_1 e_1^T     for i even,
B_(b_i,b_(i+1)) = e_0 e_0^T     for i odd.            (4)
```

All other blocker--blocker blocks vanish.  Define the blocker covectors seen
from the two endpoints by

```text
a_0=e_0^*,       a_1=e_2^*,       a_(m-1)= e_1^*,
b_0=e_0^*,       b_1=e_2^*,       b_(m-1)=-e_1^*,     (5)
```

and set every unlisted `a_u,b_u` to zero.  Realize them by the honest blocks

```text
B_(b_u,q_0)=a_u tensor e_2^*,
B_(b_u,q_1)=b_u tensor e_2^*,                         (6)
```

with transpose blocks in the reverse orientations.  Finally set
`B_(q_0,q_1)=0`.  Equations (3) and (6) evaluate to the row families in
(5).  Each family contains `e_0^*,e_1^*,e_2^*`, so both have rank three.

## Exact endpoint cofactors

Every perfect matching of `B union {q_t}` pairs `q_t` to one blocker `b_j`.
The remaining path after deleting `b_j` has a perfect matching exactly when
`j` is even.  It is then unique.

- For `j=0`, the remaining edges are
  `(b_1b_2),(b_3b_4),...`; all have colour zero.
- For `j=m-1`, the remaining edges are
  `(b_0b_1),(b_2b_3),...`; all have colour one.
- For an interior even `j`, the left and right path components have the two
  different colours, but (5) makes both endpoint rows zero there.
- For odd `j`, no complementary perfect matching exists.  In particular the
  rank-supplying row `e_2^*` at `b_1` is invisible to both endpoint
  cofactors.

Thus exactly two matching terms survive.  At `q_0` they have coefficients
`+1,+1`; at `q_1` they have coefficients `+1,-1`.  This proves (1), including
the cancellation-free vanishing of every mixed blocker word.

The construction is stronger than local dominance of scalar principal
cofactors: both prescribed tensors occur exactly, in the same sparse graph,
and the edge evaluations needed by the two-port reduction remain full-span.

The whole one-blocker-deletion ledger is explicit as well.  Put

```text
K_j=H_(B minus {b_j}).                                 (7)
```

For odd `j`, both path components have odd order, so `K_j=0`.  For even `j`,
the complementary path matching is unique and

```text
K_j
 =e_1^(tensor j) tensor e_0^(tensor (m-1-j)),          (8)
```

with the omitted `b_j` slot understood.  In particular `K_0` and
`K_(m-1)` are the two pure endpoint cofactors, while every interior even
deletion is a fixed split-colour monomial.  The rank-supplying `e_2^*` rows
in (5) sit at the odd vertex `b_1`, where `K_1=0`.  Thus the endpoint Laplace
expansions

```text
H_(B union {q_0})=sum_j a_j tensor K_j,
H_(B union {q_1})=sum_j b_j tensor K_j                (9)
```

retain full port-row rank while seeing only the two binary pure terms.  This
is an exact compatibility across the complete principal-deletion ledger,
not just an isolated pair of prescribed outputs.  A future lower-root
obstruction must prevent port rank from hiding on such zero cofactors or use
the split-colour `K_j` values.

## Four-vertex compatibility

For blockers `u<v`, expand the three perfect matchings on
`{u,v,q_0,q_1}` after fixing (3):

```text
W_uv
 =h B_uv+a_u tensor b_v+b_u tensor a_v,
h=B_(q_0,q_1)(z_0,z_1).                             (10)
```

Here `h=0`, so (10) is exactly (2), including all diagonal and off-diagonal
blocker inputs.  Therefore the construction lies on the factorized side of
[`TWO_RESIDUAL_NONBLOCKER_TWO_PORT_FACTORISATION.md`](TWO_RESIDUAL_NONBLOCKER_TWO_PORT_FACTORISATION.md),
while meeting its necessary full-span port condition.

What remains missing is decisive: no root-row family `H` is provided for

```text
P_m(H;a;b)=Delta_3.                                  (11)
```

Nor are the lower mixed-root cofactor frames from
[`ROOT_ARBITRARY_LOWER_MIXED_JET_COFACTOR_FRAME_NECESSITY.md`](ROOT_ARBITRARY_LOWER_MIXED_JET_COFACTOR_FRAME_NECESSITY.md)
claimed.  The earlier full-jet sharpness graph fails one such lower value;
the present theorem shows only that the two top deletion cofactors and the
port prerequisites themselves are not the source of that failure.

## Boundary

```text
odd blocker count m>=5:                              PROVED;
two full-root parity cofactors:                      EXACT BINARY FRAME;
mixed-colour coefficients in those two cofactors:   ZERO;
both residual port-row spans:                        THREE;
residual edge and h-term:                            ZERO;
factorized two-port blocks:                          REALIZED;
lower-root deletion cofactor compatibility:          UNKNOWN;
P_m(H;a;b) -> Delta_3:                               NOT REALIZED;
global Krenn-Gu conjecture:                          UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_root_arbitrary_two_endpoint_binary_cofactor_port_compatibility_realization.py
python claims/arbitrary-order/audit_root_arbitrary_two_endpoint_binary_cofactor_port_compatibility_realization.py
uv run --with sympy --with ruff python -m ruff check claims/arbitrary-order/verify_root_arbitrary_two_endpoint_binary_cofactor_port_compatibility_realization.py claims/arbitrary-order/audit_root_arbitrary_two_endpoint_binary_cofactor_port_compatibility_realization.py
python -m py_compile claims/arbitrary-order/verify_root_arbitrary_two_endpoint_binary_cofactor_port_compatibility_realization.py claims/arbitrary-order/audit_root_arbitrary_two_endpoint_binary_cofactor_port_compatibility_realization.py
```

The primary constructs the actual integer `3 x 3` blocks, enumerates every
surviving endpoint cofactor matching through fifteen blockers, and checks
the exact four-vertex tensor formula.  The no-import audit uses a separate
path recurrence, integer row reduction, and direct outer-product arithmetic
through twenty-one blockers.  These bounded calculations audit the indexing;
the unique path matching argument proves every odd `m>=5` in characteristic
zero.
