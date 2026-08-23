# Hostile review: zero-anchor residual-Laurent polarization and root-deck kernel anchor

## Verdict

**Accepted at the exact stated scope.**  The raw matching expansion gives the
three residual-Laurent nonconstant equations and the constant root-deck
equation without using the transverse projector.  The canonical minor normals
are polynomial, so no rank minor, response, residual coordinate, or `p` is
inverted.  The all-port and singleton kernel contractions type-check and
isolate exactly the declared residual-absent deck class.

The rational control replays exactly.  Its first-polarized fixed-point
cancellations split into distinct residual monomials, and its constant kernel
anchor has a displayed defect.  These are scope corrections to the apparent
strength of the control, not a witness exclusion theorem.  This is `GLS33`.
The Krenn--Gu conjecture remains **UNRESOLVED**.

## Audited base and artifacts

The review was performed from

```text
origin/main = c7baaa20f3c3e47a9e7c4d5f440039e5ef9265c8
```

against `GLS21`, `GLS22`, `GLS27`, `GLS31`, and `GLS32`.  The reviewed tranche
consists of

- the `GLS33` theorem document;
- its focused exact SymPy verifier;
- its independent standard-library `Fraction` audit; and
- the package-index, current-frontier, and node-DAG updates in the candidate
  tree.

## Mathematical hostile review

### 1. The raw equation, not the projector, owns the lift

Keeping both residual vectors formal and expanding the raw two-probe matching
identity is type-correct.  For a promoted pair, the two `A` slots give the
four `K^ij` tensors.  A one-`Q` label retains both terms

```text
xi_0^s tensor W_(a_1,u)+W_(a_0,u) tensor xi_1^s.
```

The minor normal kills the corresponding shore covectors, leaving the stated
`10` or `01` singleton factor and no `11` term.  The `D=Q` label is constant
because `q` belongs to the product of the two shore spans.  The top label
vanishes only under the explicit zero-anchor hypothesis.

Thus equations (8)--(10) do not require defining `P_Q` over an uncontracted
residual slot and do not cancel `p`.  An earlier possible retained-one-`Q`
projector formulation was rejected as needlessly type-fragile.

### 2. Polynomial normals retain, but do not solve, rank drops

The signed `2 x 2` minors of the two shore columns give vectors `N_i` with

```text
xi_i^0(N_i)=xi_i^1(N_i)=0.
```

Each normal has residual bidegree `(1,1)`.  It agrees projectively with the
usual normal on the rank-two open and becomes zero on shore-rank drops.  Hence
the identities extend polynomially across every rank and `p` divisor, but can
be silent there.  The theorem correctly distinguishes algebraic retention
from pointwise exclusion.

Counting residual degrees gives `(2,2)` for each first-polarized equation and
`(3,3)` for the product-normal equation.  These degrees include the physical
response or one-`Q` deck factors; treating the normal alone as the full degree
would be a type error.

### 3. The constant coefficient is exactly the root deck

At the base point `(s_0,s_1)`, a promoted pair gives `K_D^00`, a one-`Q` label
gives `lambda_0^s b_u+lambda_1^s a_u`, `D=Q` gives `pH_Uhat`, and the top term
is zero.  This proves the displayed constant equation label by label.

For `z_v in ker a_v intersect ker b_v`, every promoted-pair tensor has a
killed endpoint and every one-`Q` tensor is killed at its labelled port.  With
one free port, only that port's two labelled one-`Q` terms remain.  Therefore
the all-port and singleton contractions are exact and divide by nothing.

Modulo `span{a_u,b_u}`, the singleton formula identifies the pure diagonal
with `p[H_Uhat]`.  It does not show that this class is nonzero, survives a
complete downstream nuisance, or has a synchronized physical response.

### 4. Exact control boundary

The `GLS32` control has constant shore spaces
`span{e_1,e_2}`, so `e_0` is a valid denominator-free normal throughout the
residual family.  Independent exact collection gives

```text
profile 00: 200 residual-colour/port failures;
profile 10:  76, supported 38+38 on (0,1) and (2,0);
profile 01:  76, supported 38+38 on (0,2) and (1,0);
profile 11:   0.
```

At promoted word `0001`, the two first-polarized defects are exactly

```text
1/4(z_00 z_11-z_02 z_10),
1/4(z_00 z_12-z_01 z_10).
```

Both vanish when all residual coordinates equal one, explaining the merged
fixed-contraction certificate without deleting either residual label.  The
constant profile still has `41` failures at that contraction.

The declared all-port kernel vectors `e_1` kill every `a_u,b_u` row.  Exact
matching gives `pH_Uhat(e_1^4)=2`, while the pure diagonal side is one.  This
one-line defect independently detects the missing constant equation.

### 5. Source and downstream scope

The theorem supplies equations on a fixed physical `Q,A` package.  It does
not prove that an eligible package exists in every arbitrary-root source
branch, and it does not convert a contracted `H_Uhat` class into any named
downstream detector.  The two-active divisor and other shore normal forms are
not classified by the control calculation.

## Independence review

The primary uses SymPy, imports the reviewed `GLS32` graph helper, and collects
the full residual-colour coefficient tables from direct perfect matchings.
The independent audit imports neither the primary, `GLS32`, nor SymPy.  It
rebuilds every edge with standard-library `Fraction`, uses a separate matching
recursion and direct coefficient dictionaries, and independently checks the
kernel contraction.

The primary reproduces the formal shore covectors and their canonical
cross-product normals.  Both routes reproduce the residual supports,
displayed defect polynomials, `200/76/76/0` coefficient counts, `41/0/0/0`
all-ones counts, and the constant-kernel values `2` versus `1`.  The
arbitrary-root and all-divisor scopes rest on the written polynomial matching
proof, not the finite graph.

## Rejected stronger claims

The following are not licensed:

- one fixed residual contraction represents the Laurent family;
- polynomial retention excludes a rank-drop fibre where `N_i=0`;
- the normal equation alone detects the `GLS32` control;
- the constant kernel identity forces nonzero anchor survival;
- `H_Uhat` automatically meets a downstream target-purity or nuisance gate;
- the one-active or two-active divisor is excluded;
- an `r=3` calculation proves arbitrary-root source coverage; or
- the strategic node or global conjecture is closed.

## Remaining load-bearing obligation

Couple the coefficientwise residual identities and the constant anchor
quotient to the exact one-/two-active divisor profiles.  On every residual,
response, shore-rank, and selector-rank fibre, force a complete-`GLS23`
separator with nonzero response, synchronization, activity, nuisance
survival, and every named downstream anchor gate, or contradict the original
mixed coefficient deck.  Other shore types and arbitrary-root source coverage
remain separate.
