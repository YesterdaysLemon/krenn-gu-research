# Fixed-Q maximal-nuisance-rank common-contraction synchronization

## Status

**Exact characteristic-zero same-`Q` synchronization theorem and sharp
rank-drop boundary.**  Fix one graph, one residual pair `Q`, and any finite
family of full fixed-`Q` target modules.  Let the two residual contraction
vectors vary over their fully supported torus.  If each desired target class
survives all nuisance slices at one point where its nuisance matrix has
maximal rank, then all desired classes survive at one common contraction; in
fact they survive on one nonempty Zariski-open set.

For a hypothetical witness satisfying the full uncontracted mixed GHZ
equation, if each target additionally has pure quotient rank one at such a
maximal-rank point, then one common fully supported contraction has pure
quotient rank one for every target.  Applied to the four-root family this
synchronizes the six pair tensors and the four-port tensor required by
`GLD3`.  Applied to the conditional six-root family of `GLD7`, it synchronizes
the fifteen pair, fifteen four-port, and one six-port rows required by
`GLD6`.

The maximal-nuisance-rank qualification is essential.  Two exact
one-parameter module families can have nonempty but disjoint selector loci,
each supported entirely on a different nuisance-rank-drop point.

This theorem does not prove that any individual maximal-rank survival point
exists on the hypothetical-witness locus.  It synchronizes contractions,
not graphs, residual pairs, selector functionals, activity conditions, or
permanent restrictions.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

The module criterion used here is
[`GLD5`](FOUR_ROOT_CONSTANT_TARGET_MODULE_SELECTOR_QUOTIENT_AND_MAXIMUM_ROOT_SHARPNESS_THEOREM.md),
and the pure-rank application is
[`GLD7`](FIXED_Q_FULL_MODULE_TARGET_QUOTIENT_RANK_ONE_PURE_SURVIVAL_AND_SIX_PORT_ATTACHMENT_TRICHOTOMY_THEOREM.md).

## 1. Polynomial full-module family

Let `K` be an infinite field of characteristic zero and let

```text
T=(G_m)^m                                                   (1)
```

be the fully supported residual-contraction torus.  Its coordinate ring
`K[T]=K[z_1^{+-1},...,z_m^{+-1}]` is an integral domain, and its `K`-points are
Zariski dense.

Fix one graph and one residual pair `Q`.  Let `F` be a finite family of
desired target labels.  For each `S in F`, choose fixed bases and write the
complete nuisance coefficient slices as the columns of a matrix

```text
B_S(z),                                                     (2)
```

and write the desired companion coefficient as one column

```text
g_S(z).                                                     (3)
```

All entries are regular functions on `T`.  In the actual fixed-`Q`
companion module they are polynomial in the residual contractions; no deck
label or nuisance slice is removed.  At a point `z`,

```text
N_S(z)=im B_S(z),
[g_S(z)]!=0 in L_S^*/N_S(z)
  iff rank[B_S(z)|g_S(z)]=rank B_S(z)+1.                    (4)
```

The selector furnished by (4) may depend on the fixed graph, `Q`, and `z`.
It is constant in the open target-port coordinates and is an operator
identity on every labelled deck summand.

Put

```text
r_S=max_(z in T) rank B_S(z).                               (5)
```

## 2. Common-contraction theorem

### Theorem 1 (maximal-rank selector synchronization)

Assume that, for every `S in F`, there is a point `z_S in T(K)` such that

```text
rank B_S(z_S)=r_S,
rank[B_S(z_S)|g_S(z_S)]=r_S+1.                              (6)
```

Then there is a nonempty Zariski-open set `U subset T` such that, for every
`z in U(K)` and every `S in F`,

```text
[g_S(z)]!=0 in L_S^*/N_S(z).                               (7)
```

Consequently all targets in `F` have legal constant-open-port selectors at
one common fully supported residual contraction.

### Proof

Fix `S`.  Choose an `r_S`-minor `Delta_S` of `B_S` nonzero at `z_S`; when
`r_S=0`, take `Delta_S=1`.  Choose an `(r_S+1)`-minor `A_S` of
`[B_S|g_S]` nonzero at `z_S`.  The principal open

```text
U_S=D(Delta_S A_S) subset T                               (8)
```

is nonempty.  On `U_S`, the nuisance rank is at least `r_S` and therefore,
by maximality, exactly `r_S`.  The augmented rank is at least `r_S+1`, so
(7) holds.

The product of the finitely many nonzero Laurent polynomials
`Delta_S A_S` is nonzero because `K[T]` is an integral domain.  Hence

```text
U=intersection_(S in F) U_S                                (9)
```

is a nonempty open.  Since `K` is infinite, the `K`-points of `T` are dense,
so `U(K)` is nonempty.  Every point of `U(K)` is the required common
contraction. `square`

### Corollary 1.1 (seven and thirty-one targets)

For the four-root/four-port family, take

```text
F=binom(U,2) union {U},            |F|=7.                   (10)
```

Theorem 1 synchronizes the seven legal selector identities on one graph, one
`Q`, and one contraction.  If the graph/deck satisfies the full target
equation, applying those selectors supplies the exact six `D_uv` tensors and
`T`.

For the conditional six-root/six-port family of `GLD7`, take all

```text
|S|=2,4,6,                         |F|=15+15+1=31.          (11)
```

Theorem 1 synchronizes the thirty-one legal selector identities.  If the
graph/deck satisfies the full target equation, applying them supplies the
attached `z_2,z_4,z_6` row package required by `GLD6`.  In both cases
existence of the separate points (6) remains a hypothesis.

## 3. Witness pure-rank synchronization

Now fix one physical deck `H` whose full uncontracted equation equals the
GHZ target.  Every contraction `z in T` then satisfies the contracted target
equation.  Let

```text
P_S(H;z)                                               (12)
```

be the desired physical response tensor.  It is polynomial in `z`.

### Theorem 2 (common pure-rank-one contraction)

Suppose that for every `S in F` there is a point `z_S in T(K)` where

```text
rank B_S(z_S)=r_S,
q_S(z_S)=1.                                               (13)
```

Here `q_S` is the active pure quotient rank of `GLD7`.  Then a nonempty
Zariski-open set of common contractions satisfies

```text
q_S(z)=1,
[g_S(z)]!=0,
P_S(H;z)!=0                                               (14)
```

for every `S in F` simultaneously.

### Proof

At `z_S`, `GLD7` gives both `[g_S(z_S)]!=0` and
`P_S(H;z_S)!=0`.  Apply Theorem 1 and choose one fixed tensor coordinate
`rho_S(z)` of `P_S(H;z)` which is nonzero at `z_S`.  Shrink `U_S` further by
the principal open `D(rho_S)`.  The finite intersection remains nonempty.

At a common point, `[g_S]!=0` and `P_S(H)!=0`.  The contraction is fully
supported, so every pure colour is active.  The converse direction of the
`GLD7` pure-survival theorem then makes at least one pure class survive,
while its quotient-rank theorem bounds the span by one.  Thus `q_S=1` for
every `S`. `square`

The response factor in Theorem 2 is load-bearing.  If `P_S(H;z)=0`, the
contracted target equation permits pure quotient rank zero even when
`[g_S(z)]!=0`.

## 4. Sharp rank-drop control

The maximal-rank assumption cannot be replaced by arbitrary pointwise
survival.  On `T=G_m`, take two one-dimensional target modules

```text
B_1(t)=[t-1],       B_2(t)=[t-2],
g_1(t)=g_2(t)=[1].                                      (15)
```

Both nuisance matrices have maximal rank one.  The first desired class
survives exactly at `t=1`, where `B_1` has rank zero.  The second survives
exactly at `t=2`, where `B_2` has rank zero.  Their selector loci are
nonempty but disjoint.

This is a formal module control, not a physical graph or hypothetical
witness.  It proves that an application must either find survival on the
maximal nuisance-rank stratum or separately control the exceptional
rank-drop contraction loci.

## 5. Frontier and UNKNOWN remainder

```text
maximal-rank individual survival gives open survival:      PROVED;
finite same-Q selector conditions share one contraction:   PROVED;
seven/31 pure-rank-one points synchronize on a witness:     PROVED CONDITIONAL;
arbitrary individual survival conditions synchronize:      FALSE;
one maximal-rank survival point for every witness target:   UNKNOWN;
rank-drop-only survival loci excluded on witnesses:         UNKNOWN;
three-colour GLD3 activity after synchronization:           UNKNOWN;
coefficient-pure mixed detector:                            UNKNOWN;
weighted permanent attachment:                             UNKNOWN;
global Krenn--Gu conjecture:                                UNRESOLVED.
```

The breadth is one fixed graph, one `Q`, and a finite family of seven or
thirty-one full-module targets.  The depth is every labelled companion
nuisance used by those modules.  The reconstructed objects are the exact
attached physical response tensors.  There is no overlap transition: the
theorem synchronizes one contraction parameter.  Its ambiguity object is
the nuisance-rank-drop determinantal locus together with the chosen
augmented-minor and response-coordinate zero sets.  The target implication
is conditional exact attachment; the permanent implication is none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_maximal_nuisance_rank_common_contraction_synchronization.py
python -I claims/arbitrary-order/audit_fixed_q_maximal_nuisance_rank_common_contraction_synchronization.py
```

The primary verifier checks exact polynomial matrix families with seven and
thirty-one simultaneous targets and the disjoint rank-drop control.  The
independent no-import audit uses `fractions.Fraction`, direct elimination,
and independently generated families.  These bounded programs replay the
finite algebra; the principal-open proof above is load-bearing.
