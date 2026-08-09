# Zeon boundary jet packages every permanental boundary sector

## Status

**Exact characteristic-zero all-sector identity.**  This theorem constructs
a matching-compatible boundary-response object without enumerating boundary
sectors.  It packages the empty, elementary, second, and saturated third
boundary layers of the three-port problem as squarefree coefficients of one
permanent under one nilpotent rank-one perturbation.

The construction completes the algebraic packaging requested by the derived
boundary route.  It does not yet supply a target-rank obstruction or prove
that any physical boundary amplitude is nonzero.

## Block matrix and boundary responses

Let `K` be a characteristic-zero field, let `B` be a commutative
`K`-algebra, and let

```text
          P   Q
       +---------+
 A     | X   Y   |
 R     | Z   W   |                              (1)
       +---------+
```

be a matrix over `B`, with

```text
|A|=|P|=d,             |R|=|Q|=n.              (2)
```

For `I subseteq A` and `J subseteq P` with `|I|=|J|=k`, define the
size-`k` **boundary response**

```text
R_(I,J)=sum_(S subseteq R, T subseteq Q, |S|=|T|=k)
          per(Y_(I,T)) per(Z_(S,J))
          per(W_(R\S,Q\T)).                    (3)
```

The convention is that the permanent of the empty matrix is one.  Formula
(3) is exactly the aggregate weight of exterior matchings that cover the
core terminals `I union J`: `Y` matches `I` to `T`, `Z` matches `S` to
`J`, and `W` matches the remaining exterior vertices.

At `k=0`, `R_(empty,empty)=per(W)`.  At `k=1`, the response matrix is the
permanental-cofactor contraction

```text
R_({a_i},{p_j})=(Y C_per(W) Z)_ij.              (4)
```

## The zeon boundary jet

Work in the commuting square-zero, or **zeon**, algebra

```text
Z_(A,P)=B[u_i,v_j : i in A, j in P]
          / (u_i^2,v_j^2 : i in A, j in P).     (5)
```

Put `u_I=product_(i in I) u_i` and `v_J=product_(j in J) v_j`.  Form the
exterior column and row

```text
z(v)=Z v,                 y(u)=u^T Y,            (6)
```

and define the **zeon boundary jet**

```text
J_W(u,v)=per(W+z(v)y(u)) in Z_(A,P).             (7)
```

The perturbation `z(v)y(u)` has rank one before passage to the zeon
quotient.  The quotient makes every terminal marker vertex-exclusive, while
retaining products belonging to distinct terminals.

## Theorem 1: the all-layer coefficient formula

For every `I,J` of common size `k`,

```text
[u_I v_J] J_W(u,v) = k! R_(I,J).                 (8)
```

### Proof

Expand the permanent in (7).  Choose the `k` exterior rows `S` at which an
entry from `z(v)y(u)` is used; the corresponding permanent columns form a
set `T` of size `k`.  Square-zero survival forces the chosen `u` labels to
be a bijection onto `I` and the chosen `v` labels to be a bijection onto
`J`.  The untouched rows and columns contribute
`per(W_(R\S,Q\T))`.

Fix one term counted by (3): a `Y` matching from `I` to `T`, a `Z` matching
from `S` to `J`, and a residual `W` matching.  In the rank-one update, the
`k` removed rows may be paired with the `k` removed columns in any bijection.
There are `k!` such pairings.  For each pairing the `u` and `v` labels are
then forced by the fixed `Y` and `Z` matchings, and the resulting product is
the same.  Conversely every surviving term of `[u_Iv_J]J_W` gives exactly
these data.  Hence every boundary matching has multiplicity `k!`, proving
(8).

The factorial is not a normalization accident.  It is the bosonic
symmetrization multiplicity of pairing the selected entrance and exit
edges through the rank-one perturbation.

## Theorem 2: exact reconstruction of the block permanent

The full block permanent is the finite contraction

```text
per [X Y]
    [Z W]

 = sum_(k=0)^d sum_(|I|=|J|=k)
      per(X_(A\I,P\J)) R_(I,J)                    (9)

 = sum_(k=0)^d (1/k!) sum_(|I|=|J|=k)
      per(X_(A\I,P\J)) [u_Iv_J]J_W(u,v).         (10)
```

Responses with `k>n` are zero, so the displayed upper limit may equivalently
be `min(d,n)`.

### Proof

Partition a perfect matching of the full block matrix by the core rows `I`
sent through `Y` and the core columns `J` reached through `Z`.  Bipartite
balance gives `|I|=|J|`.  Once `I,J` are fixed, the core-internal edges sum
to `per(X_(A\I,P\J))` and all boundary/exterior choices sum to (3).  This
proves (9).  Substitution of (8), using characteristic zero to divide by
`k!`, proves (10).

Thus the boundary convolution is one apolar-style pairing between core
permanental cofactors and the squarefree Taylor coefficients of `J_W`.

## Corollary: the permanental compound tower

Index rows and columns by subsets of size `k`, and define

```text
P_k(Y)_(I,T) = per(Y_(I,T)),
D_k(W)_(T,S) = per(W_(R\S,Q\T)),
P_k(Z)_(S,J) = per(Z_(S,J)).                       (11)
```

If `R^(k)` is the matrix with entries `R_(I,J)`, then (3) is the exact
factorization

```text
R^(k)=P_k(Y) D_k(W) P_k(Z).                        (12)
```

This is a permanental compound tower, not the ordinary exterior-power
compound of determinant theory.  Nevertheless ordinary matrix rank applied
*after* the factorization gives

```text
rank R^(k) <= min(rank P_k(Y), rank D_k(W), rank P_k(Z)) (13)
```

over a field, or after passage to a fraction field when appropriate.  Thus
every graded boundary layer has determinantal flattening equations.  Local
span information can now be imposed on the permanental compounds rather
than discarded by a degree-zero quotient.

## Three-port specialization

For the Krenn--Gu three-excess core, `d=3`; there are only four graded
layers:

```text
degree 0:  [1]J_W                    = per(W),
degree 1:  [u_i v_j]J_W              = R_(i,j),
degree 2:  [u_i u_l v_j v_t]J_W      = 2 R_(i,l;j,t),
degree 3:  [u_0u_1u_2v_0v_1v_2]J_W  = 6 R_(A,P).   (14)
```

Unlike the ordinary product quotient, the jet does not disappear when an
outgoing span fills one port space.  Saturation moves information into the
higher squarefree degrees.  In particular, the top class remains a genuine
coefficient rather than being projected to zero.

This realizes a rigorous all-sector carrier for the saturated one-chord
`2+1+0` model.  It is not yet the proposed derived differential: no boundary
differential, homology class, or target-rank mismatch has been constructed.

## Theorem 3: generic support and physical cancellation

If every supported entry of `Y,Z,W` is replaced by its own algebraically
independent indeterminate, then

```text
R_(I,J) != 0
  iff the boundary graph has a matching covering exactly I union J.       (15)
```

Indeed, (3) is then a sum of distinct matching monomials with coefficient
one.  Thus the squarefree support of `J_W` is precisely the matching
delta-matroid from
`ARBITRARY_PERMANENT_THREE_EXCESS_BOUNDARY_DELTA_MATROID_THEOREM.md`, with
the `k!` coefficients harmless in characteristic zero.

After specialization to physical complex weights, distinct monomials can
cancel.  Therefore a feasible sector may have zero response.  The zeon jet
keeps all amplitude layers but does not turn support feasibility into
physical nonvanishing.

## Literature translation

Commuting square-zero generators are called zeons.  Feinsilver and McSorley
develop their connection with permanents and permanent trace formulas [1].
The repository already uses vertex-exclusive square-zero algebras for full
partial matching families in
`BLOCK_SQUARE_ZERO_WICK_COMPLETION_THEOREM.md` and for exact block selection
in `ROOT_OF_UNITY_BLOCK_PERMANENT_SELECTOR.md`.

The new transfer here is the particular bilinear rank-one update
`(Zv)(u^TY)` and coefficient law (8).  It packages a boundary-response
convolution, not a full hafnian moment family.  Consequently the earlier
log-quadratic Wick completion theorem and this permanental jet theorem are
complementary rather than interchangeable.

Reference:

1. Philip Feinsilver and John McSorley, “Zeons, Permanents, the Johnson
   Scheme, and Generalized Derangements,” *International Journal of
   Combinatorics* (2011), Article 539030,
   [doi:10.1155/2011/539030](https://doi.org/10.1155/2011/539030),
   [arXiv:1710.00788](https://arxiv.org/abs/1710.00788).

## New proof interface

Equations (8)--(12) replace an unstructured list of boundary sectors by one
finite algebra element and one permanental-compound tower.  The next
obstruction can now be formulated without a sector census:

1. impose the exact local span constraints on `P_k(Y)` and `P_k(Z)`;
2. derive cross-degree equations or a differential on the zeon coefficients;
3. contract them with the three-port permanent cofactors as in (10);
4. prove that the diagonal target has an incompatible graded rank, direction,
   or cumulant signature.

The support theorem controls which squarefree coefficients can occur.  The
jet theorem controls how every physical amplitude enters the block
permanent.  The later boundary-jet dominance theorem proves that the
unconstrained response map has no nonzero universal cross-degree polynomial
identity.  What remains must use the coloured/aligned incidence locus or
another genuine restriction on `Y,Z,W`; see
`ARBITRARY_PERMANENT_THREE_EXCESS_BOUNDARY_JET_DOMINANCE_NOGO.md`.

## Scope wall

```text
proved:     every boundary layer is a coefficient of one zeon permanent;
proved:     degree-k coefficient equals k! times the exact response;
proved:     the full block permanent is the contraction (10);
proved:     every response layer has the compound factorization (12);
proved:     generic jet support equals boundary matching feasibility;
constructed: matching-compatible saturated all-sector carrier;
excluded:   any universal unconstrained polynomial ideal among jet degrees;
not proved: an ideal on the coloured/aligned constrained response locus;
not proved: a target-rank/direction contradiction from the jet;
not proved: nonvanishing after specialization to complex weights;
not used:   support-family enumeration, finite fields, numerics;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_arbitrary_permanent_three_excess_zeon_boundary_jet_theorem.py
python claims/arbitrary-order/audit_arbitrary_permanent_three_excess_zeon_boundary_jet_theorem.py
```

The primary verifier checks the complete fixed `2+2` symbolic block identity
and the degree-three factorial.  The independent no-import audit implements
the square-zero algebra directly over integers and reconstructs the block
permanent.  These are proof guards for the arbitrary-size combinatorial proof
above, not a search over graph or coefficient families.
