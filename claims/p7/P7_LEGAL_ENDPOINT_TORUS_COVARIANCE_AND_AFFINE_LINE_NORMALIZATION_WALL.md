# Legal endpoint scaling preserves P7 projective stresses but moves the affine normalization

## Status

**Exact characteristic-zero torus-covariance theorem and proof-route
boundary.**  The degree-nine cofactor-line stresses can be pulled through
the legal five-root matching formulas without expanding any 219-variable
elimination.  Scaling every root--nonroot edge incident to a named nonroot
`u` by a nonzero scalar `rho_u` acts diagonally on the full companion map:

```text
Gamma_rho=Gamma diag(rho_D),
rho_D=product_(u in D) rho_u.                          (1)
```

This preserves legality, full sensor rank, the sensor image, and its
diagonal target-incidence subspace.  A sensor-dependent cofactor-line
generator transforms contragrediently.  In remaining-set notation,

```text
w_I^rho=(rho_I/R) w_I,
R=product_(u in N) rho_u.                              (2)
```

Pinned inversion then gives the vertex-scaled candidate graph

```text
a_pq^rho=rho_p rho_q a_pq.                             (3)
```

Every degree-nine partner/Hadamard residual is a torus semi-invariant, so
its vanishing is constant along the endpoint-torus orbit.  The same is true
of opposite-star compatibility and projective four-deck proportionality.
The required **affine** four-deck amplitude, however, is multiplied by the
single character `R`.

Consequently, if any legal pinned-open target-incidence cofactor line is
projectively hafnian-integrable, exactly one product character can have a
prescribed affine target normalization.  All endpoint scalings with a
different total product give legal full-rank incidence data on which every
projective stress still vanishes but the affine four-deck test fails.  This
is an exact conditional orbit construction, not an unconditional example:
no legal full-rank target-incidence point is currently known.

The theorem rules out a normalization-only obstruction and shows that the
magnitudes of blocker/nonblocker endpoint columns cannot force a
degree-nine stress to become nonzero.  Any genuine obstruction must use
scale-free directional data, the absence of the legal incidence line, or a
projective stress itself.  `P_7` and global Krenn--Gu remain
**UNRESOLVED**.

## 1. The legal endpoint torus

Let the five roots be `0,...,4` and the nine named nonroots be

```text
N={0,...,8}.
```

Write `h_(i,u)` for the root-side form of the edge from root `i` to nonroot
`u`, and `L_ij` for a root--root block.  The full mixed companion columns
are the matching sums

```text
G_D^(5),       |D|=5;
G_D^(3),       |D|=3;
G_u^(1),       |D|=1.                                 (4)
```

Every term of `G_D` uses each endpoint in `D` exactly once and no endpoint
outside `D`.

Choose `rho=(rho_0,...,rho_8) in (K^*)^9` and make the physical block
replacement

```text
h_(i,u) -> rho_u h_(i,u)       for every root i,
L_ij unchanged.                                        (5)
```

The reverse block is scaled by the same scalar, so symmetry and looplessness
are preserved.  A blocker evaluation that was nonzero stays nonzero; a
residual nonblocker evaluation that was zero stays zero.  Fully supported
roots and pairwise root zero-coupling are unchanged.  Thus (5) preserves the
legal incidence conditions, though it need not preserve a convenient
normalization in which every blocker evaluates to one.

### Lemma 1 (column-character factorization)

Under (5), every labeled companion column obeys

```text
G_D -> rho_D G_D,       rho_D=product_(u in D) rho_u.   (6)
```

Hence, with `R_rho=diag(rho_D)`, equation (1) holds.

### Proof

In a depth-five term, a bijection from the five roots to `D` uses every
root--endpoint form named by `D` once.  In a depth-three term, one root pair
uses an unchanged `L_ij` and the other three roots use the three endpoints
of `D` once.  In a depth-one term, two root pairs use unchanged `L` blocks
and the remaining root uses `u` once.  Every summand therefore acquires the
same factor `rho_D`, proving (6).

Since `R_rho` is invertible,

```text
im Gamma_rho=im Gamma,          rank Gamma_rho=rank Gamma. (7)
```

In particular, the intersection with the diagonal target space is exactly
the same subspace before and after endpoint scaling.

## 2. Contragredient action on the cofactor line

Let `pi_Delta` denote projection modulo the diagonal target space and put

```text
K_Gamma=ker(pi_Delta Gamma).                           (8)
```

Equation (1) gives

```text
K_(Gamma_rho)=R_rho^(-1) K_Gamma.                     (9)
```

If `w` is a generator of a one-dimensional `K_Gamma`, choose the covariant
generator

```text
w_D^rho=rho_D^(-1) w_D.                               (10)
```

Write a label by its complementary remaining set `I=N minus D`.  With

```text
rho_I=product_(u in I) rho_u,
R=product_(u in N) rho_u,
```

equation (10) becomes (2), because `rho_(N minus I)=R/rho_I`.

For a fixed diagonal target `J=Gamma(t_0 w)`, the transformed sensor has

```text
J=Gamma_rho(t_0 w^rho).                               (11)
```

Thus the target vector and its scalar `t_0` relative to the covariantly
chosen line generator stay fixed.  What moves is the affine principal-
hafnian normalization of that generator.

## 3. Pinned determinant and edge characters

Use any fixed eight-row pinned chart from
`P7_TARGET_INCIDENCE_DETERMINANT_CLEARED_HAFNIAN_INTEGRABILITY_THEOREM.md`.
For pin `p`, its selected row five-sets are a family `B_p`.  The pinned
matrix and right-hand side have entries

```text
N_p[T,s]=w_(T minus {s}),
b_p[T]=w_({p} union T).                               (12)
```

Let

```text
d_p=det N_p,
u_p=adj(N_p)b_p,
a_ps=(u_p)_s/d_p.                                     (13)
```

Define the nonzero pin character

```text
chi_p
 =R^(-8)
   (product_(T in B_p) rho_T)
   (product_(s != p) rho_s^(-1)).                     (14)
```

### Theorem 2 (pinned torus covariance)

The transformed Cramer data satisfy

```text
d_p^rho=chi_p d_p,
(u_p^rho)_s=chi_p rho_p rho_s (u_p)_s,
a_ps^rho=rho_p rho_s a_ps.                            (15)
```

### Proof

For the selected rows and columns, (2) factors the transformed matrix as

```text
N_p^rho
 =R^(-1) diag(rho_T:T in B_p)
    N_p diag(rho_s^(-1):s != p),                      (16)

b_p^rho
 =rho_p R^(-1) diag(rho_T:T in B_p)b_p.               (17)
```

Taking determinants in (16) gives the first formula in (15).  Solving
`N_p^rho a_p^rho=b_p^rho` and cancelling the invertible row factors gives

```text
diag(rho_s^(-1))a_p^rho=rho_p a_p,
```

which proves the edge formula.  Multiplying by `d_p^rho` gives the Cramer
numerator formula.

The pinned-open condition is invariant because every `chi_p` is nonzero.

## 4. Degree-nine stresses are semi-invariants

For `p in S`, `|S|=6`, recall the determinant-cleared partner residual

```text
H6_(p,S)
 =d_p w_S-sum_(s in S minus {p})(u_p)_s w_(S minus {p,s}). (18)
```

The order-eight residual `H8_(p,Q)` has the identical formula with
`|Q|=8` and six-set lower cofactors.

### Theorem 3 (projective-stress semi-invariance)

Under the legal endpoint torus,

```text
H6_(p,S)(w^rho)
 =chi_p (rho_S/R) H6_(p,S)(w),                        (19)

H8_(p,Q)(w^rho)
 =chi_p (rho_Q/R) H8_(p,Q)(w).                        (20)
```

For opposite-star compatibility,

```text
O_pq(w^rho)
 =chi_p chi_q rho_p rho_q O_pq(w).                    (21)
```

### Proof

The first term of (18) acquires `chi_p rho_S/R`.  In a summand of the
second term, (15) contributes `chi_p rho_p rho_s` and (2) contributes
`rho_(S minus {p,s})/R`.  Their product is the same character because

```text
rho_p rho_s rho_(S minus {p,s})=rho_S.
```

This proves (19); (20) is identical.  Both terms of the overlap polynomial
acquire the character in (21).

Thus vanishing of every projective partner, `h_8`, and overlap stress is
constant on each legal endpoint-torus orbit.  Endpoint magnitudes cannot
turn a vanishing projective obstruction into a nonvanishing one.

The rational Euler residual on an even set `S`,

```text
k w_S-sum_(p<q in S)a_pq w_(S minus {p,q}),           (22)
```

similarly acquires the single character `rho_S/R`.  Hence its vanishing is
also orbit-invariant.

## 5. The affine amplitude carries the total-product character

Let `A(w)` be the oriented candidate graph reconstructed on the pinned-open
chart.  For a four-set `I` with `w_I!=0`, define its required radial
amplitude

```text
t_I(w)=haf(A(w)[I])/w_I.                              (23)
```

Equation (3) gives

```text
haf(A(w^rho)[I])=rho_I haf(A(w)[I]).                  (24)
```

Together with (2), this proves

```text
t_I(w^rho)=R t_I(w).                                  (25)
```

If `w_I=0`, the corresponding zero/nonzero consistency condition in the
four-deck equation is preserved by the same nonzero factors.  Therefore:

- equality of all defined amplitudes `t_I` is endpoint-torus invariant;
- projective four-deck realizability is orbit-invariant;
- its unique required affine amplitude transforms by the one character `R`.

### Corollary 4 (conditional affine-failing incidence orbit)

Suppose a legal full-rank target-incidence point has a one-dimensional,
pinned-open cofactor line whose degree-nine stresses vanish and whose
four-deck amplitudes are projectively consistent, with required amplitude
`t_*`.  Preserve a fixed target as in (11), so its line scalar is `t_0`.
Then its legal endpoint-torus orbit has:

```text
all projective stresses zero for every rho;
affine principal-hafnian compatibility
  iff R=t_0/t_*.                                      (26)
```

In particular, if the starting point is affinely compatible, then the
codimension-one subtorus `R=1` remains compatible and every scaling with
`R!=1` is an exact legal target-incidence point on which all projective
stresses vanish but the affine four-deck test fails.

This is conditional on the existence of the starting legal incidence line.
It is not the unconditional construction still missing from the proof.

## 6. Consequences for the obstruction search

The pullback supplies a useful triage:

1. A degree-nine stress should be studied as a torus semi-invariant.  Any
   leading-term or factorization proof must use root-form directions or
   root--root coupling data, not merely endpoint magnitudes.
2. An affine four-deck failure at one arbitrary column normalization is not
   a projective P7 obstruction.  The total endpoint product moves the unique
   allowed normalization while preserving the full sensor image and target
   incidence.
3. If a legal incidence generator is found, degree-nine stresses can be
   evaluated on one convenient endpoint normalization; their vanishing then
   holds or fails on its whole torus orbit.
4. If they vanish, the remaining affine question is only the one character
   equation (26).

This theorem does not show that a degree-nine stress vanishes on every legal
incidence line, nor that one is forced nonzero.  It isolates the scale-free
part on which such a proof must operate.

## 7. Scope wall

```text
legal endpoint action on matching columns:             EXACT;
full sensor image and target-incidence space preserved: YES;
cofactor-line contragredient character:                 EXACT;
pinned candidate graph transforms by vertex scaling:   EXACT;
degree-nine partner/h8 stress vanishing:                TORUS-INVARIANT;
opposite-star and Euler stress vanishing:               TORUS-INVARIANT;
projective four-deck consistency:                       TORUS-INVARIANT;
required affine amplitude character:                   product rho_u;
normalization magnitudes force projective obstruction:  FALSE;
conditional affine-failing legal orbit:                 PROVED;
unconditional legal full-rank incidence line:           UNKNOWN;
stress forced nonzero by scale-free legal data:          UNKNOWN;
explicit legal incidence line with all stresses zero:   NOT CONSTRUCTED;
P7 obstruction or construction:                        UNKNOWN;
global Krenn--Gu:                                      UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_p7_legal_endpoint_torus_covariance_and_affine_line_normalization.py
python audit_p7_legal_endpoint_torus_covariance_and_affine_line_normalization.py
python -m py_compile verify_p7_legal_endpoint_torus_covariance_and_affine_line_normalization.py audit_p7_legal_endpoint_torus_covariance_and_affine_line_normalization.py
uv run --with ruff ruff check verify_p7_legal_endpoint_torus_covariance_and_affine_line_normalization.py audit_p7_legal_endpoint_torus_covariance_and_affine_line_normalization.py
```

The primary verifier checks the endpoint character of every legal matching
depth, the pinned determinant/Cramer characters, nonzero degree-nine
semi-invariance on a perturbed deck, vertex scaling of all 36 reconstructed
edges, and the total-product affine amplitude character.  The independent
standard-library audit repeats the same identities with rational arithmetic,
Bareiss determinants, and its own hafnian recursion.  Neither replay imports
project code or searches supports, incidence parameters, or cofactor space.
