# Non-unimodular Laurent boundary replay

## Status

This is a verified repair of the CAS limitation recorded in the parent
snapshot. It is **not** a proof that either active coordinate branch is
empty, and it does not change the global **UNRESOLVED** status.

The original high-coordinate search stopped when its coefficient-relation
lattice selected a pivot minor of determinant `2`. A deterministic replay
from record 111 reproduced all 430 preceding learned clauses, verified that
each clause was false on the SAT model that regenerated it, and then reached
three actual non-unimodular signature strata:

| Signature tuple | Pivot determinant | Explicit relation binomials |
| --- | ---: | ---: |
| `(4199,1974,272,214,2803)` | `2` | 10 |
| `(4199,1974,266,4272,2803)` | `-2` | 11 |
| `(4199,1974,266,232,2803)` | `-2` | 10 |

All three ideals are the unit ideal under:

- Singular `slimgb`, used by the discovery run;
- a fresh Singular `std` regeneration; and
- `msolve 0.6.5`, after a strict syntax-only conversion of the identical
  polynomial ideal.

The three corresponding five-literal local-signature clauses pass the
independent semantic ledger auditor with three unique clauses, no mode
drift, and `exact_recorded_mechanism` on every record.

## Why the fallback is exact

After tree-gauge normalization, every supported coefficient variable
`x_j` is nonzero. A Laurent character equation

```text
x^r = epsilon
```

is therefore equivalent on the coefficient torus to

```text
x^(r_+) - epsilon x^(r_-) = 0.
```

For a unimodular pivot minor, the generator retains its original monomial
parameter elimination. For a non-unimodular minor, it keeps every
gauge-free coefficient variable and adds the cleared binomials to the
polynomial ideal. The existing Rabinowitsch equation

```text
z * (product of all coefficient variables)
  * (product of all required pure amplitudes) - 1 = 0
```

saturates simultaneously by the coefficient torus and the three required
nonzero pure amplitudes. Thus clearing negative exponents adds no
coordinate-hyperplane components, and retaining the implicit binomial ideal
keeps every finite torsion/root component instead of choosing one square
root.

## Packaged evidence

For each signature tuple this directory contains:

- the discovery `slimgb` Singular source and `UNIT_IDEAL` log;
- the independently regenerated `std` source and `UNIT_IDEAL` log;
- the exact `msolve` input and its `[-1]:` output; and
- the three-record normalized ledger in `focused_ledger.json`.

The strict converter is
`tmp/convert_p5_singular_to_msolve.py`. The workspace-local runner is
`tmp/run_p5_msolve_replay.py`.

Run the portable hash, conversion, source-equivalence, and semantic-clause
audit with:

```text
python claims/p5/boundaries/verify_p5_nonunimodular_laurent_boundary.py
```

The msolve convention `[-1]:` means that the system has no solution over
the algebraic closure. The included outputs are replay evidence; a fresh
third-party CAS execution still trusts the selected exact CAS engine in the
usual computer-algebra sense.

The replay used the official Ubuntu Noble `msolve 0.6.5-1build2` packages,
extracted without a system installation:

```text
libmsolve-0.6.5_0.6.5-1build2_amd64
SHA-256 e225dde132a052915bec6259395398f905a04d02814c9f7ac9f7795674e39c92

msolve_0.6.5-1build2_amd64
SHA-256 dbbca584ac7518ed3924e5614a5b83ace6f89de6ab561ca63b336499fb3f575d
```

The output convention is documented by the
[official msolve manual](https://manpages.debian.org/testing/msolve/msolve.1)
and the source is available from the
[official msolve repository](https://github.com/algebraic-solving/msolve).

## Boundary

The fallback removes the previous failure mode and allows the active
high-coordinate, `C10`, and `C4+C6` searches to continue. Those searches
remain finite CEGAR work until they terminate and receive full
semantic/symmetry/SAT proof audits.
