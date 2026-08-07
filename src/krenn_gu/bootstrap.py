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

Legacy bare-name imports of a module that now lives inside a moved
claim package (hyphenated directory names are not importable as
packages) are handled by :func:`expose_claim_package`, the single
shared place for that ``sys.path`` mutation (Stage 4 consolidation of
the Stage 3 per-importer shims)::

    from krenn_gu.bootstrap import bootstrap, expose_claim_package

    REPO_ROOT, HERE = bootstrap(__file__)
    expose_claim_package(REPO_ROOT, "claims/p4/components/split-pair")
    from verify_p4_split_pair_pure_component import ...
"""

from __future__ import annotations

import sys
from pathlib import Path, PurePath

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


def expose_claim_package(repo_root, rel_package_path):
    """Expose a claim package directory to legacy bare-name imports.

    Appends ``repo_root / rel_package_path`` to ``sys.path`` so modules
    inside a moved claim package (whose hyphenated directory name is not
    a Python package) keep importing by bare module name.  This is the
    single shared replacement for the per-importer ``sys.path`` shims
    that Stage 3 introduced for the moved disjoint-mixed-star package.

    *repo_root* is the resolved repository root (as returned by
    :func:`bootstrap`); *rel_package_path* is a POSIX-style path
    relative to it, e.g. ``"claims/p4/components/disjoint-mixed-star"``.
    The directory must exist; absolute paths, escapes outside the
    repository, and missing directories are refused loudly rather than
    silently leaving the import broken.  Idempotent: calling it twice
    for the same package adds the path only once.
    """
    root = Path(repo_root).resolve()
    raw = str(rel_package_path)
    # Refuse absolute paths BEFORE any normalization: "/etc/passwd" and
    # "C:\\..." must never be silently turned into repo-relative paths.
    # PurePath treats "/etc/passwd" as drive-relative on Windows, so a
    # bare leading-slash check is required alongside is_absolute().
    if PurePath(raw).is_absolute() or raw.lstrip().startswith(("/", "\\")):
        raise ValueError(
            f"claim package path must be repository-relative: "
            f"{rel_package_path!r}")
    rel = raw.replace("\\", "/").strip("/ ")
    if not rel or rel.startswith("/") or ".." in rel.split("/"):
        raise ValueError(
            f"claim package path must be repository-relative: "
            f"{rel_package_path!r}")
    pkg = (root / rel).resolve()
    try:
        pkg.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            f"claim package path escapes the repository: "
            f"{rel_package_path!r}") from exc
    if not pkg.is_dir():
        raise FileNotFoundError(
            f"claim package directory does not exist: {pkg}")
    entry = str(pkg)
    if entry not in sys.path:
        sys.path.append(entry)
    return pkg
