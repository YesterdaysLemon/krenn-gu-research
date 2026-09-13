# Full-model recursive cancellation: parent diagnostic

Global status: **UNRESOLVED**. This is a separate full-model investigation,
not an extension of the all-diagonal RZP finite claim.

## Parent obligation and consumer

For every complex ternary pair-source system on eight vertices with matching
tensor equal to GHZ, derive an incompatible system of exact cancellations.
Success would exclude the entire eight-vertex parent without assuming an
invertible edge or a particular maximum-root branch. A Boolean support survivor
instead tests the strength of this necessary abstraction; it is not a witness.
An UNSAT solver status needs an exhaustive witness-to-encoding bridge and
independently checked certificate before becoming a finite exclusion.

This attempt synthesizes two existing mechanisms:

1. The [three-colour hyperplane-annihilation theorem](../../claims/arbitrary-order/THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md)
   supplies a genuine column-killer edge for every vertex and colour.
2. Recursive Laplace identities couple all subset coefficients back to the same
   physical entries, with truthful edge-times-cofactor supports. A zero result
   cannot have exactly one surviving term.

The downstream consumer is the remaining full eight-vertex case. The experiment
does not identify the root parameter with invertibility, impose diagonal blocks,
or treat separately chosen cofactor tensors as physical data.

## Source-preserving Boolean bridge

For every even subset A and colour word w on A let s(A,w) indicate the nonzero
coefficient of the original induced pair-source system. For a physical entry
g(uv,w_u,w_v), introduce

```text
b(A,w,uv) iff g(uv,w_u,w_v) and s(A-{u,v}, w restricted to A-{u,v}).
```

The empty coefficient is one; two-vertex coefficients alias physical entries.
For every vertex expansion, require a nonzero result to have a nonzero term and
a zero result not to have exactly one. At the full subset, precisely the three
constant words are nonzero. Their values need not be represented: nonzero pure
coefficients can be independently normalized by diagonal scaling at one vertex.

The killer at (v,c) restricts the column indexed by **the neighbour's** colour c:
W(v,u)[:,j]=0 for j!=c, while W(v,u)[:,c] is nonzero. The reverse orientation uses
the transpose. Three selected killers at v have distinct neighbours, since a
nonzero block cannot have two different unique nonzero columns. Relabelling the
vertices lets the selected neighbours of vertex zero be 1,2,3 for c=0,1,2.
This imposes neither a row colour at vertex zero nor a diagonal entry.

The [implementation](../../src/krenn_gu/recursive_tensor_support.py) is a new
encoder: it does not alter the frozen all-diagonal source or silently redefine
AP'. Coefficients indexed by different words have shared physical entries, not
independent source matrices.

## Sharp controls and no-go boundary

- The genuine four-vertex GHZ construction must satisfy the complete model,
  including the chosen root killer symmetry.
- Arbitrary exact integer blocks must satisfy the recurrence when the target and
  killers are disabled. This checks the coefficient bridge, not nonexistence.
- Without killers a dense Boolean assignment satisfies every recurrence and
  target support at n>=4: all entries and proper cofactors can be nonzero while
  mixed full coefficients are zero. This is not an exact weighted realization.
- The [pure-matching scaffold no-go](../../claims/arbitrary-order/PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_THEOREM.md)
  prevents promoting killer/annihilation gates alone into a global proof. The new
  diagnostic also imposes every full mixed coefficient zero, retaining original
  source recursion. It does not assume that this suffices.

No live-frontier update is made: this is an exploratory parent attempt, with no
new finite exclusion or global implication promoted.

## First survivors and their exact cancellation obstructions

The encoder returned SAT at n=6 and n=8, respectively 20,394 variables / 102,009
clauses and 556,971 variables / 2,825,448 clauses. Both complete assignments were
checked against every generated clause. This refutes sufficiency of this Boolean
model, not the graph conjecture. All six encoder unit tests pass, including
complete 512-block killer truth tables in both orientations and sixteen actual
integer-source controls at orders four and six.

The first physical supports have 63 and 111 nonzero entries. Among complete mixed
word fibres, 477 and 390 respectively have exactly two nonzero matching terms.
After deduplication these give 477 and 66 Laurent binomial relations. Their
integer kernels have no odd-sign dependency. Thus an odd-circuit-only test does
not exclude these supports.

However, the binomials impose restrictions on the larger fibres. At both orders,
a complete three-term mixed fibre has two terms forced to be negatives by three
binomial relations. The remaining monomial is nonzero, so the mixed coefficient
cannot vanish. This is a quotient-singleton contradiction, despite consistency
of the binomial subsystem itself.

The implementation is [full_tensor_cancellation.py](../../src/krenn_gu/full_tensor_cancellation.py).
For a signed integer row lattice L, Smith form gives a coset signature in Z^E/L,
retaining torsion residues. It also gives the sign of a monomial relative to its
chosen coset representative. Group a complete fibre by these signatures:

- if a mixed fibre has exactly one group with nonzero signed coefficient sum,
  it cannot vanish;
- if all groups of a pure fibre cancel, it cannot be nonzero.

The discovery calculation does not serve as the certificate checker. Each used
monomial transport includes an integer combination of the original complete
binomial fibres. A separate replay directly adds exponent vectors and checks
signs, rebuilds every complete matching fibre, verifies the cancellation groups,
and reconstructs the guard clause. Modified origins, terms, signs, coefficients,
groups and cuts are rejected by tests.

For each used fibre, the guard requires every entry of every live matching to
stay nonzero and one selected zero entry of every dead matching to stay zero.
The learned clause negates their conjunction. An additional cancellation term
can escape by activating its selected zero blocker. No phase constraint is
asserted without a complete-fibre guard.

The first n=6 and n=8 cuts have 29 and 30 literals. The first n=8 refinement
survives this cut with 107 nonzero entries, and the complete full-word binomial
quotient finds no contradiction. This is the next diagnostic input, not a weight
realization and not an assertion that the smaller subset equations are mutually
consistent. The six-vertex loop also finds pure-vanishing cuts, so both checks
are operational. No finite UNSAT certificate has been claimed by this loop.

Raw initial CNF hashes (ASCII DIMACS with the generating checkout's CRLF):

```text
n=6 b734759d2ceedf63d70e4b2c807fb9668883f17e04ee63cd8c9d18646d76e5c2
n=8 d282de97da78f97bf3b74c82bd5ad3f2289585d62d6d8682f15c45b68993b802
```

Local payloads live under ignored `tmp/full-recursive-n6-quotient-loop` and
`tmp/full-recursive-n8-quotient-loop`. They have not been publicly distributed.
No independent external review of this new delta has yet been completed.
