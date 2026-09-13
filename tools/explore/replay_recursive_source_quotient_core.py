"""Replay a small source-quotient/RUP certificate without a SAT executable."""

from __future__ import annotations

import argparse
import json
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf  # noqa: E402
from krenn_gu.source_quotient_core import replay_source_quotient_core  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=_BootstrapPath)
    args = parser.parse_args()
    packet = json.loads(args.certificate.read_text(encoding="utf-8"))
    instance = build_recursive_tensor_support_cnf(packet["n"], column_killers=False, fix_root_killers=False)
    print(json.dumps(replay_source_quotient_core(instance, packet), indent=2))


if __name__ == "__main__":
    main()
