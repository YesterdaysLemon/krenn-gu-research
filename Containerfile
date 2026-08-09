# Pinned Python/Singular symbolic baseline for the Krenn-Gu project.
#
# SCOPE (narrow, per the 2026-08-06 PR review): this image provides the
# symbolic-computation baseline only — Python with the pinned pip
# dependencies from requirements.lock.txt, plus Singular from the Ubuntu
# package.  It is sufficient for the sympy verifiers and the Singular
# Groebner replays.
#
# NOT PROVIDED by this image: msolve, Kissat, Glucose, drat-trim, and
# compiler tooling.  Certificate replays that need those (the SAT/DRAT
# chains) are still manual and require those tools installed
# separately.  Do not read this image as "every documented replay
# command runs with zero setup" — it is the symbolic baseline only.
#
# PYTHON VERSION CAVEAT: the image installs Ubuntu 24.04's system
# python3 (3.12 at image-build time), which is NOT necessarily the same
# interpreter as the Python 3.13 used by CI and by the machine that
# generated requirements.lock.txt.  The pinned dependencies are expected
# to install on both, but bit-exact interpreter parity is not claimed.
#
# Base: Ubuntu 24.04 (noble) — the same distro as the WSL image used for
# the 2026-08-05 stabilization replays, where Singular 4.3.2 (the Ubuntu
# noble package) reproduced the ninth-component extraction ledger and
# replayed the alternate weighted-H22 verifier and audit.
#
# Build:  docker build -t kg-symbolic -f Containerfile .
# Use:    docker run --rm -v "$PWD":/work -w /work kg-symbolic \
#             python3 claims/arbitrary-order/verify_support_three_p5_contraction_subrank.py
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Singular (certificate Groebner engine) and the system Python.
RUN apt-get update -qq \
    && apt-get install -y -qq --no-install-recommends \
        singular python3 python3-pip ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work
COPY requirements.lock.txt /opt/kg/requirements.lock.txt
RUN python3 -m pip install --break-system-packages --no-cache-dir \
        -r /opt/kg/requirements.lock.txt

# Smoke test the symbolic baseline at build time
RUN python3 -c "import sympy, numpy; print('sympy', sympy.__version__, '| numpy', numpy.__version__)"

CMD ["python3"]
