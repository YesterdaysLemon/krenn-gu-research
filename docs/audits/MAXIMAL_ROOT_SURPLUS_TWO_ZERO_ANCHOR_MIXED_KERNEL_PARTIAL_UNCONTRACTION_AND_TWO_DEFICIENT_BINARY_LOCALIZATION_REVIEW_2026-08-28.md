# Hostile review: mixed-kernel partial uncontraction and two-deficient localization

## Review target and verdict

Target reviewed:

claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_MIXED_KERNEL_PARTIAL_UNCONTRACTION_AND_TWO_DEFICIENT_BINARY_LOCALIZATION_THEOREM.md

Supporting artifacts reviewed:

claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py
claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py

**Verdict: PASS for the exact GLS63 scope, with the residual explicitly
open.** The written argument correctly proves the mixed same-source
hierarchy, the common-support incidence floor, the singleton
deficient/nonaxis synchronization implication, and the root-order-three
exactly-two-deficient localization. It does not claim to exclude the final
same-kernel binary residual. The q4 cancellation is valid for distinct
directions once pair/deck products are placed in canonical labelled order;
the independent audit now checks that distinct-direction case.

This review is mathematical and evidentiary only. It does not promote the
local controls to a source-integrability theorem, response or selector
theorem, or global resolution. The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Scope and upstream supply

The proof is correctly scoped to characteristic zero, the zero-anchor branch,
root order three, six torus-rigid auxiliary labels, and exactly two deficient
joint probe maps in the final localization. It starts from the complete
GLS8 physical matching identity and retains one actual H-tensor from one
graph. GLS55, GLS58, GLS61, and GLS62 supply the stated rank, kernel,
contraction, partial-uncontraction, and one-deficient inputs.

For arbitrary deficient set N, the mixed hierarchy chooses independent
generic vectors in the whole kernels of selected deficient labels, cross
products at selected injective nonaxis labels, and leaves every pure-probe
axis open. A pair is killed only when it meets a contracted label; hence the
structurally retained pair set is exactly binom(S,2). This is a direct
partial evaluation of the complete same-source identity, not an atlas of
independently assigned decks. A retained term or its deck may still vanish,
which the theorem preserves.

The theorem uses fraction-field quotients only after the polynomial identity
is established. The deficient quotient keeps exactly the colours in

~~~
A_n={a : e_(n,a)^* is nonzero on K_n},
~~~

and the pure-axis active-line quotient does not kill any fixed coordinate
covector because its active row is a full variable row. These are the
correct quotient semantics.

The reviewed checkpoint now states `|N|>=2` explicitly in Lemma 4.  This is
the exact scope used by the two-deficient localization and avoids silently
choosing a convention for `A_empty` in a standalone all-`N` reading.

## Incidence and common-support floor

Lemma 2 is sound. Leave all deficient and pure-axis slots open, contract
the injective nonaxis labels, quotient every deficient slot except one
chosen n, and quotient every pure-axis active line. Every retained pair
meets a quotiented slot. An a visible on all deficient kernels cannot have
E_a empty, since the untouched n coordinate separates its target colour
from the other diagonal colours.

Lemma 3 correctly strengthens this to |E_a|>=3 for every colour visible on
all deficient kernels. For |E_a|<=1, leave the deficient and pure slots
plus at most one nonaxis zero label open; every source companion is killed,
while the selected target colour survives and is isolated at the open
nonaxis slot. For E_a={u,v}, leave both zero labels open. All source pairs
except {u,v} are killed by the deficient/pure quotients. The actual
remaining complementary deck is forced nonzero by the equality, and a
functional on that deck forces g_(uv) to be supported only at (a,a).
The four injective nonaxis orientation pairs rule this out. There is no
unlicensed deck division or independent-deck substitution.

The resulting count

~~~
3|A_N| <= |U| <= 6-|N|
~~~

is therefore valid. In the two-deficient case it gives at most one common
kernel-supported colour and rules out four or more deficient labels at this
stage.

## Singleton actual-deck argument

The singleton lemma is an implication, not an exclusion by assertion. If
a is visible on every deficient label except n and E_a={u}, leave all
deficient and pure-axis slots plus u open, quotient every deficient slot
except n, and quotient every pure-axis active line. The only source pair
not killed is {n,u}. The target colour is isolated by the open u
coordinate; all other colours are killed by an opposite deficient quotient
or by a contracted nonaxis zero. Consequently the actual deck times the
actual companion forces

~~~
g_(nu) is nonzero and pure at (a,a).
~~~

For an X-oriented u, projecting its factor off the a line gives
p_n tensor pi_a(q_u)=0. Injective nonaxis orientation makes the second
factor nonzero, so p_n=0; the remaining pure companion then forces
row(Y_n)=K e_a^*. The Y-oriented case is symmetric. This correctly
forces J_n to rank one with complementary kernel support. Zero decks do not
evade the argument: the nonzero target forces the surviving actual deck
and companion to be nonzero.

## The two-deficient (d=2) census

The written support/rank case split and both finite replays agree:

~~~
support-only:  12,276 -> 1,266 -> 78
typed:         27,621 -> 1,710 -> 78 -> 15
localized categories: 36 / 3 / 24 / 15
~~~

The support-only census enumerates ordered singleton and two-colour kernel
supports, all pure-axis counts from zero through four, and the four remaining
nonaxis zero statuses. The typed census separately includes rank-two
singleton supports, rank-one two-colour supports with their complementary
readout, and rank-two two-colour supports. The singleton rule is applied in
both directions, not inferred from orbit counts.

The support comparison is exhaustive. A two-colour deficient support needs
nonempty disjoint zero sets for both visible colours; any singleton zero
forces the opposite map to be the rank-one complementary readout. Together
with the common-colour three-zero floor, every one/two, two/one, and two/two
support arrangement exceeds the four available nonaxis labels. Thus only
the two singleton-support cases remain:

1. common singleton A_n=A_m={c}, with at least three E_c labels and at
   most one pure axis;
2. distinct singletons A_n={c}, A_m={d}, with |E_c|=|E_d|=2, no pure
   axes, and E_e empty.

The finite ledger is evidence for this finite cover; the written quotient
and deck arguments supply its mathematical bridge.

## Arbitrary-map pure-companion lemma

Lemma 6 is stronger than the finite coefficient checks. If both joint maps
have rank two and the proposed pure coordinate lines lie in their row
spaces, quotient one row plane by its proposed line. Purity gives

~~~
A(z_0) q_t(z_1) + B(z_1) p_t(z_0) = 0.
~~~

If both scalar forms are nonzero, the complete images of both shores at the
other label lie on one common line, contradicting rank two. If exactly one
is nonzero, the corresponding opposite shore vanishes; quotienting the
other factor then forces the remaining shore at the first label to vanish,
making the companion zero. If both vanish, the first rank-two map lies on
the proposed line. This covers arbitrary probe maps over the
characteristic-zero function field, including zero-shore boundaries, and
excludes only a nonzero pure companion as stated.

The primary script's determinant identity and the independent finite plane
census are sanity checks for this lemma; neither is being presented as its
proof.

## Pure-axis count and P=1 target rank

The P=1 closure is correctly separate from the deficient row quotient. In
the same-singleton case, U has three E_c labels. With S={n,m,p},
quotient only the pure-axis active line. Every source pair meeting p is
killed, leaving one actual term

~~~
g_(nm) tensor hbar_p.
~~~

The c target is killed by the three contracted E_c labels. The d and e
target columns survive the pure-axis quotient and are independent: a full
variable active row has a nonzero c component, so no nontrivial
combination of e_d,e_e lies on its line. Therefore the target flattening
across (n,m)|(p) has rank exactly two, while the one-deck source has rank at
most one. This is a genuine rank contradiction, not an inference from a
possibly cancelling one-slot quotient.

The zero-pure-axis assigned-other-zero case is likewise valid: at
S={n,m}, one complementary colour survives and forces a nonzero pure
rank-two companion, which Lemma 6 excludes. The argument covers zero
cross-products at deficient labels because those labels are left open in
the relevant equations.

## Exact residual

The distinct-singleton profile is excluded by S={n,m}. The four
cross-contracted nonaxis labels kill c and d, while e survives. The only
source is the actual scalar complementary deck times g_(nm), so a
nonzero pure (e,e) companion would be required. The common e line lies in
both rank-two row planes, and Lemma 6 applies.

After the pure-axis and assigned-other-zero leaves are removed, the only
remaining exact two-deficient family is

~~~
K_n=K_m=K e_c,
P=empty,
|E_c| in {3,4},
E_d=E_e=empty,
~~~

and its S={n,m} equation is the nonzero binary diagonal identity

~~~
h_(nm) g_(nm)
 =lambda_d e_(n,d)^* tensor e_(m,d)^*
  +lambda_e e_(n,e)^* tensor e_(m,e)^*.
~~~

Both h_(nm) and the two target coefficients are nonzero over the
function field, so g_(nm) is genuinely binary diagonal. The local
opposite-orientation example in the theorem shows that this conclusion is
algebraically nonempty; it is not a claimed witness.

## q3 common-source control

For |E_c|=3, proper subsets give homogeneous equations. The pair-open
constraints only imply that the projected one-port deck h_i annihilates
k_i, hence lies in span_F{p_i,q_i}. With two X orientations and one Y
orientation,

~~~
h_u=-p_u,  h_v=-p_v,  h_w=p_w
~~~

gives the exact labelled identity

~~~
g_(uv) tensor h_w + g_(uw) tensor h_v + g_(vw) tensor h_u
 = -2 p_u tensor p_v tensor q_w,
~~~

which is pure colour c. Thus termwise separation is not valid.

The displayed edge assignment uses one common source table: choose
W_(nm)(x_n,x_m)=1, W_(nx)(x_n,k_x)=1, W_(mx)(x_m,k_x)=0, and for each
i in the three-label set choose r_i with

~~~
W_(xi)(k_x,-)=h_i+r_i,
W_(mi)(x_m,-)=-r_i,
W_(ni)(x_n,-)=0.
~~~

The r_i cancel inside the same physical four-label deck, giving h_i.
This is a fibre-level control of the displayed higher-open tensors, not a
complete GHZ witness or a polynomial source-integrability construction.

## q4 complement indexing and distinct-direction control

The apparent q4 discrepancy was checked directly. Let ports be
0,1,2,3, with

~~~
p=(c,c,s,s),  q=(r,r,c,c),
M_r=c tensor r+r tensor c,
M_s=c tensor s+s tensor c.
~~~

Then same-type companions are g_01=M_r, g_23=M_s, and every
cross-type companion is c tensor c+r tensor s. Assign

~~~
D_01=-M_r/2,  D_23=-M_s/2,
D_02=D_03=D_12=D_13=c tensor c.
~~~

The source sum uses the complementary deck, and every pair/deck product
must first be placed in canonical slot order (0,1,2,3). The two
same-type terms contribute -M_r tensor M_s; the four cross-type off-colour
terms contribute +M_r tensor M_s, leaving

~~~
sum_(i<j) g_(ij) tensor D_(complement(ij))
 =4 c tensor c tensor c tensor c.
~~~

This identity holds for arbitrary r,s, not only r=s. The primary SymPy
verifier and the corrected independent standard-library audit both check
the distinct fibre r=e_1,s=e_2. The earlier independent-script comment
that restricted the check to r=s was a coverage/documentation issue, not
a mathematical failure; it has been corrected in the reviewed working tree.

The q4 control is explicitly fibre-level and does not claim that the six
displayed decks, together with the probe rows, form a complete Krenn--Gu
witness. The shared-edge assertion is only that one common polarization can
produce these displayed pair blocks, e.g. with h=1 and
W_(ij)=D_(ij)-a_i tensor b_j-b_i tensor a_j.

## Remaining obligation and status walls

The theorem correctly leaves open the function-field restriction-separation
statement coupling all homogeneous proper-subset equations to the nonzero
binary S={n,m} contraction. Pointwise q3/q4 cancellation controls show
why polarization and termwise purity cannot supply that statement. The
remaining lemma must control the h W_(uv) branch as well as the shared
a,b rows; it must not silently replace the actual physical decks by
independent tensors.

The theorem does not close profiles with three or more deficient maps, the
unique-nonrigid branch, nonzero anchor, arbitrary root order, response,
selector, nuisance survival, synchronization/activity, attachment, or any
downstream detector. No global conjecture status change is justified.

## Parent-theorem checkpoint

The theorem contains a serious parent attempt: it states the parent
proposition and quantifiers, identifies the GLS8/23/55/58/61/62 supply,
synthesizes the mixed-kernel hierarchy with the earlier quotient and
orientation mechanisms, tests the rank-one/rank-two/pure-axis and mixed
orientation controls, records the exact residual, and updates the live
frontier and arbitrary-order README. It therefore satisfies the
“no third sibling theorem without a serious parent-theorem attempt” gate for
this lane. The proof-topology delta is localization to one binary residual,
not branch closure.

## Replay evidence

Both commands were rerun from
C:\w\kg-universal-source-parent-20260828 after the distinct-direction q4
audit correction.

Primary:

~~~powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py
~~~

Exit code 0; reported:

~~~text
support_only_ordered_total: 12276
support_only_after_incidence_floors: 1266
typed_options_total: 9
typed_profiles_total: 27621
typed_after_incidence_floors: 1710
typed_after_singleton_companion_rule: 78
refinement_distinct_supports: 36
refinement_same_support_P1: 3
refinement_same_support_P0_assigned_other_zero: 24
refinement_final_residual: 15
two_rank2_pure_companion_no_go_checks: 2
P1_flattening_target_rank: 2
allowed_binary_diagonal_checks: 1
q3_orientation_patterns: 8
q3_homogeneous_failures: 2
q3_mixed_patterns_allow: 6
q3_XXY_minus_2_pure_identity: 1
q4_six_pair_cancellation_checks: 1
PASS: exact two-deficient profile audit and local binary/orientation controls (audit only; global Krenn-Gu conjecture remains unresolved)
~~~

Independent standard-library audit:

~~~powershell
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py
~~~

Exit code 0; reported:

~~~text
support-only ledger: 12276 -> 1266 (incidence/common-three) -> 78 (singleton-compatible)
typed ledger: 27621 -> 1710 (incidence/common-three) -> 78 (singleton-compatible) -> 15 (q4 residual)
localized categories: 36/3/24/15
mixed pair-survival masks: 729
row quotient checks: 18; incidence profiles: 4182
rank-two pure-companion finite cases: 27648
P1 quotient separation checks: 192
binary g_nm controls: 3
q3 XXY triangle support terms: 1
q4 six-pair support terms (distinct r=e1,s=e2 fibre): 1
PASS (GLS63 audit scope only; no global closure claim)
~~~

Static validation also passed:

~~~powershell
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_mixed_kernel_partial_uncontraction_and_two_deficient_binary_localization.py
~~~

All three commands exited 0 (All checks passed; 2 files already
formatted). The primary and independent programs audit finite/displayed
leaves only; they do not prove the written same-source function-field
restriction-separation obligation.

Final review status: **PASS for GLS63 exactly-two-deficient localization;
residual open; global Krenn--Gu conjecture UNRESOLVED.**
