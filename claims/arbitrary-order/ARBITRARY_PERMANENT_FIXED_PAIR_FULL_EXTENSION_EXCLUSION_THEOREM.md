# Arbitrary permanent fixed-pair full-extension exclusion theorem

## Status

This note proves an exact characteristic-zero endpoint for the fixed
representative of the equality-five `(4,2)` pair.  That fixed pair admits no
exact extension from `P_6` to the three-colour diagonal tensor `Delta_3`.

The proof is a composition of three committed and hostile-reviewed results:

1. the distinct-two-low reduction leaves exactly two terminal branches;
2. the zero high-high `A`-pairing branch is impossible; and
3. the nonzero `E_22` high-high `A`-pairing branch is impossible.

No new contraction identity is asserted here.  The purpose of this package
is to pin the reviewed dependencies, check that their hypotheses and
conventions agree, and make the exhaustive proof topology explicit.

This is **not** an unrestricted `P_6 -> Delta_3` theorem.  In particular,
this note proves no normalization or transport from the fixed `(4,2)` pair
to the other equality-five pair orbits `(4,1)` or `(3,1)`.  It therefore does
not resolve the arbitrary-order permanent nonrestriction problem or the
global Krenn--Gu conjecture.  The global status remains **UNRESOLVED**.

## 1. Exact fixed-pair statement

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

At the first two modes fix

```text
u_0=x_0-x_3,      u_1=x_1-x_3,      u_2=x_2-x_3,
v_0=x_1+x_2,      v_1=x_0+x_2,      v_2=x_2-x_3.      (1)
```

This is the fixed representative called the equality-five `(4,2)` pair in
the predecessor chain.  Its two mixed and three diagonal product classes
have complementary quartics

```text
star(m_1)= x_4x_5 x_1 (x_3-x_2-x_0),
star(m_2)= x_4x_5 x_0 (x_3-x_2-x_1),
star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.                             (2)
```

For each remaining mode `t=2,3,4,5`, let

```text
(y_(t,0),y_(t,1),y_(t,2))
```

be an ordered linearly independent triple spanning `L_t subset K^6`.  An
exact extension of the fixed pair to `Delta_3` would satisfy

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (3)
```

Here every `T_z` is the complete polarization of `star(z)` on the four
ordered local triples.  Split

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5},
J((r_4,r_5),(s_4,s_5))=r_4s_5+r_5s_4,                 (4)
```

write `A_t:K^3 -> A` for the `A`-projection matrix in mode `t`, and put

```text
M_(st)=A_s^T J A_t.                                    (5)
```

### Theorem 1 (fixed `(4,2)` full-extension exclusion)

There are no four ordered independent local triples satisfying (3) over a
field of characteristic zero.  Equivalently, the fixed pair (1) has no exact
`P_6 -> Delta_3` extension.

## 2. Frozen reviewed dependencies

The proof uses the following exact committed bytes.  SHA-256 digests are
uppercase and are checked by both replay scripts.

### 2.1 Distinct-two-low reduction

```text
commit:
aa21e104645094b10830c5236210cd2961003579

theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_REDUCTION_THEOREM.md
87BD9CCC45C07088465C27FB4032BCC34DDB7004789A3FC28ECA36F3BFA67D1E

primary verifier:
claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py
20ECAA638C7AFDFB11187925C76AA6DD9F142E63AE41AD5220F27FA70518290A

independent audit:
claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py
F8A1350BD36DA6CFCEBCA674791F44B6DBCF00BD782F53B6319E609005658D56

hostile review:
docs/audits/ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_REDUCTION_REVIEW_2026-08-15.md
FA72305DCA86760A934736168D6FB8E9647A8FA8B6E5C5E66B2A008CD830FEA3
verdict: PASS.                                             (6)
```

### 2.2 Zero-branch exclusion

```text
commit:
6daade565a5424b17ba272ef609b17271e4f8c4d

theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_FIXED_PAIR_TWO_LOW_ZERO_BRANCH_EXCLUSION_THEOREM.md
236065BB239059865C91105D49590693E5D9121DD1A0BBB365863A7667FCF0CA

primary verifier:
claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py
85504804E6BF5A056C53E6E8FDD93B999AB56A0C2E63187E24C590840C58600D

independent audit:
claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py
7CB12A912E30C6A44AAC784CE6786E822106BA7A59E3EB396BE9DB33244CEDF6

hostile review:
docs/audits/ARBITRARY_PERMANENT_FIXED_PAIR_TWO_LOW_ZERO_BRANCH_EXCLUSION_REVIEW_2026-08-15.md
83462F64188C6D8D0B6D4801779828CCA43CCA88F1896B6A5052D7A3A93BBA0A
verdict: PASS.                                             (7)
```

### 2.3 Nonzero-`E_22` branch exclusion

```text
commit:
7bc6e6bb1ff97080671a1ff9f53ea37fe96e02be

theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_E22_EXCLUSION_THEOREM.md
925284C772176125855BF99199B6789E430355A0D4F87553E727CA746B206925

primary verifier:
claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py
00BA077A4F4023ECA875C2B9DD826D8FFC2690723CBA16B1C6737720A611E2FC

independent audit:
claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py
0B640BF86F7C495821705D3489307ECA668BFD6951AF342B18665E2B577473B8

hostile review:
docs/audits/ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_E22_EXCLUSION_REVIEW_2026-08-15.md
1BD0A74E440342382981BC894316D2BA4E61F3438AC4CF659C0E90FD21B9CF05
verdict: PASS.                                             (8)
```

The reviews in (6)--(8) audit the mathematical arguments, exact scopes,
characteristic-zero hypotheses, tensor-slot legality, computational replay,
and independence of the corresponding audits.  The present composition
does not promote verifier output into a proof: the three written theorems
are the proof dependencies, and their scripts and reviews are separate
evidence axes.

## 3. Interface and branch exhaustion

All three dependencies use exactly the field, fixed pair, quartics, local
triple convention, target equations, splitting, bilinear form, and pairing
matrix in (1)--(5).  No change of basis, orbit transport, genericity
specialization, or field extension is inserted between them.

Assume for contradiction that an extension satisfying (3) exists.  The
distinct-two-low theorem at commit (6), including its reviewed same-mode and
exceptional-line predecessors, yields the following exhaustive state:

```text
exactly two low modes;
one is low only for Phi_1 and one only for Phi_2;
the low modes occupy distinct tensor slots;
the other two modes s,t are high for both families;

M_(st)=0
or
M_(st)=mu E_22 for some mu!=0.                         (9)
```

The alternatives in (9) are disjoint because `mu!=0`.  They are exhaustive
because the reduction classifies every compatible pair of the two low modes:
disjoint low supports give the zero matrix, while the only nonzero case is
a different-missing pair whose common active colour is `2`, giving a nonzero
multiple of `E_22`.

The terminal theorem interfaces are exact:

```text
terminal Z:
  input  M_(st)=0 with the two-low/high-high state of (9);
  output contradiction to (3) by commit (7).

terminal E:
  input  M_(st)=mu E_22, mu!=0, with the inherited rank/support
         consequences of the same reduction;
  output contradiction to (3) by commit (8).           (10)
```

The zero theorem assumes neither singleton nor support-two low support and
therefore covers every zero case left by the reduction.  The `E_22` theorem
uses the reduction's exact rank boundary, treats both different-missing line
pairs, both orientations of the rank-two low shore, and the exhaustive
singleton/support-two split.  Thus neither edge in (10) drops a residual
case.

## 4. Proof of Theorem 1

Suppose (3) holds.  Apply the distinct-two-low reduction to obtain (9).

If `M_(st)=0`, the zero-branch exclusion theorem contradicts (3).

Otherwise the exhaustive second alternative in (9) gives

```text
M_(st)=mu E_22,                  mu!=0.
```

The nonzero-`E_22` exclusion theorem then contradicts (3).

Both exhaustive alternatives are impossible.  Therefore the assumed exact
extension does not exist.  This proves Theorem 1.

## 5. Exact boundary

```text
field:                                                   CHARACTERISTIC ZERO;
fixed pair (1), equality-five (4,2) representative:      ASSUMED;
exact local triples and full targets (3):                 ASSUMED;
distinct-two-low reduction:                               REVIEWED/PINNED;
zero terminal branch:                                     EXCLUDED;
nonzero E_22 terminal branch:                             EXCLUDED;
exact extension of the fixed pair (1):                    EXCLUDED;

transport to equality-five orbit (4,1):                   NOT PROVED;
transport to equality-five orbit (3,1):                   NOT PROVED;
arbitrary equality-five normalization:                    NOT PROVED;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.  (11)
```

The incidence-only rational fixtures in the reduction theorem do not
contradict this endpoint: each deliberately violates a mixed-zero equation,
and each terminal theorem uses the full target equations to exclude its
corresponding branch.

## 6. Exact replay

Run the composition checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_full_extension_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_full_extension_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_full_extension_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_full_extension_exclusion.py
```

The primary verifier checks every frozen SHA-256 dependency, the hostile
review verdicts, the common mathematical interface, and the exact two-leaf
proof topology.  The independent audit imports neither the primary verifier
nor SymPy.  It checks the committed Git objects against the pinned hashes,
independently reads the accepted dependency boundaries, and exhausts the
two-branch truth table.  These scripts verify dependency identity and proof
composition; they do not replace the three written characteristic-zero
arguments.
