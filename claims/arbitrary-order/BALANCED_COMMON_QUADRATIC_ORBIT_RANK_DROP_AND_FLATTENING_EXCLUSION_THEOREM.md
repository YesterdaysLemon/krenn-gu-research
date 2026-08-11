# Balanced common-quadratic orbit: rank drop and flattening exclusion

## Status

**Exact arbitrary-order characteristic-zero exclusion of one substantial
stratum of the all-balanced rank-drop branch.**  Let `n=2m` and suppose that,
after an independent invertible change of basis at every vertex, every
physical edge block is one fixed symmetric bilinear form `q`.  Equivalently,
there are isomorphisms `A_u:L_u -> V`, with `dim V=3`, such that

```text
W_uv(x_u,x_v)=q(A_u x_u,A_v x_v)                    (1)
```

for every unordered pair `{u,v}`.

For `m>=4`, every balanced complete-deck sensor of (1) has rank at most

```text
binomial(m,2)+1 < 2^(m-1),                          (2)
```

so the entire vertex-gauge common-quadratic orbit lies in `B_all`.  If `q`
is nondegenerate, however, the `2 | (2m-2)` flattening of its graph tensor
has rank exactly six, while the ternary GHZ tensor has rank three.  If `q`
is degenerate, already a one-vertex flattening has rank below three.  Thus no
graph in this orbit is a Krenn--Gu witness for any `n>=6`.

This strictly enlarges the previously exhibited diagonal-complete point to
its full local-`GL(3)` common-form orbit and proves that this whole
synchronized part of `B_all` misses the witness equations.  It does **not**
prove that an arbitrary all-balanced rank-drop graph admits (1), and it does
not exclude the remaining nonsynchronized intersection.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. The common-quadratic orbit

Work over a characteristic-zero field `K`, and extend scalars to an
algebraic closure whenever convenient.  Matrix ranks do not change under
that extension.  Let `V` be three-dimensional, let

```text
q in Sym^2(V^*)                                      (3)
```

be one symmetric bilinear form, and let `A_u:L_u -> V` be an isomorphism at
every vertex.  Define the blocks by (1).  Write `H_(2m,q)` for the complete
graph tensor obtained when every local space is `V`, every `A_u` is the
identity, and every edge block is `q`.

Every perfect matching uses every vertex once.  Pullback therefore commutes
term by term with the perfect-matching sum:

```text
T_W=(tensor_u A_u^*) H_(2m,q).                       (4)
```

The tensor product in (4) is invertible.  Consequently every bipartite
flattening rank of `T_W` equals the corresponding flattening rank of
`H_(2m,q)`.

The same covariance applies to balanced sensors.  For a cut `R | N`, put
`y_u=A_u z_u` at every contracted vertex.  Pullback by the root maps `A_i^*`
is one common invertible row transformation on every companion column.
Since `product_(u in N) A_u` is an automorphism of the contraction space,
the pointwise sensor ranks for (1), as `z_N` varies, are exactly those for
the uniform graph `H_(2m,q)`, as `y_N` varies.  No target symmetry or
target-preserving change of basis is being asserted here; this is covariance
of the graph and sensor constructions only.

When `q` is nondegenerate, every edge block in (1) is invertible and the
support is complete.  The one-vertex flattening calculation below also shows
local concision.  Thus the orbit contains strong ambient graphs, not merely
degenerate examples.

## 2. Uniform all-cut sensor rank drop

Fix a balanced partition

```text
Omega=R disjoint-union N,        |R|=|N|=m.          (5)
```

Identify all root dual spaces with `V^*`.  For `z_u in V`, define

```text
Q(x)=q(x,x),        L_u(x)=q(x,z_u).                 (6)
```

For a parity-legal companion label `D subset N`, put `k=|D|`.  The companion
is invariant under every permutation of the root slots.  Characteristic-zero
polarization therefore identifies it with its repeated-root polynomial.
Counting the cross-root choices, their bijections, and the internal root
matchings gives

```text
G_D(x,...,x)
 = a_(m,k) Q(x)^((m-k)/2) product_(u in D) L_u(x),   (7)

a_(m,k)=binomial(m,k) k! (m-k-1)!! !=0.             (8)
```

There is exactly one all-cross column, `D=N`.  Every other legal column has
`m-k>=2`, so (7) places it in

```text
Q Sym^(m-2)(V^*).                                   (9)
```

If `Q` is nonzero, multiplication by it is injective in the symmetric
algebra, and the space in (9) has dimension `binomial(m,2)`.  If `Q=0`, the
non-all-cross columns vanish, so the same upper bound is automatic.  Adding
the one all-cross column proves

```text
rank Gamma_R(z_N) <= binomial(m,2)+1                 (10)
```

for every cut and every contraction point.  At `m=4`, the right side is
seven while the sensor has eight columns.  The difference

```text
2^(m-1)-binomial(m,2)-1                              (11)
```

is positive at `m=4` and increases by `2^(m-1)-m>0`.  Hence (2) holds for
every `m>=4`.  Covariance from Section 1 transfers it to every graph (1),
proving membership in `B_all`.

At `m=3`, (10) equals the four-column count and does not force rank drop.
The theorem makes no hidden six-vertex all-rank-drop claim.

## 3. The nondegenerate orbit has two-flattening rank six

Assume now that `q` is nondegenerate.  After scalar extension and one common
change of basis, take

```text
q(x,y)=x_0 y_0+x_1 y_1+x_2 y_2.                     (12)
```

For a coordinate word `alpha` on the `2m` vertices, let `n_c` be its number
of occurrences of colour `c`.  Direct matching separation by colour gives

```text
[alpha]H_(2m,q)=0                         if some n_c is odd,
[alpha]H_(2m,q)=product_c (n_c-1)!!       otherwise. (13)
```

Consider the flattening with vertices `1,2` on the left and the remaining
`2m-2` vertices on the right.  Symmetry under exchange of the first two
vertices puts its left image inside `Sym^2(V^*)`, so its rank is at most six.
We now exhibit six independent columns.

For each colour `c`, make every right vertex colour `c`.  The corresponding
left column is diagonal.  Its `(c,c)` entry is `(2m-1)!!`, while each other
diagonal entry is `(2m-3)!!`.  In the diagonal basis the three such columns
form the matrix with diagonal

```text
A=(2m-1)!!
```

and off-diagonal

```text
B=(2m-3)!!.
```

Its eigenvalues are

```text
A-B=(2m-2)B,          A+2B=(2m+1)B,                 (14)
```

which are nonzero in characteristic zero.  The three diagonal directions
are therefore in the image.

For each unordered colour pair `{a,b}`, let `c` be the remaining colour and
choose a right word with one `a`, one `b`, and all other right vertices
colour `c`.  Formula (13) makes the only nonzero left entries `(a,b)` and
`(b,a)`, both with coefficient `(2m-5)!!`.  These three columns give the
three off-diagonal symmetric directions.  Together with the diagonal
columns they span `Sym^2(V^*)`, proving

```text
rank Flat_(2 | 2m-2)(H_(2m,q))=6.                   (15)
```

This argument works already for `m>=2`; in the Krenn--Gu range `m>=3` all
displayed right words are available.

## 4. Flattening mismatch with GHZ

The ternary diagonal tensor is

```text
Delta_3=sum_(c=0)^2 e_c^(tensor 2m).                 (16)
```

Across any nontrivial bipartition its flattening is a sum of three rank-one
maps whose left and right pure coordinate tensors are separately linearly
independent.  Hence

```text
rank Flat_(2 | 2m-2)(Delta_3)=3.                     (17)
```

Equations (4), (15), and (17) rule out `T_W=Delta_3` whenever `q` is
nondegenerate.

If instead `rank(q)<3`, every covector occurring at one fixed vertex of
`H_(2m,q)` lies in the first-factor image of `q`, a space of dimension
`rank(q)`.  Therefore

```text
rank Flat_(1 | 2m-1)(H_(2m,q)) <= rank(q) < 3,       (18)
```

whereas the corresponding GHZ flattening has rank three.  This excludes the
degenerate cases as well.  The zero form is included.

The obstruction is invariant under all independent local isomorphisms in
(1).  It is not based on choosing a target-preserving gauge, on positivity,
or on sampling a contraction point.

## 5. Exact proof-topology consequence

The all-balanced branch now contains a rigorously excluded synchronized
stratum:

```text
vertex-gauge common-quadratic orbit lies in B_all:   PROVED for n>=8;
nondegenerate orbit has every edge invertible:       PROVED;
nondegenerate orbit two-flattening rank:              EXACTLY 6;
ternary GHZ two-flattening rank:                      EXACTLY 3;
common-quadratic orbit meets witness equations:       EMPTY for n>=6;
every graph in B_all has common-quadratic form:        NOT CLAIMED;
nonsynchronized B_all witness intersection:           UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.          (19)
```

The diagonal-complete family is the specialization `A_u=id` and
`q=lambda I_3`.  Its explicit mixed coefficient remains the sharp witness
showing that pure normalization and local ambient regularity do not force a
full sensor.  The present theorem adds a different conclusion: no independent
local change of basis can turn any common-quadratic graph into GHZ, because
flattening rank is invariant.

The subsequent
[`common-quadric mixed-permanent theorem`](BALANCED_COMMON_QUADRIC_MIXED_PERMANENT_DIVISIBILITY_AND_CONFORMAL_SHORE_EXCLUSION_THEOREM.md)
strictly enlarges the excluded physical stratum.  It needs the common quadric
only on one balanced root shore, allows arbitrary blocks internal to the
nonroot half and arbitrary root/cross edge scalars, and excludes the
entire physical common-conformal shore: a nonzero cross-scalar permanent
fails a mixed word, while a zero permanent fails a constant-colour pure
residue.  General nonseparable simultaneous residue branches remain open.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_common_quadratic_orbit_rank_drop_and_flattening_exclusion.py
python claims/arbitrary-order/audit_balanced_common_quadratic_orbit_rank_drop_and_flattening_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_common_quadratic_orbit_rank_drop_and_flattening_exclusion.py claims/arbitrary-order/audit_balanced_common_quadratic_orbit_rank_drop_and_flattening_exclusion.py
uv run --with ruff ruff check claims/arbitrary-order/verify_balanced_common_quadratic_orbit_rank_drop_and_flattening_exclusion.py claims/arbitrary-order/audit_balanced_common_quadratic_orbit_rank_drop_and_flattening_exclusion.py
```

The primary verifier constructs the exact coordinate tensor, checks the
one- and two-vertex flattening ranks and the six displayed columns, and
checks the balanced symmetric-companion ranks through bounded orders.  The
independent no-import audit uses a separately written matching recursion,
fraction-free sparse row reduction, and a different companion-polynomial
representation.  These calculations audit constants and conventions.  The
arbitrary-order proof is (4), the matching count (7), polarization, the
six-column flattening certificate, and rank invariance.
