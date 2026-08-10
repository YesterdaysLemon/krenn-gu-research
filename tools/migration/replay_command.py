"""Shared fenced replay-command parsing for the migration machinery.

The rewriter (``rewrite_links.py``) and the stale-reference scanner
(``check_hygiene.py``) must agree exactly on what counts as a fenced
replay command.  Stage 4 proved that two separate patterns drift: both
machines missed the ``uv run`` wrapper and the continuation-line form,
and four real replay commands had to be repaired by hand.  This module
is the single source of truth for that grammar.

Recognized forms (inside fenced code blocks or Markdown YAML front matter;
callers enforce the container state):

    python verify_foo.py [args]                   single line
    python3 verify_foo.py / wsl ... python3 ...   single line
    uv run --with sympy python verify_foo.py      uv environment wrap
    command: uv run ... python verify_foo.py      YAML evidence field
    uv run --with ruff ruff check verify_foo.py   lint replay
    python -m py_compile verify_foo.py             compile replay
    python \\                                      continuation line
      verify_foo.py [args]
    uv run --with sympy \\                         uv continuation line
      python verify_foo.py [args]
The script name is always a bare basename (``[A-Za-z0-9_]+\\.py``);
anything path-like on the script position is not a replay command, and
arbitrary fenced prose or bare filename lists never match.
"""

from __future__ import annotations

import re

# Optional uv environment wrapper: `uv run` plus any `--flag [value]`
# pairs, as in `uv run --with sympy python ...`.
_UV_RUN = r"uv\s+run\s+(?:--\S+(?:\s+(?!-)\S+)?\s+)*"
# The python launcher itself, optionally behind a wsl wrapper.
_PYTHON = r"(?:wsl[^\n]*python3?|python3?)"
# Evidence reports often store the exact replay in a fenced YAML header.
# Treat its ``command:`` value as executable replay metadata, while keeping
# arbitrary YAML fields and prose outside the grammar.
_COMMAND_FIELD = r"(?:command\s*:\s*)?"
# A complete launcher prefix ending in whitespace.
LAUNCHER = re.compile(
    r"^\s*" + _COMMAND_FIELD
    + r"(?:(?:" + _UV_RUN + r")?" + _PYTHON + r")\s+")
# QA launchers that consume exactly one moved script path.  Multi-target QA
# lines require a separate token-preserving rewrite and are deliberately not
# partially rewritten by this grammar.
RUFF_CHECK = re.compile(
    r"^\s*(?:(?:" + _UV_RUN + r")?ruff\s+check)\s+")
PY_COMPILE = re.compile(
    r"^\s*" + _PYTHON + r"\s+-m\s+py_compile\s+")
# A launcher whose command continues on the next line (`python \`).
LAUNCHER_CONTINUATION = re.compile(
    r"^\s*" + _COMMAND_FIELD
    + r"(?:(?:" + _UV_RUN + r")?" + _PYTHON + r")\s*\\$")
# A uv environment wrapper whose command continues on the next line
# (`uv run --with sympy \` with the `python ...` part on the
# following line).
LAUNCHER_UV_CONTINUATION = re.compile(
    r"^\s*" + _COMMAND_FIELD + r"(?:" + _UV_RUN + r")\\$")
# The script token: bare basename, optional trailing arguments.
SCRIPT = re.compile(r"^\s*([A-Za-z0-9_]+\.py)(\s.*)?$")
# The bounded QA forms repaired in Stage 31 have exactly one script and no
# trailing arguments.  This prevents a line containing two script targets
# from being half-rewritten.
QA_SCRIPT = re.compile(r"^\s*([A-Za-z0-9_]+\.py)\s*$")


def match_replay(lines, index):
    """Parse a replay command opening at ``lines[index]``.

    Returns ``(base, end_index, form)`` — the bare script basename, the
    index of the last consumed line, and ``"line"`` or
    ``"continuation"`` — or ``None`` when ``lines[index]`` does not
    open a replay command.  Callers must apply this only inside fenced
    code blocks or Markdown YAML front matter; a launcher without a script
    token on the same or next line is not a command.
    """
    line = lines[index]
    m = LAUNCHER.match(line)
    if m:
        sm = SCRIPT.match(line[m.end():])
        if sm:
            return sm.group(1), index, "line"
    for launcher in (RUFF_CHECK, PY_COMPILE):
        m = launcher.match(line)
        if m:
            sm = QA_SCRIPT.match(line[m.end():])
            if sm:
                return sm.group(1), index, "line"
    c = LAUNCHER_CONTINUATION.match(line)
    if c and index + 1 < len(lines):
        sm = SCRIPT.match(lines[index + 1])
        if sm:
            return sm.group(1), index + 1, "continuation"
    u = LAUNCHER_UV_CONTINUATION.match(line)
    if u and index + 1 < len(lines):
        lm = LAUNCHER.match(lines[index + 1])
        if lm:
            sm = SCRIPT.match(lines[index + 1][lm.end():])
            if sm:
                return sm.group(1), index + 1, "continuation"
    return None
