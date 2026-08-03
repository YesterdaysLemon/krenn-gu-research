# Hamming-face pinching and the radius-two chord-completion no-go

## Status

**Exact arbitrary-port coefficient identity and exact cross-coefficient
exclusion of the completed `m=6` conformal `K_3,3` model.**  One forbidden
coefficient can realize the nonzero bosonic Plucker defect.  Its Hamming
neighbours cannot all do so.

Replacing selected port rows by singleton diagonal rows gives a principal-
minor formula on the whole Hamming face.  The exact `Q(sqrt(2))` bypass
survives the three nonautomatic distance-one equations because its three
principal `2 x 2` permanents vanish.  Any distance-two flip, however, leaves
one nonzero diagonal entry and therefore isolates a unique nonzero matching.

The same argument excludes, at arbitrary order, a coefficient-induced
completed theta whose three excess cells form the diagonal matching of its
conformal `K_3,3`.  It does not yet force an arbitrary conformal carrier to
be coefficient-induced or its excess cells to have that incidence.

The input is
[`ARBITRARY_PERMANENT_THREE_EXCESS_BOSONIC_PLUCKER_DEFECT_THEOREM.md`](ARBITRARY_PERMANENT_THREE_EXCESS_BOSONIC_PLUCKER_DEFECT_THEOREM.md).

## The Hamming-face pinch identity

Fix `k` port modes `a_1,...,a_k`, port sources `p_1,...,p_k`, and a base
word.  Assume **face-stable factorization**: at both the base and alternate
colours, every port row is supported only on the `k` port sources, while the
fixed exterior row/source block is independent of the selected alternates
and has coefficient

```text
C=per(Z)!=0.                                          (1)
```

Bottom-left exterior-to-port cells may exist, but cannot be used because the
port rows already consume every port source.  Thus the base coefficient is
`C per(X)`, where `X=(x_ij)` is the port matrix.  Assume `x_ii!=0`.  For each
port row `i`, suppose an alternate input colour makes exactly its diagonal
cell eligible, with nonzero value `z_i`.

For `S subset [k]`, let `w_S` be the word obtained by applying that alternate
colour at precisely the rows in `S`.  Then

```text
Coeff(w_S)
  = C (product_(i in S) z_i) per X_(S^c,S^c).      (2)
```

Indeed, every replaced row is forced to its distinct source `p_i`.  Delete
those rows and columns.  The other port rows contribute exactly the
principal complementary permanent, while the exterior coefficient is
unchanged.  This proves (2) for arbitrary `k`; it is not a finite check.

Equivalently, interpolate between the base and alternate local coordinates
with variables `t_i`.  The whole face has generating polynomial

```text
C per(X+diag(z_1t_1,...,z_kt_k)),                  (2a)
```

and the coefficient of `product_(i in S)t_i` is (2).  If the selected
product subspace is apolar to `Delta_3`, (2a) would have to be the zero
polynomial, although its top coefficient is `C product_i z_i!=0`.

In particular, for `S=[k] minus {j}`,

```text
Coeff(w_S)=C (product_(i!=j) z_i) x_jj !=0.         (3)
```

Therefore, if even one such co-singleton word is forbidden by the target,
the proposed coefficient face is impossible.

Equation (2) is also a tensor-contraction statement.  The permanent
restriction tensor is a sum of rank-one matching tensors.  Choosing a local
dual coordinate that annihilates every row cell except one contracts the
matching tensor to a principal permanent.  We call this operation
**Hamming-face pinching**.

## Exact radius ledger for the completed `K_3,3` model

In the six-token model, keep

```text
w(b_i)=i+2,
```

so `b_iq_i` is forced with nonzero weight `d_i`.  At the `a` rows, start
with `w(a_i)=i`; the port matrix is the bypass

```text
X = [ 1,        1, 1-sqrt(2) ]
    [ -1,       1,           1 ]
    [ 1+sqrt(2),-1,           1 ].                 (4)
```

Changing `w(a_i)` from `i` to `i+2` leaves only the excess cell

```text
E_i=a_ip_i
```

with nonzero value `z_i`.  Put `D=d_0d_1d_2`.  Formula (2) becomes

```text
C_S=D (product_(i in S) z_i) per X_(S^c,S^c).      (5)
```

Every one of these words is mixed because the unchanged `b` colours are
`2,0,1`.  The radii now have an exact interpretation:

```text
|S|=0:  C_empty=D per(X)=0;
|S|=1:  C_{i}=D z_i P_ii=0;
|S|=2:  C_{i,j}=D z_i z_j x_kk !=0;
|S|=3:  C_{0,1,2}=D z_0z_1z_2 !=0.                (6)
```

With `z_i=1`, the exact face polynomial for (4) is especially simple:

```text
per(X+diag(t_0,t_1,t_2))
  =t_0t_1+t_0t_2+t_1t_2+t_0t_1t_2.                (6a)
```

Its value and all first derivatives vanish at the origin, while every mixed
second derivative equals one.

Thus the bypass genuinely survives every nonautomatic Hamming-distance-one
equation.  The first contradiction is exactly at distance two, where the
coefficient has a unique physical matching.  This excludes the structural
model as a full restriction without checking any collection of input words.

### The complete radius-one torus

The claim about radius one includes all twelve neighbouring words.  Changing
`a_i` to either other colour gives its nonzero diagonal component times the
same principal permanent `P_ii`; the possible cell `a_iq_i` collides with the
forced `b_iq_i`.  Changing a `b_i` colour either creates a source collision
or leaves an uncovered `q` source, so those neighbours vanish structurally.
Consequently the base and all radius-one coefficients vanish exactly when

```text
per(X)=P_00=P_11=P_22=0.                            (6b)
```

On the full-support torus, use the normalized gains `a,b,c,u,v` from the
conformal--Birkhoff reduction.  Equations (6b) become

```text
a=b=c=-1,             u+v=2,             uv=-1.    (6c)
```

Thus

```text
{u,v}={1+sqrt(2),1-sqrt(2)}.                        (6d)
```

Modulo nonzero row and column scaling, these are exactly two points,
interchanged by transpose; (4) represents one.  Any distance-two pinch adds
a nonzero Laurent monomial to the zero ideal and makes the saturated system
inconsistent.  The radius-two obstruction is therefore sharp on the entire
radius-one torus, not only at the displayed matrix.

## Arbitrary-order diagonal-excess `K_3,3` theorem

Now suppose a hypothetical support-`3m+3` restriction has a
coefficient-induced conformal `K_3,3` with mode shore `a_0,a_1,a_2` and
source shore `p_0,p_1,p_2`, satisfying:

1. the three excess cells are the diagonal matching `E_i=a_ip_i`;
2. all nine core cells are eligible in one base word;
3. all six off-diagonal core cells are mandatory coordinate cells;
4. the exterior boundary sectors vanish, leaving a common nonzero exterior
   coefficient `C`.

Write the base colour at `a_i` as `alpha_i`.  Both off-diagonal core cells at
that mode have mandatory colour `alpha_i`.  The diagonal excess cell also
has a nonzero `alpha_i` component.

The core gives degree three at each `a_i`, but only the two local vectors
`e_(alpha_i)` and `E_i`.  Local rank three therefore requires another cell
at each of the three modes.  Since total mode-degree excess is exactly three,
these are the only extra cells: each `a_i` has degree four and every other
mode has degree three.  The extra cell is mandatory, say of colour
`beta_i`.  Rank three forces

```text
beta_i != alpha_i
```

and forces `E_i` to have a nonzero component in the third colour
`gamma_i`.  At colour `gamma_i`, the only eligible cell at mode `a_i` is
therefore `E_i`.  At the base colour `alpha_i`, its only eligible cells are
the three core cells.  Hence the port-to-exterior block vanishes on the
entire base/alternate face; the unchanged exterior block has coefficient
`C`, so the face-stable hypothesis of (1) holds.

Apply the pinch identity with these three alternate colours.  Among the
three two-flip words, at least one is mixed.  Indeed, two such words share
one flipped coordinate, so if both were monochromatic their monochromatic
colours would agree; comparing a coordinate that is base-coloured in one and
alternate-coloured in the other would then force `alpha_i=gamma_i`.  Thus
all three cannot be monochromatic.  For a forbidden one, (3) is nonzero.
This contradiction proves:

```text
coefficient-induced conformal K_3,3
+ diagonal excess matching + support 3m+3 + local rank three
    => impossible in a full P_m -> Delta_3 restriction.         (7)
```

This closes the exact two-chord bypass once coefficient-inducedness and the
diagonal incidence are available.  It does not prove either hypothesis from
the uncoloured conformal-core theorem.

The later boundary-entanglement rank theorem removes the diagonal-incidence
restriction: under exterior decoupling it treats both possible excess-mode
profiles `1+1+1` and `2+1+0`.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_BOUNDARY_ENTANGLEMENT_RANK_THEOREM.md`.

## Relation to apolarity and tensor support

The local alternate colour at `a_i` is an apolar selector: it annihilates the
three other physical row covectors and evaluates nontrivially on `E_i`.
Taking two selectors is a mixed contraction of the global coefficient
tensor.  On the target GHZ tensor

```text
Delta_3=sum_c lambda_c e_c^(tensor m),
```

that mixed contraction vanishes.  On the completed `K_3,3` face it returns
the nonzero monomial (3).  Hamming-face pinching is therefore the exact
apolar obstruction dual to the bosonic Plucker defect: the defect permits
one central cancellation, while the selectors expose its unsupported
neighbouring tensor coordinates.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_three_excess_hamming_face_pinch_theorem.py
python audit_arbitrary_permanent_three_excess_hamming_face_pinch_theorem.py
```

The primary verifier proves the symbolic row-replacement formula for the
three-port face, checks the exact bypass radius ledger, and verifies the
local-rank selector determinant.  The no-import audit reconstructs the
principal-minor and unique-matching ledger in exact quadratic arithmetic.
The arbitrary-`k` identity and arbitrary-order degree proof are the displayed
arguments, not an input-word census.

## Boundary

```text
arbitrary-k Hamming-face identity (2):       PROVED;
completed K_3,3 central coefficient:         CAN VANISH;
all three distance-one pinch coefficients:   CAN VANISH;
distance-two pinch coefficient:              NONZERO;
exact m=6 structural model as restriction:   EXCLUDED;
coefficient-induced diagonal-excess K_3,3:   EXCLUDED AT EVERY ORDER;
coefficient-inducedness from conformality:    NOT PROVED;
diagonal excess incidence forced globally:    NOT PROVED;
exclusion of all support 3m+3 cases:          NOT PROVED;
global Krenn--Gu conjecture:                  UNRESOLVED.
```
