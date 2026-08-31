# Four-root torus-star equal-leaf H4/Q6 a=0 physical-incidence exclusion (GLD105)

## Status and exact scope

**Proved exact scoped characteristic-zero parent composition (`GLD105`).**
The proof below composes four already proved exact results.  Juniper and
Mycelium accepted immutable pre-promotion commit `e3ee8629` from fresh
detached checkouts, giving the required `2/2` external consolidation.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

Work over `C` in the normalized, scale-fixed equal-leaf `H4` chart written in
the GLD88/F88 offset coordinates

```text
b = b88(p,q,a)+B_offset,
c = c88(p,q,a)+C_offset.
```

Put

```text
d0      = p+q-1,
P       = p^2-p+1,
L1      = p^2+2pq-2p-q,
L2      = 2pq-p+q^2-2q,
e       = 2pq^2-2pq-p-q^2-2q+2,
Delta   = (p-q)d0 P L1 L2 e,
H2deg   = 2p^2-2p+1.
```

Here `H2deg` is the leading-coefficient/degree-drop polynomial for `Q6`.
It is deliberately not called merely `H2` in this composition because GLD86
also labels the unrelated leaf-collision divisor `p-s` by that name.  On the
normalized H4 chart,

```text
p-s = L1/d0,
```

so that collision divisor is already nonzero on `D(Delta)`; it is not the
polynomial split below.

Let `B_incidence` denote the equal-leaf incidence equations, not the scalar
offset `B_offset`.  Let `C_center` be the vectorization of the physical
`3 x 3` center with scale-fixed coordinate `(C_center)_8=1`, not the scalar
offset `C_offset`.  Let `A` be the GLD86 center coefficient matrix and let
`M(G)` be the full fixed `37 x 9` GLD71 syndrome.

The theorem conclusion is exactly

```text
B_incidence intersect V(I_7(A)) intersect H4 intersect V(a,Q6)
  intersect D(Omega Delta) = empty                       (GLD105)
```

inside this one normalized F88-offset chart.  Equivalently, there is no
physical incidence point in the chart with `a=0`, `Q6=0`, `rank(A)<=6`, and
`Omega*Delta!=0`.

## 1. Exact incidence-to-syndrome bridge

The proved GLD75/GLD86 bridge gives, on the scale-fixed equal-leaf chart,

```text
B_incidence=0 iff M(G) C_center=0,
rank(A)=rank(M(G)[:,0:8]),
(C_center)_8=1.                                      (1)
```

At a point of `V(I_7(A))`, the first eight syndrome columns have rank at most
six.  The first identity and `(C_center)_8=1` express the ninth syndrome
column as a linear combination of those first eight columns.  Hence

```text
B_incidence=0 and rank(A)<=6 => rank(M(G))<=6.       (2)
```

Only this forward rank implication is used.  No selected-minor converse and
no converse from the syndrome rank to physical incidence is asserted.

## 2. Exhaustive H2deg case split

Every complex point lies in exactly one of the logical cases

```text
H2deg != 0  or  H2deg = 0.                           (3)
```

This split removes `H2deg` from the final open by combining two independent
proved routes; it does not cancel `H2deg` from an identity.

### 2.1 H2deg-open branch

Assume `H2deg!=0`.  From (2), the full syndrome has rank at most six.  The
proved GLD104 one-way rank corollary applies on

```text
V(a,Q6) intersect D(H2deg*Delta)
```

and forces

```text
B_offset=C_offset=0.                                (4)
```

Thus the leaf parameters equal the written GLD88/F88 formula at the same
`a,p,q`.  The proof now uses GLD95 with all of its qualifiers intact: GLD95
excludes

```text
B_incidence intersect V(I_7(A)) intersect F88 intersect V(Q6)
  intersect D(Omega Delta).
```

It does not say that `F88 intersect V(Q6)` is algebraically empty.  Rather,
its exact finite-minor cover makes at least one syndrome six-minor nonzero,
while the common block kernel forces every compatible physical center to be
singular; this contradicts `D(Omega)`.  The assumed physical incidence point
is therefore impossible on the `H2deg!=0` branch.

### 2.2 H2deg-zero branch

Assume `H2deg=0`.  GLD99 is an exact arbitrary-`a` theorem on the normalized
F88-offset chart.  It already combines its six-minor offset memberships with
the GLD75/GLD86 bridge and the direct GLD95 degree-drop endpoint to prove

```text
B_incidence intersect V(I_7(A)) intersect H4
  intersect V(H2deg,Q6) intersect D(Omega Delta) = empty.   (5)
```

Specializing that proved statement to `a=0` excludes the second case.  This
does not infer arbitrary-`a` GLD105 from the `a=0` theorem; it uses the wider
GLD99 leaf only in the `H2deg=0` branch.

Equations (3)--(5) exhaust the two cases and prove the displayed GLD105
statement.

## 3. Certificate and verification boundary

The composition certificate pins 19 upstream owner, verifier, independent
audit, review, evidence-test, and GLD75 carrier files by LF-normalized
SHA-256.  It also pins the accepted GLD104 promotion commit and its exact
promotion receipts.

The primary GLD105 checker verifies those pins, the accepted promotion gate,
the four upstream interface statements, the incidence/rank direction, the
`H2deg`/collision-divisor distinction, and the exhaustive two-case proof
topology.  It intentionally does not rerun the expensive algebra already
owned and independently audited by GLD86, GLD95, GLD99, and GLD104.

The independent GLD105 audit imports and executes no repository verifier.  It
has its own frozen pin manifest, reads the four theorem interfaces directly,
reconstructs `(p-s)d0=L1` with a separate integer-polynomial implementation,
and independently checks the branch truth table and status fences.

These scripts verify the composition seam and immutable dependencies.  The
mathematical force comes from the proved upstream implications and the direct
case argument above, not from string matching alone.

## 4. Nonclaims and retained obligations

GLD105 does not prove or assert:

- the six-selector proposition `P6`;
- any point on `Omega=0` or `Delta=0`;
- arbitrary `a` away from the already proved `H2deg=0` GLD99 branch;
- closure of the full `E31=0` wall;
- that arbitrary H4/Q6 points outside the written F88-offset chart enter this
  coordinate system;
- the GLD83 pulled-back Fitting ideal;
- another pivot, chart, gauge, component, or source branch;
- source integrability, target attachment, graph lifting, or global gluing;
- another root number or graph order; or
- a proof or refutation of the global Krenn--Gu conjecture.

The immutable candidate commit and tree were

```text
e3ee8629856a5d24ca18d2f1197ac11a3dc2c18e
f0b3d9f1ffdd92738ad20efc37b49a424ade76c7.
```

Commons request `kgc_01M1C11C0928AZS8DQ25B1Y8V8` received exact scoped
acceptances from Juniper (`kgc_01M1C12WAXQYFG2SPBT3ZMBYD1`) and Mycelium
(`kgc_01M1C17H0G9E9DY99JR24Y2HWH`).  These are external consolidation
receipts for this scoped theorem, not evidence for any wider or global
conclusion.  The global status remains **UNRESOLVED**.
