import json
from pathlib import Path

p = Path(__file__).resolve().parent.parent / (
    "special_slope_reduced_fitting_results.json"
)
d = json.loads(p.read_text())
d["d01_coupled"]["status"] = {
    "result": "timeout-null",
    "detail": (
        "main Groebner killed at the ~560 s budget; the four "
        "on-divisor denominator unit certificates passed "
        "(CODEX_DEN markers in scripts/coupled_singular_run.log)"
    ),
}
p.write_text(json.dumps(d, indent=2) + "\n")
print(json.dumps(d["d01_coupled"]["status"], indent=2))
