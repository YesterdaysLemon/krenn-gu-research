# The P7 root budget, conditional dual-Wick observability, and the quartic escape

## Status

**Exact characteristic-zero legality boundary, conditional selector theorem,
and legal non-observability counterfamily.**  A principal-cofactor term in an
actual `P_7` root Laplace expansion partitions the seven non-port vertices
into probe roots and the retained residual set.  This gives an unconditional
rank-layer budget for every response window obtained by the current
deletion/cofactor mechanism.

For two residual vertices, even the most favorable four-port window can make
the six residual-present pairs `z_e` and the two top values `m_W,z_W`
eligible, but no direct pair `m_e` is eligible.  With four residual vertices
only three probe roots remain, so even the residual-present pairs `z_e` and
every direct `m`-layer are outside the budget.  Thus neither case directly
produces a partition-closed four-cube.

This is not only a counting gap.  Grant the two-residual window every
budget-eligible value, the residual scalar, and all four standard marked-star
observations of the hidden direct pairs.  The resulting thirteen-coordinate
map from honest two-residual matching responses is dominant.  Hence its
visible elimination ideal is zero.  An exact pair of legal responses has
identical values of all thirteen observations, and indeed of every
budget-eligible layer on seven ports, while its hidden direct pair family is
different.

There is one useful conditional exception.  The four-point dual-Wick defect
needs only one weighted aggregate of the six hidden direct pairs.  The four
marked stars recover that aggregate exactly when the complementary `z`-pair
weights are vertex-additive, equivalently when their three opposite-pair
sums agree.  This gives a precise conditional legal test without demanding
full partition closure.

At residual order four, a further obstruction appears: the same four-point
expression equals the quartic permanental compound, not zero.  A legal
identity-incidence response makes that defect one.  Therefore even a
hypothetical partition-closed `q=4` window cannot be fed into the `q=2`
dual-Wick equation unless its quartic layer is separately proved to vanish.

None of these statements excludes or realizes the full coloured `P_7`
problem.  Mixed-colour equations or a new selector gadget can supply data
outside the root-saturated family.  The `P_7` restriction problem and the
Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. The P7 residual/probe deletion budget

Split the seven non-port vertices of the `P_7` cell as

```text
P: probe roots, |P|=r,
Q: retained residual set, |Q|=q,
r+q=7,
B: seven blocker ports.                               (1)
```

Expand a legal coefficient along the `r` probe roots.  In every matching
partition, a nonroot vertex absent from the complementary principal cofactor
must be the endpoint of a root--nonroot edge.  Distinct deleted nonroots use
distinct roots.  A root--root edge consumes two roots and deletes no nonroot.
Consequently every cofactor term obtained in this way deletes at most `r`
vertices of `B union Q`.

Write

```text
z_S=haf G[Q union S],             m_S=haf B[S].        (2)
```

To leave `z_S`, the probe-root shore must remove `B\S`, of order `7-|S|`.
To leave `m_S`, it must remove `Q union (B\S)`, of order `q+7-|S|`.

### Theorem 1 (root-budget necessary condition)

Any response coefficient directly isolated by a `P_7` probe-root
principal-cofactor
term must satisfy

```text
z_S:  7-|S|<=7-q,             equivalently |S|>=q,
m_S:  q+7-|S|<=7-q,           equivalently |S|>=2q.  (3)
```

This count is unchanged by root--root companions, which only reduce the
number of available root--nonroot edges.

For even port sets, (3) gives

```text
q=2: five probes;  z-layers 2,4,6 and m-layers 4,6 are eligible;
q=4: three probes; z-layers 4,6 are eligible; no m-layer is eligible. (4)
```

Eligibility is only necessary: a nonzero shore and a private companion
selector are still required to isolate a named value.

Fix a four-window `W`.  A partition-closed `q=2` cube needs

```text
m_empty, (m_e), m_W,        z_empty, (z_e), z_W.      (5)
```

The normalizations `m_empty=1` and `z_empty=h` may be granted externally,
but every `m_e` violates (3).  At `q=4`, the residual-present pairs, all
direct pairs, and `m_W` violate (3).  Hence no single probe-root deletion
family directly contains a
partition-closed four-window at either residual order.

This theorem applies to the current root-saturated principal-cofactor
mechanism.  It does not prohibit an added herald, vacuum simulator, mixed
polarization identity, or other gadget not present in that mechanism.

## 2. The maximal visible two-residual map is dominant

Now grant considerably more than Theorem 1 forces.  Let

```text
W={1,2,3,4},
E=(12,13,14,23,24,34).                                (6)
```

Write the direct pair vector as `B=(B_e)`.  Two residual incidence rows
`a=(a_i),b=(b_i)` give

```text
K_ij=a_i b_j+b_i a_j,
z_ij=h B_ij+K_ij.                                     (7)
```

The direct and residual-present top responses are

```text
m_W=B_12 B_34+B_13 B_24+B_14 B_23,

z_W=h m_W
    +K_12 B_34+K_34 B_12
    +K_13 B_24+K_24 B_13
    +K_14 B_23+K_23 B_14.                             (8)
```

Also grant the four standard marked-star observations

```text
s_1=B_12+B_13+B_14,
s_2=B_12+B_23+B_24,
s_3=B_13+B_23+B_34,
s_4=B_14+B_24+B_34.                                  (9)
```

Consider the polynomial observation map

```text
F:(h,B,a,b) |-> (h,(z_e),m_W,z_W,(s_i)) in A^13.     (10)
```

### Theorem 2 (maximal-window dominance)

Over every characteristic-zero field after algebraic closure, `F` is
dominant.  Therefore there is no nonzero polynomial relation involving only
the thirteen granted values in (10) that holds for every physical
two-residual response.

### Proof

At the exact point

```text
h=1,
B=(1,0,0,0,0,1),
a=(1,0,1,2),
b=(0,1,3,1),                                          (11)
```

the `13 x 13` Jacobian minor on parameter columns

```text
(h,B_12,B_13,B_14,B_23,B_24,B_34,a_1,a_2,a_3,a_4,b_1,b_2)
```

has determinant `360`.  Thus the differential has full target rank at (11),
so (10) has dense image.

The theorem is stronger than saying that the hidden pairs are not selected:
even after the marked-star overlay and both top values are adjoined, the
visible image has zero elimination ideal.  It remains a statement about one
scalar response chart, not the mixed-colour P7 equations.

## 3. The exact conditional four-point selector

The `q=2` four-point dual-Wick equation can be written using uncorrected
responses as

```text
z_W+h m_W-sum_(e in E) z_e m_(W\e)=0.                (12)
```

Thus full recovery of all six `m_e` is stronger than necessary.  In edge
order (6), define the complementary weight vector

```text
w=(z_34,z_24,z_23,z_14,z_13,z_12).                   (13)
```

Let `A` be the marked-star matrix from (9):

```text
A=[1 1 1 0 0 0]
  [1 0 0 1 1 0]
  [0 1 0 1 0 1]
  [0 0 1 0 1 1].                                    (14)
```

Then `s=AB`, and the hidden term in (12) is `w^T B`.

### Theorem 3 (additive-weight observability)

The four marked stars linearly recover the exact hidden term in (12) if and
only if

```text
w in rowspace A,                                     (15)
```

equivalently

```text
z_12+z_34=z_13+z_24=z_14+z_23.                       (16)
```

When (16) holds, there are vertex potentials `alpha_i` with

```text
w_ij=alpha_i+alpha_j,
w^T B=sum_i alpha_i s_i.                              (17)
```

For example, using the `w` labels,

```text
alpha_1=(w_12+w_13-w_23)/2,
alpha_2=(w_12+w_23-w_13)/2,
alpha_3=(w_13+w_23-w_12)/2,
alpha_4=w_14-alpha_1.                                 (18)
```

Hence on the additive locus the legally observable equation is

```text
z_W+h m_W-sum_i alpha_i s_i=0.                        (19)
```

### Proof

The selector criterion says that `w^T B` is recoverable from `AB` exactly
when `w` belongs to the row space.  The kernel of (14) is

```text
n(s,t)=(-s-t,s,t,t,s,-s-t).                          (20)
```

Orthogonality to `n(1,0)` and `n(0,1)` is precisely (16).  Equations
(18) then solve `A^T alpha=w`, proving (17)--(19).

This condition is sharp even after adjoining `m_W`.  On a fiber of the four
stars, write `B=B_0+n(s,t)`.  The homogeneous quadratic part of `m_W` is

```text
2(s^2+s t+t^2).                                      (21)
```

It is a nondegenerate conic in characteristic zero.  If `w` is not in the
row space, `w^T n(s,t)` is a nonzero linear form and is nonconstant on a
generic level conic of `m_W`.  Thus `(s_i,m_W)` does not generically determine
the hidden insertion term outside (16).

The theorem is conditional because no current P7 result forces (16) for a
target-compatible clean window or synchronizes all four marked stars with
that window.

## 4. A sharp legal non-observability pair

The failure is visible inside the exact matching-response variety.  Put

```text
B^(0)=n(1,0)=(-1,1,0,0,1,-1),
B^(1)=n(0,1)=(-1,0,1,1,0,-1).                         (22)
```

Both have

```text
A B^(j)=0,                 m_W(B^(j))=2.              (23)
```

Each is one bosonic channel:

```text
B^(0)=u_0 v_0^T+v_0 u_0^T,
u_0=(1,0,0,-1),           v_0=(0,-1,1,0),

B^(1)=u_1 v_1^T+v_1 u_1^T,
u_1=(1,0,-1,0),           v_1=(0,-1,0,1).             (24)
```

Fix any `h!=0`.  In response `j`, use direct pair matrix `B^(j)` and residual
incidence rows `-h u_j,v_j`.  Then

```text
K^(j)=-h B^(j),
z_e^(j)=0 for every pair e,
z_W^(j)=-2h.                                          (25)
```

Consequently the two honest two-residual graphs have identical values of

```text
(h,(z_e),m_W,z_W,(s_i))=(h,0,2,-2h,0),               (26)
```

but different hidden direct pair families.

Add three isolated ports to obtain seven ports.  In both graphs every
budget-eligible coefficient agrees:

```text
all z_2; all m_4,z_4; all m_6,z_6.                   (27)
```

The only nonzero four-set is `W`, with values `(m_W,z_W)=(2,-2h)`.
Therefore this is an exact counterfamily to universal recovery from the full
root-budget deletion layers, not merely a formal observation-kernel
deformation.  It is not a P7/GHZ realization.

## 5. Four residuals do not obey the dual-Wick equation

For `q=4`, the relative response has a genuine quartic layer:

```text
Phi=h+Phi_2+Phi_4,
phi_W=[x_W]Phi_4=per(R_(Q,W)).                        (28)
```

The four-point convolution is therefore

```text
z_W+h m_W-sum_(e in E)z_e m_(W\e)=phi_W,             (29)
```

not zero.  Take `B=0`, `A=0`, and `R_(Q,W)=I_4`.  This legal response has

```text
h=0,       z_e=m_e=m_W=0,       z_W=phi_W=1.         (30)
```

It violates the `q=2` zero equation by one.  Thus partition closure at
`q=4` is insufficient for dual-Wick; one must also expose the quartic
permanental compound and prove its relevant value zero.

The two graphs in Section 4 also give a sharp `q=4` non-observability pair:
adjoin two new residual vertices joined only by an edge of weight one.  With
all four residuals present, that edge factors out and the response remains
exactly (25)--(27).  In particular it fixes every `q=4` root-budget layer
(`z_4,z_6`) while retaining the two different hidden pair families.

If a future jet legally deletes two of the four residual vertices and thereby
reduces to `q=2`, Theorem 1 applies again: the direct pair faces still exceed
the resulting five-probe budget.

## Scope wall

Proved:

- the exact residual/probe deletion budget (3);
- no directly partition-closed four-window at `q=2` or `q=4` in the current
  root-saturated cofactor mechanism;
- dominance and zero visible elimination ideal for the maximal granted
  `q=2` window plus all four marked-star observations;
- the exact additive-weight condition under which the four-point equation is
  nevertheless observable;
- a legal seven-port counterfamily with every budget-visible layer fixed;
- the quartic `q=4` defect and its identity-incidence counterexample.

Not proved:

- that the additive condition (16) holds on any target-compatible P7 shore;
- synchronization of the four marked stars with the clean top window;
- impossibility of a new mixed-colour, polarized, heralded, or nonlinear
  selector beyond the root-budget mechanism;
- a full coloured `P_7 -> Delta_3` restriction or obstruction;
- the Krenn--Gu conjecture.

All five missing statements remain **UNKNOWN/UNRESOLVED**.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_root_budget_dual_wick_observability_and_quartic_escape.py
python claims/p7/audit_p7_root_budget_dual_wick_observability_and_quartic_escape.py
python -m py_compile claims/p7/verify_p7_root_budget_dual_wick_observability_and_quartic_escape.py claims/p7/audit_p7_root_budget_dual_wick_observability_and_quartic_escape.py
uv run --with ruff ruff check claims/p7/verify_p7_root_budget_dual_wick_observability_and_quartic_escape.py claims/p7/audit_p7_root_budget_dual_wick_observability_and_quartic_escape.py
```

The primary verifier checks the budget, the exact Jacobian minor `360`, the
star kernel and conditional selector, both legal counterresponses, and the
quartic identity incidence symbolically.  The independent no-import audit
uses rational automatic differentiation, separate row reduction, direct
channel products, and a permanent recurrence.  No replay enumerates blocker
supports, colour words, graph families, or response subsets.
