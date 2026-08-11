#!/usr/bin/env python3
"""Inventory persistent identifiers and validate literature source records.

This tool is deliberately offline. It validates recorded provenance but never
contacts a metadata provider or infers what a source or passage establishes.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date
import ipaddress
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Iterable
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
DEFAULT_REGISTRY = REPO_ROOT / "catalog" / "literature" / "sources.json"

USAGE_INSPECTION_LEVELS = {
    "metadata_only",
    "abstract_inspected",
    "relevant_passage_inspected",
}
USAGE_ROLES = {"background", "novelty_assessment", "imported_result"}
IDENTIFIER_KEYS = {"doi", "arxiv", "eudml", "stacks_tag"}

CITEKEY_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
ARXIV_RE = re.compile(
    r"(?:arxiv\s*:\s*|arxiv\.org/(?:abs|pdf)/)"
    r"(?P<identifier>(?:[a-z-]+(?:\.[a-z]{2})?/\d{7}|"
    r"\d{4}\.\d{4,5})(?:v\d+)?)",
    re.IGNORECASE,
)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:a-z0-9]+", re.IGNORECASE)
DOI_VALUE_RE = re.compile(r"^10\.\d{4,9}/[-._;()/:a-z0-9]+$", re.IGNORECASE)
ARXIV_VALUE_RE = re.compile(
    r"^(?:[a-z-]+(?:\.[a-z]{2})?/\d{7}|\d{4}\.\d{4,5})$", re.IGNORECASE
)
TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".txt"}


def normalize_arxiv(value: str) -> str:
    """Return an arXiv identifier without URL prefix or version suffix."""
    normalized = value.strip().lower()
    normalized = re.sub(
        r"^https?://(?:export\.)?arxiv\.org/(?:abs|pdf)/", "", normalized)
    normalized = re.sub(r"^arxiv\s*:\s*", "", normalized)
    normalized = normalized.removesuffix(".pdf")
    return re.sub(r"v\d+$", "", normalized)


def normalize_doi(value: str) -> str:
    """Return a lowercase DOI without a resolver prefix or prose punctuation."""
    normalized = value.strip().lower()
    normalized = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", normalized)
    normalized = re.sub(r"^doi\s*:\s*", "", normalized)
    normalized = normalized.rstrip(".,;:]>}")
    while normalized.endswith(")") and normalized.count(")") > normalized.count("("):
        normalized = normalized[:-1]
    return normalized


def _record_error(errors: list[str], location: str, message: str) -> None:
    errors.append(f"{location}: {message}")


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: object, *, allow_empty: bool = True) -> bool:
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(_nonempty_string(item) for item in value)
    )


def _https_url(value: object) -> bool:
    if not _nonempty_string(value) or any(char.isspace() for char in str(value)):
        return False
    try:
        parsed = urlsplit(str(value))
        hostname = parsed.hostname
        parsed.port
    except ValueError:
        return False
    if not hostname:
        return False
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        labels = hostname.rstrip(".").split(".")
        if not labels or any(
            not re.fullmatch(
                r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label, re.IGNORECASE
            )
            for label in labels
        ):
            return False
    return (
        parsed.scheme == "https"
        and bool(parsed.netloc)
        and parsed.username is None
        and parsed.password is None
    )


def _tracked_candidate_modes(repo_root: Path) -> dict[str, str]:
    proc = subprocess.run(
        ["git", "ls-files", "--stage", "-z"],
        cwd=repo_root,
        capture_output=True,
        check=True,
    )
    modes = {}
    for item in proc.stdout.split(b"\0"):
        if not item:
            continue
        metadata, raw_path = item.split(b"\t", 1)
        mode = metadata.split(b" ", 1)[0].decode("ascii")
        path = raw_path.decode("utf-8").replace("\\", "/")
        modes[path] = mode
    return modes


def _valid_repo_path(
    value: object, repo_root: Path, tracked_modes: dict[str, str]
) -> tuple[bool, str]:
    if not _nonempty_string(value):
        return False, "must be a nonempty repository-relative path"
    raw = str(value)
    rel = PurePosixPath(raw)
    if "\\" in raw or rel.is_absolute() or ".." in rel.parts:
        return False, "must use a safe POSIX repository-relative path"
    if raw not in tracked_modes:
        return False, "is not an index-visible tracked candidate file"
    if tracked_modes[raw] not in {"100644", "100755"}:
        return False, "index entry is not a regular file"
    if not (repo_root / Path(*rel.parts)).is_file():
        return False, "is not a regular file in the candidate tree"
    return True, ""


def validate_registry(data: object, repo_root: Path = REPO_ROOT) -> list[str]:
    """Return deterministic validation errors for a decoded registry."""
    errors: list[str] = []
    try:
        tracked_modes = _tracked_candidate_modes(repo_root)
    except (OSError, subprocess.CalledProcessError) as exc:
        return [f"registry: could not inspect the Git candidate index: {exc}"]
    if not isinstance(data, dict):
        return ["registry: top level must be an object"]
    if data.get("schema_version") != 1:
        _record_error(errors, "registry", "schema_version must equal 1")
    sources = data.get("sources")
    if not isinstance(sources, list):
        _record_error(errors, "registry", "sources must be an array")
        return errors

    citekeys: dict[str, int] = {}
    identities: dict[tuple[str, str], tuple[int, str]] = {}
    required = {
        "citekey",
        "title",
        "authors",
        "year",
        "identifiers",
        "authoritative_url",
        "identity_verification",
        "search_trail",
        "relevance",
        "limitations",
        "repository_usages",
    }

    for index, source in enumerate(sources):
        loc = f"sources[{index}]"
        if not isinstance(source, dict):
            _record_error(errors, loc, "must be an object")
            continue
        for field in sorted(required - source.keys()):
            _record_error(errors, loc, f"missing required field {field!r}")
        if "inspection_level" in source:
            _record_error(
                errors,
                loc,
                "inspection_level belongs on each repository usage, not the source",
            )

        citekey = source.get("citekey")
        if not _nonempty_string(citekey) or not CITEKEY_RE.fullmatch(str(citekey)):
            _record_error(errors, loc, "citekey must be stable lowercase ASCII")
        elif citekey in citekeys:
            _record_error(
                errors,
                loc,
                f"duplicate citekey {citekey!r} (first at sources[{citekeys[citekey]}])",
            )
        else:
            citekeys[str(citekey)] = index

        verification = source.get("identity_verification")
        title = source.get("title")
        if not _nonempty_string(title):
            _record_error(errors, loc, "title must be a nonempty string")
        title_key = str(title).strip().casefold() if _nonempty_string(title) else ""
        authors_may_be_unknown = verification is None
        if not _string_list(
            source.get("authors"), allow_empty=authors_may_be_unknown
        ):
            expectation = (
                "a string array (empty only for an unverified lead)"
                if authors_may_be_unknown
                else "a nonempty string array"
            )
            _record_error(errors, loc, f"authors must be {expectation}")

        year = source.get("year")
        if year is not None and (
            isinstance(year, bool) or not isinstance(year, int) or not 1400 <= year <= 2100
        ):
            _record_error(errors, loc, "year must be null or an integer from 1400 to 2100")

        identifiers = source.get("identifiers")
        if not isinstance(identifiers, dict):
            _record_error(errors, loc, "identifiers must be an object")
            identifiers = {}
        unknown_identifiers = set(identifiers) - IDENTIFIER_KEYS
        if unknown_identifiers:
            _record_error(
                errors,
                loc,
                "unsupported identifier keys: " + ", ".join(sorted(unknown_identifiers)),
            )
        for kind, value in identifiers.items():
            if kind not in IDENTIFIER_KEYS:
                continue
            if not _nonempty_string(value):
                _record_error(errors, loc, f"identifier {kind!r} must be nonempty")
                continue
            normalized = (
                normalize_doi(str(value))
                if kind == "doi"
                else normalize_arxiv(str(value))
                if kind == "arxiv"
                else str(value).strip().casefold()
            )
            well_formed = (
                bool(DOI_VALUE_RE.fullmatch(normalized))
                if kind == "doi"
                else bool(ARXIV_VALUE_RE.fullmatch(normalized))
                if kind == "arxiv"
                else normalized.isdigit()
                if kind == "eudml"
                else bool(re.fullmatch(r"[0-9a-z]{4}", normalized))
            )
            if not well_formed:
                _record_error(errors, loc, f"malformed {kind} identifier {value!r}")
                continue
            identity = (kind, normalized)
            if identity in identities:
                previous_index, previous_title = identities[identity]
                label = "conflicting source identity" if previous_title != title_key else "duplicate persistent identifier"
                _record_error(
                    errors,
                    loc,
                    f"{label} {kind}:{normalized} (first at sources[{previous_index}])",
                )
            else:
                identities[identity] = (index, title_key)

        if not _nonempty_string(source.get("relevance")):
            _record_error(errors, loc, "relevance must be a nonempty string")
        limitations = source.get("limitations")
        if not _string_list(limitations):
            _record_error(errors, loc, "limitations must be a string array")
            limitations = []
        search_trail = source.get("search_trail")
        if not _string_list(search_trail):
            _record_error(errors, loc, "search_trail must be a string array")
            search_trail = []
        if year is None and not limitations:
            _record_error(errors, loc, "a null year requires an explicit limitation")

        authoritative_url = source.get("authoritative_url")
        if verification is None:
            if not search_trail:
                _record_error(errors, loc, "an unverified lead requires a search trail")
            if not limitations:
                _record_error(errors, loc, "an unverified lead requires an explicit limitation")
        elif not isinstance(verification, dict):
            _record_error(errors, loc, "identity_verification must be null or an object")
        else:
            if not _https_url(authoritative_url):
                _record_error(errors, loc, "a verified record requires an authoritative HTTPS URL")
            if not _https_url(verification.get("source_url")):
                _record_error(errors, loc, "identity_verification.source_url must be HTTPS")
            raw_date = verification.get("date")
            parsed_date = None
            if isinstance(raw_date, str) and re.fullmatch(
                r"\d{4}-\d{2}-\d{2}", raw_date
            ):
                try:
                    parsed_date = date.fromisoformat(raw_date)
                except ValueError:
                    pass
            if parsed_date is None:
                _record_error(errors, loc, "identity_verification.date must be ISO YYYY-MM-DD")
            elif parsed_date > date.today():
                _record_error(errors, loc, "identity_verification.date cannot be in the future")

        usages = source.get("repository_usages")
        if not isinstance(usages, list):
            _record_error(errors, loc, "repository_usages must be an array")
            continue
        for usage_index, usage in enumerate(usages):
            usage_loc = f"{loc}.repository_usages[{usage_index}]"
            if not isinstance(usage, dict):
                _record_error(errors, usage_loc, "must be an object")
                continue
            for field in ("inspection_level", "source_locator"):
                if field not in usage:
                    _record_error(errors, usage_loc, f"missing required field {field!r}")
            path_ok, path_message = _valid_repo_path(
                usage.get("path"), repo_root, tracked_modes
            )
            if not path_ok:
                _record_error(errors, usage_loc, f"path {path_message}")
            role = usage.get("role")
            if role not in USAGE_ROLES:
                _record_error(
                    errors,
                    usage_loc,
                    "role must be one of " + ", ".join(sorted(USAGE_ROLES)),
                )
            usage_level = usage.get("inspection_level")
            if usage_level not in USAGE_INSPECTION_LEVELS:
                _record_error(
                    errors,
                    usage_loc,
                    "inspection_level must be one of "
                    + ", ".join(sorted(USAGE_INSPECTION_LEVELS)),
                )
            locator = usage.get("source_locator")
            if locator is not None and not _nonempty_string(locator):
                _record_error(errors, usage_loc, "source_locator must be null or nonempty")
            if usage_level == "relevant_passage_inspected" and not _nonempty_string(locator):
                _record_error(
                    errors,
                    usage_loc,
                    "relevant_passage_inspected requires an exact source_locator",
                )
            if role == "background" and verification is None:
                _record_error(errors, usage_loc, "a background citation requires verified identity")
            if role == "novelty_assessment":
                if not search_trail:
                    _record_error(errors, usage_loc, "a novelty assessment requires a search trail")
                if not limitations:
                    _record_error(errors, usage_loc, "a novelty assessment requires explicit search limits")
            if role == "imported_result":
                for field in (
                    "assumptions_scope",
                    "correspondence_note",
                    "unresolved_obligations",
                ):
                    if field not in usage:
                        _record_error(errors, usage_loc, f"missing imported-result field {field!r}")
                if not _nonempty_string(usage.get("assumptions_scope")):
                    _record_error(errors, usage_loc, "assumptions_scope must be explicit")
                if not _nonempty_string(usage.get("correspondence_note")):
                    _record_error(errors, usage_loc, "correspondence_note must be explicit")
                obligations = usage.get("unresolved_obligations")
                if not _string_list(obligations):
                    _record_error(errors, usage_loc, "unresolved_obligations must be a string array")
                    obligations = []
                if locator is None and not obligations:
                    _record_error(errors, usage_loc, "a missing source_locator must remain an unresolved obligation")
                if usage_level != "relevant_passage_inspected" and not obligations:
                    _record_error(
                        errors,
                        usage_loc,
                        "an imported result without relevant-passage inspection must retain an unresolved obligation",
                    )

    return errors


def load_registry(path: Path) -> object:
    """Load a JSON registry, leaving shape validation to validate_registry."""
    return json.loads(path.read_text(encoding="utf-8"))


def _iter_text_files(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            yield path
        elif path.is_dir():
            for candidate in sorted(path.rglob("*")):
                if candidate.is_file() and candidate.suffix.lower() in TEXT_SUFFIXES:
                    yield candidate


def inventory_identifiers(paths: Iterable[Path], repo_root: Path = REPO_ROOT) -> dict:
    """Inventory DOI and arXiv line mentions, deduplicated within each line."""
    counts = {"doi": Counter(), "arxiv": Counter()}
    locations: dict[str, dict[str, list[dict[str, object]]]] = {
        "doi": defaultdict(list),
        "arxiv": defaultdict(list),
    }
    for path in _iter_text_files(paths):
        try:
            rel = path.resolve().relative_to(repo_root.resolve()).as_posix()
        except ValueError:
            rel = path.resolve().as_posix()
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(), 1
        ):
            per_line = {
                "doi": {normalize_doi(match.group(0)) for match in DOI_RE.finditer(line)},
                "arxiv": {
                    normalize_arxiv(match.group("identifier"))
                    for match in ARXIV_RE.finditer(line)
                },
            }
            for kind, identifiers in per_line.items():
                for identifier in sorted(identifiers):
                    counts[kind][identifier] += 1
                    locations[kind][identifier].append({"path": rel, "line": line_number})
    result = {}
    for kind in ("arxiv", "doi"):
        records = [
            {
                "identifier": identifier,
                "line_mentions": counts[kind][identifier],
                "locations": locations[kind][identifier],
            }
            for identifier in sorted(counts[kind])
        ]
        result[kind] = {
            "line_mentions": sum(counts[kind].values()),
            "unique": len(records),
            "records": records,
        }
    return result


def _resolve_paths(raw_paths: list[str] | None) -> list[Path]:
    if not raw_paths:
        return [REPO_ROOT / "claims", REPO_ROOT / "docs"]
    resolved = []
    for raw in raw_paths:
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = REPO_ROOT / candidate
        resolved.append(candidate)
    return resolved


def command_validate(args: argparse.Namespace) -> int:
    registry_path = Path(args.registry)
    if not registry_path.is_absolute():
        registry_path = REPO_ROOT / registry_path
    try:
        data = load_registry(registry_path)
        errors = validate_registry(data)
    except (OSError, json.JSONDecodeError) as exc:
        errors = [f"registry: could not load {registry_path}: {exc}"]
        data = None
    payload = {
        "ok": not errors,
        "registry": registry_path.resolve().relative_to(REPO_ROOT).as_posix()
        if registry_path.resolve().is_relative_to(REPO_ROOT)
        else registry_path.resolve().as_posix(),
        "sources": len(data.get("sources", [])) if isinstance(data, dict) else 0,
        "errors": errors,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    elif errors:
        print("literature registry INVALID", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print(f"literature registry valid: {payload['sources']} sources")
    return 1 if errors else 0


def command_inventory(args: argparse.Namespace) -> int:
    paths = _resolve_paths(args.paths)
    missing = [path for path in paths if not path.exists()]
    if missing:
        for path in missing:
            print(f"inventory path does not exist: {path}", file=sys.stderr)
        return 1
    payload = inventory_identifiers(paths)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        for kind in ("arxiv", "doi"):
            print(
                f"{kind}: {payload[kind]['line_mentions']} line mentions, "
                f"{payload[kind]['unique']} unique identifiers"
            )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate the source registry")
    validate.add_argument(
        "--registry",
        default=str(DEFAULT_REGISTRY.relative_to(REPO_ROOT)),
        help="registry path relative to the repository root",
    )
    validate.add_argument("--json", action="store_true", help="emit JSON")
    validate.set_defaults(func=command_validate)

    inventory = subparsers.add_parser(
        "inventory", help="inventory DOI and arXiv identifiers without network access"
    )
    inventory.add_argument(
        "--paths",
        nargs="+",
        help="files or directories; defaults to claims and docs",
    )
    inventory.add_argument("--json", action="store_true", help="emit JSON")
    inventory.set_defaults(func=command_inventory)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
