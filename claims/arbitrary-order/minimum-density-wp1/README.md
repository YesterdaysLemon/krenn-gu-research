# WP1 at minimum crossing density: exact k=2 and k=3 leaves

Date: 2026-09-22. Status: **proved finite-order exclusion**, with exact
certificates and independent replay. Global Krenn--Gu remains **UNRESOLVED**.

Use the protected unit-K4 complex hollow-array conventions of
[PSMD](../PROTECTED_MINIMUM_CROSSING_DENSITY_EXCLUSION.md). A supported
crossing is a nonzero scalar entry counted once without physical
orientation. For background c, q_c counts protected M_c pairs with both
endpoints colored differently from c. WP1 imposes all macro GHZ targets
and every mixed physical zero target with min_c q_c<=1.

**Finite theorem.** At k=2 or k=3, every WP1 array has strictly more than
6k supported crossings. At equality, every surviving support has a mixed
low-q word with exactly one supported matching. The conclusion therefore
holds for arbitrary nonzero complex weights, without specialization.

The upstream singleton argument proves m>=6k and, at equality, gives 3k
protected-pair gadgets. This proof uses only macro rows. [K2_COVER](K2_COVER.md)
then exhausts all 4^6*2^6=262,144 literal supports without a symmetry
quotient. [K3_COVER](K3_COVER.md) proves the physical topology reduction,
Klein-four port quotient and necessary local gates, leaving exactly 32,768
supports; an independent checker reconstructs that entire residual set.
The [two-hidden-block lemma](TWO_HIDDEN_BLOCK.md) is an analytic gate,
including all possible exterior repairs, not a sampled exclusion.

## Certificate bridge

The two data files are intentional durable proof certificates, not raw
solver logs. The k2 binary format supplies one base3 word code for every
explicit allocation/orientation index. The k3 compressed JSONL supplies
the two configuration bit fields, support digest, low-q word and matching.
Checkers reconstruct support and count all compatible matchings exactly.
They also check the full instance cover, mixedness and low-q condition.
A count of one is a nonzero monomial for every allowed weighting, which
contradicts the associated WP1 zero equation. The owning proofs establish
that every equality candidate maps into the checked cover.

manifest.json pins the files, canonical primary source and uncompressed
k3 receipt. The [audit](AUDIT.md) distinguishes generator, checker and
analytic reduction roles. Certificate checking needs Python3.10+ and its
standard library; it does not need .NET or an external solver. Run these
commands with ordinary Python (without `-O`), because the k2 checker uses
assertions as certificate checks.

```text
python claims/arbitrary-order/minimum-density-wp1/verify_k2.py
python claims/arbitrary-order/minimum-density-wp1/verify_k3_topology.py
python claims/arbitrary-order/minimum-density-wp1/verify_two_hidden_block.py
python claims/arbitrary-order/minimum-density-wp1/audit_k3_words.py
```

Optional regeneration needs .NET10 for k2 and Python for k3. From the
repository root, with the bounded runner for the k3 producer:

```text
dotnet run --project claims/arbitrary-order/minimum-density-wp1/K2Generator -c Release -- tmp/k2-regenerated.bin
python tools/research/run_bounded.py --run-id regenerate-k3-wp1 --timeout-seconds 300 --memory-mb 8192 -- python claims/arbitrary-order/minimum-density-wp1/generate_k3_receipt.py tmp/k3-regenerated.jsonl
python claims/arbitrary-order/minimum-density-wp1/audit_k3_words.py tmp/k3-regenerated.jsonl
```

## Parent checkpoint and remaining scope

The parent is WP1=>m>6k for every k>=2 in this protected family. The
serious parent attempt in PSMD synthesized singleton supply and shared
resource exclusion, obtaining an all-order WP2 normal form and excluding
the unrestricted full source at equality. Its final mixed word has no
low-q bound, so that result does not close WP1. These already completed
finite leaves settle only k=2 and k=3 under the weaker WP1 antecedent;
they do not extrapolate to k>=4. The named downstream consumer is the
minimum-density branch of the all-order WP1 parent. No arbitrary witness
normal form, higher-density exclusion, general WP1/WP2 exclusion, or Lean
proof is supplied. This is publication of proved exhaustive covers,
not a new support census or a claim to solve the conjecture.
