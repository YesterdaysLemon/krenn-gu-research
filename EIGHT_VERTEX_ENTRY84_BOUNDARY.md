# Eight-vertex exact-20, 84-entry boundary

## Status

This is a finite structural theorem for `n=8`, `d=3`, and an essential
skeleton with exactly 20 blocks.  It is not a solution of the full
Krenn--Gu conjecture.

**Theorem.**  Such a support has at most 84 supported matrix entries.  If it
has exactly 84, then twelve blocks are diagonal singletons and eight blocks
are full `3 x 3` matrices.  The singleton blocks form three
colour-labelled perfect matchings.

If the 20-edge skeleton is 5-regular, the eight full blocks additionally
form a spanning 2-factor.  Hence its equality support belongs to the
7,938-support family already excluded by
[`EIGHT_VERTEX_FULL_SINGLETON_FAMILY_CERTIFICATE.md`](EIGHT_VERTEX_FULL_SINGLETON_FAMILY_CERTIFICATE.md).
Consequently, a hypothetical witness in the 5-regular exact-20 branch must
have at most 83 supported entries.

## Entry count

At every vertex and for every colour `c`, the generic-killer theorem gives
a nonzero incident block of the form

```text
a_c outer e_c.
```

Choose one such block for each of the 24 vertex-colour pairs.  A nonzero
block cannot be selected for two different colours at the same endpoint.
Let:

- `r` be the number of skeleton edges selected from both endpoints;
- `s` be the number selected from one endpoint;
- `t` be the number selected from neither endpoint.

Then

```text
2r + s = 24,
r + s + t = 20.
```

A reciprocal selected block has at most one entry, a one-way selected block
at most three, and an unused block at most nine.  Therefore

```text
entries <= r + 3s + 9t = 36 + 4r <= 84,
```

because `r <= 12`.  Equality forces

```text
(r,s,t) = (12,0,8)
```

and equality in every block bound: twelve reciprocal singleton blocks and
eight full blocks.

The same calculation works for every even `n` in the three-colour problem.
For an `m`-block essential skeleton,

```text
entries <= 9m - 12n.
```

Equality forces `3n/2` reciprocal singleton blocks, no one-way selected
block, and `m-3n/2` full blocks.  The backup argument in the next section
then makes all equality singletons diagonal.  The eight-vertex theorem is
the specialization `(n,m)=(8,20)`.

## Why every equality singleton is diagonal

Fix a vertex and its selected colour-`c` singleton.  Write its only local
entry as `(a,c)`.  Its killer vector is the coordinate vector `e_a`.

Suppose `a != c`.  The failure-hyperplane backup theorem says that another
incident block `B` must satisfy:

1. the `c`-column of `B` is nonzero and not proportional to `e_a`;
2. every nonzero non-`c` column of `B` is proportional to `e_a`.

There are only two kinds of other equality blocks.

- A full block fails condition 2: both non-`c` columns have all three
  entries.
- Another singleton is selected for one of the other two colours, because
  the three selected killer colours at a vertex are distinct.  Its
  `c`-column is zero, so it fails condition 1.

No backup exists, a contradiction.  Hence `a=c`.  This holds at every
endpoint of every reciprocal singleton, so all twelve are diagonal.  Each
vertex meets exactly one singleton of each colour, making each colour class
a perfect matching.

On a 5-regular skeleton the singleton subgraph is cubic, so the full-block
complement is 2-regular and therefore a spanning 2-factor.

## Independent finite audit

[`verify_eight_vertex_entry84_boundary.py`](verify_eight_vertex_entry84_boundary.py)
independently:

1. enumerates all nine integer solutions for `(r,s,t)`;
2. checks that 84 is the unique maximum and occurs only at `(12,0,8)`;
3. checks the general identity on 561 feasible `(n,m)` pairs with even
   `4 <= n <= 20`;
4. reconstructs the support conditions of the backup theorem;
5. exhausts all 27 local singleton-row assignments for each possible
   full-block degree from zero through four;
6. verifies that `(0,1,2)` is the only assignment satisfying every required
   backup.

Run:

```text
python verify_eight_vertex_entry84_boundary.py
python -m unittest -v \
  test_search_witness.EquationSystemTests.test_exact20_entry84_boundary
```

Pinned audit:

```text
tmp/eight_vertex_entry84_boundary_verified.json
SHA-256
  60950aadbed74aaf97cb5ecff9ad0b49d8bf7133fc77db495f886d0041419eb4
```

The audit has `"verified": true`.

## Remaining boundary

This theorem does not exclude exact-20 supports with at most 83 entries.  It
also does not identify the eight full blocks as a 2-factor when the
20-edge skeleton is not 5-regular.  Those are separate open finite
branches, and the global even-`n`, `d>=3` conjecture remains unresolved.
