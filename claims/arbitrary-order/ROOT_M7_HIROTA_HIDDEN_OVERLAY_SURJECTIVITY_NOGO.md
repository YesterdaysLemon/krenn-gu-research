# Root `m=7` Hirota hidden-overlay surjectivity no-go

## Status

This is an exact characteristic-zero proof-route no-go.  The six hidden
classes in the smallest four-terminal hafnian overlay are algebraically
independent even when they come from one common symmetric weighted graph.
Indeed, their common-weight map is surjective already with a four-vertex
core, and remains so after embedding into the actual eight-vertex
root-`m=7` core.

Therefore neither a linear nor a nonlinear universal
principal-hafnian/common-weight identity among those six classes can close
the active cell.  The next obstruction must use additional coloured,
blocker-incidence, root-row/permanent, or GHZ information.  This is not a
Krenn--Gu witness or a global proof.

## Four-terminal overlay

Let `S={s_0,s_1,s_2,s_3}` be the common core and let the terminals be
`T={1,2,3,4}`.  For even `X`, write

```text
H_X=haf(W[X]).
```

Define the four visible matching-pair products

```text
f_0=H_(S1234) H_S,
f_1=H_(S12) H_(S34),
f_2=H_(S13) H_(S24),
f_3=H_(S14) H_(S23).                                  (1)
```

Expand each product as ordered pairs of perfect matchings.  For
`0<=i<j<=3`, let `x_ij` be the matching-pair class common to `f_i` and
`f_j`, with its weight and multiplicity.  The standard overlay partition
gives

```text
f_0=x_01+x_02+x_03,     f_1=x_01+x_12+x_13,
f_2=x_02+x_12+x_23,     f_3=x_03+x_13+x_23.            (2)
```

The prior route-boundary theorem observed that the `4 x 6` incidence map
in (2) has rank four.  That left open the possibility of nonlinear
common-weight equations among the `x_ij`.  The construction below proves
that no such universal equations exist.

## A six-parameter common graph

Use the fixed nonzero weights

```text
W_(s0,s3)=-1, W_(s1,s2)=1,
W_(s0,1)=1, W_(s0,2)=-1, W_(s0,4)=-1, W_(s3,3)=-1,
```

and the variable weights

```text
a=W_(s3,1), b=W_(s3,2), c=W_(s3,4),
d=W_(1,2),  e=W_(1,4),  f=W_(2,4).                    (3)
```

All other weights are zero, with transpose entries supplied by symmetry.
Let `C={s0s3,s1s2}` be the unique core matching.

Every hidden class has one surviving matching-pair monomial.  Listing its
appearance first in `f_i` and then in `f_j` gives:

```text
x_01=-d:
  ({s0-4,s1-s2,s3-3,1-2}, C),
  ({s0-s3,s1-s2,1-2}, {s0-4,s1-s2,s3-3});

x_02= f:
  ({s0-1,s1-s2,s3-3,2-4}, C),
  ({s0-1,s1-s2,s3-3}, {s0-s3,s1-s2,2-4});

x_03=-e:
  ({s0-2,s1-s2,s3-3,1-4}, C),
  ({s0-s3,s1-s2,1-4}, {s0-2,s1-s2,s3-3});

x_12= b:
  ({s0-1,s1-s2,s3-2}, {s0-4,s1-s2,s3-3}),
  ({s0-1,s1-s2,s3-3}, {s0-4,s1-s2,s3-2});

x_13=-a:
  ({s0-2,s1-s2,s3-1}, {s0-4,s1-s2,s3-3}),
  ({s0-4,s1-s2,s3-1}, {s0-2,s1-s2,s3-3});

x_23= c:
  ({s0-1,s1-s2,s3-3}, {s0-2,s1-s2,s3-4}),
  ({s0-1,s1-s2,s3-4}, {s0-2,s1-s2,s3-3}).            (4)
```

The signs are the products of the displayed fixed edges.  Hence, exactly
and not merely to first order,

```text
(x_01,x_02,x_03,x_12,x_13,x_23)=(-d,f,-e,b,-a,c).     (5)
```

The visible products are correspondingly

```text
f_0=-d-e+f,       f_1=-a+b-d,
f_2= b+c+f,       f_3=-a+c-e,                         (6)
```

which are precisely (2).

## Surjectivity theorem

Over any field, prescribe arbitrary values for the six hidden classes and
set

```text
d=-x_01, f=x_02, e=-x_03,
b=x_12,  a=-x_13, c=x_23.                             (7)
```

Equations (3)--(5) realize them in one symmetric weighted graph.  The
six-by-six Jacobian is a signed permutation matrix with determinant one.
Therefore the image contains the entire affine six-space and

```text
the universal elimination ideal in K[x_01,...,x_23] is zero.  (8)
```

In characteristic not two, the incidence map (2) is surjective as well, so
there is no universal polynomial equation among the four visible `f_i`
either.

## Embedding into the actual core

The active `m=7` overlay has common core `B union {q_1}` of size eight.
Adjoin four new core vertices joined only as two isolated unit-weight
edges.  Every hafnian appearing in (1) must use those two edges and hence
factors by one.  All six hidden classes and all four visible products are
unchanged.  Thus (8) holds verbatim at the actual core cardinality.

This embedding concerns scalar principal hafnians.  It does not respect or
claim the coloured blocker ledger, the root-row `P_7` equations, or the GHZ
mixed-word vanishings.  Those additional structures are exactly what a
future obstruction must use.

## Verification

Run:

```text
uv run --with sympy python claims/arbitrary-order/verify_root_m7_hirota_hidden_overlay_surjectivity_nogo.py
python claims/arbitrary-order/audit_root_m7_hirota_hidden_overlay_surjectivity_nogo.py
```

The primary verifier expands the four sparse hafnian products after the
fixed weights are specialized, reconstructs their six pairwise monomial
classes, checks the signed-permutation Jacobian, and adds the isolated unit
edges.  The displayed matching-pair list (4), rather than that
specialization, certifies equality of the full edge multisets and excludes
accidental monomial collisions.  The independent no-import audit uses
exponent labels and integer coefficients.  The recursion is confined to
this fixed sparse graph; it is a proof audit, not a support search.

## Boundary

```text
abstract hidden incidence map:              SURJECTIVE;
one-graph common-weight hidden map:         SURJECTIVE;
universal hidden-class elimination ideal:   ZERO;
visible map in characteristic not two:      SURJECTIVE;
coloured/root-row/GHZ compatibility:        NOT MODELED;
arbitrary P_7 restriction:                  UNKNOWN;
global Krenn-Gu conjecture:                 UNRESOLVED.
```
