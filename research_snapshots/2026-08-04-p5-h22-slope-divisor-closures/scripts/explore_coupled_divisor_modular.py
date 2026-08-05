#!/usr/bin/env python3
"""Modular survey ON the coupled divisor af(r+1)-(r-1)=0 of the D_01
pencil (disjoint mixed-star component).  At the sample points the
divisor slope is r = (af+1)/(1-af) mod p: r=6 at p=11 (a=1,f=7),
r=5 at p=13 (a=1,f=5)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from explore_p5_h22_disjoint_mixed_star_slope_divisors_modular import (
    SAMPLES,
    survey,
)


def main():
    out = []
    for p in (11, 13):
        a, b, f, phi = SAMPLES[p]
        af = a * f % p
        r = (af + 1) * pow(1 - af, -1, p) % p
        assert (a * f * (r + 1) - (r - 1)) % p == 0
        res = survey(p, "01", r)
        res["divisor"] = "af(r+1)-(r-1)=0"
        out.append(res)
        print(
            f"[p={p} D_01 r={r} on divisor] kernel markings "
            f"{res['markings_with_kernel']}, survivors "
            f"{res['survivor_markings']}, genuine "
            f"{res['genuine_directions_total']}, min marked ranks "
            f"{res['min_marked_rank_per_mode']}, both-minors-vanish "
            f"{res['fitting_both_minors_vanish_count']}"
        )
        print("  survivor t patterns:", res["survivor_t_patterns"])
        print("  sample:", res["survivors_sample"][:12])
    path = Path(__file__).resolve().parent.parent / (
        "coupled_divisor_modular_survey.json"
    )
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
