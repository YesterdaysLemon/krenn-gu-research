# Binary resource supply also fails under the complete four-minority system

## Status and obligation

**Proved exact countercontrol to BS over Q(sqrt(3)).** Dedicated
independent reconstruction and adversarial proof review accept the scoped
claim below. This is not a CSQ4 or global counterexample. The global
Krenn--Gu conjecture remains **UNRESOLVED**.

Use the exact one-label common-star physical support class of
[PSCS](PROTECTED_SCAFFOLD_COMMON_STAR_COMPONENT_TARGET_OBSTRUCTION.md).
For a finite array over C, let S1 denote all singleton-component targets,
S2 all double-component targets with both equal and unequal changed colors,
and U4 every full physical source equation within four minorities of a
constant word. The parent tested here is

```
BS: S1 + S2 + U4 imply that for at least one unordered color pair {a,b},
    the entire binary state graph H_ab is a union of complete bicliques.
```

Its upstream supply would be a full CSQ4 witness, and its named consumer
is PSCS (15). The earlier [RCS countercontrol](PROTECTED_SCAFFOLD_COMMON_STAR_RESOURCE_ALIGNMENT_NO_GO.md)
failed tripartite alignment but satisfied the BS conclusion for every
pair. The construction here is designed to fail all three binary
conclusions simultaneously, with its weighted source equations intact.
An explicit mixed component coefficient below is nonzero, excluding it
as a CSQ4 or Krenn--Gu witness.

## An orthogonal relative-inverse matrix with noncomplete support

Let A be the 3-by-3 matrix from the RCS owner,

```
A=[[1,t,1],[1,1,t],[t,1,1]],  t=(sqrt(3)-1)/2.
```

For an invertible matrix X write R(X)=X Hadamard X^(-T), with no minus
sign in this definition. The earlier calculation gives R(A) R(A)^T=I
and R(A)1=1. All entries of A and A^(-T) are nonzero.

Embed A on indices {0,1,2} in I_5 to obtain L, and on {2,3,4} in I_5
to obtain R. Set M=LR and D=M^(-T). Since the two active coordinate
blocks overlap at exactly one index, each product entry of LR has at
most one nonzero summand. The same holds for L^(-T) R^(-T), with
exactly the same paths and supports. Therefore

```
M^(-T)=L^(-T) R^(-T),
M Hadamard M^(-T)
   = (L Hadamard L^(-T))(R Hadamard R^(-T)).           (1)
```

The matrices on the right are orthogonal, so W=M Hadamard D obeys
W W^T=I and W1=1. There is no positivity premise: entries lie in
Q(sqrt(3)) and can have either sign. M and D have the same 21-entry
support. The first three rows meet all five columns; the last two rows
meet just columns {2,3,4}. This bipartite support is connected but not
complete, witnessed by edges (0,0),(0,2),(3,2) and the missing edge (3,0).

## Coupling all three color pairs without an identity binary graph

With base indices in {0,...,4} squared, define 25-by-25 matrices

```
P_01=M^T tensor M,    P_12=M tensor I_5,    P_02=I_5 tensor M,
N_ab=-P_ab^(-T),      Q_ab=P_ab Hadamard N_ab.         (2)
```

Reverse a pair by transposition. Notice the single minus sign in N;
it is not the tensor product of two negative dual matrices. Explicitly,

```
Q_01=-W^T tensor W,   Q_12=-W tensor I_5,   Q_02=-I_5 tensor W.
```

Every Q has row and column sums -1 and Q Q^T=I. For all distinct c,d,e,
direct tensor multiplication gives the two simultaneous identities

```
Q_dc Q_ce = -Q_de,
(P_dc N_ce) Hadamard (N_dc P_ce) = -Q_de.              (3)
```

For de=02 the first product is I tensor W. The two factors of the
Hadamard product are -I tensor M and -I tensor D, so it is also I
tensor W. For de=01 they are -M^(-1) tensor M and -M^T tensor D,
giving W^T tensor W. For de=12 the analogous products give W tensor I.
Transposition proves the reverse orientations. These are exact shared
matrix identities, not independent choices of contractions.

Now apply the same two-clone construction as in the RCS owner. The states
in one resource are (a,p,f), where a is a color, p a 25-valued base index,
and f in {0,1}. For r=2+sqrt(3), set z_ab=(1,1) if b is the smaller
other color and z_ab=(1,r) otherwise. On supported entries put

```
A'_(a,p,f;b,q,h)=P_ab[p,q] z_ab[f] z_ba[h],
B'_(a,p,f;b,q,h)=N_ab[p,q]/(2 z_ab[f] z_ba[h]).        (4)
```

All supported factors remain nonzero. S1 is inherited from Q1=-1.
The same-color S2 proof uses P N^T=N P^T=-I and Q Q^T=I, exactly as
in the earlier owner, for distinct base indices and for different clones
of one base index separately. The distinct-color clone multiplier is
(1+r)(1+r^(-1))/4=3/2. Thus S2 becomes

```
Q_de=2 Q_dc Q_ce-3(P_dc N_ce) Hadamard (N_dc P_ce),    (5)
```

which follows from (3) as -2Q_de+3Q_de=Q_de. This proves both S2
families for the actual lifted factors.

The three base support counts in (2) are 441,105,105. Each binary
support fails complete-biclique decomposition. For 02 and 12 there are
five disjoint copies of the connected noncomplete support of M. For 01,
fix one supported entry in the first tensor factor; the second factor
retains the three-edge path and missing corner displayed after (1).
Those two row and two column vertices belong to the same connected
component, so that component is noncomplete. Cloning each vertex into
two identical neighbors preserves this obstruction. No choice of color
pair satisfies the BS conclusion.

## Actual finite cover and the full physical U4 bridge

Reuse the explicit SL(2,F5) incidence from the RCS owner: old components
(f,g) place their color-a state in resource g T_fa, with the same six
matrices T. Replace each old component by 25 indexed K4 components
(p,f,g), and install the local factors (4) in each resource.

There are 120 resources, 6000 K4 components and n=24000 physical vertices.
Each resource has 150 states and 2604 gadgets, giving 312480 gadgets in
total. Different old components share at most one resource, while copies
of the same old component always have the same state color when they
share a resource and are never joined. The result is a legal simple
one-label common-star physical array.

Unique resource membership of each component-color state assembles all
local S1/S2 equations. As in the RCS proof, deleted background spokes
must be retained until the one-label identity makes the product
(1+s)(1+t) zero. There is no independent-cofactor substitution.

Every actual component triangle projects to three distinct old components
and lies in one resource, hence is coherent. Together with S1, the
exhaustive crossing-cycle classification in the RCS owner proves **all**
U4 equations. The claim does not rely on sampling words or replacing
weighted U3 sums by termwise assumptions. The cover replays enumerate
all 423360 coherent component triangles; both the primary and the
independent cover companion perform that complete finite enumeration.

Each binary graph is a disjoint union of its resource-local binary graphs,
so the noncomplete components identified above survive in the full
physical realization. This is the required assembly of the exact BS
countercontrol, rather than an abstract local model alone.

## An explicit remaining global failure

Color clone-zero components 0 and clone-one components 2. The selected
02 matrix in one resource is I_5 tensor M, so it separates into five
binary blocks. In each block, its ten physical K4 components have one
forced protected edge apiece. Their remaining centers and selected leaves
form a 20-vertex scalar graph: protected center-leaf edges have weight
one, center crossings have matrix M, and leaf crossings have matrix
-D/2. The z factors for this selected clone/color pair are one.

Exact scalar hafnian recursion gives

```
F_5=-463/2592,     supported perfect matchings=6130.  (6)
```

Equivalently, (6) is the exact finite sum

```
sum_(I,J subsets of {0,...,4}, |I|=|J|)
    (-1/2)^|I| permanent(M[I,J]) permanent(D[I,J]).
```

The coefficients by subset size before multiplication by (-1/2)^|I|
are, in order |I|=0,...,5,

```
[1, 5, 10, 10/81, -83/9, 169/9].                    (6a)
```

The independent audit checks (6) by three exact routes: physical hafnian
recursion, the permanent of the 10-by-10 bipartite adjacency matrix
[[M,I],[I,-D^T/2]], and the minor-permanent sum (6a).

There are 600 such scalar blocks and 6000 isolated protected unit edges
in the literal full 24000-vertex graph. Its mixed source is therefore

```
F=(-463/2592)^600 != 0,                              (7)
```

with 6130^600 supported perfect matchings. Its target is zero. This
explicit failure rules out interpreting the construction as a CSQ4 or
global witness.

## Replay and evidence boundaries

The [primary verifier](verify_common_star_binary_resource_supply_control.py)
reads the tracked [fixture](../../tests/fixtures/common_star_binary_resource_supply_control.json).
It explicitly discloses its reuse of the RCS verifier's exact field and
elementary matrix helpers. It is not independent of that arithmetic.

The [independent algebra audit](audit_common_star_binary_resource_supply_control.py)
reconstructs the field, matrices and clone identities without importing
the primary or project scientific code. The separate
[independent cover audit](audit_common_star_binary_resource_cover.py)
reconstructs the actual 24000-vertex graph and its scalar components.
The [review](../../docs/audits/COMMON_STAR_BINARY_SUPPLY_REVIEW_2026-09-14.md)
pins the artifacts and checks the analytic bridge and negative controls.

Run the three named Python files from the repository root. Each defaults
to standard output and supports an optional --output receipt path. The
finite computations use exact Q(sqrt(3)) arithmetic, not numerical or
modular evidence. They replay the explicitly finite construction and
coefficient; the written matching classification and assembly proof
establish all global S2 and U4 equations. No enumeration of all physical
U4 words or all 3^6000 component words is claimed. No external solver,
external theorem import or Lean formalization is supplied.

## Proof-topology consequence

This eliminates the BS supply implication as
well as its stronger predecessor RCS. The conditional binary-resource
consumer in PSCS remains valid. The missing route must use additional
global component equations or a different structural implication that
does not follow merely from S1+S2+U4. No claim is made that one specific
next source layer suffices, or that arbitrary witnesses reduce to these
common-star arrays.
