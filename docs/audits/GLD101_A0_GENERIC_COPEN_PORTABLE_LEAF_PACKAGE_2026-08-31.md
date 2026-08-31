# GLD101 normalized a=0 generic C-open portable leaf package

Date: 2026-08-31

Status: scoped exact selected-necessary-minor proof leaf; independently
replayable from a clean clone; global Krenn--Gu status **UNRESOLVED**.

## Exact obligation

Work on the normalized equal-leaf H4 chart with

- `a=0`;
- `Q6(p,q)=0`;
- `B=0` and `C!=0`; and
- `H2*Delta != 0`, where `Delta` contains the GLD88 chart gates and
  `p^2-p+1`.

If the GLD71 syndrome matrix has rank at most six, each of the selected
seven-minors

`T0, T1, T2, T3, Y1, X3`

must vanish.  This implication is only necessary: the package does not claim
that vanishing these six minors is sufficient for rank at most six.

On `B=0`, direct reconstruction of every named determinant gives exactly

`selected minor = C * rational coefficient in QQ(p)[q]/(Q6)`.

There are no higher powers of `C`: each selected column set contains exactly
one of the three C-bearing component columns.  The rational denominators
factor only through

- `P=p^2-p+1`, which is already a factor of `Delta`; and
- `H2=2*p^2-2*p+1` up to a nonzero rational scalar.

Consequently `C!=0` and `D(H2*Delta)` turn selected-minor vanishing into the
six primitive numerator equations disclosed in the tracked Singular source.

## Exact rank cover

Each numerator has q-degree at most three.  Put its coefficients in the order
`q^3,q^2,q,1`; the six rows form a 6-by-4 matrix over `QQ[p]`.  All fifteen
maximal minors are nonzero.  Their primitive gcd is

`p^15*(p-1)^6*(p+1)^2*(p^2-p+1)^11*(2*p^2-2*p+1)^14`.

Away from these factors, some maximal minor is nonzero.  The six cubics then
span the four-dimensional space of q-polynomials of degree at most three, so
they cannot share a q-zero.

The remaining fibres are disposed of exactly:

- roots of `p^2-p+1` are outside `D(Delta)`;
- roots of `2*p^2-2*p+1` are outside `D(H2)`;
- at `p=-1`, the gcd of `Q6` and all six equations is `1`;
- at `p=0`, the common gcd is `q^2`, exactly the gcd of `Q6` and `Delta`;
- at `p=1`, the common gcd is `(q-1)^2`, exactly the gcd of `Q6` and
  `Delta`.

Thus the six numerator equations have no common point with `Q6=0` on the
stated open locus.  The calculations are polynomial identities over `QQ`, so
they base-change to any algebraically closed field of characteristic zero.

## Reproducible evidence

The durable package consists of:

- `claims/arbitrary-order/certificates/GLD101_A0_GENERIC_COPEN_UNIT_SCREEN.singular.txt`:
  exact coefficient disclosure, LF SHA-256
  `c514d842532f99cde4488cca048c551f39e43ed5cdf2c5ce6a54dcd7aa704850`;
- `claims/arbitrary-order/certificates/GLD101_A0_GENERIC_COPEN_PORTABLE_CERTIFICATE.json`:
  deterministic polynomial records, LF SHA-256
  `1f84c1d30c1c8403be477b5def91144f687cc08a4ed5406dffb3866cf6996afb`;
- `claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_generic_c_open.py`:
  canonical reconstruction through the hash-pinned GLD101 implementation;
- `claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_generic_c_open.py`:
  no-repository-import audit; and
- `tests/test_gld101_generic_copen_portable_leaf.py`: focused portability,
  scope, and replay tests.

The primary checker reconstructs the full sparse `B,C` determinants from the
hash-pinned GLD71 and GLD88 implementations.  It compares all six primitive
coefficient numerators to the Singular source, records all fifteen maximal
minors, and checks the generic and special-fibre cover.

The audit does not import or execute any repository module or the primary
checker.  It parses the literal GLD71 `SPARSE_RELATIONS` assignment with
`ast.literal_eval`, transcribes the hash-pinned GLD88 a=0 chart locally,
reconstructs the minors using C-dual quotient arithmetic, parses the Singular
polynomials with a restricted parser, and recomputes each 4-by-4 determinant
by the explicit Leibniz formula.  It compares every load-bearing record with
the hash-pinned certificate.

Run from repository root:

```text
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_generic_c_open.py
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_generic_c_open.py
python -m unittest -v tests.test_gld101_generic_copen_portable_leaf
```

No Singular installation, archived process, terminal transcript, ignored run
directory, Commons checkout, or machine-specific path is needed.

## Provenance and failed lineage

The historical generic-C-open Singular experiment supplied the exact
coefficient source.  Cross-audit versions v1 and v2 failed their process
identity/provenance checks and remain non-evidence.  Version v3 repaired that
identity logic and was accepted as a scoped audit.  This package does not
reinterpret the failed attempts: it removes the archived-process dependency
by making the exact rank cover and two independent reconstructions
load-bearing.

## Scope boundary and frontier effect

This package proves only the stated selected-necessary-minor emptiness.  It
does not prove:

- a converse from the six selected minors to syndrome rank;
- the `B!=0` or `C=0` loci;
- arbitrary `a`, endpoints, or physical incidence;
- the P8 parent theorem or full E31 wall; or
- the global Krenn--Gu conjecture.

No `docs/current-frontier.md` change is made because the scoped generic
C-open conclusion and its role in the recorded parent attempt already
existed before this packaging change.  The mathematical claim, quantifiers,
dependencies, and proof-topology edges are unchanged; this commit replaces a
host-local evidence dependency with a clean-clone portable certificate and
independent audit.  Any later composition that closes a residual parent
branch must update the live frontier in that separate, adversarially reviewed
change.
