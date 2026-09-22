# Independent review of resource-simple transition closure

Date: 2026-09-22. Verdict: **PASS for the conditional family theorem**.

The owner is
`claims/arbitrary-order/RESOURCE_SIMPLE_TRANSITION_CLOSED_EXCLUSION.md`.
The proof assumes at most one resource of each color per block, crossings
only within blocks, endpoint crossing supply, no physical scalar selfloops,
nonzero actual weights, and two-exit closure. No crossing-degree upper bound
is needed; no source-driven block or closure reduction is claimed.

For a base color a and a simple labeled transition cycle, each selected
foreign state has a unique incoming predecessor. Its defining crossing
puts it in the predecessor's a-resource block. The converse follows from
the unique a-resource in that block. Thus a block with r cycle endpoints
has 2-r retained states and r distinct foreign arrivals. Blocks omitting
a have none. Physical overlap does not change this state partition.

For r=0,1,2 the selected pair has respectively its protected edge, defining
crossing, or closure edge. Each is one ordinary scalar entry; selected
physical endpoints are distinct. Every active block has exactly one
matching edge, yielding a unique global nonzero product.

For mixedness, if a digraph has no proper directed cycle, fix any of its
Hamilton cycles. An arc not following its successor would close a proper
cycle, so all arcs follow the same successor. If there were different
foreign labels among these arcs, a mixed Hamilton labeling would exist.
Hence failure at color a forces a single label b. Reversing those scalar
crossings supplies a-labeled outgoing arcs at every vertex for base b.
If b also fails, its exceptional label must be a. All three colors cannot
be partitioned into such pairs. This checks the all-arc argument, including
parallel labeled arcs and auxiliary loops.

The negative control independently recounts 12 states, six degree-one
crossings, and the Hamilton word 2112 with zero compatible edges. It refutes
only closure-free use of the universal cycle-balance mechanism, not the
possibility of another unique mixed word in that array.

The positive companion independently constructs:

- A local K3,3 triple block with crossing degree two and no closure failure.
- Its all-diagonal triangular-prism mutation, with six closure failures.
- Six triple blocks on three protected K4s, all states of crossing degree
  two, with unique mixed words including one using r=2 in three blocks.
- A hybrid with two triple and six pair blocks, including r=0,1,2 cases.
- A two-vertex physical-overlap block with all six mixed words unique.

It directly enumerates physical perfect matchings of these explicit words.
The positive controls corroborate scope and closure necessity; the written
proof supplies all orders. Neither script imports the other or project
scientific code. There is no external matching theorem or solver dependency.

The scratch proof accepted after making its arrival converse explicit had
SHA-256 `DA4C19A19D01394C3AA8F394013506E59B94E748FED5E5D049AC3D21475FDA44`;
the independent audit had
`5ECC765EDE2B595C8E5A96C075E2E3A521DC56B571F96266DB23269550EF17D9`.
The tracked owner contains the complete proof, so those scratch artifacts
are not required for verification. Review was by separate agents in one
research session; no independent human-referee or formal-kernel claim is made.


## Closure-free existential-cycle control

A separate no-import audit reconstructed the literal three-K4 fixture from
JSON. It found 18 protected resources, 18 crossing entries and 36 states
of crossing degree one, with all crossings hollow. Each D_a has exactly
the one functional cycle listed by the owner, up to rotation; every cycle
contains one double-hit resource with nonadjacent exits. Each associated
physical word has zero supported matchings. Exhaustive term reconstruction
gave 364 terms on 342 words and 317 unique mixed words; 000000001111 has
one matching. This verifies the control's exact route-only boundary.

The cyclewise iff criterion follows by the same exact block balance as
the sufficient theorem. The degree-one macro factorization and strong
component-digraph counting proof are also sound; they are an alternative
derivation inside the already excluded sparse family, not additional
degree-two progress. A full-source supplier is still absent.

The reviewed scratch owner hash was
B5E69FE1A963A8ACCA238F877F58A5959A2A3E93A7682B43B14BDB1C0C3DF474;
the independent report hash was
B8862142EDCCDF3B5AFD68ED23405F35548E67FA162293321FFDE7D300C709AA.
The fixture SHA-256 is
0700ADDB50405690724141637D92E34C667ED90460F7FE66F3E5C22F1708FE03.
The durable independent checker is audit_resource_triple_bad_exit.py;
only its adjacent fixture path was changed on promotion.


## Degree-two triple polynomial

The local triple identity was accepted only after explicitly requiring six
distinct physical endpoints. The corrected owner hash is
257B7F5786640A1681BFB05772987CFCC10236C1C49D3F91FE7ECE22A58D091D.
Hollowness in the protected K4 application supplies that disjointness when
every resource pair has a crossing bijection.

Independent recursive matching enumeration gives two terms on every
binary face; four terms and no crossing-only matching for the triangular
prism; and six terms, including two crossing-only matchings, for K3,3.
The latter two matchings partition the six crossing edges, proving their
normalized product is sigma_AB*sigma_AC*sigma_BC. Three locally vanishing
prism faces therefore force its fully selected local factor to -2.
Another block may still zero the global row, so no isolation or broader
source exclusion follows. The independent report hash is
9B41355AF4A5814881C058B1BA88A48E8BC715E72E501112084DE954DF3100CE.
