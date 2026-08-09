# Order-14 `C4+C4+C6` orbit-8 partial-binomial support certificate

> **Continuation complete.**  This document records the first two
> support-level CEGAR steps.  Three mandatory-unit certificates and their
> stabilizer orbits subsequently close selector 240 with an independently
> replayed DRAT proof.  The theorem-level continuation is
> `FOURTEEN_VERTEX_C4_C4_C6_ORBIT8_CERTIFICATE.md`.

## Claim

Consider full `3 x 3` blocks on the three cycles

```text
01 12 23 03
45 56 67 47
89 9-10 10-11 11-12 12-13 8-13
```

and the following three diagonal singleton perfect matchings:

```text
colour 0: 02 13 48 59 6-12 7-10 11-13
colour 1: 05 16 27 34 8-11 9-13 10-12
colour 2: 07 14 25 36 8-12 9-11 10-13
```

There is no assignment of nonzero complex values to this explicit support
whose perfect-matching amplitudes equal the three-colour monochromatic
target.

This is a theorem for one support selected under pinned first-factor
orbit 8.  It does not close orbit 8, the `C4+C4+C6` family, or the global
Krenn--Gu conjecture.

## Exact relation selector

The partial minimal-singleton-circuit dichotomy reconstructs 22 candidate
signed Laurent relations and the following 18 necessary clauses:

```text
(0 or 1)  (0 or 2)
(1 or 3)  (1 or 4)  (1 or 5)
(2 or 3)  (2 or 4)  (2 or 5)
6  7  8  9
(10 or 11) (12 or 13) (14 or 15)
(16 or 17) (18 or 19) (20 or 21)
```

The first eight clauses have exactly two inclusion-minimal transversals,
`{1,2}` and `{0,3,4,5}`.  Choosing one relation from each of the six
independent pairs and including the four units therefore gives exactly

```text
64 selections of size 12
64 selections of size 14
128 minimal selections in total.
```

No determinant-one pivot assumption is used.  Every relation system is
reduced over its exact integer lattice through Smith normal form, including
kernel-sign consistency and nonsaturated lattice membership.

## Common two-round obstruction

Every one of the 128 minimal selections closes after two rounds of exact
binomial propagation.  Depending on the branch, the first round derives
between 4 and 61 additional signed relations from forbidden amplitudes
having exactly two nonzero lattice cosets with equal coefficient
magnitudes.

Despite that variation, all 128 branches terminate at the same forbidden
colouring:

```text
(1,1,1,1,1,0,0,1,1,0,1,2,0,2).
```

Its active perfect matchings are

```text
0 8 13 21 24 56 64 67 118 126 131 139 142.
```

Exact signed-lattice reduction cancels every class except matching 67,
whose coefficient is `+1`.  Its nonzero monomial therefore survives in a
forbidden amplitude, giving a contradiction in every relation-selection
branch.  After all 128 exact selection blocks are added, a fresh CaDiCaL
decision reports the relation selector UNSAT.

## Independent reconstruction

`verify_fourteen_vertex_partial_circuit_binomial_branch.py` independently
reconstructs, for each branch:

1. the support and all 345 skeleton perfect matchings;
2. every positive-minimal partial circuit and its exact relation clause;
3. every selected initial relation and every derived binomial relation;
4. all Smith invariants, integer memberships, transported signs, and
   same-round consistency checks;
5. the final 13-term activity and sole surviving matching.

`verify_fourteen_vertex_partial_circuit_binomial_selection_chain.py` then
freshly replays all 128 branches, checks that every selection was live
before its exact blocking clause, proves inclusion-minimality, and makes
the terminal UNSAT decision.  The complete replay took 348.87 seconds and
reported `"verified": true`.

Pinned hashes:

```text
partial analysis
d772698d3a7204b75b5a9effdd072278f7df3eb1508df77232d5af3723cb03a1

closed 128-branch chain
44e3d54239249c2e62a5227155e2af296937f4959865e36eae09bc1edd92fabe

independent chain audit
35f14dab525ece81c9d0f63e640bbfb05c031f1973986ac6dd43eb3fe77867f3
```

The authoritative audit is

```text
tmp/fourteen_vertex_c4_c4_c6_orbit8_partial_binomial_selection_cegar_minimal_v5_verified.json
```

## Audited support no-good

Negating the 21 singleton-factor literals gives the exact support no-good

```text
-230 -226 -225 -189 -178 -167 -159
-152 -151 -147 -110 -103 -92 -80
-77 -65 -61 -52 -44 -12 -1
```

The independent augmentation verifier reconstructs this clause from the
support, binds it to the complete chain by SHA-256, and reproduces the
augmented DIMACS byte for byte.  The base and augmented CNF hashes are:

```text
base       9d0e0e3da2b1c759f17b0f874766af8cff8b8e921b5e1ccea236970df9a42918
augmented  d02bdc95cbc4a963bb22698c24c7cd3017ca66df4c7c16b9a528161c78553bf1
```

The augmented orbit CNF has 324 variables and 1,220,594 clauses.  It is
still SAT; the next distinct orbit-8 support has already been extracted.
Thus this augmentation is one sound CEGAR step, not an orbit closure.

## Second CEGAR support

The next SAT support retains the same full `C4+C4+C6` factor and colour-0
singleton factor, with

```text
colour 1: 05 17 26 34 8-11 9-13 10-12
colour 2: 07 15 24 36 8-12 9-11 10-13.
```

It produces 18 candidate relations and 16 necessary clauses: four units
and twelve binaries.  There are exactly 32 inclusion-minimal selections,
split into 16 of size 10 and 16 of size 12.  All 32 close after two
binomial-propagation rounds.

Again every branch reaches one common forbidden colouring,

```text
(1,1,1,1,1,1,0,0,1,1,0,0,0,0),
```

with active matching IDs

```text
0 8 10 13 21 118 126 128 131 139 199 207 209.
```

Matching 209 is the sole surviving signed lattice class in every branch.
The fresh independent chain replay checked all 32 selections and terminal
UNSAT in 370.56 seconds.

Pinned hashes:

```text
partial analysis
e43dd1cc80ac73452230bedb10b61a7310bb102b672dde4ba2b65942b4aa8020

closed 32-branch chain
60c57e4e1d63f398fa7b89810cc00f0de6e9c40531b569045aa1654164cc9035

independent chain audit
a5fb62f6dcd50b30064266fe4671c873dd521b232a4bd58198ddee3430cf1959
```

Its independently reconstructed width-21 no-good is

```text
-230 -226 -225 -189 -177 -168 -159
-152 -151 -147 -110 -102 -93 -80
-77 -65 -61 -52 -44 -12 -1
```

Appending it to the first augmentation produces a 324-variable,
1,220,595-clause CNF with SHA-256

```text
44e5ed260e04e0cd7207691209038d5f44d0d601b02d2030f91ec8a0ca08fb3f
```

The byte-identical independent augmentation replay passed.  This CNF is
also SAT and has yielded a third support, so orbit 8 remains open.

## Audit

With the bundled dependencies on `PYTHONPATH`, run:

```text
python claims/finite/n14/verify_fourteen_vertex_partial_circuit_binomial_selection_chain.py \
  tmp/fourteen_vertex_c4_c4_c6_orbit8_partial_binomial_selection_cegar_minimal_v5.json \
  --output tmp/fourteen_vertex_c4_c4_c6_orbit8_partial_binomial_selection_cegar_minimal_v5_verified.json

python claims/finite/n14/verify_fourteen_vertex_binomial_support_closure_augmentation.py \
  tmp/fourteen_vertex_c4_c4_c6_orbit8_binomial1_augmentation.json \
  --output tmp/fourteen_vertex_c4_c4_c6_orbit8_binomial1_augmentation_verified.json

python claims/finite/n14/verify_fourteen_vertex_partial_circuit_binomial_selection_chain.py \
  tmp/fourteen_vertex_c4_c4_c6_orbit8_support2_partial_binomial_selection_cegar.json \
  --output tmp/fourteen_vertex_c4_c4_c6_orbit8_support2_partial_binomial_selection_cegar_verified.json

python claims/finite/n14/verify_fourteen_vertex_binomial_support_closure_augmentation.py \
  tmp/fourteen_vertex_c4_c4_c6_orbit8_binomial2_augmentation.json \
  --output tmp/fourteen_vertex_c4_c4_c6_orbit8_binomial2_augmentation_verified.json
```

Both outputs must contain `"verified": true`; the first must also contain
`"terminal_relation_selection_sat": false` and `"support_closed": true`.
