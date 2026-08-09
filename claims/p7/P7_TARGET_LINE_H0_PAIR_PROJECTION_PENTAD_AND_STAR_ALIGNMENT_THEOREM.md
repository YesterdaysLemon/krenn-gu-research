# P7 target-line pair projection: pentad and pinned-star alignment on `h=0`

## Status

**Exact characteristic-zero conditional obstruction and exact pinned-open
pair-sector criterion.**  This note does not enumerate graphs, supports,
quadruples, colourings, parameter points, or finite fields.

Assume that a legal P7 companion map has full 219-label sensor rank and meets
the diagonal target in a simple line.  Relabel the nine nonroots so that
`Q={0,1}` is the proposed residual pair and `B={2,...,8}` are the seven
blockers.  The target line has a unique projective shallow-cofactor vector
`[w]`.  Its 21 named four-deck coordinates

```text
y_ij=w_{ {0,1,i,j} },              2<=i<j<=8,        (1)
```

form a canonical seven-port pair array.  Every five-blocker restriction of
this array is a legal **linear coefficient window**: full sensor rank supplies
individual selectors for all ten named coordinates in that window.  Thus, at
a full-sensor target-incidence point, there is no further selector-matroid or
nuisance-column ambiguity in the proposed pentad route.

The physical obstruction is sharp.  On the branch `h=a_01=0`, every
five-subset pentad of (1) must vanish.  These 21 degree-five equations package
as one `S_7`-equivariant exterior covariant.  A single nonzero component
excludes the entire nonzero target line before pinned inversion or the
degree-nine partner stresses are evaluated.

On the chart where the pinned reconstructions at `0` and `1` are open, there
is a stronger exact criterion.  The condition `h=0` is one homogeneous
degree-eight numerator, and compatibility of all 21 coordinates (1) with the
two reconstructed residual stars is precisely projective rank one: the
`2 x 21` matrix formed by the target pair vector and the reconstructed pair
vector must have rank at most one, with the zero cases treated explicitly.
Its cleared `2 x 2` minors have degree 17.  This is necessary and sufficient
for the complete residual-pair four-deck sector, not merely necessary.

The theorem does **not** prove that the legal GHZ fibre meets the full-sensor
simple-incidence locus, and it does not settle the other 105 four-deck
coordinates or the six- and eight-decks.  P7 and global Krenn--Gu remain
**UNRESOLVED**.

## 1. From a Schubert line to named pair coordinates

Let

```text
Gamma:U -> T,                 dim U=219, dim T=243,
Delta=span{e_0^(tensor 5),e_1^(tensor 5),e_2^(tensor 5)}.   (2)
```

Suppose `Gamma` is injective and its image meets `Delta` in one dimension.
Equivalently,

```text
K_Gamma=ker(pi_Delta Gamma)=K w                         (3)
```

for a nonzero named cofactor vector `w`.  A nonzero target on this incidence
line has candidate shallow deck

```text
C=t w,                    t!=0.                         (4)
```

Injectivity of `Gamma` gives a linear left inverse on its image.  Extending
each coordinate functional from `im Gamma` to `T` produces functionals
`lambda_I in T*` satisfying

```text
lambda_I Gamma=e_I^*.                                  (5)
```

In particular, all 21 coordinates (1), and hence the ten coordinates on any
chosen five-subset of blockers, are simultaneously selectable.  This is a
statement about named coefficient functionals.  It does not replace the
still-missing proof that a legal target-incidence point exists.

## 2. The alternating pentad covariant

For ordered ports `1<2<3<4<5`, put

```text
P_12345 =
   y12 y13 y24 y35 y45 - y12 y13 y25 y34 y45
 - y12 y14 y23 y35 y45 + y12 y14 y25 y34 y35
 + y12 y15 y23 y34 y45 - y12 y15 y24 y34 y35
 + y13 y14 y23 y25 y45 - y13 y14 y24 y25 y35
 - y13 y15 y23 y24 y45 + y13 y15 y24 y25 y34
 - y14 y15 y23 y25 y34 + y14 y15 y23 y24 y35.          (6)
```

For a five-subset `A={i_1<...<i_5}` of `B`, let `P_A(y)` be (6) after
order-preserving relabeling.  If `E` is the seven-dimensional permutation
space with basis `e_2,...,e_8`, define

```text
mathfrak P(y)=sum_(|A|=5) P_A(y)
              e_(i_1) wedge ... wedge e_(i_5)
              in wedge^5 E.                            (7)
```

The pentad changes sign under an odd permutation of its five ports, exactly
as the exterior basis vector does.  Therefore (7) is `S_7`-equivariant under
simultaneous blocker relabeling.  It is homogeneous of degree five in `w`.
No `GL(7)` covariance is claimed: the named deletion basis is physical data.

### Theorem 1 (degree-five target-line obstruction)

If a nonzero point `C=t w` of the simple target-incidence line is the shallow
principal-hafnian deck of a graph with `a_01=0`, then

```text
mathfrak P(y)=0.                                       (8)
```

Consequently, if `P_A(y)!=0` for even one named five-subset `A`, no nonzero
point of the target-incidence line belongs to the physical `h=0` branch.

### Proof

For every blocker pair `i<j`, the physical four-hafnian is

```text
C_{01ij}
 =a_01 a_ij+a_0i a_1j+a_0j a_1i
 =a_0i a_1j+a_0j a_1i.                                (9)
```

By (4), the left side is `t y_ij`.  Thus every five-port restriction is the
off-diagonal hyperbolic Gram array of the two vectors
`(a_0i)` and `(a_1i)`, up to the common nonzero scalar `t`.  Substitution in
(6) gives zero, and homogeneity removes `t`.  This holds for every component
of (7).

### Sharp boundary: incidence alone does not force (8)

The obstruction uses principal-hafnian integrability, not Schubert incidence
alone.  Indeed, choose any nonzero `w in K^219` with first coordinate one and
give ten of its named pair coordinates the values `1,2,...,10` in the order

```text
12,13,14,15,23,24,25,34,35,45.                        (10)
```

Formula (6) then equals `-6`.  If `c_0,...,c_218` are coordinates on `U`,
the 218 functionals

```text
B_j(c)=c_j-w_j c_0,              1<=j<=218,            (11)
```

have common kernel `K w`.  Embed their values in the 240-dimensional
quotient `T/Delta` and set the first target coordinate of `Gamma(c)` equal to
`c_0`.  The resulting ambient `Gamma:U->T` is injective,
`ker(pi_Delta Gamma)=K w`, and its incidence line has nonzero pentad.
This model is not asserted to come from legal symmetric companion blocks; it
proves exactly that legality and hafnian integrability are indispensable.

## 3. The pinned `h=0` numerator

Use the established pinned-star matrices.  For `p=0,1`, let

```text
d_p=det Nhat_p,
u_p=adj(Nhat_p) bhat_p,                               (12)
```

evaluated on the line generator `w`.  Each `d_p` and every coordinate of
`u_p` is homogeneous of degree eight in `w`.  On the open chart

```text
d_0 d_1 !=0,                                         (13)
```

the reconstructed residual edge is

```text
h=a_01=(u_0)_1/d_0.                                  (14)
```

### Theorem 2 (one equation for the `h=0` branch)

On (13), the reconstructed graph lies on `h=0` if and only if

```text
eta(w):=(u_0(w))_1=0.                                (15)
```

The equation `eta=0` is homogeneous of degree eight and is independent of
the choice of scale for `[w]`.

### Proof

This is (14) after multiplication by the nonzero denominator `d_0`.  Under
`w -> rho w`, numerator and denominator both scale by `rho^8`, so the edge
and its zero locus are projectively well defined.

## 4. Exact pair-star alignment

Assume (13) and (15).  For blocker pairs define

```text
khat_ij=(u_0)_i (u_1)_j+(u_0)_j (u_1)_i.             (16)
```

This is homogeneous of degree 16 in `w`, and the corresponding four-hafnian
of the reconstructed residual stars is

```text
k_ij=khat_ij/(d_0 d_1).                              (17)
```

The absolute pair-sector equations for the candidate (4) are

```text
t y_ij=k_ij.                                         (18)
```

Set `tau=t d_0 d_1`.  Then all 21 equations (18) become the single vector
proportionality condition

```text
tau y=khat,                    tau!=0.                (19)
```

### Theorem 3 (necessary and sufficient pair-sector criterion)

On (13) and (15), the complete set of 21 residual-pair four-deck equations
(18) has a nonzero amplitude `t` if and only if one of the following mutually
exclusive conditions holds:

1. `y=0` and `khat=0`; or
2. `y!=0`, `khat!=0`, and

```text
A_(ef)(w):=y_e khat_f-y_f khat_e=0
             for every blocker edges e,f.            (20)
```

If exactly one of `y,khat` is zero, no nonzero amplitude exists.  In case 2,
`tau`, hence `t=tau/(d_0d_1)`, is unique.  Each alignment equation (20) is
homogeneous of degree 17 in `w`.

### Proof

Equations (20) are the `2 x 2` minors of the matrix with rows `y` and
`khat`.  If both rows are nonzero, their vanishing is equivalent over a field
to proportionality by a unique nonzero scalar.  The two zero cases follow
directly from (19).  Finally, `y` has degree one and `khat` degree 16, giving
degree 17.

### Corollary 4 (pentad versus alignment)

If Theorem 3 passes, every pentad in (8) vanishes automatically.  Indeed,
`khat_ij` itself has the hyperbolic Gram form

```text
khat_ij=(u_0)_i (u_1)_j+(u_0)_j (u_1)_i.             (21)
```

The converse is false in general.  Pentad vanishing says that a five-port
subarray lies in the two-factor-analysis hypersurface; it does not say that
the factors agree with the two stars already reconstructed from the six-deck.
Thus (7) is the lowest-degree target-line prefilter, while (15) and (20) are
the target-compatible pinned tests.

## 5. Translation to three established geometries

This route is useful because it translates the same physical question three
times, without enlarging it into a generic elimination problem.

1. **Schubert geometry.**  Simple diagonal incidence turns 219 unknown
   shallow cofactors into one projective point `[w]`.  The problem is an
   intersection of the legal companion-image locus with a Schubert incidence
   stratum, followed by testing that point against physical deck varieties.
2. **Algebraic factor analysis and circuit invariants.**  Projection to the
   residual-pair four-deck gives the off-diagonal rank-two factor-analysis
   model.  Its first circuit occurs on five ports and is the pentad.  The
   exterior package (7) records all named five-port circuits equivariantly.
3. **Segre/determinantal rank-one geometry.**  Once the residual stars are
   reconstructed, no factor completion remains: the target pair vector must
   be the same projective point as the star-pair vector.  Equations (20) are
   exactly the rank-one `2 x 2` minors, equivalently the circuits of the
   rank-one column matroid of the `2 x 21` matrix.

The factor-analysis identification and pentad formula are the transfer of
Drton, Sturmfels, and Sullivant,
[*Algebraic Factor Analysis: Tetrads, Pentads and Beyond*](https://arxiv.org/abs/math/0509390),
to the corrected two-residual hafnian channel.  The new problem-specific
content here is the projection of the P7 Schubert cofactor line to those
coordinates and its exact alignment with the pinned residual stars.

## Scope wall

```text
full sensor makes every named Q-pair label selectable: YES;
simple target incidence reduces the deck to [w]:         CONDITIONAL;
S_7-equivariant degree-five pentad covariant:             PROVED;
nonzero component excludes the entire h=0 target line:    PROVED;
target incidence alone forces pentad vanishing:           FALSE;
pinned h=0 numerator eta, degree 8:                        EXACT ON OPEN;
pair-star alignment minors, degree 17:                    EXACT ON OPEN;
all 21 Q-pair four-deck equations:                         IFF CRITERION;
other 105 four-deck equations:                             STILL REQUIRED;
six- and eight-deck partner stresses:                      STILL REQUIRED;
legal full-rank target-incidence point:                    UNKNOWN;
GHZ fibre meets simple-incidence plus pinned open:         UNKNOWN;
P7 obstruction or construction:                           UNKNOWN;
global Krenn--Gu:                                         UNRESOLVED.
```

## Exact replay

```powershell
uv run --with sympy python claims/p7/verify_p7_target_line_h0_pair_projection_pentad_and_star_alignment.py
python claims/p7/audit_p7_target_line_h0_pair_projection_pentad_and_star_alignment.py
python -m py_compile verify_p7_target_line_h0_pair_projection_pentad_and_star_alignment.py audit_p7_target_line_h0_pair_projection_pentad_and_star_alignment.py
uv run --with ruff ruff check verify_p7_target_line_h0_pair_projection_pentad_and_star_alignment.py audit_p7_target_line_h0_pair_projection_pentad_and_star_alignment.py
```

The primary replay verifies the hyperbolic-Gram pentad identity, its degree,
the exact `-6` ambient-incidence boundary, the pinned clearing, the projective
alignment criterion, and a fixed rational simple-incidence model.  The
independent standard-library audit reconstructs the pentad in a sparse
integer polynomial ring and uses separately written rational row reduction.
Both are bounded exact symbolic audits of the displayed proofs, not graph or
parameter searches and not evidence from sampled parameters.
