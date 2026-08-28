# Hostile review: four-deficient pair classes and probe-dependent four-port boundary

## Review target and verdict

Target reviewed:

`claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FOUR_DEFICIENT_PAIR_CLASS_AND_PROBE_DEPENDENT_FOUR_PORT_BOUNDARY_THEOREM.md`

Supporting artifacts reviewed:

`claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_four_deficient_pair_class_and_probe_dependent_four_port_boundary.py`

`claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_four_deficient_pair_class_and_probe_dependent_four_port_boundary.py`

**Verdict: PASS for the exact `GLS68` scope after two independent hostile
reviews and two finite replays.**  The result is conditional on the accepted
`GLS63` incidence/singleton theorems and the universal `GLS67` pair-class
theorem.  It proves a normalized necessary-profile census and rejects one
invalid receiver interface.  It does not exclude any of the `4,794`
surviving profiles.

The review began from a proposed exclusion of fifty-four fully ternary
profiles by the accepted six-vertex theorem.  Adversarial inspection found
that proposal unsound: the would-be complementary edge blocks depend on the
same probe variables that were being treated as open roots.  The exclusion
was retracted before acceptance.  The corrected theorem records the exact
interface failure and retains all fifty-four profiles as open.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Exact census scope

For four deficient labels, the six auxiliary labels split as

```text
|N|=4,       |P|+|U|=2.
```

The declared normalized convention orders the four deficient maps and the
nonaxis zero statuses, fixes one canonical placement of the `P/U` types, and
suppresses the pure-axis `X/Y` orientation.  Canonical keys then quotient
deficient-label and colour permutations and retain only the support, rank,
zero-count, and pure-count data.  They are not physical-witness orbits.

Both implementations exhaust the nine deficient types and four possible
nonaxis zero statuses.  The starting counts are

```text
p=0: 9^4*4^2 = 104,976;
p=1: 9^4*4   =  26,244;
p=2: 9^4     =   6,561.                              (1)
```

The hostile reviews checked that the first filter implements exactly:

- the `GLS63` exclusion of `|M_a|=4`, since a common colour would need at
  least three nonaxis zeros but `|U|<=2`;
- the nonempty-zero requirement for `|M_a|=3`; and
- the `R_a` missing-map conclusion when that zero set is a singleton.

The second filter implements the `GLS67` pair classes.  If an unzeroed
colour had `|M_a|>=3`, choosing a two-set inside `M_a` would force the whole
support to equal that two-set.  For every exact two-set class, both open
ranks meet the class size, a pure-axis label caps the size at one, no pure
axis caps it at two, and a singleton class cannot have two rank-two open
maps.

Both traversals return

```text
137,781 -> 20,778 -> 4,794,
50 canonical support/rank/zero-count keys.             (2)
```

The by-`p` rows are:

| `p` | start | after `GLS63` | after `GLS67` |
|---:|---:|---:|---:|
| 0 | 104,976 | 16,824 | 4,530 |
| 1 | 26,244 | 3,252 | 264 |
| 2 | 6,561 | 702 | 0 |

The two implementations separately report forty-five keys for `p=0`, five
for `p=1`, and the same zero-pattern totals.  They use different set and
integer-mask representations; they do not exchange serialized key sets.

## Ternary stratum

Exactly fifty-four profiles have

```text
p=0,       (|E_0|,|E_1|,|E_2|)=(0,0,0).             (3)
```

They occupy two canonical type keys:

```text
S_c,S_c,R_c,R_c: 18 normalized profiles;
S_c,S_c,R_c,T_c: 36 normalized profiles.             (4)
```

The remaining `4,740` profiles occupy forty-eight keys and have binary or
monocolour full-cross targets.  Equation (3) gives a fully ternary target,
but target support is not a proof that the source is a six-vertex matching
tensor.

## Receiver-interface failure

For a nonaxis label `u`, the exact contraction vector is

```text
k_u(z_0,z_1)=X_u(z_0,-) cross Y_u(z_1,-).            (5)
```

It has probe bidegree `(1,1)`.  With two nonaxis labels contracted, every
complementary two-port deck has bidegree `(2,2)`, while the deficient pair
companion has `(1,1)`.  The exact four-port pullback therefore has bidegree
`(3,3)`.

An honest six-vertex hafnian on the two roots and four deficient ports is
multilinear in those roots and has fixed edge blocks.  Its probe degree is
`(1,1)`.  The direct identification fails in both possible quantifier
orders:

1. Fixing `z_0,z_1` makes the cross products and decks fixed, but also
   evaluates the roots.  Only four physical ports remain open.
2. Freezing `k_u(z)` and reopening independent probes `x_0,x_1` no longer
   kills the companions incident with `u`; generally
   `X_u(x_0,-)(k_u(z))` and `Y_u(x_1,-)(k_u(z))` are nonzero.

Thus the exact object is a nonlinear same-source pullback of the original
eight-vertex hafnian, not the six-vertex graph required by the accepted
finite theorem.  This proves only that the displayed direct bridge is
invalid.  It does not rule out a future polarization, common-factor descent,
or different fixed-edge reconstruction.

The theorem's abstract three-term diagonal control was also reviewed.  It
is correctly labelled as an independently assigned pair/deck equation, not
a common-graph witness; arbitrary nonzero target scalars may be absorbed into
the selected factors.

## Repairs made during review

The accepted draft incorporates the following corrections:

1. The proposed `54`-profile six-vertex exclusion was withdrawn; the exact
   residual remains `4,794`, not `4,740`.
2. The support proof now says that `GLS67` first gives `|M_a|<=2`; the rank
   and singleton pure-companion constraints then force the ternary stratum's
   three supports to be two-sets.
3. The verification prose no longer claims that the independent programs
   compare exact serialized key sets.
4. The interface conclusion is scoped to the displayed direct
   reconstruction and does not exclude a different future descent.

## Replay evidence

The following commands passed in the isolated working tree:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_four_deficient_pair_class_and_probe_dependent_four_port_boundary.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_four_deficient_pair_class_and_probe_dependent_four_port_boundary.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_four_deficient_pair_class_and_probe_dependent_four_port_boundary.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_four_deficient_pair_class_and_probe_dependent_four_port_boundary.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_four_deficient_pair_class_and_probe_dependent_four_port_boundary.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_four_deficient_pair_class_and_probe_dependent_four_port_boundary.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_four_deficient_pair_class_and_probe_dependent_four_port_boundary.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_four_deficient_pair_class_and_probe_dependent_four_port_boundary.py
```

The two finite replays agree on (2), the fifty-key count, the zero-pattern
totals, the `54/4,740` split, the two ternary multiplicities, and the `(3,3)`
degree.  Compilation and Ruff checks pass.

Final review status: **PASS for `GLS68`; direct probe-dependent six-vertex
bridge invalid; all four-deficient survivors and the global Krenn--Gu
conjecture UNRESOLVED.**
