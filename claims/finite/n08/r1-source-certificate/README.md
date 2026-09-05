# Exact certificate for the eight-vertex matrix-unit parent

This package is a proof leaf of the
[eight-vertex maximum-root-one exclusion](../EIGHT_VERTEX_MATRIX_UNIT_EXCLUSION_THEOREM.md).
It contains the complete eighteen-scaffold cover, 39 exact algebraic cuts,
and eighteen independently checked UNSAT certificates. It does not prove
the global Krenn--Gu conjecture, and it is not a Lean formalization.

## Durable proof data and separate checks

[`certificate.json`](certificate.json) is the frozen specification:
SHA256 `34d3f3557e952d0c2d03c3b2f8fcb04c2f786400209f76e8e39a7dcbc9e31b8d`.
It pins the dimensions, scaffold representatives, all signed integer cores,
each final CNF's bytes/counts/hash, and both compressed and raw proof bytes.

The `proofs/*.drat.gz` files are intentionally durable mathematical
certificates, not disposable solver logs. They contain the exact accepted
text DRAT proofs, losslessly compressed. Their raw size is 8,003,487 bytes;
their compressed size is 2,039,952 bytes. Git treats these archives as
opaque binary data. Raw CNFs, temporary decompressions, solver logs, and
external executables remain untracked.

Three programs have different roles:

- [`generate_instances.py`](generate_instances.py) deterministically
  regenerates the eighteen frozen CNFs with the Python standard library.
  It uses no SAT solver and checks all output counts and hashes.
- [`audit_instances.py`](audit_instances.py) independently rebuilds the
  105 matchings, 384-element symmetry group, complete 1,884-pair cover,
  every source/collision clause, membership equivalence, and algebraic
  no-go clause. It imports neither the generator nor a solver. Its ten
  self-controls include malformed algebraic cores, a missing orbit,
  a missing reverse implication, and a dropped repair-matching literal.
- [`check_proofs.py`](check_proofs.py) validates all compressed/raw proof
  and CNF pins, then invokes a separately supplied native DRAT checker on
  every case. It checks one valid and two invalid proof controls and
  accepts only exit zero with the exact verdict `s VERIFIED` for all
  eighteen cases. It does not establish the mathematical source bridge.

The final proof needs BOTH independent source semantics and certificate
acceptance. Solver-reported UNSAT alone is not a proof. The algebraic cuts
are consequences of the complex weighted source, not claimed logical
consequences of the weaker collision-only base CNF.

## Reproduce the frozen inputs and source semantics

From the repository root, with Python 3.10 or newer:

```text
python claims/finite/n08/r1-source-certificate/generate_instances.py --output-dir tmp/r1-certificate-instances
python claims/finite/n08/r1-source-certificate/audit_instances.py --instance-dir tmp/r1-certificate-instances
```

The DIMACS format is explicit ASCII CRLF on every platform. These line
endings preserve the exact accepted input hashes; Git does not need to
track or normalize the generated files. All 14,899,605 CNF bytes must
match the specification. Optional generator flag `--maps` emits variable
descriptions for inspection; those maps are not trusted by the independent
semantic checker.

The audit's `--self-test-only` mode does not check the eighteen generated
CNF files and is not a substitute for the complete command above.

## Replay the supplied proofs

The independent implementation is
[DRAT-trim](https://github.com/marijnheule/drat-trim), pinned source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The committed LF C source hash is
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
The audited native binary hash is
`92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a`.
It was built on Ubuntu 24.04, x86-64, using GCC 13.3.0 and
`gcc drat-trim.c -std=c99 -O2 -o drat-trim`, with the source directory as
working directory. The independently rebuilt binary was byte-identical.

A source checkout may be prepared in an ignored temporary directory:

```text
git clone https://github.com/marijnheule/drat-trim.git tmp/drat-trim
git -C tmp/drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C tmp/drat-trim drat-trim
```

Run the native proof driver in Linux or WSL, from the repository root:

```text
python3 claims/finite/n08/r1-source-certificate/check_proofs.py --certificate claims/finite/n08/r1-source-certificate/certificate.json --instance-dir tmp/r1-certificate-instances --checker tmp/drat-trim/drat-trim --output-dir tmp/r1-proof-replay
```

Choose a new output directory for each proof replay. The driver preserves
its receipts and refuses to overwrite a previous run. Temporary raw
proofs are removed after checking. The recorded replay completed all
eighteen cases and all three controls in about eleven seconds; a timeout
is a failed replay, not proof of a mathematical case.

By default the driver requires the audited binary hash above. A separately
trusted build from the pinned source may have a different binary hash
because of its compiler or environment; supply its expected digest
explicitly with `--checker-sha256 HASH`. The receipt records whether this
is the original audited executable or another supplied build. A hash is an
identity check, not a proof that an arbitrary supplied executable is sound.
The external checker implementation remains an explicit tool dependency.

## Provenance and scope

CaDiCaL 1.7.3 produced the supplied text proofs; no solver is needed for
their replay. The discovery search and generating label models are not
required inputs. The specification contains all data needed to reconstruct
the final necessary source instances, and the archives contain all accepted
proof objects.

Independent reviews separately cover the
[source semantics](../../../../docs/audits/EIGHT_VERTEX_MATRIX_UNIT_SEMANTIC_REVIEW_2026-09-04.md),
[DRAT certificates](../../../../docs/audits/EIGHT_VERTEX_MATRIX_UNIT_CERTIFICATE_REVIEW_2026-09-04.md),
and [final integration](../../../../docs/audits/EIGHT_VERTEX_MATRIX_UNIT_INTEGRATION_REVIEW_2026-09-04.md).
The owning theorem supplies the explicit hypothetical-witness-to-CNF bridge.
The generator, a manifest flag, or a checker verdict by itself does not
extend the conclusion beyond the stated eight-vertex matrix-unit case.
