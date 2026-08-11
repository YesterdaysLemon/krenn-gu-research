# Balanced all-rank-drop diagonal-complete sharpness theorem

## Status

**Exact arbitrary-order characteristic-zero boundary for the all-balanced
rank-drop branch.**  Let `n=2m>=8`, take ternary local spaces, and put the
same nonzero scalar multiple of the `3 x 3` identity on every physical edge.
The scalar can be chosen so that all three monochromatic coefficients are
exactly one.  This complete block graph has:

- an invertible physical block on every edge;
- complete connected support;
- local concision at every vertex; and
- the three normalized pure GHZ coefficients.

Nevertheless, for **every** balanced partition, its complete-deck sensor has
rank at most

```text
binomial(m,2)+1 < 2^(m-1),                           (1)
```

so the graph lies in the all-balanced rank-drop locus `B_all`.

The graph is not a Krenn--Gu witness: every word whose three colour classes
have even size has a nonzero coefficient.  Thus local concision, complete
support, block invertibility, and the pure target coefficients cannot exclude
`B_all`; any exclusion on the witness locus must use mixed-word vanishing or
an exact consequence of those equations.  The theorem does not show that
`B_all` meets the witness locus.  The global conjecture remains
**UNRESOLVED**.

## 1. The diagonal-complete family

Work over `C`.  Let `V=C^3` with coordinate covectors `e_0^*,e_1^*,e_2^*`.
For every unordered vertex pair `{u,v}`, set

```text
W_uv=lambda q,
q=sum_(c=0)^2 e_(u,c)^* tensor e_(v,c)^*,           (2)
```

where `lambda!=0` will be normalized below.  Thus every edge block is
`lambda I_3` in the coordinate bases.

For a colour word `alpha` on the `2m` vertices, write

```text
n_c=#{u:alpha(u)=c}.                                 (3)
```

### Theorem 1 (complete coefficient formula)

The graph coefficient of `alpha` is zero if some `n_c` is odd.  If all three
counts are even, then

```text
[alpha]T_W
 =lambda^m product_(c=0)^2 (n_c-1)!!,                (4)
```

with `(-1)!!=1`.

### Proof

An entry of (2) is nonzero exactly when the colours at its two endpoints
agree.  Hence a contributing perfect matching is the disjoint union of one
perfect matching inside each colour class.  Such matchings exist exactly when
every `n_c` is even, and their number is the product of the three double
factorials in (4).  Every complete matching uses `m` edges, each of weight
`lambda`, proving the formula.

Choose an `m`th root

```text
lambda^m=1/(2m-1)!!.                                 (5)
```

Then the three all-colour-`c` words have coefficient one.  On the mixed word
with colour counts `(2,2m-2,0)`, however, (4)--(5) give

```text
[alpha]T_W
 =(2m-3)!!/(2m-1)!!
 =1/(2m-1) !=0.                                     (6)
```

Thus the pure coefficients are normalized but the required mixed zero is
violated exactly.

## 2. Local concision and strong ambient regularity

Every block (2) is invertible and every edge is present, so the physical
support is the complete connected graph.

Fix a vertex `v`.  For each colour `c`, set every other vertex to colour `c`
and leave the slot at `v` open.  The `c` component of the resulting covector
is the normalized pure coefficient one.  A component `d!=c` has two odd
colour classes, of sizes `2m-1` and one, and vanishes by Theorem 1.  The three
resulting covectors are therefore

```text
e_0^*, e_1^*, e_2^*.                                (7)
```

They span `V^*`, proving local concision at every vertex.  This is a property
of the full graph tensor, not merely of its edge blocks.

## 3. Every balanced sensor drops rank

Fix any balanced partition

```text
Omega=R disjoint-union N,       |R|=|N|=m.           (8)
```

Identify the root dual spaces using their common coordinate bases.  For
`z_u in V`, `u in N`, put

```text
L_u(x)=q(x,z_u),       Q(x)=q(x,x).                  (9)
```

The balanced sensor column `G_D`, where `|D|` has the parity of `m`, is
invariant under every permutation of the root slots.  Hence it is a symmetric
`m`-tensor.  In characteristic zero, diagonal evaluation identifies such
tensors with homogeneous degree-`m` polynomials.

### Theorem 2 (symmetric companion formula)

For `k=|D|`, diagonal evaluation of the companion is

```text
G_D(x,...,x)
 =a_(m,k) lambda^((m+k)/2)
    Q(x)^((m-k)/2) product_(u in D) L_u(x),           (10)

a_(m,k)=binomial(m,k) k! (m-k-1)!! !=0.              (11)
```

The exponent of `lambda` counts the `(m-k)/2` internal root edges and the
`k` cross edges.

### Proof

Choose the `k` roots used across the cut, biject them with `D`, and perfectly
match the remaining `m-k` roots.  On the repeated root vector `x`, every
choice contributes the same product in (10).  The numbers of choices are,
respectively,

```text
binomial(m,k),       k!,       (m-k-1)!!.            (12)
```

Their product is (11).  Parity makes `m-k` even, and characteristic zero
keeps the displayed integer nonzero.  This proves (10).

### Theorem 3 (uniform all-cut rank bound)

For every choice of `z_N`,

```text
rank Gamma_R(z_N) <= binomial(m,2)+1.                (13)
```

Consequently the sensor is identically column-rank-deficient for every
balanced cut when `m>=4`.

### Proof

There is one all-cross column, namely `D=N`.  Every other legal `D` has
`m-k>=2`.  Formula (10) shows that its symmetric polynomial is divisible by
the fixed nonzero quadratic `Q(x)`.  Therefore all non-all-cross columns lie
in

```text
Q Sym^(m-2)(V^*),                                   (14)
```

whose dimension is

```text
dim Sym^(m-2)(C^3)^*=binomial(m,2).                  (15)
```

Multiplication by `Q` is injective in the polynomial ring, so (15) is exact
for the ambient subspace.  Adding the single all-cross column proves (13).
The sensor has `2^(m-1)` columns.  At `m=4`,

```text
binomial(4,2)+1=7<8.                                (16)
```

If the strict inequality holds at `m>=4`, its difference at `m+1` increases
by `2^(m-1)-m>0`.  Hence it holds for every `m>=4`.  The partition (8) and
the vectors `z_N` were arbitrary, proving membership in `B_all`.

## 4. The exact low-order threshold

At `m=3`, the bound (13) equals the four-column count.  It does not force
rank drop.  Indeed, choose `z_N` so that the three linear forms `L_u` form a
basis of `V^*`.  The three one-cross columns are the independent cubics

```text
Q L_u,                                               (17)
```

and the all-cross column is `L_1L_2L_3`.  A nondegenerate ternary quadratic
does not divide that product of three linear forms, so the fourth column is
outside `Q V^*`.  The sensor has rank four.  Thus this family enters
`B_all` exactly from `n=8` onward; no six-vertex rank-drop claim is hidden in
the construction.

## 5. Consequence for the witness-locus branch

The example proves the strict route boundary

```text
complete support
+ invertible edge blocks
+ local concision
+ all three normalized pure coefficients
  does not imply
some balanced sensor has full column rank.           (18)
```

The missing hypotheses cannot be replaced by an ambient genericity slogan:
the displayed family is exact, complete, and locally concise.  Its defect is
equally exact--the mixed even-colour coefficients (4) do not vanish.

Therefore the surviving all-balanced branch is now scoped as follows.

```text
B_all meets the strong pure/local ambient locus:       PROVED for n>=8;
mixed GHZ zero equations on that intersection:         ESSENTIAL;
B_all intersect the full witness equations:            UNKNOWN;
all-balanced witness exclusion:                        UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.          (19)
```

This theorem does not weaken the balanced full-sensor dichotomy.  It prevents
an invalid attempt to discard its closed branch using only local concision,
support, invertibility, or the three pure target coefficients.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_all_rank_drop_diagonal_complete_sharpness.py
python claims/arbitrary-order/audit_balanced_all_rank_drop_diagonal_complete_sharpness.py
python -m py_compile claims/arbitrary-order/verify_balanced_all_rank_drop_diagonal_complete_sharpness.py claims/arbitrary-order/audit_balanced_all_rank_drop_diagonal_complete_sharpness.py
uv run --with ruff ruff check claims/arbitrary-order/verify_balanced_all_rank_drop_diagonal_complete_sharpness.py claims/arbitrary-order/audit_balanced_all_rank_drop_diagonal_complete_sharpness.py
```

The SymPy primary check builds the symmetric companion polynomials, verifies
their quadratic divisibility and ranks through `m=6`, checks the direct
four-root companion tensor, and audits the coefficient and inequality
ledgers.  The independent no-import audit uses a separate sparse polynomial
implementation, exact `Fraction` row reduction, and direct perfect-matching
coefficients through eight vertices.  These bounded checks support the
displayed constants and conventions.  The arbitrary-order proof is the
matching count, polarization, common-quadratic subspace, and dimension
argument above.
