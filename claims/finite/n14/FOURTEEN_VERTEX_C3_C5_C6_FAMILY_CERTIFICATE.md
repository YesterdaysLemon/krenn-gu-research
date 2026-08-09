# Order-14 `C3+C5+C6` equality-family certificate

## Theorem

There is no order-14, three-colour equality-architecture witness whose
full-block 2-factor has cycle type `C3+C5+C6`.

This is a complete finite theorem for that factor type.  It is not a
proof of the other order-14 factor types or of the global Krenn--Gu
conjecture.

## Exact exhaustion

Fix the labelled full factor

```text
C3 = (0,1,2)
C5 = (3,4,5,6,7)
C6 = (8,9,10,11,12,13).
```

The three singleton colour classes must be pairwise edge-disjoint perfect
matchings in the complement of this factor.  The exact enumeration has:

```text
eligible singleton perfect matchings             44,220
individually one-term-free factors                 2,820
two-edge one-term sets                               270
matching forks of size 3                           5,310
matching forks of size 4                          73,350
matching forks of size 5                         160,920
size-3-fork-free safe factors                      1,020
full-factor orbits of those factors                    5
compatible second factors across representatives     960
ordered thirds before size-4/5 filtering          47,936
ordered supports after size-4/5 filtering            156
colour-unlabelled supports                            78
full-factor/colour orbits                               9
```

The one-term sets give a supported monomial in a forbidden amplitude.
Each matching fork satisfies the arbitrary-order cancellation-transport
lemma in [`MATCHING_FORK_TRANSPORT_LEMMA.md`](../../../MATCHING_FORK_TRANSPORT_LEMMA.md).
Those elementary obstructions eliminate all but the final 156 ordered
supports.

## Signed-lattice closure of the nine residual orbits

Every residual orbit representative has 465 skeleton perfect matchings.
Its forbidden binomial amplitudes generate an exact signed Laurent
lattice of rank 37.  In each of the nine cases, only three basis
relations are needed:

```text
target pair exponent difference = r_i + r_j - r_k.
```

Every binomial relation has value `-1`, so the coordinate sum
`1+1-1` is odd and the target pair has ratio `-1`.  The pair therefore
cancels in a forbidden trinomial, leaving its third active matching as
one supported nonzero monomial.  This is impossible.

The target equation is 6636 in six orbits and 6742 in three orbits.
The individual analysis and replay manifests are:

```text
tmp/fourteen_vertex_c3_c5_c6_fork5_orbit0_signed_lattice.json
...
tmp/fourteen_vertex_c3_c5_c6_fork5_orbit8_signed_lattice.json

tmp/fourteen_vertex_c3_c5_c6_fork5_orbit0_signed_lattice_verified.json
...
tmp/fourteen_vertex_c3_c5_c6_fork5_orbit8_signed_lattice_verified.json
```

Every replay manifest contains `"verified": true`.

## Independent replay

`verify_fourteen_vertex_c3_c5_c6_family.py` deliberately reconstructs the
finite proof by a different route.  It:

- enumerates singleton factors using a separate bitmask recursion;
- computes fixed-cycle completions with an independent induced-factor
  recurrence;
- enumerates size-3, size-4, and size-5 matchings by first choosing their
  vertex sets and then pairing those vertices;
- regenerates and exactly compares all 239,580 matching-fork masks and all
  270 one-term masks;
- redoes the five factor orbits and the `47,936 -> 156 -> 9` support
  quotient;
- verifies that the nine independently replayed signed-lattice manifests
  cover exactly the nine residual orbits;
- checks the raw and canonical JSON hash chain.

Run:

```text
python claims/finite/n14/verify_fourteen_vertex_c3_c5_c6_family.py
```

The final audit is:

```text
tmp/fourteen_vertex_c3_c5_c6_family_verified.json
```

and contains:

```json
{
  "verified": true,
  "status": "all_c3_c5_c6_equality_supports_closed"
}
```

## Pinned hashes

```text
raw SHA-256

D3DFF2BB28342952A2C05A7D23B378317B9C09436A52166472CCFCC6015D58DF
  tmp/fourteen_vertex_c3_c5_c6_obstruction_catalogue.json

7CE270F480089F09CEFC83937630A746CFB92B12F4B412BCD4B352DA812B22E2
  tmp/fourteen_vertex_c3_c5_c6_family_enumeration.json

A705B5C6941E0768205219972D527B17D532781AB68CEF2C8689F5ABD9F82D63
  tmp/fourteen_vertex_c3_c5_c6_fork5_survivor_orbits.json

E01E74764B5891CFC971E1FE43AC6212A6800B0A3D52AE01FEA8C537F080915F
  tmp/fourteen_vertex_c3_c5_c6_family_verified.json
```

The obstruction catalogue's canonical-JSON SHA-256 is:

```text
edfba78aa7a4b67ff709a4e846b0011170a7d20bc2c2577dfcd6b3f3e034e709
```
