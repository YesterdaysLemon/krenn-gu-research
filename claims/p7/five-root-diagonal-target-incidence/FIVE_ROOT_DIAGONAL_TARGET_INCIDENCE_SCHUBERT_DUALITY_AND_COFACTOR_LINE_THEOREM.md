# Five-root diagonal target incidence is a codimension-22 Schubert condition

## Status

**Exact coordinate-free characteristic-zero theorem and proof-route
boundary.**  Let

```text
U = the 219-dimensional labeled shallow-cofactor space,
T = tensor_(i=1)^5 K^3,                    dim T=243,
Delta = span{e_0^(tensor 5),e_1^(tensor 5),e_2^(tensor 5)},
E:Delta -> T the inclusion,
Gamma:U -> T the complete five-root companion map.     (1)
```

On the full-sensor locus, `Gamma` is injective.  Put `W=im Gamma` and
`C=T/W`, so `dim C=24`.  Then every diagonal-target question is controlled
by the single obstruction map

```text
A_Gamma=q circ E:Delta -> C,                           (2)
```

where `q:T->C` is the quotient.  A nonzero diagonal GHZ completion exists
if and only if `rank A_Gamma<=2`.  Dually, if

```text
L=ker Gamma^* = W^perp,                    dim L=24,   (3)
```

then the same condition says that restriction of the left-kernel covariants
to `Delta` has rank at most two:

```text
A_Gamma^*=E^*|L:L -> Delta^*.                          (4)
```

Thus the entire family of augmented `222 x 222` minors is one exterior
covariant

```text
Omega(Gamma,E)=wedge^219 Gamma wedge wedge^3 E.        (5)
```

Its vanishing is the target-incidence equation.  No expansion of the minors
is needed.

In the ambient Grassmannian `Gr(219,T)`, the locus `W intersect Delta !=0`
is a special Schubert variety of codimension

```text
243-219-3+1=22.                                       (6)
```

At a generic incidence point the intersection is one line.  Its tangent
space is cut out by exactly 22 linear conditions, while the singular locus
starts where `dim(W intersect Delta)>=2` and has ambient codimension 46.

Target membership does impose a sharp **sensor-dependent** relation on the
219 cofactor labels.  If `pi_Delta:T->T/Delta`, then the allowable cofactor
vectors are exactly

```text
K_Gamma=ker(pi_Delta Gamma).                           (7)
```

At a generic incidence point this kernel is one-dimensional, so the
cofactor vector satisfies 218 independent `Gamma`-dependent linear
relations and is projectively unique.  For a fixed target normalization it
is unique outright because `Gamma` is injective.

There is, however, no nonzero `Gamma`-independent linear or homogeneous
polynomial relation on the cofactor vector that follows from full rank and
diagonal incidence alone: every nonzero vector of `U` occurs at some
full-rank ambient incidence map.  Principal-hafnian realizability and the
special graph-companion parametrization are essential additional structure.

The legal companion maps form a much smaller polynomial family inside
`Hom(U,T)`.  This note does not prove that its full-rank locus meets the
target-incidence Schubert variety, nor that the pullback has codimension 22.
The committed explicit rank-219 chart lies outside it.  Consequently no
`P_7` obstruction and no global Krenn--Gu conclusion is claimed; both remain
**UNRESOLVED**.

## 1. Quotient and left-kernel duality

Let `K` be a characteristic-zero field.  The linear statements below in
fact hold over every field.  Suppose `Gamma:U->T` is injective, with

```text
dim U=k=219,        dim T=n=243,
dim Delta=d=3,      q=n-k=24.                         (8)
```

Let `W=im Gamma`, let `Q:T->C=T/W`, and define

```text
A=Q E:Delta -> C.                                     (9)
```

### Theorem 1 (cokernel obstruction)

For every `s=0,1,2,3`, the following are equivalent:

```text
dim(W intersect Delta)=s,
dim ker A=s,
rank A=d-s,
rank[Gamma|E]=k+d-s.                                  (10)
```

In particular, a nonzero diagonal target lies in `W` if and only if

```text
rank A<=2
<=> rank[Gamma|E]<=221.                               (11)
```

For a fixed nonzero `lambda in Delta`,

```text
E(lambda) in W
<=> A(lambda)=0
<=> rank[Gamma|E(lambda)]=219.                        (12)
```

### Proof

The kernel of `Q|Delta` is precisely `W intersect Delta`, proving the first
three equalities.  The image of `[Gamma|E]` is `W+Delta`, whose dimension is

```text
dim W+dim Delta-dim(W intersect Delta)=k+d-s.
```

This proves (10)--(12).

Dualize the exact sequence

```text
0 -> W -> T -> C -> 0.
```

The dual `C^*` identifies canonically with the annihilator
`L=W^perp=ker Gamma^*`.  Under this identification, the dual of (9) is

```text
A^*:L -> Delta^*,            ell |-> ell restricted to Delta. (13)
```

Therefore `rank A^*=rank A=d-s`.  If `ell_1,...,ell_24` is any left-kernel
basis and `d_0,d_1,d_2` is a diagonal basis, form

```text
R_Gamma[a,c]=ell_a(E(d_c)).                            (14)
```

Then a diagonal coefficient vector `lambda` is admissible exactly when

```text
R_Gamma lambda=0.                                     (15)
```

This is the left-kernel covariant form of target incidence.  The basis
changes `ell -> S ell` and `d -> P d` act by invertible row and column
operations, so its rank and kernel are intrinsic.

## 2. One exterior equation instead of all augmented minors

Choose nonzero volume elements `u in det U` and `delta in det Delta`.  Put

```text
omega_Gamma=(wedge^k Gamma)(u) in wedge^k T,
omega_Delta=(wedge^d E)(delta) in wedge^d T.           (16)
```

Define

```text
Omega(Gamma,E)=omega_Gamma wedge omega_Delta
              in wedge^(k+d) T.                       (17)
```

Changing either volume rescales `Omega` by a nonzero scalar, so its zero
locus is coordinate-free.

### Theorem 2 (exterior target-incidence equation)

On the injective locus of `Gamma`,

```text
Omega(Gamma,E)=0
<=> W intersect Delta != {0}
<=> wedge^3 A=0
<=> wedge^3(A^*)=0.                                   (18)
```

For a fixed target `lambda`, the corresponding covariant is

```text
Omega_lambda(Gamma)=omega_Gamma wedge E(lambda)
                    in wedge^(k+1) T,                 (19)
```

and it vanishes exactly when `E(lambda) in W`.

### Proof

The wedge in (17) is nonzero exactly when a basis of `W` followed by a basis
of `Delta` is linearly independent, equivalently when their intersection is
zero.  Quotienting by `W` turns the last three vectors into the image of
`A`; their top wedge is nonzero exactly when `A` has rank three.  Duality
gives the last equivalence.  The fixed-target statement is the same argument
with one vector.

In coordinates, the components of (17) are precisely the `222 x 222`
augmented minors, while the components of `wedge^3 A` are the `3 x 3`
minors of a `24 x 3` cokernel matrix.  Equation (18), rather than an expanded
list of either family, is the intrinsic defining covariant.

## 3. Schubert codimension and singular strata

Let

```text
X=Gr(k,T),
Sigma_s={W in X:dim(W intersect Delta)>=s}.            (20)
```

The target-incidence locus is `Sigma_1`.  Consider its incidence resolution

```text
tilde Sigma_1
 ={(ell,W):ell in P(Delta), ell subset W}.             (21)
```

Choosing `ell` takes `d-1=2` parameters.  For fixed `ell`, the quotient
`W/ell` is a `(k-1)`-plane in `T/ell`, giving

```text
dim tilde Sigma_1
 =(d-1)+(k-1)(n-k)
 =2+218*24=5234.                                      (22)
```

Since

```text
dim X=k(n-k)=219*24=5256,                              (23)
```

and a generic point of `Sigma_1` has a unique intersection line, `Sigma_1`
has codimension 22.

More generally, the local model is the rank locus for a `q x d` matrix
`A`.  Requiring `dim ker A>=s`, or `rank A<=d-s`, has codimension

```text
s(q-d+s).                                             (24)
```

For `(q,d)=(24,3)`, the three strata begin at

```text
s>=1: codimension 22,
s>=2: codimension 46,
s=3:  codimension 72.                                 (25)
```

The rank-at-most-two determinantal variety is smooth at rank exactly two and
singular at rank at most one.  Hence `Sigma_1` is smooth on the one-line
intersection stratum and its singular locus is `Sigma_2`.

These are ambient Grassmannian codimensions.  If `P` is the legal graph
parameter space and `Gamma:P->Hom(U,T)` its polynomial companion map, the
physical target-incidence equations are the pullback of (17).  Their
codimension in `P` is 22 only if that pullback is nonempty and transverse.
Neither property is currently proved.

## 4. The exact tangent and normal equations

Let `W in Sigma_1 minus Sigma_2`, put

```text
D_0=W intersect Delta,                    dim D_0=1,
C=T/W,                                    dim C=24,
bar Delta=Q(Delta) subset C,              dim bar Delta=2. (26)
```

The Grassmannian tangent space is canonically

```text
T_W X=Hom(W,C).                                        (27)
```

### Theorem 3 (generic incidence tangent space)

The tangent and normal spaces of the target-incidence locus are

```text
T_W Sigma_1
 ={phi in Hom(W,C):phi(D_0) subset bar Delta},         (28)

N_(Sigma_1/X),W
 =Hom(D_0,C/bar Delta).                                (29)
```

The normal dimension is `1*(24-2)=22`.

### Proof

Let `d` span `D_0`.  Under a first-order deformation of `W` represented by
`phi`, the vector `d` may remain in the moving intersection after adding a
first-order vector from `Delta` precisely when its displacement `phi(d)` in
`C` lies in the image `bar Delta`.  This gives (28).  Taking the quotient of
the value on `D_0` by `bar Delta` gives the surjective normal map

```text
Hom(W,C) -> Hom(D_0,C/bar Delta),
phi |-> (D_0 -> C -> C/bar Delta),
```

whose kernel is (28), proving (29).

There is an equivalent formula before quotienting the sensor basis.  Let
`c` span

```text
K_Gamma=ker(pi_Delta Gamma),                           (30)
```

so `Gamma(c)` spans `D_0`.  A variation `dot Gamma` is tangent to the
variable-target incidence locus exactly when

```text
Q(dot Gamma(c)) in Q(Delta).                           (31)
```

For a fixed target `E(lambda)=Gamma(c)`, it is tangent to that fixed-target
locus exactly when

```text
Q(dot Gamma(c))=0.                                    (32)
```

Equation (31) imposes 22 conditions; (32) imposes 24.  Variations
`dot Gamma=Gamma B` coming only from a change of basis in `U` satisfy both
quotient equations automatically, as they must.

## 5. What target incidence says about the 219 labels

Let `pi_Delta:T->T/Delta`.  Because `Gamma` is injective, restriction gives
an isomorphism

```text
Gamma:ker(pi_Delta Gamma) -> W intersect Delta.        (33)
```

Consequently

```text
dim K_Gamma=dim(W intersect Delta)=s,
rank(pi_Delta Gamma)=219-s.                            (34)
```

### Corollary 4 (the generic cofactor line)

On `Sigma_1 minus Sigma_2`, the 219 shallow-cofactor values of a diagonal
target lie on the single projective line

```text
P(K_Gamma) subset P(U).                               (35)
```

Equivalently, the rows of `pi_Delta Gamma` supply 218 independent linear
relations among them.  The companion blocks determine the coefficients of
these relations.  Given a fixed nonzero diagonal target, injectivity of
`Gamma` fixes the scale and the cofactor vector is unique.

On `Sigma_s`, the allowable cofactor space has dimension `s`; deeper target
intersection weakens rather than strengthens these sensor-linear relations.

### Proposition 5 (no universal cofactor relation from incidence alone)

For every nonzero `c in U` and every nonzero `d in Delta`, there is an
injective ambient map `Gamma:U->T` such that

```text
Gamma(c)=d,
im Gamma intersect Delta=K d.                         (36)
```

Therefore no nonzero linear functional on `U`, and indeed no nonzero
homogeneous polynomial on `U`, vanishes on every full-rank incidence
cofactor vector.

### Proof

Choose decompositions

```text
U=K c direct-sum U',
Delta=K d direct-sum Delta',
T=Delta direct-sum H,                     dim H=240.  (37)
```

Since `dim U'=218<=240`, choose any injection `j:U'->H` and define

```text
Gamma(c)=d,          Gamma|U'=j.                       (38)
```

Then `Gamma` is injective and its image meets `Delta` only in `K d`.  Since
every nonzero `c` occurs and `K` is infinite, no nonzero homogeneous
polynomial can vanish on all such vectors.

This proposition is deliberately ambient.  It does not assert that the map
(38) is a permanental companion map of legal graph blocks.  Thus it rules
out only a proof based on rank and diagonal incidence **alone**.  A universal
relation could still follow after imposing:

- the matching-polynomial form of `Gamma`;
- pairwise-zero and blocker/nonblocker incidence;
- principal-hafnian realizability of the 219 entries;
- pinned-star, Euler, or nested-hafnian equations;
- the full mixed GHZ coefficient system.

## 6. Exact remaining boundary

The committed legal chart proves that the full-rank sensor locus is nonempty
and that `Omega` is not identically zero on it.  It does not provide a point
with `Omega=0`.  The next exact alternatives are therefore:

1. prove the legal full-rank companion family misses `Sigma_1`, which would
   be a direct P7 obstruction;
2. construct a legal point in `Sigma_1`, compute its line (35), and test its
   unique cofactor vector against principal-hafnian and pinned/nested
   identities;
3. show the legal pullback meets only `Sigma_2`, forcing an even stronger
   but singular two-target compatibility condition;
4. prove a transversality or excess-intersection theorem for the pullback of
   the 22-dimensional normal covariant (29).

```text
cokernel obstruction Delta -> T/im Gamma:             EXACT;
left-kernel restriction duality:                      EXACT;
all augmented minors compressed to one exterior form: YES;
ambient target-incidence codimension:                 22;
generic incidence tangent conditions:                22;
singular locus begins at intersection dimension two: PROVED;
generic allowable cofactor space:                     ONE LINE;
Gamma-dependent linear cofactor relations:           218;
Gamma-independent cofactor relation from incidence:  NONE;
legal full-rank target-incidence point:               UNKNOWN;
physical pullback codimension/transversality:         UNKNOWN;
principal-hafnian realization of the cofactor line:   UNKNOWN;
P7 nonrestriction:                                    UNKNOWN;
global Krenn--Gu:                                     UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/p7/five-root-diagonal-target-incidence/verify_five_root_diagonal_target_incidence_schubert_duality_and_cofactor_line.py
python claims/p7/five-root-diagonal-target-incidence/audit_five_root_diagonal_target_incidence_schubert_duality_and_cofactor_line.py
python -m py_compile claims/p7/five-root-diagonal-target-incidence/verify_five_root_diagonal_target_incidence_schubert_duality_and_cofactor_line.py claims/p7/five-root-diagonal-target-incidence/audit_five_root_diagonal_target_incidence_schubert_duality_and_cofactor_line.py
uv run --with ruff ruff check claims/p7/five-root-diagonal-target-incidence/verify_five_root_diagonal_target_incidence_schubert_duality_and_cofactor_line.py claims/p7/five-root-diagonal-target-incidence/audit_five_root_diagonal_target_incidence_schubert_duality_and_cofactor_line.py
```

The primary replay verifies the quotient, dual, exterior-rank, cofactor-line,
and tangent formulas on fixed rational transverse, simple-incidence, and
double-incidence models.  The independent no-import audit reconstructs the
same ranks with separate rational elimination and checks the dimension and
codimension formulas.  These small models audit the coordinate-free proofs;
neither replay expands the five-root augmented minors or searches graph
parameters.
