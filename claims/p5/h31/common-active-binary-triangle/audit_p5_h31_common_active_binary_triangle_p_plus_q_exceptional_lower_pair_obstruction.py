#!/usr/bin/env python3
"""Independent no-import audit of exceptional lower-pair H31 certificates."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT
NOTE = HERE / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_LOWER_PAIR_OBSTRUCTION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))


def git_commit() -> str:
    result = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def permanent(rows):
    state = {0: sp.Integer(1)}
    for row in rows:
        nxt = {}
        for mask, coefficient in state.items():
            for column, entry in enumerate(row):
                if not mask & (1 << column):
                    key = mask | (1 << column)
                    nxt[key] = nxt.get(key, 0) + coefficient * entry
        state = nxt
    return sp.expand(state[15])


def add(u, v):
    return tuple(sp.expand(a + b) for a, b in zip(u, v))


def scale(c, u):
    return tuple(sp.expand(c * a) for a in u)


def bases(x, y, gamma=None):
    e, ell, em, cap_c = (1, 0, 0, 0), (0, 1, -1, 0), (0, 1, 1, 0), (0, 0, 0, 1)
    w = add(scale(x, ell), scale(y, em))
    alpha = (e, em, e, add(cap_c, scale(-1, w)))
    last = ell if gamma is None else add(ell, scale(gamma, e))
    return alpha, (ell, e, add(cap_c, w), last)


def mark(alpha, beta, h):
    return tuple(add(beta[i], scale(h[i], alpha[i])) for i in range(4))


def matrices(d, alpha, beta):
    z = sp.symbols("u0:8")
    retained = tuple(i for i in range(4) if i != d)
    aa = tuple(tuple(row[i] for i in retained) + (z[m],) for m, row in enumerate(alpha))
    bb = tuple(tuple(row[i] for i in retained) + (z[4 + m],) for m, row in enumerate(beta))
    rows = {}
    for word in WORDS:
        coefficient = permanent(tuple(bb[m] if word[m] else aa[m] for m in range(4)))
        rows[word] = [sp.diff(coefficient, variable) for variable in z]
    mixed = sp.Matrix([rows[word] for word in WORDS if word not in ((0, 0, 0, 0), (1, 1, 1, 1))])
    return mixed, sp.Matrix([rows[(0, 0, 0, 0)]]), sp.Matrix([rows[(1, 1, 1, 1)]])


def marked_map(mode, alpha, beta):
    answer = []
    for bits in itertools.product((0, 1), repeat=3):
        selected, cursor = [], 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        answer.append([
            permanent(tuple(
                tuple(int(i == coordinate) for i in range(4)) if other == mode else selected[other]
                for other in range(4)
            )) for coordinate in range(4)
        ])
    return sp.Matrix(answer)


def lifted_map(d, extension, alpha, beta):
    retained = tuple(i for i in range(4) if i != d)
    aa = tuple(tuple(row[i] for i in retained) + (extension[m],) for m, row in enumerate(alpha))
    bb = tuple(tuple(row[i] for i in retained) + (extension[4 + m],) for m, row in enumerate(beta))
    return marked_map(1, aa, bb)


def pure_audit():
    x, y, gamma = sp.symbols("x y gamma")
    for alpha, beta in (bases(x, y), bases(x, y, gamma)):
        coefficients = {
            word: sp.factor(permanent(tuple(beta[m] if word[m] else alpha[m] for m in range(4))))
            for word in WORDS
        }
        assert coefficients[(1, 1, 1, 1)] == -2
        assert all(value == 0 for word, value in coefficients.items() if word != (1, 1, 1, 1))
    ell, last = (0, 1, -1, 0), (0, -y, -y, 1)
    wedge = tuple(sp.factor(ell[i] * last[j] - ell[j] * last[i]) for i, j in itertools.combinations(range(4), 2))
    assert wedge == (0, 0, 0, -2 * y, 1, -1)
    return {"pure_support": "1111", "coefficient": -2, "baseline_V3_pluecker": list(map(str, wedge))}


def branch(name, alpha, beta, d, h, rank, fa, fb, fm, rows, transverse):
    beta_h = mark(alpha, beta, h)
    mixed, diagonal_a, diagonal_b = matrices(d, alpha, beta_h)
    assert mixed.rank() == rank
    kernel = mixed.nullspace()
    assert len(kernel) == 8 - rank
    frame = sp.Matrix.hstack(*kernel)
    assert frame.rank() == len(kernel) and all(sp.factor(v) == 0 for v in mixed * frame)
    c = sp.symbols(f"c0:{len(kernel)}")
    extension = frame * sp.Matrix(c)
    actual_a = sp.factor((diagonal_a * extension)[0])
    actual_b = sp.factor((diagonal_b * extension)[0])
    minor = sp.factor(lifted_map(d, extension, alpha, beta_h).extract(rows, range(4)).det())
    assert sp.factor(actual_a - fa(*c)) == 0
    assert sp.factor(actual_b - fb(*c)) == 0
    assert sp.factor(minor - fm(*c)) == 0
    tr, tc, tv = transverse
    assert sp.factor(marked_map(1, alpha, beta_h)[tr, tc] - tv) == 0
    return {"branch": name, "rank": rank, "nullity": len(kernel), "kernel": [[str(sp.factor(v)) for v in k] for k in kernel], "A": str(actual_a), "B": str(actual_b), "minor": str(minor)}


def no_neighbour(name, alpha, beta, h, rank):
    mixed, diagonal_a, _ = matrices(3, alpha, mark(alpha, beta, h))
    assert mixed.rank() == rank
    kernel = mixed.nullspace()
    assert len(kernel) == 8 - rank
    assert all(sp.factor((diagonal_a * vector)[0]) == 0 for vector in kernel)
    return {"branch": name, "rank": rank, "nullity": len(kernel), "A_on_kernel": "zero"}


def branches():
    x, y, gamma, t = sp.symbols("x y gamma t", nonzero=True)
    ba, bb = bases(x, y)
    wa, wb = bases(x, y, gamma)
    out = [
        branch("baseline-d1", ba, bb, 1, (t, 0, 0, 0), 5, lambda X, Y, Z: -2*X, lambda X, Y, Z: -2*(X*t+Z), lambda X, Y, Z: 8*X**2*(X*t+Z), (0,1,3,7), (3,1,-1)),
        branch("baseline-d2", ba, bb, 2, (t, 0, 0, 0), 5, lambda X, Y, Z: -2*X, lambda X, Y, Z: 2*(X*t+Z), lambda X, Y, Z: -8*X**2*(X*t+Z), (0,1,3,7), (3,2,1)),
        branch("baseline-d3", ba, bb, 3, (0,0,0,0), 6, lambda X,Y: 4*X*y, lambda X,Y: -2*Y, lambda X,Y: 32*X**2*Y*y, (0,1,5,7), (5,3,-2)),
        branch("baseline-d3-x=y", *bases(y,y), 3, (t,0,0,0), 6, lambda X,Y: 4*X*y, lambda X,Y: -2*(2*X*t*y+Y), lambda X,Y: 32*X**2*y*(2*X*t*y+Y), (0,1,5,7), (5,3,-2)),
        branch("baseline-d3-x=-y", *bases(-y,y), 3, (t,0,0,0), 6, lambda X,Y: 4*X*y, lambda X,Y: 2*(2*X*t*y-Y), lambda X,Y: -32*X**2*y*(2*X*t*y-Y), (0,1,5,7), (5,3,-2)),
        branch("baseline-d3-x=0", *bases(0,y), 3, (0,0,t,0), 6, lambda X,Y: 4*X*y, lambda X,Y: -2*(X*t+Y), lambda X,Y: 32*X**2*y*(X*t+Y), (0,1,5,7), (5,3,-2)),
        branch("wall-d1", wa, wb, 1, (0,0,0,0), 5, lambda X,Y,Z: -2*X, lambda X,Y,Z: -2*Z, lambda X,Y,Z: 8*X**2*Z, (0,1,3,7), (3,1,-1)),
        branch("wall-d2", wa, wb, 2, (0,0,0,0), 5, lambda X,Y,Z: -2*X, lambda X,Y,Z: 2*Z, lambda X,Y,Z: -8*X**2*Z, (0,1,3,7), (3,2,1)),
        branch("wall-d3", wa, wb, 3, (0,0,0,0), 6, lambda X,Y: 4*Y*y/gamma, lambda X,Y: -2*(X+2*Y*x), lambda X,Y: 32*Y**2*y*(X+2*Y*x)/gamma**2, (0,1,5,7), (5,3,-2)),
        branch("wall-d3-x=0", *bases(0,y,gamma), 3, (0,0,t,0), 6, lambda X,Y: 4*Y*y/gamma, lambda X,Y: -2*(X*gamma+Y*t)/gamma, lambda X,Y: 32*Y**2*y*(X*gamma+Y*t)/gamma**3, (0,1,5,7), (5,3,-2)),
    ]
    xx = sp.Symbol("xx", nonzero=True)
    out.extend((
        no_neighbour("baseline-y0", *bases(xx,0), (0,0,0,0), 4),
        no_neighbour("baseline-origin-h0", *bases(0,0), (t,0,0,0), 2),
        no_neighbour("baseline-origin-h2", *bases(0,0), (0,0,t,0), 2),
        no_neighbour("wall-y0", *bases(xx,0,gamma), (0,0,0,0), 4),
        no_neighbour("wall-origin-h2", *bases(0,0,gamma), (0,0,t,0), 2),
    ))
    return out


def singular_spot(family, expected):
    h = sp.symbols("h0:4")
    z = sp.symbols("z0:8")
    x, y, gamma, winv, ginv = sp.symbols("x y gamma winv ginv")
    alpha, beta = bases(x, y, gamma if family == "wall" else None)
    mixed, aa, bb = matrices(3, alpha, mark(alpha, beta, h))
    extension = sp.Matrix(z)
    equations = [*tuple(mixed*extension), (aa*extension)[0]-1, winv*(bb*extension)[0]-1]
    eliminated = z + (winv,)
    parameters = h + (x,y)
    blocks = "(dp(9),dp(4),dp(2))"
    if family == "wall":
        equations.append(ginv*gamma-1); eliminated += (ginv,); parameters += (gamma,); blocks = "(dp(10),dp(4),dp(3))"
    conv = lambda value: str(sp.cancel(value)).replace("**", "^")
    program = "\n".join((
        "ring r=0,("+",".join(map(str,eliminated+parameters))+"),"+blocks+";", "option(redSB);",
        "ideal I="+",".join(map(conv,equations))+";", "I=slimgb(I);",
        "ideal J=std(eliminate(I,"+"*".join(map(str,eliminated))+"));",
        "ideal E="+",".join(map(conv,expected))+";", "E=std(E);",
        "ideal L=simplify(reduce(J,E),2);", "ideal R=simplify(reduce(E,J),2);",
        '"AUDIT:"+string((size(L)==0)&&(size(R)==0));', "quit;",
    ))
    command = (shutil.which("Singular"), "-q") if shutil.which("Singular") else ("wsl.exe","--exec","/usr/bin/Singular","-q")
    result = subprocess.run(
        command,
        input=program,
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0 and "AUDIT:1" in result.stdout and not result.stderr.strip(), result
    return {"family": family, "distinguished": 3, "ideal": list(map(conv,expected)), "bidirectional_equality": True}


def main():
    h0,h1,h2,h3,x,y = sp.symbols("h0 h1 h2 h3 x y")
    projections = [
        singular_spot("baseline", (h3,h1,(x**2-y**2)*h0+x*h2,x*h2**2,h0*h2)),
        singular_spot("wall", (h0,h1,h3,x*h2)),
    ]
    result = {
        "status": "pass", "claim_label": "VERIFIED", "verified_pass": True,
        "role": "verifier",
        "date_utc": datetime.now(UTC).isoformat(), "git_commit": git_commit(),
        "scope": "independent reconstruction of component-15 exceptional lower-pair H31 fibres at a=0,-1",
        "inputs": {NOTE.name: hashlib.sha256(NOTE.read_bytes()).hexdigest()},
        "method": "no-import permanent construction, exact kernel replay, and independent elimination spot audits",
        "command": "uv run --with sympy python claims/p5/h31/common-active-binary-triangle/audit_p5_h31_common_active_binary_triangle_p_plus_q_exceptional_lower_pair_obstruction.py",
        "outputs": {},
        "limitations": "verified only for exceptional component-15 diagonal-DVR H31 fibres; H22, arbitrary GL4, local-to-global, and the global conjecture remain open",
        "independent_code_path": True, "imports_primary_or_helper": False,
        "field": "Q(parameters), characteristic zero", "geometry": pure_audit(),
        "projection_spot_audits": projections, "branches": branches(),
        "finite_field_computation": False,
        "fresh_independent_verifier_complete": True,
        "theorem": NOTE.name, "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
        "source": Path(__file__).name, "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
