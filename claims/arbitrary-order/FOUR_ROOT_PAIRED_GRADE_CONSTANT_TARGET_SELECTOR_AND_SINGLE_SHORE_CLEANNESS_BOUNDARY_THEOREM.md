# Four-root paired-grade constant target selector and single-shore cleanness boundary

## Status

**Exact characteristic-zero cross-depth decomposition, conditional detector,
and sharp clean-selector no-go.**  At four roots with four ports and a named
residual pair, the zero-root-edge and one-root-edge matching grades obey two
displayed tensor identities.  One zero-grade equation cancels the direct
`hB` response nuisance exactly when a same-index alignment condition holds.
The nonzero complementary pairing `Omega=l^T Jp` does not imply this
alignment.

The identities also make the target-purity requirement exact.  A rational
function-field inverse of the surplus-two sensor need not preserve the
diagonal GHZ target space.  A mixed corrected response becomes an actual
target detector only through constant, synchronized target selectors, with
every displayed nuisance killed or itself supplied as a constant combination
of target-diagonal equations.

There is a sharp single-shore coefficientwise-cleanness no-go.  Under that
scoped ansatz, a root-pair shore with nonzero `Omega` cannot both isolate the
residual-absent `H_U` column and carry a nonzero corrected response channel.
One explicit sufficient route uses a response selector, its synchronized
zero-grade direct companion, and a separate target-pure `H_U` anchor, unless
an exact graph-specific nuisance identity replaces one of them.  This is not
a global lower bound: multi-shore, aggregate, shared-anchor, and two-selector
graph-specific alternatives remain open.  The ternary root--residual
assignment fan has enough raw capacity: its six columns can have rank six in
the nine-dimensional two-residual tensor space.  The obstruction in the
displayed route is simultaneous nuisance annihilation, not assignment rank
alone.

Exact physical controls show that `Omega!=0` neither forces cross-depth
alignment nor prevents nested cancellation of a nonzero corrected response by
the direct and cross sectors.  These are proof-route countermodels, not graph
witnesses.  No weighted permanent restriction is extracted.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

This theorem refines the target interface of the
[`same-graph response-defect boundary`](SAME_GRAPH_RESPONSE_DEFECT_VANISHING_AND_TARGET_COUPLED_SELECTOR_BOUNDARY_THEOREM.md)
using the raw pair-companion and physical-fibre distinction from the
[`surplus-two rank-drop theorem`](MAXIMAL_ROOT_SURPLUS_TWO_NONZERO_PAIR_COMPANION_AND_PHYSICAL_RANK_DROP_SHARPNESS_THEOREM.md).
It uses the companion-depth organization of the
[`surplus-two complete-deck sensor`](MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md),
but assumes no permanent or co-two restriction.

## 1. Four-root paired-grade notation

Work over a characteristic-zero field `K`.  Let

```text
R={1,2,3,4},       B=U disjoint-union Q,
|U|=4,             Q={q0,q1}.                         (1)
```

Fix root vectors `y_i` and residual vectors `z_q`, while leaving every port
in `U` open.  Write

```text
l_A=B_(i,j)(y_i,y_j),              A={i,j} subset R,
h=B_(q0,q1)(z_q0,z_q1),
H_(i,q)=B_(i,q)(y_i,z_q),
H_(i,u)=B_(i,u)(y_i,-).                             (2)
```

For an even outside set `E subset B`, `H_E` is its physical
perfect-matching tensor, with the `Q` slots evaluated and the `U` slots open.
For equally sized sets `S,D`, let `per H_(S,D)` be the permanental root--outside
incidence tensor.

For every root pair `A`, define

```text
p_A=per H_(A,Q),
U_A=sum_(uv in binom(U,2))
      B_uv per H_(R-A,U-{u,v}),
K_uv=H_(q0,u)H_(q1,v)+H_(q0,v)H_(q1,u),
Pi_A=sum_(uv in binom(U,2))
       K_uv per H_(R-A,U-{u,v}),
Lambda_A=h U_A+Pi_A,
V=per H_(R,U).                                        (3)
```

Thus `Pi_A` is the four-row permanent

```text
P_4(H[R-A];H_q0;H_q1).                               (4)
```

Let `J` complement root pairs and put

```text
Omega_Q=sum_A l_A p_(R-A)=l^T Jp.                    (5)
```

The exact one-root-edge and zero-root-edge grades are

```text
Y_1=sum_A l_A sum_(D subset B, |D|=2)
      (per H_(R-A,D)) H_(B-D),
Y_0=sum_(D subset B, |D|=4)
      (per H_(R,D)) H_(B-D).                         (6)
```

Finally define the one-residual cross sectors

```text
C_1=sum_A l_A sum_(q in Q,u in U)
      (per H_(R-A,{q,u})) H_((Q-{q}) union (U-{u})),
C_0=sum_(q in Q,u in U)
      (per H_(R,{q} union (U-{u}))) H_((Q-{q}) union {u}).
                                                               (7)
```

All products are canonically embedded in `tensor_(u in U)V_u^*`.

## 2. Exact adjacent-grade decomposition

Let

```text
mathcal U:K^6 -> tensor_(u in U)V_u^*,
e_A |-> U_A,
Pi(l)=sum_A l_A Pi_A.                                 (8)
```

### Theorem 1 (paired-grade identities)

The physical matching partition gives

```text
Y_1=Omega_Q H_U+h mathcal U(l)+Pi(l)+C_1,             (9)
Y_0=hV+mathcal U(p)+C_0.                             (10)
```

### Proof

In `Y_1`, fix the unique internal root pair `A`.  Partition the two outside
vertices matched to the remaining roots by their intersection with `Q`.

- If both are `Q`, their incidence coefficient is `p_(R-A)` and the four
  ports contribute `H_U`.  Summing over `A` gives `Omega_Q H_U`.
- If neither is in `Q`, rename the complementary port pair `{u,v}`.  Expanding
  `H_(Q union {u,v})` according to whether `q0q1` is an edge gives
  `hB_uv+K_uv`.  These are `hU_A+Pi_A`.
- If exactly one lies in `Q`, the term is precisely in `C_1`.

This proves (9).

In `Y_0`, partition the four outside vertices matched to roots by their
intersection with `Q`.  Matching all roots to `U` leaves `q0q1` and gives
`hV`.  Matching both residuals to a root pair `A` and expanding the remaining
two-root assignment gives `p_AU_A`.  Matching exactly one residual to a root
gives `C_0`.  These cases are disjoint and exhaustive, proving (10).  QED.

## 3. The alignment criterion

### Theorem 2 (one-equation direct-nuisance cancellation)

Assume `h!=0`.  A scalar `kappa` cancels the direct `hU_A` combination in
`Y_1` using the one zero-grade equation `h kappa Y_0` exactly when

```text
l-kappa p in ker mathcal U.                           (11)
```

Under (11),

```text
Pi(l)=Y_1-h kappa Y_0-Omega_Q H_U-C_1
      +h^2 kappa V+h kappa C_0.                       (12)
```

If `mathcal U` is injective, (11) is equivalent to `l=kappa p`.
Nonvanishing `Omega_Q=l^T Jp` does not imply (11).

### Proof

Subtract `h kappa` times (10) from (9).  The direct part is
`h mathcal U(l-kappa p)`, which, because `h!=0`, vanishes exactly under (11).
Rearrangement gives (12).  Injectivity gives the final statement.
Complementary pairing and same-index proportionality are distinct algebraic
conditions.  If `h=0`, the direct nuisance is already absent and (11) is only
a sufficient bookkeeping condition, not a necessary one.  QED.

An exact physical incidence control makes the distinction visible.  Set the
only nonzero evaluated root edge to `l_12=1`.  Set

```text
H_(3,q0)=H_(4,q1)=1                                  (13)
```

and every other root--residual incidence to zero.  Then `p=e_34` and
`l^T Jp=1`.  On the ports let the only direct block be
`B_(u1,u2)=e0 tensor e0`, and set

```text
H_(3,u3)=H_(4,u4)=e0,
H_(1,u3)=H_(2,u4)=e1,                                (14)
```

with every other root--port incidence zero.  These evaluated covectors and
blocks extend to ordinary bilinear edge blocks.  Direct substitution in (3)
gives

```text
U_12=e0 e0 e0 e0,        U_34=e0 e0 e1 e1.           (15)
```

The two tensors are independent, so no `kappa` satisfies (11).

## 4. Constant target purity is an additional theorem hypothesis

Let

```text
Delta_U=span{tensor_(u in U)e_(u,c)^*:c=0,1,2}.       (16)
```

A contraction is **target-derived on `U`** only when it is a `K`-linear
combination of full GHZ coefficient contractions whose coefficients are
independent of the open `U` variables.  Such a contraction lies in
`Delta_U`.  A selector with coefficients in `K(X_U)` is not target-pure by
definition and need not preserve (16).

### Proposition 3 (rational inversion is not target purity)

On the open set `z_v[0]!=0`, consider the diagonal target

```text
J=e0^R z_u[0]z_v[0]+e1^R z_u[1]z_v[1].               (17)
```

The rational root functional

```text
lambda(z)(e0^R)=z_v[1]/z_v[0],
lambda(z)(e1^R)=0                                    (18)
```

sends `J` to the mixed monomial `z_u[0]z_v[1]`.  Hence function-field
recovery of the physical deck does not by itself make a recovered tensor a
zero-mixed target coefficient.

### Corollary 4 (exact conditional detector)

Assume `h!=0` and (11).  In every case assume `Y_0` and `Y_1` are supplied by
constant synchronized target selectors.  In addition, assume either that
`H_U,C_1,V,C_0` are each supplied by constant synchronized target selectors,
or that their displayed combination

```text
N=Omega_Q H_U+C_1-h^2 kappa V-h kappa C_0            (19)
```

is proved target-diagonal by an exact same-shore identity.  Then `Pi(l)` is
target-diagonal.  If an exact physical computation gives a nonzero mixed
entry of `Pi(l)`, the same entry of (12) is a nonzero constant linear
combination of mixed GHZ coefficients; therefore at least one displayed full
target coefficient is nonzero.

This conclusion is invalid if `N` is merely known as graph data or is
subtracted with a rational function of the open port variables.

## 5. The open-residual assignment fan and a sufficient selector package

Now leave the two residual slots open.  Put

```text
a_i=B_(i,q0)(y_i,-),       b_i=B_(i,q1)(y_i,-),
kappa_(ij)=a_i tensor b_j+a_j tensor b_i.             (20)
```

The zero-grade tensor partitions as

```text
Y_0^Q=sum_A kappa_A tensor U_A+B_Q tensor V+N_0^Q,   (21)
```

where `N_0^Q` is the sector in which exactly one residual is matched to a
root.  For a named internal root shore `A`, with `C=R-A`, the corresponding
one-grade tensor is

```text
Y_(1,A)^Q=kappa_C tensor H_U+B_Q tensor U_A
          +Pi_A^Q+N_(1,A)^Q.                         (22)
```

Here `Pi_A^Q` is the honest open-residual four-row permanent and `N_(1,A)^Q`
is the one-residual cross sector.

Call an isolation **formal coefficientwise** when the labelled tensors
`U_A`, `V`, and the coefficient tensors of `N_0^Q` are treated as independent
records, before any graph-specific equality or aggregate cancellation among
them.

### Theorem 5 (constant coefficientwise assignment selector criterion)

A constant residual functional formally isolates the labelled coefficient
`U_A` from (21) exactly when it is one on `kappa_A` and zero on

```text
{kappa_A':A'!=A} union coefficient_Q(B_Q tensor V+N_0^Q).  (23)
```

Equivalently `kappa_A` is outside the span of the tensors in (23).  For one
fixed physical graph, (23) is sufficient but need not be necessary because
the labelled coefficient tensors may vanish or cancel in aggregate.  Full rank
of the six-column map `e_A |-> kappa_A` labels the six `U_A` only modulo the
nuisance space; it does not imply (23).

The assignment fan can have rank six.  In a ternary residual space take

```text
v1=e1, v2=e2, v3=e3, v4=e1+e2+e3,
a_i=b_i=v_i.                                          (24)
```

In the symmetric-square basis, the six `kappa_ij` have determinant of
absolute value eight.

### Proof

Equation (21) follows by partitioning zero-grade matchings according to the
number of residual vertices assigned to roots.  A linear functional isolates
one coefficient exactly under (23).  For (24), the columns `12,13,23` give
the three off-diagonal basis vectors.  Subtracting them from `14,24,34`
leaves twice the three diagonal basis vectors, so the determinant has absolute
value eight.  QED.

Equations (21)--(22) exhibit one sufficient constant-selector package for a
nontrivial detector:

1. one constant root-pair response selector for (22);
2. one synchronized constant zero-grade selector for its `U_A` term;
3. a separate target-pure `H_U` anchor, or a proved target-diagonal identity
   killing the `kappa_C tensor H_U` term.

This list is not proved minimal outside the single-shore coefficientwise
ansatz of Theorem 6.

## 6. A single shore cannot be coefficientwise clean and nontrivial

Fix a root pair `A0` and impose the following single-shore hypotheses.

1. `l_A=0` for `A!=A0`, while `l_A0!=0`.
2. Roots in `A0` have zero outside incidence, so no other root grade or shore
   contributes.
3. With `C=R-A0={i,j}` and

   ```text
   v_b=(H_(i,b),H_(j,b))^T,
   <x,y>=x^T J y,                                     (25)
   ```

   the selector is coefficientwise clean for `H_U`:

   ```text
   <v_q0,v_q1>!=0,
   <v_b,v_c>=0 for every pair {b,c}!=Q.               (26)
   ```

Condition (26) is a formal independent-cofactor-column condition.  Aggregate
cancellation among a particular graph's cofactor tensors does not imply it.

### Theorem 6 (single-shore columnwise-cleanness no-go)

Under (26), at most one port incidence vector `v_u` is nonzero.  Consequently

```text
U_A0=Pi_A0=Lambda_A0=0.                               (27)
```

Thus one nonzero `Omega` word cannot both isolate `H_U` coefficientwise and
carry a nonzero corrected response channel.

### Proof

If `v_q0,v_q1` are independent, the two rows `v_qs^T J` form an invertible
map, and the cross equations in (26) force every `v_u=0`.

If they are dependent, their common line is nonisotropic because their mutual
pairing is nonzero.  Its `J`-orthogonal complement is a one-dimensional
nonisotropic line.  Hence every `v_u` lies on that line, say
`v_u=w tensor alpha_u`, with `<w,w>!=0`.  The port-pair equations in (26)
give `alpha_u tensor alpha_v=0` for `u!=v`, so at most one is nonzero.  Every
two-port permanent therefore vanishes, proving (27).  QED.

The numerical bound "at most one" is attained by taking

```text
v_q0=v_q1=(1,1),       v_u0=(1,-1),
v_u=0 for u!=u0.                                      (28)
```

Then (26) holds and exactly one port vector is nonzero; as asserted, the
two-port response remains zero.  By contrast, if every `v_u=(1,-1)`, the
desired weight is still two and every one-residual cross coefficient is zero,
but every port-pair coefficient is `-2`.  This second control drops the
port-pair part of (26) and shows that cross cleanness alone leaves the complete
six-face response nuisance.

## 7. Nested physical cancellation is real

At one mixed coordinate word, take the following scalar edge entries and set
every unlisted entry to zero:

```text
r1r2=1;
r1q0=r2q1=r3q0=r4q1=1;
r1u1=1/2, r2u2=r3u3=r4u4=1;
q0q1=1, q0u2=1, q1u1=-3, u1u2=1, u3u4=2.            (29)
```

For the internal shore `A={1,2}`, exact matching enumeration gives

```text
Omega_Q=1, H_U=2, U_A=1, Pi_A=-3, Lambda_A=-2,
Y_1=0, Y_0=0.                                         (30)
```

Thus both adjacent physical matching-grade contributions vanish even though the
selector weight, direct companion, residual-absent anchor, and corrected
response are all nonzero.  The cancellation uses both `hU_A` in the one-grade
equation and `C_0` in the zero-grade equation.  This is an exact physical
matching control.

### Maximum-root triple-blocker realization

The scalar control lies on the same graph-side incidence stratum as the
universal maximal-root data.  Give every mode the basis `e0,e1,e2`, take

```text
x_i=(1,1,1),
y_1=y_2=e0,       y_3=y_4=e1,
z_q0=z_q1=z_u1=z_u2=e0,
z_u3=z_u4=e1.                                        (31)
```

Use

```text
B_12=(e0^*-e1^*) tensor (e0^*-e1^*)                  (32)
```

and zero for the other root--root blocks.  Realize every scalar entry in
(29) by its selected coordinate monomial.  For each low selected outside
mode `q0,q1,u1,u2`, add the helper terms

```text
e0_(r3)^* tensor e1^*,       e0_(r4)^* tensor e2^*,  (33)
```

and for each high selected mode `u3,u4`, add

```text
e1_(r1)^* tensor e0^*,       e1_(r2)^* tensor e2^*.  (34)
```

Helpers may be added to an already nonzero block.  They vanish on the
selected root word in (31).  Fill every otherwise absent outside--outside
block with `e2^* tensor e2^*`.

At the base roots `x_i`, every outside row span is all of `(K^3)^*`: its
assigned scalar edge supplies the selected coordinate and (33) or (34)
supplies the other two.  Thus all six outside modes are triple blockers.
Every outside--outside block is a nonzero coordinate monomial, so a torus-root
set contains at most one outside mode.  Each outside has an assigned
root--outside coordinate monomial, so including it excludes at least one old
root.  Hence every torus-root set has order at most four, while the displayed
four roots have zero pair evaluations by (32); `R` is maximum.

The helpers and filled blocks vanish on the selected word, so (30) is
unchanged.  Exact full-state evaluation gives pure coefficients `(0,0,0)`
and mixed coefficient

```text
C_0000001211=4.                                      (35)
```

The control is therefore decisively not a Krenn--Gu witness.

## 8. Exact GL consequence

The four-root detector edge is therefore

```text
some raw p_A!=0                                PROVED for maximum-root,
                                                blocker-saturated s=2 cells;
augmented Omega_Q=l^T Jp!=0                    SEPARATE / NOT FORCED;
same-index p=0/p=1 alignment                  SEPARATE / NOT FORCED;
constant target-pure response selector        SEPARATE / NOT FORCED;
constant target-pure H_U or nuisance anchor   SEPARATE / NOT FORCED;
all augmented/alignment/target conditions     conditional mixed detector;
one coefficientwise-clean shore               PROVED TRIVIAL RESPONSE;
nested direct/cross cancellation               PROVED possible.          (36)
```

This closes the proposed four-root single-shore, coefficientwise-clean
one-word first-defect route.  It replaces that route with one explicit
sufficient multi-selector theorem shape: two synchronized target-pure
response depths plus a separately supplied residual-absent anchor, or an
equally explicit same-shore nuisance identity.  It does not prove this shape
minimal.  Supplying a legal constant `l` with `l^T Jp!=0`, the aligned
selectors, and the nuisance anchor on every hypothetical-witness rank-drop
cell remains open.  The `h=0` detector branch of the upstream target identity
is separate from Theorem 2.

## 9. Exact verification boundary

The focused verifier expands the full generic ten-vertex hafnian, separates
the zero-root-edge and one-root-edge grades, and checks (9)--(10) against the
displayed decompositions.  It also checks the assignment-fan determinant,
the alignment control, the rational target-purity counterexample, the
single-shore controls, and (29)--(30).

The no-import audit uses a separate perfect-matching generator and a
root-partition ledger, with standard-library rational arithmetic.  It checks
the disjoint grade partitions and the bounded controls without importing the
primary verifier or SymPy.  The programs replay the finite four-root
identities; they do not prove Universal Supply on the witness locus.
