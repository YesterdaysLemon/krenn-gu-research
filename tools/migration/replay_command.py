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
    python -m ruff check verify_foo.py audit_foo.py
    python -m py_compile verify_foo.py audit_foo.py
    python -m unittest -v test_foo.py test_bar.py
    python -m json.tool certificate.json           JSON inspection replay
    python .\verify_foo.py                         PowerShell local path
    python \\                                      continuation line
      verify_foo.py [args]
    uv run --with sympy \\                         uv continuation line
      python verify_foo.py [args]
The script name is either a bare basename (``[A-Za-z0-9_]+\\.py``) or that
same basename behind PowerShell/POSIX's explicit current-directory prefix
(``.\\`` or ``./``).  Any other path-like script token is not a replay
command, and arbitrary fenced prose or bare filename lists never match.
"""

from __future__ import annotations

import re

# Markdown permits both backtick and tilde fences.  Rewriter and hygiene
# import this shared container grammar so replay recognition cannot diverge.
FENCE = re.compile(r"^\s*(?:`{3,}|~{3,})")

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
# QA launchers consume one or more script paths.  The suffix grammar below
# requires every token to be a script so a command is never half-rewritten.
RUFF_CHECK = re.compile(
    r"^\s*" + _COMMAND_FIELD + r"(?:" + _UV_RUN + r")?"
    r"(?:ruff\s+check|uvx\s+ruff\s+check|"
    + _PYTHON + r"\s+-m\s+ruff\s+check)\s+")
PY_COMPILE = re.compile(
    r"^\s*" + _COMMAND_FIELD + r"(?:" + _UV_RUN + r")?"
    + _PYTHON + r"\s+-m\s+py_compile\s+")
UNITTEST = re.compile(
    r"^\s*" + _COMMAND_FIELD + r"(?:" + _UV_RUN + r")?"
    + _PYTHON + r"\s+-m\s+unittest(?:\s+-v)?\s+")
JSON_TOOL = re.compile(
    r"^\s*" + _COMMAND_FIELD + r"(?:" + _UV_RUN + r")?"
    + _PYTHON + r"\s+-m\s+json\.tool\s+")
# A launcher whose command continues on the next line (`python \`).
LAUNCHER_CONTINUATION = re.compile(
    r"^\s*" + _COMMAND_FIELD
    + r"(?:(?:" + _UV_RUN + r")?" + _PYTHON + r")\s*\\$")
# A uv environment wrapper whose command continues on the next line
# (`uv run --with sympy \` with the `python ...` part on the
# following line).
LAUNCHER_UV_CONTINUATION = re.compile(
    r"^\s*" + _COMMAND_FIELD + r"(?:" + _UV_RUN + r")\\$")
# The script token: bare basename or explicit current-directory path, with
# optional trailing arguments for ordinary Python replay.
_LOCAL_PREFIX = r"(?:\.\\|\./)?"
_SCRIPT_BASENAME = r"[A-Za-z0-9_]+\.py"
SCRIPT = re.compile(
    r"^\s*" + _LOCAL_PREFIX + r"(" + _SCRIPT_BASENAME + r")(\s.*)?$")
# QA launchers may consume several scripts, but no arbitrary arguments.
QA_SCRIPTS = re.compile(
    r"^\s*(" + _LOCAL_PREFIX + _SCRIPT_BASENAME
    + r"(?:\s+" + _LOCAL_PREFIX + _SCRIPT_BASENAME + r")*)\s*$")
QA_SCRIPT_TOKEN = re.compile(
    _LOCAL_PREFIX + r"(" + _SCRIPT_BASENAME + r")")
_JSON_BASENAME = r"[A-Za-z0-9_]+\.json"
JSON_TARGET = re.compile(
    r"^\s*" + _LOCAL_PREFIX + r"(" + _JSON_BASENAME + r")\s*$")


def match_replay_targets(lines, index):
    """Parse every script target in one fenced replay command.

    Returns ``([base, ...], end_index, form)`` or ``None``.  Normal Python
    replay commands have one target; bounded Ruff/py_compile/unittest QA
    commands may have several.  A QA suffix is accepted only when every token
    is a script, which keeps rewriting atomic.
    """
    line = lines[index]
    m = LAUNCHER.match(line)
    if m:
        sm = SCRIPT.match(line[m.end():])
        if sm:
            return [sm.group(1)], index, "line"
    for launcher in (RUFF_CHECK, PY_COMPILE, UNITTEST):
        m = launcher.match(line)
        if m:
            sm = QA_SCRIPTS.match(line[m.end():])
            if sm:
                bases = [token.group(1)
                         for token in QA_SCRIPT_TOKEN.finditer(sm.group(1))]
                return bases, index, "line"
    m = JSON_TOOL.match(line)
    if m:
        jm = JSON_TARGET.match(line[m.end():])
        if jm:
            return [jm.group(1)], index, "line"
    c = LAUNCHER_CONTINUATION.match(line)
    if c and index + 1 < len(lines):
        sm = SCRIPT.match(lines[index + 1])
        if sm:
            return [sm.group(1)], index + 1, "continuation"
    u = LAUNCHER_UV_CONTINUATION.match(line)
    if u and index + 1 < len(lines):
        lm = LAUNCHER.match(lines[index + 1])
        if lm:
            sm = SCRIPT.match(lines[index + 1][lm.end():])
            if sm:
                return [sm.group(1)], index + 1, "continuation"
    return None


def match_replay(lines, index):
    """Parse a replay command opening at ``lines[index]``.

    Returns ``(base, end_index, form)`` — the bare script basename, the
    index of the last consumed line, and ``"line"`` or
    ``"continuation"`` — or ``None`` when ``lines[index]`` does not
    open a replay command.  Callers must apply this only inside fenced
    code blocks or Markdown YAML front matter; a launcher without a script
    token on the same or next line is not a command.
    """
    matched = match_replay_targets(lines, index)
    if matched is None:
        return None
    bases, end, form = matched
    # Preserve the historical single-target API.  Multi-target callers use
    # match_replay_targets directly.
    if len(bases) != 1:
        return None
    return bases[0], end, form
