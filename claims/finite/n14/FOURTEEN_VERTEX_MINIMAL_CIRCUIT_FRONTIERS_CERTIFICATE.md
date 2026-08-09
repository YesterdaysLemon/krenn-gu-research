# Order-14 minimal-circuit orbit frontiers

## Scope

This is a finite computer-assisted theorem inside the three unresolved
all-even order-14 equality-architecture families.  It combines the
minimal singleton-circuit rectangle theorem with previously reconstructed
transport, one-extra, and connectivity clauses.

It is not a proof of the Krenn--Gu conjecture.  The `C6+C8` and
`C4+C4+C6` frontiers use the explicit minimum-connectivity-three rule
layer, which is relevant because a minimal counterexample is known to be
4-connected.

## `C4+C10`

The minimal-circuit v10 CNF has 656 variables and 294,316 clauses:

```text
SHA-256:
0c49048f193c9b4184497d4e0abcc7df9caa209715678c5a6648c76decaba3e0
```

It excludes 364 selector orbits, including the newly closed orbit 2.
Conditioning on their disjunction gives:

```text
conditioned CNF clauses: 294,317
conditioned SHA-256:
6b322fa791c5c88a17fe176b6f6e65221c0faeea3dce64452c5dc15055aa5003

DRAT bytes: 5,381,129
DRAT SHA-256:
8b9afc9e1b9b9ca8a66536594d0d4870637b53998f6d1921e10ce3a1d7164c05
```

Independent forward `drat-trim` replay returned `s VERIFIED`.  Combining
this set with the separate orbit-0 certificate excludes 365 of 425
orbits.  The 60 not excluded by these certificates are:

```text
3--28, 58--63, 70--75, 102--105, 112--113, 121, 124,
153, 156, 164, 170--174, 176--177, 248, 251--252, 255
```

## `C6+C8`

The minimal-circuit v32 CNF has 559 variables and 264,742 clauses:

```text
SHA-256:
70ad534437167f5b5c1ee1e4ab6b1b9a5cd2abd1335b5378a24c463180ecea81
```

It excludes 292 of 328 selector orbits.  Its aggregate proof is:

```text
conditioned CNF clauses: 264,743
conditioned SHA-256:
9e9cfeb68ee891240de55437b309a4552e0636295832e46e20a0612d40bfe41b

DRAT bytes: 3,310,508
DRAT SHA-256:
8d05cd6c305c5c4c0e03943644380c6cc22e348ae328c1764350e8c06d1fc527
```

Independent forward replay returned `s VERIFIED`.  The 36 selectors not
excluded by this certificate are:

```text
17--40, 46, 53, 145--150, 156, 163, 168, 183
```

## `C4+C4+C6`

The v7 minimal-circuit CNF has 324 variables and 1,220,593 clauses:

```text
SHA-256:
9d0e0e3da2b1c759f17b0f874766af8cff8b8e921b5e1ccea236970df9a42918
```

It excludes 63 selectors in one aggregate conditioned proof:

```text
conditioned CNF clauses: 1,220,594
conditioned SHA-256:
946887be7dd4c99c7738815687bdae3f557c9af9fb25dac2638fac78ca4c30c0

DRAT bytes: 114,637,425
DRAT SHA-256:
08cd7bb800c3e34e895a7c34d2dcdd7073989eb2dabb19b2f83e271a0a811d45
```

Independent forward replay returned `s VERIFIED` in 1,752.58 seconds.
Taking the union with the earlier 61-orbit certificate gives 65 of 93:

```text
0--7, 12, 17--21, 23--35, 42--43, 52--53, 56,
58--62, 64--67, 69--92
```

The 28 selectors not excluded by this union are:

```text
8--11, 13--16, 22, 36--41, 44--51, 54--55, 57, 63, 68
```

### Targeted orbit-8 continuation

The support-local signed-lattice continuation separately excludes orbit
8.  Two exact relation-selection certificates and three
stabilizer-orbit-closed mandatory-unit certificates add 48 support
no-goods.  Conditioning the resulting 1,220,641-clause CNF on selector
240 has an independently replayed 58,902,708-byte DRAT proof.

Combining that theorem with this frontier excludes 66 of 93 selectors and
leaves 27:

```text
9--11, 13--16, 22, 36--41, 44--51, 54--55, 57, 63, 68
```

The exact hashes and replay command are in
`FOURTEEN_VERTEX_C4_C4_C6_ORBIT8_CERTIFICATE.md`.

## One-command cross-audit

With the repository runtime and bundled dependencies on `PYTHONPATH`, run:

```text
python claims/finite/n14/verify_fourteen_vertex_minimal_circuit_frontiers.py
python claims/finite/n14/verify_fourteen_vertex_c4_c4_c6_orbit8.py
```

The first audit checks every aggregate augmentation/condition/proof hash
binding, the selector clauses, all three independent aggregate DRAT
results, the prior certificate gates used in the two unions, and the
exact complements.  It must write
`tmp/fourteen_vertex_minimal_circuit_frontiers_verified.json` with
`"verified": true`.  The second reconstructs the targeted orbit-8
continuation and reruns its independent DRAT proof.

## Boundary

These are exact finite selector exclusions, not classifications of the
remaining supports.  In particular, 60 `C4+C10`, 36 `C6+C8`, and, after
the targeted orbit-8 continuation, 27 `C4+C4+C6` selector orbits remain
outside the stated certificates.  The global prize conjecture remains
unresolved.
