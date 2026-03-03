"""Nox sessions for partner-certification-checker automation."""

from pathlib import Path

import nox
import yaml


@nox.session
def validate_dependencies(session: nox.Session):
    """Validate that galaxy.yml dependencies are listed in requirements.yml.

    When a collection declares dependencies in galaxy.yml, ansible-lint needs a
    requirements.yml file to discover and install those dependencies. This session
    checks for that and gives a clear, actionable error message before ansible-lint
    runs.

    Usage:
        nox -s validate_dependencies              # Check current directory
        nox -s validate_dependencies -- /path     # Check specific directory
    """
    # Get collection_root from posargs, default to "."
    collection_root = Path(session.posargs[0] if session.posargs else ".")

    galaxy_path = collection_root / "galaxy.yml"
    requirements_path = collection_root / "requirements.yml"

    if not galaxy_path.is_file():
        session.error(f"ERROR: {galaxy_path} not found.")

    galaxy = yaml.safe_load(galaxy_path.read_text(encoding="utf-8"))

    deps = galaxy.get("dependencies", {})
    if not deps:
        return

    print(f"Validating {len(deps)} collection dependencies")

    if not requirements_path.is_file():
        deps_list = "\n".join(
            f"  - Collection '{dep}' is listed as a dependency in {galaxy_path} "
            f"but there is no requirements.yml file."
            for dep in deps
        )
        session.error(
            f"ERROR: {requirements_path} not found but {galaxy_path} declares dependencies.\n"
            f"{deps_list}\n\n"
            f"All collection dependencies must be listed in {requirements_path} "
            f"so that ansible-lint can discover and install them."
        )

    reqs = yaml.safe_load(requirements_path.read_text(encoding="utf-8")) or {}

    req_collections = {
        entry if isinstance(entry, str) else entry["name"]
        for entry in reqs.get("collections", [])
        if isinstance(entry, str) or (isinstance(entry, dict) and "name" in entry)
    }

    missing = set(deps) - req_collections

    if missing:
        deps_list = "\n".join(f"  - {dep}" for dep in missing)
        session.error(
            f"ERROR: The following dependencies from {galaxy_path} "
            f"are missing from {requirements_path}:\n{deps_list}\n\n"
            f"All collection dependencies must be listed in {requirements_path} "
            f"so that ansible-lint can discover and install them."
        )

    print("✓ All dependencies validated")
