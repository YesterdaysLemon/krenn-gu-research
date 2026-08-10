# Block-square-zero Wick completion and the synchronous Fermat shadow

## Status

**Verified characteristic-zero arbitrary-order translation theorem.**  The
complete family of coloured partial matching tensors is an exponential of one
quadratic element in a vertex-exclusive square-zero algebra.  Equivalently,
its square-zero logarithm has no terms above degree two.  This converts the
remaining local-to-global question into a precise quadratic-logarithm
completion problem.

A second theorem pulls any hypothetical Krenn--Gu witness onto the
synchronous ternary slice.  The resulting scalar form is the hafnian of a
matrix of ternary quadrics and must be the Fermat form.  The Fermat apolar
ideal then gives three compact mixed-Hessian identities involving actual
double-deletion hafnian cofactors at every order.

These are necessary structural conditions and a complete characterization
when the whole partial moment family is supplied.  They do **not** prove that
a partial cofactor frame has or has no completion, do not exclude the current
Hall-satisfying `P_7` deformation space, and do not prove the global
conjecture.

## 1. The vertex-exclusive Wick algebra

Let `K` be a characteristic-zero field, let `V` be a finite vertex set, and
let `C={0,...,d-1}` be the colour set.  Work in

```text
A_V = K[x_(i,a) : i in V, a in C]
      / <x_(i,a) x_(i,b) : i in V, a,b in C>.          (1)
```

Thus a nonzero monomial chooses at most one colour at every vertex.  Write
`m` for the ideal of positive-degree elements.  It is nilpotent, so `exp`
and `log` are finite mutually inverse polynomials on `m` and `1+m`.

Let the loopless symmetric block system satisfy

```text
W_ji[b,a] = W_ij[a,b].
```

Define

```text
Q_W = sum_(i<j) sum_(a,b in C)
          W_ij[a,b] x_(i,a) x_(j,b),                  (2)

M_W = exp(Q_W) in A_V.                                (3)
```

For `S subset V` and `alpha:S->C`, let

```text
T_(W,S)(alpha)
  = sum_(perfect matchings P of S)
      product_({i,j} in P) W_ij[alpha(i),alpha(j)],    (4)
```

with value one on the empty set and zero on odd sets.

### Theorem 1 (block-square-zero Wick exponential)

In `A_V`,

```text
M_W
 = sum_(S subset V) sum_(alpha:S->C)
       T_(W,S)(alpha) product_(i in S) x_(i,alpha(i)). (5)
```

Indeed, a term of `Q_W^r` survives (1) exactly when its `r` edges are
vertex-disjoint.  Every coloured matching occurs in all `r!` edge orders,
and the denominator in `Q_W^r/r!` cancels that multiplicity.  This proves
(5) without a positivity assumption and over every characteristic-zero
field.

The ordinary formal-Gaussian statement is the same identity before the
one-colour-per-vertex quotient: (4) is a Wick moment.  The quotient (1) is
the additional structure needed for the one-photon-per-spatial-mode slice.

## 2. A complete logarithmic representability criterion

Let

```text
M = 1 + sum_(nonempty S, alpha:S->C)
          m_(S,alpha) product_(i in S) x_(i,alpha(i))  (6)
```

be arbitrary in `1+m`.  Define its block cumulants by

```text
kappa_(S,alpha) = [x_(S,alpha)] log M.                 (7)
```

Expanding the logarithm and grouping ordered set partitions gives

```text
kappa_(S,alpha)
 = sum_(pi in Partitions(S))
     (-1)^(|pi|-1) (|pi|-1)!
     product_(B in pi) m_(B,alpha restricted to B).   (8)
```

### Theorem 2 (Wick completion criterion)

The coefficient family in (6) is the complete partial matching family of a
unique loopless block system `W` if and only if

```text
kappa_(S,alpha) = 0 whenever |S| != 2.                (9)
```

When (9) holds, the unique edge blocks are

```text
W_ij[a,b] = kappa_({i,j},(a,b)).                      (10)
```

Proof: condition (9) says exactly that `log M` is the quadratic `Q_W` in
(2).  Applying `exp` proves sufficiency and uniqueness; Theorem 1 proves
necessity.

For example, the first two nontrivial equations are

```text
m_1234 = m_12 m_34 + m_13 m_24 + m_14 m_23,           (11)

m_123456
 - sum_(2+4 partitions) m_2 m_4
 + 2 sum_(2+2+2 partitions) m_2 m_2 m_2 = 0,          (12)
```

with the inherited colour assignments understood.  Equation (11) is the
four-point Wick relation.  Equation (12) is its first genuine
cross-subset compatibility equation.  All higher equations are supplied
uniformly by (8), rather than by a support-shell census.

This pinpoints the current gap.  The arbitrary lower mixed-jet theorem fixes
parts of a candidate family `m_(S,alpha)`.  Simultaneous principal-hafnian
realizability asks whether the unspecified coefficients can be filled so
that every known coefficient is retained and every forbidden cumulant in
(8) vanishes.  The local support and span no-go constructions need not pass
this completion test.

## 3. The synchronous ternary shadow

Now take `d=3` and `|V|=n=2m`.  For `t=(t_0,t_1,t_2)`, put

```text
q_ij(t) = t^T W_ij t,
Q(t)_ij = q_ij(t),   Q(t)_ii=0,                       (13)

F_W(t) = haf(Q(t)).                                  (14)
```

Contracting every local leg of the full matching tensor against the same
vector `t` gives

```text
F_W(t) = T_W(t,...,t).                               (15)
```

Consequently a Krenn--Gu witness would satisfy the necessary identity

```text
haf([t^T W_ij t]_(i,j in V))
   = t_0^n + t_1^n + t_2^n.                          (16)
```

Thus the synchronous shadow is a pullback of the universal hafnian along a
quadratic Veronese matrix map, while its target is the rank-three Fermat
form.  This is weaker than the full tensor identity because it groups local
colour words, but it includes every off-diagonal colour entry of every edge
block and is therefore a legal necessary test.

### Theorem 3 (compact Fermat/apolar test)

Let `F` be any ternary homogeneous form of degree `n>=2`.  Then

```text
F = t_0^n+t_1^n+t_2^n                              (17)
```

if and only if

```text
F(e_0)=F(e_1)=F(e_2)=1,
partial_a partial_b F = 0 for 0<=a<b<=2.             (18)
```

In characteristic zero, a monomial involving two different variables is
detected by at least one mixed second derivative.  Hence the three Hessian
conditions leave only pure powers, and the three evaluations normalize
their coefficients.

Equivalently, the apolar ideal of the Fermat form contains the quadratic
ideal

```text
<partial_0 partial_1,
 partial_0 partial_2,
 partial_1 partial_2>,                               (19)
```

and is completed in top degree by

```text
partial_0^n-partial_1^n,
partial_0^n-partial_2^n.                             (20)
```

For a hypothetical witness, the pure evaluations in (18) are the three
monochromatic amplitudes.  The new symbolic content is therefore the three
polynomial mixed-Hessian equations.

## 4. The mixed-Hessian cofactor equations

Write `E(V)` for the unordered vertex pairs.  For an edge `e`, let `V-e`
mean deletion of its two endpoints.  Put

```text
h_e(t)    = haf(Q(t)[V-e]),
h_(e,f)(t)= haf(Q(t)[V-e-f])                          (21)
```

for disjoint edges `e,f`.  Differentiating the hafnian matching expansion
gives, for all coordinate directions `a,b`,

```text
partial_a partial_b F_W(t)
 = sum_(e in E(V))
       (partial_a partial_b q_e) h_e

   + sum_({e,f} disjoint)
       ((partial_a q_e)(partial_b q_f)
        +(partial_b q_e)(partial_a q_f)) h_(e,f).     (22)
```

Therefore every witness must obey the following three arbitrary-order
identities in `K[t_0,t_1,t_2]`:

```text
0 = right_hand_side_of_(22)  for (a,b)=(0,1),(0,2),(1,2).
                                                               (23)
```

Unlike a support-saturation condition, (23) uses the actual values of the
one-edge and two-edge deletion hafnians.  It is precisely of the type left
open by the arbitrary lower mixed-jet cofactor-frame theorem.  It also
packages all synchronously grouped mixed words at once.

More generally, repeated polarization has a closed symbolic form.  Partition
the derivative labels into blocks of size one or two, inject those blocks
into pairwise vertex-disjoint graph edges, differentiate the assigned edge
quadric once or twice according to the block size, and multiply by the
hafnian after deleting all assigned endpoints.  Summing these terms gives
the corresponding derivative of `F_W`.  Every mixed coordinate polarization
of the Fermat target vanishes.  This is the loop-hafnian/Hermite companion to
(22), but (18) shows that the second-order equations already characterize
the entire synchronous shadow.

## 5. Boundary-preserving Holant translation

There is an exact tensor-network formulation that keeps the no-herald rule
visible.  Give every virtual edge the alphabet

```text
{vacuum,0,1,2}.                                       (24)
```

On an edge `{i,j}`, use the binary signature

```text
E_ij(vacuum,vacuum)=1,
E_ij(a,b)=W_ij[a,b],
```

with all mixed vacuum/colour entries zero.  At vertex `i`, use a physical-
qutrit ExactOne router: it outputs colour `c` exactly when one incident
virtual leg has state `c` and every other incident leg is vacuum.  Contracting
all virtual legs chooses exactly one occupied edge at every vertex, hence a
perfect matching, and returns precisely `T_W` on the open physical legs.

Thus Krenn--Gu asks whether qutrit equality/GHZ lies in the
**boundary-preserving transversal Holant species** generated by arbitrary
binary edge tensors and these ExactOne routers.  Boundary-preserving means
that every physical leg remains open: unary caps, pins, herald measurements,
and physical traces are forbidden.  Conservative Holant-clone results that
adjoin arbitrary unary signatures therefore address a strictly larger
closure problem.

## 6. What the literature transfers, and what does not

The original problem is the weighted perfect-matching restriction problem
of Krenn--Gu--Soltesz
([arXiv:1902.06023](https://arxiv.org/abs/1902.06023)).  The direct
hafnian/Gaussian correspondence is standard in Gaussian boson sampling
([arXiv:1612.01199](https://arxiv.org/abs/1612.01199)), and Gaussian moment
varieties place moment parametrizations into algebraic geometry
([arXiv:1510.04654](https://arxiv.org/abs/1510.04654)).  Theorem 1 adds the
vertex-exclusive quotient needed here; Theorem 2 identifies the exact
completion equations in that quotient.

Efimov's sum-of-matrices hafnian formula
([arXiv:2101.09722](https://arxiv.org/abs/2101.09722)) is the scalar
two-summand relative of the exponential/convolution viewpoint.  The
repository's hafnian convolution-split lemma is recovered by extracting a
fixed bidegree from `exp(Q_L)exp(Q_L)=exp(2Q_L)`.  Formula (8) retains the
whole labelled and coloured lower-subset family and is therefore the form
suited to gluing.

The synchronous pullback (16) points toward apolarity and the geometry of
powers of quadrics.  Recent work determines apolar ideals and decompositions
for powers of quadrics
([arXiv:2411.03161](https://arxiv.org/abs/2411.03161)) and studies border rank
for powers of ternary quadrics
([arXiv:2208.07921](https://arxiv.org/abs/2208.07921)).  Our source is not one
power `q^m`: it is a sum, indexed by perfect matchings, of products of `m`
edge quadrics.  What transfers immediately is the apolar method, not those
classification theorems verbatim.  Equations (18)--(23) are the safe first
transfer.

Photon-number cumulants of Gaussian states are expressible through connected
cycle sums (the Montrealer)
([arXiv:2212.06067](https://arxiv.org/abs/2212.06067)).  That suggests a
connected-diagram refinement, but photon-number observables are quadratic
and differ from the present transversal linear moments.  The direct rigorous
cumulants here are (8); importing a Montrealer identity without changing the
observable would be invalid.

Planar matchgate signatures satisfy Pfaffian matchgate identities, with a
necessary-and-sufficient characterization in
[arXiv:1303.6729](https://arxiv.org/abs/1303.6729).  The arbitrary-graph
bosonic hafnian family here has no Pfaffian signs, and the repository already
contains locally independent principal-cofactor frames.  Spinor/Pluecker
equations therefore cannot be assumed.  Their safe role is as a comparison
class: any proposed transfer must first prove a bosonic identity such as
(8), (22), or a specialization thereof.

Finally, tensor-network varieties provide the right global algebraic setting
for polynomial images and their boundary behavior
([arXiv:1105.4449](https://arxiv.org/abs/1105.4449)), while tensor-network
contractions can encode invariant polynomials
([arXiv:1209.0631](https://arxiv.org/abs/1209.0631)).  In that language,
Theorem 2 says that the hidden partial-signature extension must lie in the
log-quadratic matching subvariety, not merely in the product of its local
projection images.

Holant-clone theory formalizes gadget expressibility and shows explicitly
how adjoining unary signatures changes a clone
([arXiv:1811.00817](https://arxiv.org/abs/1811.00817)); the tensor-network/
quantum-entanglement dictionary for Holant problems is developed in
[arXiv:2004.05706](https://arxiv.org/abs/2004.05706).  These sources motivate
the closure language, while the boundary-preserving restriction above is the
problem-specific condition that prevents heralds from being smuggled in.

## 7. Next symbolic target

Do not enlarge the `P_7` support shell.  Pull the known arbitrary lower
mixed-jet cofactor frames into (22), in this order:

1. impose one mixed Hessian, say `(a,b)=(0,1)`, on the two-residual axis cell;
2. quotient by the already classified diagonal frame and retain actual
   `h_e,h_(e,f)` values;
3. test whether the three equations (23) force a forbidden cumulant (8) on
   one four- or six-vertex deletion set;
4. if they do not, record the resulting log-quadratic completion as a genuine
   symbolic survivor and move to the next polarization.

This is an arbitrary-order local-to-global programme.  Its unit of progress
is a proved cumulant or polar incompatibility, not another incidence count.

## Verification

Run from the repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_block_square_zero_wick_completion.py
python claims/arbitrary-order/audit_block_square_zero_wick_completion.py
```

The primary verifier checks the exponential coefficient theorem and
logarithmic criterion symbolically on a generic four-vertex/two-colour
family, derives the mixed-Hessian cofactor formula for a generic
four-vertex ternary quadratic system, and checks the compact Fermat test.
The independent audit uses only the Python standard library, exact integer
arithmetic, and a separately written sparse vertex-exclusive algebra.  It
checks `log(exp(Q))=Q`, reconstructs all partial moments from the cumulants,
and checks (22) by exact polynomial differentiation on six vertices.  These
finite checks audit the implementations; the proofs above are
arbitrary-order.
