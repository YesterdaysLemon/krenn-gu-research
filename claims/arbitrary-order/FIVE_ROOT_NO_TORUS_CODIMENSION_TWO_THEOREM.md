# The five-root no-torus locus has codimension at least two

## Status

This is an exact algebraic-geometric strengthening of
[`FIVE_ROOT_TORUS_RESULTANT_DICHOTOMY.md`](FIVE_ROOT_TORUS_RESULTANT_DICHOTOMY.md).
The fifteen degree-108 boundary resultants form a convenient hypersurface
envelope, but none of those hypersurfaces is itself a component of the true
exceptional locus where all five-root solutions lie on the coordinate
boundary.

More precisely, in the projective coefficient space of the ten **nonzero**
bilinear blocks, the Zariski closure of the no-torus locus has codimension at
least two.  A general point of any one boundary-resultant divisor has exactly
one simple solution on that boundary and twenty-three simple solutions in the
coordinate torus.

The projective coefficient space does not contain a zero edge block.  An
induced `K_5` having any zero block is therefore a separate exceptional
branch in every projective application below; no projectivization or
projective-space codimension claim is applied to that branch.  The affine
corollary later includes it only through the codimension-nine zero-block
coordinate subspaces.

This theorem constrains the coordinate-boundary branch.  It does **not** show
that the edge blocks of a hypothetical Krenn--Gu witness avoid the resulting
codimension-two locus, exclude `P_5 -> Delta_3` or `P_6 -> Delta_3`, or rule
out blocker surplus.

## Universal five-root family

Put

```text
X = product_(i=0)^4 P(V_i),       V_i=C^3,
P = product_(ij in E(K_5)) P((V_i tensor V_j)^*).
```

Thus `dim X=10` and `dim P=80`.  Let

```text
Z = {(x,B) in X x P : B_ij(x_i,x_j)=0 for every i<j}.
```

For fixed `x`, each equation cuts one hyperplane in its own `P^8`
coefficient block.  Hence `Z` is a smooth irreducible `(P^7)^10`-bundle over
`X`, of dimension `80`.  The proper projection

```text
pi: Z -> P
```

is generically finite etale of degree

```text
product_(i<j)(h_i+h_j)=24 h_0^2 h_1^2 h_2^2 h_3^2 h_4^2.       (1)
```

In particular `pi` is dominant.  Since it is also proper, it is surjective,
so every coefficient system in `P` has a nonempty five-root scheme.

Let `T` be the coordinate torus in `X`, and write the boundary as

```text
H = X minus T = union_a H_a,
```

where `a=(i,c)` runs over the fifteen vertex/colour pairs and
`H_a={x_i[c]=0}`.  Define

```text
N = {B in P : Z_B intersect T is empty}.                         (2)
```

The set `N` need not be assumed closed in what follows.

For each `a`, let

```text
I_a = Z intersect (H_a x P),
D_a = image(I_a -> P).
```

The earlier boundary-resultant theorem proves that `D_a` is an irreducible
hypersurface and that `I_a -> D_a` has generic degree one.  Its defining
resultant has edge-block degree `12` on the four edges incident with `i`,
degree `10` on the six nonincident edges, and total degree `108`.

## A single resultant generically leaves twenty-three torus roots

Fix `a=(i,c)` and choose a point

```text
x in H_a minus union_(b!=a) H_b.                                (3)
```

Inside `P`, the systems having `x` as a common root form

```text
S_x = product_(e in E(K_5)) P(ker(ev_(e,x))) ~= (P^7)^10,
dim S_x=70.                                                       (4)
```

A general member of `S_x` has no other boundary root.  Here is the exact
dimension count.  For a second boundary point `y!=x`, let `S` be the set of
vertices on which `[y_j]=[x_j]`, and put `s=|S|`.  Evaluation at `x` and `y`
gives two independent linear conditions in an edge block unless both
endpoints lie in `S`; exactly `binomial(s,2)` conditions coincide.  The
coefficient fibre therefore has dimension

```text
10*6 + binomial(s,2).                                           (5)
```

If `s=0`, the boundary point `y` varies in dimension nine, so the two-root
incidence has dimension `69`.  If `1<=s<=4`, its dimension is at most

```text
60 + binomial(s,2) + 2(5-s),
```

whose values are `68,67,67,68`.  Every value is strictly below `70`.
The case `s=5` is the excluded diagonal `y=x`.  Thus the systems in `S_x`
with a second boundary root lie in a proper closed subset: the closure of
the off-diagonal incidence still has dimension at most `69`, and its image
under the projective incidence projection is closed.

The root `x` can be made transverse.  Orient `K_5` as a regular tournament
and assign its two incoming edges at every vertex to the two projective
tangent coordinates there.  The ten edge differentials are then the ten
different coordinate covectors, so the projective tangent Jacobian is a
permutation matrix.  A bilinear block constrained to vanish at `x` can
realize arbitrary endpoint tangent covectors, so this Jacobian pattern occurs
inside `S_x`.  Transversality is therefore a nonempty open condition.

It remains to justify reducedness away from `x` without hiding it in a
Bertini slogan.  On the torus, stratify a second root `y` by the number `s`
of projective factors shared with `x`.  Because `x_i` is on a coordinate
boundary while `y_i` is in the torus, the boundary vertex is never shared,
so `0<=s<=4`.  The same evaluation count gives total incidence dimension

```text
60 + binomial(s,2) + 2(5-s),                                  (6)
```

namely `70,68,67,67,68` for `s=0,1,2,3,4`.  Thus every shared-factor
stratum is proper over `S_x`; only the main `s=0` stratum can dominate.
That main incidence is a smooth `(P^6)^10`-bundle over the smooth open set
of torus points sharing no factor with `x`, and it has the same dimension
`70` as `S_x`.  In characteristic zero, generic smoothness makes its
dominant projection generically etale.  (It must dominate after restricting
to the transverse open: otherwise a general projective fibre would consist
only of the simple point `x`, contradicting the top intersection number
`24`.)  Its non-etale locus is then a proper subset of dimension at most
`69`, so the closure of its coefficient image is also proper.  Hence a
general transverse member of `S_x` has a finite reduced common-zero scheme
away from `x`.

Together with (1), that scheme consists of `x` and twenty-three further
points.  The earlier boundary-incidence count puts all twenty-three further
points in `T`.  At this coefficient point `pi` is quasi-finite and etale at
every point of its fibre.  Properness then supplies a coefficient
neighbourhood on which `pi` is finite, and the proper image of the closed
non-etale locus can be avoided.  Thus this coefficient point lies in a base
open over which `pi` is finite etale.

Consequently every `D_a` meets the finite-etale locus of `pi`, and it has a
dense open subset on which the full five-root scheme consists of one simple
`H_a` root and twenty-three simple torus roots.

## Codimension-two theorem

Let `U subset P` be the union of all base opens over which `pi` is finite
etale.  This is the maximal finite-etale base open; it is nonempty, and the
degree there is `24`.  Put `Sigma=P minus U`.  For each `a`, choose a dense
open `O_a subset D_a` over which the birational map `I_a -> D_a` is an
isomorphism, and let

```text
Exc_a = D_a minus O_a.                                           (7)
```

After shrinking `O_a` if necessary, `Exc_a` is a proper closed subset of
`D_a`.  The construction above shows `D_a` is not contained in `Sigma`.
Therefore every member of the finite union

```text
C = union_a ((D_a intersect Sigma) union Exc_a)                  (8)
```

has codimension at least two in `P`.

We claim `N subset C`.  If `B in N intersect Sigma`, the nonempty five-root
scheme has a boundary point, so `B` lies in some `D_a` and hence in the
first part of (8).  If `B in N minus Sigma`, then `Z_B` consists of twenty-four
distinct boundary points.  Assign to each point one of the fifteen coordinate
hyperplanes containing it.  Since `24>15`, one hyperplane `H_a` contains at
least two distinct roots.  The fibre of `I_a -> D_a` then has at least two
points, so `B in Exc_a`.

Thus

```text
codim_P closure(N) >= 2.                                        (9)
```

In particular, vanishing of one boundary resultant is only a first-order
warning.  A system with no torus root must also satisfy an independent
degeneracy: either the full intersection is outside the finite-etale locus,
or one boundary incidence projection is outside its generic one-root chart.

## Affine coefficient-space corollary

Let

```text
A=(C^9)^10
```

be the full `90`-dimensional affine space of ten `3 x 3` blocks, now allowing
zero blocks, and let `A^o` be the open set where all ten blocks are nonzero.
Independent block projectivization is a smooth quotient

```text
q:A^o -> P
```

with ten-dimensional torus fibres.  The inverse image `q^(-1)(C)` of the
closed envelope (8) has dimension at most `78+10=88`; its affine closure has
the same dimension bound.  The complement `A minus A^o` is the union of the
ten coordinate subspaces on which one whole `3 x 3` block is zero.  Each has
codimension nine.

On `A^o`, the existence of a torus root is invariant under independently
rescaling the ten blocks.  Hence, if `N_A` denotes the affine no-torus locus,

```text
N_A intersect A^o = q^(-1)(N) subset q^(-1)(C).
```

Therefore the affine no-torus locus, including systems with zero blocks, is
contained in

```text
closure_A(q^(-1)(C)) union (A minus A^o),                         (10)
```

a closed set of codimension at least two in `A`.  The zero-block pieces are
still listed separately in applications because they do not define points of
the projective coefficient space, even though they have the stronger affine
codimension-nine bound.

## Consequence for the arbitrary-order blocker route

Apply the theorem to the ten blocks induced by any five vertices of a
hypothetical three-colour witness.  There is first a separate alternative
that at least one of those ten blocks is zero.  If all ten blocks are nonzero,
they define a point of `P`, and outside the codimension-two set (8) a fully
supported pairwise zero-coupled five-root tuple exists.  Combining the
multi-star blocker lower bound with
[`FIVE_ROOT_TIGHT_BLOCKER_P5_EXTRACTION.md`](FIVE_ROOT_TIGHT_BLOCKER_P5_EXTRACTION.md)
and
[`ODD_RESIDUAL_PORT_PERMANENT_EXTRACTION.md`](ODD_RESIDUAL_PORT_PERMANENT_EXTRACTION.md)
gives the exact next alternatives:

```text
some induced block is zero -> separate nonprojective branch,
nonzero system has no torus root -> codimension-at-least-two branch,
five blockers  -> P_5 -> Delta_3,
six blockers   -> P_6 -> Delta_3,
otherwise      -> at least seven blockers.                       (11)
```

Neither permanent nonrestriction in (11) is asserted here.  The `P_5` case
is the current finite tensor bottleneck, while no `P_6` nonrestriction
theorem is presently certified in this repository.

## Exact replay

```text
python claims/arbitrary-order/verify_five_root_no_torus_codimension_two.py
python claims/arbitrary-order/audit_five_root_no_torus_codimension_two.py
```

The primary verifier expands the relevant Chow products, checks all
two-boundary-root incidence dimensions, and constructs the regular-tournament
permutation Jacobians.  The independent audit recomputes the intersection
numbers by endpoint-orientation dynamic programming and checks the
codimension and pigeonhole inputs separately.  These programs audit the
discrete intersection and tangent data; properness, generic smoothness, and
the incidence argument above prove (9) over `C`.
