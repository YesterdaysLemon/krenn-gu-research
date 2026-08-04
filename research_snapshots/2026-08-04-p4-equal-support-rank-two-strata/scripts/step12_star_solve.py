#!/usr/bin/env python3
"""Solve the star-purity geometric system for (e1,e2,e3) over Q(n2,n3)."""
import json, subprocess, pathlib

data = json.loads(pathlib.Path("star_purity_data.json").read_text())
G = [g.replace("**", "^") for g in data["G"]]
polys = ";\n".join(f"poly g{i}={g}" for i, g in enumerate(G))
program = "\n".join((
    'LIB "primdec.lib";',
    "ring R=(0,n2,n3),(e1,e2,e3),lp;",
    polys + ";",
    "ideal I=" + ",".join(f"g{i}" for i in range(len(G))) + ";",
    "ideal J=std(I);",
    '"CODEX_DIM:"+string(dim(J));',
    "list L=minAssGTZ(I);",
    '"CODEX_NCOMP:"+string(size(L));',
    "for (int k=1; k<=size(L); k++) { \"CODEX_COMP\"+string(k); std(L[k]); }",
    "quit;",
))
completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                           encoding="utf-8", errors="replace",
                           capture_output=True, timeout=560, check=False)
print(completed.stdout)
if completed.stderr.strip():
    print("STDERR:", completed.stderr[-2000:])
