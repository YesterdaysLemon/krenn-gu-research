"""Convert a P5 product-saturation Singular program to split saturation."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


RING_PATTERN = re.compile(
    r"^ring r=0,\((?P<variables>[A-Za-z0-9_,]+)\),(?:dp|lp|Dp|ds);$",
    re.MULTILINE,
)
IDEAL_PATTERN = re.compile(
    r"^ideal I=(?P<equations>.*?);$\n^ideal G=",
    re.MULTILINE | re.DOTALL,
)
MIXED_COUNT_PATTERN = re.compile(
    r"^// distinct mixed equations: (?P<count>[0-9]+)$",
    re.MULTILINE,
)
RELATION_COUNT_PATTERN = re.compile(
    r"^// explicit binomial equations: (?P<count>[0-9]+)$",
    re.MULTILINE,
)
SATURATED_COUNT_PATTERN = re.compile(
    r"^// saturated parameters: (?P<count>[0-9]+)$",
    re.MULTILINE,
)
IDENTIFIER_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def split_top_level_product(expression: str) -> list[str]:
    factors = []
    depth = 0
    start = 0
    for index, character in enumerate(expression):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth < 0:
                raise ValueError("unbalanced saturation parentheses")
        elif character == "*" and depth == 0:
            factors.append(expression[start:index])
            start = index + 1
    if depth:
        raise ValueError("unbalanced saturation parentheses")
    factors.append(expression[start:])
    if any(not factor for factor in factors):
        raise ValueError("empty saturation factor")
    return factors


def convert_text(text: str, algorithm: str = "slimgb") -> str:
    if algorithm not in ("slimgb", "std"):
        raise ValueError("unsupported Singular basis algorithm")
    normalized = text.replace("\r\n", "\n")
    if "\r" in normalized or not normalized.endswith("$;\n"):
        raise ValueError("incomplete or non-LF Singular source")
    ring_match = RING_PATTERN.search(normalized)
    ideal_match = IDEAL_PATTERN.search(normalized)
    mixed_match = MIXED_COUNT_PATTERN.search(normalized)
    relation_match = RELATION_COUNT_PATTERN.search(normalized)
    saturated_match = SATURATED_COUNT_PATTERN.search(normalized)
    if (
        ring_match is None
        or ideal_match is None
        or mixed_match is None
        or relation_match is None
    ):
        raise ValueError("unrecognized Singular source")

    variables = ring_match.group("variables").split(",")
    equations = ideal_match.group("equations").split(",\n")
    expected = (
        int(mixed_match.group("count"))
        + int(relation_match.group("count"))
        + 1
    )
    if len(equations) != expected:
        raise ValueError("equation count does not match source metadata")
    parameters = variables[:-1]
    rabinowitsch = variables[-1]
    saturation = equations[-1]
    prefix = f"{rabinowitsch}*("
    if not saturation.startswith(prefix) or not saturation.endswith(")-1"):
        raise ValueError("unrecognized saturation equation")
    factors = split_top_level_product(saturation[len(prefix) : -3])
    saturated_count = (
        int(saturated_match.group("count"))
        if saturated_match is not None
        else len(parameters)
    )
    saturated_parameters = factors[:saturated_count]
    if (
        len(factors) != saturated_count + 3
        or len(set(saturated_parameters)) != saturated_count
        or any(
            parameter not in parameters
            for parameter in saturated_parameters
        )
    ):
        raise ValueError("unexpected saturation factors")

    safe_parameters = [
        f"v{index:02d}" for index in range(len(parameters))
    ]
    safe_name = dict(zip(parameters, safe_parameters, strict=True))
    safe_mixed = [
        IDENTIFIER_PATTERN.sub(
            lambda match: safe_name[match.group(0)],
            equation,
        )
        for equation in equations[:-1]
    ]
    safe_factors = [
        IDENTIFIER_PATTERN.sub(
            lambda match: safe_name[match.group(0)],
            factor,
        )
        for factor in factors
    ]
    inverse_variables = [
        f"w{index:02d}" for index in range(len(safe_factors))
    ]
    inverse_equations = [
        f"{inverse}*({factor})-1"
        for inverse, factor in zip(
            inverse_variables,
            safe_factors,
            strict=True,
        )
    ]
    return "\n".join(
        [
            "// exact split-saturation conversion",
            (
                "ring r=0,("
                + ",".join(safe_parameters + inverse_variables)
                + "),dp;"
            ),
            "option(redSB);",
            "ideal I="
            + ",\n".join(inverse_equations + safe_mixed)
            + ";",
            f"ideal G={algorithm}(I);",
            'if (size(G)==1 && G[1]==1) { "UNIT_IDEAL"; }',
            'else { "SURVIVOR"; size(G); vdim(G); }',
            "$;",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--algorithm",
        choices=("slimgb", "std"),
        default="slimgb",
    )
    args = parser.parse_args()
    converted = convert_text(
        args.input.read_text(encoding="utf-8"),
        args.algorithm,
    )
    args.output.write_text(
        converted,
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
