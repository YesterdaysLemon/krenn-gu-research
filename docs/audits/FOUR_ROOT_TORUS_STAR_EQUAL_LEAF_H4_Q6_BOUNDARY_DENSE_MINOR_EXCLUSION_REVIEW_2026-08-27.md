# GLD92 hostile review: H4 Q6-boundary dense minor exclusion

## Disposition

**Accepted as an exact, narrowly scoped boundary theorem.** The package is
correct only on the three-parameter family `F88` already supplied by GLD88.
It excludes the union of two principal opens on `F88 intersect V(Q6)` and leaves the
finite common-minor residual and the rest of the H4 Q6 boundary open. It does
not prove that arbitrary points of `H4 intersect V(Q6)` lie in `F88`, and it does not
change the global status: Krenn--Gu remains **UNRESOLVED**.

The reviewed conclusion is

```text
B intersect V(I_7(A)) intersect F88 intersect V(Q6) intersect D(Omega Delta)
  intersect (D(F28) union D(F31)) = empty,
```

where `Delta=(p-q)(p+q-1)P L1 L2 e`. The union is intentional: the claim
needs at least one of the two alternative six-minors, not both.

## Exact evidence inspected

The primary verifier
`claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_boundary_dense_minor_exclusion.py`
reconstructs the fixed GLD71 `37 x 9` syndrome on the GLD88 H4 family and
checks:

1. all `111` common block-kernel identities, giving rank at most six on the
   family;
2. the exact two six-row minors with columns `(0,1,3,4,6,7)` and rows
   `(0,1,2,17,25,28)` and `(0,1,2,17,25,31)`;
3. the common denominator `P^2 e^2` and the factor shapes
   `N28=(p-q)^3 F28` and
   `N31=(p+q-1)(p-q)^3 F31`;
4. the two numerator hashes, their nonzero `Q6`-division remainders, and the
   irreducibility metadata for `Q6`, `F28`, and `F31`;
5. coprimality of each Delta factor with irreducible `Q6`;
6. the exact `a`-resultant and `gcd(Res_a(F28,F31),Q6)=1`; and
7. an exact coefficient-ideal check ruling out vertical `a`-lines on
   `D(Delta)`.

The independent audit
`claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_boundary_dense_minor_exclusion.py`
imports none of the primary, GLD71 builder, or GLD88 family builder. It
directly evaluates the seven fixed sparse relation supports used by the two
minors, uses its own explicit family expression, and repeats the exact
determinants, divisions, resultant, and vertical-fibre calculation. The
support digest is pinned as
`9bea8532ac1a79352508e04db8eca836402a9153edb18fa45e94a012d63162f8`.

Both scripts pass on the candidate tree. The symbolic runs were bounded and
the previously timed-out full Q6 eliminations were not rerun; those timeout
outcomes are not evidence for this theorem.

## Adversarial checks

### Quantifier and family boundary

The old GLD90 pivots both contain `Q6`, so GLD90 does not force the GLD88
Schur family at a general Q6 point. GLD92 therefore states `F88` explicitly
as an assumption. Any wording that says "the H4 Q6 boundary" without the
`F88` qualifier would be an overclaim and is rejected. The theorem document
records this limitation in its first paragraph and residual table.

### Rank and center argument

The block-kernel identities supply three independent kernel vectors and hence
rank at most six. On `D(F28)` or `D(F31)`, the corresponding exact six-minor
is nonzero because `p-q`, `d0`, `P`, and `e` are units on the declared open.
Thus rank is exactly six, the three displayed kernel vectors are complete,
and every compatible center has proportional rows. The contradiction is with
the inherited `D(Omega)` condition `det(C)det(G) != 0`. No pointwise sample is
used as a generic-to-pointwise substitute.

### Factor and denominator handling

The determinant denominator is exactly `P^2 e^2`; it is not silently
cancelled on Q6. The leaf determinant retains the factor
`-3a+p+1`:

```text
det(G)=-(p-q)(-3a+p+1)L1L2/(d0 P e).
```

The factor is part of the determinant-safe `D(Omega)` gate. The coefficient
boundaries `L1,L2,e`, the affine/denominator boundaries, and any whole-zero
block issues outside the GLD88 family are not erased by this package.

### Properness and nonempty control

`Q6` is irreducible of total degree six. Both minor numerators have a nonzero
degree-three remainder on division by Q6, so neither stripped factor is a
Q6 multiple. The primary also checks that each factor of `Delta` is coprime
to Q6. Therefore the two displayed principal opens are proper dense opens
of the Q6 curve wherever the inherited Omega gate is defined.

The complement is not asserted empty. The resultant has total degree `99`
and `q`-degree `53`, with exact gcd one against Q6. To prevent a resultant
blind spot, the coefficient ideal of Q6 and all `a`-coefficients of F28/F31
has zero-dimensional base, q eliminant `q^6(q^2-q+1)^4`, and
`((p-q)P)^6` in that ideal. Any vertical common-minor fibre is therefore
outside `D(Delta)`, making
`Z_fin=V(Q6,F28,F31) intersect D(Omega Delta)` a finite residual on the declared open.
No finite point is enumerated or excluded.

### Independence

The audit is materially different at the determinant layer: it uses direct
sparse-support loops and does not import the relation or family builders.
It shares the seven fixed support records and the GLD88 rational family as
mathematical input, and it does not independently reprove the GLD75/GLD86
incidence bridge or GLD88's common-kernel lemma. Calling it a fully
independent proof would be inaccurate; the package calls it an independent
exact sparse-support replay.

## Accepted residuals and non-claims

| item | review verdict |
| --- | --- |
| `F88 intersect V(Q6) intersect D(F28)` | excluded, exact six-minor argument |
| `F88 intersect V(Q6) intersect D(F31)` | excluded, exact six-minor argument |
| `Z_fin=V(Q6,F28,F31) intersect D(Omega Delta)` | finite residual retained; not solved |
| all of `H4 intersect V(Q6)` | not covered outside `F88` |
| `L1=0`, `L2=0`, `e=0` | open |
| GLD83 Fitting pullback | not computed |
| other charts/components/gauges/source branches | open |
| global Krenn--Gu conjecture | **UNRESOLVED** |
