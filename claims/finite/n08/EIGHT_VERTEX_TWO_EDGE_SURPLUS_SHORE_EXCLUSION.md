# Eight-vertex two-edge surplus-shore exclusion

## Status and exact scope

**Proved conditional physical-source exclusion over every field**, with an
independent exact audit. Fifteen named zero entries and two named nonzero entries
exclude an eight-vertex normalized ternary GHZ matching tensor. All other
physical entries are arbitrary, including the two base entries below. No proper
cofactor is assigned a value or assumed nonzero. No division, genericity, or
boundary relation is used. This excludes the preserved 134-entry Boolean
projection as a possible physical support, not the unrestricted eight-vertex
parent. Global Krenn–Gu remains **UNRESOLVED**. No Lean formalization is supplied.

The source-coupled degree-six computation discovered the identity after the
complete declared degree-five module failed. The underlying majority-shore
principle is already owned by [the internal-edge ideal hierarchy](../../arbitrary-order/MAJORITY_SUBSET_INTERNAL_EDGE_IDEAL_HIERARCHY.md)
and [the five-root boundary-incidence theorem](../../arbitrary-order/EIGHT_VERTEX_FIVE_ROOT_THREE_COLOUR_BOUNDARY_INCIDENCE_CODIMENSION_THREE_THEOREM.md).
The new result is an explicit physical guard and four-equation certificate.

## The physical identity

Use vertices 0 through 7, colours 0 through 2, and the repository's one-based
lexicographic physical entry numbering. Set

```text
a=g172=W35[0,0], b=g174=W35[0,2],
c=g244=W67[0,0], d=g245=W67[0,1].
```

Impose exactly the fifteen zeros

```text
163,181,190,191,199,201,208,217,218,226,232,235,236,241,242.
```

Equivalently:

```text
W34[0,0]=W36[0,0]=0;
W37[0,0]=W37[0,1]=0;
W45[0,0]=W45[0,2]=W46[0,0]=0;
W47[0,0]=W47[0,1]=0;
W56[0,0]=W56[2,0]=0;
W57[0,0]=W57[0,1]=W57[2,0]=W57[2,1]=0.
```

Require only `b*d!=0`. Let `T_ij` be the full matching coefficient with vertex
5 coloured `i in {0,2}`, vertex 7 coloured `j in {0,1}`, and all others 0.
Write `P_ij=T_ij-1` for `ij=00`, and `P_ij=T_ij` otherwise. Then

```text
b*d = -a*c P_21 + a*d P_20 + b*c P_01 - b*d P_00.       (1)
```

This is an integer polynomial identity after the fifteen zero substitutions.
The full coefficients have physical degree four and the multipliers degree
two. At a GHZ witness all four P vanish, contradicting `b*d!=0`.
For a diagonal target with nonzero base amplitude `lambda_0`, replace the
left side by `lambda_0*b*d`; the same obstruction holds.

## Human proof and shared-source structure

Take `S={3,4,5,6,7}`. Across the four words, only edges 35 and 67 can contribute
inside S. Every perfect matching uses an internal edge of S: the three outside
vertices cannot match all five vertices of S.

Partition matching contributions into those using 35 only, 67 only, and both.
There are actual shared source polynomials `H,U_j,V_i` such that

```text
T_ij = a_i*c_j*H + a_i*U_j + c_j*V_i,
(a_0,a_2)=(a,b), (c_0,c_1)=(c,d).                     (2)
```

Here H is the induced four-vertex hafnian on `{0,1,2,4}`. The U and V terms
are the matching sums on the corresponding remaining six vertices with the
other distinguished edge excluded. They are not independent variables.
Applying `(b,-a)` to the first varying slot and `(d,-c)` to the second kills
every term of (2), giving `bd T_00-bc T_01-ad T_20+ac T_21=0`, hence (1).

Equivalently the covectors on S are `e0*,e0*,b e0*-a e2*,e0*,d e0*-c e1*`.
They kill every internal edge contraction but evaluate the selected pure target
to `bd`. This is the explicit connection to the existing majority theorem.

The same proof works if the two covering edges share their fixed endpoint
(35 and 37), and when the two nonzero alternate colours agree. These give
four types: disjoint/shared-centre times equal/distinct alternates. Vertex
permutations and one common colour permutation cover this defined two-moving-
leaf family. This is not a classification of all possible majority annihilators.

## Exact evidence and controls

The [certificate fixture](../../../tests/fixtures/eight_vertex_two_edge_surplus_shore.json)
contains the fifteen zeros, two nonzeros, four words, signed multipliers, and
target monomial. The [primary replay](verify_eight_vertex_two_edge_surplus_shore.py)
uses sparse physical matching polynomials. The
[independent audit](audit_eight_vertex_degree6_source_134.py) imports no primary
scientific implementation, checks bitmask matching enumeration against the
permutation quotient, and reconstructs all 252 entry IDs and all 105 matchings.

With only the fifteen zeros each source has 15 terms; the 60 signed products
cancel in 24 pairs and three groups of four. The adjacent types have 12 terms
per source. On the original 134-entry projection the four term counts are
4,4,5,5. The audit checks wrong signs, omitted sources, the pure target term,
every individually removed zero, both required nonzero factors, and the
admitted `a=0`, `c=0`, and `a=c=0` boundaries. Removing any one zero destroys
this particular polynomial identity with the other entries arbitrary; this
does not assert globally minimal guards for every possible obstruction.

```text
python claims/finite/n08/verify_eight_vertex_two_edge_surplus_shore.py
python claims/finite/n08/audit_eight_vertex_degree6_source_134.py --fixture tests/fixtures/eight_vertex_two_edge_surplus_shore.json
python -m unittest -v tests.test_two_edge_surplus_shore
```

## Parent attempt and remaining obligation

The [resolution attempt](../../../docs/strategy/source-module-resolution-attempt-2026-09-14.md)
records the exact parent. Adding all four new orbits to the previous recursive,
killer, ratio-component and four physical-cut-orbit model gives 600,063 variables
and 4,708,644 clauses. A complete assignment was checked against every clause:
the Boolean occurrence implication remains false. The new orbit sizes are
20,160,20,160,10,080,10,080. The survivor is a different physical projection,
not a weighted witness. The next source-coupled calculation acts on that
survivor; neither this family nor the existing majority hierarchy is a proved
cover of the unrestricted parent.

Its [complete packed Boolean assignment](../../../tests/fixtures/eight_vertex_two_edge_parent_survivor.json)
uses 75,008 uncompressed bitset bytes (25,284 gzip bytes), preserving every
variable rather than only the physical projection. The
[parent tool](../../../tools/explore/probe_two_edge_shore_parent.py) supports
`--replay-assignment` to regenerate the exact hashed clauses and check this
assignment without a SAT solve. The later
[two-slice transfer](../../arbitrary-order/TWO_SLICE_SHARED_HAFNIAN_TRANSFER_OBSTRUCTION.md)
excludes its physical support with eighteen zeros and two nonzeros.

The [protected pure-matching scaffold no-go](../../arbitrary-order/PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_THEOREM.md)
already shows why majority tests alone cannot supply a global bridge.
The frontier delta is this explicit guarded exclusion and the elimination of
the previously preserved 134-entry support, with parent coverage still open.
