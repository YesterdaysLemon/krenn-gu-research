# Legal P7 secant--factor codimension barrier and Artinian pair-ideal reduction

## Status

**Exact characteristic-zero legal-companion theorem and strict reduction of
the localized pair-ideal question.**  This note works inside an arbitrary
legal full-rank 219-label P7 companion map

```text
Gamma:U -> T,                 dim U=219,
T=(K^3)^(tensor 5),           dim T=243.              (1)
```

It does not replace `Gamma` by an arbitrary incidence map.  The only linear
geometry used is the image of the actual legal symmetric companion map.

Two projective varieties in `P(U)=P^218` are unavoidable:

1. the preimage `Z_Gamma` of the third secant of the five-qutrit Segre,
   which has dimension at least eight for every full sensor; and
2. the inverse image `F_Q` of the seven-port two-factor-analysis variety in
   the 21 residual-pair coordinates, which has codimension exactly eight.

The projective dimension theorem therefore forces

```text
Z_Gamma intersect F_Q != empty                       (2)
```

for **every legal full sensor**.  Thus the complete factor-analysis circuit
layer, not merely one pentad, can never exclude all mandatory border-GHZ
lines.  If a point of (2) is torus-concise, simple, and root-torus admissible,
a legal root-local basis change turns it into an actual diagonal target
incidence while leaving its named cofactor line and pair equations unchanged.

The full weighted pair ideal is not proved nonunit.  Its additional `h=0`
gate and alignment with the specifically reconstructed residual stars can
still remove (2), and (2) may be trapped in the secant, pinned, or root-torus
boundary.  On the expected proper-intersection chart, however, the problem
reduces exactly to finite-dimensional Artinian linear algebra: multiplication
by the degree-eight gate decides whether it is a unit on the mandatory finite
scheme, and the Laurent amplitude equations decide the surviving star
alignment.

This changes the frontier from an unrestricted companion-parameter ideal to
one mandatory secant--factor intersection plus a finite quotient.  Whether
the exact legal localized pair ideal is the unit ideal remains **UNKNOWN**.
P7 and global Krenn--Gu remain **UNRESOLVED**.

No label, graph, parameter, support, secant decomposition, or quadruplet
enumeration is used.

## 1. The mandatory legal border-GHZ preimage

Let

```text
X=Segre((P^2)^5) subset P(T),
Sigma=sigma_3(X).                                     (3)
```

The third secant has projective dimension 32.  Indeed, three pure tensors
contribute 30 projective factor parameters and two projective mixture
parameters.  At

```text
e_0^(tensor 5)+e_1^(tensor 5)+e_2^(tensor 5),         (4)
```

the three pure words and the 30 single-flip words are independent affine
tangent directions, proving that the upper bound 32 is attained.

Since `Gamma` is injective, it embeds `P(U)` as a projective 218-plane
`P(W)` in `P(T)=P^242`.  Define

```text
Z_Gamma={ [q] in P(U) : [Gamma q] in Sigma }.         (5)
```

### Theorem 1 (legal secant floor)

Every irreducible component of `Z_Gamma` has projective dimension at least
eight.  In particular, `Z_Gamma` is nonempty for every legal full sensor.

### Proof

Under the embedding by `Gamma`, (5) is `P(W) intersect Sigma`.  The
projective dimension theorem gives

```text
dim Z_Gamma >=218+32-242=8.                           (6)
```

Nothing in this argument forgets legality: `W` is the image of the actual
legal companion map.  The conclusion is border rank at most three.  It does
not assert that a point lies in the open locally diagonalizable rank-three
orbit.

## 2. The exact seven-port factor locus has codimension eight

Let `Q={0,1}` be the residual pair and `B={2,...,8}` the seven blockers.
The named coordinate projection is

```text
pi_Q:U -> K^(binom(7,2)),
pi_Q(q)_(ij)=q_{ {0,1,i,j} }.                         (7)
```

Let `FA_(7,2)` be the Zariski closure of the arrays

```text
y_ij=a_i b_j+b_i a_j,              i<j in B.         (8)
```

This is the exact off-diagonal two-factor-analysis variety.  It is defined
by the full elimination ideal `I_(7,2)`.  Five-port pentads belong to this
ideal, but no claim is made that they generate it at seven ports.

### Lemma 2 (factor-locus dimension)

The affine cone `FA_(7,2)` is irreducible of dimension 13.  Its projective
closure in `P^20` has dimension 12 and codimension eight.

### Proof

The parameter space in (8) has dimension 14.  The one-dimensional action

```text
(a,b) -> (s a,s^(-1)b)                               (9)
```

fixes every `y_ij`, so the image dimension is at most 13.  At

```text
a_i=i+1,             b_i=(i+1)^2,       0<=i<=6,     (10)
```

the `21 x 14` Jacobian of (8) has rank 13.  Hence the image closure has
dimension 13.  Irreducibility follows from irreducibility of the parameter
space.  Projectivizing subtracts one dimension.

The primary and independent replays verify the exact rank-13 certificate in
(10); it is a fixed Jacobian witness, not a parameter search.

Define the projective inverse image

```text
F_Q=P(pi_Q^(-1)(FA_(7,2))) subset P(U).               (11)
```

Because (7) is a surjective named coordinate projection, its affine kernel
has dimension `219-21=198`.  Therefore

```text
dim F_Q=198+13-1=210,
codim_(P(U)) F_Q=8.                                  (12)
```

### Theorem 3 (mandatory secant--factor intersection)

For every legal full-rank P7 companion map,

```text
S_Gamma:=Z_Gamma intersect F_Q != empty.              (13)
```

Every component of the intersection supplied by the projective dimension
theorem has dimension at least zero.

### Proof

Equations (6) and (12), now inside `P(U)=P^218`, give

```text
dim S_Gamma >=8+210-218=0.                            (14)
```

This proves nonemptiness over the algebraic closure.  All varieties and
maps are defined in characteristic zero over the original coefficient
field; rationality of an intersection point is not asserted.

### Corollary 4 (the factor/pentad layer cannot be the unit obstruction)

The pullback to `Z_Gamma` of the complete ideal `I_(7,2)` is proper for
every legal full sensor.  In particular, no argument using only the
seven-port factor-analysis equations can exclude every border-GHZ line in a
legal sensor image.

This is stronger than saying that a chosen pentad might vanish accidentally:
at least one mandatory border line satisfies the whole two-factor-analysis
elimination ideal.

The dimension theorem allows the forced intersection to lie in the base
locus `P(ker pi_Q)`, where all 21 pair coordinates vanish.  Thus Theorem 3
proves properness of the factor ideal but does not by itself supply a nonzero
five-port window.

## 3. Legal local bases preserve the cofactor survivor

Suppose `[q] in S_Gamma` and `Gamma q` is in the torus-concise rank-three
open of `Sigma`.  Thus

```text
Gamma q=sum_(c=0)^2 lambda_c
  a_(0,c) tensor ... tensor a_(4,c),                  (15)
```

where the three `a_(i,c)` form a basis at every root, every `lambda_c` is
nonzero, and the factors evaluate nontrivially on the chosen root vectors.
Independent legal root-local changes of basis send (15) to a diagonal GHZ
tensor.  They act on the companion map by left multiplication:

```text
Gamma'=(g_0 tensor ... tensor g_4)Gamma.              (16)
```

Consequently the named preimage is still exactly `q`.  The coordinate array
(7), every factor-analysis equation, the pinned determinants, `eta(q)`, and
the star-alignment equations are unchanged.

If the transformed image meets the diagonal plane only in `K Gamma' q`,
this gives an actual legal full-sensor **simple** target-incidence point in
the factor locus.  Therefore Theorem 3 gives the exact alternative:

```text
S_Gamma meets the torus-concise, root-torus, simple open,
or every point of S_Gamma lies in its explicit closed boundary.       (17)
```

The theorem does not choose the first branch of (17).

## 4. An eight-equation barrier on the border family

Let `f_1,...,f_k` be homogeneous positive-degree polynomials on `U`.  They
may be the degree-eight gate `eta`, named pentad components, or named
degree-17 alignment minors.  Homogeneity is essential because the cofactor
line is projective.

### Theorem 5 (no eight scalar covariants exhaust the border preimage)

For every legal full sensor and every `k<=8`,

```text
Z_Gamma intersect V(f_1,...,f_k) != empty,
dim >=8-k.                                            (18)
```

In particular:

- `Z_Gamma intersect V(eta)` has dimension at least seven;
- `eta` together with any one named pentad still leaves dimension at least
  six; and
- any chosen collection of at most eight scalar components from the
  pentad/gate/alignment hierarchy has a common border-rank-three survivor.

### Proof

Intersect an at-least-eight-dimensional projective component of `Z_Gamma`
successively with the projective hypersurfaces `V(f_i)`.  Each equation
either contains the current component or lowers its dimension by at most
one.  After at most eight equations, a nonempty projective intersection
remains and has the stated lower bound.

The conclusion concerns the border secant.  The surviving set may be wholly
non-concise or lie on `d_0d_1=0`.  Thus (18) is a lower bound on the algebraic
complexity of a unit proof, not a construction of a GHZ witness.

## 5. Finite Artinian reduction on the proper chart

The expected dimension in (14) is zero.  Assume a legal full sensor lies on
the meaningful invariant chart where

```text
S_Gamma=Z_Gamma intersect F_Q
```

is zero-dimensional and is not wholly contained in the irrelevant pair
coordinate locus.  Let `A_Gamma` be its finite homogeneous coordinate
algebra after choosing one nonzero projective coordinate.  Localize further
at the full-sensor, simple-incidence, root-torus, and pinned determinants as
needed.

The degree-eight gate defines a multiplication operator

```text
m_eta:A_Gamma -> A_Gamma,             x -> eta x.     (19)
```

### Theorem 6 (norm and finite quotient criterion)

On this proper chart:

1. `eta` has no zero on `S_Gamma` if and only if

   ```text
   N_eta(Gamma):=det(m_eta) !=0.                      (20)
   ```

2. The full `h=0` pair sector survives if and only if the finite Laurent
   algebra

   ```text
   A_Gamma[tau,tau^(-1)] /
   < eta,
     tau y_ij-khat_ij : 2<=i<j<=8 >                  (21)
   ```

   is nonzero.

Thus, on the proper secant--factor chart, the legal localized pair ideal is
the unit ideal exactly when (21) is the zero algebra.  This is a finite
linear-algebra problem after the mandatory intersection is formed; it is not
a huge elimination over free companion and cofactor variables.

### Proof

In a finite-dimensional commutative algebra, an element is a unit exactly
when its multiplication map is invertible.  This proves (20).  Quotient
(21) is precisely the weighted pair ideal restricted to the factor scheme;
invertibility of `tau` enforces a nonzero target amplitude and handles zero
pair coordinates without spurious rank-one-minor solutions.  A proper ideal
has a nonzero quotient, proving the second assertion.

The primary and independent replays check (20) on fixed exact Artinian
algebras.  No claim is made that `A_Gamma` has yet been constructed for the
committed integer sensor.

## 6. Exact frontier

Theorem 3 eliminates one possible strategy: the degree-five
factor-analysis layer cannot alone prove that every legal full sensor avoids
even border-GHZ incidence.  Theorem 5 likewise prevents a unit proof from
coming from only a handful of scalar components.

The remaining legal task has three sharply separated possibilities:

1. prove `S_Gamma` lies in the non-concise, root-torus, deeper-incidence, or
   pinned boundary;
2. on a proper good component, prove the finite quotient (21) is zero; or
3. exhibit a nonzero point of (21), proving the legal localized pair ideal
   nonunit on that chart, after which the other 105 four-deck and upper-deck
   equations remain.

## Scope wall

```text
legal rank-219 companion image used throughout:                 YES;
mandatory border-rank-three preimage dimension:                 AT LEAST 8;
seven-port factor-analysis locus codimension:                   EXACTLY 8;
legal secant--factor intersection:                              NONEMPTY;
complete factor-analysis pullback unit on border family:        FALSE;
eta plus <=7 chosen scalar components exhaust border family:    FALSE;
torus-concise point in mandatory intersection:                  UNKNOWN;
simple diagonal incidence after legal basis change:             UNKNOWN;
mandatory intersection meets pinned open:                       UNKNOWN;
mandatory intersection has a nonzero Q-pair coordinate:          UNKNOWN;
eta vanishes on the secant--factor intersection:                UNKNOWN;
star alignment survives there:                                  UNKNOWN;
proper-intersection Artinian algebra for committed sensor:       NOT BUILT;
legal localized full pair ideal is unit:                         UNKNOWN;
legal localized full pair ideal has a point:                     UNKNOWN;
other 105 four-deck and upper-deck equations:                    STILL REQUIRED;
P7 obstruction or construction:                                 UNKNOWN;
global Krenn--Gu:                                                UNRESOLVED.
```

## Exact replay

```powershell
uv run --with sympy python claims/p7/verify_legal_p7_secant_factor_codimension_barrier_and_artinian_pair_ideal.py
python claims/p7/audit_legal_p7_secant_factor_codimension_barrier_and_artinian_pair_ideal.py
python -m py_compile verify_legal_p7_secant_factor_codimension_barrier_and_artinian_pair_ideal.py audit_legal_p7_secant_factor_codimension_barrier_and_artinian_pair_ideal.py
uv run --with ruff ruff check verify_legal_p7_secant_factor_codimension_barrier_and_artinian_pair_ideal.py audit_legal_p7_secant_factor_codimension_barrier_and_artinian_pair_ideal.py
```

The primary replay verifies the exact rank-13 factor Jacobian, its
one-dimensional gauge kernel, the codimension arithmetic, covariance of a
named preimage under legal left basis change, and the Artinian norm test.
The independent standard-library audit repeats the Jacobian rank with
rational row reduction and rebuilds the norm criterion with separate exact
matrix arithmetic.  These are bounded symbolic audits of the proofs, not
evidence from sampled companion parameters.
