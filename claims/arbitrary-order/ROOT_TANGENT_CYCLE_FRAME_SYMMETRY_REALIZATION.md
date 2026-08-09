# Root-tangent quotient frames survive edge-block symmetry

## Status

**Exact characteristic-zero first-jet realization.**  The quotient-frame
condition in
[`ROOT_TANGENT_COMPANION_NECESSITY_FOR_COORDINATE_SLICE.md`](ROOT_TANGENT_COMPANION_NECESSITY_FOR_COORDINATE_SLICE.md)
does not become contradictory merely because a root--root edge is one
undirected bilinear block and its companion cofactor class is shared by its
two endpoints.

For every `r>=3`, every collection of fully supported roots `x_i`, and every
collection of quotient isomorphisms

```text
F_i: V/<x_i> -> Diag/<Lambda>,
```

there is an `r`-cycle of formal root--root companions with the following
properties:

1. every edge has one cofactor class used at both endpoints;
2. the two incident classes form a basis of `Diag/<Lambda>` at every root;
3. the two endpoint covectors of every edge come from one bilinear edge
   block, with the reverse orientation given by transpose;
4. the sum of the two incident companion terms is exactly `F_i` at every
   root.

Thus any genuine next obstruction must use realizability of the proposed
cofactor classes by complementary hafnians, second or higher derivatives,
or additional global incidence.  This construction is not a graph witness
and does not resolve the Krenn--Gu conjecture.  No finite field is used.

## A cycle of shared quotient classes

Write the two-dimensional quotient `Diag/<Lambda>` as `Q=K^2`.  Number the
roots modulo `r` and put on the cycle edge

```text
e_i={i,i+1}
```

the shared class

```text
q_i=(1,t_i),
```

where the `t_i` are pairwise distinct.  At root `i`, the incident classes
`q_(i-1),q_i` form a basis because

```text
det [q_(i-1) q_i]=t_i-t_(i-1) != 0.                 (1)
```

Consequently there are unique covectors `a_i^-` and `a_i^+` such that

```text
F_i(y)=a_i^-(y) q_(i-1)+a_i^+(y) q_i.              (2)
```

Since `F_i(x_i)=0`, independence in (1) gives

```text
a_i^-(x_i)=a_i^+(x_i)=0.                           (3)
```

Because `F_i` is an isomorphism on `V/<x_i>`, the two covectors in (2) span
the whole annihilator `x_i^perp`.

For the GHZ derivative, one may take quotient coordinates

```text
pi = [ d_1  -d_0   0  ]
     [ d_2    0  -d_0 ],

F_i=pi diag(d_0/x_i0,d_1/x_i1,d_2/x_i2).           (4)
```

Then `pi(d_0,d_1,d_2)^T=0`, so (4) is exactly the induced derivative
`V/<x_i> -> Diag/<Lambda>`.

## One symmetric edge block realizes both endpoint covectors

Choose a covector `u_i` with `u_i(x_i)=1`.  On the oriented representative
`e_i=(i,i+1)`, let

```text
a=a_i^+,
b=a_(i+1)^-,
M_i=a u_(i+1)^T + u_i b^T.                         (5)
```

The edge bilinear form is `B_i(y,z)=y^T M_i z`; reversing the edge uses
`M_i^T`.  Equations (3) and (5) give

```text
M_i x_(i+1)=a,
M_i^T x_i=b,
x_i^T M_i x_(i+1)=0.                               (6)
```

Hence one legal bilinear block simultaneously realizes the required
companion covector at both ends and preserves the pairwise-zero base
incidence.  Summing the two incident edge terms at root `i` gives (2), so
all quotient frames are realized at once.

## Boundary

The classes `q_i` are formal prescribed complementary-cofactor classes.
The proof does **not** construct blocker--blocker edges whose complementary
hafnians equal chosen lifts of those classes.  It also does not match scalar
multiples of `Lambda`, unspecialized tensors away from the first jet, or
mixed second derivatives.  In particular:

```text
transpose/shared-class first-jet obstruction: NO;
formal simultaneous quotient frames for r>=3: REALIZED;
complementary-hafnian realizability: UNKNOWN;
second-order compatibility: UNKNOWN;
full arbitrary-order local-to-global reduction: UNKNOWN;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_root_tangent_cycle_frame_symmetry_realization.py
python audit_root_tangent_cycle_frame_symmetry_realization.py
```

The primary checks the generic quotient-coordinate formulas symbolically
and exact cycles of lengths three through nine.  The no-import audit uses an
independent rational implementation and checks lengths three through
twelve.
