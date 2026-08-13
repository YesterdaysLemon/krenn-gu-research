# Balanced `m=3` source-aligned exceptional-root-row obstruction

## Status

**Exact characteristic-zero exclusion inside the S2U sparse
block-permanent branch.**  Put the surviving full-joint-rank normal form in
the notation of S2U:

```text
U=A_1 tensor e_(2,s) tensor e_(3,s),
G_N in J + U.                                           (1)
```

Let `R_i` be the three-dimensional row space of the `i`th root block row of
the invertible joint cross map

```text
H:(X direct-sum Y direct-sum Z)
  -> A_1 direct-sum A_2 direct-sum A_3.                 (2)
```

The root `1` in (1) is the exceptional root, opposite the unique surviving
root--root edge.  It is impossible for `R_1` to equal any one source
summand.  Equivalently, after a permutation of `X,Y,Z`, the sparse equation
(1) has no invertible solution of block-row form

```text
H=[ H_1X   0      0   ]
  [ H_2X  H_2Y  H_2Z ]
  [ H_3X  H_3Y  H_3Z ],                det(H_1X)!=0.    (3)
```

This excludes a nonmonomial family not covered by the monomial theorem in
S2U.  It does not exclude an exceptional root row meeting two or three
source summands, an arbitrary invertible nonmonomial `H`, joint rank at most
eight, the other S2Q strata, any higher order, a witness, or a
counterexample.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The sparse target gives an off-diagonal zero grid

Write a root-2 row and a root-3 row, after discarding their `X` components,
as

```text
p_b=(v_b,w_b) in Y^* direct-sum Z^*,
q_c=(x_c,y_c) in Y^* direct-sum Z^*.                   (4)
```

Every word in the support of (1) has equal root-2 and root-3 colours.  Hence
for each `b!=c`, the entire root-1 output row is zero.  Since `R_1=X^*`, the
corresponding block-permanent identity is

```text
r tensor (v_b tensor y_c + x_c tensor w_b)=0
for every r in X^*.                                   (5)
```

Thus

```text
m(p_b,q_c):=v_b tensor y_c+x_c tensor w_b=0
whenever b!=c.                                        (6)
```

The first block row in (3) is invertible.  Expanding `det H` along it shows
that the lower complementary block

```text
[ H_2Y H_2Z ]
[ H_3Y H_3Z ]                                         (7)
```

is invertible.  Consequently the three `p_b` and the three `q_c` together
form a basis of `Y^* direct-sum Z^*`.  In particular each triple is a basis
of a three-plane and every two members of either triple are independent.

## 2. Zero divisors of the mixed product

### Lemma (pure-or-line zero divisor)

Let `V,W` be vector spaces over a field and let `q=(x,y)` be nonzero in
`V direct-sum W`.  For

```text
m((v,w),(x,y))=v tensor y+x tensor w                  (8)
```

the zero-divisor space

```text
Z(q)={ (v,w):m((v,w),q)=0 }                           (9)
```

is

```text
V,                         if y=0;
W,                         if x=0;
span((x,-y)),              if x!=0 and y!=0.          (10)
```

### Proof

The first two cases are immediate from the injectivity of tensoring by a
nonzero vector.  In the last case, equality of the two nonzero rank-one
tensors in (8) forces `v=lambda x` and `w=-lambda y`.  The same conclusion
also contains the zero solution.  QED.

## 3. Pigeonhole contradiction

Fix `c`.  Equation (6) puts the two independent vectors `p_b`, `b!=c`, in
`Z(q_c)`.  The one-dimensional mixed case of (10) is impossible.  Therefore
every `q_c` is pure: it lies in `Y^*` or in `Z^*`.

Among the three `q_c`, two lie in the same summand.  Suppose, after
relabeling, that

```text
q_0,q_1 in Y^*.                                       (11)
```

Then `Z(q_0)=Z(q_1)=Y^*`.  The four off-diagonal equations involving
`q_0,q_1` force

```text
p_1,p_2 in Y^*,
p_0,p_2 in Y^*,                                       (12)
```

so all three `p_b` lie in `Y^*`.  Since they are independent, they span
`Y^*`.  But (11) then places two nonzero `q_c` in that same span, contradicting
the independence of the six vectors in (7).  The `Z^*` case is identical.
This contradiction proves the theorem.

The proof uses only exact linear algebra.  S2U supplies the
characteristic-zero physical localization and the sparse support (1).

## 4. Proof-topology consequence

The full-joint-rank residue now has the exact refinement

```text
invertible monomial H:                                 IMPOSSIBLE (S2U);
nonmonomial H with source-aligned exceptional row:     IMPOSSIBLE (here);
nonmonomial H with exceptional row on >=2 sources:     OPEN;
joint cross rank <=8:                                  OPEN;
global Krenn--Gu conjecture:                            UNRESOLVED.       (13)
```

The next local obligation is therefore not an unconstrained search over all
invertible `9 x 9` matrices: it is the two-source-support exceptional-row
chart, followed by the fully supported chart.  Cancellation across those
charts has not been excluded.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_full_joint_cross_rank_source_aligned_exceptional_root_row_obstruction.py
python -I claims/arbitrary-order/audit_balanced_m3_full_joint_cross_rank_source_aligned_exceptional_root_row_obstruction.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_full_joint_cross_rank_source_aligned_exceptional_root_row_obstruction.py claims/arbitrary-order/audit_balanced_m3_full_joint_cross_rank_source_aligned_exceptional_root_row_obstruction.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_full_joint_cross_rank_source_aligned_exceptional_root_row_obstruction.py claims/arbitrary-order/audit_balanced_m3_full_joint_cross_rank_source_aligned_exceptional_root_row_obstruction.py
```

The primary replay checks the pure and mixed zero-divisor ranks, all eight
purity patterns, the exact five-word target support, and the aligned
block-permanent reduction.  The independent no-import audit uses its own
finite-field zero-divisor census and a separate purity-pattern enumeration.
The arbitrary-field argument is the rank-one tensor proof in Section 2.

## Dependency

- [`BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_MONOMIAL_ROOT_EDGE_LOCALIZATION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_MONOMIAL_ROOT_EDGE_LOCALIZATION_THEOREM.md)
