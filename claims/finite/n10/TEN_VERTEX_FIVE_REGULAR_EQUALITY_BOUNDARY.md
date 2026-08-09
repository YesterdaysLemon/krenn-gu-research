# Ten-vertex five-regular equality boundary

## Status

This is a finite structural and computer-assisted theorem for `n=10`,
`d=3`, a 5-regular 25-edge essential skeleton, and the 105-entry equality
boundary.  It is not a solution of the global Krenn--Gu conjecture.

**Theorem.**  No such 105-entry support realizes the Krenn--Gu target over
the complex numbers.

The exhaustive certificate covers 37,107 support orbits representing
779,297,500,800 labelled coloured supports.

## Why 105 entries force the enumerated architecture

Choose one generic-killer block for each of the 30 vertex-colour pairs.
Let `r`, `s`, and `t` count skeleton edges selected from both endpoints,
one endpoint, and neither endpoint.  Then

```text
2r + s = 30,
r + s + t = 25.
```

A reciprocal selected block has at most one supported entry, a one-way
selected block at most three, and an unused block at most nine.  Hence

```text
entries <= r + 3s + 9t = 45 + 4r <= 105.
```

Equality uniquely forces

```text
(r,s,t) = (15,0,10).
```

Thus there are fifteen reciprocal singleton blocks and ten full blocks.
The independently audited failure-hyperplane backup argument forces every
equality singleton to be diagonal.  Each vertex meets one singleton of each
colour, so the singleton colour classes are three perfect matchings.

On a 5-regular skeleton the singleton subgraph is cubic.  The ten full
blocks therefore have degree two at every vertex and form a spanning
2-factor.

## Exhaustion of the full factor

A 2-factor in a simple graph is a partition into cycles of length at least
three.  There are exactly five such partitions of ten:

```text
full factor   support orbits   labelled coloured supports   obstruction
C10                   23,204              491,794,208,640   3-binomial transport
C4+C6                  4,903              101,287,065,600   3-amplitude fork
C5+C5                  2,536               50,152,556,160   1-term amplitude
C3+C7                  5,558              118,737,964,800   1-term amplitude
C3+C3+C4                 906               17,325,705,600   1-term amplitude
total                  37,107              779,297,500,800
```

The family proofs are:

- [`TEN_VERTEX_C10_EQUALITY_CERTIFICATE.md`](TEN_VERTEX_C10_EQUALITY_CERTIFICATE.md);
- [`TEN_VERTEX_C4_C6_FAMILY_CERTIFICATE.md`](TEN_VERTEX_C4_C6_FAMILY_CERTIFICATE.md);
- [`TEN_VERTEX_ODD_FACTOR_EQUALITY_CERTIFICATE.md`](TEN_VERTEX_ODD_FACTOR_EQUALITY_CERTIFICATE.md).

## Independent aggregate audit

`verify_ten_vertex_five_regular_equality_boundary.py`:

1. checks the general three-colour entry-bound audit and its diagonal
   singleton backup result at full degree two;
2. independently reconstructs the unique `(15,0,10)` equality row;
3. enumerates all cycle partitions of ten and requires exactly the five
   types above;
4. requires `"verified": true` from each hardened family audit;
5. checks every orbit and labelled-support count;
6. pins every component audit by SHA-256.

Run:

```text
python verify_ten_vertex_c10_equality_family.py --certificates tmp/ten_vertex_c10_equality_support_transport_final2.json
python verify_ten_vertex_c4_c6_equality_family.py
python verify_ten_vertex_odd_factor_equality_family.py --orbits tmp/ten_vertex_c5_c5_equality_support_orbits.json --certificates tmp/ten_vertex_c5_c5_equality_support_one_term.json --output tmp/ten_vertex_c5_c5_equality_family_verified.json
python verify_ten_vertex_five_regular_equality_boundary.py
```

Pinned aggregate:

```text
tmp/ten_vertex_five_regular_equality_boundary_verified.json
SHA-256
  6cee340c304fc10397f6542963f5f34435a71680f02dc184665caf8a302c94f5
```

The aggregate contains `"verified": true`.

## Remaining boundary

This theorem does not exclude:

- 5-regular supports with at most 104 entries;
- non-5-regular exact-25-edge supports;
- other ten-vertex skeleton sizes;
- arbitrary larger even `n`;
- the global conjecture.

Those scopes remain explicitly unresolved.
