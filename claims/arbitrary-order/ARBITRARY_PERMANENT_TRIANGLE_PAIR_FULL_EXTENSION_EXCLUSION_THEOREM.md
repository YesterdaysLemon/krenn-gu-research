# Arbitrary permanent triangle-pair full-extension exclusion theorem

## Status

This note proves an exact characteristic-zero endpoint for the **displayed
based** Delta-admissible equality-five `(3,1)` triangle frame.  That displayed
frame has no exact extension from `P_6` to the three-colour diagonal tensor
`Delta_3`.

The proof only composes four committed, hostile-reviewed results:

1. a `Phi_2` rank-drop mode must exist;
2. every local rank is at least two, and a `Phi_2` low kernel is `N` or `X`;
3. no local mode can be low for both projection families; and
4. an `X` occurrence forces a distinct-mode `N` companion.

No new contraction identity is asserted here.  In particular, the proof does
not use the refuted shortcut that scalarizes a second contraction with a
possibly non-pure companion-mode colour vector.

This endpoint is **not** transported to every based-frame stabilizer orbit
inside the unbased `(3,1)` orbit.  Such a transport or classification remains
missing.  The unrestricted `P_6 -> Delta_3` problem and the global Krenn--Gu
conjecture therefore remain **UNRESOLVED**.

## 1. Exact displayed-frame statement

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

At the first two modes fix the ordered bases

```text
u_0=x_1-x_2,       u_1=x_3,          u_2=-x_0+x_2,
v_0=-x_1+x_2,      v_1=x_0+x_1,      v_2=x_3.                (1)
```

Put

```text
ell_1=x_2-x_1-x_0,                 ell_2=x_2-x_1,
Phi_1=(x_3,x_4,x_5,ell_1),         Phi_2=(x_0,x_4,x_5,ell_2).
                                                                  (2)
```

The two mixed and three diagonal complementary quartics are

```text
F_1=x_4x_5 x_3 ell_1,              F_2=x_4x_5 x_0 ell_2,
D_0=2x_4x_5 x_0x_3,
D_1= x_4x_5 x_2(x_0+x_1),
D_2= x_4x_5 x_1(x_0-x_2).                              (3)
```

For `t=2,3,4,5`, let the ordered independent triple
`(y_(t,0),y_(t,1),y_(t,2))` span the local plane `L_t subset K^6`.  An exact
extension to `Delta_3` would satisfy

```text
T_(F_1)=T_(F_2)=0,
T_(D_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (4)
```

Every `T_z` is the complete polarization of the displayed quartic `z` on the
four ordered local triples.

### Theorem 1 (displayed based `(3,1)` full-extension exclusion)

There are no four ordered independent local triples satisfying (4) over a
field of characteristic zero.  Equivalently, the displayed based frame (1)
has no exact `P_6 -> Delta_3` extension.

## 2. Frozen reviewed dependencies

The proof uses the following exact committed bytes.  SHA-256 digests are
uppercase.  The independent audit additionally pins and checks each Git blob.

### 2.1 Two-sided projection drop

```text
commit: ba39b00cc3d49309fc25e44754cb06f66eaefbdb

theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_TRIANGLE_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md
C5E8F47B499318595481D84DB75425240BA6A01AD512A92BF923F5FAB56BF485

primary verifier:
claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py
770F21C2D34A5B98CE5820D023405D0A95B3FE167539747E3EFB9EDE4A538153

independent audit:
claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py
14AB3E48905246452B9B02D962D0D5902D543398EA74B0009ACAF12C720D136D

hostile review:
docs/audits/ARBITRARY_PERMANENT_TRIANGLE_PAIR_TWO_SIDED_PROJECTION_DROP_REVIEW_2026-08-15.md
4E52015588B2DA8353B717D3704C7D2149B21B0046BD4FDD1B3664500E5A27F6
verdict: PASS.                                             (5)
```

Accepted interface used here:

```text
min_(2<=t<=5) rank(Phi_2|L_t) <= 2.                       (6)
```

### 2.2 Kernel-support boundary

```text
commit: 6e4d8ec79191a51c90dd188f7bdc2d7fde36b5f7

theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_TRIANGLE_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
60858DFE1C1C9E11C74662B815E1A4173616C3277E28A25520EDAD97148EBA82

primary verifier:
claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_kernel_support_boundary.py
67F27BEF7A3C8A071344F6B48BEA265DF2173E839586C988239F039DBB72F8DF

independent audit:
claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_kernel_support_boundary.py
B0C5DFBC8ED8086BCF5EDAA8665BD57131E2291ED73601A269F35996B973FBA8

hostile review:
docs/audits/ARBITRARY_PERMANENT_TRIANGLE_PAIR_KERNEL_SUPPORT_BOUNDARY_REVIEW_2026-08-15.md
09692AF859DB180F6D2BD5E0A51361F07BDFD33CCBC47671794A5B06FB2D1676
verdict: PASS.                                             (7)
```

Accepted interface used here, for every `k in {1,2}` and every local mode
`t`, is

```text
rank(Phi_k|L_t)>=2.                                      (8)
```

If `rank(Phi_2|L_t)=2`, its one-dimensional kernel intersection is one of

```text
N=K(x_1+x_2),          with local support in {1,2},
X=Kx_3,                with local support exactly {0}.    (9)
```

Both generators lie in the displayed ambient kernels as follows:

```text
N subset ker(Phi_1) intersect ker(Phi_2),
X subset ker(Phi_2).                                    (10)
```

### 2.3 Same-mode two-low exclusion

```text
commit: f8267fc172ac8f9bee528e3b2ae876635253823b

theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_TRIANGLE_PAIR_SAME_MODE_TWO_LOW_EXCLUSION_THEOREM.md
196A46E7B85A332956DB6CCF99BD72F1999E3B8205E774F077C552C70961A155

primary verifier:
claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py
9DDA7DB2F2059A596E242D69834078CE852E70DBB90B450E0775F040394870E5

independent audit:
claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py
4F0B502445D5330421D597CCF674B1F0227E5D14E8DADABFF26253954827BE95

hostile review:
docs/audits/ARBITRARY_PERMANENT_TRIANGLE_PAIR_SAME_MODE_TWO_LOW_EXCLUSION_REVIEW_2026-08-15.md
48D59C4408EA1F91E6B6AA436C474B903B578B41C0E23444A201510F1E08C0AC
verdict: PASS.                                            (11)
```

Accepted interface used here:

```text
There is no t with
rank(Phi_1|L_t)=rank(Phi_2|L_t)=2.                       (12)
```

In particular, the reviewed theorem includes the proportional `N/N` case.

### 2.4 Exceptional companion propagation

```text
commit: 76240ca4becc1b58b9803ac1ec6a4db159c07d3c

theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_THEOREM.md
9C70842573B3DD02BE5AC9CC65B08047AF0C6877892EA816A5D89B2024ED36A3

primary verifier:
claims/arbitrary-order/verify_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py
97177FE5D7A44821428AAED34707FAD30490D50D80163609A28FB3AE7BE663F0

independent audit:
claims/arbitrary-order/audit_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py
9DB62582D752C85F2E7AE8343EC806B95786C5693466ECFB3666C5F838A35289

hostile review:
docs/audits/ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_REVIEW_2026-08-15.md
7BDFE90C91664B8A8AF5C3B6BFC8997F274D8EB4BCBF863757CD63E81DC30300
verdict: PASS.                                            (13)
```

The triangle-row interface used here is exactly

```text
Phi_2 low X=x_3, local support {0}
  => some distinct local mode contains a nonzero vector in
     N=K(x_1+x_2), with nonempty local support in {1,2}.  (14)
```

The reviews in (5), (7), (11), and (13) audit the mathematical arguments,
their characteristic-zero and displayed-frame scopes, tensor-slot legality,
computational replay, and audit independence.  The written dependency
theorems remain the mathematical proof sources; verifier output is a separate
evidence axis.

## 3. Exhaustive `N/X` proof topology

Assume for contradiction that an extension satisfying (4) exists.  By (6),
some local mode `t` has `rank(Phi_2|L_t)<=2`.  The floor (8) makes this rank
exactly two.  Hence (9) gives exactly two possible kernel lines.

### Leaf `N`

Suppose `N subset L_t`.  By (10), the same nonzero vector lies in both ambient
kernels, so

```text
rank(Phi_1|L_t)<=2,       rank(Phi_2|L_t)=2.
```

The first inequality and (8) give `rank(Phi_1|L_t)=2`.  Thus `t` is low for
both families, contradicting the same-mode exclusion (12).

### Leaf `X`

Suppose instead `X subset L_t`.  Its support is exactly `{0}`, so the
companion theorem applies.  It supplies a distinct local mode `s!=t` and a
nonzero vector

```text
q in L_s intersect N,
```

with nonempty local support contained in `{1,2}`.  Since `N` lies in both
ambient kernels, both restricted ranks at `s` are at most two.  The floor (8)
makes both ranks exactly two, again contradicting (12).

The two leaves `N` and `X` exhaust (9), and both are impossible.  This proves
Theorem 1.  Notice that the `X` leaf uses only the reviewed occurrence-to-
companion implication (14); it performs no second contraction and does not
assume that unrelated colour vectors in the companion mode are pure `R`.

## 4. Exact boundary

```text
field:                                                   CHARACTERISTIC ZERO;
displayed based Delta-admissible (3,1) frame (1):        ASSUMED;
exact local triples and full targets (4):                ASSUMED;
Phi_2 rank-drop existence:                               REVIEWED/PINNED;
rank floor and Phi_2 N/X kernel classification:          REVIEWED/PINNED;
same-mode cross-family low exclusion:                    REVIEWED/PINNED;
X -> distinct-mode N companion:                          REVIEWED/PINNED;
exact extension of the displayed based frame (1):        EXCLUDED;

all based-frame stabilizer orbits of unbased (3,1):      NOT CLASSIFIED;
transport from (1) to every based (3,1) frame:           NOT PROVED;
unbased (3,1) orbit universally excluded:                NOT PROVED;
active-support-five/six cases:                           OPEN;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.   (15)
```

Any later PR that promotes this displayed-frame endpoint into the live
frontier must update `docs/current-frontier.md`.  This frozen local package
does not itself assert the missing based-frame transport.

## 5. Exact replay

Run

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_full_extension_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_full_extension_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_full_extension_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_full_extension_exclusion.py
```

The primary verifier checks all frozen SHA-256 dependencies, the reviewed
interfaces, the `N/X` proof topology, and the scope fence.  The independent
audit imports neither the primary verifier nor SymPy.  It checks the pinned
Git objects and blobs directly, reads the accepted dependency boundaries by
an independent route, and exhausts the same two leaves.  These scripts audit
dependency identity and proof composition; they do not replace the four
written characteristic-zero arguments.
