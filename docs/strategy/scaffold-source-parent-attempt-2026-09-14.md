# Shared-source parent attempt on the protected scaffold

Status: the complete k=2 scaffold is excluded by an independently checked full-source RUP proof. MS and two stronger proposed subsystem parents have exact audited countermodels.
Global Krenn–Gu remains **UNRESOLVED**. The preceding goal turn made verified
progress through P17, ST20 and exact module limitations, committed through
ae29f652. The current 129-entry support is a Boolean model, not weights.

## Exact parent and why this test is load-bearing

Let k>=2 and n=4k. On each four-vertex component fix the three edge-disjoint
perfect matchings M0={01,23}, M1={02,13}, M2={03,12}, with edge weight E_cc
on Mc. Every crossing physical block is an arbitrary hollow complex matrix.
This is the protected pure-matching scaffold; its pure amplitudes, killer
structure and entire majority-ideal hierarchy hold identically.

The proposed parent MS is: no such source can satisfy T_W(a)=delta_a for every
colour word a that is constant on at least one complete scaffold component.
This is an exact complex pointwise statement, including exceptional fillings.
Full GHZ supplies these equations. Its named downstream consumer is exclusion
of the complete protected scaffold family, a required sharp control for the
proposed full-source high-surplus descent route. Excluding this family would
still not exclude arbitrary sources or prove that descent theorem.

This synthesizes the existing majority-scaffold no-go with the newly proved
shared-hafnian transfer: retain whole source slices and their shared physical
coefficients rather than only vanishing edge products. At k=2, MS asks whether
all equations with either four-vertex shore monochromatic already contradict
the six shared crossing colour matrices. A countermodel at k=2 refutes MS as
stated and forces a uniform route to use additional equations; it is not a
Krenn–Gu counterexample unless every full word also passes independent audit.

Success is a proof of MS (with its full quantifiers), an exact physical
countermodel to MS, or a precise source-level obstruction that isolates a
load-bearing next lemma. Failure of a restricted search is only experimental.
No reduction from arbitrary sources to the scaffold, nor from larger k to k=2,
is asserted. The generic maximum-torus-root-five part of the earlier scaffold
theorem requires k>=5; it is not a property attributed to this k=2 test.

## First exact subsystem

For k=2 write L,R for the shores and X_cd for the four-by-four crossing matrix
with left colour c and right colour d. X_cc=0. For fixed left colour c, put
z_j^a=(X_ca[i,j])_i and let J_c be the matching matrix of Mc on L. The same
source supplies, for every Mc edge jk on R and every a,b!=c,

    (z_j^a)^T J_c z_k^b = 0.

These follow by fixing the other right Mc edge to c. The reversed-shore
equations use the same X_cd, transposed; no independent cofactor is introduced.
For a right word w without colour c, the full coefficient is the sum of its
zero-crossing internal matching term, all two-crossing Gram terms and the
four-crossing permanent. All those terms, including the pure constant, must
be retained. The one-matrix control X_cd=t P with P mapping Md to Mc gives
the proper-subsystem cancellation (1+t^2)^2=0 at t^2=-1, so positivity and
single-colour Gram rank are insufficient.

One bounded constructive probe restricts X_cd to i times a permutation matrix
mapping Md to Mc. This contains the sharp two-colour cancellation control and
allows exact arithmetic in Q(i). It seeks a countermodel, not a complete
exclusion. A separate algebraic review considers the full matrix equations.
Each launched computation is bounded to 900 seconds and 8192 MiB, with at most
three concurrent research processes. An apparent full-target solution triggers
dedicated adversarial validation immediately, before any status promotion.

## Exact obstruction found and sharper next implication

The full-permutation probe has sixteen Gram-compatible pairs per fixed shore,
but each retains an uncancelled four-crossing monomial. Rank-two partial
permutations remove that obstruction: allocate each left colour's two scaffold
edges to its two other right colours, and do the transpose allocation on R.
Join each allocated pair by two crossing entries r_cd,-1/r_cd. All 477 MS8
equations then hold identically, including both shores on the same source.
Independent complete expansion finds 27 remaining full-word residuals, each
one nonzero Laurent monomial. For example T(00012121)=-r02/r12. The rational
specialization r_cd=1 uses only crossing weights 1,-1. This refutes MS as stated;
it does not realize the full target. Arbitrary other monochromatic four-sets
and binary restrictions are not satisfied.

The next candidate implication B8 retains every actual two-colour word on
the same two-K4 scaffold, first for one colour pair and then for all three
pairs together with MS8. A hypothetical full witness necessarily supplies
these equations; their incompatibility would exclude this complete scaffold
at n=8, with no general reduction to it asserted. A feasible support model
alone is not a physical countermodel to B8.

For a pair c,d put A=X_cd, B=X_dc, and let p_s be the partner involution of
M_s. A word with two c vertices, one on each shore, has the unique term
A[u,p_d(v)] B[p_d(u),v]. Interchanging c,d gives the corresponding p_c term.
Thus the binary full source supplies the monomial equations

    A[i,j] B[p_s(i),p_s(j)] = 0,  s in {c,d}, i,j in {0,1,2,3}.

These are missing from MS8 and visibly couple opposite crossing matrices.
A bounded Boolean probe will retain the exact expanded binary polynomials
(and their constants), forbidding singleton cancellation. This is a necessary
model only: SAT is not weights, and UNSAT requires independent generation,
an exact proof check, and a reviewed witness-to-model bridge before promotion.


## Completed parent attempt and finite closure

The exact physical controls are preserved in
[the complete eight-vertex scaffold package](../../claims/finite/n08/EIGHT_VERTEX_PROTECTED_SCAFFOLD_EXCLUSION.md).
The first six-parameter family satisfies MS8 (477 distinct words) and fails
27 full words. A corrected routing satisfies MS8 plus all binary restrictions
(1,065 distinct words), but fails 29 genuinely three-colour words. A third
routing satisfies every independent-minority equation and all nine
component-constant targets (1,869 distinct words), but fails 27 full words.
Each full error is one nonzero Laurent monomial, so these are physical
countermodels to the named subsystems and explicit nonwitnesses for GHZ.
Independent exact matching expansion checks all three families.

Restoring all 6,561 physical source equations makes the necessary support CNF
unsatisfiable on the entire 96-dimensional crossing parameter space. The
accepted proof uses 1,521 original clauses and 108 ordered RUP additions.
Primary matching-first and independent word-first reconstructions agree on
every coefficient, variable and clause. Two independent unit-propagation
implementations replay the tracked 13 KB certificate and reject mutations.
This closes the complete k=2 protected scaffold, with zeros and exceptional
fillings included. It does not exclude the separate 129-entry survivor or
arbitrary eight-vertex sources. The mathematical proof is the one-way
witness-to-CNF bridge plus exact refutation; no SAT-to-weights inference is used.

The discovery process wrote a complete proof but failed on Windows native
cleanup. That run remains failed. The independently accepted proof, including
portable solver-free replay, establishes the result. Generated solver dumps
remain local and are not needed for the durable theorem.

## What survives at arbitrary order

The [minority-cycle and resource theorem](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_MINORITY_CYCLE_AND_RESOURCE_BOUNDARY.md)
proves an exact permanent formula whenever minorities occupy at most one
endpoint of each majority-colour protected edge. Vanishing of all these
actual source equations is equivalent to absence of an admissible directed
cycle. More general boundary words retain an injection-labelled hafnian sum
of exterior matching-edge resources. Each resource can be consumed only once.

An independently checked twelve-vertex array satisfies all 46,875 indexed
localized evaluations (46,851 distinct words), yet an exterior component
changes a two-component mixed amplitude from one to zero. It explicitly fails
another full equation. Thus the eight-vertex exclusion cannot be transferred
by discarding those resources. The third six-parameter eight-vertex control
also refutes adding only the component-constant equations to the localized
system. These are exact mechanism failures, not repeated support assignments.

## Next parent: fixed minority depth U4 and its all-depth extension

The next parent, stated before the new proof dispatch, is U4: for every k>=2,
no protected scaffold satisfies every actual source equation for a word that
differs from some constant word at at most four vertices. Full GHZ supplies
all these equations. The named downstream consumer remains exclusion of the
protected scaffold family for the full-source high-surplus route. Four is the
first depth containing a whole component's constant-bearing equation;
shallower conditions hold at zero crossing filling. Success means an exact
proof or a physical countermodel with an explicit remaining full-target error.

At k=2 a 4,881-row necessary model reports UNSAT. Its first native Glucose
trace was truncated and rejected by drat-trim, so that attempt is failed.
A new standalone Linux CaDiCaL 1.7.3 run on the identical CNF completed with
UNSAT and a proof accepted by drat-trim -U (zero RAT steps). This is local
calibration, not the all-k theorem, and it is not the portable accepted full
source fixture. Raw calibration artifacts remain in tmp/scaffold-u4-k2.

The uniform analysis classifies an arbitrary minority set by its exposed
majority partners and fully consumed majority matching pairs. For at most
four minorities it is a closed interaction system of degree at most four,
with zero, one or two exterior resources. This raises the wider parent: can
any fixed minority-depth truncation uniformly exclude the protected scaffold?
The [fixed-depth no-go theorem](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_FIXED_MINORITY_DEPTH_NO_GO.md)
now refutes that entire family of uniform parents. The n=248 base uses 62 K4
components and exact +1,-1 pair gadgets on a girth-six labelled graph. Every
source word through depth five passes by a matching-cut parity argument;
an explicit mixed component coloring has amplitude one. For arbitrary fixed
r, finite permutations of reduced words give a graph cover of girth greater
than r, preserving that failure word. The proof is constructive and uniform;
finite checks are companions, not an exhaustive computation over r. A fresh
independent proof review checks the forest argument, factorization, directed
minority cycle, finite group construction and explicit failure.

The proof-topology delta is therefore stronger than another finite exclusion:
no fixed-depth selection of these full source equations can close the
protected scaffold uniformly. This does not claim that every finite proof
method fails, that r may grow with n, or that a full source counterexample
exists. These sparse controls are not assigned the generic maximum-root-five
property of the earlier structural theorem.

## Sharper unresolved parent Q4

For every k>=2, do all 3^k component-constant target equations, together with
every full source equation at minority depth at most four, exclude the
protected scaffold over C? This is the next exact parent, supplied by any full
GHZ witness and consumed by the same scaffold-exclusion step. A proof must
retain the shared exterior-resource sums; a countermodel must supply actual
weights and an explicit full-target failure before any promotion.

The third eight-vertex Laurent family passes all component-constant and
independent-minority equations but fails depth four. The new graph lifts pass
arbitrary fixed depth but fail a global component-constant word. Neither
refutes Q4. On the specific pair-allocation gadget family, component-constant
amplitudes factor as a product of (1-1) over compatible gadgets; hence those
targets ask whether the labelled component graph has only its three constant
colorings avoiding compatible edges. This is a precise subproblem for that
family, not a reduction of arbitrary protected fillings to pair gadgets.

No third sibling census is authorized merely by this finite checkpoint. The
next research must attack Q4, an exact no-go to it, or a sublemma shown to be
load-bearing for it. Global Krenn-Gu remains UNRESOLVED.
