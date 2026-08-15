# Hostile review of the fixed-pair exceptional-kernel necessity theorem

## Verdict and scope

**PASS, for the stated fixed-pair, pointwise, characteristic-zero,
full-target scope.**  No mathematical, quantifier, rank-nullity,
one-diagonal, field-assumption, dependency, or implementation blocker survived
hostile review.

The package proves that a nonzero local kernel direction in either mixed-factor
projection family cannot have generic projective parameters

```text
a b (a+b) != 0.
```

Together with the frozen kernel-support predecessor, every rank-two local
projection therefore has its one-dimensional kernel on one of three explicit
ambient lines.  Together with the two-sided projection-drop predecessor, at
least one such exceptional incidence occurs in each projection family.

This is a necessary finite localization only.  It does not prove that any
exceptional incidence is realizable, classify simultaneous incidences, exclude
the fixed pair, or transport the conclusion to another equality-five orbit.
Unrestricted `P_6 -> Delta_3` nonrestriction remains unknown, and the global
Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_EXCEPTIONAL_KERNEL_NECESSITY_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_exceptional_kernel_necessity.py
  audit_arbitrary_permanent_fixed_pair_exceptional_kernel_necessity.py
```

Load-bearing frozen predecessor:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_kernel_support_boundary.py
  audit_arbitrary_permanent_fixed_pair_kernel_support_boundary.py
```

The final existence statement also uses the separately frozen and reviewed
two-sided projection-drop package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_two_sided_projection_drop.py
  audit_arbitrary_permanent_fixed_pair_two_sided_projection_drop.py
```

## 1. Independent derivation of the one-diagonal obstruction

Write `W=R direct-sum A`, with `dim R=4`, `dim A=2`, and let `J` be a
nondegenerate symmetric bilinear form on `A`.  For

```text
C(y,z,w)=r(y)J(a(z),a(w))
        +r(z)J(a(y),a(w))
        +r(w)J(a(y),a(z)),
```

assume that three independent local triples have every tensor entry zero
except a nonzero `(0,0,0)` entry.

Fix two modes and labels `(i,j)!=(0,0)`.  The linear map

```text
K_(i,j): W -> R,
w |-> C(y_(s,i),y_(u,j),w)
```

kills the three-dimensional third local plane.  Rank-nullity on its
six-dimensional domain gives

```text
rank K_(i,j) <= 6-3=3.
```

On the four-dimensional `R`-summand its restriction is

```text
r |-> J(a(y_(s,i)),a(y_(u,j))) r.
```

If that scalar were nonzero, this restriction alone would have rank four,
contradicting the upper bound.  Permuting the three modes proves

```text
J(a(y_(q,i)),a(y_(q',j)))=0
```

for every pair of distinct modes whenever the two labels are not both zero.
The rank argument uses only the inclusion of the third local plane in the
kernel; it does not assume that this is the whole kernel or that the map is
surjective.

The nonzero `(0,0,0)` value is a sum of three `R`-vectors weighted by the
three pairings of zero-labelled `A`-vectors.  If all three pairings vanished,
the tensor value would vanish, so at least one is nonzero.  After permuting
modes, take

```text
J(a(y_(s,0)),a(y_(u,0))) != 0.
```

For `l=1,2`, both cross pairings involving `a(y_(v,l))` vanish by the
previous paragraph.  The zero tensor entry `(0,0,l)` reduces to

```text
r(y_(v,l)) J(a(y_(s,0)),a(y_(u,0)))=0,
```

and hence `r(y_(v,l))=0`.  The same two vectors are orthogonal to the
nonzero vector `a(y_(s,0))`.  Nondegeneracy makes its orthogonal complement
in the two-space `A` one-dimensional.  Thus `y_(v,1)` and `y_(v,2)` lie in
the same line and are dependent, contradicting independence of the local
triple.

This derivation is insensitive to cancellation among the three summands of
`C`: cancellation may occur, but the proof uses only the safe implication
that a nonzero sum has at least one nonzero pairing coefficient.

## 2. Exact bridge from a generic local kernel to the lemma

Solving the four projection equations independently reproduces

```text
ker(Phi_1)={(a,0,b,a+b,0,0)},
ker(Phi_2)={(0,a,b,a+b,0,0)}.
```

After contracting the five complementary quartics with either kernel
vector and suppressing the common factor `x_4x_5`, the usable residual
covectors are the nonidentically-zero mixed channel and the three diagonal
channels.  In the coordinate basis of `R=K^{0,1,2,3}`, their determinant is

```text
8 a^2 b(a+b)
```

for both projection families.  Hence under `a b (a+b)!=0` they form a
basis of `R^*`.

The full exact target, not a shell or sampling surrogate, then determines
the `R`-valued contraction tensor on the three remaining local colour bases:

```text
C(y_(s,i),y_(u,j),y_(v,l))=0 unless i=j=l,
C(y_(s,e),y_(u,e),y_(v,e))!=0 iff alpha_e!=0.
```

The frozen kernel-support theorem proves that a generic kernel vector in
the removed local plane has exactly one nonzero local coefficient
`alpha_e`.  Relabelling this single index only inside the abstract lemma
therefore produces exactly its forbidden one-surviving-diagonal
configuration.  No genericity of the remaining three local planes, no
algebraic closure, and no unproved noncancellation assumption enters this
application.

## 3. Quantifiers and the finite exceptional set

The argument applies to every mode `t`, either projection family `k`, and
every nonzero generic vector in `L_t intersect ker(Phi_k)`.  Thus any
nonzero intersection contains no generic direction.

The predecessor already proves

```text
rank(Phi_k|L_t)>=2.
```

Since `L_t` has dimension three, its intersection with the ambient kernel
has dimension at most one.  Whenever it is nonzero it therefore has a
unique projective direction.  In the projective parameter line, the
failure of genericity is exactly

```text
a b (a+b)=0,
```

whose three nonzero projective solutions over a characteristic-zero field
are

```text
(a:b)=(0:1), (1:0), (1:-1).
```

Consequently the only possible local kernel lines are

```text
K p_k(0,1), K p_k(1,0), K p_k(1,-1).
```

The two-sided predecessor supplies at least one rank-drop mode in each
family, while the kernel-support predecessor upgrades every such drop to
rank exactly two.  Therefore each family has at least one incidence on this
finite list.  The minimizing modes may coincide, and the theorem correctly
makes no converse or realizability claim.

## 4. Field and characteristic audit

Characteristic zero is sufficient for every step.  It makes the displayed
factor `8` invertible and makes the base field infinite where the frozen
predecessor uses a finite-union argument.  The new rank proof itself needs
only finite-dimensional linear algebra and nondegeneracy of `J`.

The orthogonal-complement step is valid over an arbitrary field once `J`
is nondegenerate: pairing with a nonzero vector is a nonzero functional on
the two-space, so its kernel has dimension one.  The proof uses no square
roots, diagonalization, algebraic closure, order, positivity, or division by
a parameter that has not explicitly been assumed nonzero.

## 5. Computational replay and independence

Focused replay passed:

```text
new primary exact verifier:                    PASS;
new independent no-import audit:               PASS;
kernel-support predecessor primary:             PASS;
kernel-support predecessor independent audit:   PASS;
two-sided predecessor primary:                  PASS;
two-sided predecessor independent audit:        PASS;
py_compile on both new scripts:                 PASS;
Ruff on both new scripts:                       PASS;
tracked diff whitespace check:                  PASS.
```

The primary verifier uses SymPy to reconstruct both ambient kernels,
symbolically polarize all ten fixed-pair contractions, factor both generic
determinants, and replay the rank-four scalar-identity and orthogonal-line
steps.  Its symbolic checks support the displayed identities; the written
argument remains the proof.

The independent audit imports neither the primary verifier nor SymPy.  It
rebuilds the quartics using standard-library rational arithmetic, evaluates
the polarizations directly, uses a separate Gaussian-elimination
determinant, and exhausts the two-dimensional common-orthogonality core over
`F_3` and `F_5`.  The finite-field runs audit algebra and case geometry only;
they are not presented as the characteristic-zero proof.

Selected exact outputs were:

```text
symbolic polarized contractions checked:       10;
rational determinant parameter checks:          14;
generic nonzero determinant checks:               8;
exceptional zero determinant checks:              6;
F_3 nonzero endpoint pairs:                       48;
F_5 nonzero endpoint pairs:                      480.
```

The frozen predecessor replay also passed its 245760 direct square-free
coefficient checks, 96 projective determinant checks, `F_11`
cross-orthogonality exhaustion, and finite-union rank stress test.

## 6. Accepted boundary

```text
fixed pair, generic local kernel directions:             EXCLUDED;
fixed pair, every low kernel direction exceptional:      PROVED;
three projective candidates per projection family:       PROVED NECESSARY;
exceptional-line incidence classification/exclusion:     OPEN;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

## Final reviewed hashes

```text
new theorem:
2FAB590264EDE5999F55540F2234BE2055637386B978D77469F592F58B004B60

new primary verifier:
256D1F4DEB3639E912E41C426E2D28E5FCB384C72DCDB00F9592064D33C904E5

new independent audit:
90014EC8E37B0F48F26BD4A9528E235F2FC26D5E757948E34B1744B1B743D6F1

kernel-support predecessor theorem:
7AEC9CD00DEBAC1D5CFA91D44E5D3634BD6D05FF8CA755BA1C2E83D1F8C3C45B

kernel-support predecessor primary verifier:
2B5FC62CA56FA06E5CF06AAC12679CB1051CD7336E1F4B473ECB86AED48AF53C

kernel-support predecessor independent audit:
038EDA376B773687523FA0885157907725FD38EB5D63AA83BCFD0095090C6F68

two-sided predecessor theorem:
A383731E094E0D0E45482AAB889FB8B202FC7A2CF452D8534D5035E737089F36

two-sided predecessor primary verifier:
E170A513301ECD84A8989066A29B51B89635FD54B0CEF88DCEBBEEDBAAF641DE

two-sided predecessor independent audit:
47A30C8C09E3931526C4CFAC2E9ABE66B7FD10B4EA95336C93E12D63C360E6B2
```
