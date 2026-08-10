# The explicit binary cofactor gadget has a two-port Hall deficiency

## Status

**Exact arbitrary-order characteristic-zero obstruction.**  The odd-blocker
residual gadget in
[`ROOT_ARBITRARY_TWO_ENDPOINT_BINARY_COFACTOR_PORT_COMPATIBILITY_REALIZATION.md`](ROOT_ARBITRARY_TWO_ENDPOINT_BINARY_COFACTOR_PORT_COMPATIBILITY_REALIZATION.md)
realizes the two required binary top cofactors and gives each residual port
family full global row span.  Nevertheless no choice of root-row matrices can
make its shared two-port permanent tensor a three-colour diagonal.

For every odd `m>=5`, every family

```text
H_u in K^((m-2) x 3),             u=0,...,m-1,          (1)
```

and the explicit port rows `a_u,b_u`, one has

```text
[c^m] P_m(H;a;b)=0,              c=0,1,2.              (2)
```

Thus the gadget fails even the three desired pure coefficients, before any
mixed-colour cancellation is imposed.  In particular, at `m=7` it cannot
extend to the five-root/seven-blocker identity for any legal root-row family
`H`.

The argument generalizes as a necessary Hall condition for every two-port
permanent restriction: for each desired colour, the two port rows must be
matchable to two distinct blocker columns on that pure input.  Global span of
the two row families separately does not imply this colourwise condition.

This closes the explicit residual gadget, not the whole two-endpoint axis
branch.  Other full-span port families may satisfy the Hall condition, and
the coordinate-monomial residual-edge branch remains separate.  The
arbitrary-order local-to-global reduction and the global Krenn--Gu conjecture
remain **UNRESOLVED**.  No finite field is used.

## Pure coefficient expansion

For a target word `w`, the coefficient of the contracted permanent is the
permanent of the `m x m` matrix whose blocker column `u` is

```text
(H_u[0,w_u],...,H_u[m-3,w_u],a_u[w_u],b_u[w_u])^T.    (3)
```

Put `w=c^m` and expand the permanent along its final two rows.  If

```text
R_(uv,c)=per([H_t[:,c]]_(t notin {u,v})),             (4)
```

then

```text
[c^m] P_m(H;a;b)
 =sum_(u<v)
   (a_u[c] b_v[c]+b_u[c] a_v[c]) R_(uv,c).            (5)
```

This is the unsigned two-row Laplace expansion.  The root cofactors in (4)
are completely arbitrary for the present argument.

## The support defect

The explicit port rows are

```text
a_0=e_0^*,       a_1=e_2^*,       a_(m-1)= e_1^*,
b_0=e_0^*,       b_1=e_2^*,       b_(m-1)=-e_1^*,     (6)
```

with every unlisted row zero.  Therefore their colourwise supports are

```text
supp(a[-,0])=supp(b[-,0])={0},
supp(a[-,2])=supp(b[-,2])={1},
supp(a[-,1])=supp(b[-,1])={m-1}.                      (7)
```

For distinct columns `u,v`, every two-port permanent in parentheses in (5)
is zero.  Equivalently, the bipartite incidence graph from the two port rows
to nonzero pure-colour columns has only one neighbour, violating Hall's
condition.  Equation (2) follows independently of (4).

Notice the distinction exposed by the two exact packages:

```text
span{a_u:u in B}=span{b_u:u in B}=K^3,               (8)
```

but the same colour occurs in both families only at one shared blocker.
The earlier full-span theorem is necessary, while (7) is a new and strictly
stronger colourwise obstruction for this gadget.

## General two-port Hall corollary

For arbitrary port families define

```text
A_c={u:a_u[c] != 0},       B_c={u:b_u[c] != 0}.       (9)
```

If the pure coefficient of colour `c` is nonzero, then there are distinct
columns `u,v` with either

```text
u in A_c and v in B_c,
or u in B_c and v in A_c.                            (10)
```

In particular

```text
A_c != emptyset,   B_c != emptyset,   |A_c union B_c|>=2.             (11)
```

These are support necessities only.  Even when (11) holds, the root
cofactors in (5) may vanish or the nonzero summands may cancel.  No
sufficiency claim is made.

## Consequence for the axis frontier

At five roots and seven blockers, the alternating-path construction proved
that the following data coexist exactly:

```text
binary full-root cofactor frame;
zero mixed coefficients in both top cofactors;
zero residual edge;
rank-three port family a;
rank-three port family b.
```

The present theorem proves that this compatibility was obtained by hiding
the third row directions on zero principal cofactors and concentrating each
pure port colour at one column.  That mechanism cannot cross the first
shared identity `P_7(H;a;b)=Delta_3`.  A surviving two-endpoint axis system
on the torus-zero branch must therefore use different port data satisfying
(11) for all three colours, in addition to the previously proved lower-jet
cofactor frames.

The exact boundary is

```text
explicit alternating-path port gadget:        EXCLUDED at P_m identity;
all three pure P_m coefficients:               IDENTICALLY ZERO;
obstruction valid for every odd m>=5:          YES;
arbitrary full-span Hall-satisfying ports:      UNKNOWN;
coordinate-monomial residual edge:              UNKNOWN;
global Krenn-Gu conjecture:                     UNRESOLVED.
```

## Replay

Replay the construction first:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_root_arbitrary_two_endpoint_binary_cofactor_port_compatibility_realization.py
python claims/arbitrary-order/audit_root_arbitrary_two_endpoint_binary_cofactor_port_compatibility_realization.py
```

Then run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_root_arbitrary_two_endpoint_port_hall_deficiency_obstruction.py
python claims/arbitrary-order/audit_root_arbitrary_two_endpoint_port_hall_deficiency_obstruction.py
uv run --with sympy --with ruff python -m ruff check claims/arbitrary-order/verify_root_arbitrary_two_endpoint_port_hall_deficiency_obstruction.py claims/arbitrary-order/audit_root_arbitrary_two_endpoint_port_hall_deficiency_obstruction.py
python -m py_compile claims/arbitrary-order/verify_root_arbitrary_two_endpoint_port_hall_deficiency_obstruction.py claims/arbitrary-order/audit_root_arbitrary_two_endpoint_port_hall_deficiency_obstruction.py
```

The primary checks the symbolic two-row Laplace coefficients at `m=7` and
exact integer permanents through `m=15`.  The independent no-import audit
enumerates the port assignments, verifies Hall deficiency through `m=25`,
and checks a mixed-word control showing that the permanent map itself need
not vanish.  These bounded computations audit the indexing; equations
(5)--(7) prove every odd order in characteristic zero.
