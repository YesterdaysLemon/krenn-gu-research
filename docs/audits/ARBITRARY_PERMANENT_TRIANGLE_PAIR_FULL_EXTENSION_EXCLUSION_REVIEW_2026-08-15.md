# Hostile review of triangle-pair full-extension exclusion

## Verdict and exact scope

**PASS, for the displayed based `(3,1)` triangle frame, pointwise,
characteristic-zero composition.**  No Git-object pin, theorem/review-byte,
field, based-frame, quartic, projection, ordered-slot, target, rank,
exceptional-line, companion-mode, branch-exhaustion, dependency-cycle,
implementation, or scope blocker survived hostile review.

The reviewed composition proves that the explicitly displayed ordered
`(3,1)` frame has no exact `P_6 -> Delta_3` extension.  It does not classify
all based-frame stabilizer orbits inside the unbased `(3,1)` orbit and does
not transport the result to every based `(3,1)` frame.  It proves no result
for the inequivalent `(4,1)` or `(4,2)` orbits, no unrestricted permanent
nonrestriction theorem, and no global Krenn--Gu resolution.  The global
status remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_TRIANGLE_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md
  verify_arbitrary_permanent_triangle_pair_full_extension_exclusion.py
  audit_arbitrary_permanent_triangle_pair_full_extension_exclusion.py
```

Frozen endpoint hashes:

```text
theorem:
02C87A0811777B0A833598D9217FBF117613F8B7089A21C0AE6D4ED6964648B9

primary verifier:
FF980524DD507C17B6209325C9C6CAB7B3AECFADFE758A3508B24824595559F1

independent audit:
5139CE6E1DAEE82FAE7B472954BC9195C8F0C002F9D8D7838A0EC77D3DBFCC42
```

## 1. Frozen Git objects and reviews

All four dependency commits resolve as commits, are ancestors of the
reviewed head, and occur in the required order:

```text
ba39b00cc3d49309fc25e44754cb06f66eaefbdb
  Prove triangle-pair two-sided projection drop

6e4d8ec79191a51c90dd188f7bdc2d7fde36b5f7
  Localize triangle-pair kernel supports

f8267fc172ac8f9bee528e3b2ae876635253823b
  Exclude triangle-pair same-mode lows

76240ca4becc1b58b9803ac1ec6a4db159c07d3c
  Propagate star-triangle exceptional companions
```

For every dependency artifact, the committed bytes, current bytes,
SHA-256 pin, and Git blob pin agree.  The exact pins are:

```text
two-sided projection drop at ba39b00:
  theorem  C5E8F47B499318595481D84DB75425240BA6A01AD512A92BF923F5FAB56BF485
           blob 7d51cee48633c7f625cfcd1a0b94530cc82fb3d6
  primary  770F21C2D34A5B98CE5820D023405D0A95B3FE167539747E3EFB9EDE4A538153
           blob 0d5e16265201ff476b2f8e80c4bc6abfac97f5ca
  audit    14AB3E48905246452B9B02D962D0D5902D543398EA74B0009ACAF12C720D136D
           blob a40cfe160f9eb6e9f90fcf4901021c18dc836844
  review   4E52015588B2DA8353B717D3704C7D2149B21B0046BD4FDD1B3664500E5A27F6
           blob fde4bbaef4be2d4f04269fa6ff27d68c04e4a44d

kernel-support boundary at 6e4d8ec:
  theorem  60858DFE1C1C9E11C74662B815E1A4173616C3277E28A25520EDAD97148EBA82
           blob 952b7e876b8670d0a85f850713d87b04d0cbf310
  primary  67F27BEF7A3C8A071344F6B48BEA265DF2173E839586C988239F039DBB72F8DF
           blob 02e574815669c64ebdb28c486291c95ee197ad28
  audit    B0C5DFBC8ED8086BCF5EDAA8665BD57131E2291ED73601A269F35996B973FBA8
           blob 54570210a36e48febf6e52ce4e2ec2cffca25f5a
  review   09692AF859DB180F6D2BD5E0A51361F07BDFD33CCBC47671794A5B06FB2D1676
           blob 591a356909b3a412f5dee63f8a3913336d75f74b

same-mode exclusion at f8267fc:
  theorem  196A46E7B85A332956DB6CCF99BD72F1999E3B8205E774F077C552C70961A155
           blob f99ca79a211b5ec241dfc5c460131cb73dac0658
  primary  9DDA7DB2F2059A596E242D69834078CE852E70DBB90B450E0775F040394870E5
           blob bafe1cc290e887264e4c94613689ab1d73eb4774
  audit    4F0B502445D5330421D597CCF674B1F0227E5D14E8DADABFF26253954827BE95
           blob f7731259bf5fe75e7e48fd2f57f81e5001da165a
  review   48D59C4408EA1F91E6B6AA436C474B903B578B41C0E23444A201510F1E08C0AC
           blob 3bd7f333ab735891b452566e29edf251997435e5

exceptional companion propagation at 76240ca:
  theorem  9C70842573B3DD02BE5AC9CC65B08047AF0C6877892EA816A5D89B2024ED36A3
           blob b75c8b3baf1f181129aac68020c51e038b4900b0
  primary  97177FE5D7A44821428AAED34707FAD30490D50D80163609A28FB3AE7BE663F0
           blob cd8fcab56f71e3833972103dac9498acd74b43d9
  audit    9DB62582D752C85F2E7AE8343EC806B95786C5693466ECFB3666C5F838A35289
           blob d0f44eb3cb6be8ff94d9981115f19ba7d5e8c44e
  review   7BDFE90C91664B8A8AF5C3B6BFC8997F274D8EB4BCBF863757CD63E81DC30300
           blob c858dd723a0035262fedf9c61fa62c706b089bfb
```

Each pinned hostile review contains a PASS verdict on its exact recorded
bytes and preserves the global `UNRESOLVED` boundary.

## 2. Common displayed-frame interface

The dependency theorems use one common characteristic-zero interface.  The
based pair is exactly

```text
u_0=x_1-x_2,       u_1=x_3,          u_2=-x_0+x_2,
v_0=-x_1+x_2,      v_1=x_0+x_1,      v_2=x_3.
```

Its projection families and complementary quartics agree literally across
the packages:

```text
ell_1=x_2-x_1-x_0,                 ell_2=x_2-x_1,
Phi_1=(x_3,x_4,x_5,ell_1),         Phi_2=(x_0,x_4,x_5,ell_2),

F_1=x_4x_5 x_3 ell_1,              F_2=x_4x_5 x_0 ell_2,
D_0=2x_4x_5 x_0x_3,
D_1=x_4x_5 x_2(x_0+x_1),
D_2=x_4x_5 x_1(x_0-x_2).
```

All theorem inputs are four ordered independent local triples, and all use
the complete-polarization target

```text
T_(F_1)=T_(F_2)=0,
T_(D_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0.
```

The companion theorem writes the same channels generically as `m_1,m_2`
and `d_0,d_1,d_2`; its triangle table gives precisely the quadratic cores
above.  This is a naming change, not a frame or target change.  No basis
transport, generic specialization, algebraic closure, or field extension is
inserted in the composition.

The characteristic-zero scope is common.  The proofs use exact linear
algebra, nonzero target scalars, infinitude of the field, and `2!=0`; modular
enumerations are error-detecting checks only.

## 3. Rank-drop and exact `Phi_2` kernel cover

The two-sided theorem gives, for every putative exact extension of this
displayed frame,

```text
min_(2<=t<=5) rank(Phi_2|L_t)<=2.
```

The kernel theorem independently gives, for every local mode and both
families,

```text
rank(Phi_k|L_t)>=2.
```

Thus some mode `t` has `Phi_2` rank exactly two.  The ambient kernel is

```text
ker(Phi_2)={(0,a,a,b,0,0):a,b in K}.
```

For a kernel vector with `ab!=0`, the exact diagonal residual relation

```text
-(a/b)i_pD_0+i_pD_1+i_pD_2=0
```

would give a linear relation among three nonzero pure target tensors with
disjoint colour support, forcing every local coefficient of the nonzero
kernel vector to vanish.  Hence `ab=0`.  The two and only two projective
lines are

```text
N=K(x_1+x_2),           local support a nonempty subset of {1,2};
X=Kx_3,                 local support exactly {0}.
```

No generic `Phi_2` line, third exceptional line, empty support, or support
containing colour `0` for `N` survives.  This is the exhaustive split used
by the endpoint.

## 4. Same-mode contradiction at `N`

The line `N` lies in both ambient kernels:

```text
N subset ker(Phi_1) intersect ker(Phi_2).
```

If a local plane contains a nonzero vector on `N`, both restricted ranks are
at most two.  The common rank floor makes both ranks exactly two.  The
same-mode theorem excludes every local mode with this profile, including
the proportional `N/N` case.

Its five-line cover was checked independently.  Rank-nullity removes the
common/noncommon pairs, legal single-slot contractions remove `B/X` and
`C/X`, and the full exact target removes the proportional `N/N` cycle.  In
particular, the final all-colour-zero `D_0` slice is used; the theorem does
not rely on the insufficient pairwise-incidence shortcut recorded by its
exact near-survivor.

Therefore the initial `N` leaf is impossible.

## 5. The `X` companion and second contradiction

For `p=X=x_3`, the companion theorem computes

```text
Q_X=span{B_zp}=span{ell_1,x_0},
H_X=ann_R(Q_X)=span{x_1+x_2,x_3}.
```

The all-support quotient lemma applies because `dim Q_X=2` and the local
support of `X` is the singleton `{0}`.  It supplies a nonzero vector in
`H_X` in a **distinct** local mode, with support disjoint from `{0}`.
Writing that vector as

```text
q=(0,a,a,b),
```

the exact single-contraction relation

```text
-a B_(d_0)q+b(B_(d_1)q+B_(d_2)q)=0
```

forces `b=0`; otherwise all three local coefficients of `q` vanish.  Hence
the companion is exactly a nonzero vector on `N`, with nonempty support in
`{1,2}`.

At that distinct companion mode, membership in the two ambient kernels and
the rank floor again make both restricted ranks exactly two.  The same-mode
theorem supplies the contradiction.  The endpoint uses only this reviewed
occurrence-to-companion implication.

No second contraction is needed in the endpoint.  In particular, it never
replaces the full second-contraction tensor by a scalar multiple of an
uncontracted `A`-pairing matrix.  The companion package explicitly refutes
that shortcut with an exact rational countermodel.

## 6. Exhaustion and acyclicity

The proof graph is

```text
Phi_2 rank drop + rank floor
  -> exact low kernel line is N or X
       N -> same-mode N/N contradiction
       X -> distinct-mode N companion -> same-mode N/N contradiction.
```

The leaves are disjoint projective lines and exhaust the rank-two
`Phi_2` kernel pencil.  Both terminate in the same already-reviewed
same-mode obstruction, and no exceptional line survives.

The mathematical dependency direction is

```text
two-sided projection drop
  -> kernel-support localization
       -> same-mode exclusion
       -> exceptional companion propagation
  -> present N/X composition.
```

The same-mode theorem precedes the generalized companion theorem and proves
its own triangle `N`-cycle propagation internally.  It does not depend on
the later `X -> N` theorem.  The generalized companion theorem uses the
kernel-support predecessors and does not use the present endpoint.  The
endpoint contributes no new contraction identity.  No circular dependency
was found.

## 7. Replay and implementation audit

Fresh replay passed for all ten scripts:

```text
two-sided projection-drop primary/audit:                PASS/PASS;
kernel-support primary/audit:                           PASS/PASS;
same-mode exclusion primary/audit:                      PASS/PASS;
companion-propagation primary/audit:                    PASS/PASS;
endpoint composition primary/audit:                     PASS/PASS.
```

The independent endpoint audit imports neither its primary verifier nor
SymPy.  It checks commit ancestry, committed bytes, SHA-256 pins, and Git
blob IDs directly.  Its independent `N/X` table has two rows and no
survivor.

Focused QA passed:

```text
py_compile on all ten scripts:                          PASS;
Ruff on all ten scripts:                                PASS;
tracked diff whitespace check:                          PASS;
new-package trailing-whitespace scan:                   PASS.
```

The scripts audit identities, case tables, and frozen-object provenance;
the written characteristic-zero arguments remain the proof.

## 8. Accepted boundary

```text
field:                                                   CHARACTERISTIC ZERO;
displayed based Delta-admissible (3,1) frame:             ASSUMED;
exact ordered local triples and full targets:             ASSUMED;
Phi_2 rank-drop existence:                                REVIEWED/PINNED;
rank floor and exact Phi_2 N/X cover:                      REVIEWED/PINNED;
same-mode cross-family low exclusion:                     REVIEWED/PINNED;
X -> distinct-mode N companion:                           REVIEWED/PINNED;
exact extension of the displayed based frame:             EXCLUDED;

all based-frame stabilizer orbits of unbased (3,1):       NOT CLASSIFIED;
transport to every based (3,1) frame:                     NOT PROVED;
unbased (3,1) orbit universally excluded:                 NOT PROVED;
other equality-five orbits:                               NOT ADDRESSED;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```
