# Hall-satisfying two-port data reach the pure `P_7` coefficients

## Status

**Exact bounded characteristic-zero construction and proof-route no-go.**  On
the five-root/seven-blocker torus-zero branch there are legal residual blocks,
two full-span port families `a,b`, and root-row matrices `H_u` such that:

1. the two endpoint cofactors are exactly `D_0+D_1` and `D_0-D_1` with no
   mixed blocker word;
2. the residual edge is zero and every four-vertex residual block is
   `a_u tensor b_v+b_u tensor a_v`;
3. both port families have rank three and satisfy the colourwise two-column
   Hall condition for all three colours;
4. every one of the five root-row families spans the full target dual;
5. every local seven-by-three blocker map has rank three; and
6. the three pure coefficients of `P_7(H;a;b)` are exactly `(1,1,1)`.

Thus the Hall condition added by
[`ROOT_ARBITRARY_TWO_ENDPOINT_PORT_HALL_DEFICIENCY_OBSTRUCTION.md`](ROOT_ARBITRARY_TWO_ENDPOINT_PORT_HALL_DEFICIENCY_OBSTRUCTION.md)
is genuinely attainable jointly with all presently required rank and top-
cofactor data.  It is still far from sufficient: the first lexicographic
mixed word

```text
0000102
```

has coefficient one.  The complete tensor has 36 nonzero coefficients: the
three desired pure coefficients and 33 forbidden mixed coefficients.

This is not a `P_7 -> Delta_3` restriction and not a Krenn--Gu counterexample.
It identifies mixed-colour cancellation as the first failure of this exact
Hall-satisfying model.  Whether some other Hall-satisfying port/root system
cancels every mixed word remains **UNKNOWN**.  The arbitrary-order
local-to-global reduction and the global Krenn--Gu conjecture remain
**UNRESOLVED**.  No finite field is used.

## Shared blocker path and endpoint cofactors

Let `B={0,...,6}` and fix both endpoint vectors to `(1,1,1)`.  On the blocker
path put diagonal rank-one blocks of alternating colours:

```text
edge 01: colour 1,    edge 12: colour 0,
edge 23: colour 1,    edge 34: colour 0,
edge 45: colour 1,    edge 56: colour 0.              (1)
```

The principal blocker cofactors `K_j=H_(B minus {j})` are zero for odd `j`
and, with the deleted slot omitted,

```text
K_0=e_0^6,
K_2=e_1^2 tensor e_0^4,
K_4=e_1^4 tensor e_0^2,
K_6=e_1^6.                                           (2)
```

Choose the two endpoint row families as follows; an omitted entry is zero.

```text
u       0       1       3       5       6
a_u    e_0             e_2     e_1     e_1
b_u    e_0     e_0             e_2    -e_1.          (3)
```

Realize these rows by the legal symmetric blocks

```text
B_(u,q_0)=a_u tensor e_2^*,
B_(u,q_1)=b_u tensor e_2^*,
B_(q_0,q_1)=0.                                      (4)
```

Only the even endpoint rows at `u=0,6` see nonzero cofactors in (2).  Hence

```text
H_(B union {q_0})=D_0+D_1,
H_(B union {q_1})=D_0-D_1.                          (5)
```

All mixed words vanish termwise.  The additional rows at `u=1,3,5` lie on
zero principal cofactors and do not change (5).

Both families in (3) span all three coordinate covectors.  Their colourwise
supports are

```text
A_0={0},       B_0={0,1},
A_1={5,6},     B_1={6},
A_2={3},       B_2={5}.                              (6)
```

Each pair is nonempty and its union has size two, so every colour passes the
two-port Hall condition sharply.

## Exact root rows

Let `f_0,...,f_4` be the standard basis of the five root-row slots.  Define
the three columns of the `5 x 3` root matrix `H_u` by the table

```text
u       H_u[:,0]    H_u[:,1]    H_u[:,2]
0          0          -f_0         f_1
1          0           f_1         f_0
2         f_0          f_2         f_4
3         f_1          f_3          0
4         f_2          f_4         f_3
5         f_3           0            0
6         f_4           0           f_2.             (7)
```

These are honest root--blocker rows.  With every root vector
`x=(1,1,1)` and scalar tangent covector `e_2^*`, the edge block

```text
B_(r_i,u)=e_2^* tensor H_u[i,-]                       (8)
```

has value `H_u[i,-]` at `x`, vanishes on `ker(e_2^*)`, and is paired with
its transpose in the reverse orientation.  Root--root and root--endpoint
blocks may be set to zero for this bounded residual construction.  Direct
row reduction of (7) gives

```text
dim span{H_u[i,-]:u in B}=3       for every root i.   (9)
```

Moreover, append `a_u,b_u` below `H_u`.  Every resulting local `7 x 3` map

```text
M_u=[H_u;a_u;b_u]                                    (10)
```

has rank three.  Thus the construction does not hide its failure in a
nonconcise local map.

## The pure coefficients

Expand the last two permanent rows first.

- On `0^7`, the unique port assignment is `a -> 0`, `b -> 1`.  The remaining
  root columns `2,3,4,5,6` are `f_0,f_1,f_2,f_3,f_4`.
- On `1^7`, the unique assignment is `a -> 5`, `b -> 6`.  Its port product
  is `-1`, while root columns `0,1,2,3,4` are
  `-f_0,f_1,f_2,f_3,f_4`, so the root permanent is also `-1`.
- On `2^7`, the unique assignment is `a -> 3`, `b -> 5`.  Root columns
  `0,1,2,4,6` are `f_1,f_0,f_4,f_3,f_2`, a permutation basis.

Therefore

```text
[0^7]P_7(H;a;b)=[1^7]P_7(H;a;b)=[2^7]P_7(H;a;b)=1.   (11)
```

This proves that top-cofactor compatibility, full port and root-row spans,
local concision, colourwise Hall support, and all three desired pure
coefficients coexist over the integers.

## First mixed failure

Take the word

```text
w=(0,0,0,0,1,0,2).                                  (12)
```

Only the port assignment `a -> 0`, `b -> 1` survives.  The remaining root
columns `2,3,4,5,6` are

```text
f_0,f_1,f_4,f_3,f_2,                                (13)
```

again a permutation basis.  Hence

```text
[w]P_7(H;a;b)=1,                                     (14)
```

where the GHZ target coefficient is zero.  No cancellation is possible in
this coefficient because it contains one permanent term.

Exact enumeration of all `3^7=2187` words gives

```text
coefficient  0: 2151 words,
coefficient +1:   24 words,
coefficient -1:   12 words.                          (15)
```

The three monochromatic words are among the `+1` entries, leaving 33 nonzero
mixed words.  Equation (14) is the first such word in lexicographic order.

## Boundary

```text
binary endpoint cofactor frame:                REALIZED;
zero mixed words in the endpoint cofactors:    REALIZED;
h=0 two-port factorization:                    REALIZED;
rank(a)=rank(b)=3:                             REALIZED;
colourwise Hall support:                       REALIZED;
all five root-row spans equal three:           REALIZED;
all seven local map ranks equal three:         REALIZED;
three pure P_7 coefficients equal one:         REALIZED;
all mixed P_7 coefficients vanish:             NO for this construction;
arbitrary Hall-satisfying P_7 restriction:      UNKNOWN;
global Krenn-Gu conjecture:                     UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_root_m7_hall_satisfying_two_port_pure_p7_construction.py
python claims/arbitrary-order/audit_root_m7_hall_satisfying_two_port_pure_p7_construction.py
uv run --with sympy --with ruff python -m ruff check verify_root_m7_hall_satisfying_two_port_pure_p7_construction.py audit_root_m7_hall_satisfying_two_port_pure_p7_construction.py
python -m py_compile verify_root_m7_hall_satisfying_two_port_pure_p7_construction.py audit_root_m7_hall_satisfying_two_port_pure_p7_construction.py
```

The primary constructs the legal integer blocks, verifies every span and
local rank, enumerates the endpoint cofactors, checks all four-vertex
factorizations, and evaluates all 2,187 `P_7` coefficients.  The no-import
audit uses independent rational row reduction, a separate permanent dynamic
program, and a separate path-matching recursion.  Everything is over the
integers; no finite-field inference occurs.
