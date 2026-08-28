# Hostile review: three-deficient pair classes and dual `P_3` localization

## Review target and verdict

Target reviewed:

`claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_THREE_DEFICIENT_PAIR_CLASS_AND_P3_ORBIT_LOCALIZATION_THEOREM.md`

Supporting artifacts reviewed:

`claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py`

`claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py`

**Verdict: PASS for the exact `GLS67` scope after two independent hostile
reviews and two finite replays.**  No load-bearing algebraic defect was
found.  The result gives a uniform two-open pair-class theorem, an exact
finite three-deficient census, two same-source `P_3` extractions, and an
exact common-support exclusion.

The initial census has `453` labelled profiles in ten orbits.  The
all-deficient-kernel `P_3` equation excludes the two common-support orbits,
leaving exactly

```text
432 labelled profiles in eight colour/map orbits.     (1)
```

The eight residual orbits, four-plus-deficient branches, unique-nonrigid
branch, attachment, response, selector, synchronization, activity, nonzero
anchor, arbitrary root order, and the global conjecture remain open.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## Pair-class extraction

For distinct deficient labels `i,j`, contract every other deficient label
at a generic vector of its joint kernel, contract every nonaxis label at its
cross product, leave the pure-axis labels open, and quotient their active
full-support lines.  Every source pair except `{i,j}` is killed.  A target
colour initially survives exactly when

```text
N-{i,j} subseteq M_a,          E_a=empty.
```

Quotienting the open `i`-slot by `row J_i` and isolating colour `a` at `j`
forces `a notin A_i`; the symmetric quotient forces `a notin A_j`.
Therefore every surviving colour has

```text
M_a=N-{i,j}.                                           (2)
```

The exact remaining identity is one actual companion `g_ij` times one
quotient of the original complementary physical deck.  No deck is selected
independently.  If its target class has size `k`, both open row spaces have
rank at least `k`; a pure-axis quotient forces `k<=1`, no pure axis forces
`k<=2`, and `k=1` is impossible when both open maps have rank two by the
accepted pure-companion no-go.  The review confirmed that the pure-axis
argument uses the inherited fact that its active covector has all three
coordinates nonzero.

## Exact finite census

For three deficient maps, the nine exact rigid types are

```text
S_c: rank 2, A={c};
R_c: rank 1, coordinate readout c, A={0,1,2}-{c};
T_c: rank 2, A={0,1,2}-{c}.
```

Each of the other three labels is pure-axis or nonaxis, and a nonaxis cross
product has no zero coordinate or one of three zero coordinates.  The two
implementations independently replayed

```text
61,965  typed profiles
 2,367  after GLS63 incidence and singleton constraints
   516  after the pair-class constraints
   453  after the full-cross local target-span condition
    10  canonical localized orbits.                  (3)
```

All `516` pair-class survivors have `P=empty` and `|U|=3`.  The census is a
necessary-profile calculation; it does not assert that a residual profile
extends to a physical witness.

## Full-cross `P_3` and pair/deck coupling

Cross-contract all three members of `U` and leave the deficient labels
open.  If `{i,j,k}=N`, let `h_k` be the actual remaining one-port physical
deck.  The six pair/order choices are exactly the six permutations of the
source labels `P,Q,H`, so

```text
(L_0 tensor L_1 tensor L_2)P_3
 =sum_(a:E_a=empty) kappa_a e_(0,a)^* tensor e_(1,a)^*
                                      tensor e_(2,a)^*,
L_i(P)=p_i, L_i(Q)=q_i, L_i(H)=h_i.                  (4)
```

The scalar deck in the two-open equation is not a second object.  It is
exactly `h_k(x_k)`, where `x_k` is the generic vector in the third
deficient kernel.  Hence a nonempty pair class makes `h_k` nonzero on that
kernel, puts it outside `row J_k`, and forces `rank L_k>=2`.

The exact decomposable- and zero-`P_3` classifications apply over the
characteristic-zero function field because their proofs are algebraic.
They give the binary/pure/zero fork in the theorem.  The hostile review
specifically confirmed the repaired distinction between `rank J_i` and
`rank L_i`: rank two of the former is never used by itself to infer rank two
of the latter.

For a pure target, a rank-one `L_i` has image equal to the fixed target
line, forcing `J_i` to be the corresponding rank-one readout.  The
pair/deck coupling and the exact sign-chart zero pattern further force the
displayed `R_2` map to have rank-one `L_i` in residual orbits 7 and 8.
For a zero target, either some `L_i` has rank one or the zero-`P_3` theorem
gives exactly one of the uniform alternatives `X_N=0`, `Y_N=0`, or
`h_N=0`.

## Kernel-side `P_3` and common-support exclusion

Contract all three deficient kernels and instead leave all three nonaxis
labels open.  The same six-term count gives a second exact `P_3` equation:

```text
(tensor_(u in U) K_u)P_3
 =sum_(a in A_N) theta_a tensor_(u in U)e_(u,a)^*,
K_u(P)=p_u, K_u(Q)=q_u, K_u(H)=d_u.                  (5)
```

Each `d_u` is one complementary deck from the fixed graph.  It depends on
the deficient-kernel variables but not on either probe-variable set.  Each
`K_u` has rank at least two because `u` is injective and nonaxis.

If `A_N` is empty, (5) is zero.  The zero-`P_3` theorem makes all three
source rowspaces one common coordinate plane.  The independent `p_u,q_u`
columns rule out omission of `P` or `Q`, so the plane omits `H` and

```text
d_u=0 for all u in U.                                 (6)
```

If `A_N={c}`, the GLS63 three-zero floor gives `E_c=U`, so every `u` has an
exact `X`- or `Y`-orientation at `c` and (5) has a nonzero pure target.
The hostile reviews checked all orientation words.

- In the all-`X` case, quotienting two slots off the `c`-line gives
  `bar q_i tensor bar d_j+bar d_i tensor bar q_j=0`.  The transverse
  coefficient span of each `q_i` is two-dimensional while the `d` rows are
  probe-independent, forcing every `bar d_i=0`.  The three one-slot
  equations then force the remaining scalar components to vanish in
  characteristic zero.  The all-`Y` case is symmetric.
- In the mixed `X,X,Y` case, the two-`X` quotient first puts the two
  corresponding decks on their `c`-lines.  A one-slot quotient gives
  `alpha_j d_k+delta_j p_k=0`.  The `Y`-oriented transverse coefficient
  span of `p_k` is two-dimensional, forcing `delta_j=0` and `d_k=0`; the
  symmetric equation kills the last deck.  Probe exchange and port
  permutation cover every mixed word.

Thus the source in (5) would be zero while its pure target is nonzero.
Exactly census orbits 1 and 6 have common support, with multiplicities `3`
and `18`.  Removing them gives (1).

The older mixed-orientation controls do not contradict this argument: they
choose rows proportional to probe rows after specializing a fibre.  An
actual deck in (5) cannot track the probe variables, and the theorem uses
the full function-field identity.

## Controls and remaining integrability wall

Exact abstract restrictions of `P_3` realize all three remaining endpoint
types: a common full-support plane has binary hyperdeterminant `-48`, a sign
chart gives a nonzero decomposable tensor, and the common `span{P,Q}` plane
gives zero.  These are source controls, not physical graph witnesses and not
profile-compatible solutions by declaration.

The remaining deficient-side deck has the exact physical expansion

```text
h_i=W_(iu)(-,k_u)w_(vw)
   +W_(iv)(-,k_v)w_(uw)
   +W_(iw)(-,k_w)w_(uv).                              (7)
```

At one fixed fibre a nonzero internal cofactor allows the distinct incident
edges to prescribe these rows independently.  The missing lemma must
therefore couple (6), (7), the pair-class equations, and higher-open members
over the common function field.  A fibrewise choice of unrelated bases or
decks is not sufficient.

## Replay evidence

The following commands were rerun in the isolated working tree:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_deficient_pair_class_and_p3_orbit_localization.py
```

Both finite implementations returned

```text
61,965 -> 2,367 -> 516 -> 453 -> 432,
10 localized orbits -> 8 residual orbits.
```

The primary also checks the six source assignments, binary
hyperdeterminant, and pure/zero controls.  The standard-library audit uses a
separate support-mask implementation.  Compilation and Ruff checks passed.
The scripts audit the finite and displayed leaves; the same-source and
orientation quotient arguments remain the written proof.

Final review status: **PASS for `GLS67`; common-support three-deficient
profiles empty; eight three-deficient orbits and the global Krenn--Gu
conjecture UNRESOLVED.**
