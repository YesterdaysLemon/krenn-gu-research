# The two-endpoint full-jet cofactor frame is sharp at every root count

## Status

**Exact arbitrary-order characteristic-zero sharpness theorem and proof-route
no-go.**  For every `r>=2`, put `m=r+2`.  There is a legal loopless symmetric
three-colour graph on

```text
R={r_0,...,r_(r-1)},   B={b_0,...,b_(m-1)},   Q={q_0,q_1}                 (1)
```

with fully supported pairwise-zero root vectors, exactly the two effective
nonblocker endpoints in `Q`, and projectively constant root--blocker first
derivatives, such that the following all hold.

1. Every root's rows across the complete blocker union span `(C^3)^*`.
2. On the common tangent plane `S=ker(e_2^*)`, the derivative taken once at
   every root is exactly

   ```text
   (tensor_i e_0^*|S) tensor e_0^(tensor m)
   +(tensor_i e_1^*|S) tensor e_1^(tensor m).          (2)
   ```

3. The two parity-allowed complementary hafnian cofactors are the two pure
   diagonal tensors in (2).  They are independent and attain equality in the
   two-class bound of
   [`ROOT_FINITE_ENDPOINT_FULL_JET_COFACTOR_SPAN_BOUND.md`](ROOT_FINITE_ENDPOINT_FULL_JET_COFACTOR_SPAN_BOUND.md).
4. The effective companion graph has a matching saturating every root subset,
   so it also meets the topology condition in
   [`ROOT_RESTRICTED_JET_COMPANION_MATCHING_SATURATION_NECESSITY.md`](ROOT_RESTRICTED_JET_COMPANION_MATCHING_SATURATION_NECESSITY.md).

Thus the axis branch surviving the two-endpoint cofactor-span theorem cannot
be eliminated from the full-root jet, the shared principal-cofactor frame,
pairwise-zero incidence, projective constancy, full root-row span, or
companion matching saturation alone.  The actual cofactor-valued lower mixed
jets or another global compatibility condition are essential.

This graph is **not** a Krenn--Gu counterexample.  It realizes only the
displayed restricted full-root derivative and the necessary support topology,
not the cofactor-valued lower jets or the unspecialized GHZ identity.  The
arbitrary-order local-to-global reduction and the global Krenn--Gu conjecture
remain **UNRESOLVED**.  No finite field is used.

## Legal edge blocks

Work over a characteristic-zero field.  Set

```text
x_i=z_0=z_1=(1,1,1),
c=2,  p=0,  q=1,
a=e_2^*,
phi_p=e_0^*-e_2^*,  phi_q=e_1^*-e_2^*,
S=ker(a).                                               (3)
```

Every unspecified edge block is zero.  An expression `alpha tensor beta` on
an unordered edge means that the reverse orientation carries its transpose,
so all blocks define one legal symmetric loopless graph.

For every root `r_i` and blocker `b_u`, put

```text
B_(r_i,b_u)=a tensor e_((i+u) mod 3)^*.                (4)
```

Then

```text
B_(r_i,b_u)(x_i,-)=e_((i+u) mod 3)^*,
B_(r_i,b_u)(y,-)=a(y)e_((i+u) mod 3)^*.                (5)
```

Hence the root--blocker derivatives are projectively constant and vanish on
`S`.  Because `m>=4`, the rows in (5) span all three coordinate covectors for
every root.  Every `b_u` belongs to the blocker union.  The root--endpoint
blocks below contain `phi_p` or `phi_q` on the root side and `e_2^*` on the
endpoint side.  Since `phi_p(x_i)=phi_q(x_i)=0`, both `q_j` have the full
space as simultaneous kernel and are nonblockers.  The root--root blocks used
in the full-root matching of colour `p` are

```text
phi_p tensor phi_p+phi_p tensor a+a tensor phi_p,     (6)
```

while the other root--root blocks are `phi_q tensor phi_q`.  Every displayed
block vanishes at `(x_i,x_j)`, so the roots are pairwise zero-coupled.  On
`S tensor S`, the two terms containing `a` in (6) vanish, and the first term
is the required pure `p` tangent edge.  If only one endpoint of such an edge
is differentiated and the other is fixed at `x`, however, (6) evaluates to
`phi_p`.  This one-tangent stabilization supplies every lower-subset
saturating matching without changing the full-root jet.

On `S` and at the fixed endpoint vectors, these blocks reduce exactly to

```text
phi_p|S=e_0^*|S,   phi_q|S=e_1^*|S,   e_2^*(z_j)=1.   (7)
```

It remains to give the parity-dependent sparse companion graph.

## Odd number of roots

Suppose `r` is odd.  On the root path, label the edge
`r_i r_(i+1)` by `q` for even `i` and by `p` for odd `i`.  A root-path edge
labelled `q` carries `phi_q tensor phi_q`, while a `p` edge carries the
stabilized block (6).  Add

```text
q_0--r_0       labelled p,
q_1--r_(r-1)   labelled q.                            (7)
```

Here a root--endpoint edge labelled `k` carries
`phi_k tensor e_2^*`.

On the blocker path, label `b_u b_(u+1)` by `q` for even `u` and by `p` for
odd `u`.  A blocker-path edge labelled `k` carries
`e_k^* tensor e_k^*`.  Add

```text
q_1--b_0       labelled p,
q_0--b_(m-1)   labelled q,                            (8)
```

where the endpoint side is `e_2^*` and the blocker side is `e_k^*`.

After all roots are restricted to `S`, every root--blocker edge vanishes.
The remaining graph has exactly two perfect matchings.  In the first,
`q_0` uses `r_0`, `q_1` uses `b_0`, and both remaining paths take their
odd-indexed edges; every variable endpoint has colour `p`.  In the second,
`q_1` uses `r_(r-1)`, `q_0` uses `b_(m-1)`, and both paths take their
even-indexed edges; every variable endpoint has colour `q`.  The two other
ways of assigning `q_0,q_1` to the root and blocker sectors leave odd paths
and have no perfect matching.

The endpoint subset used by roots is respectively `{q_0}` and `{q_1}`.
Thus the two complementary cofactors are

```text
C_(R union {q_0})=e_0^(tensor m),
C_(R union {q_1})=e_1^(tensor m).                     (9)
```

The corresponding scalar root forms are the two factors in (2).

## Even number of roots

Suppose `r` is even.  Label the root-path edge `r_i r_(i+1)` by `p` for even
`i` and by `q` for odd `i`; again the `p` edges carry (6) and the `q` edges
carry `phi_q tensor phi_q`.  Add

```text
q_0--r_0       labelled q,
q_1--r_(r-1)   labelled q.                           (10)
```

Label the blocker-path edge `b_u b_(u+1)` by `q` for even `u` and by `p` for
odd `u`, and add

```text
q_0--b_0       labelled p,
q_1--b_(m-1)   labelled p.                           (11)
```

There are again exactly two restricted perfect matchings.  One uses no
root--endpoint edge: the roots take the even `p` edges, both endpoints pair
to the ends of the blocker path, and the blocker interior takes its odd `p`
edges.  The other uses both root--endpoint edges: the root interior takes its
odd `q` edges and the blockers take their even `q` edges.  A matching using
exactly one root--endpoint edge would leave odd vertex counts in both
disconnected sectors.

The root-used endpoint subsets are now `emptyset` and `{q_0,q_1}`, so

```text
C_R=e_0^(tensor m),
C_(R union {q_0,q_1})=e_1^(tensor m).                (12)
```

Equations (9) and (12) are precisely the two parity cases in the committed
cofactor-span theorem.

## Why the target jet agrees

Differentiate the three-colour GHZ tensor once at every root, keep the
blocker modes free, and fix both endpoints at `(1,1,1)`.  Its restriction to
`S^(tensor r)` is

```text
sum_(k=0)^2 (tensor_i e_k^*|S) tensor e_k^(tensor m).
```

The `k=2` term is zero because `e_2^*|S=0`; the remaining two terms are (2).
The perfect-matching classification above gives the same two terms, each
with coefficient one.  This proves the exact full-jet identity and the
independence of both the scalar row forms and the complementary cofactor
columns.

The construction is also compatible with the first-jet covector count: at
every root, its two incident root/root-or-endpoint companion covectors are
`phi_p,phi_q`, which span `x_i^perp`; together with `a` they span the full
dual.  This is only a covector-span statement, not the missing cofactor-valued
first-jet identity.

## Every root subset is matching-saturated

The colour-`p` root edges in the construction form one fixed matching `M_p`
that saturates all roots.  For odd `r`, it consists of `q_0--r_0` and the
odd-indexed root-path edges.  For even `r`, it consists of the even-indexed
root-path edges.

Let `I subset R`.  Process every edge of `M_p` independently.

- If both root endpoints lie in `I`, use its nonzero tangent--tangent
  restriction `phi_p tensor phi_p`.
- If exactly one lies in `I`, use its nonzero one-tangent contraction
  `phi_p` against the fixed vector `x` at the other root.
- If neither lies in `I`, omit it.
- In the odd case, use `q_0--r_0` exactly when `r_0 in I`.

The chosen edges are vertex-disjoint because `M_p` is a matching, and they
saturate every root of `I`.  Hence every subset, not merely every
axis-deficient subset, passes the exact matching-saturation necessity.

This still does not check the complementary hafnian carried by those lower
mixed derivatives, its mixed-colour cancellations, or equality with the GHZ
coefficient forms.  The construction is therefore a no-go for support-only
and full-root-frame arguments, not a global realization.

## Explicit non-global boundary

The construction already fails the undifferentiated root slice, so there is
no hidden counterexample claim.  Fix all roots at `x_i` and both endpoints at
`(1,1,1)`.  Every root--root and root--endpoint edge then evaluates to zero.
Both endpoints have a unique blocker neighbour and are forced to use it.  The
`r` roots biject with the remaining blocker indices `u=1,...,r` through the
coordinate rows in (4).

Choose the interior blocker colour at `u=i+1` to be `(i+u) mod 3`.  The
identity root--blocker bijection contributes one.  Every other contribution
to this coefficient is also zero or one, so the coefficient is a positive
integer in characteristic zero.  For odd `r`, the two endpoint blockers have
colours `p,q`; for even `r` they both have colour `p`, while the first
interior blocker has colour `q`.  In either parity the displayed blocker word
is nonconstant.  Its nonzero coefficient contradicts the diagonal GHZ slice.

Thus the same exact graph proves both sides of the boundary: it realizes all
claimed full-root and support data, and it is provably not an unspecialized
GHZ witness.

Consequently the exact conclusion is

```text
two-endpoint full-root cofactor bound: SHARP;
two-class diagonal frame in legal symmetric blocks: REALIZED;
pairwise-zero roots and full blocker-row spans: COMPATIBLE;
every root subset companion-matching saturated: YES;
cofactor-valued lower mixed jets: NOT CLAIMED;
undifferentiated GHZ root slice: EXPLICITLY FAILS;
global Krenn--Gu conjecture: UNRESOLVED.                (13)
```

## Replay

```powershell
uv run --with sympy python verify_root_arbitrary_order_two_endpoint_full_jet_frame_sharpness_nogo.py
python audit_root_arbitrary_order_two_endpoint_full_jet_frame_sharpness_nogo.py
uv run --with sympy --with ruff python -m ruff check verify_root_arbitrary_order_two_endpoint_full_jet_frame_sharpness_nogo.py audit_root_arbitrary_order_two_endpoint_full_jet_frame_sharpness_nogo.py
python -m py_compile verify_root_arbitrary_order_two_endpoint_full_jet_frame_sharpness_nogo.py audit_root_arbitrary_order_two_endpoint_full_jet_frame_sharpness_nogo.py
```

The primary constructs the actual integer `3 x 3` edge blocks, verifies every
incidence and span assertion, recursively enumerates the restricted perfect
matchings for both parities through twelve roots, and checks every root subset
against the fixed saturating matching.  The no-import audit uses a different
integer coordinate permutation, independent rational rank reduction, a
separate bitmask matching recurrence through sixteen roots, and an independent
subset-saturation ledger.  Both also reconstruct the positive mixed
undifferentiated coefficient.  These bounded enumerations audit the indexing;
the two alternating-path, fixed-matching, and positive-permanent proofs above
establish every `r>=2` in characteristic zero.
