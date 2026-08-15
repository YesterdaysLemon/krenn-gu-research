# Hostile review of fixed-pair same-mode common/noncommon exclusion

## Verdict and exact scope

**PASS, for the stated fixed-pair, pointwise, characteristic-zero,
same-mode common/noncommon scope.**  No ambient-kernel, rank-nullity,
orientation, predecessor, field, quantifier, implementation, or scope blocker
survived hostile review.

For any exact fixed-pair `Delta_3` extension, if a remaining local plane
contains the common ambient kernel line

```text
N=K(x_2+x_3),
```

then its intersections with both projection kernels equal `N`.  Therefore
none of the four family-oriented pairs

```text
(N,A_1), (N,C_1), (A_0,N), (C_0,N)
```

can occur in one mode.  This conclusion depends essentially on the frozen
kernel-support theorem's target-dependent rank floor.  It is not true for an
arbitrary three-plane with no target equations imposed.

The proportional `N/N` incidence is compatible with the rank-nullity
argument and remains open.  The package supplies no existence result for
that incidence, makes no new distinct-mode claim, and does not prove
unrestricted `P_6 -> Delta_3` nonrestriction.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_SAME_MODE_COMMON_NONCOMMON_EXCLUSION_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_same_mode_common_noncommon_exclusion.py
  audit_arbitrary_permanent_fixed_pair_same_mode_common_noncommon_exclusion.py
```

Load-bearing frozen predecessor:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_kernel_support_boundary.py
  audit_arbitrary_permanent_fixed_pair_kernel_support_boundary.py
```

The finite exceptional-line context was checked against the frozen
exceptional-kernel necessity theorem, and the complementary noncommon pair
cases were checked against the separately reviewed sibling theorem.  Neither
is silently substituted for the rank-floor predecessor.

## 1. Independent ambient-kernel derivation

The two projection maps are

```text
Phi_1(v)=(x_1,x_4,x_5,x_3-x_2-x_0),
Phi_2(v)=(x_0,x_4,x_5,x_3-x_2-x_1).
```

Solving their coordinate equations independently gives

```text
ker Phi_1={(a,0,b,a+b,0,0):a,b in K},
ker Phi_2={(0,c,b,c+b,0,0):c,b in K}.
```

Each kernel has dimension two.  A vector killed by both maps satisfies

```text
x_0=x_1=x_4=x_5=0,                x_3=x_2,
```

and hence

```text
ker Phi_1 intersect ker Phi_2
 =K(0,0,1,1,0,0)=N.
```

The five common-kernel equations have rank five over `K`, so no additional
common direction has been discarded.  This calculation uses no target
equation and no classification theorem.

Direct substitution also confirms

```text
A_0=K(1,0,0,1,0,0),      C_0=K(1,0,-1,0,0,0) subset ker Phi_1,
A_1=K(0,1,0,1,0,0),      C_1=K(0,1,-1,0,0,0) subset ker Phi_2.
```

Each of these four lines is independent of `N` in characteristic zero.
Indeed, the independence already holds over every field because the
noncommon generator has a nonzero `x_0` or `x_1` coordinate while `N` does
not.

## 2. The exact target-dependent rank floor

For a remaining mode `t`, the local space `L_t` has dimension three.  The
frozen kernel-support boundary theorem proves, under the full fixed-pair
target equations,

```text
rank(Phi_k|L_t)>=2,                   k=1,2.
```

Rank-nullity therefore gives

```text
dim ker(Phi_k|L_t)<=1.
```

Because restriction does not change which vectors are killed,

```text
ker(Phi_k|L_t)=L_t intersect ker Phi_k.
```

This identification is exact; it does not assume that `L_t` is transverse
to the ambient kernel.  The predecessor proves the floor for every remaining
mode, not merely for a minimizing mode or a generic local plane.

If `N subset L_t`, then the ambient intersection calculation puts the same
nonzero line inside both restricted kernels.  Their dimensions are at most
one, so

```text
L_t intersect ker Phi_1=N=L_t intersect ker Phi_2.
```

Both restricted ranks are consequently exactly two.  This is the complete
logical bridge; no contraction with two vectors from the shared mode is
needed.

## 3. All four oriented exclusions

The pair notation is family-oriented: the first entry is the `Phi_1` kernel
line and the second is the `Phi_2` kernel line.

For `(N,A_1)` or `(N,C_1)`, the local plane contains `N` and the indicated
noncommon line.  Both independent lines lie in `ker Phi_2`, so

```text
dim(L_t intersect ker Phi_2)>=2,
rank(Phi_2|L_t)<=1,
```

contradicting the predecessor floor.

For `(A_0,N)` or `(C_0,N)`, both independent lines lie in `ker Phi_1`.
Thus

```text
dim(L_t intersect ker Phi_1)>=2,
rank(Phi_1|L_t)<=1,
```

and the same contradiction follows.

These four cases exhaust the configurations with exactly one family kernel
equal to `N` and the other equal to a noncommon exceptional line.  No
unmentioned symmetry is required: the two `Phi_2` orientations and the two
`Phi_1` orientations were checked separately.

## 4. Why `N/N` remains open

If both family kernels are `N`, the local plane contains only one independent
killed direction for each projection.  Rank-nullity then permits

```text
rank(Phi_1|L_t)=rank(Phi_2|L_t)=2.
```

The primary verifier constructs a sample three-plane containing `N` on
which both restricted maps have rank two.  This sample checks only that the
linear-algebra boundary is sharp.  It is not asserted to extend the fixed
pair to the exact `Delta_3` target and is not evidence that the `N/N`
incidence is realizable.

Accordingly, the theorem proves the rigidity implication

```text
N subset L_t => both restricted kernels equal N,
```

but neither excludes nor constructs an exact target satisfying that
implication.  The `N/N` same-mode branch remains a genuine residual.

## 5. Dependency and quantifier audit

The new linear-algebra step itself is characteristic-free, but the claimed
pointwise theorem is stated over characteristic zero because its rank floor
comes from the characteristic-zero kernel-support package.  That predecessor
uses the full fixed-pair target, including `lambda_c!=0`, and an infinite-field
finite-union argument.  The present note correctly retains all of those
assumptions rather than promoting the conclusion to arbitrary local planes or
fields.

The exceptional-kernel theorem localizes arbitrary low directions to
`N,A_0,C_0` and `N,A_1,C_1`; it is contextual rather than the source of the
rank floor.  The sibling same-mode noncommon theorem excludes the four cases
in which neither family kernel is `N`; it does not prove the common-line
rigidity reviewed here.  Combining those packages leaves precisely the
same-mode `N/N` branch, but says nothing by itself about the distinct-mode
incidence residual.

No double contraction, numerical experiment, genericity assumption,
algebraic closure, order, positivity, or division is used in the new proof.

## 6. Computational replay and independence

Focused replay passed:

```text
new primary exact verifier:                         PASS;
new independent no-import audit:                    PASS;
kernel-support predecessor primary and audit:       PASS;
exceptional-kernel context primary and audit:       PASS;
noncommon sibling primary and audit:                PASS;
py_compile on new and predecessor scripts:          PASS;
Ruff on new and predecessor scripts:                PASS;
tracked and untracked whitespace checks:             PASS.
```

The primary verifier uses SymPy to reconstruct the two projection matrices,
their two-dimensional kernels and one-dimensional common kernel.  It checks
all four oriented pairs and exhibits the forced restricted-rank ceiling of
one.  It separately exhibits a three-plane containing `N` with restricted
rank two in both families, explicitly reporting `N/N` as open.

The independent audit imports neither the primary module nor SymPy.  It
rebuilds the maps as coordinate functions, verifies the five independent
intersection equations by exact rational row reduction, checks all four
oriented pairs, and distinguishes the rank-one pair span in the proportional
`N/N` case from the rank-two spans in every forbidden case.  The executables
replay finite linear algebra; the written proof plus the frozen rank-floor
predecessor proves the theorem.

## 7. Accepted boundary

```text
same mode, N x A_1 or N x C_1:                         EXCLUDED;
same mode, A_0 x N or C_0 x N:                         EXCLUDED;
same mode, N x N:                                      OPEN;
same mode, two noncommon lines:       EXCLUDED BY SIBLING THEOREM;
distinct-mode exceptional incidences:              NOT RECLASSIFIED;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```

## Final reviewed hashes

```text
new theorem:
05F1655F238025804309A8A0071BA0B53FE4BB5A250DE76DD5ABF15438FAF990

new primary verifier:
33EB2C3508124E876EA1EC01A574CDCA58EC84BF135362CDB57A24B1804C1ED2

new independent audit:
DDAE4AE02DCC21343DC4BAB8A37F2FAC4C5437FFE98DD4388DF5CA62E8D47208

kernel-support predecessor theorem:
7AEC9CD00DEBAC1D5CFA91D44E5D3634BD6D05FF8CA755BA1C2E83D1F8C3C45B

kernel-support predecessor primary verifier:
2B5FC62CA56FA06E5CF06AAC12679CB1051CD7336E1F4B473ECB86AED48AF53C

kernel-support predecessor independent audit:
038EDA376B773687523FA0885157907725FD38EB5D63AA83BCFD0095090C6F68

same-mode noncommon sibling theorem:
BC8851D171C140163259385135B81F9A52567B57D36912C682CD181061966B68

exceptional-kernel context theorem:
2FAB590264EDE5999F55540F2234BE2055637386B978D77469F592F58B004B60
```
