# Hostile review of fixed-pair full-extension exclusion

## Verdict and exact scope

**PASS, for the stated fixed `(4,2)` representative, pointwise,
characteristic-zero composition.**  No Git-object pin, theorem/review-byte,
field, fixed-frame, quartic, ordered-slot, target, pairing-matrix, same-mode,
low-count, branch-exhaustion, terminal-interface, dependency-cycle,
implementation, or scope blocker survived hostile review.

The reviewed composition proves that the displayed equality-five `(4,2)`
pair has no exact `P_6 -> Delta_3` extension.  This is not transport to either
other equality-five orbit.  In particular, it proves no result for the
`(4,1)` or `(3,1)` representatives, no unrestricted permanent
nonrestriction theorem, and no global Krenn--Gu resolution.  The global
status remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_full_extension_exclusion.py
  audit_arbitrary_permanent_fixed_pair_full_extension_exclusion.py
```

Frozen package hashes:

```text
theorem:
8AE57E0032B046303260BCEF9DC0AE56635DC9AEAA9AF096D609079523D65DDE

primary verifier:
BFBE3D709E015791DE53A6694076192488DE0F2CC42C639AE4C0E0D04D3F2C54

independent audit:
8690F4F8ED9C2E5F29D25E0317E77BEAD585291091CE3BC89ED5AF9990C25454
```

## 1. Git-object and review pins

All three dependency commits resolve as commits, are ancestors of the
reviewed branch head, and form the expected linear history:

```text
aa21e104645094b10830c5236210cd2961003579
  Reduce fixed pair to two distinct low modes

6daade565a5424b17ba272ef609b17271e4f8c4d
  Exclude fixed-pair two-low zero branch

7bc6e6bb1ff97080671a1ff9f53ea37fe96e02be
  Exclude fixed-pair two-low E22 branch
```

For each commit, `git show <commit>:<path>` agrees byte-for-byte with the
current theorem, primary verifier, independent audit, and hostile review.
Their SHA-256 digests are exactly:

```text
distinct-two-low reduction at aa21e10:
  theorem  87BD9CCC45C07088465C27FB4032BCC34DDB7004789A3FC28ECA36F3BFA67D1E
  primary  20ECAA638C7AFDFB11187925C76AA6DD9F142E63AE41AD5220F27FA70518290A
  audit    F8A1350BD36DA6CFCEBCA674791F44B6DBCF00BD782F53B6319E609005658D56
  review   FA72305DCA86760A934736168D6FB8E9647A8FA8B6E5C5E66B2A008CD830FEA3

zero-branch exclusion at 6daade5:
  theorem  236065BB239059865C91105D49590693E5D9121DD1A0BBB365863A7667FCF0CA
  primary  85504804E6BF5A056C53E6E8FDD93B999AB56A0C2E63187E24C590840C58600D
  audit    7CB12A912E30C6A44AAC784CE6786E822106BA7A59E3EB396BE9DB33244CEDF6
  review   83462F64188C6D8D0B6D4801779828CCA43CCA88F1896B6A5052D7A3A93BBA0A

nonzero-E_22 exclusion at 7bc6e6b:
  theorem  925284C772176125855BF99199B6789E430355A0D4F87553E727CA746B206925
  primary  00BA077A4F4023ECA875C2B9DD826D8FFC2690723CBA16B1C6737720A611E2FC
  audit    0B640BF86F7C495821705D3489307ECA668BFD6951AF342B18665E2B577473B8
  review   1BD0A74E440342382981BC894316D2BA4E61F3438AC4CF659C0E90FD21B9CF05
```

Each pinned hostile review contains a PASS verdict on the exact bytes above.
The endpoint audit checks the committed objects rather than merely checking
the current checkout.

## 2. Common mathematical interface

The three dependency theorems use the same interface, with no intervening
normalization, specialization, or field extension:

```text
field:       an arbitrary field K of characteristic zero;
algebra:     Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2);
fixed pair:  the displayed equality-five (4,2) representative;
slots:       four ordered independent local triples after fixing two modes;
targets:     T_(m_1)=T_(m_2)=0 and
             T_(d_c)=lambda_c e_c^* tensor4 with lambda_c!=0;
splitting:   K^6=R direct-sum A, with dim R=4 and dim A=2;
form:        J((r_4,r_5),(s_4,s_5))=r_4s_5+r_5s_4;
matrix:      M_(st)=A_s^T J A_t.
```

The five complementary quartics agree literally in all three theorem texts:

```text
star(m_1)= x_4x_5 x_1 (x_3-x_2-x_0),
star(m_2)= x_4x_5 x_0 (x_3-x_2-x_1),
star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.
```

The zero theorem writes `A_t:L_t -> A`, while the reduction and endpoint
write its matrix in the ordered local basis as `A_t:K^3 -> A`; these are the
same map and convention.  The terminal relabellings only permute symmetric
tensor slots.  No proof moves a local vector to a different slot.

Characteristic zero is inherited without strengthening or weakening.  The
written arguments use exact finite-dimensional linear algebra and the
nonvanishing of displayed factors `2`; the finite-field checks are only
error-detecting audits.

## 3. Same-mode and low-count exhaustion

The reduction's predecessor tree was checked separately from the terminal
theorems.  Its same-mode cover is:

```text
noncommon/noncommon:
  A_0/A_1, A_0/C_1, C_0/A_1, C_0/C_1                  EXCLUDED;

common/noncommon:
  N/A_1, N/C_1, A_0/N, C_0/N                          EXCLUDED;

common/common N/N:
  propagated q_- companion                             EXCLUDED;
  propagated q_+ companion                             EXCLUDED.
```

For `N/N`, singleton and support-two occurrence of `N` are exhaustive, and
the exact companion propagation gives precisely the two projective forks
`q_-` and `q_+`.  Both sibling exclusions precede the reduction commit.
Thus no mode is low for both projection families, and the common line `N`
cannot occur in a remaining local plane.

Each projection family nevertheless has at least one rank-two mode by the
two-sided projection-drop and rank-floor predecessors.  Hence the number of
distinct low modes is at least two and, among four remaining slots, is one
of `2,3,4`.  The reduction independently excludes:

```text
four lows:  every complementary low pair forces all colour-0 and colour-1
            A-pairings to vanish, killing live d_0,d_1 coefficients;

three lows: the complete zero/one-E_22 complementary-edge split reduces to
            the proved two-colour three-line obstruction.
```

Therefore exactly two distinct low modes remain, one for each family, and
the other two modes are rank three for both projection families.  Neither
terminal exclusion is used in this count.

## 4. Disjoint and exhaustive terminal leaves

After same-mode exclusion, the family-1 low is `A_0` or `C_0`, and the
family-2 low is `A_1` or `C_1`.  Their actual coefficient supports are
nonempty subsets of the corresponding two-colour maximal supports:

```text
A_0,C_1: {1,2};                 C_0,A_1: {0,2}.
```

The exact distinct-slot contraction table gives:

```text
same missing colour:
  supports are complementary singletons, so M_(st)=0;

different missing colours, not both containing 2:
  supports are disjoint, so M_(st)=0;

different missing colours, both containing 2:
  M_(st)=mu E_22 with mu!=0.
```

These cases cover all four cross-family line pairs and every nonempty
support subset.  The leaves are disjoint because `E_22` is nonzero and
`mu!=0` over the stated field:

```text
Z: M_(st)=0;
E: M_(st)=mu E_22, mu!=0.
```

There is no third matrix type and no surviving same-mode, same-family,
three-low, or four-low input at this stage.

## 5. Terminal theorem fit

The zero theorem accepts exactly leaf Z together with the inherited
two-low/high-high state.  It assumes neither singleton nor support-two low
support.  The zero matrix forces both high `A`-maps to have rank one.  Legal
single-low contractions of the two mixed-zero tensors put both low images
in the common orthogonal complement of the high image lines.  The exhaustive
dependent/independent line dichotomy then makes every cross-mode `J` pairing
zero, contradicting a live diagonal target.

The `E_22` theorem accepts exactly leaf E and the reduction's inherited rank
boundary.  It covers both different-missing line pairs, both orientations
of the rank-two low shore, and for each low the exhaustive singleton `{2}`
versus support `{k,2}` split.  In the singleton case the residual equations
make two columns of the rank-one high mode dependent.  In the support-two
case a rank-two pairing matrix would equal a nonzero rank-one matrix unit.
Both alternatives contradict the exact target.

Thus both and only both reduction leaves end in contradiction.  The zero
theorem does not invoke the `E_22` theorem, and the `E_22` theorem does not
invoke the zero theorem.

## 6. Dependency acyclicity

The load-bearing direction is:

```text
projection/rank-floor and exceptional-line results
  -> same-mode noncommon and common/noncommon exclusions
  -> q_- and q_+ N/N exclusions
  -> aa21e10 distinct-two-low reduction
       -> 6daade5 zero terminal
       -> 7bc6e6b E_22 terminal
  -> present two-leaf composition.
```

All reduction predecessors occur before `aa21e10`.  The zero commit has
`aa21e10` as its parent, and the `E_22` commit descends from both.  The
reduction leaves both terminal branches explicitly open; neither terminal
result is used to prove the reduction.  The present theorem adds no new
mathematical identity.  No circular proof dependency was found.

## 7. Replay and implementation audit

Fresh replay passed for all eight scripts:

```text
distinct-two-low primary and independent audit:        PASS/PASS;
zero-terminal primary and independent audit:           PASS/PASS;
E_22-terminal primary and independent audit:           PASS/PASS;
composition primary and independent audit:             PASS/PASS.
```

The dependency replays include exact symbolic or independent dictionary
polarization, finite support exhaustions, rational fixtures, rank-boundary
checks, and the two terminal identities.  The composition audit imports
neither the primary composition verifier nor SymPy.  Its Git subprocess path
checks committed object bytes and ancestry directly, and its independent
truth table has two admissible rows and zero survivors.

Focused QA passed:

```text
py_compile on all eight scripts:                        PASS;
Ruff on all eight scripts:                              PASS;
tracked diff whitespace check:                          PASS;
new-package trailing-whitespace scan:                   PASS.
```

The scripts are replay evidence for dependency identity and exact algebra;
the written, reviewed characteristic-zero arguments remain the proof.

## 8. Accepted boundary

```text
fixed equality-five (4,2) representative:               ASSUMED;
exact ordered local triples and full Delta_3 targets:    ASSUMED;
same-mode low incidences:                                EXCLUDED;
three- and four-low diagrams:                            EXCLUDED;
exactly-two-low reduction:                               REVIEWED/PINNED;
zero high-high pairing leaf:                             EXCLUDED;
nonzero E_22 high-high pairing leaf:                     EXCLUDED;
exact extension of the displayed fixed pair:             EXCLUDED;

transport to equality-five orbit (4,1):                  NOT PROVED;
transport to equality-five orbit (3,1):                  NOT PROVED;
arbitrary equality-five normalization:                   NOT PROVED;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```
