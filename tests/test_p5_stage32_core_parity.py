"""Bounded parity guards for the Stage 32 inverse-taper extractions."""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

import sympy as sp

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from claims.finite.n12 import (  # noqa: E402
    twelve_vertex_complement_chain_orbits_core as n12,
)
from krenn_gu import p5_exact_three_support_system as exact_three  # noqa: E402
from krenn_gu import p5_exact_two_support_system as exact_two  # noqa: E402
from krenn_gu import p5_high_coordinate as high  # noqa: E402
from krenn_gu import p5_marked_basis as marked  # noqa: E402
from krenn_gu import p5_pair_catalogue as pair_catalogue  # noqa: E402
from krenn_gu import p5_q5_311_program as q5_program  # noqa: E402
from krenn_gu import p5_q5_311_support as q5_support  # noqa: E402
from krenn_gu import p5_split_saturation as split  # noqa: E402
from krenn_gu import p5_support_system as exact_one  # noqa: E402


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_json(value) -> str:
    return digest_bytes(
        json.dumps(value, separators=(",", ":")).encode("utf-8")
    )


class Stage32CoreParityTests(unittest.TestCase):
    def test_marked_basis_public_api_and_symbolic_fixtures(self) -> None:
        self.assertEqual(
            marked.__all__,
            ["marked_extension", "mixed_matrix", "one_marked_map", "permanent"],
        )
        alpha = (
            (1, 0, 2, -1),
            (0, 1, 1, 2),
            (2, -1, 0, 1),
            (1, 2, -2, 0),
        )
        beta = (
            (0, 2, 1, 1),
            (1, -1, 2, 0),
            (2, 1, 0, -1),
            (-1, 0, 1, 2),
        )
        extension = sp.Matrix(sp.symbols("z0:8"))
        rows = (
            (1, 2, 0, -1),
            (0, 1, 3, 2),
            (2, -2, 1, 0),
            (1, 0, 2, 1),
        )

        def entries(matrix: sp.MatrixBase) -> list[str]:
            return [str(sp.expand(value)) for value in list(matrix)]

        self.assertEqual(marked.permanent(rows), 20)
        self.assertEqual(
            digest_json(str(marked.permanent(rows))),
            "046419ca5ecebeb34fdfe9dde8106ccee5ce39f8e4dd115e8ef20b869f8bed82",
        )
        self.assertEqual(
            digest_json(entries(marked.one_marked_map(1, alpha, beta))),
            "bd26dd704ec72ae244555fd41f39ea84cbb35ae3cd655eb1173bf80084df2f31",
        )
        self.assertEqual(
            digest_json(
                entries(marked.marked_extension(2, extension, alpha, beta, 3))
            ),
            "c5c3d8add23dbd855e755a819dbacd06a5537d1c0ffa6329df2716f3609954bf",
        )
        self.assertEqual(
            digest_json([entries(matrix) for matrix in marked.mixed_matrix(2, alpha, beta)]),
            "bcd2e3c3b557be935f9777c1fbfc67c6a37d92d2e96664dc9416886c2b570b50",
        )

    def test_support_generators_match_frozen_programs(self) -> None:
        supports = (
            (1, 2, 4, 3, 7),
            (7, 1, 2, 4, 7),
            (7, 7, 1, 2, 4),
            (4, 7, 7, 1, 2),
            (2, 4, 7, 7, 1),
        )
        indices = (0, 1, 2, 3, 4)
        exact_two_supports = tuple(
            tuple(5 if (row, column) == (0, 4) else value for column, value in enumerate(values))
            for row, values in enumerate(supports)
        )
        exact_three_supports = tuple(
            tuple(6 if (row, column) == (1, 0) else value for column, value in enumerate(values))
            for row, values in enumerate(exact_two_supports)
        )
        fixtures = (
            (
                exact_one.generate(supports, indices),
                "858a186dc3c201f3469a54d1fd7761283345dbcff81a69e12fd2483ea2c9eb77",
                (44, 25, 25, 25, 224, 3),
            ),
            (
                exact_two.generate(exact_two_supports, indices),
                "a205705b4dd62ff375e85559008408ab3a9fc0076b76017585e9ae7c004a1234",
                (43, 24, 24, 24, 207, 3),
            ),
            (
                exact_three.generate(exact_three_supports, indices),
                "78037b864dea60d5b9fc10ac745fd4598beb8205a7fcd141277d518d76f6508e",
                (42, 23, 23, 23, 193, 3),
            ),
        )
        keys = (
            "nonzero_entries",
            "gauge_free_variables",
            "laurent_parameters",
            "saturated_parameters",
            "mixed_equations",
            "pure_coefficients",
        )
        for (program, metadata), expected_hash, expected_metadata in fixtures:
            self.assertEqual(digest_bytes(program.encode("utf-8")), expected_hash)
            self.assertEqual(tuple(metadata[key] for key in keys), expected_metadata)

    def test_split_saturation_fixture(self) -> None:
        source = """// distinct mixed equations: 1
// explicit binomial equations: 0
// saturated parameters: 2
ring r=0,(a,b,z),dp;
option(redSB);
ideal I=a+b,
z*(a*b*(a+b)*(a-b)*(a+2*b))-1;
ideal G=slimgb(I);
if (size(G)==1 && G[1]==1) { "UNIT_IDEAL"; }
else { "SURVIVOR"; size(G); vdim(G); }
$;
"""
        self.assertEqual(split.__all__, ["IDENTIFIER_PATTERN", "convert_text"])
        self.assertEqual(
            digest_bytes(split.convert_text(source).encode("utf-8")),
            "cf0f03255973751e17ac5c7bf83009520127cc3ad85b7d7396858bf47ebcd6f9",
        )
        self.assertEqual(
            digest_bytes(split.convert_text(source, "std").encode("utf-8")),
            "373c155cfc4eadb7202184992fa1a55fedcb31b90bf27566c4a13b2bf85d247e",
        )

    def test_high_coordinate_and_q5_program_fixtures(self) -> None:
        closure = ((1, 1, 1, 2, 4),) + ((7, 7, 7, 7, 7),) * 4
        edges = high.support_edges(closure)
        tree = high.gauge_tree(closure, closure)
        self.assertEqual((len(edges), len(tree)), (65, 19))
        self.assertEqual(
            digest_json(edges),
            "468d0cb88462a72c2b2ada626608998aeed4ea4ef21912e6f5ba7b8bd0fdb3a8",
        )
        self.assertEqual(
            digest_json(tree),
            "bd8a3b36c44c024bf41160206e2f45865c85b67ffe8491239c06c5ef28481437",
        )
        self.assertEqual(high.validate_forest(closure, closure, tree), (1, 1))
        stabilizer_hashes = {
            "q4_211": "7097c8c5b7a38ed8d2f3fb92d5599d53bdb482cd51851bfbb37bc003a4e9412f",
            "q5_311": "de077811a7a3d629b6000832f24c5bab5115ec043900d158867a51927b39170e",
            "q5_221": "8584e694cf0f6f500a8c29886a66495e1c428de9a147da7b8dd69571bad080d5",
        }
        for branch, expected in stabilizer_hashes.items():
            self.assertEqual(digest_json(high.source_colour_stabilizer(branch)), expected)

        record = {
            "supports": closure,
            "closure_supports": closure,
            "gauge_tree": tree,
        }
        program, split_program, metadata = q5_program.build_program(record)
        self.assertEqual(
            digest_bytes(program.encode("utf-8")),
            "0d932eae6916e48138ef9949db5cf384211f862d41d63b29a92ffc8f20a9e184",
        )
        self.assertEqual(
            digest_bytes(split_program.encode("utf-8")),
            "02750170093d04c419fdb4ee9003de471c28056ed61d5ea86719c5e5dec41204",
        )
        self.assertEqual(
            (
                metadata["closure_entries"],
                metadata["gauge_forest_edges"],
                metadata["variables"],
                metadata["rare_mixed_equations"],
                metadata["saturated_pure_colours"],
            ),
            (65, 19, 47, 160, (1, 2)),
        )

    def test_q5_support_words(self) -> None:
        rare = q5_support.rare_mixed_colourings()
        self.assertEqual((len(rare), rare[0], rare[-1]), (160, (1, 0, 0, 0, 0), (2, 2, 2, 2, 1)))
        self.assertEqual(
            digest_json(rare),
            "1d92fda2b5c7d538bbba2a023945decc68d9c24cc841332be6c427a094fb08a8",
        )

    def test_pair_catalogue_fixture(self) -> None:
        catalogue = pair_catalogue.finite_field_local_signatures()
        self.assertEqual(len(catalogue), 6495)
        self.assertEqual(
            digest_json(catalogue),
            "432ca246fb57f11fe7e9a66db9762f21217477fc2a9b22c1abb69a37aef6b18f",
        )

    def test_n12_orbit_core_fixtures(self) -> None:
        variables = n12.membership_variables()
        leaves = n12.canonical_leaves()
        self.assertEqual((len(variables), len(leaves)), (2769, 16))
        self.assertEqual(sum(leaf["orbit_weight"] for leaf in leaves), 120)
        self.assertEqual(
            digest_json(sorted((colour, mask, value) for (colour, mask), value in variables.items())),
            "9598d1f03fce246c8cdad8e7f9c65b58695edf046a939725838bf2bfe6415d1d",
        )
        self.assertEqual(
            digest_json(leaves),
            "d4ec7aeec24bdf0f751a12c6c649130837488f1a0be1cc6f1382bc42e9c9ee3d",
        )
        records = []
        for leaf in leaves:
            assumptions, pair_masks, suffix_masks = n12.chain_assumptions(
                variables, leaf["pairs"]
            )
            records.append(
                {
                    "partner_permutation": leaf["partner_permutation"],
                    "orbit_weight": leaf["orbit_weight"],
                    "assumptions": assumptions,
                    "pair_masks": pair_masks,
                    "suffix_masks": suffix_masks,
                }
            )
        self.assertEqual(
            digest_json(records),
            "cdcc44c30a1c728d6c8efe92c6fbeac2de08ef38e8ad66e9d9a7b3a7526bc437",
        )


if __name__ == "__main__":
    unittest.main()
