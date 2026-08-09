from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import types
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
AUDIT_PATH = REPO_ROOT / "audit_component20_intrinsic_zero_diagonal_dvr_atlas_candidate.py"


def run_git(root: pathlib.Path, *args: str) -> str:
    return subprocess.run(
        ("git", *args),
        cwd=root,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
        timeout=15,
    ).stdout.strip()


def load_audit():
    spec = importlib.util.spec_from_file_location("component20_guard_audit", AUDIT_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load Component20 audit")
    module = importlib.util.module_from_spec(spec)
    previous_z3 = sys.modules.get("z3")
    sys.modules["z3"] = types.ModuleType("z3")
    try:
        spec.loader.exec_module(module)
    finally:
        if previous_z3 is None:
            del sys.modules["z3"]
        else:
            sys.modules["z3"] = previous_z3
    return module


class Component20SourceGuardTests(unittest.TestCase):
    def test_repository_checkpoint_guard_is_live(self) -> None:
        audit = load_audit()
        self.assertTrue(audit.frozen_component_sources_unchanged())
        self.assertEqual(len(audit.HISTORICAL_COMPONENT_SOURCES), 4)
        self.assertEqual(len(audit.CURRENT_COMPONENT_SOURCES), 4)
        self.assertTrue(all("/" in path for path, _ in audit.CURRENT_COMPONENT_SOURCES))

    def test_nested_source_mutation_fails_closed(self) -> None:
        audit = load_audit()
        old_paths = tuple(path for path, _ in audit.HISTORICAL_COMPONENT_SOURCES)
        current_paths = tuple(path for path, _ in audit.CURRENT_COMPONENT_SOURCES)

        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            run_git(root, "init", "--quiet")
            run_git(root, "config", "user.email", "guard@example.invalid")
            run_git(root, "config", "user.name", "Component Guard Test")

            for index, relative in enumerate(old_paths):
                (root / relative).write_text(f"historical {index}\n", encoding="utf-8")
            run_git(root, "add", "-A")
            run_git(root, "commit", "--quiet", "-m", "historical")
            historical_commit = run_git(root, "rev-parse", "HEAD")
            historical_sources = tuple(
                (relative, run_git(root, "rev-parse", f"HEAD:{relative}"))
                for relative in old_paths
            )

            for index, (old, current) in enumerate(zip(old_paths, current_paths)):
                target = root / current
                target.parent.mkdir(parents=True, exist_ok=True)
                (root / old).replace(target)
                target.write_text(f"rewritten {index}\n", encoding="utf-8")
            run_git(root, "add", "-A")
            run_git(root, "commit", "--quiet", "-m", "rewrite checkpoint")
            checkpoint = run_git(root, "rev-parse", "HEAD")
            current_sources = tuple(
                (relative, run_git(root, "rev-parse", f"HEAD:{relative}"))
                for relative in current_paths
            )

            self.assertTrue(
                audit._component_sources_unchanged(
                    root,
                    historical_commit,
                    checkpoint,
                    historical_sources,
                    current_sources,
                )
            )
            (root / current_paths[0]).write_text("mutated\n", encoding="utf-8")
            self.assertFalse(
                audit._component_sources_unchanged(
                    root,
                    historical_commit,
                    checkpoint,
                    historical_sources,
                    current_sources,
                )
            )


if __name__ == "__main__":
    unittest.main()
