"""Convert one generated P5 Singular ideal to strict msolve input."""

from __future__ import annotations

import argparse
import pathlib
import re


RING_PATTERN = re.compile(
    r"^ring r=0,\((?P<variables>[A-Za-z0-9_,]+)\),(?:dp|lp|Dp|ds);$",
    re.MULTILINE,
)
IDEAL_PATTERN = re.compile(
    r"^ideal I=(?P<equations>.*?);$\n^ideal G=",
    re.MULTILINE | re.DOTALL,
)
POLYNOMIAL_PATTERN = re.compile(r"^[A-Za-z0-9_+\-*/^()]+$")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=pathlib.Path)
    parser.add_argument("output", type=pathlib.Path)
    args = parser.parse_args()

    text = args.source.read_text(encoding="utf-8")
    ring_match = RING_PATTERN.search(text)
    ideal_match = IDEAL_PATTERN.search(text)
    if ring_match is None or ideal_match is None:
        raise ValueError("source is not a recognized generated P5 ideal")

    variables = ring_match.group("variables").split(",")
    if len(variables) != len(set(variables)):
        raise ValueError("ring repeats a variable")

    equations = ideal_match.group("equations").split(",\n")
    if not equations or any(not equation for equation in equations):
        raise ValueError("ideal has an empty equation")
    for equation in equations:
        compact = equation.replace(" ", "")
        if compact != equation:
            raise ValueError("unexpected whitespace inside an equation")
        if POLYNOMIAL_PATTERN.fullmatch(equation) is None:
            raise ValueError(f"unsupported polynomial syntax: {equation!r}")
        identifiers = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", equation))
        unknown = identifiers.difference(variables)
        if unknown:
            raise ValueError(f"unknown polynomial variables: {sorted(unknown)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        ",".join(variables)
        + "\n0\n"
        + ",\n".join(equations)
        + "\n",
        encoding="utf-8",
    )
    print(
        {
            "source": str(args.source),
            "output": str(args.output),
            "variables": len(variables),
            "equations": len(equations),
        }
    )


if __name__ == "__main__":
    main()
