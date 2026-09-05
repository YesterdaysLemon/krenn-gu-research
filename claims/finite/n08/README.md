# Eight-vertex packages

The [maximum-root-one exclusion](EIGHT_VERTEX_MATRIX_UNIT_EXCLUSION_THEOREM.md)
rules out every complete nonzero ternary matrix-unit source at order eight, with
arbitrary complex weights and endpoint colours. Its complete eighteen-case
scaffold cover, 39 exact algebraic cuts, and eighteen independently checked
UNSAT certificates are supplied in the [replay package](r1-source-certificate/README.md).
Every hypothetical ternary eight-vertex witness therefore has maximum root size at
least two. This is not an arbitrary eight-vertex or arbitrary-order exclusion.

The [complete two-root common-coordinate exclusion](TWO_ROOT_COMMON_COORDINATE_COMPLETION_THEOREM.md)
rules out the full GHZ source over C at maximum torus-root cardinality two
when both physical root incidences at every outside port share a coordinate
column. No root-block rank assumption remains: the prior
[rank-at-least-two proof](TWO_ROOT_COMMON_COORDINATE_EXCLUSION_THEOREM.md),
the [rank-one proof](TWO_ROOT_COMMON_COORDINATE_RANK_ONE_EXCLUSION.md), and
the [zero-block proof](TWO_ROOT_COMMON_COORDINATE_ZERO_EXCLUSION.md) form an
exhaustive cover. The last uses a supplied, independently checked
[Boolean certificate](two-root-zero-source-certificate/README.md).
General incidence patterns and unrestricted eight-vertex witnesses remain
open.

The [invertible-root joint-kernel boundary](TWO_ROOT_JOINT_KERNEL_BOUNDARY_THEOREM.md)
uses the full source to go beyond common-column incidences. At every
invertible physical edge of an n=8/max-r=2 witness, some outsider must have
joint kernel zero or a coordinate axis. Its proof supplies one actual binary
common-column anchor per colour pair before using a mixed 2D/1D cofactor
argument. The residual kernel types and lower-rank root edges remain open.

The [six-diagonal-leg source reduction](TWO_ROOT_DIAGONAL_LEG_COMMON_PLANE_REDUCTION_THEOREM.md)
handles paired invertible root stars with complementary diagonal unit legs.
It forces three inactive image planes on at least one shore to coincide,
and forces the outside hafnian to vanish when that shore is inactive and
the opposite shore is fully open. The full corrected cofactor equations
are retained. At maximum root cardinality two, adjacent degree-four
vertices in the invertible-edge graph supply this root configuration.
For arbitrary outside blocks its coincident-plane source system remains open.

The [complete diagonal-leg source exclusion](TWO_ROOT_DIAGONAL_LEG_SOURCE_EXCLUSION_THEOREM.md)
closes the configuration when the six physical AA/BB edges are nonzero
matrix units. One uniform cofactor contradiction joins the exhaustive
three-, two-, and one-coordinate normal cases, retaining all opposite
plane configurations and all AB-normal terms. At maximum root cardinality
two, invertible two-edge paths supply the required units. Consequently
the invertible-edge graph has no adjacent degree-four vertices. Other
eight-vertex configurations and the global conjecture remain open.

The nine Stage 28 claim documents have distinct support and case-cover
hypotheses:

- [`EIGHT_VERTEX_16EDGE_CERTIFICATE.md`](EIGHT_VERTEX_16EDGE_CERTIFICATE.md)
- [`EIGHT_VERTEX_17EDGE_CERTIFICATE.md`](EIGHT_VERTEX_17EDGE_CERTIFICATE.md)
- [`EIGHT_VERTEX_4REGULAR_CERTIFICATE.md`](EIGHT_VERTEX_4REGULAR_CERTIFICATE.md)
- [`EIGHT_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md`](EIGHT_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md)
- [`EIGHT_VERTEX_DEGREE3_E19_CERTIFICATE.md`](EIGHT_VERTEX_DEGREE3_E19_CERTIFICATE.md)
- [`EIGHT_VERTEX_DEGREE4_FRONTIER.md`](EIGHT_VERTEX_DEGREE4_FRONTIER.md)
- [`EIGHT_VERTEX_DOUBLE_C4_FAMILY_CERTIFICATE.md`](EIGHT_VERTEX_DOUBLE_C4_FAMILY_CERTIFICATE.md)
- [`EIGHT_VERTEX_ENTRY84_BOUNDARY.md`](EIGHT_VERTEX_ENTRY84_BOUNDARY.md)
- [`EIGHT_VERTEX_FULL_SINGLETON_FAMILY_CERTIFICATE.md`](EIGHT_VERTEX_FULL_SINGLETON_FAMILY_CERTIFICATE.md)

Stage 33 added the mixed-lifecycle
[`degree-six-kotzig-port/`](degree-six-kotzig-port/) package and preserved the
withdrawn overstrong record under
[`history/withdrawn-balanced-all-bridge-set-tree/`](history/withdrawn-balanced-all-bridge-set-tree/).
Neither is flattened into the nine live Stage 28 documents.

Their colocated scripts are the carriers named by those documents; several
shared support and Laurent providers live under `src/krenn_gu/`. Read each
document's status and boundary before using a carrier. The exact 18-edge
degree-four case remains open where the ledger says it is open, and the union
of these packages is not silently promoted to an arbitrary-order result.

The global Krenn-Gu conjecture remains **UNRESOLVED**. Return to the
[finite package index](../README.md).
