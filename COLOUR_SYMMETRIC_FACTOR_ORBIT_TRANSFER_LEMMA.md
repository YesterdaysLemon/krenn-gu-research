# Colour-symmetric factor-orbit transfer

## Lemma

Fix one full-factor type in the three-colour equality architecture and one
explicit connectivity regime.  If no witness can have its colour-0
singleton perfect matching in a full-factor automorphism orbit `O`, then
no witness can have *any* of its three singleton perfect matchings in
`O`.

## Proof

The target tensor

```text
e_0 tensor ... tensor e_0
+ e_1 tensor ... tensor e_1
+ e_2 tensor ... tensor e_2
```

is invariant under a common permutation of the three colour coordinates
at every vertex.  Apply a colour permutation that moves the chosen
singleton factor into colour position 0.  It preserves:

- the full-factor cycle skeleton;
- the support graph and its vertex connectivity;
- every perfect-matching amplitude equation; and
- membership of the moved factor in its orbit under full-factor vertex
  automorphisms.

The permuted object would therefore be a witness with its colour-0 factor
in `O`, contradicting the assumed orbit theorem.

## Order-14 `C4+C4+C6` consequence

The independently replayed minimum-connectivity-three frontier plus the
targeted orbit-8 certificate exclude 66 of the 93 first-factor orbits.
Consequently each of the three singleton factors in any remaining
candidate must lie among the same 27 orbit classes:

```text
9--11, 13--16, 22, 36--41, 44--51, 54--55, 57, 63, 68
```

The factor census contains 44,196 eligible perfect matchings.  Exactly
38,500 lie in the 66 excluded orbits, leaving 5,696 allowed factors.
Transport to all three colour roles produces 115,500 width-seven factor
no-goods.

The augmentation and its independent audit are:

```text
python augment_fourteen_vertex_c4_c4_c6_with_colour_symmetric_orbit_exclusions.py \
  --base-cnf tmp/fourteen_vertex_c4_c4_c6_rule_sat_late_combined_v7_orbit8_partial2_minimal_circuits_kappa3_symbinomial3.cnf \
  --output-cnf tmp/fourteen_vertex_c4_c4_c6_colour_symmetric_orbit_exclusions.cnf \
  --output tmp/fourteen_vertex_c4_c4_c6_colour_symmetric_orbit_exclusions_augmentation.json

python verify_fourteen_vertex_c4_c4_c6_colour_symmetric_orbit_exclusions.py \
  tmp/fourteen_vertex_c4_c4_c6_colour_symmetric_orbit_exclusions_augmentation.json \
  --output tmp/fourteen_vertex_c4_c4_c6_colour_symmetric_orbit_exclusions_verified.json
```

This is a conditional finite reduction inside the stated order-14
equality architecture.  It is not a proof of the complete
`C4+C4+C6` family or of the global Krenn--Gu conjecture.
