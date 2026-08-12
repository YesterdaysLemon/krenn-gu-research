# Hostile review of the beta-three binomial-sublattice port-sign dichotomy

## Verdict and immutable pins

This read-only hostile review accepts
[`MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_FIXED_COMPLETION_BINOMIAL_SUBLATTICE_PORT_SIGN_DICHOTOMY_THEOREM.md`](../../claims/arbitrary-order/MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_FIXED_COMPLETION_BINOMIAL_SUBLATTICE_PORT_SIGN_DICHOTOMY_THEOREM.md)
at exact core commit

```text
98b7c83f7d04d63d18cdb4474e25f717edbf410a
```

with the following committed LF-normalized Git-byte SHA-256 pins:

```text
theorem:
82c4aeab65897e927292d93caeef8228524656f5e1d2835644e8d412bcee7588

primary verifier:
69bc74958f13b9e2eb58a4fce52400e64351d39432ed8cec1a18bbf0083f3e88

independent audit:
779cee712881d458acde517d93dd032cc500912ff722bc902c3188eaa95061b4
```

The review found no P0, P1, P2, or P3 defect. The result is an exact
conditional characteristic-zero interface theorem. It does not prove the
lattice containment, the fixed completion, existence of a suitable
binomial core, or exclusion of the simultaneous all-bridge branch. The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Accepted conditional implication

The theorem starts from the A6 fixed-completion block

```text
p_A6=1+X^u1+X^u2+X^u3
```

inside one complete mixed multidegree. Its branch-specific physical
cancellation supplies the additional equation `p_A6=0`. The new hypothesis
is the integral containment

```text
L_A6=<u1,u2,u3>_Z subset L_bin
```

for one parity-consistent U7F binomial core. This is actual lattice
membership, not rational-span containment, and is not derived by the
theorem.

The binomial core has one fixed sign character `rho_bin`. In the original
non-untwisted presentation, `X^l=rho_bin(l)` modulo the binomial-core ideal
for every `l in L_bin`. Hence the A6 polynomial reduces to the single scalar

```text
s=1+rho_bin(u1)+rho_bin(u2)+rho_bin(u3).
```

Because every `ui` has zero class in `L_mu/L_bin`, this scalar is the same on
every later U7F torsion-character sheet. The eight sign rows in the evidence
are exhaustive alternatives for the one realized restriction
`rho_bin|L_A6`; they are not eight simultaneous sheets.

## 2. Global scalar unit versus balanced branch

If `s` is nonzero, it is an invertible complex scalar and

```text
(J_bin,p_A6)=A_mu.
```

Faithful Laurent extension carries this unit conclusion to the full physical
Laurent ring. This is a global no-solution conclusion for the explicitly
stated fixed-completion branch, not merely the death of one torsion sheet.
It does not make `J_bin` alone a unit and does not apply away from the branch
where `p_A6=0` is known.

If `s=0`, exactly two of the four signs are positive and two are negative,
and `p_A6` already belongs to `J_bin`. Adjoining it changes neither the
binomial-core ideal nor its quotient. Additional complete target equations
may nevertheless exclude this balanced branch.

The original/untwisted orientation was checked explicitly: selected
equations are `1+X^r=0`, so `X^r=-1`, while the U7F untwisting maps them to
`1-X^r`. The theorem uses the former sign character consistently.

## 3. The Q/C^2 nonzero-port locus

With one matching from the first A5 doubleton as reference, the two
block-restricted port polynomials are

```text
q_x=1+X^u1,
q_y=X^u2+X^u3.
```

A5 and A6 supply the load-bearing pointwise facts that both port sums are
nonzero and are exact negatives. In a balanced sign restriction, both are
nonzero exactly when signs are constant inside each doubleton and opposite
across the two doubletons. Thus exactly one of the three balanced partitions
survives.

For either misaligned partition, both port polynomials lie in `J_bin`, so

```text
(J_bin:(q_x q_y)^infinity)=A_mu.
```

This is correctly presented as a no-solution result on the inherited
nonzero-port locus. It is not an unsaturated unit statement. Conversely, the
aligned unimodular control has signs `(+,+,-,-)` and `q_x=2`, `q_y=-2`
modulo `J_bin`, so localization preserves the proper parity-consistent ideal.

## 4. The Q/Q boundary and sharpness controls

Every A6 `Q/Q` route port inside the block is a nonzero singleton. Therefore
these ports select none of the three balanced sign partitions. All three
remain live absent another complete target equation or structural input.

The primary verifier realizes both sides sharply:

- `r_i=u_i` gives a parity-consistent core with signs `(1,-1,-1,-1)`,
  scalar `-2`, and inverse `-1/2`;
- `r1=u2`, `r2=u3`, `r3=u1+u2` has determinant `+1`, gives signs
  `(1,1,-1,-1)`, and leaves the Q/C^2 port sums `+2,-2`.

These are exact free-lattice controls, not complete physical matrix-unit
tables or all-bridge witnesses.

## 5. Evidence and independence

The primary verifier directly enumerates all eight possible sign
restrictions, distinguishes the five scalar-unit cases from the three
balanced cases, checks the fixed Q/C^2 doubleton partition, preserves all
three Q/Q balanced cases, and verifies both explicit integer-lattice
controls.

The independent audit imports neither repository code nor the primary. It
uses a separate bitmask-character representation of `Hom(Z^3,{+1,-1})`,
checks multiplicativity on positive and negative exponent boxes, evaluates
the block and port multiples, and independently reconstructs the same
three-partition boundary. The two implementations therefore differ in
representation and derivation rather than only filename or random seed.

Both are bounded QA for the four-term interface. The arbitrary theorem is
the written quotient and port-locus proof. Exact replays passed:

```text
python -I -B claims/arbitrary-order/verify_matrix_unit_all_bridge_beta_three_fixed_completion_binomial_sublattice_port_sign_dichotomy.py
python -I -B claims/arbitrary-order/audit_matrix_unit_all_bridge_beta_three_fixed_completion_binomial_sublattice_port_sign_dichotomy.py
uvx --from ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_matrix_unit_all_bridge_beta_three_fixed_completion_binomial_sublattice_port_sign_dichotomy.py claims/arbitrary-order/audit_matrix_unit_all_bridge_beta_three_fixed_completion_binomial_sublattice_port_sign_dichotomy.py
```

## 6. Scope and severity audit

The exact severity verdict is

```text
P0: none
P1: none
P2: none
P3: none
```

The theorem does not infer a fixed completion, integral containment, a
binomial complete fibre, a universal target generator, or a physical
witness. It does not turn Q/C^2 port localization into an unsaturated unit,
and it does not exclude balanced Q/Q. It has no Larry/A3R, S2N, or S2O
conclusion. The simultaneous all-bridge branch and global Krenn--Gu
conjecture remain **UNRESOLVED**.
