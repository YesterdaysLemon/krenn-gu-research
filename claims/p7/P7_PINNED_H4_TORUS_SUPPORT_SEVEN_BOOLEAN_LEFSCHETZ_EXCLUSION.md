# P7 pinned-star torus circuits cannot have support seven

## Status

**Exact characteristic-zero support-seven exclusion.**  Let `B` be a
weighted graph on eight named vertices and let

```text
N_B[T,i]=haf B[T minus {i}]  if i in T,
         =0                  otherwise,     |T|=5.    (1)
```

On the full edge torus,

```text
B_ij!=0 for every i<j,  N_B x=0,  x!=0
                  => |supp(x)|=8.                     (2)
```

The preceding notes excluded supports one through six.  This note excludes
support seven without enumerating supports, graphs, or parameter values.  A
hypothetical seven-supported kernel vector has one complement vertex.  The
rows containing that vertex form a `35 x 21` **complement-star Boolean
Lefschetz operator** on the internal support edges.  It factors as

```text
degree 2 --multiply by a full-support linear form--> degree 3
         --multiply by the all-one linear form----> degree 4.       (3)
```

In the square-free algebra on seven variables, the first map is injective
and the second is the invertible middle Lefschetz map.  Hence every internal
edge is forced to zero, contradicting the full edge torus.

Thus every P7 pinned rank drop on the full edge torus, if one exists, has a
kernel vector with all eight entries nonzero.  Support eight remains
**UNKNOWN**.  This is not a P7 obstruction, and global Krenn--Gu remains
**UNRESOLVED**.

## 1. The single-complement equations

Work over a characteristic-zero field `K`.  Suppose `N_B x=0` and

```text
S=supp(x),       |S|=7,       V minus S={c}.           (4)
```

The diagonal vertex gauge

```text
B_ij -> d_i d_j B_ij,       x_i -> d_i x_i             (5)
```

multiplies each five-set equation by the product of its five vertex scales.
Choose `d_i=x_i^(-1)` on `S`.  Then

```text
x_i=1  for i in S,       x_c=0.                         (6)
```

Put

```text
u_a=B_ca,             D_ab=B_ab       (a,b in S).       (7)
```

Every `u_a` and every `D_ab` is nonzero on the full edge torus.

Fix a four-set `U subset S` and use the row `T=U union {c}`.  Only the four
supported columns contribute.  In the hafnian on `{c,a,b,k}`, the term that
pairs `c` with `k` is `u_k D_ab`.  Consequently the coefficient of an
internal edge `D_ab`, `a,b in U`, is the sum of the two complementary star
entries:

```text
0=(L_u D)_U
  =sum_({a,b} subset U)
       (sum_(k in U minus {a,b}) u_k) D_ab,
                                  for every |U|=4.      (8)
```

These are all 35 rows containing the single complement vertex.  Rows wholly
inside `S` will not be needed.

## 2. Square-free factorization

Let

```text
A=K[z_a : a in S]/(z_a^2 : a in S),
ell=sum_(a in S) z_a,       u=sum_(a in S) u_a z_a,
Q_D=sum_(a<b) D_ab z_a z_b.                            (9)
```

The coefficient of `z_U` in `ell*u*Q_D` is exactly (8).  Therefore

```text
L_u = m_ell^(3) o m_u^(2): A_2 -> A_3 -> A_4,          (10)
```

where `m_v^(k)` means multiplication by the linear form `v` from degree
`k` to degree `k+1`.  We call (10) the complement-star Boolean Lefschetz
factorization.

There is an equivalent reciprocal-incidence form.  Put

```text
E_ab=D_ab/(u_a u_b),       q_a=1/u_a,
f_T=sum_({a,b} subset T) E_ab.                         (11)
```

Direct cancellation gives
`(L_uD)_U=(prod_(a in U)u_a)(delta_q f)_U`.  The row factor is nonzero,
so equation (8) is equivalent to

```text
(delta_q f)_U=sum_(a in U) q_a f_(U minus {a})=0.      (12)
```

Thus, up to invertible row and column scalings,

```text
L_u  ~  m_q^(3) W_(2,3)(7),                            (13)
```

where `W_(2,3)(7)` sends an edge vector to its triangle sums.  Formula
(13) is the weighted four-subset/edge incidence operator requested by the
single-complement reduction.

## 3. The Boolean Lefschetz lemma

### Lemma 1

In the square-free algebra on seven variables over a characteristic-zero
field:

1. `m_v^(2):A_2 -> A_3` is injective whenever every coefficient of `v` is
   nonzero;
2. `m_v^(3):A_3 -> A_4` is an isomorphism whenever every coefficient of
   `v` is nonzero.

### Proof

First take `v=ell`.  In the square-free monomial bases, `m_ell^(2)` is the
two-subset/three-subset inclusion matrix `W_(2,3)(7)`.  Its Gram matrix has
diagonal entries five, entry one when two edges meet, and entry zero when
they are disjoint.  If `R` is the unsigned vertex-edge incidence matrix of
`K_7`, then

```text
W_(2,3)(7)^T W_(2,3)(7)=3I+R^T R.                    (14)
```

Now `R R^T=5I+J`.  Hence the eigenvalues of (14) are

```text
15 (multiplicity 1),  8 (multiplicity 6),
 3 (multiplicity 14).                                (15)
```

They are nonzero in characteristic zero, so `m_ell^(2)` is injective.  In
particular,

```text
det(W_(2,3)^T W_(2,3))=15*8^6*3^14.                 (16)
```

The map `m_ell^(3)` is the square `35 x 35` inclusion matrix
`W_(3,4)(7)`.  Identify a four-set row with its complementary three-set.
The resulting matrix is the disjointness matrix on three-subsets of a
seven-set.  On the standard Boolean flag quotients of levels
`j=0,1,2,3`, its eigenvalues and multiplicities are

```text
 4 (1),   -3 (6),    2 (14),   -1 (14).              (17)
```

The eigenvalue formula is the elementary inclusion--exclusion count
`(-1)^j binom(4-j,3-j)`; the quotient dimensions are
`binom(7,j)-binom(7,j-1)`.  All four values are nonzero.  Therefore
`m_ell^(3)` is invertible.  In fixed lexicographic subset order,

```text
det W_(3,4)(7)=-2^16*3^6.                            (18)
```

Finally, if `v=sum v_a z_a` has no zero coefficient, the diagonal algebra
automorphism `z_a -> v_a z_a` carries `ell` to `v`.  On every pair of
adjacent degrees it conjugates multiplication by `ell` to multiplication by
`v`, with invertible diagonal matrices on source and target.  The two rank
statements therefore hold for every such `v`.  This proves the lemma.

The determinant displays in (16) and (18) are exact integer
characteristic-zero certificates, not finite-field evidence.

## 4. Support seven is impossible

Apply Lemma 1 directly to (10).  Since all seven `u_a` are nonzero,
`m_u^(2)` is injective.  The middle map `m_ell^(3)` is invertible.  Hence
their composite `L_u` is injective, and (8) forces

```text
D_ab=0        for every a<b in S.                    (19)
```

This contradicts the full edge torus.  Equivalently, (13) first uses the
injectivity of the triangle-sum map and then the invertibility of the
weighted middle Lefschetz map.  No row wholly inside the seven-point support
is required.

Combining (19) with the prior support-one-through-six exclusions proves
(2).  Notice the scope: (2) does not say that `N_B` is nonsingular.  It says
that any surviving kernel must meet every pinned column.

## 5. Incidence-line consequence

If a one-dimensional P7 target-incidence cofactor line is contained in the
selected pinned determinantal locus and a nonzero point of that line is
realized by a full-edge-torus graph, every pinned dependency at that graph
has full support eight.  A future exclusion or classification may therefore
work on the dense kernel torus and may normalize all eight kernel entries at
once.  This removes every coordinate-support boundary but does not establish
target-line graph realizability or rule out a full-support dependency.

## 6. The final primitive Boolean-square locus

The full-support case has a compact intrinsic form.  Gauge all eight nonzero
kernel coordinates to one and work in

```text
A^(8)=K[z_1,...,z_8]/(z_1^2,...,z_8^2),
ell=z_1+...+z_8,
Q_B=sum_(i<j) B_ij z_i z_j.                          (20)
```

The coefficient of a five-set `T` in `ell Q_B^2` is twice the pinned row
`sum_(i in T) haf B[T minus {i}]`.  Hence a full-support kernel is equivalent
to

```text
Q_B^2 in P_4^(8):=ker(m_ell:A_4^(8)->A_5^(8)).       (21)
```

The Boolean Lefschetz map in (21) is surjective in characteristic zero, so

```text
dim P_4^(8)=binom(8,4)-binom(8,5)=70-56=14.          (22)
```

Define the **primitive Boolean-square locus**

```text
S_8={ [Q] in P(A_2^(8)) : Q^2 in P_4^(8) }.
```

The remaining torus question is exactly whether `S_8` meets the open set on
which all 28 edge coefficients of `Q` are nonzero.  This packages the final
pinned branch as the intersection of a quadratic square map with a
14-dimensional primitive Lefsche space.  It is a representation-theoretic
and projective-incidence problem, not an invitation to enumerate weighted
graphs.  Nonemptiness of that torus intersection remains **UNKNOWN**.

## 7. Exact wall

```text
P7 full-edge-torus pinned circuits of size 1..4: IMPOSSIBLE (PRIOR);
P7 full-edge-torus pinned circuits of size 5:    IMPOSSIBLE (PRIOR);
P7 full-edge-torus pinned circuits of size 6:    IMPOSSIBLE (PRIOR);
P7 full-edge-torus pinned circuits of size 7:    IMPOSSIBLE (THIS NOTE);
P7 full-edge-torus pinned circuits of size 8:    UNKNOWN;
P7 pinned matrix full rank on the edge torus:    UNKNOWN;
target cofactor line graph-torus realizability:  UNKNOWN;
P7 obstruction:                                 UNKNOWN;
primitive Boolean-square space dimension:           14;
primitive Boolean-square locus meets edge torus:     UNKNOWN;
global Krenn--Gu:                                UNRESOLVED.           (23)
```

No supports, configurations, graphs, finite fields, words, or parameter
tuples were enumerated.  The replays construct only the fixed Boolean
incidence maps on seven named points and check the universal hafnian and
Lefschetz identities above.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_pinned_h4_torus_support_seven_boolean_lefschetz_exclusion.py
python claims/p7/audit_p7_pinned_h4_torus_support_seven_boolean_lefschetz_exclusion.py
python -m py_compile claims/p7/verify_p7_pinned_h4_torus_support_seven_boolean_lefschetz_exclusion.py claims/p7/audit_p7_pinned_h4_torus_support_seven_boolean_lefschetz_exclusion.py
uv run --with ruff ruff check claims/p7/verify_p7_pinned_h4_torus_support_seven_boolean_lefschetz_exclusion.py claims/p7/audit_p7_pinned_h4_torus_support_seven_boolean_lefschetz_exclusion.py
```

The primary verifier checks all universal single-complement hafnian row
identities, both matrix factorizations, the exact characteristic-zero ranks,
the determinant certificates, and the rank-56 Boolean map defining the
14-dimensional final primitive space.  The independent standard-library
audit reconstructs the coefficient tensors and uses exact rational and
fraction-free integer elimination.  Neither imports the other or any project
code.
