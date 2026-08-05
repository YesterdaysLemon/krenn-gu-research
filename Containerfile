# Reproducible environment for the Krenn-Gu certificate replays.
#
# Base: Ubuntu 24.04 (noble) — the same distro as the WSL image used for
# the 2026-08-05 stabilization replays, where Singular 4.3.2 (the Ubuntu
# noble package) reproduced the ninth-component extraction ledger and both
# alternate weighted-H22 replays byte-for-byte.
#
# Build:  docker build -t kg-replay -f Containerfile .
# Use:    docker run --rm -v "$PWD":/work -w /work kg-replay \
#             python verify_support_three_p5_contraction_subrank.py
#
# Full Singular replays (hours) are manual; the image exists so that any
# documented command runs from a clean checkout with zero machine setup.
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Singular (certificate Groebner engine), python3.13 if available, else 3.12
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
