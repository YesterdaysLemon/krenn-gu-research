"""Central path bootstrap for the Krenn-Gu repository migration.

Single source of truth for repository-root discovery and ``sys.path``
setup.  Moved claim-package scripts MUST call :func:`bootstrap` rather
than re-deriving the root themselves; the duplicated ``_repo_root()``
helpers from the pilot are replaced by this module.

Root discovery does NOT depend on ``.git``.  It walks upward from the
calling script until it finds a repository marker file, so it works in
clean checkouts and in source archives alike.

Typical header in a moved verifier::

    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[DEPTH] / "src"))
    from krenn_gu.bootstrap import bootstrap

    REPO_ROOT, HERE = bootstrap(__file__)

``DEPTH`` is the number of directories between the script and the
repository root (4 for ``claims/p5/h22/<family>/``, 5 for a
``.../boundaries/`` or ``.../alternate/`` subdirectory).  Scripts that
also import siblings one level up (e.g. a ``boundaries/`` verifier that
reuses the package-root verifier) pass ``also=[".."]``.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Files that exist only at the repository root.  Any one of these
# identifies the root; we do not rely on ``.git``.
_MARKERS = (
    "Containerfile",
    "requirements.lock.txt",
    "catalog/theorem-ledger.json",
)


def find_repo_root(start: Path) -> Path:
    """Walk upward from *start* until a repository marker is found.

    Raises ``RuntimeError`` if no marker is found, which indicates the
    file is not inside a repository checkout or archive.
    """
    for candidate in (start, *start.parents):
        if any((candidate / m).exists() for m in _MARKERS):
            return candidate
    raise RuntimeError(
        "could not locate the repository root above "
        f"{start}; expected one of: " + ", ".join(_MARKERS))


def bootstrap(script_file, also=()):
    """Return ``(REPO_ROOT, HERE)`` and install ``sys.path`` entries.

    ``REPO_ROOT`` is added so root-level verifier/audit modules import,
    and ``REPO_ROOT/src`` is added so ``krenn_gu`` imports.  Any
    additional directories in *also* (relative to ``HERE``) are added
    too, e.g. ``also=[".."]`` from a ``boundaries/`` script exposes the
    package root.
    """
    here = Path(script_file).resolve().parent
    repo_root = find_repo_root(here)
    dirs = [repo_root, repo_root / "src"]
    for rel in also:
        dirs.append(here / rel)
    for p in dirs:
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    return repo_root, here
