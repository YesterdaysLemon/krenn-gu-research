# Eight-vertex 4-regular exclusion

## Claim

There is no complex three-colour Krenn-Gu witness whose eight-vertex
skeleton is 4-regular.

This is a finite computer-assisted theorem.  It does not exclude
nonregular eight-vertex skeletons and does not settle the arbitrary-vertex
prize conjecture.

## Analytic input

Every exact three-colour witness has, for each `(vertex,colour)`, a distinct
nonzero generic killer block supported on that colour's column.  A second
contraction gives a diagonal anchor for each task.  At a vertex of skeleton
degree exactly four these identities imply that at least one incident block
is a nonzero monochromatic singleton

```text
alpha e_c outer(e_c),   alpha != 0.
```

The full proof is in `RESEARCH_NOTES.md` under “Degree-four singleton
theorem.”

## Complete graph classification

The complement of an eight-vertex 4-regular graph is cubic, but it need not
be connected.  The House of Graphs catalogue and the first nauty run both
contained the five **connected** cubic classes:

```text
geng -cd3D3 8
```

That is not a complete complement catalogue: the disconnected cubic graph
`K4 disjoint-union K4` gives the sixth 4-regular class `K4,4`.

The repaired audit uses two independent nauty 2.9.3 enumerations:

```text
geng -d3D3 8       -> six cubic graphs, connectivity unrestricted
geng -c -d4D4 8    -> six connected 4-regular graphs directly
```

Their files and hashes are:

```text
tmp/cub08_all_nauty.g6
a8bbfcf47bd61aaec24ca2f04122dc90fc0aafc4f6ae82e5c118c328226d192e

tmp/reg4_08_nauty.g6
781b0a4dd2c4289669bc9ff37264cc85afccfa9aaddc9313ae8466fd1bb111e5
```

Brute-force isomorphism gives a bijection between the complements of the
six cubic graphs and the six directly generated 4-regular graphs.  The
catalogue-to-all-cubic permutation is `[3,2,4,0,1,5]`; the corresponding
direct-regular indices are `[1,2,3,4,5,0]`.

Five classes are 4-connected.  The remaining connected-complement class
has a three-vertex cut and was certified directly too; this theorem does not
rely on reducing it through the exceptional four-vertex witness.

## Necessary support encoding

For each fixed skeleton, `eight_vertex_degree4_support.py` introduces a
Boolean for every matrix entry and imposes:

1. every skeleton block is nonzero;
2. every monochromatic amplitude has at least one nonzero matching monomial;
3. no forbidden amplitude has exactly one nonzero matching monomial;
4. every generic killer task has an eligible block;
5. every vertex has an incident exact monochromatic singleton.

These are necessary conditions over every field.  Therefore UNSAT excludes
an exact complex witness; SAT would only mean that the relaxation survived.

The six materialized instances are all UNSAT:

| Class | PMs | Variables | Clauses | CNF SHA-256 |
|---:|---:|---:|---:|---|
| 0 | 16 | 105,312 | 631,779 | `97a388ff469b45317093aa44c54f488a2523f2f3ed8a7b72a72c113b48497ccf` |
| 1 | 14 | 92,190 | 553,053 | `47d91520313ed5a5324c6a1a76018c167cd87c32ba75310a2e2d969150bb185a` |
| 2 | 14 | 92,190 | 553,053 | `522ccb3fef84df670ebf23bdc3ba277ad3d1c3551227fa11f337e093d53837dd` |
| 3 | 16 | 105,312 | 631,779 | `f61556520776af1e8138a877ec83c4cc1398431ba09f6f55aacfed634e8415fd` |
| 4 | 14 | 92,190 | 553,053 | `e65096f573d4e38cfb29bbcfb021205edd4a1bba95b09071c9c9cec3b7685e40` |
| 5 (`K4,4`) | 24 | 157,800 | 946,683 | `418d09659b6b425c4dd9005761bb73fbd6e98e8b60d9dd365391ef90cae960d7` |

## Independent solvers and proof checking

CaDiCaL 1.9.5 produced one DRAT trace per class.  Glucose 4.2 independently
returns UNSAT on the same CNFs.  `drat-trim` returns `s VERIFIED` for every
trace.

| Class | Proof bytes | Proof SHA-256 | Resolution steps |
|---:|---:|---|---:|
| 0 | 10,706,444 | `389457c7a49ba088c750ae60e1a6997720c21c2a09f0264c0117c882a9b5e380` | 2,907,449 |
| 1 | 8,783,946 | `ed807dfcfdc4eef33b33164af11aff97b51038bdf45e1671061bb6c81d0f8c52` | 2,450,274 |
| 2 | 7,234,471 | `f8e88d600d74383633e0870b57c8d03f7f6ce70391fa59e8978fcbde332a3526` | 2,175,560 |
| 3 | 9,738,661 | `a1866d6805885cc6e770f42951769ac239ac27b5075d12eaa20f0068c8724ae5` | 2,877,918 |
| 4 | 7,628,467 | `bec393bfe221b3c3718d8c5e7058e2e2089e415d9ecb36611f7878970ff5e510` | 2,414,474 |
| 5 (`K4,4`) | 26,301,644 | `a6456784f7ef18336d834b2fd52b8cdb3635f5abac23756aa2926b1421304c96` | 10,052,726 |

## Fail-closed audit

Run:

```text
python verify_eight_vertex_4regular.py
```

The verifier pins all four graph catalogues (including the two historical
connected-cubic lists), all CNF hashes, all proof hashes, connectivity
metadata, both six-class bijections, the independent Glucose results, the
CaDiCaL terminal lines, and all six `drat-trim` verification logs.  Its
authoritative output is

```text
tmp/eight_vertex_4regular_final_audit.json
```

with `"verified": true`.
