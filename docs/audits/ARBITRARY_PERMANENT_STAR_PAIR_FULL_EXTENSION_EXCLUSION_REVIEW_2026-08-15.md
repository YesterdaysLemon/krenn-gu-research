# Hostile review of star-pair full-extension exclusion

## Verdict and exact scope

**PASS, for the displayed based `(4,1)` star frame, pointwise, over fields
of characteristic zero.**  No Git-object pin, reviewed-byte, field,
based-frame, quartic-core, projection, ordered-slot, target, kernel-support,
same-mode, companion-support, exceptional-leaf, slice-rank, restricted-core,
factorization, dependency-cycle, implementation, or scope blocker survived
hostile review.

The reviewed package proves that the one explicitly displayed ordered
`(4,1)` frame has no exact `P_6 -> Delta_3` extension.  It does not classify
the based-frame stabilizer orbits inside the unbased `(4,1)` orbit and does
not transport the result to any other based frame.  It proves no result for
the inequivalent `(3,1)` or `(4,2)` orbits, no unrestricted permanent
nonrestriction theorem, and no global Krenn--Gu resolution.  The global
status remains **UNRESOLVED**.

Reviewed endpoint:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_STAR_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md
  verify_arbitrary_permanent_star_pair_full_extension_exclusion.py
  audit_arbitrary_permanent_star_pair_full_extension_exclusion.py
```

Frozen endpoint hashes:

```text
theorem:
C9DAABB0C288F6FB54C9FB209FD5D2E341118EFE0C181442899757063EA0B66D

primary verifier:
D74024BC0B34373DC0E88A9F0EAB98A08DFC0804070E426AA0ADA6DBD9C7C5F8

independent audit:
921EB4FECB3D14633043C13DF864048E292F297796E769BACB5AF0C5D9413824
```

## 1. Frozen Git objects and predecessor reviews

All five predecessor commits resolve as commits and occur in this ancestry
order:

```text
ca21e1d32c2e00a228d5be8050e57badd95f73d4
  Prove star-pair two-sided projection drop

985f1a4cd49508da067ba1b4d788b2e576368448
  Localize star-pair kernel supports

76240ca4becc1b58b9803ac1ec6a4db159c07d3c
  Propagate star-triangle exceptional companions

85e49d1100b6b77b610b07744ac377eb291691e7
  Constrain star-pair same-mode lows

4541cce432f621b9954251a0454f820cef500aac
  Exclude star-pair singleton common cycles
```

For every predecessor artifact, the bytes at the pinned commit, the current
bytes, the recorded SHA-256 digest, and the recorded Git blob agree.  The
exact pins are:

```text
two-sided projection drop at ca21e1d:
  theorem  76AEBB661CA3E89DF3E4228954B0D7CB3D736414A4AB22C2EBC9A2C84A774D62
           blob 29d6874fad7057122ece6a4bad2a60ce3f89c836
  primary  223B61126635FE59987B75684CFA6FCA1173737913CEAD0F46D98AA3A8C3DF1B
           blob 037c730d7e95c2b95597b8400232ed723b63baac
  audit    CD4D833DB7CB132FCFED02A0BD2353799E184DAC3DFAC9EC5F714F998F614311
           blob f9867fb2c03a3a5cda2b40a743bed9fef32f7edc
  review   F0C61339191FDD02C6F72F721C175636DC4A302554C71FF51C8809747D30203F
           blob c47ded42913e03a7dde7562ec9333b3b58e6cf02

kernel-support boundary at 985f1a4:
  theorem  2B44641806EEE9B14D2F9DCC692C2E8E1CB9917832A9C2FD9E658243ACFE51F5
           blob c6da76f7c05de49a923120d83e931d0e94b1a4e8
  primary  73406FF9C62A2113341BBC97E36E2E4F4151CF399E72EEBFD831A05944744124
           blob 98c0c18d9e4548040ca1f75e3b11e0e319a80d1c
  audit    0D4F649C78577158E39577FB5CBDDA1A0057534E75A803F1EB73F25726DA5721
           blob 44e26a0f87ece8d37dbf51c2f7e89e155c86a633
  review   EC573CB950EFBCB9DFE300DBCEBDCE9992E6DF839EF77A45C038E605EA925A45
           blob 3282fda7525aa36c0ac30d0506518dee26bccb29

exceptional companion propagation at 76240ca:
  theorem  9C70842573B3DD02BE5AC9CC65B08047AF0C6877892EA816A5D89B2024ED36A3
           blob b75c8b3baf1f181129aac68020c51e038b4900b0
  primary  97177FE5D7A44821428AAED34707FAD30490D50D80163609A28FB3AE7BE663F0
           blob cd8fcab56f71e3833972103dac9498acd74b43d9
  audit    9DB62582D752C85F2E7AE8343EC806B95786C5693466ECFB3666C5F838A35289
           blob d0f44eb3cb6be8ff94d9981115f19ba7d5e8c44e
  review   7BDFE90C91664B8A8AF5C3B6BFC8997F274D8EB4BCBF863757CD63E81DC30300
           blob c858dd723a0035262fedf9c61fa62c706b089bfb

same-mode boundary at 85e49d1:
  theorem  27AA460A9846A3568F3160DF3F6A03C798E87696D1A6E22900F13F8A76EF5AD9
           blob bcfb433dd3d4022be83ec09d43d0b4008560b298
  primary  0D24DC727902A18824B5D5470542F5BDF7E87FDAB4C5D5FEBE5C439CCE4FFAEA
           blob bb0ac965729742e316de620819b89397ef0197de
  audit    E849C2F5A3D0A14414156F70DC7A58CF62B332585A4271268EB54B705719F543
           blob d9070888749620e95533db24fbe8ec21160d5e0d
  review   FB85A20E79B35020FECD790A6A9B5B2922F12B2D699C50052967AF434C164E82
           blob 910ce207f2004d52f4e851d501e6e4022f132688

singleton `N/N` completion at 4541cce:
  theorem  EA29D52F17100A7D99F5A56254309B69BC21744E5C2BAFE78A981F19097B4693
           blob 3ca61522b4ede881e53fdd08d9d914bf72b56cea
  primary  CED670F3D48B567CBC62B4759718E056E21A5E21CB1F42DDA85426F502A4B0FE
           blob f26d073c5bbf60d0f850ed488854b3b6b0a55286
  audit    8ADCB1EAF9B4E3C5B140463AEC89615DBE323A385DC3893030F57C10ECAFA031
           blob 5953ae1325e90fa35584f203990233bcefe2204d
  review   271D2C87D4F76FDF3541816183A40E83A3E7B5B8F9379FDEB6FC584188122535
           blob 9cdfb41d6798a45d67f32a7c332589e77688ed51
```

Each pinned hostile review has a PASS verdict on those exact bytes and
retains the global `UNRESOLVED` boundary.

## 2. One common field, frame, and target interface

All five predecessors and the endpoint use the same characteristic-zero
square-free algebra

```text
K[x_0,...,x_5]/(x_0^2,...,x_5^2)
```

and the same displayed ordered based star frame:

```text
u_0=-x_0+x_2,      u_1=x_0-x_3,       u_2=x_1-x_2,
v_0=x_0+x_1-x_2+x_3,
v_1=x_0+x_1,       v_2=-x_1+x_2.
```

The five complementary quadratic cores agree literally:

```text
g_(m_1)=x_3(x_0+x_1-x_2),
g_(m_2)=(x_0-x_3)(x_1-x_2),
g_(d_0)=x_0x_1+x_0x_3-x_1x_2+2x_1x_3-x_2x_3,
g_(d_1)=-x_2(x_0+x_1-x_3),
g_(d_2)=2x_0x_3.
```

The projection families are exactly

```text
Phi_1=(x_3,x_4,x_5,x_0+x_1-x_2),
Phi_2=(x_0-x_3,x_4,x_5,x_1-x_2).
```

The local inputs are four **ordered** independent triples
`L_a,L_b,L_c,L_d`.  The complete common target convention is

```text
T_(m_1)=T_(m_2)=0,
T_(d_i)=lambda_i e_i^* tensor e_i^* tensor e_i^*
                         tensor e_i^*,
lambda_i != 0 for i=0,1,2.
```

Thus the composition neither swaps a tensor slot nor weakens a full
four-slot identity to a diagonal-only or scalar identity.

## 3. Exhaustive reduction to four noncommon lines

The two-sided predecessor supplies a mode with projection rank at most two
for each family.  The kernel boundary supplies the matching rank floor, so
every low rank is exactly two, and classifies every possible kernel and its
nonempty support:

```text
Phi_1:
  N  =x_1+x_2               support subset {0,1}
  B_0=x_0+x_2               support subset {1,2}
  C_0=x_0-x_1               support subset {0,2}

Phi_2:
  N  =x_1+x_2               support subset {0,1}
  B_1=x_0+x_3               support subset {0,2}
  C_1=x_0+x_1+x_2+x_3       support subset {1,2}.
```

Here every support is a nonempty subset of its displayed pair.  There is no
unlisted generic kernel direction and no support-three low.

The same-mode boundary excludes common/noncommon, all four
noncommon/noncommon pairs, and support-two `N/N`.  The singleton completion
excludes the remaining singleton `N/N`, so no local mode is low for both
families.  Because `N` belongs to both ambient projection kernels, any local
plane containing `N` would nevertheless have both restricted ranks at most
two; the rank floor would make both exactly two, contradicting that complete
same-mode exclusion.  Therefore `N` cannot occur at all.

Every low occurrence is consequently one of

```text
B_0, C_0, B_1, C_1.
```

For each occurrence, companion propagation gives a normalized companion in
a **different** local mode.  Excluding one arbitrary occurrence of each
line therefore suffices regardless of the number, family, or placement of
any other lows.  This is why there is no omitted same-mode or low-count
diagram.

## 4. All four exceptional cycles and all twelve support leaves

In channel order `(m_1,m_2,d_0,d_1,d_2)`, direct contraction gives:

```text
low p / allowed support      companion q / colour e
  r_p                         r_q                       common ell

B_0=x_0+x_2 / {1,2}         q=x_2-x_0 / 0
  (0,-1,0,1,-1)              (0,0,1,0,0)              -2(x_1+x_3)

C_0=x_0-x_1 / {0,2}         q=x_0+x_1 / 1
  (0,1,-1,0,-1)              (0,0,0,1,0)              -2x_2

B_1=x_0+x_3 / {0,2}         q=x_3-x_0 / 1
  (-3,0,1,0,1)               (0,0,0,1,0)               2x_2

C_1=x_0+x_1+x_2+x_3 / {1,2}
                              q=-x_0+x_1+x_2+x_3 / 0
  (-1,0,0,1,1)               (-2,0,1,0,0)              2(x_3-x_1)
```

For every row, both contractions give the displayed nonzero covector:

```text
B_(r_p)p=B_(r_q)q=ell.
```

The companion combination has diagonal coefficient one only at colour `e`;
the other nonzero entries are mixed channels.  The low combination has
nonzero diagonal coefficients at both allowed colours.  Full single
contraction of the ordered targets therefore gives two full three-slot
tensors for `P=pol(ell*x_4*x_5)`: a nonzero pure `e` diagonal from the
companion and nonzero pure diagonals at every colour actually used by the
low.

Each allowed pair has exactly three nonempty subsets.  The table therefore
has `4 * 3 = 12` leaves: four support-two leaves and eight singleton leaves.
The two arguments below close all twelve.

## 5. Support-two slice-rank obstruction

For a support-two low with allowed colours `i_1,i_2`, the companion colour
`e` is the third colour.  With `E` carrying coordinates
`(X,U,V)=(ell,x_4,x_5)`, the first-shore vectors

```text
y_(a,e), y_(b,i_1), y_(b,i_2)
```

give three nonzero independent diagonal slices of `P=pol(XUV)` on the
other two shores.  Their span is three-dimensional, and the restriction is
a concise weighted `Delta_3`.  Because `P` factors through the three
evaluation maps to the three-space `E`, conciseness makes all three maps
isomorphisms.  This would make `pol(XUV)` equivalent under `GL_3^3` to a
rank-three weighted diagonal tensor.

That rank conclusion is impossible.  The symmetric first-slice space is

```text
span{sym(UV),sym(XV),sym(XU)}.
```

It contains no nonzero rank-one matrix.  Equivalently, the three principal
two-minors of

```text
[ 0  V  U ]
[ V  0  X ]
[ U  X  0 ]
```

are `-V^2,-U^2,-X^2`; a nonzero slice cannot have rank one.  A concise
rank-at-most-three three-by-three-by-three tensor would supply nonzero
rank-one matrices spanning its first-slice space.  Hence
`rank(pol(XUV))>3`, closing all four support-two leaves.

## 6. Singleton rank-two/rank-three dichotomy

Let `i` be the singleton low colour, `e` the companion colour, and `t` the
unused allowed colour.  Write

```text
bar(v)=(ell(v),x_4(v),x_5(v)) in E
```

and let `S:E -> Mat_(3x3)(K)` be the slice map on the two remaining local
modes.  The two contraction identities put nonzero multiples of
`E_(ee),E_(ii)` in its image, while the unused vectors in the low and
companion modes map to its kernel.  Thus `rank S` is two or three.

If `rank S=3`, injectivity forces

```text
bar(y_(a,t))=bar(y_(b,t))=0.
```

If `rank S=2`, the image is exactly `span{E_(ee),E_(ii)}`.  The live
diagonal and zero cross cells make the two `e,i` evaluation vectors on each
of the remaining shores independent.  For every nonzero vector `d` in
`E`, the contraction map with `d` has kernel dimension at most one, as the
same three principal minors `-V^2,-U^2,-X^2` show.  A nonzero unused vector
cannot therefore annihilate both independent live vectors.  Hence

```text
bar(y_(c,t))=bar(y_(d,t))=0.
```

This argument includes coordinate-zero and isotropic-looking vectors; it
does not assume that all three evaluation coordinates are nonzero.  It also
asserts only that the displayed projections vanish, never that an ambient
local vector is zero.

## 7. Restricted core gate and legal full factorization

The exact core identities are:

```text
B_0:
  -g_(m_1)+g_(m_2)+g_(d_0)-g_(d_1)+g_(d_2)
    =2x_0(x_1+x_3)

C_0 and B_1:
  -3g_(m_1)-g_(m_2)+g_(d_0)+g_(d_2)
    =x_2(x_0-x_1+x_3)

C_1:
  -g_(m_1)-g_(m_2)+g_(d_1)+g_(d_2)
    =-(x_0+x_2)(x_1-x_3).
```

Each right side is divisible, up to a nonzero scalar, by the row's `ell`.
Its bilinear polarization therefore vanishes on
`ker(ell) x ker(ell)`.  For the two possible unused colours in each row,
the corresponding live diagonal coefficients are:

```text
B_0:       d_1=-1, d_2= 1
C_0,B_1:   d_0= 1, d_2= 1
C_1:       d_1= 1, d_2= 1.
```

All are nonzero in characteristic zero.

In the rank-three slice branch, the two unused vectors on the low and
companion shores have zero `(ell,x_4,x_5)` projection.  Thus, at the full
all-colour-`t` four-slot entry, the only surviving factor placement in
`x_4x_5g_z` puts `g_z` on those two shores and the `x_4,x_5` pairing on the
other two.  The applicable core combination vanishes, whereas the exact
target combination is its nonzero listed `d_t` coefficient times
`lambda_t`.

In the rank-two slice branch, the same full factorization is used with the
two pairs of shores reversed.  Again the core combination vanishes and the
target is nonzero.

This is not a scalar-times-`M` shortcut.  The factorization is invoked only
after two whole ordered shores have zero `x_4,x_5` evaluation, so every
other polarization placement vanishes explicitly.  No two vectors from one
local plane are inserted into different tensor slots.  The primary verifier
checks both shore orientations in the full six-variable square-free algebra;
the independent audit separately exhausts the basis factorizations.

## 8. Proof topology and circularity audit

The proof graph is finite and acyclic:

```text
two-sided rank drop
  -> existence of a low in each projection family

kernel-support boundary
  -> rank floor and the six-line/support classification

same-mode boundary + singleton completion
  -> no mode low for both families
  -> common line N absent

companion propagation
  -> every B_0,C_0,B_1,C_1 occurrence has its displayed
     distinct-mode singleton companion

endpoint table
  -> support two impossible
  -> singleton rank 3 impossible
  -> singleton rank 2 impossible
  -> all twelve leaves impossible

two-sided existence + no surviving leaf
  -> contradiction for the displayed based frame.
```

The predecessor commits form the ancestry chain recorded in Section 1.
None of the predecessor theorem, verifier, audit, or review files refers to
or imports the endpoint package.  The endpoint imports neither predecessor
verifier implementation nor predecessor audit implementation as a proof
step; it consumes their reviewed theorem interfaces and pins all twenty
artifacts.  No conclusion is fed back into an assumption.

The final contradiction needs only one low occurrence, whose existence is
provided by the two-sided theorem.  Since every possible common or
noncommon line and every nonempty allowed support has been handled, there is
no missing exceptional line, same-mode branch, or low-count case.

## 9. Replay and QA

All predecessor primary verifiers and independent audits were replayed, as
were both endpoint scripts:

```text
star-pair two-sided projection drop:          primary PASS; audit PASS
star-pair kernel-support boundary:            primary PASS; audit PASS
star-triangle companion propagation:          primary PASS; audit PASS
star-pair same-mode boundary:                 primary PASS; audit PASS
star-pair singleton N/N completion:           primary PASS; audit PASS
star-pair full-extension endpoint:            primary PASS; audit PASS
```

The endpoint primary reconstructed the four common-cubic rows, the core
relations, the full quartic factorizations, the `XUV` gates, and all twelve
proof leaves.  The endpoint audit imported neither the primary verifier nor
SymPy.  It independently checked Git-object pins, rebuilt the integer and
rational tables, exhausted both full-factorization orientations, checked
the formal `XUV` minors, and ran finite-field annihilator countermodel
searches.  The finite-field searches are corroborative only; the proof is
the exact characteristic-zero argument above.

All twelve Python files passed `py_compile` and Ruff.  `git diff --check`
and the package trailing-whitespace scan also passed.

## 10. Final boundary

The audited conclusion is exactly:

```text
displayed based Delta-admissible (4,1) frame:  no exact P_6 -> Delta_3 extension
field:                                         characteristic zero
claim mode:                                    pointwise, exact
orbit transport:                               not proved
all based (4,1) frames:                        not classified
unbased (4,1) orbit:                           not universally excluded
(3,1), (4,2), and active-support 5/6:          no claim here
unrestricted P_6 -> Delta_3:                   unknown
global Krenn--Gu conjecture:                   UNRESOLVED
```
