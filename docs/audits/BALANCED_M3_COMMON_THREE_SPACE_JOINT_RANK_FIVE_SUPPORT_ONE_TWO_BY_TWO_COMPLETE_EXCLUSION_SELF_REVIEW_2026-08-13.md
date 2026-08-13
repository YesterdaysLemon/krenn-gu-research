# Hostile review: support-one `(2,2)` complete exclusion

## Claim under review

The proposed theorem excludes only the transverse two-root,
joint-rank-five support-one profile in which both involved rows have rank
two.  Combined with S2AL, it closes that transverse two-root rank-five
branch.  It does not exclude any three-root Hilbert--Burch coordinate atlas,
joint rank at most four, another physical component, another pole stratum, a
higher order, or the global conjecture.

Global status remains **UNRESOLVED**.

## Adversarial questions

### 1. Are the two involved kernels known to be target-coordinate lines?

Yes.  This is the target-kernel conclusion already used in S2AI and in the
mixed profiles of S2AL.  A rank-two involved row has kernel
`span(e_c^*)`; target consistency simultaneously fixes the corresponding
root--root block row to a nonzero multiple of `e_c`.  The new theorem invokes
that proved conclusion separately on the two involved shores and does not
derive coordinate kernels from filenames or support heuristics.

### 2. Why is there a unique correction vector for every nonroot
coefficient?

S2AG gives `U=D_(B,C)(P)` and proves that the derivative restriction to the
relation three-plane `P` is injective.  Hence every coefficient of
`G_N-J` in the nonroot tensor factors has one and only one preimage in `P`.
The proof extends `T_0,T_1,T_2` to a full coefficient basis before comparing
rows, so no other coefficient can leak into a target line.

### 3. Does a zero involved row really remove the other singleton block?

Yes.  On the complete row with second coordinate `d`, `p_d=0` kills the
all-cross permanent.  Every vector `(a_E,b_E) in P` has `(b_E)_d=0`, so the
`C tensor b_E` singleton term also vanishes.  The sole remaining row is
`B_(d,-)=kappa e_d`, which determines the entire first projection `a_E`.
The first-coordinate zero row is symmetric and determines `b_E`.

### 4. Could the two missing colours coincide?

No.  If `c=d`, the second-root zero row forces the `T_d` correction to have
first projection `-e_d/kappa`.  But every first projection of `P` lies in
`e_c^perp=e_d^perp`.  This is an immediate coefficient contradiction; no
genericity or block invertibility is used.

### 5. Is the correction table complete or merely a selected slice?

It is complete.  The two zero-row equations are written for an arbitrary
coefficient tensor `E`.  Once `c!=d`, they give exactly
`w_(T_d)=(-e_d/kappa,0)`,
`w_(T_c)=(0,-e_c/kappa')`, and `w_E=0` for every other basis coefficient.
Reassembling those coefficients yields the full tensor identity (11), not a
projection of it.

### 6. Why is the relation-plane normal form exhaustive?

The two nonzero correction vectors put `(e_d,0)` and `(0,e_c)` in `P`.
The first and second projections of `P` both have rank two.  They lie in
`e_c^perp=span(e_d,e_j)` and
`e_d^perp=span(e_c,e_j)`, respectively.  Subtracting the two known vectors
from a third basis vector leaves `(alpha e_j,beta e_j)`.  Both projection
ranks force `alpha beta!=0`; rescaling gives `(e_j,tau e_j)` with
`tau!=0`.  There is no second chart.

### 7. Why must the support-one colour be one of the involved missing
colours?

After relabelling, `q_2=0`.  If `2` were neither `c` nor `d`, the complete
zero-row table would give `w_(T_2)=0`.  The all-cross coefficient at root row
`(2,2,2)` is also zero, so the nonzero target `T_2` would have no source.
Thus `2 in {c,d}`.  Exchanging the two involved roots swaps `c,d`, so taking
`d=2` loses no case.

### 8. Is the row normal form using the correct dual orientation?

Yes.  Evaluate each root coordinate covector on the ordered basis
`(e_d,0),(0,e_c),(e_j,tau e_j)` of `P`.  The first-shore coefficient rows
are `v_d,0,v_j`; the second-shore rows are `0,v_c,tau v_j`.  Both scripts
reconstruct these evaluations for every ordered distinct pair `(c,d)`.

### 9. Does the complete target table discard unrestricted entries of
`B` or `C`?

No.  Formula (20) retains arbitrary `B_(b,k)` and `C_(a,k)`.  Only the two
rows fixed by the target-kernel theorem are specialized.  The four root
pairs used in (21) explicitly retain the entries
`B_(j,k),B_(c,k),C_(j,k),C_(d,k)`.  The argument uses only that their images
lie in `span(T_d,T_c)`.

### 10. Is the untouched square really nonzero and rank one on `Q`?

Yes.  Since `d=2`, the third colour `j` is zero or one.  The kernel relation
`q_2=0` and `rank theta=2` make `q_0,q_1` a basis of `Q`.  Equation (21)
maps `q_j` to the nonzero tensor `T_j/tau` and every `q_k` into the same
line.  Hence the restricted square has rank exactly one.

### 11. Does the inherited common-zero lemma apply after relabelling?

Yes.  S2AK's lemma assumes a three-plane `V`, a two-plane `Q` with
`V intersect Q=0`, a rank-one square onto one decomposable target, and three
mixed maps into the plane spanned by two targets fully transverse to the
square target.  S2AG supplies the dimension and intersection statements;
equations (21)--(23) supply the four maps; and the three colour-diagonal
targets are pairwise fully transverse.  Renaming `(d,c,j)` as `(0,1,2)`
changes no hypothesis.  The lemma's two-source and three-source atlas is
exact in characteristic zero.

### 12. Why does a zero alternating tensor contradict the physical sensor?

The three displayed relation vectors form a basis of `P`, and the derivative
is injective on `P`.  In that basis the determinant of the three separately
linear singleton columns is the alternating separated tensor
`Alt_XYZ(v_d,v_c,v_j)`, multiplied by the nonzero basis determinant and by
the nonzero scalar `tau`.  The full function-field sensor hypothesis makes
this tensor nonzero, exactly as in S2AH, S2AI, and S2AK.

### 13. Is closing the transverse two-root rank-five branch a global
resolution?

No.  The closure combines support-two S2AI--S2AK with support-one S2AL and
this theorem.  The three-root `(1,2,2)`, `(1,1,2)`, and `(1,1,1)`
Hilbert--Burch coordinate atlases remain open at joint rank five.  Lower
joint ranks, other component and pole strata, and higher orders also remain
open.  No global status change is justified.

### 14. What do the scripts prove and not prove?

The primary verifier checks all ordered colour cases, exact correction and
row normal forms, support forcing, the arbitrary-symbolic-block target
table, diagonal-plane transversality, and the inherited two-/three-source
atlas.  The independent audit imports no repository module and no
third-party package; it rebuilds the correction table with `Fraction`, uses
numeric unrestricted block entries, and expands sparse polarized tensors.
Neither script replaces S2AG's arbitrary-vector localization, the
target-kernel theorem, or S2AK's written atlas exhaustion.  Those are stated
dependencies rather than silently inferred computations.

## Verdict

The proof supports the exact characteristic-zero exclusion of the
support-one `(2,2)` profile and, together with S2AL, the complete transverse
two-root joint-rank-five branch.  The Hilbert--Burch coordinate atlases,
lower joint ranks, other physical branches, higher orders, and the global
Krenn--Gu conjecture remain open.
