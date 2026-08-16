# Arbitrary permanent fixed-pair same-mode common/noncommon exclusion

## Status

This note closes a bookkeeping residual inside the simultaneous projection-drop
boundary for the fixed equality-five pair.  If one remaining local plane
contains the common exceptional line

```text
N=K(x_2+x_3),
```

then `N` is the unique kernel line of **both** restricted projection maps on
that plane.  Consequently `N` cannot be paired in the same mode with any of
the four noncommon exceptional lines `A_0,C_0,A_1,C_1`.

The proof is exact linear algebra.  It combines the common ambient kernel with
the already-proved rank-two floor for every restricted projection.  No double
contraction is used; indeed, no target contraction is needed after the rank
floor has been established.  The proportional `N/N` same-mode case remains
open.  This note does not exclude all simultaneous-low incidences and does not
prove unrestricted permanent nonrestriction.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## 1. Fixed pair and the rank floor

Let `K` be a field of characteristic zero.  At the fixed equality-five pair,
the two mixed-factor projections on `K^6` are

```text
Phi_1=(x_1,x_4,x_5,x_3-x_2-x_0),
Phi_2=(x_0,x_4,x_5,x_3-x_2-x_1).                       (1)
```

Let the ordered independent local triple in mode `t` span the three-space
`L_t subset K^6`.  For all four remaining modes, assume the exact fixed-pair
`Delta_3` target equations

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (2)
```

The characteristic-zero kernel-support boundary theorem
`ARBITRARY_PERMANENT_FIXED_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md` proves

```text
rank(Phi_k|L_t)>=2,                         k=1,2.       (3)
```

Since `dim L_t=3`, rank-nullity turns (3) into

```text
dim(L_t intersect ker Phi_k)<=1,            k=1,2.       (4)
```

This is the only target-dependent input used below.

## 2. The common ambient line

Solving (1) gives

```text
ker Phi_1={a x_0+b x_2+(a+b)x_3:a,b in K},
ker Phi_2={c x_1+b x_2+(c+b)x_3:c,b in K}.              (5)
```

Thus

```text
ker Phi_1 intersect ker Phi_2=K(x_2+x_3)=:N.            (6)
```

The noncommon exceptional lines from the fixed-pair exceptional-kernel
classification are

```text
A_0=K(x_0+x_3),       C_0=K(x_0-x_2)       in ker Phi_1,
A_1=K(x_1+x_3),       C_1=K(x_1-x_2)       in ker Phi_2. (7)
```

Every line in (7) is different from `N`.

## 3. Common-line rigidity

### Theorem 1 (same-mode common/noncommon exclusion)

For every remaining mode `t`,

```text
N subset L_t
  => L_t intersect ker Phi_1=L_t intersect ker Phi_2=N. (8)
```

In particular, none of the same-mode family pairs

```text
(N,A_1), (N,C_1), (A_0,N), (C_0,N)                     (9)
```

can occur as two restricted projection-kernel lines.

### Proof

Suppose `N subset L_t`.  Equation (6) puts `N` in each of

```text
L_t intersect ker Phi_1,       L_t intersect ker Phi_2. (10)
```

Both intersections are nonzero, while (4) says that each has dimension at
most one.  Hence both equal `N`, proving (8).

For example, if the `Phi_1` kernel line were `N` and the `Phi_2` kernel line
were `A_1`, then `L_t intersect ker Phi_2` would contain the independent
lines `N` and `A_1`.  Its dimension would be at least two, contradicting
(4).  The other three pairs in (9) are identical, with the family labels
interchanged where necessary.  This proves the theorem.

Equivalently, once a local plane contains the common ambient line, both
restricted maps have rank exactly two and the same one-dimensional kernel.

## 4. A useful discarded overcomplication

An initially tempting route was to choose `N` and a noncommon line as two
independent vectors in one local plane, contract the quartics legally once in
that shared slot, and classify the resulting two- or three-colour diagonal
tensor.  That route can be made into consistent exact algebra, but its first
assumption has already created a two-dimensional kernel for one of the maps
in (1).  The rank floor (3) rules it out before any residual-tensor analysis.

The correction is scientifically useful: the common line must be propagated
through the **ambient** intersection (6) before treating family labels as
independent incidence data.  It also avoids the illegal alternative of
placing two vectors from one local plane into two different tensor slots.

## 5. Exact scope and replay

```text
same mode, N x A_1 or N x C_1:                         EXCLUDED;
same mode, A_0 x N or C_0 x N:                         EXCLUDED;
same mode, N x N:                                      OPEN HERE;
same mode, two noncommon lines:       EXCLUDED BY THE SIBLING THEOREM;
distinct-mode exceptional incidences:              NOT RECLASSIFIED;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.       (11)
```

Here the sibling result is
`ARBITRARY_PERMANENT_FIXED_PAIR_SAME_MODE_NONCOMMON_EXCEPTIONAL_PAIR_EXCLUSION.md`.

Replay the exact linear algebra with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_same_mode_common_noncommon_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_same_mode_common_noncommon_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_same_mode_common_noncommon_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_same_mode_common_noncommon_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_same_mode_common_noncommon_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_same_mode_common_noncommon_exclusion.py
```

The primary verifier reconstructs the two projection matrices, their
two-dimensional kernels and one-dimensional common kernel, and all four
forbidden line pairs with exact symbolic arithmetic.  The independent audit
imports neither the primary verifier nor SymPy: it rebuilds the projections
as coordinate functions and checks the intersection, line independence, and
rank-nullity contradiction by exact rational row reduction.  The scripts
replay the displayed linear algebra.  The written argument, together with
the characteristic-zero rank-floor predecessor, proves the theorem.
