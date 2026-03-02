"""Validate that galaxy.yml dependencies are listed in requirements.yml.

When a collection declares dependencies in galaxy.yml, ansible-lint needs a
requirements.yml file to discover and install those dependencies. This script
checks for that and gives a clear, actionable error message before ansible-lint
runs.
"""

import argparse
import os
import sys

import yaml


def main():
    parser = argparse.ArgumentParser(
        description="Validate that galaxy.yml dependencies are listed in requirements.yml.",
    )
    parser.add_argument(
        "collection_root",
        nargs="?",
        default=".",
        help="Path to the collection root directory (where galaxy.yml lives). Defaults to '.'",
    )
    args = parser.parse_args()
    collection_root = args.collection_root

    galaxy_path = os.path.join(collection_root, "galaxy.yml")
    requirements_path = os.path.join(collection_root, "requirements.yml")

    if not os.path.isfile(galaxy_path):
        print(f"ERROR: {galaxy_path} not found.")
        sys.exit(1)

    with open(galaxy_path) as f:
        galaxy = yaml.safe_load(f)

    deps = galaxy.get("dependencies") or {}
    if not deps:
        print(
            f"No dependencies declared in {galaxy_path}, skipping requirements.yml check."
        )
        return

    print(f"Found {len(deps)} dependency(ies) in {galaxy_path}: {list(deps.keys())}")

    if not os.path.isfile(requirements_path):
        print(
            f"ERROR: {requirements_path} not found but {galaxy_path} declares dependencies."
        )
        for dep in deps:
            print(
                f"  - Collection '{dep}' is listed as a dependency in "
                f"{galaxy_path} but there is no requirements.yml file."
            )
        print(
            "\nAll collection dependencies must be listed in "
            f"{requirements_path} so that ansible-lint can discover "
            "and install them."
        )
        sys.exit(1)

    with open(requirements_path) as f:
        reqs = yaml.safe_load(f) or {}

    req_collections = set()
    for entry in reqs.get("collections") or []:
        if isinstance(entry, str):
            req_collections.add(entry)
        elif isinstance(entry, dict) and "name" in entry:
            req_collections.add(entry["name"])

    missing = [dep for dep in deps if dep not in req_collections]

    if missing:
        print(
            f"ERROR: The following dependencies from {galaxy_path} are "
            f"missing from {requirements_path}:"
        )
        for dep in missing:
            print(f"  - {dep}")
        print(
            "\nAll collection dependencies must be listed in "
            f"{requirements_path} so that ansible-lint can discover "
            "and install them."
        )
        sys.exit(1)

    print(f"All {galaxy_path} dependencies are present in {requirements_path}.")


if __name__ == "__main__":
    main()
