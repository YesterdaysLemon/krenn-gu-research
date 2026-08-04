#!/usr/bin/env python3
"""Record the outcome of the direct coupled_program.sing run into the
results ledger (the program was dumped by the symbolic-fitting script
in DUMP_PROGRAM mode and executed directly; this records its log)."""

import json
import sys
from pathlib import Path

base = Path(__file__).resolve().parent
log = (base / "coupled_singular_run.log")
ledger = base.parent / "special_slope_reduced_fitting_results.json"

text = log.read_text() if log.exists() else ""
dens = {
    str(m): (f"CODEX_DEN:{m}:1" in text) for m in range(4)
}
if "CODEX_RESULT:coupled:1" in text:
    status = {"result": "unit"}
elif "CODEX_RESULT:coupled:0" in text:
    status = {"result": "not-unit"}
elif text.strip():
    status = {"result": "incomplete-or-error", "tail": text[-400:]}
else:
    status = {"result": "timeout-null", "timeout_s": 560}

data = json.loads(ledger.read_text()) if ledger.exists() else {}
data["d01_coupled"] = {
    "case": "coupled",
    "direction": "01",
    "divisor": "a*f*(r+1)-(r-1)",
    "mode": 3,
    "minor_rows": [[0, 2, 4, 7], [0, 4, 5, 7]],
    "denominator_certificates_on_divisor": dens,
    "status": status,
    "note": (
        "program dumped by "
        "verify_p5_h22_disjoint_mixed_star_slope_divisor_symbolic_"
        "fitting.py (DUMP_PROGRAM mode) and executed directly; "
        "log scripts/coupled_singular_run.log"
    ),
}
ledger.write_text(json.dumps(data, indent=2) + "\n")
print(json.dumps(data["d01_coupled"], indent=2))
