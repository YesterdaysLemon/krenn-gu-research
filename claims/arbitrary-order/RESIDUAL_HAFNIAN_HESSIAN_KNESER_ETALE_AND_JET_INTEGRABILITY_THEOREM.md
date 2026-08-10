# Residual-hafnian Hessian Kneser chart and complete open-jet integrability

## Status

**Exact arbitrary-even-order characteristic-zero theorem.**  Let `A` be a
hollow symmetric scalar matrix on `q=2m>=4` residual vertices.  Write `h` for
its hafnian, `c` for the edge-indexed principal two-deletion cofactors, and
`D` for the edge-indexed Hessian of the hafnian.  Then

```text
D A=(m-1)c.                                             (1)
```

At the all-one graph, `D` is `(q-5)!!` times the adjacency matrix of the
Kneser graph `KG(q,2)`.  Its determinant is

```text
((q-5)!!)^(binom(q,2)) binom(q-2,2) (-(q-3))^(q-1),    (2)
```

which is nonzero in characteristic zero.  Thus the full-edge torus contains
an etale point of the principal-cofactor polar map.  Principal cofactors,
even when restricted to full-support residual graphs, satisfy no universal
polynomial equation.

On the open set `det D!=0`, the **joint** first and second cofactor data
recover every residual edge rationally:

```text
A=(m-1)D^(-1)c.                                        (3)
```

This reconstruction is necessary but not sufficient for an arbitrary
numerical pair `(c,D)`.  The theorem below gives a complete
determinant-cleared necessary-and-sufficient system for the observed jet
`(h,c,D)`.  Its nonlinear hafnian-deck equations are essential.  Symmetry,
Kneser support, Euler's equation, and equality of the three entries belonging
to each four-vertex set do **not** by themselves prove representability.

This is a new exact obstruction interface for the arbitrary-order two-port
programme.  It does not show that a hypothetical Krenn--Gu witness exposes
the complete labeled scalar jet, and it does not force that jet to violate
the equations.  The global conjecture remains **UNRESOLVED**.

No graph, support, matching family, or parameter grid is enumerated.

## 1. Hafnian jet and Euler identities

Let `K` be a characteristic-zero field, let `Q` be a named set of order
`q=2m>=4`, and let

```text
E=binom(Q,2),                    N=|E|=binom(q,2).
```

For an edge `e={i,j}`, let `a_e=A_ij`.  Put

```text
h(A)=haf(A),
c_e(A)=partial_e h=haf(A[Q minus e]),
D_ef(A)=partial_f c_e.                                (4)
```

The second derivative has the exact deletion form

```text
D_ef(A)=0                                      if e intersects f,
D_ef(A)=haf(A[Q minus (e union f)])             if e and f are disjoint.
                                                               (5)
```

Consequently `D` is symmetric.  If a four-set has its three partitions

```text
{i,j}|{k,l},       {i,k}|{j,l},       {i,l}|{j,k},    (6)
```

then the corresponding three entries of `D` are equal: all three are the
same principal four-vertex-deletion hafnian.

The polynomial `c_e` is homogeneous of degree `m-1`.  Euler's identity,
applied once to every component of `c`, gives

```text
D(A)a=(m-1)c(A).                                      (7)
```

Euler's identity for the degree-`m` polynomial `h` gives the second stress

```text
a^T c(A)=m h(A).                                      (8)
```

These are formal polynomial identities.  Characteristic zero is needed
below only when dividing by the displayed integers and when using the
nonzero determinant certificates.

## 2. The all-one Kneser spectrum

Let `J` denote the residual graph with `a_e=1` for every edge.  If `e,f` are
disjoint, deleting their four endpoints leaves `q-4` vertices and therefore

```text
D_ef(J)=(q-5)!!.
```

Intersecting entries vanish, so

```text
D(J)=(q-5)!! K_q,                                    (9)
```

where `K_q` is the adjacency matrix of `KG(q,2)`.

### Theorem 1 (self-contained spectrum)

Over characteristic zero, the spectrum of `K_q` is

```text
binom(q-2,2)       with multiplicity 1,
-(q-3)             with multiplicity q-1,
1                  with multiplicity q(q-3)/2.        (10)
```

### Proof

The constant edge vector has eigenvalue `binom(q-2,2)`, the number of edges
disjoint from a fixed edge.

Choose vertex scalars `u_i` with `sum_i u_i=0` and put

```text
x_ij=u_i+u_j.
```

For a fixed edge `{i,j}`, every remaining vertex occurs in exactly `q-3`
disjoint edges.  Hence

```text
(K_q x)_ij=(q-3) sum_(r notin {i,j}) u_r
           =-(q-3)(u_i+u_j).                          (11)
```

This gives a `(q-1)`-dimensional eigenspace.

Finally take an edge vector `x` whose unsigned sum at every vertex is zero.
Its total edge sum is zero.  Inclusion--exclusion around `{i,j}` gives

```text
(K_q x)_ij
 =sum_e x_e-sum_(e incident i)x_e-sum_(e incident j)x_e+x_ij
 =x_ij.                                               (12)
```

The unsigned vertex-edge incidence matrix has rank `q` in characteristic
zero, so this last space has dimension `N-q=q(q-3)/2`.  The three dimensions
sum to `N`, proving (10).

Multiplying the eigenvalues proves (2).  With the convention `(-1)!!=1`,
the formula includes `q=4`.

### Corollary 2 (full-torus etaleness and the cofactor-only no-go)

The principal-cofactor map

```text
Phi: A^N -> A^N,              A |-> c(A)              (13)
```

has Jacobian `D(A)`.  Equation (2) shows that it is etale at the all-one
point, which lies in the full-edge torus `(K^*)^N`.  Therefore the image of
the torus is Zariski dense, `Phi` is dominant and generically finite, and
there is no nonzero polynomial relation satisfied by every cofactor vector
of a full-support residual graph.

This complements
`HAFNIAN_PRINCIPAL_COFACTOR_GRADIENT_DOMINANCE.md`, whose etale certificate
is a sparse single-perfect-matching point.  The present calculation places
the certificate inside the full-edge torus and supplies the symmetric exact
determinant (2).  Neither theorem says that `Phi` is globally injective or
birational.

Over a field of positive characteristic, (2) remains the integer determinant
formula, but the all-one certificate can vanish.  It is invertible precisely
when the characteristic divides none of

```text
(q-5)!!,       q-3,       binom(q-2,2).               (14)
```

No positive-characteristic conclusion is used here.

## 3. Rational reconstruction from the first two cofactors

### Theorem 3 (joint-jet reconstruction)

At every point with `delta=det D(A)!=0`, the edge vector is uniquely
recovered from the pair `(c,D)` by

```text
a=(m-1)D^(-1)c.                                       (15)
```

Moreover the scalar hafnian is then forced by

```text
m delta h=(m-1)c^T adj(D)c.                           (16)
```

### Proof

Equation (15) is (7) with `D` inverted.  Substitute (15) into (8), and use
`D^(-1)=adj(D)/delta`, to obtain (16).

The pair `(c,D)` therefore has a rational inverse on its actual image inside
`delta!=0`.  This is stronger than local inversion of `c` alone, but it does
not make an arbitrary pair representable: a proposed `D` still has to be the
hafnian Hessian of the reconstructed `A`.

## 4. Complete determinant-cleared open-jet equations

Now start from candidate data

```text
(h,c,D) in K x K^E x Mat_(E x E)(K),       delta=det D!=0. (17)
```

Define an edge vector and hollow symmetric matrix by

```text
b=(m-1)adj(D)c,                  B_e=b_e.              (18)
```

Thus the only possible residual graph is `A=B/delta`.

### Theorem 4 (open-jet integrability, exact iff)

The candidate `(h,c,D)` equals

```text
(haf(A), (partial_e haf(A))_e,
 (partial_e partial_f haf(A))_(e,f))                  (19)
```

for a hollow symmetric residual matrix `A` if and only if all of the
following hold:

1. `D` is symmetric, `d_ef=0` whenever `e` and `f` intersect, and the three
   disjoint pairings (6) have equal entries for every four-set;
2. for every disjoint edge pair `e,f`,

   ```text
   delta^(m-2) d_ef
      =haf(B[Q minus (e union f)]);                    (20)
   ```

3. the scalar stress is

   ```text
   m delta h=(m-1)c^T adj(D)c.                        (21)
   ```

Condition 2 already implies the three-pairing equality in condition 1.  It
is displayed separately because that equality is the immediately observable
linear deck symmetry, whereas (20) is the essential nonlinear
representability equation.

### Proof

Necessity is direct.  If the data come from `A`, equation (7) gives

```text
b=(m-1)adj(D)c=delta a,                               (22)
```

so homogeneity of the order-`q-4` hafnian gives (20).  Equation (21) is
(16), and the support and equality conditions are (5)--(6).

Conversely, put `A=B/delta`.  For disjoint `e,f`, equation (20) gives

```text
haf(A[Q minus (e union f)])
 =delta^(-(m-2))haf(B[Q minus (e union f)])
 =d_ef.                                               (23)
```

For intersecting pairs, both the hafnian second derivative and `d_ef`
vanish.  Hence

```text
D=D(A).                                               (24)
```

By construction and `delta!=0`,

```text
A=(m-1)D^(-1)c,
D(A)A=(m-1)c.                                         (25)
```

Euler applied to the genuine cofactor vector `c(A)` also gives
`D(A)A=(m-1)c(A)`.  Since characteristic zero and `m>=2`, subtraction yields

```text
c=c(A).                                               (26)
```

Finally Euler for `haf(A)`, together with (21), gives `h=haf(A)`.  This
proves sufficiency.

Equation (20) is polynomial in the observed data: `b` is polynomial in
`(c,D)`, and no inverse occurs.  It is therefore an exact characteristic-zero
obstruction, not a numerical reconstruction test.

## 5. Why the visible linear shell is not sufficient

The support and three-pairing equalities identify a symmetric candidate `D`
with one free scalar `y_S` for every four-set `S subset Q`:

```text
d_ef=y_(e union f)              for e disjoint f.     (27)
```

This linear space has dimension `binom(q,4)`.  It contains invertible points
because the all-one Kneser point is invertible.

The actual Hessian-deck map

```text
A^binom(q,2) -> A^binom(q,4),
A |-> (haf(A[Q minus S]))_(|S|=4)                     (28)
```

has image dimension at most `binom(q,2)`.  For every `q>=8`,

```text
binom(q,4)>binom(q,2).                                (29)
```

Therefore a generic invertible array satisfying every linear Kneser-support
and four-set equality condition is not a hafnian Hessian.  The nonlinear
equations (20), or an equivalent elimination ideal, cannot be discarded.

The small orders make the boundary exact.

- At `q=4`, every genuine Hessian has disjoint entries exactly `1`; even a
  nonzero scalar multiple of `KG(4,2)` usually fails representability.
- At `q=6`, the four-set value is the weight of the complementary edge, so
  the linear deck symmetry does reconstruct `D` from an arbitrary `A`.
- Starting at `q=8`, the four-set values are genuine quadratic or higher
  hafnians and carry nonlinear compatibility.

Euler's equation also cannot repair a false `D`: it merely defines the only
possible `A` after `D` is inverted.  Equation (20) is the check that taking
the Hessian of that reconstructed `A` returns the proposed `D`.

## 6. Interface with the two-port decomposition

The arbitrary-residual two-port formula is

```text
H_uv=h B_uv+R_u^T C(A)R_v.                            (30)
```

If a legal chart exposes the labeled scalar `h`, every labeled cofactor
`c_e`, and every labeled second cofactor `d_ef` from one common residual
graph, then Theorem 4 is a complete test on `det D!=0`:

```text
observed (h,c,D)
 -> form delta and B
 -> test the determinant-cleared hafnian deck (20)
 -> test the scalar stress (21)
 -> either exact obstruction or unique reconstructed A. (31)
```

Passing the common-Gram rank equations is much weaker: a generic symmetric
middle form is not required to satisfy (20).  Passing the three-pairing
equalities is also weaker for `q>=8` by (29).

`HIGHER_RESIDUAL_PERMANENTAL_TOMOGRAPHY_NESTED_COFACTOR_STRESS_AND_CUMULANT_INTERFACE.md`
gives a complete nested integrability criterion when every even principal
cofactor depth is reconstructed through invertible permanental compounds.
The present theorem is complementary.  On `det D!=0`, just the first two
cofactor decks reconstruct `A`; equation (20) tests their self-consistency
by evaluating the required lower hafnians on that reconstructed graph.
It therefore avoids assuming that all intermediate observed depths are
available.  Conversely, it gives no replacement on `det D=0`, where the
full nested tower may still carry information.

The outstanding physical problem is observability.  Current root-jet results
often expose only a cofactor span or a compressed tensor, not the complete
synchronously labeled pair `(c,D)`.  The theorem must not be applied after
arbitrary label mixing or across unrelated contractions.

`SHALLOW_HAFNIAN_HESSIAN_TWO_DECK_INVERSION_AND_P7_LEGAL_SENSOR_INTERFACE.md`
specializes the same Hessian inverse to one legal eight-vertex P7 shore and
an omitted-vertex star system; the present note supplies the additional
open-jet representability equations that its reconstruction must satisfy.

## 7. Literature interface

The gradient map of a homogeneous form is its classical polar map; the
distinction between a generically finite polar map and a birational
homaloidal map is standard in Dolgachev's
[*Polar Cremona transformations*](https://arxiv.org/abs/math/0005048).
Here the nonzero Hessian proves only dominance and generic finiteness of the
cofactor polar map, not birationality.

Maeno and Watanabe's
[*Lefschetz elements of Artinian Gorenstein algebras and Hessians of
homogeneous polynomials*](https://arxiv.org/abs/0903.3581) characterizes
Lefschetz elements using higher Hessians.  Numata's
[*The Lefschetz property for an algebra defined by matchings*](https://arxiv.org/abs/2302.11039)
places weighted matching generating functions in a directly neighboring
Artinian-Gorenstein setting.  These works motivate treating (2) as a
Lefschetz-type nondegeneracy certificate; the self-contained spectrum proof
is what establishes the certificate here.

Chaput and Sabatino's study of
[*homaloidal polynomial functions and prehomogeneous vector
spaces*](https://arxiv.org/abs/1011.5975) is only a polar-map analogy.
Homaloidal means birational polar map.  Equations (2)--(3) prove that the
hafnian polar map is etale on a nonempty open and that its **two-jet** has a
rational inverse; they do not prove that the first cofactor map alone is
birational.

Branden--Huh Lorentzian theory must not be imported here.  A nonzero
Lorentzian polynomial has a Hessian with exactly one positive eigenvalue on
the positive orthant
([*Lorentzian polynomials*](https://arxiv.org/abs/1902.03719)).  By (10),
the all-one hafnian Hessian has positive multiplicity

```text
1+N-q,
```

which is already three at `q=4` and is larger thereafter.  Thus the present
nonvanishing is not a Lorentzian-signature theorem, and Lorentzian
log-concavity or Hodge--Riemann consequences do not follow.

The cited theories provide translations and warnings, not black boxes:
(5), the Kneser spectrum, the determinant, and the integrability iff are
proved directly.

## 8. Exact frontier and UNKNOWN wall

```text
arbitrary-order Hessian deletion formula:            PROVED;
all-one Kneser spectrum and determinant:              PROVED;
full-edge-torus etale cofactor chart:                 PROVED;
cofactor-only universal polynomial obstruction:       IMPOSSIBLE;
(c,D) rationally reconstruct A on det D!=0:           PROVED;
determinant-cleared (h,c,D) integrability iff:         PROVED;
four-set equality alone sufficient at q=6:            YES FOR D-DECK;
four-set equality alone sufficient at q=4:            NO WITHOUT NORMALIZATION;
four-set equality alone sufficient at q>=8:           NO GENERICALLY;
global injectivity of cofactor map:                    NOT CLAIMED;
legal labeled (h,c,D) exposure on a P7 eight-shore:  PROVED ON SENSOR OPEN;
legal complete labeled (h,c,D) exposure in P5/P6:     ABSENT IN CURRENT JETS;
GHZ incidence meets the legal P7 sensor/Hessian open: UNKNOWN;
GHZ forces a violation of (20) or (21):                UNKNOWN;
coordinate-boundary replacement for det D=0:          UNKNOWN;
global Krenn--Gu:                                      UNRESOLVED.       (32)
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_residual_hafnian_hessian_kneser_etale_and_jet_integrability.py
python claims/arbitrary-order/audit_residual_hafnian_hessian_kneser_etale_and_jet_integrability.py
python -m py_compile claims/arbitrary-order/verify_residual_hafnian_hessian_kneser_etale_and_jet_integrability.py claims/arbitrary-order/audit_residual_hafnian_hessian_kneser_etale_and_jet_integrability.py
uv run --with ruff ruff check claims/arbitrary-order/verify_residual_hafnian_hessian_kneser_etale_and_jet_integrability.py claims/arbitrary-order/audit_residual_hafnian_hessian_kneser_etale_and_jet_integrability.py
```

The primary replay differentiates the generic six-vertex hafnian, checks the
exact Kneser determinants at `q=4,6,8`, and verifies the reconstructed and
determinant-cleared equations on a fixed nonconstant exact six-vertex graph.
The independent no-import audit uses a separately written hafnian recurrence,
Bareiss determinant, and rational elimination.  Both also check the `q=4`
scaled-Kneser false control.  These are fixed exact audits of the formulas;
the proofs above are arbitrary order.
