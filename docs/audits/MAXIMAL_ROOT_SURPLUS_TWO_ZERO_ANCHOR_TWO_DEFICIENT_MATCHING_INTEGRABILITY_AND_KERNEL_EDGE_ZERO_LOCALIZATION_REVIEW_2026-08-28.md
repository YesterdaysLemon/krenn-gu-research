# Hostile review: two-deficient matching integrability and kernel-edge-zero localization

## Review target and verdict

Target reviewed:

`claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TWO_DEFICIENT_MATCHING_INTEGRABILITY_AND_KERNEL_EDGE_ZERO_LOCALIZATION_THEOREM.md`

Supporting artifacts reviewed:

`claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_two_deficient_matching_integrability_and_kernel_edge_zero_localization.py`

`claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_two_deficient_matching_integrability_and_kernel_edge_zero_localization.py`

**Verdict: PASS for the exact `GLS64` scope after two notation repairs.**
The proof correctly forces the raw deficient--deficient edge to vanish on
the common kernel in every `GLS63` exactly-two-deficient residual.  It covers
both three and four `c`-zero cross products.  It does not exclude the
resulting zero-edge divisor.

The review required the theorem to identify the nonzero scalar `H` explicitly
with the `GLS63` `S={n,m}` complementary deck, and to write the two generic
kernel vectors as separately chosen scalar multiples rather than call those
collinear vectors independent.  Both repairs are present in the reviewed
version.

This is an exact same-source localization, not a complete source-
integrability theorem, attachment, synchronization theorem, or global
resolution.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Exact upstream scope

The proof starts only after the full `GLS63` localization:

```text
K_n=K_m=K e_c,
rank J_n=rank J_m=2,
P=empty,
U={0,1,2,3} consists of injective nonaxis labels,
Z=E_c has size 3 or 4,
E_d=E_e=empty,
the S={n,m} contraction is nonzero binary diagonal.    (1)
```

The hypotheses `P=empty`, exactly two deficient labels, and `|Z|>=3` are all
load-bearing.  Nothing in the proof extends them silently to a three-plus-
deficient profile or an arbitrary lower-rank port.

All evaluated edges come from one physical table.  With the notation in the
theorem,

```text
eta=W_nm(x_n,x_m),
A_i=W_ni(x_n,k_i),
B_i=W_mi(x_m,k_i),
w_ij=W_ij(k_i,k_j),
delta_ij=eta w_ij+A_iB_j+B_iA_j.                     (2)
```

No `delta`, cofactor, or deck is introduced as an independently selectable
tensor.

## Companion nonvanishing

The rank-two/nonaxis companion lemma covers every companion divided out by
coefficient comparison in the proof.  A nonaxis injective label has both
probe blocks nonzero.  If one block at the rank-at-least-two label vanished,
the remaining decomposable tensor in the companion could not vanish.  If
all four blocks are nonzero, zero companion would make the two probe-block
images at the first label lie on one common line, contradicting joint rank
at least two.

The finite-union choice of probe vectors is valid over the infinite
characteristic-zero coefficient field.  The lemma uses no determinant open,
edge division, or deck nonvanishing assumption.  It applies to every
`g_st` with `s,t in U` and to `g_mu,g_nu` because `J_m,J_n` have rank two.

## Six pair equations

For each pair `{i,j} subset U`, take in the `GLS63` hierarchy

```text
R={n,m},       C={i,j},       S=U-{i,j}={s,t}.        (3)
```

The only structurally retained pair is `{s,t}`.  Its actual complementary
deck on `{n,m,i,j}` has exactly the three matchings in (2), hence the source
is `g_st delta_ij`.

Every two-subset of a four-set meets a fixed subset of size at least three.
Thus `{i,j}` contains a `c`-zero cross product.  The two deficient kernel
vectors kill target colours `d,e`, and that cross product kills `c`; the
target is zero.  Companion nonvanishing therefore gives all six equations

```text
delta_ij=0.                                           (4)
```

This is a same-source consequence of the hierarchy, not pairwise
polarization applied to independently chosen restrictions.

## Eight one-kernel cofactor equations

For each `u in U`, take

```text
R={n},       C=U-{u},       S={m,u}.                  (5)
```

The sole source pair is `{m,u}`.  Its deck is the physical matching scalar
on `{n} union (U-{u})`:

```text
C_u^A=sum_(i in U-{u}) A_i w_((U-{u})-{i}).           (6)
```

The contracted three-set `U-{u}` meets `Z`; together with the `n` kernel it
kills all three target colours.  Hence `g_mu C_u^A=0`, and companion
nonvanishing gives `C_u^A=0`.  Exchanging `n,m` gives the four equations
`C_u^B=0`.

The proof correctly distinguishes these one-kernel equations from the pair
equations.  They do not follow from (4) alone.

## Complementary-edge identity and the nonzero bridge

The displayed algebra is exact:

```text
sum_({i,j} subset U) w_ij delta_(U-{i,j})
 =2 eta H+sum_(u in U) B_u C_u^A,                    (7)

H=w_01 w_23+w_02 w_13+w_03 w_12.
```

In the cofactor sum, the coefficient of `w_ij` is the cross term on the
complementary edge.  Substitution from (2) leaves six products
`eta w_ij w_kl`; the three perfect matchings are each counted twice.  The
factor two and all complement labels are correct.  The `A/B`-exchanged
identity is a valid redundant mate.

Equations (4) and (6) turn (7) into `2 eta H=0`.  The nonzero bridge is not a
new assumption: for the `GLS63` member `R=empty`, `C=U`, `S={n,m}`, the
scalar called `h_nm` there is precisely `H_U(k_U)=H`.  Its binary target has
two nonzero coefficients, so `H!=0`.  Characteristic zero then forces
`eta=0`.

Writing `x_n=alpha_n e_c` and `x_m=alpha_m e_c` with
`alpha_n alpha_m!=0` gives exactly

```text
W_nm(e_c,e_c)=0.                                     (8)
```

No localization at `eta`, `H`, or a companion occurs in the polynomial
identity itself.

## Retained boundary

The theorem correctly stops at (8).  Its scalar equations allow, for
example,

```text
eta=0,       A_i=1,       B_i=0,
w_01=w_23=1,       w_03=w_12=-1,
w_02=w_13=0.                                        (9)
```

All six `delta` values and all eight cofactors vanish, while `H=2`.  This is
not a physical GHZ witness, but it proves the new scalar identity alone
cannot remove the zero-edge divisor.

On that divisor the effective port edges are
`a_i tensor b_j+b_i tensor a_j`.  Excluding their full common-source
permanent-type tensor together with the nonzero raw deck, or legally
transporting it to a receiver, remains an explicit open obligation.  Fixed-
frame rank failures and fibre-level cancellation tables are evidence or
controls, not a coordinate-free proof of this remaining step.

## Replay evidence

The following commands were rerun in the isolated working tree:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_two_deficient_matching_integrability_and_kernel_edge_zero_localization.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_two_deficient_matching_integrability_and_kernel_edge_zero_localization.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_two_deficient_matching_integrability_and_kernel_edge_zero_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_two_deficient_matching_integrability_and_kernel_edge_zero_localization.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_two_deficient_matching_integrability_and_kernel_edge_zero_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_two_deficient_matching_integrability_and_kernel_edge_zero_localization.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_two_deficient_matching_integrability_and_kernel_edge_zero_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_two_deficient_matching_integrability_and_kernel_edge_zero_localization.py
```

The primary exact replay reported six complementary-edge terms, three
perfect matchings with multiplicity two, five zero-coordinate patterns,
thirty pair-incidence checks, twenty one-kernel-incidence checks, both
symbolic residuals zero, and the retained scalar boundary with `H=2`.

The independent standard-library replay reconstructed fifteen labelled
polynomial monomials and agreed exactly on both complementary-edge
identities.  Static compilation and Ruff checks passed.  The programs audit
the displayed finite algebra and incidence cover only; the physical
same-source bridge and companion lemma remain the written proof.

Final review status: **PASS for `GLS64`; `eta=0` residual open; global
Krenn--Gu conjecture UNRESOLVED.**
