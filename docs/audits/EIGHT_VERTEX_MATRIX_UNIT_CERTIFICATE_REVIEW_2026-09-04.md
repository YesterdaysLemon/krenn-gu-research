# Independent DRAT certificate audit of all 18 final r=1 CNFs

**PASS: 18/18 exact final CNFs independently certified UNSAT.** Every official drat-trim invocation returned exit code 0 and the exact line `s VERIFIED`; no case was ignored. Three checker controls passed. This report does not audit the semantic case cover, CNF encoding bridge, or algebraic cuts; those have a separate independent owner. No global resolution or Lean formalization is claimed.

## Checker provenance and exact build

Official source: [DRAT-trim](https://github.com/marijnheule/drat-trim), commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
- Checked source SHA256: `78026871882de3f2fee66034e549e9c1a0a9a5291abd817d06f611f9ba0f355d`.
- Committed LF source SHA256: `d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
- Executed checker SHA256: `92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a`.
The checked source differs from the committed blob only by Windows CRLF line endings, verified by exact normalized byte comparison. An independent `gcc drat-trim.c -std=c99 -O2` rebuild, with source-directory working directory, produced the exact same 51216 binary bytes. Compiler: gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0. The checker binary remained unchanged through all cases.

The producer is a separate CaDiCaL 1.7.3 search emitting text DRAT. Its exit status supplies no independent verification. This audit used the official independent drat-trim implementation, without importing producer code or trusting native PySAT output.

## Input/proof identities and complete results

Final-CNF manifest SHA256: `56c48349478e901c742357452fd792e4f97263aa813a31fdaa108a8662073320`.
Frozen proof-production manifest SHA256: `9d6f00e836f6be788de177b68f92d777be5d7301c72a122d7e7d514b3e0cfdf3`.
Every final CNF hash matches its CEGAR result and producer before/after pins. Every proof matches the producer proof pin. Both CNF and proof bytes were rehashed unchanged after checking, and both manifests were rehashed unchanged at completion.

| Case | CNF SHA256 | Proof SHA256 | Exit | Verdict |
| --- | --- | --- | ---: | --- |
| r1-scaffold-000 | `f59ebd415deead3a80e39886ac75dcf7298996f9325640ce6f83c8ac81adcbc6` | `6594580b141267be3a76d02f8ff5e837007c00a3aff83ecf85ae787c704e6acf` | 0 | s VERIFIED |
| r1-scaffold-001 | `deecd9fe0b1e0dd40fb3d817659ef8ba8d8ef9c915cb566908a96220eacccadb` | `b0e1f03aebdfeb2dc2045e6e508c621128ce3daae0496de57a9d3c01cd5768c3` | 0 | s VERIFIED |
| r1-scaffold-002 | `d0c83f977187025393423f7ed9bdfe4d1c8903749f124316a2a5277ca8efe03e` | `597bff1c265449ec5b0bdbab76e90b32c8aec64527784a1c1921f19d376935f1` | 0 | s VERIFIED |
| r1-scaffold-003 | `6c0e4cc3815e76e35950cdf1df130c5cb554cb29be732d429d303f7ccb1eb6f7` | `fd258f66f4a144984e9ae91d47e1873f8988218b6102216d74a843a7070e20e5` | 0 | s VERIFIED |
| r1-scaffold-004 | `3a9b325733e43a14158ac52808209da15ee66ab6692db26811ad50c9701c40de` | `66bea444ec5e28a8671506ee38250106f2ab9d22b40132a8414d15aae67aacdc` | 0 | s VERIFIED |
| r1-scaffold-005 | `9191ad99ebb7b8fe518949a0ac82b4d2498573c4e237cfa73fb77b4bac96ef3f` | `8738b2b4c05c78a09e9f949081c6ff7de174b6e0a6264530971f4471db9acde2` | 0 | s VERIFIED |
| r1-scaffold-006 | `784975cada93e4940e6278e46ba93e33e2e5aa81417850b2f260df4ca67bdd54` | `17ac396c10550261af1b50f3e19551b8d6902fa7baf9123df8dd0912a601a6a9` | 0 | s VERIFIED |
| r1-scaffold-007 | `25c6d025a5dc9aed2a5b5363debc008ffaf9cb5ab5bb88b50f7049ceba258066` | `c76444672be44d1b7f104a73b099cc0a8562013f00431a2c877cf3e042ce6f2b` | 0 | s VERIFIED |
| r1-scaffold-008 | `4653fda0c62aba91aa8c52608eefe80478aefdafaade2a8bde40f498546e2a54` | `bcb63e44ea4cd1aa5d669466e25ad541396c42542ec960da680ae4047607f64c` | 0 | s VERIFIED |
| r1-scaffold-009 | `b08515a943e2f7f439298beddd7a6cf44b9a6db4c971d981bc51e15de43aef0c` | `e1a889f602419281eee3b2e9083ed7b26573f838a1a990b7c295fd312c681c4f` | 0 | s VERIFIED |
| r1-scaffold-010 | `6792c87839ce5e107c53a8e8c1c0944a3c4fef6c5bd4e157fdab62d7c41bf29a` | `2e0bd4505b6b6206da5b08f5f4ffc3b4d73694360173010d99c9ef2eeecb0f76` | 0 | s VERIFIED |
| r1-scaffold-011 | `b24283c4e7f9aea89e7faca627af35fbd55b6e8f6c2cc2133fcee99f9de4b144` | `fe73585a6ed97f092faed4028c8bb40fdf515556e80292554046e2d70a82737d` | 0 | s VERIFIED |
| r1-scaffold-012 | `be6917ad3d18537b13ca33ad8d75c1ec95dacf67669601168cac52d2f4988672` | `9b43762e9acb3d0ae08e83170750445ac0b07c173ea335a76471f3ada7bf476e` | 0 | s VERIFIED |
| r1-scaffold-013 | `81644dcd2748700c222d4edc180d26852295b82a203eba26a4a0fce003274294` | `6878bc958bb22e5757c0651e24a8094eb6f5505f8b5f7036a05cb309599145ad` | 0 | s VERIFIED |
| r1-scaffold-014 | `9a03feb143ba8cd2e00ca517021ee54111b1318ffb0c3272dc55e323a8a8d6d4` | `395583f045b86cdd879d8d6b853c240006f1b9aaf39098afe6c903c9fe924b83` | 0 | s VERIFIED |
| r1-scaffold-015 | `5d6a3f546dca5c7b5f5a3aa99d5151f1dffe4c6144e88fd875460d75a5a4a3ec` | `2ee06691c25b606c584b45ef007210aca9bf4e506bb40f94fd950a3368914510` | 0 | s VERIFIED |
| r1-scaffold-016 | `ed90af787b463d430fbc21fe494d76a3b764cd6ccdb7ab51d596f0fd3c850e98` | `2cc1c378bcdcf69090fc77a41a87b6a8f6b79aa367fadc062d52f68618fb93b1` | 0 | s VERIFIED |
| r1-scaffold-017 | `536a5f9900d7c1cd41d36e0d458e02f894cbe5d87f308c1891c01b9e1e11f86d` | `3c3bfa3db1010d0f23bc3e1f4ddce61a8cf4d69f9379b001ddcb3ff7821e0af6` | 0 | s VERIFIED |

Each case log, log hash, exact command, dimensions, bytes, elapsed time, and all input/proof before/after hashes are recorded in `tmp/lab-r1-drat-audit.json`.

## Controls

A nontrivial four-clause contradiction with a valid two-step proof was accepted (exit 0, s VERIFIED). The same CNF with an unjustified immediate empty-clause step was rejected (exit 1, s NOT VERIFIED). A satisfiable CNF with a false empty-clause proof was likewise rejected (exit 1, s NOT VERIFIED). Their exact bytes and log pins are in the JSON receipt.

## Containment and completion

One sequential Linux driver checked all cases under `ulimit -v 2097152` and GNU `timeout --signal=TERM --kill-after=3s 180s`, with process-group termination semantics. The outer Windows bounded runner used 200 seconds and 2048 MiB. The successful outer run took 10.955 seconds and returned child/runner exit code 0.

Two preliminary runs stopped before any proof checks: first on cross-platform git CRLF comparison, then on a reproducibility mismatch caused by compiling with an absolute source filename embedded by C assertions. Their failed receipts remain preserved. Source bytes were never edited. Exact normalization and relative source-name compilation resolved these setup issues before the successful run.

Outer receipts:
- `.research-runs/lab-r1-drat-independent-audit-01/20260905T010925Z-24684/run.json`: child 1, runner 1.
- `.research-runs/lab-r1-drat-independent-audit-02/20260905T011011Z-4516/run.json`: child 1, runner 1.
- `.research-runs/lab-r1-drat-independent-audit-03/20260905T011050Z-1968/run.json`: child 0, runner 0.

Linux driver PID 787 and all recorded Windows runner/WSL PIDs were confirmed absent after completion. No owned process remains. No tracked edits or PR were made.

Final audit JSON SHA256: `2e4226deea754216acb1d6c57b2750d4479e927b2857ad021cb2bdcb7988d9ed`.
Audit driver SHA256: `89d7a634e14d8fbd8eb82908c78aa0e32ebc12fd4691d3782d86ded676c846dc`.

# Final static review of the r=1 certificate package and proof layer

Final proof-package static review: **PASS**, including documentation, code identity, archive identity, CLI, totals, evidence claims, and corrected Git byte portability. No new proof replay was run or needed; the packaged driver and all accepted proof inputs retain their accepted bytes.

## Read set and role

Read claims/finite/n08/r1-source-certificate/README.md and Section4 plus evidence-status passages of claims/finite/n08/EIGHT_VERTEX_MATRIX_UNIT_EXCLUSION_THEOREM.md. Checked package code/specification hashes, all eighteen compressed archive hashes and sizes, archive count, aggregate raw/compressed/CNF bytes, the 39 stored core count, and effective Git attributes.

This is a static certificate/proof-layer review. It does not independently re-prove the whole mathematical source bridge, case cover, or algebraic cuts; the separate semantic and integration auditors own those conclusions.

## Accepted objects are unchanged

- Packaged check_proofs.py is byte-for-byte equal to the accepted portable driver; SHA256 e2c0ed26bf21070c2416228fe7f2c9a6c18e781a4732b7cd176d82e9819b7b89.
- Frozen certificate.json SHA256 remains 34d3f3557e952d0c2d03c3b2f8fcb04c2f786400209f76e8e39a7dcbc9e31b8d.
- All eighteen compressed archives match their specification SHA256 and byte size. Their exact accepted decompressed hashes were checked by the prior complete portable replay.
- Original independent DRAT audit JSON SHA256 remains 2e4226deea754216acb1d6c57b2750d4479e927b2857ad021cb2bdcb7988d9ed.
- Portable package replay JSON SHA256 remains 48c76e88836aa50c9d4743616c5c055871ca571d8a13e7c9bb7f58358c06f7e5.

The static sums are exactly 8,003,487 raw proof bytes, 2,039,952 compressed proof bytes, and 14,899,605 final CNF bytes. The README and theorem Section4 report the proof totals correctly and do not confuse compressed storage bytes with the raw mathematical proof objects. There are eighteen cases/archives and 39 stored algebraic cores.

## CLI and checker trust distinctions

README regeneration and proof commands use the agreed instance filenames, explicit certificate path, separate checker path, and fresh output directory. The Linux/WSL requirement matches the driver. The generator's explicit ASCII CRLF CNF bytes are correctly described. The external checker build command uses the pinned source commit and a relative source filename from the source directory, matching the audited build route.

The source commit is 2e3b2dc0ecf938addbd779d42877b6ed69d9a985; committed LF source SHA256 is d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee. The default audited binary SHA256 is 92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a. The earlier independent rebuild was byte-identical under its recorded GCC13.3.0 environment. README does not promise compiler-independent binary reproducibility.

The optional --checker-sha256 override is accurately described as the expected identity of a separately trusted external build. It is not a no-hash mode, and the receipt distinguishes the actual supplied hash from the original audited executable. The documentation correctly states that a hash does not establish arbitrary-executable soundness. The accepted package replay used no override and matched the audited binary exactly.

The driver requires all eighteen cases, hashes/counts/sizes, and checker exit zero plus an exact s VERIFIED line. Its controls include one valid and two invalid proofs. Solver-reported UNSAT, a manifest flag, self-test-only controls, and semantic auditing are not conflated with full certificate acceptance. No Lean or other kernel-checked formalization is asserted. The certificate checker is correctly distinguished from the independent source-semantic checker and producer. Global status remains UNRESOLVED.

## Codec, prior acceptance, and process closure

The accepted portable replay used CPython3.12.3, standard-library gzip, and built-in zlib compile/runtime1.3. The gzip module SHA256 was 31e7275c5c20d1b414063c28088b68e7a3e657af60c9c23435bf92e77a1fd1e5; the interpreter containing built-in zlib had SHA256 a92f0f95e883390c7256b2e441484aac06b1002dbe1d924141a77c8d82f96223.

The portable replay accepted eighteen cases and three controls in 10.471 seconds, with outer child/runner exit zero. Its receipt is tmp/lab-r1-package-proof-replay/replay.json; outer receipt is .research-runs/lab-r1-package-proof-replay-01/20260905T012051Z-27720/run.json. Linux memory/timeout containment was 2GiB/180seconds, with outer Windows 2GiB/200seconds. Temporary decompression directories were confirmed absent afterward; owned Windows/Linux processes were confirmed gone. This static review launched no persistent process and did not repeat the proof run.

## Git byte-portability finding

At initial inspection, proofs/*.drat.gz had text unset, but certificate.json had text unspecified. The current specification bytes are LF-only, while the repository has core.autocrlf=true. A fresh Windows checkout could therefore change the specification to CRLF and fail its hard-coded raw-byte pin.

The integration owner added `certificate.json -text` to the package-local .gitattributes. This reviewer reran git check-attr and confirmed certificate.json has text unset. The initial HOLD is cleared. The fix preserves checkout bytes without changing certificate, code, proof bytes, or mathematical meaning.
